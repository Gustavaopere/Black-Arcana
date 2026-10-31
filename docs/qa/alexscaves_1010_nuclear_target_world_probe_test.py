#!/usr/bin/env python3
"""Regression tests for fail-closed NuclearExplosion target/world evidence."""
import json
import unittest
from pathlib import Path

from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_nuclear_target_world_probe import (
    HIGHLIGHTS, TICK_COUNT, TICK_SHA, compact, digest, scan_method, seal, window,
)


def instruction(at, opcode="fconst_0", symbol=""):
    return {"offset":at, "opcode":opcode, "operand":"", "symbol":symbol}


def method(*ins, name="tick"):
    return {"header":"public void "+name+"()", "descriptor":"()V", "instructions":list(ins)}


class NuclearWorldContractTests(unittest.TestCase):
    def test_selected_offset_is_bytecode_exact(self):
        selected=window(method(instruction(0),instruction(5),instruction(10)),5)
        self.assertEqual(selected["at"],5)
        self.assertEqual([x["offset"] for x in selected["ins"]],[0,5,10])

    def test_missing_offset_fails_closed(self):
        with self.assertRaisesRegex(GumballStateProbeError,"missing/duplicate"):
            window(method(instruction(0)),4)

    def test_duplicate_offset_fails_closed(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate target/world"):
            scan_method(method(instruction(1),instruction(1)))

    def test_critical_branch_and_field_collection(self):
        m=scan_method(method(
            instruction(0,"getstatic","Field Registry.NO_GRIEFING:Z"),
            instruction(2,"ifeq"),
            instruction(7,"ldc","float 1.0f"),
            instruction(9,"invokevirtual","Method Level.getBlockState:()V"), name="synthetic"))
        self.assertEqual([x["offset"] for x in m["references"]],[0,7,9])
        self.assertEqual([x["offset"] for x in m["branches"]],[2])
        self.assertEqual([x["offset"] for x in m["constants"]],[7])

    def test_excess_tick_method_budget(self):
        long_method=method(*[instruction(i) for i in range(451)])
        with self.assertRaisesRegex(GumballStateProbeError,"budget"):
            scan_method(long_method)

    def test_prior_sha_and_instruction_count_pinned(self):
        self.assertEqual(TICK_COUNT,348)
        self.assertEqual(TICK_SHA,"64f9a412c81a25525edf5b9576d56cec8354f6963ef718a44e6179347fcd8a25")
        self.assertLessEqual(len(HIGHLIGHTS),25)
        self.assertEqual(len(set(HIGHLIGHTS)),len(HIGHLIGHTS))

    def test_seal_strips_context_windows(self):
        doc={
            "schema_version":1,"scope":"SYNTHETIC","artifact":{},
            "class_path":"path","class_sha256":"sha",
            "declared_method_count":1,"selected_methods":{
                "tick:()V":{"instruction_count":1,"parsed_method_sha256":"abc",
                    "references":[],"branches":[],"constants":[],
                    "windows":[{"at":7,"ins":[compact(instruction(6)),compact(instruction(7)),
                                             compact(instruction(8))]}]}
            },"limitations":{"physical_qa":"NOT_TESTED"}
        }
        result=seal(doc)
        self.assertEqual([x["offset"] for x in
                         result["selected_methods"]["tick:()V"]["windows"][0]["ins"]],[7])

    def test_snapshot_duplicate_key_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"offset":1,"offset":3}',object_pairs_hook=strict_pairs)


class PublisherTargetWorldSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        snap=(Path(__file__).resolve().parents[2] /
              "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NUCLEAR-TARGET-WORLD-1.0.10.json")
        cls.doc=json.loads(snap.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
        cls.methods=cls.doc["selected_methods"]

    def test_artifact_identity_scope_and_nonpromotion(self):
        self.assertEqual(self.doc["artifact"]["sha256"],
                         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(self.doc["class_sha256"],
                         "d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912")
        self.assertEqual(self.doc["declared_method_count"],19)
        self.assertFalse(self.doc["limitations"]["complete_perk_ready"])
        self.assertEqual(self.doc["limitations"]["safe_mutating_hook"],"NOT_VERIFIED")

    def test_snapshot_selected_method_roster(self):
        exp={"tick:()V":348,"removeChunk:(I)V":269,"loadChunksAround:(Z)V":53,
             "getChunksAffected:()I":6,"getSize:()F":7,"isNoGriefing:()Z":7,
             "isDestroyable:(Lnet/minecraft/world/level/block/state/BlockState;)Z":25}
        self.assertEqual({k:x["instruction_count"] for k,x in self.methods.items()},exp)
        self.assertEqual(self.methods["tick:()V"]["parsed_method_sha256"],TICK_SHA)

    def test_tick_server_and_griefing_guards(self):
        m=self.methods["tick:()V"]
        refs={x["offset"]:x["symbol"] for x in m["references"]}
        br={x["offset"]:(x["opcode"],x["operand"]) for x in m["branches"]}
        self.assertIn("isClientSide",refs[177])
        self.assertEqual(br[180],("ifne","361"))
        self.assertIn("isNoGriefing",refs[184])
        self.assertEqual(br[187],("ifne","361"))
        self.assertIn("loadChunksAround",refs[211])
        self.assertIn("removeChunk",refs[352])
        self.assertIn("Math.min",refs[337])
        self.assertEqual(br[347],("if_icmpge","361"))

    def test_target_radius_and_native_filters_are_not_spell_range(self):
        m=self.methods["tick:()V"]
        refs={x["offset"]:x["symbol"] for x in m["references"]}
        self.assertIn("AABB.inflate",refs[389])
        self.assertIn("getEntitiesOfClass",refs[421])
        self.assertIn("calculateDamage",refs[466])
        self.assertIn("RaycatEntity",refs[525])
        self.assertIn("RESISTS_RADIATION",refs[545])
        self.assertIn("TremorzillaEntity",refs[570])
        self.assertIn("LivingEntity.hurt",refs[623])
        self.assertIn("IRRADIATED",refs[659])
        self.assertIn("LivingEntity.addEffect",refs[698])

    def test_block_limit_helper_and_special_egg_exception(self):
        m=self.methods["isDestroyable:(Lnet/minecraft/world/level/block/state/BlockState;)Z"]
        refs={x["offset"]:x["symbol"] for x in m["references"]}
        br={x["offset"]:(x["opcode"],x["operand"]) for x in m["branches"]}
        self.assertIn("NUKE_PROOF",refs[1])
        self.assertIn("nukeMaxBlockExplosionResistance",refs[20])
        self.assertIn("TREMORZILLA_EGG",refs[38])
        self.assertEqual(br[7],("ifne","37"))
        self.assertEqual(br[34],("iflt","55"))
        self.assertEqual(br[52],("ifeq","59"))

    def test_native_world_effects_and_force_chunk_not_whitewashed(self):
        rem=self.methods["removeChunk:(I)V"]["references"]
        sym={x["offset"]:x["symbol"] for x in rem}
        self.assertIn("ACPlatform.explosion",sym[105])
        self.assertIn("isDestroyable",sym[337])
        self.assertIn("spawnDinosaurs",sym[416])
        self.assertIn("nukesSpawnItemDrops",sym[425])
        self.assertIn("Level.destroyBlock",sym[472])
        self.assertIn("ACCompat.onBlockExploded",sym[490])
        self.assertIn("Level.setBlockAndUpdate",sym[545])
        load={x["offset"]:x["symbol"] for x in
              self.methods["loadChunksAround:(Z)V"]["references"]}
        self.assertIn("getChunksAffected",load[26])
        self.assertIn("getViewDistance",load[36])
        self.assertIn("ACPlatform.forceChunk",load[88])


if __name__=="__main__":
    unittest.main()
