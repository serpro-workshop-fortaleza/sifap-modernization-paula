#!/usr/bin/env python3
"""Validate legacy sources and report requirement references in tests."""

import argparse
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[2]
REQUIREMENT_ID = r"REQ-(?:\d+|[A-Z]+(?:-[A-Z]+)*-\d+)"
DECLARATION = re.compile(
    rf"^\s*(?:#{{1,6}}\s+(?P<heading>{REQUIREMENT_ID})(?=\s|:|$)|"
    rf"(?:[-*]\s+)?(?:\*\*)?(?P<key>{REQUIREMENT_ID})(?:\*\*)?"
    r"(?:\s+\([^)]+\))?(?:\s*:|\s+-|\s*$))"
)
REFERENCE = re.compile(rf"\b({REQUIREMENT_ID})\b")
SOURCE = re.compile(r"source_legacy\s*:(.+)")
LEGACY_SOURCE = re.compile(
    r"01-archaeology/legacy-sifap/"
    r"(?:natural-programs/[A-Za-z0-9_-]+\."
    r"(?:NSP|NSN|NSS|NSA|NSL|NSC|NSM|jcl)|"
    r"adabas-ddms/[A-Za-z0-9_-]+\.(?:NSD|ddm|txt))"
    r"(?:#L[1-9]\d*(?:-L[1-9]\d*)?)?$"
)
GREENFIELD_SOURCE = re.compile(r"\[GREENFIELD\]\s+\S(?:.*\S)?$")


def declared_requirements(lines):
    return [
        (line_number, match.group("heading") or match.group("key"))
        for line_number, line in enumerate(lines)
        if (match := DECLARATION.match(line))
    ]


def source_value_is_valid(value, repo_root):
    value = value.strip()
    if value[:1] in {"'", '"'}:
        if len(value) < 2 or value[-1:] != value[:1]:
            return False
        value = value[1:-1].strip()
    elif value[-1:] in {"'", '"'}:
        return False
    if GREENFIELD_SOURCE.fullmatch(value):
        return True
    if not LEGACY_SOURCE.fullmatch(value):
        return False
    return (repo_root / value.split("#", maxsplit=1)[0]).is_file()


def validate_legacy_sources(documents, repo_root):
    failures = []
    requirements_found = 0
    for document_path, lines in documents:
        requirements = declared_requirements(lines)
        requirements_found += len(requirements)
        for index, (line_number, requirement) in enumerate(requirements):
            next_line = (
                requirements[index + 1][0]
                if index + 1 < len(requirements) else len(lines)
            )
            end_line = min(line_number + 21, next_line)
            sources = [
                match.group(1)
                for line in lines[line_number + 1:end_line]
                if (match := SOURCE.fullmatch(line.strip()))
            ]
            if not any(
                source_value_is_valid(value, repo_root) for value in sources
            ):
                relative_path = document_path.relative_to(repo_root)
                failures.append(
                    f"{relative_path}:{line_number + 1}: {requirement}"
                )
    if failures:
        print(
            "::error::Every REQ-ID needs a valid source_legacy within the "
            "next 20 lines and before the next requirement."
        )
        print("\n".join(failures))
        return 1
    if requirements_found:
        print("All declared requirements have a valid source_legacy.")
    else:
        print("No declared requirements found in specs/.")
    return 0


def is_test_file(file_path):
    return (
        "tests" in file_path.parts
        or "__tests__" in file_path.parts
        or ".test." in file_path.name
        or ".spec." in file_path.name
    )


def test_files(repo_root):
    test_roots = (
        ("backend/src/test", True),
        ("frontend", False),
        ("site/tests", False),
    )
    for directory_name, all_files_are_tests in test_roots:
        directory = repo_root / directory_name
        if not directory.is_dir():
            continue
        for file_path in sorted(directory.rglob("*")):
            if not file_path.is_file():
                continue
            relative_path = file_path.relative_to(repo_root)
            if not all_files_are_tests and not is_test_file(relative_path):
                continue
            yield file_path


def report_test_traceability(documents, repo_root):
    requirements = {
        requirement for _document_path, lines in documents
        for _line_number, requirement in declared_requirements(lines)
    }
    test_requirements = set()
    for file_path in test_files(repo_root):
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            relative_path = file_path.relative_to(repo_root)
            print(
                f"::warning file={relative_path}::"
                "Skipped a non-UTF-8 test artifact."
            )
            continue
        test_requirements.update(REFERENCE.findall(text))
    missing = sorted(requirements - test_requirements)
    if missing:
        print("::warning::Requirements not yet referenced by automated tests:")
        print("\n".join(missing))
    elif requirements:
        print("All declared requirements are referenced by automated tests.")
    else:
        print("No declared requirements found in specs/.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=REPO_ROOT,
        help="Repository root; defaults to this script's repository.",
    )
    parser.add_argument(
        "--mode", choices=("all", "legacy", "tests"), default="all",
        help="Run the source gate, warning-only test report, or both.",
    )
    arguments = parser.parse_args(argv)
    repo_root = arguments.repo_root.resolve()
    if not repo_root.is_dir():
        parser.error("--repo-root must be an existing directory")
    specs_directory = repo_root / "specs"
    if not specs_directory.is_dir():
        print("No specifications directory (specs/); checks skipped.")
        return 0
    documents = [
        (file_path, file_path.read_text(
            encoding="utf-8", errors="ignore",
        ).splitlines())
        for file_path in sorted(specs_directory.rglob("*"))
        if file_path.is_file()
    ]
    exit_code = 0
    if arguments.mode in {"all", "legacy"}:
        exit_code = validate_legacy_sources(documents, repo_root)
    if arguments.mode in {"all", "tests"}:
        report_test_traceability(documents, repo_root)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
