from __future__ import annotations

from copy import deepcopy
from typing import Any


SITE = {
    "name": "SoulCont",
    "base_url": "https://soulcontt.com.br",
    "email": "contato@soulcont.com",
    "tax_id": "63.937.299/0001-25",
    "logo": "https://soulcontt.com.br/assets/img/soulcont/favicon-512.png",
    "og_image": "https://soulcontt.com.br/assets/img/soulcont/og-soulcont.jpg",
    "same_as": [
        "https://www.instagram.com/soulcontt/",
        "https://www.youtube.com/@contabilidadeempresarial",
    ],
}


PROFESSIONALS = {
    "vitor": {
        "name": "Vitor Rodrigues de Lima",
        "job_title": "Contador responsável",
        "registration": "CRC SP353836",
        "image": "/assets/img/soulcont/vitor-rodrigues-retrato-3x4.webp",
    },
    "leonardo": {
        "name": "Leonardo Silva de Sousa",
        "job_title": "Contador responsável",
        "registration": "CRCCE 024206/O5",
        "image": "/assets/img/soulcont/leonardo-silva-retrato-real-640w.webp",
    },
}


REGIONS = {
    "ceara": {
        "state_name": "Ceará",
        "state_code": "CE",
        "phone_e164": "+5588921791670",
        "phone_display": "(88) 92179-1670",
        "base_city": "Icó",
        "base_description": "com base operacional em Icó, Ceará",
        "footer_description": (
            "Contabilidade consultiva com sede em Icó e atendimento digital "
            "para empresas do Ceará."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Rua São José, 1245 - Novo Centro",
            "addressLocality": "Icó",
            "addressRegion": "CE",
            "postalCode": "63430-000",
            "addressCountry": "BR",
        },
        "professionals": ["vitor", "leonardo"],
    },
    "sao-paulo": {
        "state_name": "São Paulo",
        "state_code": "SP",
        "phone_e164": "+5511916539680",
        "phone_display": "(11) 91653-9680",
        "base_city": "São Paulo",
        "base_description": (
            "com atendimento on-line e encontros presenciais externos mediante agendamento"
        ),
        "footer_description": (
            "Contabilidade consultiva com atendimento on-line em São Paulo e "
            "encontros presenciais externos mediante agendamento."
        ),
        # A unidade paulista não recebe o público em endereço comercial. Manter
        # este valor nulo evita publicar um endereço de área de atendimento.
        "address": None,
        "professionals": ["vitor"],
        "related_services": [
            {
                "label": "Abrir empresa em São Paulo",
                "url": "/servicos/abrir-empresa-em-sao-paulo/",
            },
            {
                "label": "Trocar de contador em São Paulo",
                "url": "/servicos/trocar-de-contador-em-sao-paulo/",
            },
            {
                "label": "Contabilidade para prestadores de serviço",
                "url": "/servicos/contador-para-prestadores-de-servico-em-sao-paulo/",
            },
        ],
        "related_articles": [
            {
                "label": "Como abrir uma empresa em São Paulo",
                "url": "/BLOG/posts/abrir-empresa-em-sao-paulo.html",
            },
            {
                "label": "Como trocar de contador em São Paulo",
                "url": "/BLOG/posts/trocar-de-contador-em-sao-paulo.html",
            },
        ],
    },
}


DEFAULT_REGION = "ceara"
ATTENDANCE_MODES = {"public_location", "digital", "service_area"}


def _attendance_mode(city: dict[str, Any]) -> str:
    explicit = city.get("attendance_mode")
    if explicit:
        return explicit

    legacy_mode = city.get("mode")
    if legacy_mode == "presencial":
        return "public_location"
    if legacy_mode == "digital":
        return "digital"
    return "service_area"


def regionalize_city(city: dict[str, Any]) -> dict[str, Any]:
    """Return a city record enriched with its regional operating data."""

    result = deepcopy(city)
    region_key = result.get("region", DEFAULT_REGION)
    if region_key not in REGIONS:
        raise ValueError(f"Unknown city region: {region_key}")

    region = REGIONS[region_key]
    mode = _attendance_mode(result)
    if mode not in ATTENDANCE_MODES:
        raise ValueError(
            f"{result.get('slug', '<missing slug>')}: invalid attendance mode {mode}"
        )

    result["region"] = region_key
    result["attendance_mode"] = mode
    for key in (
        "state_name",
        "state_code",
        "phone_e164",
        "phone_display",
        "base_city",
        "base_description",
        "footer_description",
    ):
        result.setdefault(key, region[key])

    result.setdefault("professionals", list(region["professionals"]))
    result.setdefault("service_areas", [result["name"]])

    if "address" not in result:
        result["address"] = deepcopy(region["address"])
    if mode != "public_location":
        # Páginas digitais e de área de atendimento não podem herdar o
        # endereço físico de uma unidade localizada em outra cidade.
        result["address"] = None

    return result


def validate_city_dataset(cities: list[dict[str, Any]]) -> None:
    required_text_fields = {
        "slug",
        "name",
        "state_name",
        "state_code",
        "phone_e164",
        "phone_display",
        "context_title",
        "context",
        "focus",
        "focus_text",
        "faq_q",
        "faq_a",
    }
    seen_slugs: set[str] = set()

    for city in cities:
        missing = sorted(
            field for field in required_text_fields if not str(city.get(field, "")).strip()
        )
        if missing:
            raise ValueError(f"{city.get('slug', '<missing slug>')}: missing {missing}")

        slug = city["slug"]
        if slug in seen_slugs:
            raise ValueError(f"Duplicate city slug: {slug}")
        seen_slugs.add(slug)

        if not city["phone_e164"].startswith("+55"):
            raise ValueError(f"{slug}: phone_e164 must use Brazilian E.164 format")
        if not city.get("audiences") or not city.get("decisions"):
            raise ValueError(f"{slug}: audiences and decisions cannot be empty")
        if not city.get("service_areas") or not all(
            str(area).strip() for area in city["service_areas"]
        ):
            raise ValueError(f"{slug}: service_areas cannot be empty")

        mode = city["attendance_mode"]
        if mode not in ATTENDANCE_MODES:
            raise ValueError(f"{slug}: invalid attendance mode {mode}")
        if mode == "public_location" and not city.get("address"):
            raise ValueError(f"{slug}: a public location requires an address")
        if mode == "service_area" and city.get("address"):
            raise ValueError(f"{slug}: service-area pages cannot expose an address")

        unknown_professionals = [
            key for key in city["professionals"] if key not in PROFESSIONALS
        ]
        if unknown_professionals:
            raise ValueError(f"{slug}: unknown professionals {unknown_professionals}")
