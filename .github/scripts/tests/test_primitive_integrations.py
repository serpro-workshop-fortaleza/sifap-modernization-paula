from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]


def read_text(relative_path):
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class PrimitiveIntegrationTests(unittest.TestCase):
    def test_assigned_prompts_are_listed_by_owning_agent(self):
        agents_directory = REPO_ROOT / ".github/agents"
        prompts_directory = REPO_ROOT / ".github/prompts"
        agent_files = {}
        for agent_path in agents_directory.glob("*.agent.md"):
            text = agent_path.read_text(encoding="utf-8")
            frontmatter = text.split("---", 2)[1]
            match = re.search(r'^name:\s*"([^"]+)"', frontmatter, re.M)
            if match:
                agent_files[match.group(1)] = (agent_path, text)

        assigned = {}
        for prompt_path in prompts_directory.glob("*.prompt.md"):
            text = prompt_path.read_text(encoding="utf-8")
            frontmatter = text.split("---", 2)[1]
            match = re.search(r'^agent:\s*"([^"]+)"', frontmatter, re.M)
            if match and match.group(1) in agent_files:
                assigned.setdefault(match.group(1), set()).add(
                    prompt_path.name
                )

        missing = {}
        for agent_name, prompt_files in assigned.items():
            _agent_path, agent_text = agent_files[agent_name]
            linked = set(re.findall(
                r"\.\./prompts/([^\)]+\.prompt\.md)", agent_text
            ))
            if prompt_files - linked:
                missing[agent_name] = sorted(prompt_files - linked)

        self.assertEqual({}, missing)

    def test_instruction_index_matches_checked_in_files(self):
        index = read_text(".github/instructions/README.md")
        indexed = set(re.findall(
            r"^\| `([^`]+\.instructions\.md)` \|",
            index,
            re.MULTILINE,
        ))
        checked_in = {
            path.name
            for path in (REPO_ROOT / ".github/instructions").glob(
                "*.instructions.md"
            )
        }

        self.assertEqual(checked_in, indexed)

    def test_sdd_instruction_scope_targets_kit_artifacts(self):
        instructions = read_text(
            ".github/instructions/sdd-artifacts.instructions.md"
        )

        self.assertIn('applyTo: "specs/**/*.md,', instructions)
        self.assertNotIn('applyTo: ".specs/', instructions)
        self.assertIn("specs/<NNN>-<feature>/", instructions)

    def test_sdd_python_commands_reference_existing_scripts(self):
        documents = (
            ".github/instructions/sdd-artifacts.instructions.md",
            ".github/skills/sdd-requirements-engineer/SKILL.md",
            ".github/skills/sdd-requirements-engineer/references/"
            "sdd-document-and-mermaid-standard.md",
        )
        command_pattern = re.compile(
            r"python3(?: -B)? ((?:\.github/)?scripts/[A-Za-z0-9_-]+\.py)"
        )
        referenced = {
            script
            for document in documents
            for script in command_pattern.findall(read_text(document))
        }

        self.assertTrue(referenced)
        for script in referenced:
            with self.subTest(script=script):
                self.assertTrue((REPO_ROOT / script).is_file())

    def test_playwright_workflow_exposes_required_toolset(self):
        agent = read_text(".github/agents/qa-engineer.agent.md")
        prompt = read_text(
            ".github/prompts/playwright-generate-test.prompt.md"
        )
        skill = read_text(
            ".github/skills/playwright-generate-test/SKILL.md"
        )

        self.assertIn('"playwright/*"', agent)
        self.assertIn('"playwright/*"', prompt)
        self.assertIn("report the workflow as blocked", skill)

    def test_external_action_prompts_expose_required_toolsets(self):
        devops = read_text(".github/agents/devops-engineer.agent.md")
        cost = read_text(".github/prompts/az-cost-optimize.prompt.md")
        health = read_text(
            ".github/prompts/azure-resource-health-diagnose.prompt.md"
        )
        specs = read_text(".github/prompts/gen-specs-as-issues.prompt.md")

        self.assertIn('"Azure MCP Server/*"', devops)
        self.assertIn('"github/*"', devops)
        self.assertIn('"Azure MCP Server/*"', cost)
        self.assertIn('"github/*"', cost)
        self.assertIn('"Azure MCP Server/*"', health)
        self.assertIn('"github/*"', specs)
        for prompt in (cost, specs):
            with self.subTest(prompt=prompt[:80]):
                self.assertIn("explicit approval", prompt)
                self.assertIn("search for duplicate", prompt)

    def test_azure_analysis_skills_are_non_destructive(self):
        skills = (
            read_text(".github/skills/az-cost-optimize/SKILL.md"),
            read_text(
                ".github/skills/azure-resource-health-diagnose/SKILL.md"
            ),
        )
        mutating_apply = re.compile(
            r"^\s*terraform(?:\s+-chdir=\S+)?\s+apply\b",
            re.MULTILINE,
        )
        for skill in skills:
            with self.subTest(skill=skill[:80]):
                self.assertIsNone(mutating_apply.search(skill))
                self.assertNotIn("Priority score =", skill)
                self.assertIn("explicit", skill.lower())

    def test_stage_three_uses_scope_and_repository_coverage_gates(self):
        builder = read_text(".github/agents/builder.agent.md")
        team_flow = read_text("00-TEAM-FLOW.md")

        self.assertIn("80% line and 70% branch coverage", builder)
        self.assertIn("approved `spec.md`, `plan.md`, and `tasks.md`", builder)
        self.assertNotIn("at least 3 working endpoints", builder)
        self.assertNotIn("at least 2 Next.js pages", builder)
        self.assertNotIn("at least 60% line coverage", builder)
        self.assertIn(">= 80% de linhas e >= 70% de branches", team_flow)

    def test_stage_four_delegates_one_item_with_real_github_actions(self):
        evolution = read_text(".github/agents/evolution.agent.md")
        delegation = read_text(
            ".github/prompts/stage-evolution-delegate-to-"
            "copilot-agent.prompt.md"
        )

        self.assertNotIn("at least 3 well-structured", evolution)
        self.assertNotIn("at least 1 IaC module", evolution)
        self.assertIn("one approved, reviewable issue or draft", evolution)
        self.assertIn(
            'tools: ["read", "search", "edit", "github/*"]',
            delegation,
        )
        self.assertIn("Create and assign", delegation)
        self.assertIn("explicitly authorized", delegation)

    def test_workflows_execute_cross_primitive_gates(self):
        spec_quality = read_text(".github/workflows/spec-quality.yml")
        continuous_integration = read_text(".github/workflows/ci.yml")

        self.assertIn(
            "python3 -B -m unittest discover -s .github/scripts/tests -v",
            spec_quality,
        )
        self.assertIn("validate-copilot-primitives.py", spec_quality)
        self.assertIn(
            "validate-spec-traceability.py --mode tests", spec_quality
        )
        self.assertIn(
            "validate-spec-traceability.py --mode legacy", spec_quality
        )
        self.assertIn("pnpm build", continuous_integration)
        self.assertIn("pnpm test --run --coverage", continuous_integration)


if __name__ == "__main__":
    unittest.main()
