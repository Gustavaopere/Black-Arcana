#!/usr/bin/env python3
"""Check exact resources and four separately sealed static damage contracts."""
import hashlib
import json
import re
import unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest, validate_structure, validate_cards

ROOT = Path(__file__).resolve().parents[2]
FAMILY = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SNAP = FAMILY / "EXACT-RESOURCE-MANIFEST-1.0.10.json"
STATIC_CONTRACTS = {
    "acid": {
        "manifest": "EXACT-ACID-CONTRACT-1.0.10.json",
        "profile": "acid",
        "family": "ACID_DAMAGE_CONTRACT",
        "cards": frozenset({"damage-types/acid.md"}),
    },
    "dark_arrow": {
        "manifest": "EXACT-DREADBOW-CONTRACTS-1.0.10.json",
        "profile": "dreadbow",
        "family": "DREADBOW_AND_DARK_ARROW",
        "cards": frozenset({"damage-types/dark-arrow.md", "equipment/dreadbow.md"}),
    },
    "desolate_dagger": {
        "manifest": "EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json",
        "profile": "desolate_dagger",
        "family": "DESOLATE_DAGGER_CONTRACTS",
        "cards": frozenset({"damage-types/desolate-dagger.md", "equipment/desolate-dagger.md"}),
    },
    "forsaken_sonic_boom": {
        "manifest": "EXACT-FORSAKEN-CONTRACT-1.0.10.json",
        "profile": "forsaken",
        "family": "FORSAKEN_SONIC_CONTRACT",
        "cards": frozenset({"damage-types/forsaken-sonic-boom.md"}),
    },
}


FORSAKEN_PRIOR_MANIFEST_SHA256 = {
    'EXACT-FORSAKEN-SONIC-1.0.10.json': '56c82085ba92270a4058fce09b7e8ccd3cfc7fdd72a2e2e92d92395d8e9709de',
    'EXACT-FORSAKEN-HELPERS-1.0.10.json': '9cbf5578c77e1161cccddb28fcddd7e774b7ac7904175aa0b0c05cf7f1cd26f5',
    'EXACT-FORSAKEN-LIFECYCLE-1.0.10.json': '440f04830670fa222b54591e9b74689900bdfcc120f96f4f0724a084c0fb15fa',
    'EXACT-FORSAKEN-TIMING-1.0.10.json': 'cf3aa736e435452b8d597f3f3eabf353c614efb75344bf755984bea612d0045d',
    'EXACT-FORSAKEN-TARGETING-1.0.10.json': '75032b22493e0fd432be0917656e26cca3340e562a8189e08c26a4bfc7c330ab',
}


def assert_sealed_damage_contract(case, damage_id):
    """A promoted card needs an exact seal and matching static-only ledger evidence."""
    provider = FAMILY.parent
    if damage_id == "forsaken_sonic_boom":
        for name, expected in FORSAKEN_PRIOR_MANIFEST_SHA256.items():
            case.assertEqual(hashlib.sha256((FAMILY / name).read_bytes()).hexdigest(), expected,
                             "historical partial evidence must remain immutable: " + name)
    scope = STATIC_CONTRACTS[damage_id]
    manifest = load_manifest(provider / scope["manifest"])
    validate_structure(manifest, profile=scope["profile"])
    validate_cards(manifest, provider, profile=scope["profile"])
    snapshot = json.loads(SNAP.read_text(encoding="utf8"))
    ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
    case.assertEqual(manifest["catalog_family"], scope["family"])
    case.assertEqual(set(manifest["cards"]), scope["cards"])
    case.assertEqual(set(manifest["contract_evidence"]), scope["cards"])
    case.assertFalse(manifest["provider_universe_closed"])
    case.assertEqual(manifest["semantic_magic_roots"], 8)
    expected_fields = {
        "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
        "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
        "version": "1.0.10",
        "artifact_sha1": snapshot["artifact"]["sha1"],
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
    }
    for card_relative in scope["cards"]:
        case.assertEqual(manifest["cards"][card_relative],
                         hashlib.sha256((provider / card_relative).read_bytes()).hexdigest())
        cert = ledger["objects"][provider.name + "/" + card_relative]
        case.assertEqual(cert["status"], "COMPLETE_PERK_READY")
        for evidence in (cert, manifest):
            for key, expected in expected_fields.items():
                case.assertEqual(evidence[key], expected)
        case.assertEqual(set(cert["evidence"]), {"identity", "behavior", "parameters", "targeting",
                                               "costs", "integration", "validation"})
        for record in cert["evidence"].values():
            case.assertEqual(record["path"], str((provider / card_relative).relative_to(ROOT)))
            case.assertTrue(isinstance(record["reason"], str) and record["reason"].strip())
    relative = "damage-types/" + damage_id.replace("_", "-") + ".md"
    resource = "data/alexscaves/damage_type/" + damage_id + ".json"
    case.assertEqual(manifest["resources"][resource], snapshot["damage_types"][damage_id]["sha256"])
    case.assertIn(resource, manifest["contract_evidence"][relative]["resources"])
    return manifest


class DamageTypeCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(SNAP.read_text(encoding="utf-8"))

    def test_exact_eleven_resource_cards(self):
        ids = set(self.manifest["damage_types"])
        actual = {x.stem.replace("-", "_") for x in FAMILY.glob("*.md")
                  if x.name not in {"INDEX.md", "README.md"}}
        self.assertEqual(ids, actual)
        self.assertEqual(11, len(ids))
        self.assertEqual(6, len(self.manifest["damage_type_tags"]))

    def test_literal_fields_and_direct_tag_memberships(self):
        for id, obj in self.manifest["damage_types"].items():
            with self.subTest(id=id):
                text = (FAMILY / (id.replace("_", "-") + ".md")).read_text(encoding="utf-8")
                self.assertIn("alexscaves:" + id, text)
                self.assertIn(obj["sha256"], text)
                for field in ("message_id", "scaling", "exhaustion"):
                    self.assertIn("| `" + field + "` | `" + str(obj["json"][field]) + "` |", text)
                for tag in self.manifest["direct_tag_entries"][id]:
                    self.assertIn("- `" + tag + "`", text)
                for deny in ("NOT_VERIFIED", "NOT_TESTED"):
                    self.assertIn(deny, text)
                self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY" if id in STATIC_CONTRACTS else "NOT_CERTIFIED", text)
                self.assertIn("**+0 raízes mágicas novas**", text)

    def test_four_static_certificates_have_sealed_cards_and_runtime_limits(self):
        self.assertEqual(set(STATIC_CONTRACTS), {"acid", "dark_arrow", "desolate_dagger", "forsaken_sonic_boom"})
        for id in STATIC_CONTRACTS:
            with self.subTest(id=id):
                assert_sealed_damage_contract(self, id)

    def test_other_seven_damage_types_remain_uncertified(self):
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        remaining = set(self.manifest["damage_types"]) - set(STATIC_CONTRACTS)
        self.assertEqual(len(remaining), 7)
        for id in remaining:
            with self.subTest(id=id):
                relative = FAMILY.parent.name + "/damage-types/" + id.replace("_", "-") + ".md"
                self.assertNotIn(relative, ledger["objects"])

    def test_dark_arrow_ambiguity_is_retained(self):
        a = self.manifest["damage_types"]["dark_arrow"]
        b = self.manifest["damage_types"]["desolate_dagger"]
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertEqual(a["json"]["message_id"], "desolate_dagger")
        text = (FAMILY / "dark-arrow.md").read_text(encoding="utf-8")
        self.assertIn("dois resource IDs diferentes", text)
        self.assertIn("message_id", text)

if __name__ == "__main__":
    unittest.main()
