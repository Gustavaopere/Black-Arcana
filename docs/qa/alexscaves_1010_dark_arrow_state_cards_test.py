#!/usr/bin/env python3
"""Verify Dark Arrow's 1.0.10 static state evidence without certifying runtime."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
DOC=DIR/"dark-arrow.md"
SNAP=DIR/"EXACT-DARK-ARROW-STATE-1.0.10.json"

class DarkArrowCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SNAP.read_text(encoding="utf-8"))
        cls.index={c["class"].split("/")[-1]:c for c in cls.d["selected_classes"]}
        cls.card=DOC.read_text(encoding="utf-8")
    def test_exact_version_and_limits(self):
        self.assertEqual(self.d["scope"],"EXACT_ALEXSCAVES_1010_DARK_ARROW_SYMBOLIC_STATE_FLOW_ONLY")
        self.assertEqual(self.d["candidate_classes"],5)
        self.assertEqual(len(self.d["selected_classes"]),4)
        self.assertEqual(self.d["total_symbolic_anchors"],28)
        self.assertFalse(self.d["limits"]["complete_perk_ready"])
        self.assertFalse(self.d["limits"]["provider_universe_closed"])
        self.assertEqual(self.d["limits"]["mutating_hook"],"NOT_VERIFIED")
    def methods(self,klass):
        return {m["method_header"].split("(")[0].split()[-1]:m for m in self.index[klass]["methods"]}
    def test_exact_setters_and_defaults(self):
        m=self.methods("DarkArrowEntity.class")
        for name,descriptor in (
            ("setShadowArrowDamage","(F)V"),("setPerfectShot","(Z)V"),
            ("getShadowArrowDamage","()F"),("isPerfectShot","()Z")):
            self.assertEqual(m[name]["descriptor"],descriptor)
            self.assertIn(name,self.card)
        self.assertTrue(any("float" in a["symbol"] or "SHADOW_ARROW_DAMAGE" in a["symbol"]
                            for a in m["defineSynchedData"]["anchors"]))
        self.assertTrue(any(x["opcode"]=="fconst_0"
                            for a in m["defineSynchedData"]["anchors"] for x in a["nearby"]))
        self.assertTrue(any(x["opcode"]=="iconst_0"
                            for a in m["defineSynchedData"]["anchors"] for x in a["nearby"]))
        for name in ("setShadowArrowDamage","setPerfectShot"):
            self.assertTrue(any("SynchedEntityData.set" in a["symbol"]
                                for a in m[name]["anchors"]))
    def test_dreadbow_direct_callsite_offsets(self):
        m=self.methods("DreadbowItem.class")
        release={a["offset"]:a["symbol"] for a in m["releaseUsing"]["anchors"]}
        tick={a["offset"]:a["symbol"] for a in m["onUseTick"]["anchors"]}
        self.assertIn("setShadowArrowDamage",release[402])
        self.assertIn("setPerfectShot",release[409])
        self.assertIn("setShadowArrowDamage",tick[196])
        self.assertTrue(any(x["symbol"]=="float 3.0f"
                            for a in m["releaseUsing"]["anchors"] for x in a["nearby"]))
        self.assertTrue(any(x["opcode"]=="fconst_2"
                            for a in m["onUseTick"]["anchors"] for x in a["nearby"]))
    def test_card_provenance_and_fail_closed(self):
        self.assertIn(self.index["DreadbowItem.class"]["sha256"],self.card)
        self.assertIn(self.index["DarkArrowEntity.class"]["sha256"],self.card)
        for tok in ("NOT_CERTIFIED","NOT_VERIFIED","NOT_TESTED","NO_MUTATION"):
            self.assertIn(tok,self.card)
        self.assertEqual(self.d["limits"]["runtime_writers"],"NOT_CERTIFIED")
if __name__=="__main__":
    unittest.main()
