#!/usr/bin/env python3
"""Validate GitHub Copilot primitives and repository governance policies.

This is the evaluation and governance layer of the datacorp-mm-team-kit
agent harness. It turns rules previously enforced through human memory into
automated checks, so broken primitives fail visibly rather than silently.

Checks
------
1. Frontmatter schemas for agents, prompts, instructions, and skills.
2. Referential integrity: prompt -> agent, agent handoffs, and relative
    Markdown links in .github/.
3. Hook definitions: JSON validity, version, event names, handler types,
    and the existence and executable permission of every referenced script.
4. Repository policy: no markdownlint pragmas, incorrect event names,
    competing assistant/IDE recommendations, or stale directory names.
5. Structure: every Markdown file in .github/ ends with exactly one newline
    and contains exactly one H1.
6. Body sections: every agent, prompt, skill, and instruction has its
    required `## ` sections (in canonical order for prompts), following
    the reference primitives.

Design constraints
------------------
- Python 3.11+, standard library only. CI must not need `pip install`, so
  a small tolerant parser reads YAML frontmatter instead of PyYAML.
- Files are enumerated with `git ls-files` so the validator sees exactly
  what CI checks out (tracked files), ignoring untracked temporary files.

Exit code
---------
Exit nonzero for any error-level violation. Warnings do not fail the check.
Each finding emits a GitHub Actions `::error`/`::warning` annotation,
followed by a grouped summary.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]

# Repository-relative POSIX paths for this script and its companion document.
# They are exempt from content-policy checks because they legitimately contain
# forbidden literals in regexes and documentation.
SCRIPT_RELPATH = os.path.relpath(SCRIPT_PATH, REPO_ROOT).replace(os.sep, "/")
DOC_RELPATH = "docs/copilot-primitive-validation.md"
POLICY_EXEMPT_FILES = {SCRIPT_RELPATH, DOC_RELPATH}

# --- Official frontmatter schemas -----------------------------------------

AGENT_ALLOWED_KEYS = {
    "name", "description", "tools", "model", "handoffs", "mcp-servers",
    "argument-hint", "target", "user-invocable", "disable-model-invocation",
    "metadata", "agents",
}
AGENT_REQUIRED_KEYS = {"description"}
AGENT_RETIRED_KEYS = {
    "infer": "retired frontmatter key 'infer' (removed from the agent schema)",
}

PROMPT_ALLOWED_KEYS = {"name", "description",
                       "agent", "model", "tools", "argument-hint"}
PROMPT_REQUIRED_KEYS: set[str] = set()
PROMPT_RETIRED_KEYS = {
    "mode": "retired key 'mode' (chat-mode syntax replaced by 'agent')",
    "tested_with": "invalid key 'tested_with' (not part of the prompt schema)",
}

INSTRUCTION_ALLOWED_KEYS = {"applyTo", "name", "description", "excludeAgent"}
INSTRUCTION_REQUIRED_KEYS: set[str] = set()
INSTRUCTION_RETIRED_KEYS: dict[str, str] = {}

SKILL_NONSTANDARD_KEYS = {"license",
                          "allowed-tools", "compatibility", "metadata"}

# --- Hook schema ----------------------------------------------------------

HOOK_EVENTS = {
    "sessionStart", "sessionEnd", "userPromptSubmitted", "userPromptTransformed",
    "preToolUse", "postToolUse", "postToolUseFailure", "agentStop",
    "subagentStart", "subagentStop", "errorOccurred", "notification",
    "permissionRequest", "preCompact",
}
HOOK_TYPES = {"command", "http", "prompt"}

# --- Repository policy ----------------------------------------------------

STALE_PATHS = ["01-arqueologia", "02-spec-moderna",
               "06-agentes-de-estagio", "legado-sifap"]

# Files allowed to retain an inline markdownlint pragma. Otherwise the root
# .markdownlint-cli2.jsonc is the single source of truth.
PRAGMA_ALLOWED_FILES = {"docs/adr/0000-template.md", "docs/DOC-STYLE-GUIDE.md"}
# Files documenting the event-name prohibition may quote the forbidden words.
TERMINOLOGY_EXEMPT_FILES = {"docs/DOC-STYLE-GUIDE.md"} | POLICY_EXEMPT_FILES

COMPETING_TOOLS = [
    "Cursor", "Windsurf", "Codex", "Cline", "Continue", "Aider", "Codeium",
    "Tabnine", "IntelliJ", "Eclipse", "Neovim",
]
TOOL_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(COMPETING_TOOLS) + r")(?![A-Za-z0-9])")
RECOMMEND_VERB_RE = re.compile(
    r"\b(use|uses|using|used|try|tries|trying|install|installs|installing|"
    r"adopt|adopts|adopting|switch|switching|migrate|migrating|recommend|"
    r"recommends|recommended|recommending|prefer|prefers|choose|choosing|"
    r"pick|picking|run|running|open|opens|opening|usar?|use|utiliz(?:a|e|ar|ando)|"
    r"tentar?|tente|instal(?:a|e|ar|ando)|adot(?:a|e|ar|ando)|trocar?|troque|"
    r"migr(?:a|e|ar|ando)|recomend(?:a|e|ar|ando)|prefer(?:e|ir|indo)|"
    r"escolh(?:a|e|er|endo)|selecion(?:a|e|ar|ando)|execut(?:a|e|ar|ando)|"
    r"abr(?:a|e|ir|indo))\b",
    re.IGNORECASE,
)
NEGATION_RE = re.compile(
    r"(?i)(\bdo not\b|\bdon'?t\b|\bnever\b|\bavoid(?:ing)?\b|\binstead of\b|"
    r"\brather than\b|\bnot\b|"
    r"\bno\s+one(?=\s|[,;:.!?]|$)|\bnobody\b|"
    r"\bno\s+(?:[A-Za-z][A-Za-z'-]*\s+){1,6}"
    r"(?:(?:should|must|may|can|could|would|will)\s+)?"
    r"(?:us(?:e|es|ed|ing)|tr(?:y|ies|ied|ying)|install(?:s|ed|ing)?|"
    r"adopt(?:s|ed|ing)?|switch(?:es|ed|ing)?|migrat(?:e|es|ed|ing)|"
    r"recommend(?:s|ed|ing)?|prefer(?:s|red|ring)?|choos(?:e|es|ing)|chose|"
    r"pick(?:s|ed|ing)?|run(?:s|ning)?|ran|open(?:s|ed|ing)?)\b|"
    r"\b(?:there\s+(?:is|are)|(?:i|we|the team)\s+(?:have|has))\s+no\s+"
    r"(?:plans?|intentions?|reasons?|needs?|requirements?|obligations?|necessit(?:y|ies)|"
    r"permissions?)\s+to\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+(?:need|reason|way|justification|requirement|obligation|necessity|"
    r"intention|plan|permission)\s+to\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+(?:reason|need|requirement|obligation|necessity|permission)\s+for\s+"
    r"(?:\w+\s+){1,3}to\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+(?:reason|need)\s+(?:i|we|you|they|users?|developers?|teams?|people|persons?|"
    r"members?|organizations?|projects?)\s+(?:should|must|may|can|could|would|will)\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+use\s+of\b|"
    r"\bno longer\b|"
    r"\bban(?:ned|s|ning)?\b|\bprohibit\w*\b|"
    r"\bforbid\w*\b|\bdisallow\w*\b|\bunlike\b|\bcannot\b|\bcan'?t\b|"
    r"\bwon'?t\b|\bshould ?n'?t\b|\bshould not\b|\bmust ?n'?t\b|\bmust not\b|"
    r"\brefrain\b|\breject\w*\b|\bdeprecat\w*\b|\bnão\b|\bnunca\b|\bjamais\b|"
    r"^\s*(?:[-*+>]\s+|\d+[.)]\s+)*(?:nem|tampouco|nor|neither)\b|"
    r"\bevit(?:e|ar|ando)\b|\bsem\s+(?:usar?|utiliz(?:ar|e)|instal(?:ar|e)|"
    r"adot(?:ar|e)|trocar?|migrar?|recomendar?|preferir|escolher|selecionar|"
    r"executar?|abrir)\b|"
    r"\b(?:ninguém|nenhum(?:a)?\s+"
    r"(?:usuários?|desenvolvedor(?:es)?|equipes?|pessoas?|membros?|organizações?|projetos?))\b|"
    r"\bem vez de\b|\bao invés de\b|\bproib\w*\b|\bvedad\w*\b|\bnão pode\b|"
    r"\bnão deve\b|\bnão usar\b|\brejeit\w*\b|\bdescontinu\w*\b|❌)"
)
INTERROGATIVE_RE = re.compile(
    r"(?i)(\b(?:can|could|should|may|shall|do|would|will)\s+(?:i|we|you)\b|"
    r"^\s*(?:[-*+>#]\s*)*(?:eu\s+)?posso\b|"
    r"\b(?:verifique|verificar|avalie|avaliar|confirme|confirmar|determine|"
    r"determinar|descubra|descobrir|pergunte|perguntar|saber)\s+se\s+"
    r"(?:eu\s+)?(?:posso|podemos|pode|devo|devemos|deveria|poderia)\b|"
    r"\bwhat about\b|\bis it ok\b|\be quanto a\b|\bestá tudo bem\b|\?)"
)
RECOMMEND_WINDOW = 40  # Characters before a tool name that may contain the verb
HARD_CLAUSE_BOUNDARIES = ";!?"
CONTRAST_BOUNDARY_RE = re.compile(
    r",\s+(?:mas|porém|contudo|todavia|portanto|logo|então|but|however|yet|so|"
    r"therefore|thus)(?:,\s*|\s+)",
    re.IGNORECASE,
)
PERIOD_ABBREVIATIONS = {
    "dr", "dra", "e.g", "etc", "ex", "i.e", "jr", "mr", "mrs", "ms",
    "p.ex", "prof", "sr", "sra", "v", "ver", "vs",
}


class Reporter:
    """Collect findings, emit GitHub annotations, and print a summary."""

    def __init__(self) -> None:
        self.findings: list[dict] = []

    def _add(self, level: str, check: str, file: str, line: int | None, message: str) -> None:
        self.findings.append(
            {"level": level, "check": check, "file": file,
                "line": line, "message": message}
        )
        location = file if file else "repository"
        annotation = f"::{level} file={file}" if file else f"::{level} "
        if file and line:
            annotation += f",line={line}"
        annotation += f"::[{check}] {location}"
        if line:
            annotation += f":{line}"
        annotation += f" - {message}"
        print(annotation)

    def error(self, check: str, file: str, line: int | None, message: str) -> None:
        self._add("error", check, file, line, message)

    def warning(self, check: str, file: str, line: int | None, message: str) -> None:
        self._add("warning", check, file, line, message)

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f["level"] == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f["level"] == "warning")

    def summarize(self) -> None:
        print("\n" + "=" * 72)
        print("Copilot primitive validation summary")
        print("=" * 72)
        if not self.findings:
            print(
                "No issues found. All Copilot primitives and policies passed.")
            return
        by_check: dict[str, dict[str, int]] = {}
        for finding in self.findings:
            bucket = by_check.setdefault(
                finding["check"], {"error": 0, "warning": 0})
            bucket[finding["level"]] += 1
        for check in sorted(by_check):
            counts = by_check[check]
            print(
                f"  {check:<24} {counts['error']:>3} error(s)"
                f"  {counts['warning']:>3} warning(s)"
            )
        print("-" * 72)
        print(
            f"  {'TOTAL':<24} {self.error_count:>3} error(s)  {self.warning_count:>3} warning(s)")
        print("=" * 72)


# --- File utilities -------------------------------------------------------

def tracked_files() -> list[str]:
    """Return repository-relative POSIX paths of tracked files, as in CI.

    Fall back to a filesystem scan when Git is unavailable.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
            capture_output=True,
            check=True,
        )
        return [p for p in result.stdout.decode("utf-8", "replace").split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        skip_dirs = {".git", "node_modules"}
        skip_prefixes = ("backend/target/", "frontend/.next/")
        paths: list[str] = []
        for root, dirs, files in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for name in files:
                rel = os.path.relpath(os.path.join(
                    root, name), REPO_ROOT).replace(os.sep, "/")
                if not rel.startswith(skip_prefixes):
                    paths.append(rel)
        return paths


def read_text(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8", errors="replace")


def read_bytes(rel: str) -> bytes:
    return (REPO_ROOT / rel).read_bytes()


def looks_binary(data: bytes) -> bool:
    return b"\x00" in data[:8192]


# --- Frontmatter parsing --------------------------------------------------

FM_DELIM_RE = re.compile(r"^---\s*$")
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")


def split_frontmatter(text: str) -> list[str] | None:
    """Return frontmatter lines or None if missing or incomplete."""
    lines = text.split("\n")
    if lines and lines[0].startswith("\ufeff"):
        lines[0] = lines[0].lstrip("\ufeff")
    if not lines or not FM_DELIM_RE.match(lines[0]):
        return None
    for i in range(1, len(lines)):
        if FM_DELIM_RE.match(lines[i]):
            return lines[1:i]
    return None


def top_level_entries(fm_lines: list[str]) -> list[tuple[str, str, int]]:
    """Return (key, inline_value, frontmatter_index) for top-level keys."""
    entries = []
    for idx, line in enumerate(fm_lines):
        if not line or line[0] in " \t#":
            continue
        match = TOP_KEY_RE.match(line)
        if match:
            entries.append((match.group(1), match.group(2), idx))
    return entries


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def get_top_value(fm_lines: list[str], key: str) -> str | None:
    """Return a top-level scalar value, joining block scalars."""
    for idx, line in enumerate(fm_lines):
        match = TOP_KEY_RE.match(line)
        if not match or match.group(1) != key or (line[:1].isspace()):
            continue
        inline = match.group(2).strip()
        if inline and inline not in ("|", ">", "|-", ">-", "|+", ">+"):
            return unquote(inline)
        collected = []
        for follow in fm_lines[idx + 1:]:
            if follow.strip() == "":
                continue
            if follow[0] in " \t":
                collected.append(follow.strip())
            else:
                break
        return unquote(" ".join(collected)) if collected else ""
    return None


def handoff_agents(fm_lines: list[str]) -> list[tuple[str, int]]:
    """Return (agent_value, index) for each agent named in the handoffs block."""
    results = []
    in_block = False
    for idx, line in enumerate(fm_lines):
        entry = TOP_KEY_RE.match(line)
        if entry and not line[:1].isspace():
            in_block = entry.group(1) == "handoffs"
            continue
        if in_block:
            nested = re.match(r"^\s+-?\s*agent:\s*(.+?)\s*$", line)
            if nested:
                results.append((unquote(nested.group(1)), idx))
    return results


def fm_line_number(idx: int) -> int:
    """Convert a frontmatter content index to a 1-based line number."""
    return idx + 2  # Line 1 is the opening '---'


# --- Schema checks --------------------------------------------------------

def check_closed_schema(
    rel: str,
    fm_lines: list[str],
    allowed: set[str],
    required: set[str],
    retired: dict[str, str],
    reporter: Reporter,
    check: str,
) -> None:
    seen: dict[str, int] = {}
    for key, _inline, idx in top_level_entries(fm_lines):
        seen.setdefault(key, idx)
    for key, idx in seen.items():
        if key in retired:
            reporter.error(check, rel, fm_line_number(idx), retired[key])
        elif key not in allowed:
            reporter.error(
                check, rel, fm_line_number(idx),
                f"unknown frontmatter key '{key}' (allowed: {', '.join(sorted(allowed))})",
            )
    for key in sorted(required):
        if key not in seen:
            reporter.error(
                check, rel, 1, f"missing required frontmatter key: '{key}'")


def check_agents(agent_files: list[str], reporter: Reporter) -> None:
    for rel in agent_files:
        check_agent_structure(rel, reporter)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("agents", rel, 1,
                           "missing or incomplete YAML frontmatter")
            continue
        check_closed_schema(
            rel, fm_lines, AGENT_ALLOWED_KEYS, AGENT_REQUIRED_KEYS,
            AGENT_RETIRED_KEYS, reporter, "agents",
        )


def check_prompts(prompt_files: list[str], valid_agent_ids: set[str], reporter: Reporter) -> None:
    for rel in prompt_files:
        check_prompt_structure(rel, reporter)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("prompts", rel, 1,
                           "missing or incomplete YAML frontmatter")
            continue
        check_closed_schema(
            rel, fm_lines, PROMPT_ALLOWED_KEYS, PROMPT_REQUIRED_KEYS,
            PROMPT_RETIRED_KEYS, reporter, "prompts",
        )
        agent_value = get_top_value(fm_lines, "agent")
        if agent_value and agent_value not in valid_agent_ids:
            reporter.error(
                "referential-integrity", rel, 1,
                f'agent: "{agent_value}" does not match any agent in .github/agents/',
            )


def check_instructions(instruction_files: list[str], reporter: Reporter) -> None:
    for rel in instruction_files:
        check_instruction_structure(rel, reporter)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("instructions", rel, 1,
                           "missing or incomplete YAML frontmatter")
            continue
        check_closed_schema(
            rel, fm_lines, INSTRUCTION_ALLOWED_KEYS, INSTRUCTION_REQUIRED_KEYS,
            INSTRUCTION_RETIRED_KEYS, reporter, "instructions",
        )
        apply_to = get_top_value(fm_lines, "applyTo")
        if apply_to is not None and apply_to.strip() == "**":
            reporter.error(
                "instructions", rel, 1,
                "applyTo: \"**\" injects this file into every request and consumes the "
                "context window; restrict it to concrete globs",
            )


def check_skills(skill_files: list[str], reporter: Reporter) -> None:
    for rel in skill_files:
        check_skill_structure(rel, reporter)
        dirname = rel.split("/")[-2]
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("skills", rel, 1,
                           "missing or incomplete YAML frontmatter")
            continue
        seen = {key: idx for key, _inline, idx in top_level_entries(fm_lines)}
        for key in ("name", "description"):
            if key not in seen:
                reporter.error("skills", rel, 1,
                               f"missing required frontmatter key: '{key}'")
        for key in sorted(SKILL_NONSTANDARD_KEYS):
            if key in seen:
                reporter.error(
                    "skills", rel, fm_line_number(seen[key]),
                    f"nonstandard skill frontmatter key: '{key}'",
                )
        name = get_top_value(fm_lines, "name")
        if name is not None:
            if name != dirname:
                reporter.error(
                    "skills", rel, fm_line_number(seen.get("name", 0)),
                    f"skill name '{name}' must match directory name '{dirname}' "
                    "(a mismatch makes the skill silently fail to load)",
                )
            if not re.fullmatch(r"[a-z0-9-]+", name):
                reporter.error(
                    "skills", rel, fm_line_number(seen.get("name", 0)),
                    f"skill name '{name}' must contain only lowercase letters, digits, and hyphens",
                )
            if len(name) > 64:
                reporter.error(
                    "skills", rel, fm_line_number(seen.get("name", 0)),
                    f"skill name has {len(name)} characters; the limit is 64",
                )
        description = get_top_value(fm_lines, "description")
        if description is not None and len(description) > 1024:
            reporter.error(
                "skills", rel, fm_line_number(seen.get("description", 0)),
                f"skill description has {len(description)} characters; the limit is 1024",
            )


def build_agent_registry(agent_files: list[str], reporter: Reporter) -> set[str]:
    """Get valid agent identifiers from files in .github/agents/.

    The canonical ID is the frontmatter `name:`, falling back to the file stem
    when `name:` is absent. When both exist, they must match; a mismatch is
    reported because a prompt using one spelling would silently miss the other.
    """
    ids: set[str] = set()
    for rel in agent_files:
        stem = Path(rel).name[: -len(".agent.md")]
        ids.add(stem)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is not None:
            name = get_top_value(fm_lines, "name")
            if name:
                ids.add(name)
                if name != stem:
                    reporter.error(
                        "referential-integrity", rel, 1,
                        f"agent name '{name}' does not match file stem '{stem}'; "
                        "rename them so the declared name and file match",
                    )
    return ids


def check_handoffs(agent_files: list[str], valid_agent_ids: set[str], reporter: Reporter) -> None:
    for rel in agent_files:
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            continue
        for agent_value, idx in handoff_agents(fm_lines):
            if agent_value not in valid_agent_ids:
                reporter.error(
                    "referential-integrity", rel, fm_line_number(idx),
                    f"handoff targets agent '{agent_value}', which does not exist in .github/agents/",
                )


# --- Hook checks ----------------------------------------------------------

def check_hooks(hook_files: list[str], subdir_hook_files: list[str], reporter: Reporter) -> None:
    for rel in subdir_hook_files:
        reporter.warning(
            "hooks", rel, 1,
            "hooks.json in a subdirectory is not discovered; only root-level "
            ".github/hooks/NAME.json files are loaded",
        )
    for rel in hook_files:
        try:
            data = json.loads(read_text(rel))
        except json.JSONDecodeError as exc:
            reporter.error("hooks", rel, exc.lineno,
                           f"invalid JSON: {exc.msg}")
            continue
        if data.get("version") != 1:
            reporter.error(
                "hooks", rel, 1, f"hook 'version' must be 1 (found {data.get('version')!r})")
        hooks = data.get("hooks")
        if not isinstance(hooks, dict):
            reporter.error("hooks", rel, 1,
                           "hook file must contain a 'hooks' object")
            continue
        for event, handlers in hooks.items():
            if event not in HOOK_EVENTS:
                reporter.error("hooks", rel, 1,
                               f"unknown hook event: '{event}'")
            if not isinstance(handlers, list):
                reporter.error(
                    "hooks", rel, 1, f"event '{event}' must map to a list of handlers")
                continue
            for handler in handlers:
                if not isinstance(handler, dict):
                    reporter.error("hooks", rel, 1,
                                   f"event '{event}' has a handler that is not an object")
                    continue
                handler_type = handler.get("type")
                if handler_type not in HOOK_TYPES:
                    reporter.error(
                        "hooks", rel, 1,
                        f"handler for event '{event}' has type {handler_type!r}; "
                        f"expected one of {', '.join(sorted(HOOK_TYPES))}",
                    )
                for shell_key in ("bash", "powershell"):
                    value = handler.get(shell_key)
                    if not value:
                        continue
                    script = value.split()[0]
                    script_path = REPO_ROOT / script
                    if not script_path.is_file():
                        reporter.error(
                            "hooks", rel, 1,
                            f"{shell_key} script '{script}' for event '{event}' does not exist",
                        )
                    elif not os.access(script_path, os.X_OK):
                        reporter.error(
                            "hooks", rel, 1,
                            f"{shell_key} script '{script}' for event '{event}' is not executable",
                        )


# --- Markdown structure and links -----------------------------------------

H1_RE = re.compile(r"^ {0,3}#(?:[ \t].*)?$")
FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*([^)]*?)\s*\)")
REF_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")


def fence_mask(lines: list[str]) -> list[bool]:
    """Mark fenced code block lines according to CommonMark.

    A closing delimiter must repeat the opening character, be at least as long,
    and have no info string. This prevents an inner ```lang delimiter (which
    has an info string) from being mistaken for the end of an outer ``` block.
    """
    mask = [False] * len(lines)
    in_fence = False
    fence_char = ""
    fence_len = 0
    for i, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if not in_fence:
            if match:
                in_fence = True
                fence_char = match.group(2)[0]
                fence_len = len(match.group(2))
                mask[i] = True
        else:
            mask[i] = True
            if (
                match
                and match.group(2)[0] == fence_char
                and len(match.group(2)) >= fence_len
                and match.group(3).strip() == ""
            ):
                in_fence = False
                fence_char = ""
                fence_len = 0
    return mask


def frontmatter_end(lines: list[str]) -> int:
    """Return the first line index after YAML frontmatter, or 0 if absent."""
    if not lines or lines[0].strip() != "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1
    return 0


def iter_prose(rel: str):
    """Yield (line_number, text) for prose lines only.

    Skip fenced code blocks and remove inline code so content-policy checks
    flag active prose occurrences of a forbidden pattern rather than quoted
    code examples documenting the rule itself.
    """
    lines = read_text(rel).split("\n")
    mask = fence_mask(lines)
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        yield i + 1, INLINE_CODE_RE.sub("", line)


def check_markdown_structure(rel: str, reporter: Reporter) -> None:
    data = read_bytes(rel)
    if not data.endswith(b"\n"):
        reporter.error("markdown-structure", rel, None,
                       "file must end with exactly one newline")
    elif data.endswith(b"\n\n"):
        reporter.error("markdown-structure", rel, None,
                       "file has more than one trailing newline")

    lines = data.decode("utf-8", "replace").split("\n")
    mask = fence_mask(lines)
    start = frontmatter_end(lines)
    h1_lines = [
        offset + 1
        for offset in range(start, len(lines))
        if not mask[offset] and H1_RE.match(lines[offset])
    ]
    if len(h1_lines) == 0:
        reporter.error("markdown-structure", rel, None,
                       "file has no H1 heading (expected: exactly one)")
    elif len(h1_lines) > 1:
        reporter.error(
            "markdown-structure", rel, h1_lines[1],
            f"file has {len(h1_lines)} H1 headings (expected: exactly one); "
            f"extra H1 at line {h1_lines[1]}",
        )


def check_markdown_links(rel: str, reporter: Reporter) -> None:
    lines = read_text(rel).split("\n")
    mask = fence_mask(lines)
    base_dir = (REPO_ROOT / rel).parent
    for lineno, raw in enumerate(lines, start=1):
        if mask[lineno - 1]:
            continue
        line = INLINE_CODE_RE.sub("", raw)
        targets = list(LINK_RE.findall(line))
        ref_def = REF_DEF_RE.match(raw)
        if ref_def:
            targets.append(ref_def.group(1))
        for target in targets:
            _check_link_target(rel, lineno, target, base_dir, reporter)


def _check_link_target(rel: str, lineno: int, target: str, base_dir: Path, reporter: Reporter) -> None:
    target = target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:].split(">", 1)[0]
    elif target:
        target = target.split()[0]
    target = target.split("#", 1)[0]
    if not target:
        return
    if URI_SCHEME_RE.match(target) or target.startswith("//"):
        return
    if any(ch in target for ch in "{}<>$*"):
        return
    if target.startswith("/"):
        candidate = REPO_ROOT / target.lstrip("/")
    else:
        candidate = base_dir / target
    if not os.path.exists(os.path.normpath(candidate)):
        reporter.error(
            "referential-integrity", rel, lineno,
            f"broken relative link '{target}' (resolves to a nonexistent path)",
        )


# --- Primitive body structure checks --------------------------------------
#
# Frontmatter tells the loader how to connect a primitive; body `## ` sections
# are the human-readable contract. Reference primitives (the archaeologist
# agent, stage/persona prompts, and native skills and instructions) share a
# fixed set of sections. These checks enforce that convention so omitting
# "What I Will NOT Do" or "Quality Gate" fails visibly instead of drifting.
# Findings use the `primitive-structure` category. Fenced blocks and YAML
# frontmatter are ignored using the same detectors as elsewhere, so `## `
# lines in example templates never count as real document sections.

STRUCTURE_CHECK = "primitive-structure"

H2_RE = re.compile(r"^ {0,3}##(?!#)[ \t]+(.+?)[ \t]*$")
ATX_CLOSING_RE = re.compile(r"[ \t]+#+[ \t]*$")

# Agents: presence only. The reference archaeologist puts the definition of
# done before "Available Prompts", while persona agents put it afterward;
# therefore section order is not enforced.
AGENT_REQUIRED_SECTIONS = [
    ("Mission", {"Missão", "Mission"}),
    ("Leading Personas", {"Personas líderes", "Leading Personas"}),
    ("Operating Principles", {
     "Princípios operacionais", "Operating Principles"}),
    ("What This Agent Knows", {
     "O que este agente sabe", "What This Agent Knows"}),
    ("What This Agent Does NOT Know", {
     "O que este agente NÃO sabe", "What This Agent Does NOT Know"}),
    ("Available Prompts", {"Prompts disponíveis", "Available Prompts"}),
    ("Anti-Patterns This Agent Rejects", {
        "Antipadrões que este agente rejeita",
        "Anti-Patterns This Agent Rejects"}),
]
# The archaeologist uses "Stage 1 Definition of Done"; persona agents use
# "Definition of Done". Retain Portuguese aliases for translated editions.
AGENT_DOD_TITLES = {"Definição de pronto", "Definition of Done"}
AGENT_DOD_PT_BR_PREFIX = "Definição de pronto do Estágio "
# Common but not universal; absence produces a warning, not an error.
AGENT_RECOMMENDED_SECTIONS = [
    ("SDD Workflow", {"SDD Workflow", "Integração com o Spec-Kit"})
]

# Prompts: presence AND canonical relative order. Extra sections (such as
# "## Rules for <file>" between "Output Format" and "Definition of Done")
# are allowed and ignored by the order check.
PROMPT_REQUIRED_SECTIONS = [
    ("Objective", {"Objetivo", "Objective"}),
    ("When to Invoke", {
     "Quando invocar", "Quando usar", "When to Invoke", "When to Use"}),
    ("Preconditions", {"Pré-condições", "Preconditions"}),
    ("Inputs the Team Must Provide", {
     "Entradas que a equipe deve fornecer", "Inputs the Team Must Provide"}),
    ("What I Will Do", {"O que farei", "What I Will Do"}),
    ("What I Will NOT Do", {
     "O que NÃO farei", "O que não farei", "What I Will NOT Do"}),
    ("Output Format", {"Formato da saída", "Output Format"}),
    ("Definition of Done", {"Definição de pronto", "Definition of Done"}),
    ("Prompt Body", {"Corpo do prompt", "Prompt Body"}),
    ("Example Invocation", {
     "Exemplo de invocação", "Exemplo de chamada", "Example Invocation"}),
]

# Skills: case-insensitive comparison because native skills use sentence case
# while some imported skills use title case.
SKILL_REQUIRED_SECTIONS = [
    ("When to Invoke", {"Quando usar", "Quando invocar",
     "When to Use", "When to Invoke"}),
    ("Output Template", {"Modelo de saída", "Output Template"}),
    ("Quality Gate", {
     "Critério de qualidade", "Critérios de qualidade", "Quality Gate"}),
]

# Instructions: presence only, with exact heading matches.
INSTRUCTION_REQUIRED_SECTIONS = [
    ("Conventions", {"Convenções", "Conventions"}),
    ("Do / Don't", {"Faça / Não faça", "Do / Don't"}),
    ("PR Checklist", {
        "Lista de verificação antes de abrir uma PR",
        "PR Checklist",
    }),
]


def h2_sections(rel: str) -> list[tuple[str, int]]:
    """Return (title, 1-based line) for every real ## heading in Markdown.

    Reuse the fence mask and frontmatter detector so ## lines inside example
    blocks or YAML frontmatter do not count as sections.
    """
    lines = read_text(rel).split("\n")
    mask = fence_mask(lines)
    start = frontmatter_end(lines)
    sections: list[tuple[str, int]] = []
    for i in range(start, len(lines)):
        if mask[i]:
            continue
        heading = H2_RE.match(lines[i])
        if heading:
            title = ATX_CLOSING_RE.sub("", heading.group(1)).strip()
            sections.append((title, i + 1))
    return sections


def _report_missing_sections(
    rel: str,
    present: set[str],
    required: list[tuple[str, set[str]]],
    reporter: Reporter,
) -> None:
    for section, aliases in required:
        if present.isdisjoint(aliases):
            reporter.error(
                STRUCTURE_CHECK, rel, None, f"missing required section: '## {section}'"
            )


def check_agent_structure(rel: str, reporter: Reporter) -> None:
    titles = [title for title, _ in h2_sections(rel)]
    present = set(titles)
    _report_missing_sections(rel, present, AGENT_REQUIRED_SECTIONS, reporter)
    has_definition_of_done = any(
        title in AGENT_DOD_TITLES
        or (
            title.startswith("Stage ")
            and title.endswith(" Definition of Done")
        )
        or title.startswith(AGENT_DOD_PT_BR_PREFIX)
        for title in titles
    )
    if not has_definition_of_done:
        reporter.error(
            STRUCTURE_CHECK, rel, None,
            "missing required definition-of-done section "
            "(for example, '## Definition of Done' or "
            "'## Stage 1 Definition of Done')",
        )
    for section, aliases in AGENT_RECOMMENDED_SECTIONS:
        if present.isdisjoint(aliases):
            reporter.warning(
                STRUCTURE_CHECK, rel, None,
                f"missing recommended section: '## {section}'",
            )


def check_prompt_structure(rel: str, reporter: Reporter) -> None:
    sections = h2_sections(rel)
    present = {title for title, _ in sections}
    _report_missing_sections(rel, present, PROMPT_REQUIRED_SECTIONS, reporter)

    # Check that required sections appear in canonical relative order.
    # Track the highest required section rank encountered; a lower-ranked
    # section appearing later is reported against the section it should precede.
    canonical = {
        alias: (index, name)
        for index, (name, aliases) in enumerate(PROMPT_REQUIRED_SECTIONS)
        for alias in aliases
    }
    highest_rank = -1
    highest_title: str | None = None
    seen: set[int] = set()
    for title, lineno in sections:
        if title not in canonical:
            continue
        rank, canonical_title = canonical[title]
        if rank in seen:
            continue
        seen.add(rank)
        if rank < highest_rank:
            reporter.error(
                STRUCTURE_CHECK, rel, lineno,
                f"section '## {canonical_title}' is out of order: it must appear before "
                f"'## {highest_title}'",
            )
            return
        highest_rank = rank
        highest_title = canonical_title


def check_skill_structure(rel: str, reporter: Reporter) -> None:
    sections = h2_sections(rel)
    lower_titles = [title.lower() for title, _ in sections]
    for section, aliases in SKILL_REQUIRED_SECTIONS:
        lower_aliases = {alias.lower() for alias in aliases}
        if set(lower_titles).isdisjoint(lower_aliases):
            reporter.error(
                STRUCTURE_CHECK, rel, None, f"missing required section: '## {section}'"
            )
    # A compliant skill has at least one procedure section between its trigger
    # ("When to Invoke") and "Output Template". A distance of one means adjacent
    # headings with no procedure, which produces a warning.
    trigger_aliases = {alias.lower()
                       for alias in SKILL_REQUIRED_SECTIONS[0][1]}
    output_aliases = {alias.lower() for alias in SKILL_REQUIRED_SECTIONS[1][1]}
    first = next((i for i, title in enumerate(lower_titles)
                 if title in trigger_aliases), None)
    last = next((i for i, title in enumerate(lower_titles)
                if title in output_aliases), None)
    if first is not None and last is not None:
        if last - first < 2:
            reporter.warning(
                STRUCTURE_CHECK, rel, sections[last][1],
                "no procedure section between '## When to Invoke' and "
                "'## Output Template'; document the steps performed by the skill",
            )


def check_instruction_structure(rel: str, reporter: Reporter) -> None:
    present = {title for title, _ in h2_sections(rel)}
    _report_missing_sections(
        rel, present, INSTRUCTION_REQUIRED_SECTIONS, reporter)


# --- Repository policy checks ---------------------------------------------

PRAGMA_RE = re.compile(r"<!--\s*markdownlint-disable")
# The event is an immersion. "hackath?on" also covers the misspelling "hackaton";
# an earlier regex, `hackat[o]?on`, matched neither spelling.
EVENT_TERM_RE = re.compile(r"hackath?ons?|workshops?", re.IGNORECASE)
# Real identifiers that legitimately contain a forbidden word: GitHub
# organization and enterprise slugs, an active repository, and an Azure tag
# applied to the lab.
EVENT_TERM_ALLOWED_RE = re.compile(
    r"workshop-gbb|software-gbb-workshops|workshop-datacorp|"
    r"workshop-legacy-modernization|team=workshop-XX"
)
STALE_RE = re.compile("|".join(re.escape(name) for name in STALE_PATHS))


def check_pragmas(markdown_files: list[str], reporter: Reporter) -> None:
    for rel in markdown_files:
        if rel in PRAGMA_ALLOWED_FILES or rel in POLICY_EXEMPT_FILES:
            continue
        for lineno, line in iter_prose(rel):
            if PRAGMA_RE.search(line):
                reporter.error(
                    "policy-pragma", rel, lineno,
                    "inline markdownlint pragmas are forbidden; the root "
                    ".markdownlint-cli2.jsonc is the single source of truth",
                )


GLOBAL_INSTRUCTIONS = ".github/copilot-instructions.md"
GLOBAL_INSTRUCTIONS_MAX_LINES = 100


def check_global_instructions_size(reporter: Reporter) -> None:
    """Limit repository instructions, which are injected into every request."""
    if not (REPO_ROOT / GLOBAL_INSTRUCTIONS).is_file():
        return
    count = len(read_text(GLOBAL_INSTRUCTIONS).splitlines())
    if count > GLOBAL_INSTRUCTIONS_MAX_LINES:
        reporter.error(
            "global-instructions-size", GLOBAL_INSTRUCTIONS, count,
            f"{count} lines exceed the {GLOBAL_INSTRUCTIONS_MAX_LINES}-line limit; "
            "this file loads in every Copilot request. Move path-specific rules "
            "to .github/instructions/*.instructions.md "
            "(see .github/PRIMITIVE-STANDARD.md)",
        )


def check_event_terminology(text_files: list[str], reporter: Reporter) -> None:
    for rel in text_files:
        if rel in TERMINOLOGY_EXEMPT_FILES:
            continue
        source = iter_prose(rel) if rel.lower().endswith(
            ".md") else _iter_all_lines(rel)
        for lineno, line in source:
            if EVENT_TERM_RE.search(EVENT_TERM_ALLOWED_RE.sub("", line)):
                reporter.error(
                    "policy-event-term", rel, lineno,
                    "call the event an immersion; \"workshop\", \"hackathon\" "
                    "and \"hackaton\" are forbidden",
                )


def check_stale_paths(text_files: list[str], reporter: Reporter) -> None:
    for rel in text_files:
        if rel in POLICY_EXEMPT_FILES:
            continue
        source = iter_prose(rel) if rel.lower().endswith(
            ".md") else _iter_all_lines(rel)
        for lineno, line in source:
            match = STALE_RE.search(line)
            if match:
                reporter.error(
                    "policy-stale-path", rel, lineno,
                    f"stale directory name '{match.group(0)}' (the repository was renamed; "
                    "update to the current path)",
                )


def _iter_all_lines(rel: str):
    for lineno, line in enumerate(read_text(rel).split("\n"), start=1):
        yield lineno, line


def check_competing_tools(markdown_files: list[str], reporter: Reporter) -> None:
    for rel in markdown_files:
        if rel in POLICY_EXEMPT_FILES:
            continue
        lines = read_text(rel).split("\n")
        mask = fence_mask(lines)
        for lineno, raw in enumerate(lines, start=1):
            if mask[lineno - 1]:
                continue
            _scan_competing_line(rel, lineno, raw, reporter)


def _scan_competing_line(rel: str, lineno: int, line: str, reporter: Reporter) -> None:
    for match in TOOL_RE.finditer(line):
        clause, tool_start = _recommendation_clause(
            line, match.start(), match.end())
        window = clause[max(0, tool_start - RECOMMEND_WINDOW):tool_start]
        if not RECOMMEND_VERB_RE.search(window):
            continue
        if NEGATION_RE.search(clause) or INTERROGATIVE_RE.search(clause):
            continue
        reporter.error(
            "policy-competing-tool", rel, lineno,
            f"appears to recommend '{match.group(1)}'; only the approved toolchain "
            "(VS Code + GitHub Copilot) may be recommended",
        )
        return


def _recommendation_clause(line: str, start: int, end: int) -> tuple[str, int]:
    """Isolate the clause containing the tool and return its local offset."""
    cuts = _clause_cuts(line)
    left = max(position for position in cuts if position <= start)
    right = min(position for position in cuts if position >= end)
    return line[left:right], start - left


def _clause_cuts(line: str) -> list[int]:
    cuts = {0, len(line)}
    for index, character in enumerate(line):
        if character in HARD_CLAUSE_BOUNDARIES:
            cuts.add(index + 1)
        elif character == "." and _is_sentence_period(line, index):
            cuts.add(index + 1)
    cuts.update(match.end() for match in CONTRAST_BOUNDARY_RE.finditer(line))
    return sorted(cuts)


def _is_sentence_period(line: str, index: int) -> bool:
    next_index = index + 1
    if index > 0:
        initial = line[index - 1].lower()
        remainder = line[next_index:]
        if initial == "p" and re.match(r"\s*ex\.", remainder, re.IGNORECASE):
            return False
    if next_index < len(line) and not line[next_index].isspace():
        return False
    if index > 0 and next_index < len(line):
        if line[index - 1].isdigit() and line[next_index].isdigit():
            return False
    token_match = re.search(r"([A-Za-zÀ-ÿ.]+)$", line[:index])
    token = token_match.group(1).lower() if token_match else ""
    if token == "etc":
        following = line[next_index:].lstrip()
        return not following or following[0].isupper()
    return token not in PERIOD_ABBREVIATIONS


# --- File set selectors ---------------------------------------------------

def match(rel: str, pattern: str) -> bool:
    return re.match(pattern, rel) is not None


def main() -> int:
    reporter = Reporter()
    # A fresh CI checkout materializes every tracked file, but a local tree may
    # list files left in the index by a concurrent rename after removal on disk.
    # Restrict checks to existing files so reading them never fails.
    files = [f for f in tracked_files() if (REPO_ROOT / f).is_file()]

    agent_files = [f for f in files if match(
        f, r"\.github/agents/[^/]+\.agent\.md$")]
    prompt_files = [f for f in files if match(
        f, r"\.github/prompts/[^/]+\.prompt\.md$")]
    instruction_files = [f for f in files if match(
        f, r"\.github/instructions/[^/]+\.instructions\.md$")]
    skill_files = [f for f in files if match(
        f, r"\.github/skills/[^/]+/SKILL\.md$")]
    hook_files = [f for f in files if match(f, r"\.github/hooks/[^/]+\.json$")]
    subdir_hook_files = [f for f in files if match(
        f, r"\.github/hooks/[^/]+/.+/?hooks\.json$")]
    github_markdown = [f for f in files if f.startswith(
        ".github/") and f.lower().endswith(".md")]
    all_markdown = [f for f in files if f.lower().endswith(".md")]
    text_files = [
        f for f in files
        if not looks_binary(read_bytes(f))
    ]

    valid_agent_ids = build_agent_registry(agent_files, reporter)

    check_agents(agent_files, reporter)
    check_prompts(prompt_files, valid_agent_ids, reporter)
    check_instructions(instruction_files, reporter)
    check_skills(skill_files, reporter)
    check_handoffs(agent_files, valid_agent_ids, reporter)

    check_hooks(hook_files, subdir_hook_files, reporter)

    for rel in github_markdown:
        # GitHub issue, pull request, and discussion templates intentionally
        # omit H1: frontmatter `name:` supplies the title rendered by GitHub.
        # Their links are still checked.
        if not match(rel, r"\.github/(ISSUE_TEMPLATE|PULL_REQUEST_TEMPLATE|DISCUSSION_TEMPLATE)(/|\.md$)"):
            check_markdown_structure(rel, reporter)
        check_markdown_links(rel, reporter)

    check_pragmas(all_markdown, reporter)
    check_global_instructions_size(reporter)
    check_event_terminology(text_files, reporter)
    check_stale_paths(text_files, reporter)
    check_competing_tools(all_markdown, reporter)

    reporter.summarize()

    counts = (
        f"agents={len(agent_files)} prompts={len(prompt_files)} "
        f"instructions={len(instruction_files)} skills={len(skill_files)} "
        f"hooks={len(hook_files)} markdown-github={len(github_markdown)}"
    )
    print(f"Checked: {counts}")
    return 1 if reporter.error_count else 0


if __name__ == "__main__":
    sys.exit(main())
