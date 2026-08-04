"""Fase 4: rebuilds assets/css/home.bundle.css, dropping top-level CSS rules
that have zero selector overlap with classes/ids used by index.html (static
markup + classes injected by its own JS via classList/innerHTML).

Only index.html loads home.bundle.css (verified: `grep -rl home.bundle.css`
returns just index.html), so this is safe to prune aggressively without
touching main.css/site-v2.css/motion.css/soulcont-brand.css themselves --
those files are still served unmodified, in full, to every other page.

Conservative rules, matching the ones enforced in tools/qa/css_usage_audit.py:
  - @-rules (@media, @supports, @keyframes, @font-face, ...) are always kept
    whole, never parsed/pruned internally.
  - A normal rule is dropped only if its selector contains at least one
    class/id token AND none of those tokens are in the used-token set.
  - Tag-only / pseudo-only selectors (no class or id token) are always kept.
  - cookies.css, mediaquery.css and hero-background.css are copied through
    unfiltered: cookies.css is almost entirely classes injected at runtime
    by cookies.js (innerHTML), and the other two had zero unused top-level
    rules in the audit, so pruning them buys nothing.

Run this after editing index.html or its JS if class usage changes, and
re-run tools/qa/css_usage_audit.py first to sanity-check the used-token set.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILES = [
    "assets/css/main.css",
    "assets/css/mediaquery.css",
    "assets/css/cookies.css",
    "assets/css/site-v2.css",
    "assets/css/motion.css",
    "assets/css/hero-background.css",
    "assets/css/soulcont-brand.css",
]

UNFILTERED_FILES = {
    "assets/css/mediaquery.css",
    "assets/css/cookies.css",
    "assets/css/hero-background.css",
}

JS_FILES = [
    "assets/js/menu.js",
    "assets/js/cookies.js",
    "assets/js/footer.js",
    "assets/js/motion.js",
    "assets/js/main.js",
    "assets/js/soulcont-brand.js",
]

TOKEN_RE = re.compile(r"[.#][a-zA-Z_-][\w-]*")


def used_tokens() -> set[str]:
    used: set[str] = set()
    html_source = (ROOT / "index.html").read_text(encoding="utf-8")

    for cls in re.findall(r'class="([^"]*)"', html_source):
        used.update("." + t for t in cls.split())
    for id_ in re.findall(r'id="([^"]*)"', html_source):
        used.add("#" + id_)

    for js_rel in JS_FILES:
        js_source = (ROOT / js_rel).read_text(encoding="utf-8", errors="ignore")
        for m in re.findall(r'''classList\.(?:add|remove|toggle|contains)\(\s*['"]([^'"]+)['"]''', js_source):
            used.add("." + m)
        for m in re.findall(r'''querySelector(?:All)?\(\s*['"]([^'"]+)['"]''', js_source):
            used.update(TOKEN_RE.findall(m))
        for m in re.findall(r'''\.className\s*=\s*['"]([^'"]+)['"]''', js_source):
            used.update("." + t for t in m.split())
        for m in re.findall(r'''getElementById\(\s*['"]([^'"]+)['"]''', js_source):
            used.add("#" + m)
        for m in re.findall(r'''class=["']([^"']+)["']''', js_source):
            used.update("." + t for t in m.split())
        for m in re.findall(r'''\bid=["']([^"']+)["']''', js_source):
            used.add("#" + m)

    return used


def filter_css(css: str, used: set[str]) -> tuple[str, int, int]:
    """Removes unused top-level rules in place, preserving order/whitespace
    of everything else. Returns (filtered_css, kept_rule_bytes, dropped_bytes).
    """
    out: list[str] = []
    i, n = 0, len(css)
    dropped_bytes = 0
    kept_bytes = 0

    while i < n:
        if css.startswith("/*", i):
            end = css.index("*/", i) + 2
            out.append(css[i:end])
            i = end
            continue

        if css[i] == "@":
            # @-rule: keep whole, whether block ({...}) or statement (;)
            j = i
            depth = 0
            while j < n:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                elif css[j] == ";" and depth == 0:
                    j += 1
                    break
                j += 1
            out.append(css[i:j])
            kept_bytes += j - i
            i = j
            continue

        if css[i] in " \t\r\n":
            out.append(css[i])
            i += 1
            continue

        # Regular rule: selector { body }
        brace = css.index("{", i)
        selector = css[i:brace]
        depth = 1
        k = brace + 1
        while depth > 0 and k < n:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        rule_text = css[i:k]

        tokens = TOKEN_RE.findall(selector)
        keep = (not tokens) or any(tok in used for tok in tokens)
        if keep:
            out.append(rule_text)
            kept_bytes += len(rule_text)
        else:
            dropped_bytes += len(rule_text)
        i = k

    return "".join(out), kept_bytes, dropped_bytes


def main() -> None:
    used = used_tokens()
    sections = []
    total_dropped = 0

    for rel in SOURCE_FILES:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        normalized = (
            source.replace("﻿", "")
            .removeprefix('@charset "UTF-8";')
            .strip()
        )
        # tolerate the exact original stripping behaviour of build-home-css.mjs
        normalized = re.sub(r'^@charset\s+["\']UTF-8["\'];?\s*', "", normalized, flags=re.I)
        normalized = re.sub(r"[ \t]+$", "", normalized, flags=re.M)

        if rel in UNFILTERED_FILES:
            filtered = normalized
            dropped = 0
        else:
            filtered, _kept, dropped = filter_css(normalized, used)
        total_dropped += dropped

        sections.append(f"/* Source: {rel} */\n{filtered.strip()}\n")
        print(f"{rel}: dropped {dropped} bytes of confirmed-unused top-level CSS")

    output = '@charset "UTF-8";\n\n' + "\n".join(sections)
    output_path = ROOT / "assets/css/home.bundle.css"
    output_path.write_text(output, encoding="utf-8", newline="\n")
    print(f"\nGenerated {output_path.relative_to(ROOT)} ({len(output.encode('utf-8'))} bytes)")
    print(f"Total bytes removed vs. plain concatenation: {total_dropped}")


if __name__ == "__main__":
    main()
