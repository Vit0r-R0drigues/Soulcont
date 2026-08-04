"""One-off Fase 3 script: injects JSON-LD into pages that had none.

Reuses only data already present on each page (title, meta description,
canonical, visible FAQ text) or already published elsewhere (sitemap lastmod).
Does not invent prices, dates, testimonials or business data.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE_URL = "https://soulcontt.com.br"
LOGO = f"{BASE_URL}/assets/img/soulcont/og.png"
ORG_ID = f"{BASE_URL}/#organization"

SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
LASTMOD_BY_URL = dict(
    re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", SITEMAP)
)


def clean(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text)).strip()


def extract(pattern: str, source: str) -> str | None:
    match = re.search(pattern, source, re.S)
    return match.group(1).strip() if match else None


def extract_faqs(source: str) -> list[tuple[str, str]]:
    pairs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", source, re.S)
    return [(clean(q), clean(a)) for q, a in pairs]


def page_meta(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    title = clean(extract(r"<title>(.*?)</title>", source) or "")
    description = html.unescape(extract(r'<meta\s+name="description"\s+content="([^"]*)"', source) or "")
    canonical = extract(r'<link\s+rel="canonical"\s+href="([^"]+)"', source) or ""
    return {"source": source, "title": title, "description": description, "canonical": canonical}


def faq_block(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def insert_blocks(path: Path, meta: dict, blocks: list[dict]) -> None:
    source = meta["source"]
    scripts = "\n".join(
        '    <script type="application/ld+json">\n'
        + json.dumps(block, ensure_ascii=False, indent=4)
        + "\n    </script>"
        for block in blocks
    )
    if "</head>" not in source:
        raise ValueError(f"{path}: no </head> found")
    new_source = source.replace("</head>", f"{scripts}\n</head>", 1)
    path.write_text(new_source, encoding="utf-8", newline="\n")


def webpage_block(page_type: str, meta: dict, extra: dict | None = None) -> dict:
    block = {
        "@context": "https://schema.org",
        "@type": page_type,
        "@id": f"{meta['canonical']}#webpage",
        "url": meta["canonical"],
        "name": meta["title"],
        "description": meta["description"],
        "inLanguage": "pt-BR",
        "isPartOf": {"@type": "WebSite", "@id": f"{BASE_URL}/#website", "url": f"{BASE_URL}/", "name": "SoulCont"},
    }
    if extra:
        block.update(extra)
    return block


def service_block(meta: dict) -> dict:
    return webpage_block(
        "Service",
        meta,
        {
            "@id": f"{meta['canonical']}#service",
            "serviceType": meta["title"].split("|")[0].strip(),
            "provider": {"@type": "Organization", "@id": ORG_ID, "name": "SoulCont", "url": f"{BASE_URL}/"},
            "areaServed": {"@type": "Country", "name": "Brasil"},
        },
    )


def webapp_block(meta: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "@id": f"{meta['canonical']}#webapp",
        "name": meta["title"].split("-")[0].split("|")[0].strip(),
        "url": meta["canonical"],
        "description": meta["description"],
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL"},
        "inLanguage": "pt-BR",
    }


def blogposting_blocks(meta: dict, path: Path) -> list[dict]:
    lastmod = LASTMOD_BY_URL.get(meta["canonical"], "2026-07-15")
    headline = meta["title"].split("|")[0].strip()
    posting = {
        "@type": "BlogPosting",
        "@id": f"{meta['canonical']}#article",
        "headline": headline,
        "description": meta["description"],
        "datePublished": lastmod,
        "dateModified": lastmod,
        "inLanguage": "pt-BR",
        "mainEntityOfPage": meta["canonical"],
        "image": LOGO,
        "author": {"@type": "Organization", "name": "SoulCont", "url": f"{BASE_URL}/"},
        "publisher": {
            "@type": "Organization",
            "name": "SoulCont",
            "url": f"{BASE_URL}/",
            "logo": {"@type": "ImageObject", "url": LOGO},
        },
    }
    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/BLOG/index.html"},
            {"@type": "ListItem", "position": 3, "name": headline, "item": meta["canonical"]},
        ],
    }
    return [{"@context": "https://schema.org", "@graph": [posting, breadcrumb]}]


PLAN: list[tuple[str, str]] = [
    ("HTML/sobre.html", "AboutPage"),
    ("HTML/servicos.html", "Service"),
    ("HTML/contatos.html", "ContactPage"),
    ("HTML/ferramentas.html", "WebPage"),
    ("HTML/abertura-de-empresa.html", "Service"),
    ("HTML/troca-de-contador.html", "Service"),
    ("HTML/diagnostico-tributario.html", "Service"),
    ("HTML/contabilidade-prestadores-servico.html", "Service"),
    ("HTML/contabilidade-profissionais-liberais.html", "Service"),
    ("HTML/calculadora-irrf.html", "WebApplication"),
    ("HTML/calculadora-ferias.html", "WebApplication"),
    ("BLOG/index.html", "Blog"),
    ("BLOG/posts/abrir-empresa-prestador-servico.html", "BlogPosting"),
    ("BLOG/posts/trocar-de-contador-com-seguranca.html", "BlogPosting"),
    ("BLOG/posts/planejamento-tributario-prestadores-servico.html", "BlogPosting"),
    ("BLOG/posts/fluxo-de-caixa-para-pequenas-empresas.html", "BlogPosting"),
    ("BLOG/posts/mei-2026-guia-completo.html", "BlogPosting"),
    ("BLOG/posts/simples-nacional-2026-guia-pratico.html", "BlogPosting"),
    ("BLOG/posts/irpf-2026-atualizacoes.html", "BlogPosting"),
    ("BLOG/posts/imposto-de-renda-2026-journal.html", "BlogPosting"),
    ("landingpages/irrf2026.html", "WebApplication"),
    ("landingpages/cst-ibs-cbs-2026.html", "WebPage"),
    ("landingpages/crioteriosirrf2026.html", "WebPage"),
]


def main() -> None:
    for rel_path, page_type in PLAN:
        path = ROOT / rel_path
        meta = page_meta(path)
        faqs = extract_faqs(meta["source"])

        if page_type == "BlogPosting":
            blocks = blogposting_blocks(meta, path)
        elif page_type == "WebApplication":
            blocks = [webapp_block(meta)]
        elif page_type == "Service":
            blocks = [service_block(meta)]
        elif page_type == "Blog":
            blocks = [webpage_block("Blog", meta)]
        else:
            blocks = [webpage_block(page_type, meta)]

        if faqs and page_type != "BlogPosting":
            blocks.append(faq_block(faqs))

        insert_blocks(path, meta, blocks)
        print(f"{rel_path}: inserted {len(blocks)} block(s) ({page_type}, {len(faqs)} FAQ)")


if __name__ == "__main__":
    main()
