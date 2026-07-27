from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from generate_sp_bairros import (
    NEIGHBORHOODS,
    PHONE_E164,
    RELATED_NEIGHBORHOODS,
    canonical_url,
    generate_pages,
    page_schema,
    render_page,
    validate_neighborhoods,
)


EXPECTED_SLUGS = {
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


class NeighborhoodDatasetTests(unittest.TestCase):
    def test_dataset_contains_only_required_unique_neighborhoods(self) -> None:
        validate_neighborhoods()
        self.assertEqual({item["slug"] for item in NEIGHBORHOODS}, EXPECTED_SLUGS)
        self.assertEqual(len(NEIGHBORHOODS), 10)

    def test_all_pages_are_service_areas_without_addresses(self) -> None:
        for item in NEIGHBORHOODS:
            self.assertEqual(item["attendance_mode"], "service_area")
            self.assertIsNone(item["address"])

    def test_commercial_copy_is_unique(self) -> None:
        self.assertEqual(
            len({item["page_description"] for item in NEIGHBORHOODS}), 10
        )
        self.assertEqual(len({item["context"] for item in NEIGHBORHOODS}), 10)
        self.assertEqual(len({item["faq_q"] for item in NEIGHBORHOODS}), 10)


class NeighborhoodSchemaTests(unittest.TestCase):
    def test_area_served_is_a_neighborhood_inside_sao_paulo(self) -> None:
        for item in NEIGHBORHOODS:
            schema = page_schema(item)
            area = schema["areaServed"]

            self.assertEqual(area["@type"], "AdministrativeArea")
            self.assertEqual(area["name"], item["name"])
            self.assertEqual(area["containedInPlace"]["@type"], "City")
            self.assertEqual(area["containedInPlace"]["name"], "São Paulo")
            self.assertEqual(
                area["containedInPlace"]["containedInPlace"]["@type"], "State"
            )
            self.assertNotIn("address", schema)
            self.assertEqual(schema["telephone"], PHONE_E164)

    def test_canonical_and_schema_ids_are_unique(self) -> None:
        urls = [canonical_url(item) for item in NEIGHBORHOODS]
        ids = [page_schema(item)["@id"] for item in NEIGHBORHOODS]

        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(len(ids), len(set(ids)))


class NeighborhoodRendererTests(unittest.TestCase):
    def test_each_page_has_own_canonical_one_h1_and_sp_phone(self) -> None:
        for item in NEIGHBORHOODS:
            source = render_page(item)
            self.assertIn(f'<link rel="canonical" href="{canonical_url(item)}">', source)
            self.assertEqual(len(re.findall(r"<h1(?:\s[^>]*)?>", source)), 1)
            self.assertIn(f'href="tel:{PHONE_E164}"', source)
            self.assertNotIn("Rua São José", source)

    def test_all_json_ld_blocks_are_valid(self) -> None:
        for item in NEIGHBORHOODS:
            source = render_page(item)
            blocks = re.findall(
                r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
                source,
                flags=re.IGNORECASE | re.DOTALL,
            )
            self.assertEqual(len(blocks), 2)
            for block in blocks:
                json.loads(block)

    def test_each_page_links_to_related_neighborhoods(self) -> None:
        for item in NEIGHBORHOODS:
            source = render_page(item)
            related = RELATED_NEIGHBORHOODS[item["slug"]]
            self.assertGreaterEqual(len(related), 2)
            for slug in related:
                self.assertIn(f'href="/cidades/sao-paulo/{slug}/"', source)

    def test_portuguese_place_prepositions(self) -> None:
        rendered = {item["slug"]: render_page(item) for item in NEIGHBORHOODS}
        self.assertIn("Contabilidade na Mooca", rendered["mooca"])
        self.assertIn("Contabilidade em Santo Amaro", rendered["santo-amaro"])
        self.assertIn("Contabilidade na Vila Mariana", rendered["vila-mariana"])
        self.assertIn("Contabilidade na Vila Prudente", rendered["vila-prudente"])

    def test_generator_writes_only_the_ten_neighborhood_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "cidades" / "sao-paulo"
            generated = generate_pages(output_root)
            relative = {
                path.relative_to(output_root).as_posix() for path in generated
            }

            self.assertEqual(
                relative,
                {f"{slug}/index.html" for slug in EXPECTED_SLUGS},
            )
            self.assertFalse((output_root / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
