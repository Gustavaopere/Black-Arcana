#!/usr/bin/env python3
"""Regression checks for the bounded exact-JAR dynamic attribute discovery JSON.

These tests prove selected native call/branch anchors, not runtime hooks,
attribute application, player isolation or a complete seven-axis certificate.
"""
import json
import os
from pathlib import Path
import unittest

PREFIX="com/github/alexmodguy/alexscaves/"
ITEM=PREFIX+"server/item/"
HELPER=PREFIX+"server/misc/ACCompat"
NAMES={
    "DivingArmorItem","GingerbreadArmorItem","OrtholanceItem",
    "PrimitiveClubItem","SharpenedCandyCaneItem","SpearItem",
    "TotemOfPossessionItem",
}


class ExactNativeDiscovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=os.environ.get("AC_DYNAMIC_ATTRIBUTE_REPORT")
        if not path:
            raise RuntimeError("set AC_DYNAMIC_ATTRIBUTE_REPORT for exact-JAR tests")
        cls.doc=json.loads(Path(path).read_text(encoding="utf8"))
        cls.methods=cls.doc["native_methods"]

    def method(self,owner,name,desc=None):
        found=[m for m in self.methods[owner] if m["name"]==name
               and (desc is None or desc==m["descriptor"])]
        self.assertEqual(len(found),1, (owner,name,desc))
        return {row["offset"]:row for row in found[0]["instructions"]}

    def pivot(self,rows,offset,opcode,token=""):
        self.assertIn(offset,rows)
        self.assertEqual(rows[offset]["opcode"],opcode)
        self.assertIn(token,rows[offset]["symbol"]+" "+rows[offset]["operand"])

    def test_artifact_and_static_limit(self):
        d=self.doc
        self.assertEqual(d["artifact"]["sha256"],
            "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(d["artifact"]["size_bytes"],75279314)
        self.assertEqual(d["class_entries_scanned"],1555)
        self.assertEqual(d["scope"],"SHA_EXACT_DISCOVERY_ONLY_NOT_CERTIFIED")
        self.assertEqual(d["mutation"],"NO_MUTATION")
        self.assertEqual(d["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(d["physical_qa"],"NOT_TESTED")
        self.assertFalse(d["provider_universe_closed"])

    def test_abstract_contract_and_exact_owner_roster(self):
        d=self.doc
        target=ITEM+"ACDynamicAttributeItem"
        self.assertEqual(d["target"],target)
        self.assertEqual(set(d["direct_implementers"]),{ITEM+n for n in NAMES})
        self.assertEqual(set(d["inherited_implementers"]),
            {ITEM+n for n in ("ExtinctionSpearItem","FrostmintSpearItem","LimestoneSpearItem")})
        decl={row["owner"]:row["methods"] for row in d["callback_declarations"]}
        self.assertEqual(set(decl),{target,*d["direct_implementers"]})
        self.assertEqual(decl[target][0]["access"],1025)
        self.assertIsNone(decl[target][0]["code_sha256"])
        for owner in d["direct_implementers"]:
            self.assertEqual(decl[owner][0]["access"],1)
            self.assertIsNotNone(decl[owner][0]["code_sha256"])
            self.assertEqual(len(decl[owner][0]["exception_handlers"]),0)
        self.assertEqual({r["caller"] for r in d["callback_typed_member_references"]},
            set(d["direct_implementers"]))

    def test_seven_callbacks_and_wrappers_route_to_helper(self):
        for owner in self.doc["direct_implementers"]:
            self.method(owner,"acModifiers")
            wrapper=self.method(owner,"getDefaultAttributeModifiers")
            self.assertEqual(len(wrapper),8)
            self.pivot(wrapper,14,"invokestatic","ACCompat.itemAttributes:")

    def test_armors_return_empty_instead_of_null_for_wrong_slot(self):
        for owner, branch in ((ITEM+"DivingArmorItem",18),
                              (ITEM+"GingerbreadArmorItem",26)):
            m=self.method(owner,"acModifiers")
            self.pivot(m,8,"if_acmpne",str(branch))
            self.pivot(m,branch,"invokestatic","ImmutableMultimap.of:")

    def test_weapons_decline_non_mainhand_slots_with_null(self):
        for name in ("OrtholanceItem","SharpenedCandyCaneItem",
                     "SpearItem","TotemOfPossessionItem"):
            m=self.method(ITEM+name,"acModifiers")
            self.pivot(m,1,"getstatic","EquipmentSlot.MAINHAND")
            self.pivot(m,4,"if_acmpne","14")
            self.pivot(m,14,"aconst_null")
        club=self.method(ITEM+"PrimitiveClubItem","acModifiers")
        self.pivot(club,4,"if_acmpeq","9")
        self.pivot(club,7,"aconst_null")

    def test_gingerbread_cache_and_unclamped_ratio(self):
        m=self.method(ITEM+"GingerbreadArmorItem","getOrCreateDurabilityAttributes")
        self.assertEqual(len(m),73)
        for offset,opcode,token in (
            (8,"invokeinterface","Map.containsKey:"),
            (24,"invokeinterface","Map.get:"),
            (37,"fdiv",""),
            (39,"ldc2_w","double 0.1d"),
            (42,"ldc2_w","double 0.9d"),
            (85,"getstatic","Attributes.ARMOR"),
            (95,"getfield","acDefense:I"),
            (111,"getstatic","Attributes.MOVEMENT_SPEED"),
            (122,"getstatic","ADD_MULTIPLIED_BASE"),
            (149,"invokeinterface","Map.put:"),
        ):
            self.pivot(m,offset,opcode,token)
        self.assertFalse(any(row["opcode"].startswith("if") for offset,row in m.items()
            if offset>=33 and offset<=48), "ratio computation contains an unreviewed guard")

    def test_swiftwood_consumer_is_bounded_to_four_cached_levels(self):
        m=self.method(ITEM+"PrimitiveClubItem","acModifiers")
        self.pivot(m,10,"getstatic","SWIFTWOOD")
        self.pivot(m,13,"invokestatic","ACCompat.enchantLevel")
        self.pivot(m,22,"iconst_0")
        self.pivot(m,23,"iconst_3")
        self.pivot(m,24,"invokestatic","Mth.clamp")
        self.pivot(m,27,"aaload")

    def test_helper_null_vs_empty_semantics_and_fallback(self):
        methods=self.methods[HELPER]
        self.assertEqual(sum(m["name"]=="itemAttributes" for m in methods),2)
        single=self.method(HELPER,"itemAttributes",
            "(Lcom/google/common/collect/Multimap;Lnet/minecraft/world/entity/EquipmentSlot;Ljava/util/function/Supplier;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;")
        self.assertEqual(len(single),19)
        self.pivot(single,1,"ifnonnull","14")
        self.pivot(single,5,"invokeinterface","Supplier.get:")
        self.pivot(single,33,"invokeinterface","Multimap.forEach:")
        whole=self.method(HELPER,"itemAttributes",
            "(Ljava/util/function/BiFunction;Lnet/minecraft/world/item/ItemStack;Ljava/util/function/Supplier;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;")
        self.assertEqual(len(whole),48)
        for offset,opcode,token in (
            (7,"invokestatic","EquipmentSlot.values:"),
            (24,"if_icmpge","87"),
            (38,"invokeinterface","BiFunction.apply:"),
            (50,"ifnonnull","56"),
            (56,"iconst_1",""),
            (76,"invokeinterface","Multimap.forEach:"),
            (89,"ifeq","99"),
            (93,"invokevirtual","Builder.build:"),
            (100,"invokeinterface","Supplier.get:"),
        ):
            self.pivot(whole,offset,opcode,token)


if __name__=="__main__":
    unittest.main()
