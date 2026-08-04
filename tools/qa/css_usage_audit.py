"""Fase 4 helper: finds CSS rules in the home bundle's source files that have
zero selector overlap with classes/ids actually referenced by index.html or
by the JS files it loads (static HTML *and* dynamic classList usage).

Conservative by design: only flags top-level (non @media) rules, and only
when every class/id token in the rule's selector list is absent from the
used-token set. Nothing is deleted automatically; this only reports.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILES = [
    "assets/css/main.css",
    "assets/css/mediaquery.css",
    "assets/css/cookies.css",
    "assets/css/site-v2.css",
    "assets/css/motion.css",
    "assets/css/hero-background.css",
    "assets/css/soulcont-brand.css",
]

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
        for token in cls.split():
            used.add("." + token)
    for id_ in re.findall(r'id="([^"]*)"', html_source):
        used.add("#" + id_)

    for js_rel in JS_FILES:
        js_source = (ROOT / js_rel).read_text(encoding="utf-8", errors="ignore")
        for m in re.findall(r'''classList\.(?:add|remove|toggle|contains)\(\s*['"]([^'"]+)['"]''', js_source):
            used.add("." + m)
        for m in re.findall(r'''querySelector(?:All)?\(\s*['"]([^'"]+)['"]''', js_source):
            for token in TOKEN_RE.findall(m):
                used.add(token)
        for m in re.findall(r'''\.className\s*=\s*['"]([^'"]+)['"]''', js_source):
            for token in m.split():
                used.add("." + token)
        for m in re.findall(r'''getElementById\(\s*['"]([^'"]+)['"]''', js_source):
            used.add("#" + m)
        # HTML injected via innerHTML/template literals: class="a b c" or class='a b c'
        for m in re.findall(r'''class=["']([^"']+)["']''', js_source):
            for token in m.split():
                used.add("." + token)
        for m in re.findall(r'''\bid=["']([^"']+)["']''', js_source):
            used.add("#" + m)

    return used


RULE_RE = re.compile(r"([^{}@]+)\{([^{}]*)\}")


def strip_media_blocks(css: str) -> tuple[str, int]:
    """Removes @media {...} blocks (balanced) and returns (remaining_css, media_byte_count)."""
    out = []
    i = 0
    media_bytes = 0
    n = len(css)
    while i < n:
        if css.startswith("@media", i) or css.startswith("@supports", i):
            start = i
            depth = 0
            j = css.index("{", i)
            depth = 1
            k = j + 1
            while depth > 0 and k < n:
                if css[k] == "{":
                    depth += 1
                elif css[k] == "}":
                    depth -= 1
                k += 1
            media_bytes += k - start
            i = k
        else:
            out.append(css[i])
            i += 1
    return "".join(out), media_bytes


def analyze(path: Path, used: set[str]) -> None:
    css = path.read_text(encoding="utf-8", errors="ignore")
    top_level, media_bytes = strip_media_blocks(css)

    unused_bytes = 0
    unused_rules: list[str] = []
    for selector, body in RULE_RE.findall(top_level):
        selector = selector.strip()
        if not selector or selector.startswith(("/*", "@")):
            continue
        tokens = TOKEN_RE.findall(selector)
        if not tokens:
            continue  # tag-only or pseudo-only selector: keep, too broad to judge safely
        if any(tok in used for tok in tokens):
            continue
        rule_text = f"{selector}{{{body}}}"
        unused_bytes += len(rule_text)
        unused_rules.append(selector)

    total = len(css)
    print(f"\n=== {path.relative_to(ROOT)} ({total} bytes total, {media_bytes} bytes in @media) ===")
    print(f"  Top-level rules with zero overlap: {len(unused_rules)} ({unused_bytes} bytes, {unused_bytes/total:.1%} of file)")
    if unused_rules:
        preview = ", ".join(unused_rules[:15])
        print(f"  Sample selectors: {preview}{' ...' if len(unused_rules) > 15 else ''}")


def main() -> None:
    used = used_tokens()
    print(f"Used class/id tokens referenced by index.html + its JS: {len(used)}")
    for rel in SOURCE_FILES:
        analyze(ROOT / rel, used)


if __name__ == "__main__":
    main()
