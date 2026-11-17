#!/usr/bin/env python3
"""Check eleven damage resource cards, nine historical seals and later contracts."""
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
    "spirit_dinosaur": {
        "manifest": "EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json",
        "profile": "spirit_dinosaur",
        "family": "SPIRIT_DINOSAUR_DAMAGE_CONTRACT",
        "cards": frozenset({"damage-types/spirit-dinosaur.md"}),
    },
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
    "radiation": {
        "manifest": "EXACT-RADIATION-CONTRACT-1.0.10.json",
        "profile": "radiation",
        "family": "RADIATION_DAMAGE_CONTRACT",
        "cards": frozenset({"damage-types/radiation.md"}),
    },
    "gumball": {
        "manifest": "EXACT-GUMBALL-CONTRACTS-1.0.10.json",
        "profile": "gumball",
        "family": "GUMBALL_CONTRACTS",
        "cards": frozenset({"damage-types/gumball.md", "equipment/shot-gum.md"}),
    },

    "intentional_game_design": {
        "manifest": "EXACT-NUCLEAR-CONTRACTS-1.0.10.json",
        "profile": "nuclear",
        "family": "NUCLEAR_DAMAGE_CONTRACTS",
        "cards": frozenset({"damage-types/intentional-game-design.md", "damage-types/nuke.md"}),
    },
    "nuke": {
        "manifest": "EXACT-NUCLEAR-CONTRACTS-1.0.10.json",
        "profile": "nuclear",
        "family": "NUCLEAR_DAMAGE_CONTRACTS",
        "cards": frozenset({"damage-types/intentional-game-design.md", "damage-types/nuke.md"}),
    },
}


NEW_DAMAGE_TYPE_STATIC = frozenset({"tremorzilla_beam", "raygun"})

FORSAKEN_PRIOR_MANIFEST_SHA256 = {
    'EXACT-FORSAKEN-SONIC-1.0.10.json': '56c82085ba92270a4058fce09b7e8ccd3cfc7fdd72a2e2e92d92395d8e9709de',
    'EXACT-FORSAKEN-HELPERS-1.0.10.json': '9cbf5578c77e1161cccddb28fcddd7e774b7ac7904175aa0b0c05cf7f1cd26f5',
    'EXACT-FORSAKEN-LIFECYCLE-1.0.10.json': '440f04830670fa222b54591e9b74689900bdfcc120f96f4f0724a084c0fb15fa',
    'EXACT-FORSAKEN-TIMING-1.0.10.json': 'cf3aa736e435452b8d597f3f3eabf353c614efb75344bf755984bea612d0045d',
    'EXACT-FORSAKEN-TARGETING-1.0.10.json': '75032b22493e0fd432be0917656e26cca3340e562a8189e08c26a4bfc7c330ab',
}


GUMBALL_PRIOR_MANIFEST_SHA256 = {
    "EXACT-GUMBALL-IMPACT-1.0.10.json": "9c906ae9c44d01f7a1ca38f3b43c7ea4280bc3d49cee7bb9346bf66ae6b48198",
    "EXACT-GUMBALL-PRODUCERS-1.0.10.json": "a618be101c4c73384a7bf0b32fb2202b5e9ebdce371d4cc442be0a0fe723c455",
    "EXACT-GUMBALL-STATE-1.0.10.json": "e2c74f0e2999e8b7286f21f89494cd84b8c0aafee4dcbb7c6ec190610a19a0e1",
    "EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json": "2ace1627c2fd451a23d0aae596301d4d1037d1e03994cc4b21adbaed7e048f9e"
}

NUCLEAR_PRIOR_MANIFEST_SHA256 = {'EXACT-NUCLEAR-CHUNK-LIFECYCLE-1.0.10.json': '685b250b6ec56f1e9139619e7202c39641e5426cbd11b1c4ccf330b344f0202c', 'EXACT-NUCLEAR-ENVELOPE-1.0.10.json': '6bb9d1dabb8d3fb333a795a6a428f35caa77da42192f07e4da9c486f6f759bc1', 'EXACT-NUCLEAR-NUMERIC-1.0.10.json': '3923074f3915e9f01c3b15117fdc08aed8bd68e1f8182e1eeff4c0275b0bc34d', 'EXACT-NUCLEAR-PRODUCERS-1.0.10.json': 'c7314202887c12af9007680ce455ea5de984c8e8482ae612d5c99be1ff32e6ea', 'EXACT-NUCLEAR-TARGET-WORLD-1.0.10.json': 'f37f7ea49653a7ec050869880b0f070a9629aabfa6a12aeca908eac155dc3b25', 'EXACT-NEOFORGE-TICKETS-21.1.248.json': '61625bef510ebe5e34a65b69e60cdd4a9a2cd9fc2689701620fdb98c72016d3c'}

def assert_sealed_damage_contract(case, damage_id):
    """A promoted card needs an exact seal and matching static-only ledger evidence."""
    provider = FAMILY.parent
    if damage_id == "forsaken_sonic_boom":
        for name, expected in FORSAKEN_PRIOR_MANIFEST_SHA256.items():
            case.assertEqual(hashlib.sha256((FAMILY / name).read_bytes()).hexdigest(), expected,
                             "historical partial evidence must remain immutable: " + name)
    if damage_id == "gumball":
        for name, expected in GUMBALL_PRIOR_MANIFEST_SHA256.items():
            case.assertEqual(hashlib.sha256((provider / name).read_bytes()).hexdigest(), expected,
                             "historical partial evidence must remain immutable: " + name)
    if damage_id in {"intentional_game_design", "nuke"}:
        for name, expected in NUCLEAR_PRIOR_MANIFEST_SHA256.items():
            case.assertEqual(hashlib.sha256((provider / name).read_bytes()).hexdigest(), expected,
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
                  if x.name not in {"INDEX.md", "README.md"}
                  and not x.name.startswith("EXACT-")}
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
                    self.assertIn("`" + tag + "`", text)
                for deny in ("NOT_VERIFIED", "NOT_TESTED"):
                    self.assertIn(deny, text)
                self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY" if id in STATIC_CONTRACTS or id in NEW_DAMAGE_TYPE_STATIC else "NOT_CERTIFIED", text)
                self.assertIn("**+0 raízes mágicas**" if id == "raygun"
                              else "**+0 raízes mágicas novas**", text)

    def test_nine_static_certificates_have_sealed_cards_and_runtime_limits(self):
        self.assertEqual(set(STATIC_CONTRACTS), {"acid", "dark_arrow", "desolate_dagger", "forsaken_sonic_boom", "gumball", "radiation", "intentional_game_design", "nuke", "spirit_dinosaur"})
        for id in STATIC_CONTRACTS:
            with self.subTest(id=id):
                assert_sealed_damage_contract(self, id)

    def test_tremorzilla_beam_individual_static_seal_and_runtime_boundaries(self):
        provider = FAMILY.parent
        path = provider / "EXACT-TREMORZILLA-BEAM-STATIC-1.0.10.json"
        cert = json.loads(path.read_text(encoding="utf-8"))
        ledger = json.loads(
            (ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text()
        )
        relative = provider.name + "/damage-types/tremorzilla-beam.md"
        entry = ledger["objects"][relative]
        self.assertEqual(cert["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["enchantment"], "alexscaves:tremorzilla_beam")
        self.assertEqual(cert["artifact"]["sha1"],
                         self.manifest["artifact"]["sha1"])
        resource = cert["resource"]["data/alexscaves/damage_type/tremorzilla_beam.json"]
        self.assertEqual(resource["sha256"],
                         self.manifest["damage_types"]["tremorzilla_beam"]["sha256"])
        self.assertEqual(len(cert["native_full_method_census"]), 12)
        self.assertEqual(sum(m["instruction_count"]
                             for m in cert["native_full_method_census"]), 2808)
        self.assertEqual(cert["native_damage_factory"]["instructions"], 13)
        self.assertEqual(cert["damage_helper_opcode_pivots"], 46)
        self.assertEqual(cert["producer_calls"]["tickBreath"], [552, 578])
        self.assertEqual(len(cert["producer_calls"]["tick"]), 7)
        self.assertEqual(cert["producer_calls"]["stompEffect"], [357])
        self.assertEqual(cert["direct_damage_tags_in_publisher"], [])
        self.assertEqual(entry["status"], "COMPLETE_PERK_READY")
        self.assertEqual(entry["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(entry["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(entry["artifact_sha1"], self.manifest["artifact"]["sha1"])
        self.assertEqual(entry["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(entry["physical_qa"], "NOT_TESTED")
        self.assertEqual(set(entry["evidence"]),
                         {"identity","behavior","parameters","targeting",
                          "costs","integration","validation"})
        for proof in entry["evidence"].values():
            self.assertTrue((ROOT / proof["path"]).is_file())
            self.assertGreaterEqual(len(proof["reason"].strip()), 18)
        self.assertEqual(cert["safety"]["mutation"], "NO_MUTATION")
        self.assertEqual(cert["safety"]["world_effect_policy"], "NOT_VERIFIED")
        self.assertEqual(cert["safety"]["physical_qa"], "NOT_TESTED")
        self.assertFalse(cert["safety"]["provider_universe_closed"])

    def test_last_damage_type_raygun_has_separate_static_contract(self):
        ledger = json.loads(
            (ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text()
        )
        remaining = set(self.manifest["damage_types"]) - set(STATIC_CONTRACTS) - NEW_DAMAGE_TYPE_STATIC
        self.assertFalse(remaining)
        provider = FAMILY.parent
        seal = json.loads((provider / "EXACT-RAYGUN-CONTRACT-1.0.10.json").read_text())
        entry = ledger["objects"][provider.name + "/damage-types/raygun.md"]
        self.assertEqual(seal["primary_resource"]["sha256"],
                         self.manifest["damage_types"]["raygun"]["sha256"])
        self.assertEqual(seal["primary_resource"]["json"],
                         self.manifest["damage_types"]["raygun"]["json"])
        self.assertEqual(seal["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(entry["claim_scope"], seal["claim_scope"])
        self.assertEqual(set(entry["evidence"]),
                         {"identity", "behavior", "parameters", "targeting",
                          "costs", "integration", "validation"})
        self.assertEqual(seal["census"]["declared_methods"], 26)
        self.assertEqual(len(seal["method_dispositions"]), 26)
        for key, value in {"mutating_hook": "NOT_VERIFIED",
                           "physical_qa": "NOT_TESTED",
                           "provider_universe_closed": False}.items():
            self.assertEqual(seal["safety"][key], value)
        archive = FAMILY / "EXACT-RAYGUN-HISTORICAL-CARD-1.0.10.md"
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),
                         "75f033bc9c27195c85ca952e0b70bc18ff00f5f1aba1955e58242c98c11e0f87")

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
