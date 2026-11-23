#!/usr/bin/env python3
"""
eoto Markdown Documentation Linter (ASD-STE100 & Canonical Glossary Guardrail).

Checks Markdown files for:
1. [ERROR] STE-8.1: Prohibition of semicolons (';' and '；') outside code blocks/spans.
2. [ERROR] GLOSSARY-ALIAS: Non-canonical / prohibited term aliases (skipped on standards docs,
           downgraded to WARN on exploratory docs under docs/research/).
3. [WARN]  STE-PARAGRAPH: Paragraphs exceeding 6 sentences.
4. [WARN]  STE-LENGTH: Sentences exceeding 40 Chinese chars (or 25 English words).
5. [WARN]  STE-VERB: Prohibited English perfect tenses or common phrasal verbs.
6. [WARN]  STE-NOMINAL: Common Chinese nominalization / empty-verb patterns.

Usage:
    python3 check_docs.py [path ...]
"""

from __future__ import annotations

import pathlib
import re
import sys
from dataclasses import dataclass

# Prohibited aliases mapped to their canonical eoto replacement.
# Only unambiguous aliases are listed here to avoid false positives.
PROHIBITED_ALIASES: list[tuple[str, str]] = [
    ("企微", "企业微信"),
    ("主 AI 大脑", "`eoto Core`"),
    ("总控大脑", "`eoto Core`"),
    ("对话壳子", "`eoto Link`"),
    ("聊天壳子", "`eoto Link`"),
    ("子智能体", "子 Agent"),
    ("插件/配置层", "`eoto Studio`"),
    ("AI 原生企业一体化平台", "`eoto`"),
    ("人工介入", "人工确认"),
    ("人工兜底", "人工确认"),
    ("记账报税", "核算报税"),
    ("做账报税", "核算报税"),
    ("WXWork", "企业微信 / WeCom"),
]

# English prohibited verb patterns (perfect tenses & common phrasal verbs).
EN_VERB_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(have|has|had)\s+(been|[a-z]+ed|received|done|made|taken|built)\b", re.I),
     "Avoid perfect tense (use simple past/present)"),
    (re.compile(r"\b(set up|carry out|turn off|turn on|find out|put off|bring up)\b", re.I),
     "Avoid phrasal verb (STE Rule 9.3)"),
]

# Chinese empty-verb / nominalization patterns to review.
ZH_NOMINAL_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"进行了[^，。！？\n]{1,12}"), "Avoid nominalization with '进行了' (STE Rule 3.7)"),
    (re.compile(r"开展了[^，。！？\n]{1,12}"), "Avoid nominalization with '开展了' (STE Rule 3.7)"),
    (re.compile(r"加以[^，。！？\n]{1,8}"), "Avoid empty verb '加以' (STE Rule 3.7)"),
]

STANDARDS_EXEMPT_NAMES = {"统一术语表.md", "文档写作规范.md", "glossary.md", "ste-writing-rules.md"}

# Exploratory docs may quote customers verbatim, so glossary aliases are warnings there.
EXPLORATORY_DIR_NAMES = {"research"}


@dataclass
class Issue:
    path: str
    line: int
    severity: str  # ERROR or WARN
    code: str
    message: str


def strip_inline_code_and_urls(text: str) -> str:
    """Remove inline code spans and markdown link URLs so only visible prose is checked."""
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"&[a-zA-Z0-9#]+;", " ", text)
    return text


def split_sentences(text: str) -> list[str]:
    """Split a paragraph into sentences on Chinese/English sentence terminators."""
    cleaned = strip_inline_code_and_urls(text)
    # Remove markdown emphasis markers
    cleaned = re.sub(r"[*_~]+", "", cleaned)
    parts = re.split(r"[。！？!?]+|(?<!\d)\.(?!\d)(?:\s+|$)", cleaned)
    return [p.strip() for p in parts if p.strip()]


def count_sentence_units(sentence: str) -> tuple[int, bool]:
    """Return (unit_count, is_chinese_dominant).

    For Chinese-dominant sentences, count each CJK char as 1 unit and each English word/number as 1 unit.
    For English-only sentences, count English words.
    """
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", sentence)
    en_words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", sentence)
    if cjk_chars:
        return len(cjk_chars) + len(en_words), True
    return len(en_words), False


def collect_markdown_files(paths: list[str]) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for raw in paths:
        p = pathlib.Path(raw)
        if p.is_file() and p.suffix.lower() == ".md":
            files.append(p)
        elif p.is_dir():
            for child in sorted(p.rglob("*.md")):
                files.append(child)
    return files


def check_file(path: pathlib.Path) -> list[Issue]:
    issues: list[Issue] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    is_standards_doc = path.name in STANDARDS_EXEMPT_NAMES
    is_exploratory_doc = any(part in EXPLORATORY_DIR_NAMES for part in path.parts)

    in_fenced_code = False
    in_frontmatter = False
    paragraph_lines: list[tuple[int, str]] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        start_line = paragraph_lines[0][0]
        joined = " ".join(text.strip() for _, text in paragraph_lines)
        sentences = split_sentences(joined)
        if len(sentences) > 6:
            issues.append(Issue(
                path=str(path),
                line=start_line,
                severity="WARN",
                code="STE-PARAGRAPH",
                message=f"Paragraph has {len(sentences)} sentences (max 6).",
            ))
        for s in sentences:
            units, is_zh = count_sentence_units(s)
            limit = 40 if is_zh else 25
            if units > limit:
                preview = s[:48] + ("..." if len(s) > 48 else "")
                unit_label = "units" if is_zh else "words"
                issues.append(Issue(
                    path=str(path),
                    line=start_line,
                    severity="WARN",
                    code="STE-LENGTH",
                    message=f"Sentence has {units} {unit_label} (max {limit}): '{preview}'",
                ))
        paragraph_lines.clear()

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip YAML frontmatter at top of file
        if idx == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue

        # Toggle fenced code blocks
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush_paragraph()
            in_fenced_code = not in_fenced_code
            continue
        if in_fenced_code:
            continue

        prose = strip_inline_code_and_urls(line)

        # 1. STE-8.1: No semicolons anywhere in prose (including tables and lists)
        if ";" in prose or "；" in prose:
            issues.append(Issue(
                path=str(path),
                line=idx,
                severity="ERROR",
                code="STE-8.1",
                message="Semicolon (';' or '；') is strictly prohibited. Split into separate sentences or a list.",
            ))

        # 2. Glossary prohibited aliases (skip standards definition docs)
        if not is_standards_doc:
            for alias, canonical in PROHIBITED_ALIASES:
                if alias in prose:
                    issues.append(Issue(
                        path=str(path),
                        line=idx,
                        severity="WARN" if is_exploratory_doc else "ERROR",
                        code="GLOSSARY-ALIAS",
                        message=f"Prohibited alias '{alias}' found. Use canonical term: {canonical}.",
                    ))

        # 3. English verb / phrasal verb patterns (skip standards examples docs)
        if not is_standards_doc:
            for pattern, reason in EN_VERB_PATTERNS:
                m = pattern.search(prose)
                if m:
                    issues.append(Issue(
                        path=str(path),
                        line=idx,
                        severity="WARN",
                        code="STE-VERB",
                        message=f"{reason}: '{m.group(0)}'",
                    ))

            for pattern, reason in ZH_NOMINAL_PATTERNS:
                m = pattern.search(prose)
                if m:
                    issues.append(Issue(
                        path=str(path),
                        line=idx,
                        severity="WARN",
                        code="STE-NOMINAL",
                        message=f"{reason}: '{m.group(0)}'",
                    ))

        # Collect plain prose paragraphs for paragraph/sentence length checks
        is_non_paragraph = (
            not stripped
            or stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith(">")
            or stripped.startswith("---")
            or stripped.startswith("***")
            or re.match(r"^[-*+]\s+", stripped) is not None
            or re.match(r"^\d+\.\s+", stripped) is not None
        )
        if is_non_paragraph:
            flush_paragraph()
        else:
            paragraph_lines.append((idx, stripped))

    flush_paragraph()
    return issues


def main() -> int:
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["docs", "README.md", "AGENTS.md"]
    files = collect_markdown_files(targets)
    if not files:
        print("No Markdown files found.")
        return 0

    all_issues: list[Issue] = []
    for f in files:
        all_issues.extend(check_file(f))

    errors = [i for i in all_issues if i.severity == "ERROR"]
    warnings = [i for i in all_issues if i.severity == "WARN"]

    for issue in all_issues:
        print(f"[{issue.severity}] {issue.path}:{issue.line} ({issue.code}) {issue.message}")

    print(
        f"\nChecked {len(files)} file(s): {len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
