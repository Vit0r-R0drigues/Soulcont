from __future__ import annotations

import html
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from generate_cidades import CITIES


ROOT = Path(__file__).resolve().parents[1]
CITY_ROOT = ROOT / "cidades"


def extract(pattern: str, source: str, label: str, path: Path) -> str:
    match = re.search(pattern, source, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise AssertionError(f"{path}: missing {label}")
    return html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()


def visible_text(source: str) -> str:
    source = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    source = html.unescape(source).lower()
    return re.sub(r"\s+", " ", source).strip()


def validate() -> None:
    errors: list[str] = []
    titles: dict[str, Path] = {}
    canonicals: dict[str, Path] = {}
    h1s: dict[str, Path] = {}
    texts: dict[str, str] = {}
    expected_urls = {"https://soulcontt.com.br/cidades/"}

    hub = CITY_ROOT / "index.html"
    if not hub.exists():
        errors.append("Missing cidades/index.html")
        hub_source = ""
    else:
        hub_source = hub.read_text(encoding="utf-8")

    for city in CITIES:
        path = CITY_ROOT / city["slug"] / "index.html"
        expected_url = f"https://soulcontt.com.br/cidades/{city['slug']}/"
        expected_urls.add(expected_url)
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
            continue

        source = path.read_text(encoding="utf-8")
        try:
            title = extract(r"<title>(.*?)</title>", source, "title", path)
            canonical = extract(r'<link\s+rel="canonical"\s+href="([^"]+)"', source, "canonical", path)
            h1 = extract(r"<h1[^>]*>(.*?)</h1>", source, "h1", path)
            if canonical != expected_url:
                errors.append(f"{path.relative_to(ROOT)}: canonical {canonical} != {expected_url}")
            for value, collection, label in (
                (title, titles, "title"),
                (canonical, canonicals, "canonical"),
                (h1, h1s, "h1"),
            ):
                if value in collection:
                    errors.append(f"Duplicate {label}: {value}")
                collection[value] = path

            blocks = re.findall(
                r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
                source,
                flags=re.I | re.S,
            )
            if len(blocks) != 2:
                errors.append(f"{path.relative_to(ROOT)}: expected 2 JSON-LD blocks, found {len(blocks)}")
            for block in blocks:
                json.loads(block)

            refs = set(re.findall(r'(?:href|src)="(/[^"?#]+)', source, flags=re.I))
            for ref in refs:
                target = ROOT / ref.lstrip("/")
                if ref.endswith("/"):
                    target /= "index.html"
                if not target.exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing local reference {ref}")

            if f'/cidades/{city["slug"]}/' not in hub_source:
                errors.append(f"Hub missing link to {city['name']}")
            if city["slug"] == "ico":
                if "Rua São José, 1245" not in source:
                    errors.append("Icó page is missing the physical address")
            elif "não possui unidade física na cidade" not in source:
                errors.append(f"{city['name']}: missing digital-only location disclosure")

            texts[city["slug"]] = visible_text(source)
        except (AssertionError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_urls = set(re.findall(r"<loc>(https://soulcontt\.com\.br/cidades/[^<]*)</loc>", sitemap))
    missing_sitemap = expected_urls - sitemap_urls
    extra_sitemap = sitemap_urls - expected_urls
    if missing_sitemap:
        errors.append(f"Sitemap missing: {sorted(missing_sitemap)}")
    if extra_sitemap:
        errors.append(f"Sitemap has unexpected city URLs: {sorted(extra_sitemap)}")

    max_pair = ("", "", 0.0)
    slugs = sorted(texts)
    for index, left in enumerate(slugs):
        for right in slugs[index + 1 :]:
            ratio = SequenceMatcher(None, texts[left], texts[right]).ratio()
            if ratio > max_pair[2]:
                max_pair = (left, right, ratio)
    if max_pair[2] >= 0.86:
        errors.append(
            f"City pages too similar: {max_pair[0]} x {max_pair[1]} = {max_pair[2]:.1%}"
        )

    if errors:
        print("City page validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Validated hub + {len(CITIES)} city pages")
    print(f"Unique titles: {len(titles)}; unique canonicals: {len(canonicals)}; unique H1s: {len(h1s)}")
    print(f"Sitemap city URLs: {len(sitemap_urls)}")
    print(f"Highest visible-text similarity: {max_pair[0]} x {max_pair[1]} = {max_pair[2]:.1%}")


if __name__ == "__main__":
    validate()
