import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1] / "validate-spec-traceability.py"
)
MODULE_SPEC = importlib.util.spec_from_file_location(
    "spec_traceability", VALIDATOR_PATH,
)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:
    raise RuntimeError("Cannot load the specification validator")
VALIDATOR = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(VALIDATOR)


class SpecificationTraceabilityTests(unittest.TestCase):
    def setUp(self):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.repo_root = Path(temporary_directory.name)

    def write_fixture(self, relative_path, text):
        destination = self.repo_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
        return destination

    def run_check(self, mode="all"):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = VALIDATOR.main([
                "--repo-root", str(self.repo_root), "--mode", mode,
            ])
        return exit_code, output.getvalue()

    def test_accepts_existing_legacy_source_with_line_anchor(self):
        source = "01-archaeology/legacy-sifap/natural-programs/SAMPLE.NSN"
        self.write_fixture(source, "DEFINE DATA LOCAL\nEND-DEFINE\nEND\n")
        self.write_fixture("specs/001-validation/spec.md", (
            f"## REQ-001: Validation\nsource_legacy: {source}#L1-L3\n"
        ))

        exit_code, output = self.run_check("legacy")

        self.assertEqual(0, exit_code)
        self.assertNotIn("::error", output)

    def test_ears_prompt_example_passes_the_legacy_source_gate(self):
        prompt_path = (
            VALIDATOR_PATH.parents[1] / "prompts"
            / "stage-architect-write-ears-spec.prompt.md"
        )
        prompt_text = prompt_path.read_text(encoding="utf-8")
        output_section = prompt_text.split("## Output Format\n", 1)[1]
        template = output_section.split("```markdown\n", 1)[1]
        example = template.split("```", 1)[0]
        example = example.replace("<PROGRAM>", "SAMPLE")
        example = example.replace("<start>", "1").replace("<end>", "3")
        self.write_fixture(
            "01-archaeology/legacy-sifap/natural-programs/SAMPLE.NSN",
            "DEFINE DATA LOCAL\nEND-DEFINE\nEND\n",
        )
        self.write_fixture("specs/001-validation/spec.md", example)

        exit_code, output = self.run_check("legacy")

        self.assertEqual(0, exit_code, output)

    def test_rejects_nonexistent_legacy_source(self):
        self.write_fixture("specs/001-validation/spec.md", (
            "## REQ-001: Validation\n"
            "source_legacy: 01-archaeology/legacy-sifap/"
            "natural-programs/MISSING.NSN\n"
        ))

        exit_code, output = self.run_check("legacy")

        self.assertEqual(1, exit_code)
        self.assertIn("REQ-001", output)
        self.assertIn("::error", output)

    def test_accepts_justified_greenfield_and_existing_namespaced_ids(self):
        self.write_fixture("specs/portal.md", (
            "## REQ-PORTAL-001: Search\n"
            'source_legacy: "[GREENFIELD] Documentation search is new."\n'
        ))

        exit_code, output = self.run_check("legacy")

        self.assertEqual(0, exit_code)
        self.assertNotIn("::error", output)

    def test_rejects_missing_source(self):
        self.write_fixture(
            "specs/001-validation/spec.md", "## REQ-001: Validation\n",
        )

        exit_code, output = self.run_check("legacy")

        self.assertEqual(1, exit_code)
        self.assertIn("REQ-001", output)

    def test_rejects_unjustified_greenfield_and_unbalanced_quotes(self):
        sources = (
            "[GREENFIELD]", '"[GREENFIELD] Reason', "[GREENFIELD] Reason'",
        )
        for source in sources:
            with self.subTest(source=source):
                self.write_fixture("specs/001-validation/spec.md", (
                    f"## REQ-001: Validation\nsource_legacy: {source}\n"
                ))

                exit_code, _output = self.run_check("legacy")

                self.assertEqual(1, exit_code)

    def test_preserves_twenty_line_source_window(self):
        for distance, expected in ((20, 0), (21, 1)):
            with self.subTest(distance=distance):
                self.write_fixture("specs/001-validation/spec.md", (
                    "## REQ-001: Validation\n" + "\n" * (distance - 1)
                    + "source_legacy: [GREENFIELD] Explicit scope decision.\n"
                ))

                exit_code, _output = self.run_check("legacy")

                self.assertEqual(expected, exit_code)

    def test_does_not_borrow_source_from_next_requirement(self):
        self.write_fixture("specs/001-validation/spec.md", (
            "## REQ-001: First\n\n## REQ-002: Second\n"
            "source_legacy: [GREENFIELD] Applies only to REQ-002.\n"
        ))

        exit_code, output = self.run_check("legacy")

        self.assertEqual(1, exit_code)
        self.assertIn("REQ-001", output)
        self.assertNotIn("REQ-002", output)

    def test_missing_test_references_warn_without_blocking(self):
        self.write_fixture("specs/001-validation/spec.md", (
            "## REQ-001: Validation\n"
            "source_legacy: [GREENFIELD] Explicit scope decision.\n"
        ))

        exit_code, output = self.run_check("tests")

        self.assertEqual(0, exit_code)
        self.assertIn("::warning", output)
        self.assertIn("REQ-001", output)

    def test_finds_backend_frontend_and_portal_test_references(self):
        self.write_fixture("specs/example.md", (
            "## REQ-001: Backend\n## REQ-002: Frontend\n"
            "## REQ-PORTAL-001: Portal\n"
        ))
        self.write_fixture(
            "backend/src/test/java/ExampleTest.java", "// REQ-001\n",
        )
        self.write_fixture("frontend/app/example.test.ts", "// REQ-002\n")
        self.write_fixture(
            "site/tests/example.test.mjs", "// REQ-PORTAL-001\n",
        )

        exit_code, output = self.run_check("tests")

        self.assertEqual(0, exit_code)
        self.assertNotIn("::warning", output)

    def test_production_references_do_not_count_as_tests(self):
        self.write_fixture("specs/example.md", "## REQ-001: Validation\n")
        self.write_fixture("frontend/app/page.tsx", "// REQ-001\n")

        exit_code, output = self.run_check("tests")

        self.assertEqual(0, exit_code)
        self.assertIn("REQ-001", output)
        self.assertIn("::warning", output)

    def test_binary_test_artifact_is_reported_without_crashing(self):
        self.write_fixture("specs/example.md", "## REQ-001: Validation\n")
        binary_file = self.write_fixture("site/tests/screenshot.bin", "")
        binary_file.write_bytes(b"\xff\xfe\x00")

        exit_code, output = self.run_check("tests")

        self.assertEqual(0, exit_code)
        self.assertIn("screenshot.bin", output)
        self.assertIn("::warning", output)

    def test_absent_specs_directory_is_explicitly_skipped(self):
        exit_code, output = self.run_check()

        self.assertEqual(0, exit_code)
        self.assertIn("No specifications directory", output)

    def test_cli_returns_failure_independently_of_working_directory(self):
        self.write_fixture("specs/example.md", "## REQ-001: Missing source\n")

        result = subprocess.run([
            sys.executable, "-B", str(VALIDATOR_PATH),
            "--repo-root", str(self.repo_root), "--mode", "legacy",
        ], cwd=self.repo_root, capture_output=True, text=True, check=False)

        self.assertEqual(1, result.returncode)
        self.assertIn("REQ-001", result.stdout)


if __name__ == "__main__":
    unittest.main()
