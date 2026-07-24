from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_BASE = "https://soulcontt.com.br"
EXPECTED_PAGES = {
    "cidades/sao-paulo/index.html": f"{PUBLIC_BASE}/cidades/sao-paulo/",
    "servicos/trocar-de-contador-em-sao-paulo/index.html": (
        f"{PUBLIC_BASE}/servicos/trocar-de-contador-em-sao-paulo/"
    ),
    "servicos/contador-para-prestadores-de-servico-em-sao-paulo/index.html": (
        f"{PUBLIC_BASE}/servicos/contador-para-prestadores-de-servico-em-sao-paulo/"
    ),
    "servicos/abrir-empresa-em-sao-paulo/index.html": (
        f"{PUBLIC_BASE}/servicos/abrir-empresa-em-sao-paulo/"
    ),
    "BLOG/posts/abrir-empresa-em-sao-paulo.html": (
        f"{PUBLIC_BASE}/BLOG/posts/abrir-empresa-em-sao-paulo.html"
    ),
    "BLOG/posts/nota-fiscal-de-servico-em-sao-paulo.html": (
        f"{PUBLIC_BASE}/BLOG/posts/nota-fiscal-de-servico-em-sao-paulo.html"
    ),
    "BLOG/posts/trocar-de-contador-em-sao-paulo.html": (
        f"{PUBLIC_BASE}/BLOG/posts/trocar-de-contador-em-sao-paulo.html"
    ),
}
PROHIBITED_LOCATION_MARKERS = (
    "Rua Silveira da Mota",
    "R. Silveira da Mota",
    "01521-010",
)


def extract(pattern: str, source: str, label: str, path: Path) -> str:
    match = re.search(pattern, source, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise AssertionError(f"{path.relative_to(ROOT)}: missing {label}")
    return html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()


def validate() -> None:
    errors: list[str] = []
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    html_sources: dict[str, str] = {}

    for relative_path, expected_canonical in EXPECTED_PAGES.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"Missing {relative_path}")
            continue

        source = path.read_text(encoding="utf-8")
        html_sources[relative_path] = source

        try:
            title = extract(r"<title>(.*?)</title>", source, "title", path)
            description = extract(
                r'<meta\s+name="description"\s+content="([^"]+)"',
                source,
                "meta description",
                path,
            )
            canonical = extract(
                r'<link\s+rel="canonical"\s+href="([^"]+)"',
                source,
                "canonical",
                path,
            )
            h1 = extract(r"<h1[^>]*>(.*?)</h1>", source, "H1", path)

            if canonical != expected_canonical:
                errors.append(
                    f"{relative_path}: canonical {canonical!r} != {expected_canonical!r}"
                )
            if len(title) > 65:
                errors.append(f"{relative_path}: title is too long ({len(title)} characters)")
            if not 90 <= len(description) <= 165:
                errors.append(
                    f"{relative_path}: description length is {len(description)}, expected 90-165"
                )
            if len(re.findall(r"<h1\b", source, flags=re.IGNORECASE)) != 1:
                errors.append(f"{relative_path}: expected exactly one H1")
            if "são paulo" not in f"{title} {description} {h1}".lower():
                errors.append(f"{relative_path}: primary metadata does not mention São Paulo")

            json_ld_blocks = re.findall(
                r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
                source,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if not json_ld_blocks:
                errors.append(f"{relative_path}: missing JSON-LD")
            for block in json_ld_blocks:
                json.loads(block)

            if "/assets/css/cookies.css" not in source:
                errors.append(f"{relative_path}: missing cookie consent CSS")
            if "/assets/js/cookies.js" not in source:
                errors.append(f"{relative_path}: missing cookie consent/Analytics JS")
            if "5511916539680" not in source and "+5511916539680" not in source:
                errors.append(f"{relative_path}: missing São Paulo contact number")
            if any(marker.lower() in source.lower() for marker in PROHIBITED_LOCATION_MARKERS):
                errors.append(f"{relative_path}: exposes the non-public São Paulo base address")

            local_refs = set(
                re.findall(r'(?:href|src)="(/[^"?#]+)', source, flags=re.IGNORECASE)
            )
            for ref in local_refs:
                target = ROOT / ref.lstrip("/")
                if ref.endswith("/"):
                    target /= "index.html"
                if not target.exists():
                    errors.append(f"{relative_path}: missing local reference {ref}")

            if f"<loc>{expected_canonical}</loc>" not in sitemap:
                errors.append(f"Sitemap missing {expected_canonical}")
        except (AssertionError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    if html_sources:
        unique_titles = {
            extract(r"<title>(.*?)</title>", source, "title", ROOT / relative_path)
            for relative_path, source in html_sources.items()
        }
        unique_h1s = {
            extract(r"<h1[^>]*>(.*?)</h1>", source, "H1", ROOT / relative_path)
            for relative_path, source in html_sources.items()
        }
        if len(unique_titles) != len(html_sources):
            errors.append("São Paulo pages have duplicate titles")
        if len(unique_h1s) != len(html_sources):
            errors.append("São Paulo pages have duplicate H1s")

    inbound_sources = [
        path
        for path in ROOT.rglob("*.html")
        if "output" not in path.parts and path.relative_to(ROOT).as_posix() not in EXPECTED_PAGES
    ]
    inbound_count = sum(
        1
        for path in inbound_sources
        if '/cidades/sao-paulo/' in path.read_text(encoding="utf-8", errors="ignore")
    )
    if inbound_count < 3:
        errors.append(
            f"São Paulo city page has links from only {inbound_count} other HTML files; expected at least 3"
        )

    sitemap_urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append("Sitemap contains duplicate URLs")

    if errors:
        print("São Paulo expansion validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Validated {len(EXPECTED_PAGES)} São Paulo landing and editorial pages")
    print(f"Inbound HTML sources linking to São Paulo hub: {inbound_count}")
    print(f"Sitemap URLs: {len(sitemap_urls)}")


if __name__ == "__main__":
    validate()
