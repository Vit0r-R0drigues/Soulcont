from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "migration" / "cloudflare-vl-to-soulcont.csv"
OLD_HOSTS = (
    "vlcontabilidadeempresarial.com.br",
    "www.vlcontabilidadeempresarial.com.br",
)
NEW_ORIGIN = "https://soulcontt.com.br"

REDIRECTS = (
    ("/", "/"),
    ("/index.html", "/"),
    ("/HTML/index.html", "/"),
    ("/404.html", "/404.html"),
    ("/HTML/404.html", "/404.html"),
    ("/contatos.html", "/HTML/contatos.html"),
    ("/HTML/contatos.html", "/HTML/contatos.html"),
    ("/HTML/sobre.html", "/HTML/sobre.html"),
    ("/HTML/servicos.html", "/HTML/servicos.html"),
    ("/HTML/ferramentas.html", "/HTML/ferramentas.html"),
    ("/HTML/abertura-de-empresa.html", "/HTML/abertura-de-empresa.html"),
    ("/HTML/troca-de-contador.html", "/HTML/troca-de-contador.html"),
    ("/HTML/diagnostico-tributario.html", "/HTML/diagnostico-tributario.html"),
    (
        "/HTML/contabilidade-prestadores-servico.html",
        "/HTML/contabilidade-prestadores-servico.html",
    ),
    (
        "/HTML/contabilidade-profissionais-liberais.html",
        "/HTML/contabilidade-profissionais-liberais.html",
    ),
    ("/HTML/calculadora-irrf.html", "/HTML/calculadora-irrf.html"),
    ("/HTML/calculadora-ferias.html", "/HTML/calculadora-ferias.html"),
    ("/HTML/calculadora-rescisao.html", "/HTML/calculadora-rescisao.html"),
    ("/HTML/calculadora-suite.html", "/HTML/calculadora-suite.html"),
    ("/HTML/checklist.html", "/HTML/checklist.html"),
    (
        "/HTML/politica-de-privacidade.html",
        "/HTML/politica-de-privacidade.html",
    ),
    (
        "/Agradecimento/agradecimento.html",
        "/Agradecimento/agradecimento.html",
    ),
    (
        "/HTML/agradecimento.html",
        "/Agradecimento/agradecimento.html",
    ),
    ("/BLOG/index.html", "/BLOG/index.html"),
    ("/BLOG/blogemconstru%C3%A7%C3%A3o.html", "/BLOG/index.html"),
    ("/BLOG/template.html", "/BLOG/index.html"),
    (
        "/BLOG/posts/abrir-empresa-prestador-servico.html",
        "/BLOG/posts/abrir-empresa-prestador-servico.html",
    ),
    (
        "/BLOG/posts/fluxo-de-caixa-para-pequenas-empresas.html",
        "/BLOG/posts/fluxo-de-caixa-para-pequenas-empresas.html",
    ),
    (
        "/BLOG/posts/imposto-de-renda-2026-journal.html",
        "/BLOG/posts/imposto-de-renda-2026-journal.html",
    ),
    (
        "/BLOG/posts/irpf-2026-atualizacoes.html",
        "/BLOG/posts/irpf-2026-atualizacoes.html",
    ),
    (
        "/BLOG/posts/mei-2026-guia-completo.html",
        "/BLOG/posts/mei-2026-guia-completo.html",
    ),
    (
        "/BLOG/posts/planejamento-tributario-prestadores-servico.html",
        "/BLOG/posts/planejamento-tributario-prestadores-servico.html",
    ),
    (
        "/BLOG/posts/simples-nacional-2026-guia-pratico.html",
        "/BLOG/posts/simples-nacional-2026-guia-pratico.html",
    ),
    (
        "/BLOG/posts/trocar-de-contador-com-seguranca.html",
        "/BLOG/posts/trocar-de-contador-com-seguranca.html",
    ),
    ("/landingpages/irrf2026.html", "/landingpages/irrf2026.html"),
    ("/landingpages/irrf2025.html", "/landingpages/irrf2026.html"),
    (
        "/landingpages/crioteriosirrf2026.html",
        "/landingpages/crioteriosirrf2026.html",
    ),
    (
        "/landingpages/cst-ibs-cbs-2026.html",
        "/landingpages/cst-ibs-cbs-2026.html",
    ),
    ("/INSTAGRAM/index.html", "/INSTAGRAM/index.html"),
)


def validate_local_targets() -> None:
    missing: list[str] = []
    for _, target_path in REDIRECTS:
        local_path = ROOT / target_path.lstrip("/")
        if target_path == "/":
            local_path = ROOT / "index.html"
        elif target_path.endswith("/"):
            local_path /= "index.html"
        if not local_path.exists():
            missing.append(target_path)
    if missing:
        raise SystemExit(f"Missing redirect targets: {sorted(set(missing))}")


def build() -> None:
    validate_local_targets()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, lineterminator="\n")
        for source_path, target_path in REDIRECTS:
            target_url = f"{NEW_ORIGIN}{target_path}"
            for host in OLD_HOSTS:
                writer.writerow(
                    (
                        f"{host}{source_path}",
                        target_url,
                        301,
                        "TRUE",
                        "FALSE",
                        "FALSE",
                        "FALSE",
                    )
                )

    print(f"Generated {len(REDIRECTS) * len(OLD_HOSTS)} Cloudflare redirect rows")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    build()
