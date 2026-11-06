#!/usr/bin/env python3
"""Plummeting Flight exact static dossier: fail-closed causal regression."""
import hashlib,json,unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,validate_cards
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PRE="com/github/alexmodguy/alexscaves/"
SPEAR=PRE+"server/entity/item/ExtinctionSpearEntity.class"
SPIRIT=PRE+"server/entity/item/DinosaurSpiritEntity.class"
CARD="enchantments/plummeting-flight.md"
class PlummetingFlightContract(unittest.TestCase):
    def contracts(self):
        s=json.loads((P/"EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.json").read_text(encoding="utf-8"))
        d=load_manifest(P/"EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json")
        validate_structure(d,profile="spirit_dinosaur")
        validate_cards(d,P,profile="spirit_dinosaur")
        self.assertEqual(s["catalog_family"],"PLUMMETING_FLIGHT_ENCHANTMENT_CONTRACT")
        self.assertEqual(s["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(s["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(s["physical_qa"],"NOT_TESTED")
        self.assertEqual(s["mutation"],"NO_MUTATION")
        self.assertFalse(s["provider_universe_closed"])
        self.assertEqual(s["artifact"]["sha256"],d["artifact_sha256"])
        self.assertEqual(s["resource"]["sha256"],d["resources"]["data/alexscaves/enchantment/plummeting_flight.json"])
        self.assertEqual(hashlib.sha256((P/CARD).read_bytes()).hexdigest(),s["card"]["sha256"])
        return s,d
    def anchors(self,d,cl,name):
        a=[m for m in d["classes"][cl]["methods"] if m["name"]==name]
        self.assertEqual(len(a),1,(cl,name))
        return {x["offset"]:x for x in a[0]["anchors"]}
    def test_json_and_costs(self):
        s,d=self.contracts();j=s["resource"]["json"]
        self.assertEqual((j["weight"],j["max_level"],j["anvil_cost"],j["slots"]),(2,3,4,["mainhand"]))
        self.assertEqual(j["min_cost"],{"base":1,"per_level_above_first":13})
        self.assertEqual(j["max_cost"],{"base":41,"per_level_above_first":10})
        self.assertEqual(j["supported_items"],"#alexscaves:enchantable/extinction_spear")
        self.assertEqual(s["item_tag"]["json"],{"values":["alexscaves:extinction_spear"]})
        self.assertEqual(s["portuguese_translations"],{})
    def test_all_pivots_match_parent_and_artifact(self):
        s,d=self.contracts()
        self.assertGreaterEqual(len(s["anchors"]),300)
        self.assertEqual(len(s["anchors"]),s["limits"]["sealed_pivots"])
        self.assertEqual(set(s["class_hashes"]),{x["class"] for x in s["anchors"]})
        for cl,sha in s["class_hashes"].items():self.assertEqual(sha,d["classes"][cl]["sha256"])
        for x in s["anchors"]:
            row=self.anchors(d,x["class"],x["method"])[x["offset"]]
            self.assertEqual({k:x[k] for k in ("offset","opcode","operand","symbol")},
                             {k:row[k] for k in ("offset","opcode","operand","symbol")})
    def test_accepted_spear_hit_and_level_transfer(self):
        s,d=self.contracts();a=self.anchors(d,SPEAR,"onHitEntity")
        for off,sym in ((5,"10.0f"),(29,"damageBonus"),(58,"causeSpiritDinosaurDamage"),
                        (85,"igniteForSeconds"),(92,"ACCompat.hurt"),(201,"SUBTERRANODON"),
                        (245,"PLUMMETING_FLIGHT"),(248,"enchantLevel"),(251,"setEnchantmentLevel"),
                        (277,"addFreshEntity")):self.assertIn(sym,a[off]["symbol"])
        self.assertEqual((a[95]["opcode"],a[95]["operand"]),("ifeq","281"))
        self.assertEqual(a[108]["opcode"],"return")
        self.assertEqual((a[150]["opcode"],a[150]["operand"]),("ifnull","281"))
        self.assertEqual(a[280]["opcode"],"pop")
    def test_vertical_movement_is_not_guaranteed_height(self):
        s,d=self.contracts();a=self.anchors(d,SPIRIT,"tickSubterranodon")
        for off,sym in ((11,"0.03d"),(14,"0.005f"),(18,"getEnchantmentLevel"),
                        (29,"setDeltaMovement"),(68,"Vec3.ZERO"),(71,"setDeltaMovement"),
                        (87,"setPos"),(97,"duration"),(105,"setFading")):
            self.assertIn(sym,a[off]["symbol"])
        self.assertEqual(a[22]["opcode"],"fmul")
        self.assertEqual(a[40]["operand"],"40")
        self.assertEqual(a[46]["opcode"],"iconst_5")
        self.assertEqual((a[49]["opcode"],a[49]["operand"]),("if_icmpge","103"))
        self.assertNotIn("ACCompat.hurt",str(a))
    def test_tick_nbt_and_owner_distinct(self):
        s,d=self.contracts();a=self.anchors(d,SPIRIT,"tick")
        self.assertIn("move",a[243]["symbol"])
        self.assertIn("0.8999999761581421d",a[251]["symbol"])
        self.assertIn("tickSubterranodon",a[306]["symbol"])
        self.assertIn("discard",a[195]["symbol"])
        data=self.anchors(d,SPIRIT,"defineSynchedData")
        self.assertIn("ENCHANTMENT_LEVEL",data[72]["symbol"])
        self.assertEqual(data[75]["opcode"],"iconst_0")
        for n in ("addAdditionalSaveData","readAdditionalSaveData"):
            rows=self.anchors(d,SPIRIT,n)
            self.assertFalse(any("ENCHANTMENT_LEVEL" in row["symbol"] or
                                 "ATTACKING_ENTITY_ID" in row["symbol"] for row in rows.values()))
        self.assertIn("UsingPlayerUUID",self.anchors(d,SPIRIT,"addAdditionalSaveData")[10]["symbol"])
    def test_certification_and_index_scopes(self):
        s,d=self.contracts()
        ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cert=ledger["objects"][P.name+"/"+CARD]
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),{"identity","behavior","parameters","targeting","costs","integration","validation"})
        self.assertEqual({v["path"] for v in cert["evidence"].values()},{str((P/CARD).relative_to(ROOT))})
        cross=(P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        cards=[path for path in (P/"enchantments").glob("*.md")
               if path.name not in ("INDEX.md","README.md")]
        certified=[key for key in ledger["objects"]
                   if key.startswith(P.name+"/enchantments/")]
        for value in (f"individual_full_enchantment_dossiers={len(certified)}/51",
                      f"individual_partial_enchantment_dossiers={len(cards)-len(certified)}/51",
                      f"individual_existing_enchantment_dossiers={len(cards)}/51",
                      "alexscaves:plummeting_flight"):
            self.assertIn(value,cross)
if __name__=="__main__":unittest.main()
