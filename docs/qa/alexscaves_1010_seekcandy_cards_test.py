#!/usr/bin/env python3
"""Seekcandy 1.0.10: individual exact static evidence and semantic regressions.

No gameplay mutation, accepted damage, provider closure or physical QA implied.
"""
from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
MANIFEST=BASE/"EXACT-SEEKCANDY-STATIC-1.0.10.json"
CARD=BASE/"enchantments/seekcandy.md"
PARENT=BASE/"EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json"
LEDGER=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
ENTRY="✅-alexs-caves-continued/enchantments/seekcandy.md"
ITEM="com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.class"
SELECTOR="com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.class"
PROJ="com/github/alexmodguy/alexscaves/server/entity/item/SpinningPeppermintEntity.class"

class SeekcandyStaticContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(MANIFEST.read_text(encoding="utf8"))
        cls.prior=json.loads(PARENT.read_text(encoding="utf8"))
        cls.card=CARD.read_text(encoding="utf8")
    def m(self,cls_name,method): return self.d["selected_methods"][cls_name][method]
    def piv(self,cls_name,method,offset,opcode=None,contains=None,operand=None):
        row=next((r for r in self.m(cls_name,method)["flow_pivots"]
                  if r["offset"]==offset),None)
        self.assertIsNotNone(row,"missing exact JVM pivot "+str(offset))
        if opcode is not None: self.assertEqual(row["opcode"],opcode)
        if contains is not None: self.assertIn(contains,row["symbol"]+" "+row["operand"])
        if operand is not None: self.assertEqual(row["operand"].strip(),str(operand))
        return row
    def test_resource_exact_config_and_provider_reference_universe(self):
        e=self.d["enchantment"]
        self.assertEqual(e["id"],"alexscaves:seekcandy")
        self.assertEqual(e["size_bytes"],361)
        self.assertEqual(e["sha256"],
                         "7e564925928b90368d9042f1b722f89464bfbd708abf69ced0d785b5871f0a74")
        self.assertEqual(e["json"]["supported_items"],"#alexscaves:enchantable/sugar_staff")
        self.assertEqual(e["json"]["max_level"],1)
        self.assertEqual(e["json"]["weight"],2)
        self.assertEqual(e["json"]["min_cost"],{"base":1,"per_level_above_first":16})
        self.assertEqual(e["json"]["max_cost"],{"base":41,"per_level_above_first":10})
        self.assertEqual(e["json"]["anvil_cost"],4)
        self.assertEqual(e["json"]["slots"],["mainhand"])
        self.assertNotIn("exclusive_set",e["json"])
        self.assertEqual(self.d["item_tag"]["json"],{"values":["alexscaves:sugar_staff"]})
        self.assertEqual(self.d["locale"]["translations"]["enchantment.alexscaves.seekcandy"],"Seekcandy")
        self.assertEqual(self.d["provider_class_census"]["scanned"],1555)
        self.assertEqual(self.d["provider_class_census"]["direct_seekcandy_class_hits"],[
            "com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class",ITEM])
        self.assertEqual(self.d["artifact"]["sha256"],self.prior["artifact_sha256"])
        for cls,digest in self.d["class_sha256"].items():
            self.assertEqual(digest,self.prior["classes"][cls]["sha256"])
    def test_exact_producer_target_condition_speed_cooldown_and_cost(self):
        self.assertEqual(self.m(ITEM,"use")["instruction_count"],226)
        self.assertEqual(self.m(ITEM,"use")["parsed_method_sha256"],
                         "76ba0a5bbf219e25f809c5e4d512fab3503f3e4dd99721e628787a7bde37d475")
        self.piv(ITEM,"use",8,contains="isClientSide")
        self.piv(ITEM,"use",30,contains="getClosestLookingAtEntityFor")
        self.piv(ITEM,"use",349,contains="SEEKCANDY")
        self.piv(ITEM,"use",352,contains="enchantLevel")
        self.piv(ITEM,"use",355,opcode="ifle",operand=379)
        self.piv(ITEM,"use",365,contains="setSeekingEntityId")
        self.piv(ITEM,"use",372,contains="setSpinSpeed")
        self.piv(ITEM,"use",375,opcode="bipush",operand=50)
        self.piv(ITEM,"use",418,contains="addFreshEntity")
        self.piv(ITEM,"use",421,opcode="pop")
        self.piv(ITEM,"use",461,contains="addCooldown")
        self.piv(ITEM,"use",468,contains="hurtAndBreakUsedHand")
    def test_selection_filters_mob_los_and_clip_reference(self):
        self.assertEqual(self.m(SELECTOR,"getClosestLookingAtEntityFor")["instruction_count"],119)
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",30,contains="Block.VISUAL")
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",33,contains="Fluid.NONE")
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",40,contains="Level.clip")
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",174,contains="getEntitiesOfClass")
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",238,opcode="ifeq")
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",247,opcode="ifeq")
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",259,contains="distanceToSqr")
        self.piv(SELECTOR,"getClosestLookingAtEntityFor",270,opcode="ifge")
    def test_projectile_tracking_steering_vs_straight_overwrites(self):
        self.assertEqual(self.m(PROJ,"tick")["instruction_count"],373)
        self.piv(PROJ,"tick",65,contains="setSpinRadius")
        self.piv(PROJ,"tick",71,contains="setSpinSpeed")
        self.piv(PROJ,"tick",358,contains="getSeekingEntityId")
        self.piv(PROJ,"tick",377,contains="Level.getEntity")
        self.piv(PROJ,"tick",435,contains="Math.min")
        self.piv(PROJ,"tick",440,contains="setSpinRadius")
        self.piv(PROJ,"tick",465,contains="isStraight")
        self.piv(PROJ,"tick",479,opcode="ifne")
        self.piv(PROJ,"tick",596,contains="move:")
        self.piv(PROJ,"tick",624,opcode="ifne")
        self.piv(PROJ,"tick",733,contains="spinAngle")
        self.piv(PROJ,"tick",737,contains="hurtEntities")
    def test_hit_acceptance_owner_culling_and_discard_not_per_target(self):
        self.assertEqual(self.m(PROJ,"hurtEntities")["instruction_count"],90)
        self.piv(PROJ,"hurtEntities",14,contains="mobProjectile")
        self.piv(PROJ,"hurtEntities",27,contains="getEntitiesOfClass")
        self.piv(PROJ,"hurtEntities",65,opcode="ifne")
        self.piv(PROJ,"hurtEntities",72,opcode="ifnull")
        self.piv(PROJ,"hurtEntities",137,opcode="ifne")
        self.piv(PROJ,"hurtEntities",143,contains="float 3.0f")
        self.piv(PROJ,"hurtEntities",145,contains="ACCompat.hurt")
        self.piv(PROJ,"hurtEntities",148,opcode="ifeq")
        self.piv(PROJ,"hurtEntities",178,contains="ACCompat.knockback")
        self.piv(PROJ,"hurtEntities",193,opcode="if_icmpeq")
        self.piv(PROJ,"hurtEntities",197,contains="discard")
        self.assertIn("qualquer hit aceito",self.card)
    def test_persistence_target_is_synched_but_not_in_native_nbt(self):
        self.piv(PROJ,"defineSynchedData",74,contains="SEEKING_ENTITY")
        self.piv(PROJ,"defineSynchedData",77,opcode="iconst_m1")
        self.piv(PROJ,"getSeekingEntityId",4,contains="SEEKING_ENTITY")
        self.piv(PROJ,"setSeekingEntityId",4,contains="SEEKING_ENTITY")
        own=self.prior["classes"][PROJ]["methods"]
        for mname in ("addAdditionalSaveData","readAdditionalSaveData"):
            method=next(x for x in own if x["name"]==mname)
            self.assertEqual(len(method["anchors"]),self.m(PROJ,mname)["instruction_count"])
            symbols=" ".join(x["symbol"] for x in method["anchors"])
            self.assertNotIn("SEEKING_ENTITY",symbols)
            self.assertNotIn("SeekingEntityId",symbols)
        self.piv(PROJ,"readAdditionalSaveData",117,contains="ACCompat.getDouble")
        read=next(x for x in own if x["name"]=="readAdditionalSaveData")
        self.assertIn("AroundZ",next(x for x in read["anchors"] if x["offset"]==114)["symbol"])
        self.piv(PROJ,"getOwner",35,contains="ServerLevel.getEntity")
        self.assertIn("NO_MUTATION",self.card)
    def test_certificate_claims_all_seven_axes_without_runtime_promotion(self):
        d=self.d
        self.assertEqual(d["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(d["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(d["limits"]["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(d["limits"]["physical_qa"],"NOT_TESTED")
        certs=json.loads(LEDGER.read_text(encoding="utf8"))
        entry=certs["objects"][ENTRY]
        self.assertEqual(entry["status"],"COMPLETE_PERK_READY")
        self.assertEqual(entry["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(entry["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(entry["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(entry["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(entry["evidence"]),{"identity","behavior","parameters",
                                                "targeting","costs","integration","validation"})
        self.assertIn("| ✅ | `alexscaves:seekcandy`",
                      (BASE/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(encoding="utf8"))
if __name__=="__main__": unittest.main()
