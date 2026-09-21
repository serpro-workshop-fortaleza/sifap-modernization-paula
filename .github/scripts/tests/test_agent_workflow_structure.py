import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch


VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1] / "validate-copilot-primitives.py"
)
MODULE_SPEC = importlib.util.spec_from_file_location(
    "primitive_validator", VALIDATOR_PATH
)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:
    raise RuntimeError("Cannot load the primitive validator")
VALIDATOR = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(VALIDATOR)


class AgentWorkflowStructureTests(unittest.TestCase):
    def validate_workflow_heading(self, heading):
        titles = [title for title, _ in VALIDATOR.AGENT_REQUIRED_SECTIONS]
        titles.append(next(iter(VALIDATOR.AGENT_DOD_TITLES)))
        if heading is not None:
            titles.append(heading)
        sections = [
            (title, index) for index, title in enumerate(titles, start=1)
        ]
        reporter = VALIDATOR.Reporter()
        with patch.object(VALIDATOR, "h2_sections", return_value=sections):
            with contextlib.redirect_stdout(io.StringIO()):
                VALIDATOR.check_agent_structure(
                    ".github/agents/example.agent.md", reporter
                )
        return reporter

    def test_accepts_tool_independent_sdd_workflow(self):
        reporter = self.validate_workflow_heading("SDD Workflow")
        self.assertEqual([], reporter.findings)

    def test_preserves_legacy_workflow_heading(self):
        reporter = self.validate_workflow_heading(
            "Integra\u00e7\u00e3o com o Spec-Kit"
        )
        self.assertEqual([], reporter.findings)

    def test_missing_workflow_section_still_warns(self):
        reporter = self.validate_workflow_heading(None)
        self.assertEqual(0, reporter.error_count)
        self.assertEqual(1, reporter.warning_count)
        self.assertIn("SDD Workflow", reporter.findings[0]["message"])


class EnglishPrimitiveStructureTests(unittest.TestCase):
    agent_headings = (
        "Mission",
        "Leading Personas",
        "Operating Principles",
        "What This Agent Knows",
        "What This Agent Does NOT Know",
        "Available Prompts",
        "Definition of Done",
        "Anti-Patterns This Agent Rejects",
        "SDD Workflow",
    )
    prompt_headings = (
        "Objective",
        "When to Invoke",
        "Preconditions",
        "Inputs the Team Must Provide",
        "What I Will Do",
        "What I Will NOT Do",
        "Output Format",
        "Definition of Done",
        "Prompt Body",
        "Example Invocation",
    )

    def validate_headings(self, headings, check):
        content = "# Example\n\n" + "\n\n".join(
            f"## {heading}" for heading in headings
        ) + "\n"
        reporter = VALIDATOR.Reporter()
        with patch.object(VALIDATOR, "read_text", return_value=content):
            with contextlib.redirect_stdout(io.StringIO()):
                check(".github/example.md", reporter)
        return reporter

    def test_accepts_english_agent_and_stage_headings(self):
        for definition in ("Definition of Done", "Stage 2 Definition of Done"):
            with self.subTest(definition=definition):
                headings = [
                    definition if title == "Definition of Done" else title
                    for title in self.agent_headings
                ]
                reporter = self.validate_headings(
                    headings, VALIDATOR.check_agent_structure
                )
                self.assertEqual([], reporter.findings)

    def test_accepts_english_prompt_headings_in_order(self):
        reporter = self.validate_headings(
            self.prompt_headings, VALIDATOR.check_prompt_structure
        )
        self.assertEqual([], reporter.findings)

    def test_missing_english_agent_section_is_still_rejected(self):
        reporter = self.validate_headings(
            self.agent_headings[1:], VALIDATOR.check_agent_structure
        )
        self.assertEqual(1, reporter.error_count)
        self.assertEqual(0, reporter.warning_count)

    def test_out_of_order_english_prompt_is_still_rejected(self):
        headings = list(self.prompt_headings)
        headings[0], headings[1] = headings[1], headings[0]
        reporter = self.validate_headings(
            headings, VALIDATOR.check_prompt_structure
        )
        self.assertEqual(1, reporter.error_count)


if __name__ == "__main__":
    unittest.main()
