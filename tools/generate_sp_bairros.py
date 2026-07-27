from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from cidades_config import PROFESSIONALS, REGIONS, SITE


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "cidades" / "sao-paulo"
SP_REGION = REGIONS["sao-paulo"]
PHONE_E164 = SP_REGION["phone_e164"]
PHONE_DISPLAY = SP_REGION["phone_display"]


NEIGHBORHOODS: list[dict[str, Any]] = [
    {
        "slug": "bras",
        "name": "Brás",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade no Brás para comércios, prestadores e pequenas empresas. "
            "Tributos, folha e organização financeira com atendimento on-line."
        ),
        "context_title": "Contabilidade conectada à rotina comercial do Brás",
        "context": (
            "Empresas do Brás costumam precisar de informação rápida sobre compras, "
            "vendas, estoque, documentos fiscais e equipe. A SoulCont organiza esses "
            "dados em uma rotina contábil acompanhada, sem indicar escritório físico "
            "ou atendimento aberto ao público no bairro."
        ),
        "focus": "Comércio, estoque e equipe",
        "focus_text": (
            "Organização fiscal e financeira para negócios que precisam acompanhar "
            "movimento, margem e custo operacional."
        ),
        "audiences": [
            "Comércios varejistas e atacadistas sediados no Brás",
            "Lojas com funcionários, comissões e folha recorrente",
            "Prestadores que atendem empresas da região",
            "Negócios que desejam trocar de contador com estoque e documentos organizados",
        ],
        "decisions": [
            "Conciliar vendas, compras e documentos antes da apuração",
            "Revisar regime tributário conforme faturamento e operação",
            "Planejar folha, comissões e custo da equipe",
            "Acompanhar margem e fluxo de caixa para decisões de compra",
        ],
        "faq_q": "A SoulCont possui escritório aberto ao público no Brás?",
        "faq_a": (
            "Não. O atendimento para empresas do Brás é on-line. Encontros presenciais "
            "externos podem ser avaliados mediante agendamento e disponibilidade."
        ),
    },
    {
        "slug": "mooca",
        "name": "Mooca",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade na Mooca para comércios, prestadores e empresas familiares. "
            "Rotina fiscal, sucessão e gestão com atendimento consultivo on-line."
        ),
        "context_title": "Organização contábil para negócios consolidados na Mooca",
        "context": (
            "A SoulCont atende empresas da Mooca que precisam estruturar responsabilidades, "
            "retiradas e controles sem perder a agilidade da operação. O acompanhamento "
            "é digital e considera a história, a composição societária e o momento real "
            "de cada negócio."
        ),
        "focus": "Empresas familiares e organização societária",
        "focus_text": (
            "Clareza sobre pró-labore, distribuição, responsabilidades dos sócios e "
            "continuidade da rotina fiscal."
        ),
        "audiences": [
            "Empresas familiares e sociedades empresárias da Mooca",
            "Comércios que precisam separar finanças dos sócios e da empresa",
            "Prestadores com operação recorrente e equipe",
            "Negócios preparando entrada de sócio ou reorganização",
        ],
        "decisions": [
            "Definir pró-labore e distribuição com documentação adequada",
            "Revisar contrato, atividades e responsabilidades societárias",
            "Organizar calendário fiscal e trabalhista",
            "Criar indicadores para acompanhar caixa e resultado",
        ],
        "faq_q": "A SoulCont atende empresas familiares localizadas na Mooca?",
        "faq_a": (
            "Sim. O atendimento pode organizar rotina contábil, retiradas, documentação "
            "societária e indicadores. Ele acontece on-line, sem unidade física aberta "
            "ao público no bairro."
        ),
    },
    {
        "slug": "cambuci",
        "name": "Cambuci",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade no Cambuci para abrir empresa, organizar impostos e trocar "
            "de contador. Atendimento digital para prestadores e pequenos negócios."
        ),
        "context_title": "Uma rotina contábil simples e acompanhada para o Cambuci",
        "context": (
            "Prestadores e pequenas empresas do Cambuci podem centralizar documentos, "
            "prazos e dúvidas em um processo digital com a SoulCont. A orientação começa "
            "pela atividade e pela situação atual da empresa, evitando decisões baseadas "
            "apenas no valor da guia."
        ),
        "focus": "Formalização e rotina mensal",
        "focus_text": (
            "Apoio para abrir o CNPJ corretamente ou colocar notas, impostos e "
            "documentos em uma sequência previsível."
        ),
        "audiences": [
            "Prestadores do Cambuci preparando a abertura do primeiro CNPJ",
            "Pequenas empresas com documentos e solicitações descentralizados",
            "MEIs avaliando crescimento, contratação ou desenquadramento",
            "Empresas insatisfeitas com falta de acompanhamento contábil",
        ],
        "decisions": [
            "Escolher CNAE, natureza jurídica e regime antes da abertura",
            "Definir um checklist mensal de notas, extratos e documentos",
            "Avaliar a migração do MEI com custos e obrigações",
            "Trocar de contador com pendências e responsáveis mapeados",
        ],
        "faq_q": "É possível abrir uma empresa no Cambuci com atendimento on-line?",
        "faq_a": (
            "Sim. A análise da atividade, dos CNAEs, da estrutura e dos documentos pode "
            "ser conduzida on-line. A SoulCont não divulga unidade física no Cambuci."
        ),
    },
    {
        "slug": "sacoma",
        "name": "Sacomã",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade no Sacomã para MEIs, prestadores e pequenas empresas em "
            "crescimento. Enquadramento, impostos e folha com atendimento on-line."
        ),
        "context_title": "Suporte contábil para negócios em crescimento no Sacomã",
        "context": (
            "A SoulCont atende empreendedores do Sacomã que estão aumentando faturamento, "
            "assumindo equipe ou profissionalizando a gestão. O processo digital ajuda a "
            "comparar o cenário atual com os próximos custos antes de mudar de porte ou "
            "ampliar a operação."
        ),
        "focus": "MEI, mudança de porte e contratação",
        "focus_text": (
            "Planejamento para crescer com clareza sobre limite, tributos, folha e "
            "responsabilidades mensais."
        ),
        "audiences": [
            "MEIs do Sacomã próximos do limite de faturamento",
            "Prestadores que pretendem contratar o primeiro funcionário",
            "Pequenos negócios avaliando mudança para microempresa",
            "Empresas que precisam rever retirada e capital de giro",
        ],
        "decisions": [
            "Projetar custos antes da saída do MEI",
            "Comparar enquadramentos conforme receita e atividade",
            "Calcular impacto de salário, encargos e benefícios",
            "Separar retirada pessoal, despesas e caixa da empresa",
        ],
        "faq_q": "A SoulCont orienta a saída do MEI para empresas do Sacomã?",
        "faq_a": (
            "Sim. O atendimento avalia limite, atividade, equipe e custos da nova "
            "estrutura. Todo o processo pode ser acompanhado on-line."
        ),
    },
    {
        "slug": "ipiranga",
        "name": "Ipiranga",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade no Ipiranga para profissionais liberais e empresas de "
            "serviços. Regime, pró-labore e indicadores com atendimento on-line."
        ),
        "context_title": "Contabilidade consultiva para profissionais do Ipiranga",
        "context": (
            "Profissionais e empresas de serviços do Ipiranga podem usar a contabilidade "
            "para compreender imposto, retirada e resultado, não apenas para cumprir "
            "obrigações. A SoulCont conduz a rotina on-line e adapta a análise ao modelo "
            "de receita e à estrutura de cada empresa."
        ),
        "focus": "Profissionais liberais e empresas de serviços",
        "focus_text": (
            "Estrutura tributária e financeira para operações baseadas em honorários, "
            "contratos e prestação recorrente."
        ),
        "audiences": [
            "Profissionais liberais do Ipiranga que atuam por pessoa jurídica",
            "Consultorias e empresas de serviços recorrentes",
            "Negócios com dúvidas sobre pró-labore e distribuição",
            "Empresas que precisam compreender margem por contrato ou serviço",
        ],
        "decisions": [
            "Comparar regimes conforme receita, atividade e folha",
            "Estruturar pró-labore e distribuição de resultados",
            "Organizar emissão de notas e calendário tributário",
            "Acompanhar margem, caixa e ponto de equilíbrio",
        ],
        "faq_q": "A SoulCont atende profissionais liberais no Ipiranga?",
        "faq_a": (
            "Sim. O atendimento pode abranger abertura, enquadramento, pró-labore, "
            "distribuição, tributos e leitura financeira, sempre por canais on-line."
        ),
    },
    {
        "slug": "tatuape",
        "name": "Tatuapé",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade no Tatuapé para clínicas, consultorias e prestadores. "
            "Tributação, folha e gestão financeira com atendimento on-line."
        ),
        "context_title": "Decisões contábeis para empresas de serviços no Tatuapé",
        "context": (
            "A SoulCont atende empresas do Tatuapé que combinam atendimento profissional, "
            "receitas recorrentes e custos de equipe. A análise reúne tributação, folha e "
            "indicadores para apoiar escolhas sobre preço, contratação e crescimento, "
            "sem alegar unidade física no bairro."
        ),
        "focus": "Clínicas, consultorias e serviços especializados",
        "focus_text": (
            "Acompanhamento para operações que precisam equilibrar carga tributária, "
            "custo de equipe e rentabilidade."
        ),
        "audiences": [
            "Clínicas e empresas de serviços especializados do Tatuapé",
            "Consultorias com contratos e faturamento recorrente",
            "Profissionais que estruturaram equipe de apoio",
            "Empresas avaliando revisão tributária ou troca de contador",
        ],
        "decisions": [
            "Revisar enquadramento conforme atividade e folha",
            "Planejar contratações e custo da equipe",
            "Organizar retirada e distribuição dos sócios",
            "Relacionar faturamento, margem e capacidade de crescimento",
        ],
        "faq_q": "A SoulCont atende clínicas e consultorias do Tatuapé?",
        "faq_a": (
            "Sim. O escopo pode incluir contabilidade, tributos, folha e análise financeira. "
            "O atendimento é on-line e não há escritório aberto ao público no bairro."
        ),
    },
    {
        "slug": "itaim-bibi",
        "name": "Itaim Bibi",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade no Itaim Bibi para consultorias, tecnologia e empresas de "
            "serviços. Planejamento e indicadores com atendimento consultivo on-line."
        ),
        "context_title": "Contabilidade para serviços de alto valor no Itaim Bibi",
        "context": (
            "Consultorias, empresas de tecnologia e outros prestadores do Itaim Bibi "
            "podem conectar contratos, faturamento, retirada e rentabilidade em uma mesma "
            "leitura. A SoulCont trabalha on-line, com orientação direta e decisões "
            "fundamentadas nos dados da operação."
        ),
        "focus": "Consultorias, tecnologia e serviços empresariais",
        "focus_text": (
            "Análise tributária e financeira para empresas que precisam acompanhar "
            "contratos, margem e remuneração dos sócios."
        ),
        "audiences": [
            "Consultorias e assessorias empresariais do Itaim Bibi",
            "Empresas de tecnologia e serviços digitais",
            "Prestadores com contratos de maior valor ou receitas recorrentes",
            "Sociedades que precisam organizar remuneração e indicadores",
        ],
        "decisions": [
            "Comparar regimes considerando faturamento, folha e atividade",
            "Definir pró-labore e distribuição com previsibilidade",
            "Acompanhar margem por contrato e concentração de receita",
            "Planejar caixa, contratações e expansão da operação",
        ],
        "faq_q": "A SoulCont atende consultorias e empresas de tecnologia no Itaim Bibi?",
        "faq_a": (
            "Sim. O atendimento consultivo é realizado on-line e considera tributação, "
            "contratos, remuneração dos sócios e indicadores. Não há unidade física da "
            "SoulCont aberta ao público no bairro."
        ),
    },
    {
        "slug": "santo-amaro",
        "name": "Santo Amaro",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade em Santo Amaro para comércios, serviços e empresas com equipe. "
            "Fiscal, folha e troca de contador com atendimento on-line."
        ),
        "context_title": "Rotina fiscal e trabalhista para empresas de Santo Amaro",
        "context": (
            "A SoulCont atende empresas de Santo Amaro que precisam integrar notas, "
            "tributos, folha e controles financeiros. O acompanhamento digital organiza "
            "responsabilidades e prazos para negócios com diferentes frentes de operação "
            "e decisões recorrentes sobre equipe."
        ),
        "focus": "Operação, folha e transição contábil",
        "focus_text": (
            "Processos para empresas que precisam coordenar movimento fiscal, pessoas "
            "e informações financeiras."
        ),
        "audiences": [
            "Comércios e prestadores de serviços de Santo Amaro",
            "Empresas com folha, férias e admissões recorrentes",
            "Negócios com mais de uma frente de receita",
            "Empresas preparando uma troca de contador",
        ],
        "decisions": [
            "Organizar calendário de notas, impostos e folha",
            "Avaliar custo da equipe antes de contratar",
            "Revisar regime e atividades cadastradas",
            "Conduzir transição contábil sem interromper obrigações",
        ],
        "faq_q": "Como funciona a troca de contador para uma empresa de Santo Amaro?",
        "faq_a": (
            "A SoulCont realiza diagnóstico, checklist documental e implantação da nova "
            "rotina por canais digitais. Não é necessário existir atendimento em um "
            "escritório físico no bairro."
        ),
    },
    {
        "slug": "vila-mariana",
        "name": "Vila Mariana",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade na Vila Mariana para profissionais, clínicas e empresas de "
            "serviços. Impostos, pró-labore e folha com atendimento on-line."
        ),
        "context_title": "Contabilidade para profissionais e clínicas da Vila Mariana",
        "context": (
            "Profissionais, clínicas e empresas de serviços da Vila Mariana podem "
            "estruturar faturamento, despesas, retiradas e equipe com uma leitura integrada. "
            "A SoulCont atende on-line e orienta cada decisão conforme atividade, regime "
            "e dados reais do negócio."
        ),
        "focus": "Profissionais, clínicas e equipes de apoio",
        "focus_text": (
            "Organização tributária e trabalhista para serviços que dependem de agenda, "
            "honorários e pessoas."
        ),
        "audiences": [
            "Profissionais liberais e clínicas da Vila Mariana",
            "Empresas de saúde e serviços especializados",
            "Prestadores com equipe administrativa ou técnica",
            "Sociedades profissionais com dúvidas sobre retirada",
        ],
        "decisions": [
            "Escolher enquadramento compatível com a atividade profissional",
            "Organizar pró-labore, distribuição e despesas da operação",
            "Planejar folha e custo da equipe de apoio",
            "Acompanhar ocupação, receita, margem e caixa",
        ],
        "faq_q": "A SoulCont atende clínicas e profissionais da Vila Mariana?",
        "faq_a": (
            "Sim. A análise pode incluir enquadramento, tributos, retiradas, folha e "
            "indicadores. O atendimento ocorre on-line, sem unidade física aberta no bairro."
        ),
    },
    {
        "slug": "vila-prudente",
        "name": "Vila Prudente",
        "attendance_mode": "service_area",
        "address": None,
        "page_description": (
            "Contabilidade na Vila Prudente para comércios, prestadores e pequenas "
            "empresas. Organização fiscal e financeira com atendimento on-line."
        ),
        "context_title": "Contabilidade organizada para empresas da Vila Prudente",
        "context": (
            "A SoulCont atende empresas da Vila Prudente que querem reduzir improvisos "
            "na entrega de documentos, na apuração de impostos e nas decisões de caixa. "
            "O processo é digital, com contato direto e uma rotina adaptada ao porte e "
            "à atividade de cada negócio."
        ),
        "focus": "Pequenas empresas e previsibilidade",
        "focus_text": (
            "Estrutura mensal para acompanhar obrigações, retirada, equipe e resultado "
            "com responsabilidades claras."
        ),
        "audiences": [
            "Comércios e pequenas empresas da Vila Prudente",
            "Prestadores com faturamento recorrente",
            "MEIs em transição para uma estrutura empresarial",
            "Negócios que precisam organizar documentos e fluxo de caixa",
        ],
        "decisions": [
            "Definir rotina para notas, extratos e obrigações",
            "Avaliar regime conforme faturamento e atividade",
            "Planejar retirada e custo de contratação",
            "Usar caixa e margem para orientar o crescimento",
        ],
        "faq_q": "A SoulCont atende pequenas empresas na Vila Prudente?",
        "faq_a": (
            "Sim. O atendimento on-line pode incluir abertura, rotina contábil, folha, "
            "diagnóstico tributário e apoio financeiro. Não existe unidade física da "
            "SoulCont aberta ao público no bairro."
        ),
    },
]

RELATED_NEIGHBORHOODS: dict[str, list[str]] = {
    "bras": ["mooca", "cambuci", "tatuape"],
    "mooca": ["bras", "tatuape", "vila-prudente"],
    "cambuci": ["bras", "ipiranga", "vila-mariana"],
    "sacoma": ["ipiranga", "vila-prudente"],
    "ipiranga": ["sacoma", "vila-mariana", "vila-prudente"],
    "tatuape": ["mooca", "bras", "vila-prudente"],
    "itaim-bibi": ["vila-mariana", "santo-amaro"],
    "santo-amaro": ["itaim-bibi", "vila-mariana"],
    "vila-mariana": ["ipiranga", "itaim-bibi", "santo-amaro"],
    "vila-prudente": ["mooca", "ipiranga", "sacoma"],
}

PLACE_PREPOSITIONS: dict[str, tuple[str, str]] = {
    "bras": ("no", "do"),
    "mooca": ("na", "da"),
    "cambuci": ("no", "do"),
    "sacoma": ("no", "do"),
    "ipiranga": ("no", "do"),
    "tatuape": ("no", "do"),
    "itaim-bibi": ("no", "do"),
    "santo-amaro": ("em", "de"),
    "vila-mariana": ("na", "da"),
    "vila-prudente": ("na", "da"),
}


PAGE_CSS = """
html,body{max-width:100%;overflow-x:hidden}.neighborhood-breadcrumb{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:20px;color:#66737d;font-size:.9rem}.neighborhood-breadcrumb a{color:#2c6b57;font-weight:700;text-decoration:none}.neighborhood-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.neighborhood-grid--two{grid-template-columns:repeat(2,minmax(0,1fr))}.neighborhood-grid .detail-card{height:100%;min-width:0}.neighborhood-note{margin-top:24px;padding:18px 20px;border-left:4px solid #d99a3e;background:rgba(217,154,62,.1);border-radius:0 14px 14px 0}.neighborhood-note p{margin:0}.neighborhood-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.neighborhood-links a{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:18px;border:1px solid rgba(15,34,51,.1);border-radius:14px;background:#fff;color:#0f2233;font-weight:700;text-decoration:none}.neighborhood-links a:hover,.neighborhood-links a:focus-visible{border-color:#d99a3e;color:#2c6b57}.cta-actions-v2{flex-wrap:wrap}@media(max-width:800px){.neighborhood-grid,.neighborhood-links{grid-template-columns:1fr 1fr}}@media(max-width:640px){.neighborhood-grid,.neighborhood-grid--two,.neighborhood-links{grid-template-columns:1fr}.cta-actions-v2>*{width:100%;justify-content:center;text-align:center}.detail-hero h1{font-size:clamp(2rem,10vw,3rem);overflow-wrap:break-word}}
""".strip()


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def canonical_url(neighborhood: dict[str, Any]) -> str:
    return f"{SITE['base_url']}/cidades/sao-paulo/{neighborhood['slug']}/"


def place_phrase(neighborhood: dict[str, Any]) -> str:
    return f"{PLACE_PREPOSITIONS[neighborhood['slug']][0]} {neighborhood['name']}"


def possessive_phrase(neighborhood: dict[str, Any]) -> str:
    return f"{PLACE_PREPOSITIONS[neighborhood['slug']][1]} {neighborhood['name']}"


def neighborhood_place(neighborhood: dict[str, Any]) -> dict[str, Any]:
    return {
        "@type": "AdministrativeArea",
        "@id": f"{canonical_url(neighborhood)}#bairro",
        "name": neighborhood["name"],
        "containedInPlace": {
            "@type": "City",
            "name": "São Paulo",
            "containedInPlace": {
                "@type": "State",
                "name": "São Paulo",
            },
        },
    }


def page_schema(neighborhood: dict[str, Any]) -> dict[str, Any]:
    url = canonical_url(neighborhood)
    place = neighborhood_place(neighborhood)
    return {
        "@context": "https://schema.org",
        "@type": "AccountingService",
        "@id": f"{url}#accounting-service",
        "name": f"SoulCont — atendimento contábil {place_phrase(neighborhood)}",
        "url": url,
        "description": neighborhood["page_description"],
        "telephone": PHONE_E164,
        "email": SITE["email"],
        "taxID": SITE["tax_id"],
        "logo": SITE["logo"],
        "image": SITE["logo"],
        "areaServed": place,
        "provider": {
            "@type": "Organization",
            "@id": f"{SITE['base_url']}/#organization",
            "name": SITE["name"],
            "url": f"{SITE['base_url']}/",
            "telephone": PHONE_E164,
            "email": SITE["email"],
        },
        "employee": [
            {
                "@type": "Person",
                "name": PROFESSIONALS[key]["name"],
                "jobTitle": PROFESSIONALS[key]["job_title"],
                "identifier": PROFESSIONALS[key]["registration"],
            }
            for key in SP_REGION["professionals"]
        ],
        "sameAs": SITE["same_as"],
    }


def faq_schema(neighborhood: dict[str, Any]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": neighborhood["faq_q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": neighborhood["faq_a"],
                },
            },
            {
                "@type": "Question",
                "name": f"A SoulCont atende empresas {possessive_phrase(neighborhood)}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"Sim. O atendimento para empresas {possessive_phrase(neighborhood)} "
                        "é realizado on-line. Encontros externos podem ser avaliados "
                        "mediante agendamento e disponibilidade."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": "Quais serviços contábeis podem ser contratados?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "Abertura de empresa, troca de contador, diagnóstico tributário, "
                        "contabilidade fiscal, departamento pessoal e consultoria "
                        "financeira, conforme a necessidade do negócio."
                    ),
                },
            },
        ],
    }


def list_items(items: list[str]) -> str:
    return "\n".join(
        f'<li><i class="fi fi-rr-check-circle"></i> {esc(item)}</li>'
        for item in items
    )


def related_links(slug: str) -> str:
    by_slug = {item["slug"]: item for item in NEIGHBORHOODS}
    return "\n".join(
        (
            f'<a href="/cidades/sao-paulo/{related_slug}/">'
            f'<span>{esc(by_slug[related_slug]["name"])}</span>'
            '<i class="fi fi-rr-arrow-right"></i></a>'
        )
        for related_slug in RELATED_NEIGHBORHOODS[slug]
    )


def render_page(neighborhood: dict[str, Any]) -> str:
    name = esc(neighborhood["name"])
    place = esc(place_phrase(neighborhood))
    possessive = esc(possessive_phrase(neighborhood))
    url = canonical_url(neighborhood)
    description = esc(neighborhood["page_description"])
    page_json = json.dumps(page_schema(neighborhood), ensure_ascii=False, indent=8)
    faq_json = json.dumps(faq_schema(neighborhood), ensure_ascii=False, indent=8)
    professional = PROFESSIONALS[SP_REGION["professionals"][0]]

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0F2233">
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="SoulCont">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="pt_BR">
    <meta property="og:site_name" content="SoulCont">
    <meta property="og:title" content="Contabilidade {place}, São Paulo | SoulCont">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{SITE['logo']}">
    <meta property="og:url" content="{url}">
    <title>Contabilidade {place}, São Paulo | SoulCont</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Syne:wght@500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css">
    <link rel="icon" href="/assets/img/soulcont/favicon.svg?v=2" type="image/svg+xml">
    <link rel="apple-touch-icon" href="/assets/img/soulcont/apple-touch-icon.png" sizes="180x180">
    <link rel="stylesheet" href="/assets/css/main.css?v=3.7">
    <link rel="stylesheet" href="/assets/css/mediaquery.css?v=3.7">
    <link rel="stylesheet" href="/assets/css/site-v2.css?v=1.0">
    <link rel="stylesheet" href="/assets/css/motion.css?v=1.0">
    <link rel="stylesheet" href="/assets/css/soulcont-brand.css?v=1.3">
    <link rel="stylesheet" href="/assets/css/cookies.css?v=4.0">
    <style>{PAGE_CSS}</style>
    <script type="application/ld+json">
{page_json}
    </script>
    <script type="application/ld+json">
{faq_json}
    </script>
</head>
<body>
    <header>
        <div class="logo"><a href="/index.html"><img src="/assets/img/soulcont/wordmark.svg?v=2" alt="Logo SoulCont"></a></div>
        <nav role="navigation" aria-label="Menu principal"><ul class="menu">
            <li><a href="/index.html"><i class="fi fi-rr-home"></i> Home</a></li>
            <li><a href="/HTML/servicos.html"><i class="fi fi-rr-briefcase"></i> Serviços</a></li>
            <li><a href="/HTML/ferramentas.html"><i class="fi fi-rr-calculator"></i> Ferramentas</a></li>
            <li><a href="/HTML/contatos.html"><i class="fi fi-rr-phone-call"></i> Contato</a></li>
        </ul></nav>
        <div class="menu-mobile"><button class="menu-toggle" aria-label="Abrir menu" aria-expanded="false" id="btn-mobile"><i class="fi fi-rr-menu-burger"></i></button></div>
    </header>
    <main class="site-main-v2">
        <section class="section-shell">
            <div class="detail-hero">
                <div class="neighborhood-breadcrumb"><a href="/cidades/">Cidades atendidas</a><span>/</span><a href="/cidades/sao-paulo/">São Paulo</a><span>/</span><strong>{name}</strong></div>
                <span class="eyebrow-label"><i class="fi fi-rr-marker"></i> Área de atendimento em São Paulo</span>
                <h1>Contador para empresas {place}, em São Paulo</h1>
                <p>A SoulCont atende empresas {possessive} on-line, com contato direto com o contador e análise do momento real do negócio.</p>
                <div class="cta-actions-v2"><a href="tel:{PHONE_E164}" class="btn-v2 btn-v2-primary">Ligar para a SoulCont</a><a href="#como-ajudamos" class="btn-v2 btn-v2-secondary">Ver como podemos ajudar</a></div>
                <p class="hero-responsible-line">Atendimento conduzido por {esc(professional['name'])} · {esc(professional['registration'])}</p>
            </div>
        </section>
        <section class="section-block"><div class="section-shell"><div class="neighborhood-grid">
            <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-laptop"></i></span><h2>Atendimento {place}</h2><p>Reuniões e documentos on-line. Encontros presenciais externos dependem de agendamento e disponibilidade.</p></article>
            <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-phone-call"></i></span><h2>Telefone de São Paulo</h2><p><a class="city-link" href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a></p></article>
            <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-bulb"></i></span><h2>{esc(neighborhood['focus'])}</h2><p>{esc(neighborhood['focus_text'])}</p></article>
        </div></div></section>
        <section class="section-block" id="como-ajudamos"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-chart-histogram"></i> Contexto do negócio</span><h2>{esc(neighborhood['context_title'])}</h2><p>{esc(neighborhood['context'])}</p></div>
            <ul class="detail-list">
                {list_items(neighborhood['audiences'])}
            </ul>
            <div class="neighborhood-note"><p>Esta é uma página de área atendida. A SoulCont não divulga unidade física aberta ao público {place}.</p></div>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-compass-alt"></i> Decisões empresariais</span><h2>O que podemos organizar com sua empresa {place}</h2><p>A orientação depende da atividade, do faturamento, da equipe e dos documentos reais do negócio.</p></div>
            <ul class="detail-list">
                {list_items(neighborhood['decisions'])}
            </ul>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-briefcase"></i> Serviços relacionados</span><h2>Apoio para abrir, reorganizar ou desenvolver o negócio</h2></div>
            <div class="neighborhood-links">
                <a href="/servicos/abrir-empresa-em-sao-paulo/"><span>Abrir empresa em São Paulo</span><i class="fi fi-rr-arrow-right"></i></a>
                <a href="/servicos/trocar-de-contador-em-sao-paulo/"><span>Trocar de contador</span><i class="fi fi-rr-arrow-right"></i></a>
                <a href="/servicos/contador-para-prestadores-de-servico-em-sao-paulo/"><span>Contabilidade para prestadores</span><i class="fi fi-rr-arrow-right"></i></a>
            </div>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-map-marker"></i> Regiões relacionadas</span><h2>Conheça também o atendimento em bairros próximos</h2><p>Veja outras páginas da capital e encontre o conteúdo mais próximo da rotina da sua empresa.</p></div>
            <div class="neighborhood-links">
                {related_links(neighborhood['slug'])}
            </div>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-interrogation"></i> Perguntas frequentes</span><h2>Contabilidade para empresas {possessive}</h2></div>
            <div class="faq-details">
                <details><summary>{esc(neighborhood['faq_q'])}</summary><p>{esc(neighborhood['faq_a'])}</p></details>
                <details><summary>A SoulCont atende empresas {possessive}?</summary><p>Sim. O atendimento é on-line, com possibilidade de encontro presencial externo mediante agendamento e disponibilidade.</p></details>
                <details><summary>Quais serviços podem ser contratados?</summary><p>Abertura, troca de contador, diagnóstico tributário, contabilidade fiscal, departamento pessoal e consultoria financeira, conforme a necessidade.</p></details>
            </div>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="final-cta-panel">
            <span class="eyebrow-label"><i class="fi fi-rr-headset"></i> Próximo passo</span>
            <h2>Quer organizar a contabilidade da sua empresa {place}?</h2>
            <p>Converse com a SoulCont e explique o momento do negócio. A análise começa pelo contexto da empresa.</p>
            <div class="cta-actions-v2"><a href="tel:{PHONE_E164}" class="btn-v2 btn-v2-primary">Ligar para {PHONE_DISPLAY}</a><a href="/HTML/contatos.html" class="btn-v2 btn-v2-secondary">Outras formas de contato</a></div>
        </div></div></section>
    </main>
    <footer class="site-footer-v2"><div class="footer-panel-v2"><div class="footer-grid-v2">
        <div class="footer-brand-v2"><strong>SoulCont</strong><p>Contabilidade consultiva com atendimento on-line em São Paulo e encontros externos mediante agendamento.</p></div>
        <div class="footer-group-v2"><h2>Navegação</h2><ul><li><a href="/cidades/sao-paulo/">São Paulo</a></li><li><a href="/HTML/servicos.html">Serviços</a></li><li><a href="/BLOG/">Conteúdos</a></li></ul></div>
        <div class="footer-group-v2"><h2>Contato</h2><ul><li><a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a></li><li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li></ul></div>
    </div><div class="footer-meta-v2"><p>&copy; <span id="current-year">2026</span> SoulCont.</p><p>{esc(professional['name'])} · {esc(professional['registration'])}</p></div></div></footer>
    <script src="/assets/js/menu.js?v=4.1" defer></script>
    <script src="/assets/js/footer.js?v=3.7" defer></script>
    <script src="/assets/js/motion.js?v=1.0" defer></script>
    <script src="/assets/js/main.js?v=1.0" defer></script>
    <script src="/assets/js/soulcont-brand.js?v=1.0" defer></script>
    <script src="/assets/js/cookies.js?v=4.0" defer></script>
</body>
</html>
"""


def validate_neighborhoods() -> None:
    expected = {
        "bras",
        "mooca",
        "cambuci",
        "sacoma",
        "ipiranga",
        "tatuape",
        "itaim-bibi",
        "santo-amaro",
        "vila-mariana",
        "vila-prudente",
    }
    slugs = [item["slug"] for item in NEIGHBORHOODS]
    if set(slugs) != expected or len(slugs) != len(expected):
        raise ValueError("The São Paulo neighborhood dataset must contain the ten required unique slugs")

    required = {
        "name",
        "page_description",
        "context_title",
        "context",
        "focus",
        "focus_text",
        "faq_q",
        "faq_a",
    }
    for item in NEIGHBORHOODS:
        missing = [key for key in required if not str(item.get(key, "")).strip()]
        if missing:
            raise ValueError(f"{item['slug']}: missing fields {missing}")
        if item.get("attendance_mode") != "service_area":
            raise ValueError(f"{item['slug']}: attendance_mode must be service_area")
        if item.get("address") is not None:
            raise ValueError(f"{item['slug']}: neighborhood pages cannot publish an address")
        if item["slug"] not in PLACE_PREPOSITIONS:
            raise ValueError(f"{item['slug']}: missing Portuguese place prepositions")
        if len(item.get("audiences", [])) < 4 or len(item.get("decisions", [])) < 4:
            raise ValueError(f"{item['slug']}: insufficient unique commercial content")
        related = RELATED_NEIGHBORHOODS.get(item["slug"], [])
        if not (2 <= len(related) <= 3):
            raise ValueError(f"{item['slug']}: must link to two or three related neighborhoods")
        if item["slug"] in related or any(slug not in expected for slug in related):
            raise ValueError(f"{item['slug']}: invalid related-neighborhood mapping")


def generate_pages(output_root: Path = DEFAULT_OUTPUT) -> list[Path]:
    validate_neighborhoods()
    generated: list[Path] = []
    for neighborhood in NEIGHBORHOODS:
        target = output_root / neighborhood["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(neighborhood), encoding="utf-8", newline="\n")
        generated.append(target)
    return generated


def main() -> None:
    generated = generate_pages()
    print(f"Generated {len(generated)} São Paulo neighborhood pages")


if __name__ == "__main__":
    main()
