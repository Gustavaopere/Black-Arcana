#!/usr/bin/env python3
"""Exact static Precise Volley causal and index regression."""
import hashlib,json,unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,validate_cards
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PRE="com/github/alexmodguy/alexscaves/"
BOW=PRE+"server/item/DreadbowItem.class"
ARROW=PRE+"server/entity/item/DarkArrowEntity.class"
CARD="enchantments/precise-volley.md"
class PreciseVolleyStatic(unittest.TestCase):
    def contracts(self):
        s=json.loads((P/"EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
        m=load_manifest(P/"EXACT-DREADBOW-CONTRACTS-1.0.10.json")
        validate_structure(m,profile="dreadbow")
        validate_cards(m,P,profile="dreadbow")
        self.assertEqual(s["catalog_family"],"PRECISE_VOLLEY_ENCHANTMENT_CONTRACT")
        self.assertEqual(s["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(s["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(s["physical_qa"],"NOT_TESTED")
        self.assertEqual(s["mutation"],"NO_MUTATION")
        self.assertFalse(s["provider_universe_closed"])
        self.assertEqual(s["artifact"]["sha256"],m["artifact_sha256"])
        self.assertEqual(s["resource"]["sha256"],m["resources"]["data/alexscaves/enchantment/precise_volley.json"])
        self.assertEqual(hashlib.sha256((P/CARD).read_bytes()).hexdigest(),s["card"]["sha256"])
        return s,m
    def offsets(self,m,owner,method):
        found=[x for x in m["classes"][owner]["methods"] if x["name"]==method]
        self.assertEqual(len(found),1,(owner,method))
        return {x["offset"]:x for x in found[0]["anchors"]}
    def test_publisher_identity_level_cost_and_translation(self):
        s,m=self.contracts()
        j=s["resource"]["json"]
        self.assertEqual(j["description"]["translate"],"enchantment.alexscaves.precise_volley")
        self.assertEqual(j["supported_items"],"#alexscaves:enchantable/dreadbow")
        self.assertEqual((j["weight"],j["max_level"],j["anvil_cost"],j["slots"]),(2,1,4,["mainhand"]))
        self.assertEqual(j["min_cost"],{"base":1,"per_level_above_first":18})
        self.assertEqual(j["max_cost"],{"base":41,"per_level_above_first":10})
        self.assertEqual(s["item_tag"]["json"],{"values":["alexscaves:dreadbow"]})
        self.assertIn("more central position",s["english_translations"]["enchantment.alexscaves.precise_volley.desc"])
    def test_anchor_hashes_and_offsets_parent_exact(self):
        s,m=self.contracts()
        self.assertGreaterEqual(len(s["anchors"]),145)
        self.assertEqual(len(s["anchors"]),s["limits"]["sealed_pivots"])
        self.assertTrue(set(a["class"] for a in s["anchors"])<=set(s["class_hashes"]))
        for cl,sha in s["class_hashes"].items():
            self.assertEqual(sha,m["classes"][cl]["sha256"])
        seen=set()
        for a in s["anchors"]:
            key=(a["class"],a["method"],a["descriptor"],a["offset"])
            self.assertNotIn(key,seen)
            seen.add(key)
            z=self.offsets(m,a["class"],a["method"])[a["offset"]]
            self.assertEqual({k:a[k] for k in ("offset","opcode","operand","symbol")},
                             {k:z[k] for k in ("offset","opcode","operand","symbol")})
    def test_boolean_precise_release_only_and_damage_requests(self):
        s,m=self.contracts()
        a=self.offsets(m,BOW,"releaseUsing")
        self.assertIn("RELENTLESS_DARKNESS",a[14]["symbol"])
        self.assertEqual((a[20]["opcode"],a[20]["operand"]),("ifgt","899"))
        self.assertIn("PRECISE_VOLLEY",a[43]["symbol"])
        self.assertIn("enchantLevel",a[46]["symbol"])
        self.assertEqual((a[49]["opcode"],a[49]["operand"]),("ifle","56"))
        self.assertEqual(a[52]["opcode"],"iconst_1")
        self.assertEqual(a[56]["opcode"],"iconst_0")
        self.assertIn("setShadowArrowDamage",a[402]["symbol"])
        self.assertEqual(a[395]["opcode"],"fconst_2")
        self.assertIn("3.0f",a[399]["symbol"])
        self.assertIn("setPerfectShot",a[409]["symbol"])
        self.assertEqual((a[665]["opcode"],a[665]["operand"]),("ifeq","672"))
        self.assertEqual(a[668]["opcode"],"fconst_0")
        self.assertIn("shoot",a[769]["symbol"])
        self.assertIn("addFreshEntity",a[775]["symbol"])
        self.assertIn("hurtAndBreakUsedHand",a[874]["symbol"])
        t=self.offsets(m,BOW,"onUseTick")
        self.assertIn("RELENTLESS_DARKNESS",t[23]["symbol"])
        self.assertIn("setShadowArrowDamage",t[196]["symbol"])
        self.assertFalse(any("PRECISE_VOLLEY" in x["symbol"] for x in t.values()))
    def test_volley_count_raycast_and_perfect_damage_are_separate(self):
        s,m=self.contracts()
        b=self.offsets(m,BOW,"releaseUsing")
        for off,val in ((185,"128.0f"),(228,"42.0f"),(335,"30"),(340,"8"),
                        (365,"Math.ceil"),(751,"0.5f"),(753,"1.5f")):
            self.assertIn(val,b[off]["symbol"]+" "+b[off]["operand"])
        d=self.offsets(m,ARROW,"onHitEntity")
        self.assertIn("getShadowArrowDamage",d[11]["symbol"])
        self.assertIn("isPerfectShot",d[17]["symbol"])
        self.assertEqual(d[25]["opcode"],"fconst_2")
        self.assertIn("causeDarkArrowDamage",d[37]["symbol"])
        self.assertIn("ACCompat.hurt",d[82]["symbol"])
        self.assertEqual((d[85]["opcode"],d[85]["operand"]),("ifeq","93"))
        self.assertIn("startFading",d[90]["symbol"])
        for at in (51,59,67,74):self.assertEqual(d[at]["operand"],"93")
    def test_ledger_and_alphabetical_counters(self):
        s,m=self.contracts()
        ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cert=ledger["objects"][P.name+"/"+CARD]
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),{"identity","behavior","parameters","targeting","costs","integration","validation"})
        self.assertEqual({v["path"] for v in cert["evidence"].values()},
                         {str((P/CARD).relative_to(ROOT))})
        cross=(P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        cards=[p for p in (P/"enchantments").glob("*.md") if p.name not in ("INDEX.md","README.md")]
        done=[k for k in ledger["objects"] if k.startswith(P.name+"/enchantments/")]
        for expected in (f"individual_full_enchantment_dossiers={len(done)}/51",
                         f"individual_partial_enchantment_dossiers={len(cards)-len(done)}/51",
                         f"individual_existing_enchantment_dossiers={len(cards)}/51",
                         "| ✅ | `alexscaves:precise_volley`"):
            self.assertIn(expected,cross)
if __name__=="__main__":unittest.main()
