from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITEMAP = ROOT / "sitemap.xml"
BASE_URL = "https://soulcontt.com.br"

# Apenas links de navegacao reais (<a href>). Ignora <link rel="canonical">,
# og:url e outras referencias que nao representam link interno navegavel.
HREF_RE = re.compile(r'<a\b[^>]*\bhref="([^"]+)"', re.IGNORECASE)


def sitemap_paths() -> list[str]:
    source = SITEMAP.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", source)
    paths = []
    for loc in locs:
        path = loc.replace(BASE_URL, "")
        if not path.startswith("/"):
            path = "/" + path
        paths.append(path)
    return paths


def normalize(href: str, source_path: Path) -> str | None:
    href = href.split("#")[0].split("?")[0]
    if not href:
        return None
    if href.startswith("http://") or href.startswith("https://"):
        if not href.startswith(BASE_URL):
            return None
        href = href[len(BASE_URL):]
        if not href:
            href = "/"
    if not href.startswith("/"):
        # relative link (e.g. blog posts linking with a relative path)
        href = "/" + str((source_path.parent / href).resolve().relative_to(ROOT)).replace("\\", "/")
    return href


def build_inbound_counts() -> dict[str, list[str]]:
    inbound: dict[str, list[str]] = {}
    html_files = [p for p in ROOT.rglob("*.html") if "output" not in p.parts and ".git" not in p.parts]
    for path in html_files:
        source = path.read_text(encoding="utf-8", errors="ignore")
        rel_source = "/" + path.relative_to(ROOT).as_posix()
        for href in HREF_RE.findall(source):
            target = normalize(href, path)
            if target is None or target == rel_source:
                continue  # ignora links de uma pagina para ela mesma
            inbound.setdefault(target, [])
            if rel_source not in inbound[target]:
                inbound[target].append(rel_source)
    return inbound


def main() -> None:
    inbound = build_inbound_counts()
    paths = sitemap_paths()

    zero, one, two = [], [], []
    for path in paths:
        key = path
        if key.endswith("/") and key != "/":
            pass
        count = len(inbound.get(key, []))
        if count == 0:
            zero.append(path)
        elif count == 1:
            one.append(path)
        elif count == 2:
            two.append(path)

    print(f"Total sitemap URLs: {len(paths)}")
    print(f"URLs com 0 links internos recebidos: {len(zero)}")
    for p in sorted(zero):
        print(f"  - {p}")
    print(f"URLs com 1 link interno recebido: {len(one)}")
    for p in sorted(one):
        print(f"  - {p}  <- {inbound.get(p)}")
    print(f"URLs com 2 links internos recebidos: {len(two)}")
    for p in sorted(two):
        print(f"  - {p}  <- {inbound.get(p)}")


if __name__ == "__main__":
    main()
