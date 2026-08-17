#!/usr/bin/env python3
"""Temporary one-shot translator for the cn branch.

Translates only the explicitly listed historical Markdown files. It preserves
fenced/indented code, inline code, link destinations, URLs, HTML tags, and
Markdown structure as much as possible. This helper is removed after the run.
"""

from __future__ import annotations

import re
import time
from pathlib import Path

import argostranslate.package
import argostranslate.translate

TARGETS = [
    "RELEASE-NOTES.md",
    "docs/porting-to-a-new-harness.md",
    "docs/superpowers/plans/2026-01-22-document-review-system.md",
    "docs/superpowers/plans/2026-02-19-visual-brainstorming-refactor.md",
    "docs/superpowers/plans/2026-03-11-zero-dep-brainstorm-server.md",
    "docs/superpowers/plans/2026-03-23-codex-app-compatibility.md",
    "docs/superpowers/plans/2026-04-06-worktree-rototill.md",
    "docs/superpowers/plans/2026-05-06-lift-drill-into-evals.md",
    "docs/superpowers/plans/2026-05-07-pi-extension-and-evals.md",
    "docs/superpowers/plans/2026-06-09-sdd-task-scoped-review-dispatch.md",
    "docs/superpowers/plans/2026-06-09-visual-companion-issues.md",
    "docs/superpowers/plans/2026-06-10-visual-companion-auth-hardening.md",
    "docs/superpowers/plans/2026-06-11-visual-companion-final-hardening-fixup.md",
    "docs/superpowers/plans/2026-07-06-sdd-plan-scoped-workspace.md",
    "docs/superpowers/plans/2026-07-15-sdd-fix-loop-redesign.md",
    "docs/superpowers/plans/2026-07-30-codex-efficiency-fixes.md",
    "docs/superpowers/plans/2026-08-06-hermes-version-bump-wiring.md",
    "docs/superpowers/specs/2026-01-22-document-review-system-design.md",
    "docs/superpowers/specs/2026-02-19-visual-brainstorming-refactor-design.md",
    "docs/superpowers/specs/2026-03-11-zero-dep-brainstorm-server-design.md",
    "docs/superpowers/specs/2026-03-23-codex-app-compatibility-design.md",
    "docs/superpowers/specs/2026-04-06-worktree-rototill-design.md",
    "docs/superpowers/specs/2026-05-05-platform-neutral-config-refs-design.md",
    "docs/superpowers/specs/2026-05-05-platform-neutral-prose-design.md",
    "docs/superpowers/specs/2026-05-05-platform-neutral-readme-design.md",
    "docs/superpowers/specs/2026-05-06-lift-drill-into-evals-design.md",
    "docs/superpowers/specs/2026-06-09-sdd-task-scoped-review-dispatch-design.md",
    "docs/superpowers/specs/2026-06-10-positive-instruction-redesign-design.md",
    "docs/superpowers/specs/2026-06-10-strict-cost-sdd-design.md",
    "docs/superpowers/specs/2026-06-10-visual-companion-auth-hardening-design.md",
    "docs/superpowers/specs/2026-06-11-visual-companion-final-hardening-fixup-design.md",
    "docs/superpowers/specs/2026-07-06-sdd-plan-scoped-workspace-eval-results.md",
    "docs/superpowers/specs/2026-07-06-sdd-plan-scoped-workspace.md",
    "docs/superpowers/specs/2026-07-15-sdd-fix-loop-redesign-design.md",
    "docs/superpowers/specs/2026-07-30-codex-efficiency-fixes-design.md",
    "docs/superpowers/specs/2026-08-05-hermes-version-bump-wiring-design.md",
]

FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_SEP_RE = re.compile(r"^\s*:?-{3,}:?\s*$")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
HTML_RE = re.compile(r"<[^>\n]+>")
LINK_DEST_RE = re.compile(r"(?<=\]\()[^)\n]+(?=\))")
REF_DEST_RE = re.compile(r"^(\s*\[[^\]]+\]:\s*)(\S+)(.*)$")
MARKDOWN_PREFIX_RE = re.compile(
    r"^(\s*(?:#{1,6}\s+|>\s*|[-+*]\s+(?:\[[ xX]\]\s+)?|\d+[.)]\s+)?)(.*)$"
)

PROTECTED_PATTERNS = [INLINE_CODE_RE, URL_RE, LINK_DEST_RE, HTML_RE]


def install_model() -> None:
    argostranslate.package.update_package_index()
    packages = argostranslate.package.get_available_packages()
    matches = [p for p in packages if p.from_code == "en" and p.to_code in {"zh", "zh-CN"}]
    if not matches:
        raise RuntimeError("No Argos English→Chinese package found")
    pkg = matches[0]
    download_path = pkg.download()
    argostranslate.package.install_from_path(download_path)


def should_translate(text: str) -> bool:
    if not text.strip():
        return False
    if not re.search(r"[A-Za-z]", text):
        return False
    # Pure paths, flags, identifiers, and separator-like content should stay exact.
    stripped = text.strip()
    if TABLE_SEP_RE.fullmatch(stripped):
        return False
    if re.fullmatch(r"[-_=*`~|:./\\\[\](){}<>0-9A-Za-z_+@#$%^&!?]+", stripped):
        if " " not in stripped:
            return False
    return True


def protect(text: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    counter = 0

    # Reference-style link destinations need special handling because they may be local paths.
    m = REF_DEST_RE.match(text)
    if m:
        token = f"ZXQPROT{counter:04d}QXZ"
        counter += 1
        mapping[token] = m.group(2)
        text = m.group(1) + token + m.group(3)

    for pattern in PROTECTED_PATTERNS:
        while True:
            m = pattern.search(text)
            if not m:
                break
            token = f"ZXQPROT{counter:04d}QXZ"
            counter += 1
            mapping[token] = m.group(0)
            text = text[: m.start()] + token + text[m.end() :]
    return text, mapping


def restore(text: str, mapping: dict[str, str]) -> str:
    for token, value in mapping.items():
        # Argos may introduce spaces around a token; accept those variants.
        text = re.sub(r"\s*" + re.escape(token) + r"\s*", value, text)
    return text


def translate_piece(text: str) -> str:
    if not should_translate(text):
        return text
    protected, mapping = protect(text)
    try:
        out = argostranslate.translate.translate(protected, "en", "zh")
    except Exception:
        # One retry after a brief pause; fail hard if it still does not work.
        time.sleep(0.2)
        out = argostranslate.translate.translate(protected, "en", "zh")
    return restore(out, mapping)


def translate_table_line(line: str) -> str:
    # Preserve pipe layout and separator cells.
    parts = line.split("|")
    out: list[str] = []
    for part in parts:
        left = len(part) - len(part.lstrip())
        right = len(part) - len(part.rstrip())
        core = part.strip()
        if not core or TABLE_SEP_RE.fullmatch(core):
            translated = core
        else:
            translated = translate_piece(core)
        out.append(" " * left + translated + " " * right)
    return "|".join(out)


def translate_markdown(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    in_frontmatter = bool(lines and lines[0].strip() == "---")
    frontmatter_end_seen = False

    for idx, raw in enumerate(lines):
        newline = "\n" if raw.endswith("\n") else ""
        line = raw[:-1] if newline else raw

        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            out.append(raw)
            continue

        if in_fence:
            out.append(raw)
            continue

        # Preserve indented code lines. This intentionally favors structural safety over translation.
        if line.startswith("    ") and line.strip():
            out.append(raw)
            continue

        # Preserve frontmatter keys and machine-facing scalar values.
        if in_frontmatter and not frontmatter_end_seen:
            if idx > 0 and line.strip() == "---":
                frontmatter_end_seen = True
                out.append(raw)
                continue
            # Translate only natural-language description values; leave all other keys/values exact.
            m = re.match(r"^(\s*description:\s*)(.*)$", line)
            if m:
                out.append(m.group(1) + translate_piece(m.group(2)) + newline)
            else:
                out.append(raw)
            continue

        if not line.strip():
            out.append(raw)
            continue

        if "|" in line and line.count("|") >= 2:
            out.append(translate_table_line(line) + newline)
            continue

        m = MARKDOWN_PREFIX_RE.match(line)
        assert m is not None
        prefix, body = m.groups()
        if body.strip():
            body = translate_piece(body)
        out.append(prefix + body + newline)

    return "".join(out)


def main() -> None:
    install_model()
    changed = []
    for rel in TARGETS:
        path = Path(rel)
        if not path.exists():
            raise FileNotFoundError(rel)
        original = path.read_text(encoding="utf-8")
        translated = translate_markdown(original)
        if translated == original:
            raise RuntimeError(f"Translation produced no changes for {rel}")
        path.write_text(translated, encoding="utf-8")
        changed.append(rel)
        print(f"translated: {rel}")
    print(f"translated {len(changed)} files")


if __name__ == "__main__":
    main()
