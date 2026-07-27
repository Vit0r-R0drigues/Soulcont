from __future__ import annotations

import json
import re
import unittest

from cidades_config import regionalize_city, validate_city_dataset
from generate_cidades import CITIES, page_schema, render_city


def sample_city(**overrides: object) -> dict:
    city = {
        "slug": "sao-paulo",
        "name": "São Paulo",
        "region": "sao-paulo",
        "attendance_mode": "service_area",
        "context_title": "Contabilidade consultiva para empresas de São Paulo",
        "context": "Atendimento contábil com análise do contexto da empresa.",
        "focus": "Prestadores de serviços",
        "focus_text": "Troca de contador, abertura e revisão tributária.",
        "audiences": ["Prestadores de serviços", "Pequenas empresas"],
        "decisions": ["Revisar o regime", "Organizar a troca de contador"],
        "faq_q": "Como funciona o atendimento em São Paulo?",
        "faq_a": "O atendimento é on-line, com encontros externos agendados.",
    }
    city.update(overrides)
    return regionalize_city(city)


class CityDatasetTests(unittest.TestCase):
    def test_current_dataset_is_valid(self) -> None:
        validate_city_dataset(CITIES)

    def test_sao_paulo_municipal_pages_are_service_areas_without_addresses(self) -> None:
        expected_slugs = {
            "guarulhos",
            "osasco",
            "barueri",
            "santo-andre",
            "sao-bernardo-do-campo",
        }
        municipal_pages = {
            city["slug"]: city for city in CITIES if city["slug"] in expected_slugs
        }

        self.assertEqual(set(municipal_pages), expected_slugs)
        for city in municipal_pages.values():
            self.assertEqual(city["region"], "sao-paulo")
            self.assertEqual(city["attendance_mode"], "service_area")
            self.assertEqual(city["phone_e164"], "+5511916539680")
            self.assertIsNone(city["address"])
            self.assertEqual(city["service_areas"], [city["name"]])

    def test_service_area_cannot_publish_an_address(self) -> None:
        city = sample_city(address={"streetAddress": "Endereço indevido"})
        self.assertIsNone(city["address"])

    def test_digital_city_does_not_inherit_the_regional_address(self) -> None:
        city = sample_city(
            slug="cedro",
            name="Cedro",
            region="ceara",
            attendance_mode="digital",
        )
        self.assertIsNone(city["address"])
        self.assertNotIn("address", page_schema(city))

    def test_public_location_requires_an_address(self) -> None:
        city = sample_city(attendance_mode="public_location", address=None)
        with self.assertRaisesRegex(ValueError, "requires an address"):
            validate_city_dataset([city])


class CityRendererTests(unittest.TestCase):
    def test_sao_paulo_uses_its_own_phone_state_and_attendance(self) -> None:
        source = render_city(sample_city())

        self.assertIn("Contabilidade em São Paulo, São Paulo", source)
        self.assertIn('href="tel:+5511916539680"', source)
        self.assertIn("(11) 91653-9680", source)
        self.assertNotIn("+5588921791670", source)
        self.assertNotIn("Rua São José", source)
        self.assertIn("encontros presenciais externos mediante agendamento", source)

    def test_generated_page_preserves_consent_assets_and_analytics_loader(self) -> None:
        source = render_city(sample_city())

        self.assertIn("/assets/css/cookies.css?v=4.0", source)
        self.assertIn("/assets/js/cookies.js?v=4.0", source)

    def test_schema_has_page_specific_id_and_omits_hidden_address(self) -> None:
        city = sample_city()
        schema = page_schema(city)

        self.assertEqual(
            schema["@id"],
            "https://soulcontt.com.br/cidades/sao-paulo/#accounting-service",
        )
        self.assertEqual(schema["telephone"], "+5511916539680")
        self.assertEqual(
            schema["areaServed"][0]["containedInPlace"]["name"], "São Paulo"
        )
        self.assertNotIn("address", schema)

    def test_json_ld_blocks_are_valid_json(self) -> None:
        source = render_city(sample_city())
        blocks = re.findall(
            r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
            source,
            flags=re.IGNORECASE | re.DOTALL,
        )

        self.assertEqual(len(blocks), 2)
        for block in blocks:
            json.loads(block)

    def test_city_pages_do_not_share_schema_ids(self) -> None:
        sao_paulo = page_schema(sample_city())
        guarulhos = page_schema(sample_city(slug="guarulhos", name="Guarulhos"))

        self.assertNotEqual(sao_paulo["@id"], guarulhos["@id"])


if __name__ == "__main__":
    unittest.main()
