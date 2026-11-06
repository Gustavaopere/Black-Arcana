#!/usr/bin/env python3
"""Regression for native Rapid Possession data and movement contract; no mutators."""
import hashlib,json,unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,validate_cards
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
CARD="enchantments/rapid-possession.md"
SEAL="EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.json"
OWNER="com/github/alexmodguy/alexscaves/server/item/TotemOfPossessionItem.class"

class RapidPossessionContract(unittest.TestCase):
    def read(self):
        s=json.loads((P/SEAL).read_text(encoding="utf8"))
        d=load_manifest(P/"EXACT-TECHNICAL-CONTRACTS-1.0.10.json")
        validate_structure(d,profile="actions")
        validate_cards(d,P,profile="actions")
        self.assertEqual(s["catalog_family"],"RAPID_POSSESSION_ENCHANTMENT_CONTRACT")
        for key,val in (("claim_scope","STATIC_TECHNICAL_CATALOG_ONLY"),
                        ("evidence_grade","SHA_EXACT_BINARY_BEHAVIOR"),
                        ("mutating_hook","NOT_VERIFIED"),("physical_qa","NOT_TESTED"),
                        ("mutation","NO_MUTATION")):
            self.assertEqual(s[key],val)
        self.assertFalse(s["provider_universe_closed"])
        self.assertEqual(s["artifact"]["sha256"],d["artifact_sha256"])
        self.assertEqual(s["resource"]["sha256"],d["resources"]["data/alexscaves/enchantment/rapid_possession.json"])
        self.assertEqual(hashlib.sha256((P/CARD).read_bytes()).hexdigest(),s["card"]["sha256"])
        return s,d
    def test_publisher_identity_data_costs(self):
        s,d=self.read()
        j=s["resource"]["json"]
        self.assertEqual(j["description"]["translate"],"enchantment.alexscaves.rapid_possession")
        self.assertEqual(j["supported_items"],"#alexscaves:enchantable/totem_of_possession")
        self.assertEqual((j["weight"],j["max_level"],j["anvil_cost"],j["slots"]),(10,3,1,["mainhand"]))
        self.assertEqual(j["min_cost"],{"base":1,"per_level_above_first":5})
        self.assertEqual(j["max_cost"],{"base":41,"per_level_above_first":10})
        self.assertEqual(s["item_tag"]["json"],{"values":["alexscaves:totem_of_possession"]})
        self.assertIn("move faster",s["english_translations"]["enchantment.alexscaves.rapid_possession.desc"])
    def test_speed_pivots_native_and_old_action_immutability(self):
        s,d=self.read()
        self.assertEqual(s["reused_binary_manifest"]["unchanged_action_card_sha256"],d["cards"]["actions/totem-possession-remote-control.md"])
        self.assertEqual(s["on_use_tick"]["owner"],OWNER)
        m=[x for x in d["classes"][OWNER]["methods"] if x["name"]=="onUseTick"]
        self.assertEqual(len(m),1)
        self.assertEqual(s["on_use_tick"]["descriptor"],m[0]["descriptor"])
        self.assertEqual(s["on_use_tick"]["inherited_anchors"],m[0]["anchors"])
        rows={x["offset"]:x for x in s["on_use_tick"]["level_expression_anchors"]}
        self.assertEqual(len(rows),len(s["on_use_tick"]["level_expression_anchors"]))
        self.assertEqual(rows[318]["symbol"],"float 1.25f")
        self.assertEqual(rows[321]["symbol"],"float 0.35f")
        self.assertIn("RAPID_POSSESSION",rows[325]["symbol"])
        self.assertIn("ACCompat.enchantLevel",rows[328]["symbol"])
        self.assertEqual([rows[x]["opcode"] for x in (331,332,333,334)],["i2f","fmul","fadd","fstore"])
        self.assertEqual(rows[310]["symbol"],"float 32.0f")
        self.assertEqual(s["limits"]["native_anchor_count"],
                         len(m[0]["anchors"])+len(s["on_use_tick"]["level_expression_anchors"]))
        for cl,hashval in s["class_hashes"].items():
            self.assertEqual(hashval,d["classes"][cl]["sha256"])
    def test_speed_formula_and_command_range_are_distinct(self):
        s,d=self.read()
        for level,factor,nonmob in ((0,1.25,0.1875),(1,1.60,0.24),
                                     (2,1.95,0.2925),(3,2.30,0.345)):
            self.assertAlmostEqual(1.25+0.35*level,factor,places=6)
            self.assertAlmostEqual(0.15*factor,nonmob,places=6)
        inherited={x["offset"]:x for x in s["on_use_tick"]["inherited_anchors"]}
        self.assertIn("float 32.0f",inherited[310]["symbol"])
        self.assertIn("PathNavigation.moveTo",inherited[404]["symbol"])
        self.assertIn("float 0.15f",inherited[601]["symbol"])
        self.assertIn("double 0.800000011920929d",inherited[637]["symbol"])
        self.assertIn("double 3.0d",inherited[722]["symbol"])
        self.assertIn("Player.attack",inherited[1073]["symbol"])
        self.assertIn("resetAttackStrengthTicker",inherited[1078]["symbol"])
        self.assertTrue(s["limits"]["no_claimed_server_wear"])
        self.assertEqual(s["limits"]["actual_speed_blocks_per_tick"],"NOT_CERTIFIED")
    def test_certificate_and_alphabetical_progress(self):
        s,d=self.read()
        ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cert=ledger["objects"][P.name+"/"+CARD]
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),{"identity","behavior","parameters","targeting","costs","integration","validation"})
        self.assertEqual({x["path"] for x in cert["evidence"].values()},
                         {str((P/CARD).relative_to(ROOT))})
        cross=(P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        cards=[p for p in (P/"enchantments").glob("*.md") if p.name not in ("INDEX.md","README.md")]
        full=[k for k in ledger["objects"] if k.startswith(P.name+"/enchantments/")]
        for expected in (f"individual_full_enchantment_dossiers={len(full)}/51",
                         f"individual_partial_enchantment_dossiers={len(cards)-len(full)}/51",
                         f"individual_existing_enchantment_dossiers={len(cards)}/51",
                         "| ✅ | `alexscaves:rapid_possession`"):
            self.assertIn(expected,cross)
if __name__=="__main__":unittest.main()
