"""Regression coverage for evidence and submission boundaries, using fictional data."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "arxivcheck", ROOT / "skills/arxivchecker/scripts/arxivcheck.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class StudyCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="arxivchecker-test-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name).resolve()
        self.study = self.work / "study"
        self.study.mkdir()
        self.data = {"correct": 8, "n": 10, "cost": 1.25}
        self.results = self.study / "results.json"
        self.save_data()
        self.metric = {"id": "accuracy", "source": "results.json", "pointer": "/correct",
                       "kind": "proportion", "unit": "per problem", "denominator_pointer": "/n"}
        self.spec = {"schema_version": 1, "metrics": [self.metric]}
        self.main = self.study / "main.tex"
        self.main.write_text(
            "\\documentclass{article}\n\\title{Fictional checker fixture}\n"
            "\\author{Example Researcher}\n\\date{}\n\\begin{document}\n"
            "\\maketitle\nThis text is a software test fixture, with no empirical claim.\n"
            "\\end{document}\n", encoding="utf-8")
        self.manifest = {
            "schema_version": 1, "main_tex": "main.tex", "engine": "pdflatex",
            "files": ["main.tex"],
            "authors": [{"name": "Example Researcher", "affiliation": "Fictional Laboratory"}],
            "human_review": ["Confirm names, claims, references, visual layout and permission."]}

    def save_data(self):
        self.results.write_text(json.dumps(self.data), encoding="utf-8")

    def extract(self):
        return checker.extract(self.study, self.spec)["metrics"][0]

    def test_source_trace_and_known_wilson_interval(self):
        result = self.extract()
        self.assertEqual(result["source_sha256"], checker.sha256(self.results))
        self.assertEqual(result["pointer"], "/correct")
        self.assertEqual(result["value"], 8)
        self.assertEqual(result["denominator"], 10)
        self.assertAlmostEqual(result["rate"], 0.8)
        self.assertAlmostEqual(result["wilson95"][0], 0.4901624715, places=9)
        self.assertAlmostEqual(result["wilson95"][1], 0.9433178485, places=9)

    def test_renamed_series_fails_instead_of_disappearing(self):
        self.data["renamed_correct"] = self.data.pop("correct")
        self.save_data()
        with self.assertRaisesRegex(ValueError, "missing data"):
            self.extract()

    def test_zero_and_complete_successes_remain_valid(self):
        for correct in [0, 10]:
            with self.subTest(correct=correct):
                self.data["correct"] = correct
                self.save_data()
                item = self.extract()
                self.assertEqual(item["rate"], correct / 10)
                self.assertTrue(0 <= item["wilson95"][0] <= item["wilson95"][1] <= 1)

    def test_invalid_denominators_and_counts(self):
        for numerator, denominator in [(1, 0), (1, -1), (11, 10), (-1, 10),
                                       (1.5, 10), (1, 10.0), (True, 10), (1, True), (1, 10 ** 300)]:
            with self.subTest(numerator=numerator, denominator=denominator):
                self.data.update(correct=numerator, n=denominator)
                self.save_data()
                with self.assertRaises(ValueError):
                    self.extract()

    def test_non_numeric_bool_nonfinite_and_object_values_fail(self):
        self.metric.update(kind="number", pointer="/cost")
        for value in [True, False, "1.25", None, {}, [], float("nan"), float("inf")]:
            with self.subTest(value=repr(value)):
                self.data["cost"] = value
                self.save_data()
                with self.assertRaises(ValueError):
                    self.extract()

    def test_duplicate_json_keys_are_rejected(self):
        self.results.write_text('{"correct":8,"correct":9,"n":10}')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            self.extract()

    def test_unrepresentable_large_number_is_rejected_cleanly(self):
        self.metric.update(kind="number", pointer="/cost")
        self.data["cost"] = 10 ** 1000
        self.save_data()
        with self.assertRaisesRegex(ValueError, "finite number"):
            self.extract()

    def test_package_refuses_source_changed_after_static_check(self):
        original = checker.check
        def changed(root, manifest):
            result = original(root, manifest)
            self.main.write_text(self.main.read_text() + "\n% concurrent edit\n")
            return result
        archive = self.work / "changed.tar.gz"
        with patch.object(checker, "check", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "source changed"):
                checker.package(self.study, self.manifest, archive)
        self.assertFalse(archive.exists())

    def test_unit_is_mandatory(self):
        for unit in [None, "", "   "]:
            with self.subTest(unit=unit):
                self.metric["unit"] = unit
                with self.assertRaisesRegex(ValueError, "unit"):
                    self.extract()

    def test_duplicate_metric_ids_fail(self):
        self.spec["metrics"].append(copy.deepcopy(self.metric))
        with self.assertRaisesRegex(ValueError, "duplicate metric"):
            checker.extract(self.study, self.spec)

    def test_cost_scope_is_preserved_and_must_be_nonempty(self):
        self.metric.update(kind="number", pointer="/cost", unit="USD model calls",
                           cost_scope="Assumed model prices only; excludes labor and setup.")
        self.assertEqual(self.extract()["cost_scope"], self.metric["cost_scope"])
        self.metric["cost_scope"] = ""
        with self.assertRaisesRegex(ValueError, "cost_scope"):
            self.extract()

    def test_escaped_pointer_and_array_index(self):
        self.data = {"a/b": {"c~d": [5, 6]}}
        self.save_data()
        self.metric.update(kind="number", pointer="/a~1b/c~0d/1", unit="seconds")
        self.assertEqual(self.extract()["value"], 6)
        for pointer in ["/a~2b", "/a~1b/c~0d/-1", "/a~1b/c~0d/01", "/a~1b/c~0d/2"]:
            with self.subTest(pointer=pointer):
                self.metric["pointer"] = pointer
                with self.assertRaises(ValueError):
                    self.extract()

    def test_explicit_allowlist_blocks_traversal_unsafe_names_and_symlinks(self):
        outside = self.work / "outside.tex"
        outside.write_text("outside source")
        link = self.study / "link.tex"
        link.symlink_to(outside)
        unsafe = self.study / "has space.tex"
        unsafe.write_text("unsafe filename")
        for bad in ["../outside.tex", str(outside), "has space.tex", "link.tex", "missing.tex"]:
            with self.subTest(path=bad):
                m = copy.deepcopy(self.manifest)
                m["files"].append(bad)
                with self.assertRaises(ValueError):
                    checker.load_manifest(self.study, m)

    def test_directory_symlink_cannot_import_external_results(self):
        external = self.work / "external"
        external.mkdir()
        (external / "data.json").write_text('{"correct":8,"n":10}')
        (self.study / "linked").symlink_to(external, target_is_directory=True)
        self.metric["source"] = "linked/data.json"
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.extract()

    def test_inventory_excludes_private_and_hidden_paths(self):
        for name in [".env", "credentials", "id_rsa", ".notes"]:
            (self.study / name).write_text("private test value")
        (self.study / ".git").mkdir()
        (self.study / ".git/config").write_text("private git config")
        (self.study / "cache-link").symlink_to(self.results)
        report = checker.inventory(self.study)
        self.assertEqual({row["path"] for row in report["files"]}, {"main.tex", "results.json"})
        self.assertEqual(report["excluded"], [{"path": "cache-link", "reason": "symlink"}])
        self.assertNotIn("private test value", json.dumps(report))

    def test_literal_graphics_dependency_does_not_count_as_nonliteral_input(self):
        # A .pdf byte fixture is sufficient: static checking must not parse it.
        (self.study / "diagram.pdf").write_bytes(b"fictional dependency fixture")
        self.main.write_text("\\includegraphics{diagram}\n")
        self.manifest["files"].append("diagram.pdf")
        self.assertEqual(checker.check(self.study, self.manifest)["errors"], [])

    def test_missing_input_graphic_and_bibliography_are_reported(self):
        self.main.write_text("\\input{methods}\n\\includegraphics{figure}\n\\bibliography{sources}\n")
        errors = checker.check(self.study, self.manifest)["errors"]
        for name in ["methods", "figure", "sources"]:
            self.assertTrue(any("dependency missing" in error and name in error for error in errors))

    def test_bib_source_is_valid_even_when_local_no_bibliography_profile_cannot_build_it(self):
        self.main.write_text("\\bibliography{references}\n")
        (self.study / "references.bib").write_text("% Fictional bibliography fixture\n")
        self.manifest["files"].append("references.bib")
        # Official arXiv can process .bib; local three-pass pdflatex is narrower.
        self.assertEqual(checker.check(self.study, self.manifest)["errors"], [])

    def test_prepared_bbl_does_not_require_original_bib_source(self):
        self.main.write_text("\\bibliography{references}\n")
        (self.study / "main.bbl").write_text("% Empty fictional build fixture\n")
        self.manifest["files"].append("main.bbl")
        self.assertEqual(checker.check(self.study, self.manifest)["errors"], [])

    def test_human_affiliation_is_not_invented_to_satisfy_machine_schema(self):
        self.manifest["authors"] = [{"name": "Example Researcher"}]
        self.assertEqual(checker.check(self.study, self.manifest)["errors"], [])

    def test_legitimate_todo_word_is_review_finding_not_policy_error(self):
        self.main.write_text("\\title{TODO: A Task Management Protocol}\\begin{document}"
                             "We study TODO list prioritization.\\end{document}")
        report = checker.check(self.study, self.manifest)
        self.assertEqual(report["errors"], [])
        self.assertTrue(report["warnings"], "ambiguous editing markers should invite review")

    def test_braceless_and_dot_relative_tex_inputs_are_not_policy_errors(self):
        (self.study / "methods.tex").write_text("Fictional methods fixture.")
        self.manifest["files"].append("methods.tex")
        for command in ["\\input methods.tex\n", "\\input{./methods}\n", "\\input  {methods}\n"]:
            with self.subTest(command=command):
                self.main.write_text(command)
                self.assertEqual(checker.check(self.study, self.manifest)["errors"], [])

    def test_macro_and_graphicspath_dependencies_need_review_not_rejection(self):
        figures = self.study / "figures"
        figures.mkdir()
        (figures / "diagram.pdf").write_bytes(b"fictional dependency fixture")
        self.manifest["files"].append("figures/diagram.pdf")
        for command in ["\\graphicspath{{figures/}}\\includegraphics{diagram}\n",
                        "\\newcommand{\\figurefile}{figures/diagram.pdf}"
                        "\\includegraphics{\\figurefile}\n",
                        "\\includegraphics*[width=2cm]{figures/diagram.pdf}\n"]:
            with self.subTest(command=command):
                self.main.write_text(command)
                report = checker.check(self.study, self.manifest)
                self.assertEqual(report["errors"], [])

    def test_custom_class_and_nested_main_are_not_rejected(self):
        nested = self.study / "source"
        nested.mkdir()
        self.main.unlink()
        (nested / "main.tex").write_text("\\documentclass{custom}\\input{source/methods}\n")
        (nested / "methods.tex").write_text("Fictional section fixture.")
        (self.study / "custom.cls").write_text("\\NeedsTeXFormat{LaTeX2e}"
                                                "\\ProvidesClass{custom}\\LoadClass{article}\n")
        self.manifest.update(main_tex="source/main.tex",
                             files=["source/main.tex", "source/methods.tex", "custom.cls"])
        self.assertEqual(checker.check(self.study, self.manifest)["errors"], [])

    def test_unsupported_engine_message_describes_local_scope(self):
        for engine in ["xelatex", "latex", "tex", "pdftex"]:
            with self.subTest(engine=engine):
                self.manifest["engine"] = engine
                try:
                    report = checker.check(self.study, self.manifest)
                except ValueError as error:
                    self.assertIn("local", str(error).lower())
                    self.assertNotIn("ineligible", str(error).lower())
                else:
                    self.assertEqual(report["errors"], [])

    def test_supported_arxiv_engine_outside_local_profile_is_not_an_eligibility_failure(self):
        self.manifest["engine"] = "xelatex"
        output = self.work / "xelatex-profile"
        report = checker.preflight(self.study, self.manifest, output)
        self.assertEqual(report["status"], "not-run-unsupported-local-profile")
        self.assertEqual(report["arxiv_eligibility"], "not-assessed")
        self.assertFalse(output.exists(), "unsupported profile should not create a misleading build")

    def test_generic_check_explicitly_does_not_assess_arxiv_eligibility(self):
        report = checker.check(self.study, self.manifest)
        self.assertEqual(report["arxiv_eligibility"], "not-assessed")
        self.assertTrue(report["scope"])

    def test_stale_build_artifacts_cannot_enter_source_archive(self):
        for name in ["main.pdf", "main.aux", "main.log", "main.fls", "main.toc", "main.out"]:
            with self.subTest(path=name):
                (self.study / name).write_text("stale fixture")
                m = copy.deepcopy(self.manifest)
                m["files"].append(name)
                with self.assertRaisesRegex(ValueError, "generated build artifact"):
                    checker.load_manifest(self.study, m)

    def test_required_generated_inputs_and_frozen_cache_are_retained(self):
        names = ["index.ind", "terms.gls", "symbols.nls", "results.out", "_minted/code.pygtex"]
        for name in names:
            path = self.study / name
            path.parent.mkdir(exist_ok=True)
            path.write_text("Fictional required-input fixture.\n")
        self.manifest["files"].extend(names)
        self.assertEqual(checker.check(self.study, self.manifest)["errors"], [])
        archive = self.work / "inputs.tar.gz"
        checker.package(self.study, self.manifest, archive)
        with tarfile.open(archive) as package:
            self.assertTrue(set(names).issubset(package.getnames()))

    def test_nonliteral_input_and_remaining_placeholders_trigger_review(self):
        self.main.write_text("\\input outside.tex\nREPLACE_ME\n")
        report = checker.check(self.study, self.manifest)
        findings = report["errors"] + report["warnings"]
        self.assertTrue(any("input" in finding or "dependency" in finding for finding in findings))
        self.assertTrue(any("placeholder" in finding or "marker" in finding for finding in findings))

    def test_archive_is_deterministic_and_contains_only_allowlist(self):
        a, b = self.work / "first.tar.gz", self.work / "second.tar.gz"
        one = checker.package(self.study, self.manifest, a)
        two = checker.package(self.study, self.manifest, b)
        self.assertEqual(a.read_bytes(), b.read_bytes())
        self.assertEqual(one["archive_sha256"], two["archive_sha256"])
        self.assertEqual(one["status"], "packaged-unreviewed")
        with tarfile.open(a) as archive:
            self.assertEqual(archive.getnames(), ["main.tex"])
            self.assertEqual(archive.extractfile("main.tex").read(), self.main.read_bytes())
        sidecar = checker.read_json(Path(str(a) + ".manifest.json"))
        self.assertEqual(sidecar["files"][0]["sha256"], checker.sha256(self.main))
        self.assertTrue(sidecar["human_review"])

    def test_no_output_or_sidecar_overwrites(self):
        archive = self.work / "paper.tar.gz"
        archive.write_bytes(b"existing archive")
        with self.assertRaisesRegex(ValueError, "already exists"):
            checker.package(self.study, self.manifest, archive)
        self.assertEqual(archive.read_bytes(), b"existing archive")
        archive.unlink()
        sidecar = Path(str(archive) + ".manifest.json")
        sidecar.write_text("existing sidecar")
        with self.assertRaisesRegex(ValueError, "already exists"):
            checker.package(self.study, self.manifest, archive)
        self.assertFalse(archive.exists())
        output = self.work / "metrics.json"
        output.write_text("existing metrics")
        with self.assertRaises(FileExistsError):
            checker.write_json({"changed": True}, output)
        self.assertEqual(output.read_text(), "existing metrics")

    def test_failed_static_check_does_not_package(self):
        self.main.write_text("\\input{missing-required-source}\n")
        archive = self.work / "paper.tar.gz"
        result = checker.package(self.study, self.manifest, archive)
        self.assertEqual(result["status"], "fail")
        self.assertFalse(archive.exists())

    @unittest.skipUnless(all(shutil.which(x) for x in ["pdflatex", "pdffonts", "pdfinfo", "pdftotext"]),
                         "local TeX/font/text inspection tools unavailable")
    def test_real_clean_build_embedded_fonts_and_reference_text(self):
        first = self.work / "preflight-first"
        report = checker.preflight(self.study, self.manifest, first)
        self.assertEqual(report["errors"], [], (report, (first / "pass-1.txt").read_text()))
        self.assertEqual(report["status"], "local-preflight-pass")
        self.assertEqual(report["pages"], 1)
        self.assertTrue((first / "fonts.txt").exists())
        second = self.work / "preflight-reference"
        result = checker.preflight(self.study, self.manifest, second, first / "source/main.pdf")
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["reference_text_matches"])
        self.assertTrue(result["reference_pages_match"])
        self.assertFalse((self.study / "main.pdf").exists())

    @unittest.skipUnless(all(shutil.which(x) for x in ["pdflatex", "pdffonts", "pdfinfo", "pdftotext"]),
                         "local TeX/font/text inspection tools unavailable")
    def test_preflight_wont_write_into_study_or_existing_directory(self):
        alias = self.work / "study-alias"
        alias.symlink_to(self.study, target_is_directory=True)
        for output in [self.study / "build", self.work, alias / "build"]:
            with self.subTest(output=output):
                with self.assertRaisesRegex(ValueError, "new directory outside"):
                    checker.preflight(self.study, self.manifest, output)


if __name__ == "__main__":
    unittest.main()
