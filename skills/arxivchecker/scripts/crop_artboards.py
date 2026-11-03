#!/usr/bin/env python3
"""Crop explicit boxes from one source image without modifying it.

Box JSON: {"schema_version":1,"preview_width":750,"crops":[{"name":"design","box":[10,20,700,500]}]}.
Omit preview_width for full-resolution pixel coordinates. Requires Pillow to crop.
Review every crop for lost labels and footnotes; coordinates alone cannot do that.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def validate_boxes(document, width, height):
    if document.get("schema_version") != 1 or not isinstance(document.get("crops"), list) or not document["crops"]:
        raise ValueError("expected schema_version 1 and a nonempty crops list")
    preview_width = document.get("preview_width", width)
    if isinstance(preview_width, bool) or not isinstance(preview_width, int) or preview_width <= 0:
        raise ValueError("preview_width must be a positive integer")
    scale = width / preview_width
    selected, names = [], set()
    for crop in document["crops"]:
        if not isinstance(crop, dict):
            raise ValueError("every crop must be an object")
        name = crop.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name) or name in names:
            raise ValueError("crop names must be unique, safe filename stems")
        names.add(name)
        box = crop.get("box")
        if not isinstance(box, list) or len(box) != 4 or any(isinstance(value, bool) or not isinstance(value, int) for value in box):
            raise ValueError(f"{name}: box must contain four integer coordinates")
        left, top, right, bottom = box
        if not (0 <= left < right <= preview_width and 0 <= top < bottom and bottom * scale <= height):
            raise ValueError(f"{name}: box is outside image bounds or empty; no clamping is allowed")
        actual = [round(value * scale) for value in box]
        if not (0 <= actual[0] < actual[2] <= width and 0 <= actual[1] < actual[3] <= height):
            raise ValueError(f"{name}: scaled box is outside image bounds or empty")
        selected.append({"name": name, "box": box, "pixel_box": actual})
    return selected


def crop_image(input_path, box_path, output):
    if output.exists() or output.is_symlink():
        raise ValueError(f"refusing to overwrite {output}; choose a new output directory")
    if not output.parent.is_dir():
        raise ValueError("output parent directory must already exist")
    source_bytes = input_path.read_bytes()
    box_bytes = box_path.read_bytes()
    document = json.loads(box_bytes)
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValueError("cropping needs Pillow in this Python environment; core box checks do not") from exc
    with Image.open(input_path) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise ValueError("choose a single image frame before cropping")
        orientation = source.getexif().get(274, 1)
        if orientation != 1:
            raise ValueError("normalize image orientation before selecting crop coordinates")
        selected = validate_boxes(document, source.width, source.height)
        source.load()
        output.mkdir()
        outputs = {}
        for item in selected:
            target = output / (item["name"] + ".png")
            crop = source.crop(tuple(item["pixel_box"]))
            if crop.mode not in ("1", "L", "LA", "P", "RGB", "RGBA", "I", "I;16"):
                crop = crop.convert("RGB")
            crop.save(target, format="PNG")
            outputs[target.name] = {"sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "size": list(crop.size)}
        dimensions = [source.width, source.height]
    manifest = {
        "schema_version": 1, "input": str(input_path), "input_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "boxes_sha256": hashlib.sha256(box_bytes).hexdigest(), "source_size": dimensions,
        "crops": selected, "outputs": outputs,
        "visual_review": "pending: inspect every crop for clipped labels, footnotes, legends and intended panel boundaries",
    }
    (output / "crop-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="one source raster image, not a PDF")
    parser.add_argument("--boxes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new directory")
    args = parser.parse_args(argv)
    try:
        manifest = crop_image(args.input, args.boxes, args.output)
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"crop error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
