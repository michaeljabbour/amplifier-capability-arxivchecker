"""Regression checks for series omission and silent image clipping failures."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "skills/arxivchecker/scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


figures = load_module("make_figures")
crops = load_module("crop_artboards")


class FigureIntegrityTests(unittest.TestCase):
    def metric(self, key="approach", **overrides):
        item = {"id": key, "value": 8, "unit": "per task", "source": "results.json",
                "source_sha256": "a" * 64, "pointer": "/success", "kind": "proportion",
                "denominator": 10, "rate": 0.8, "wilson95": figures.wilson(8, 10)}
        item.update(overrides)
        return item

    def test_missing_explicit_series_cannot_be_silently_omitted(self):
        with self.assertRaisesRegex(ValueError, "missing required series: renamed"):
            figures.select_metrics({"schema_version": 1, "metrics": [self.metric()]}, ["approach", "renamed"])

    def test_ambiguous_duplicate_series_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate metric id"):
            figures.select_metrics({"schema_version": 1, "metrics": [self.metric(), self.metric()]}, ["approach"])

    def test_per_call_and_per_problem_cannot_share_axis(self):
        doc = {"schema_version": 1, "metrics": [self.metric(), self.metric("other", unit="per call")]}
        with self.assertRaisesRegex(ValueError, "share one kind and unit"):
            figures.select_metrics(doc, ["approach", "other"])

    def test_denominator_rate_and_interval_must_agree(self):
        for change in ({"denominator": 20}, {"rate": 0.9}, {"wilson95": [0.7, 0.9]}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                figures.select_metrics({"schema_version": 1, "metrics": [self.metric(**change)]}, ["approach"])

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "matplotlib not installed; rendering optional")
    def test_render_includes_pdf_preview_and_source_record(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            source = folder / "metrics.json"
            source.write_text(json.dumps({"schema_version": 1, "metrics": [self.metric()]}))
            record = figures.render(source, ["approach"], folder / "metrics.pdf")
            self.assertTrue((folder / "metrics.pdf").read_bytes().startswith(b"%PDF"))
            self.assertTrue((folder / "metrics.png").read_bytes().startswith(b"\x89PNG"))
            self.assertEqual(record["series"][0]["id"], "approach")
            self.assertIn("pending", record["visual_review"])
            with self.assertRaisesRegex(ValueError, "overwrite"):
                figures.render(source, ["approach"], folder / "metrics.pdf")


class CropIntegrityTests(unittest.TestCase):
    def boxes(self, box, **other):
        return {"schema_version": 1, "crops": [{"name": "design", "box": box}], **other}

    def test_oversized_bottom_is_not_silently_clamped(self):
        with self.assertRaisesRegex(ValueError, "no clamping"):
            crops.validate_boxes(self.boxes([0, 0, 100, 201]), 100, 200)

    def test_scaled_preview_coordinates_are_checked(self):
        selected = crops.validate_boxes(self.boxes([5, 10, 45, 80], preview_width=50), 100, 200)
        self.assertEqual(selected[0]["pixel_box"], [10, 20, 90, 160])
        with self.assertRaisesRegex(ValueError, "no clamping"):
            crops.validate_boxes(self.boxes([5, 10, 45, 101], preview_width=50), 100, 200)

    def test_path_traversal_crop_name_rejected(self):
        document = self.boxes([0, 0, 10, 10])
        document["crops"][0]["name"] = "../secret"
        with self.assertRaises(ValueError):
            crops.validate_boxes(document, 100, 200)

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow not installed; cropping optional")
    def test_lossless_crop_preserves_source_and_records_hash(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            image = folder / "source.png"
            Image.new("RGB", (100, 200), color=(12, 34, 56)).save(image)
            before = hashlib.sha256(image.read_bytes()).hexdigest()
            boxes = folder / "boxes.json"
            boxes.write_text(json.dumps(self.boxes([10, 20, 80, 150])))
            record = crops.crop_image(image, boxes, folder / "out")
            self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), before)
            self.assertEqual(record["input_sha256"], before)
            with Image.open(folder / "out/design.png") as crop:
                self.assertEqual(crop.size, (70, 130))
            with self.assertRaisesRegex(ValueError, "overwrite"):
                crops.crop_image(image, boxes, folder / "out")


if __name__ == "__main__":
    unittest.main()
