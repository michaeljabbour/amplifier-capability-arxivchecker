#!/usr/bin/env python3
"""Draw selected extracted metrics as vector PDF plus a PNG review copy.

Requires matplotlib only for rendering. This checks the shape of extracted data,
not the validity of the study. The caller must explicitly name every series.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

COLORS = ("#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#000000")


def finite_number(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{field} must be a finite number")
    return value


def wilson(k, n):
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0.0, center - half), min(1.0, center + half)]


def select_metrics(document, series):
    """Fail on absent or ambiguous series, mismatched units, or bad intervals."""
    if document.get("schema_version") != 1 or not isinstance(document.get("metrics"), list):
        raise ValueError("expected schema_version 1 and a metrics list")
    if not series or len(set(series)) != len(series):
        raise ValueError("name one or more distinct --series IDs explicitly")
    by_id = {}
    for metric in document["metrics"]:
        if not isinstance(metric, dict) or not isinstance(metric.get("id"), str) or not metric["id"]:
            raise ValueError("every metric needs a nonempty id")
        if metric["id"] in by_id:
            raise ValueError(f"duplicate metric id: {metric['id']}")
        by_id[metric["id"]] = metric
    missing = [key for key in series if key not in by_id]
    if missing:
        raise ValueError("missing required series: " + ", ".join(missing))
    selected = []
    for key in series:
        metric = dict(by_id[key])
        for field in ("unit", "source", "source_sha256", "pointer"):
            if not isinstance(metric.get(field), str) or (field != "pointer" and not metric[field].strip()):
                raise ValueError(f"{key}: missing {field}")
        if len(metric["source_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in metric["source_sha256"]):
            raise ValueError(f"{key}: source_sha256 must be a lowercase SHA-256 digest")
        if metric["kind"] not in ("number", "proportion"):
            raise ValueError(f"{key}: kind must be number or proportion")
        value = finite_number(metric.get("value"), f"{key}.value")
        if metric["kind"] == "proportion":
            denominator = finite_number(metric.get("denominator"), f"{key}.denominator")
            if not isinstance(value, int) or not isinstance(denominator, int) or not 0 <= value <= denominator or denominator <= 0:
                raise ValueError(f"{key}: a proportion needs integer successes and a positive integer denominator")
            expected_rate = value / denominator
            rate = finite_number(metric.get("rate"), f"{key}.rate")
            if not math.isclose(rate, expected_rate, rel_tol=1e-10, abs_tol=1e-12):
                raise ValueError(f"{key}: rate disagrees with value / denominator")
            interval = metric.get("wilson95")
            expected_interval = wilson(value, denominator)
            if not isinstance(interval, list) or len(interval) != 2:
                raise ValueError(f"{key}: missing Wilson 95% interval")
            for actual, expected in zip(interval, expected_interval):
                finite_number(actual, f"{key}.wilson95")
                if not math.isclose(actual, expected, rel_tol=1e-5, abs_tol=1e-7):
                    raise ValueError(f"{key}: interval disagrees with a Wilson 95% interval")
        selected.append(metric)
    if len({(metric["kind"], metric["unit"]) for metric in selected}) != 1:
        raise ValueError("all selected series must share one kind and unit; use separate figures otherwise")
    return selected


def render(input_path, series, output):
    source_bytes = input_path.read_bytes()
    selected = select_metrics(json.loads(source_bytes), series)
    if output.suffix.lower() != ".pdf":
        raise ValueError("--output must end in .pdf")
    png = output.with_suffix(".png")
    record_path = output.with_suffix(".figure.json")
    for target in (output, png, record_path):
        if target.exists() or target.is_symlink():
            raise ValueError(f"refusing to overwrite {target}")
    if not output.parent.is_dir():
        raise ValueError("output parent directory must already exist")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.ticker import PercentFormatter
    except ImportError as exc:
        raise ValueError("rendering needs matplotlib in this Python environment; core checks do not") from exc
    matplotlib.rcParams.update({
        "font.family": "serif", "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix", "font.size": 8, "axes.labelsize": 8,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "pdf.fonttype": 42,
        "axes.spines.top": False, "axes.spines.right": False,
    })
    fig, ax = plt.subplots(figsize=(6.5, max(2.0, 0.38 * len(selected) + 0.8)), layout="constrained")
    proportion = selected[0]["kind"] == "proportion"
    for index, metric in enumerate(selected):
        y = len(selected) - index - 1
        color = COLORS[int(hashlib.sha256(metric["id"].encode()).hexdigest()[:8], 16) % len(COLORS)]
        if proportion:
            value = metric["rate"]
            low, high = metric["wilson95"]
            # At k=0 or k=n, rounding can move a bound a few ulps past the estimate.
            ax.errorbar(value, y, xerr=[[max(0, value - low)], [max(0, high - value)]],
                        fmt="o", color=color, capsize=2.5, markersize=4, linewidth=0.8)
        else:
            ax.scatter(metric["value"], y, color=color, s=22)
    labels = [metric["id"] + (f" ({metric['value']}/{metric['denominator']})" if proportion else "") for metric in selected]
    ax.set_yticks(list(range(len(selected) - 1, -1, -1)), labels)
    ax.set_xlabel(selected[0]["unit"] + ("; Wilson 95% intervals" if proportion else ""))
    ax.grid(axis="x", color="#dddddd", linewidth=0.4)
    ax.set_axisbelow(True)
    ax.set_ylim(-0.6, len(selected) - 0.4)
    if proportion:
        ax.set_xlim(-0.02, 1.02)
        ax.xaxis.set_major_formatter(PercentFormatter(1.0))
    fig.savefig(output, format="pdf", metadata={"Title": "Study metrics for human review", "CreationDate": None, "ModDate": None})
    fig.savefig(png, dpi=180)
    plt.close(fig)
    record = {
        "schema_version": 1,
        "input": str(input_path), "input_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "series": selected, "outputs": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in (output, png)},
        "visual_review": "pending: inspect PNG at publication size; check labels, intervals, units and all expected series",
        "limits": "Reproduces selected values. Does not validate experimental design, source truth, or justify selection.",
    }
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--series", action="append", required=True, help="required metric id; repeat for each series")
    parser.add_argument("--output", type=Path, required=True, help="new PDF path; PNG and provenance sidecars are also created")
    args = parser.parse_args(argv)
    try:
        record = render(args.input, args.series, args.output)
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"figure error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
