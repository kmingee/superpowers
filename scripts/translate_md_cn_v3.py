#!/usr/bin/env python3
"""Patch the temporary cn translator so nested protected tokens restore safely."""

import re
from scripts import translate_md_cn as base


def restore_nested(text: str, mapping: dict[str, str]) -> str:
    # Protection can be nested (e.g. a URL inside a Markdown link destination,
    # or a URL inside an HTML tag). Restore in reverse creation order so the
    # outer token expands first and exposes the inner token before it is restored.
    for token, value in reversed(list(mapping.items())):
        text = re.sub(r"\s*" + re.escape(token) + r"\s*", value, text)
    return text


base.restore = restore_nested

if __name__ == "__main__":
    base.main()
