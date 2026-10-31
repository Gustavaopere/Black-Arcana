#!/usr/bin/env python3
"""Fail-closed synthetic regression tests for chunk-force ownership evidence."""
import json
import unittest

from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_nuclear_chunk_lifecycle_probe import (
    MAX_CANDIDATES, MAX_METHOD_INSNS, chosen_sites, method_sha, seal,
)


def instr(offset, symbol="", opcode="invokestatic"):
    return {"offset":offset,"opcode":opcode,"operand":"#7","symbol":symbol}


def method(*ins):
    return {"header":"public void sample()","descriptor":"()V","instructions":list(ins)}


class NuclearChunkLifecycleTests(unittest.TestCase):
    def test_exact_force_and_unforce_callsite_windows(self):
        m=method(instr(0,"Method ACPlatform.forceChunk:(...)V"),instr(3),
                 instr(6,"Method ACPlatform.forceChunk:(...)V"))
        sites=chosen_sites(m)
        self.assertEqual([x["at"] for x in sites],[0,6])
        self.assertEqual([x["offset"] for x in sites[0]["window"]],[0,3,6])

    def test_absence_of_symbol_does_not_invent_callsites(self):
        self.assertEqual(chosen_sites(method(instr(0,"Method Other.doSomething:()V"))),[])

    def test_duplicate_instruction_offset_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate chunk-lifecycle offset"):
            chosen_sites(method(instr(0),instr(0)))

    def test_bounded_method_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"instruction budget"):
            chosen_sites(method(*[instr(i) for i in range(MAX_METHOD_INSNS+1)]))

    def test_static_digest_identity_sensitive(self):
        a=method(instr(2,"Method ACPlatform.forceChunk:(...)V"))
        b=method(instr(3,"Method ACPlatform.forceChunk:(...)V"))
        self.assertNotEqual(method_sha(a),method_sha(b))

    def test_snapshot_projection_strips_context_not_anchor(self):
        doc={
            "schema_version":1,"scope":"unit","artifact":{},
            "nuclear_class_path":"a","nuclear_class_sha256":"sha",
            "nuclear_declared_method_roster":[],"candidate_class_count":1,
            "candidate_classes":[{
                "class_path":"a","class_sha256":"sha","method_count":1,
                "relevant_methods":[{
                    "name":"tick","descriptor":"()V","header":"void tick()",
                    "instruction_count":1,"parsed_method_sha256":"digest",
                    "sites":[{"at":7,"anchor":instr(7,"Method ACPlatform.forceChunk:(...)V"),
                              "window":[instr(5),instr(7)]}]
                }]
            }],
            "limitations":{"force_chunk_release_at_every_lifecycle_exit":"NOT_PROVEN"}
        }
        sealed=seal(doc)
        selected=sealed["candidate_classes"][0]["relevant_methods"][0]
        self.assertEqual(selected["site_anchors"][0]["offset"],7)
        self.assertNotIn("window",selected)
        self.assertLess(MAX_CANDIDATES,100)

    def test_duplicate_snapshot_keys_fail(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"scope":1,"scope":2}',object_pairs_hook=strict_pairs)


class ExactNuclearLifecycleSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pathlib import Path
        snap=Path(__file__).resolve().parents[2] / (
            "wiki/modpack-catalog/providers/✅-alexs-caves-continued/"
            "EXACT-NUCLEAR-CHUNK-LIFECYCLE-1.0.10.json")
        cls.data=json.loads(snap.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
        cls.classes={x["class_path"].rsplit("/",1)[-1]:x
                     for x in cls.data["candidate_classes"]}

    def method(self,cls,method_name,descriptor=None):
        ms=[m for m in self.classes[cls]["relevant_methods"]
            if m["name"]==method_name and
            (descriptor is None or m["descriptor"]==descriptor)]
        self.assertEqual(len(ms),1)
        return ms[0]

    def at(self,cls,name,descriptor=None):
        m=self.method(cls,name,descriptor)
        return {x["offset"]:x for x in m["site_anchors"]}

    def test_exact_artifact_and_candidate_scope(self):
        self.assertEqual(self.data["artifact"]["sha1"],
                         "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570")
        self.assertEqual(self.data["artifact"]["sha256"],
                         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(self.data["candidate_class_count"],5)
        self.assertEqual(len(self.data["nuclear_declared_method_roster"]),19)
        self.assertFalse(self.data["limitations"]["perk_ready"])

    def test_nuclear_remove_override_native_cleanup(self):
        names={x["name"]:x for x in self.data["nuclear_declared_method_roster"]}
        self.assertIn("remove",names)
        self.assertEqual(names["remove"]["descriptor"],
                         "(Lnet/minecraft/world/entity/Entity$RemovalReason;)V")
        self.assertEqual(names["remove"]["instruction_count"],17)
        self.assertEqual(names["remove"]["parsed_method_sha256"],
                         "8eb89c85d5125decad3a9975e1d0b453e9911f59f4fd8f2f36f40b15d96d5854")
        sites=self.at("NuclearExplosionEntity.class","remove")
        self.assertIn("loadingChunks:Z",sites[11]["symbol"])
        self.assertIn("loadingChunks:Z",sites[19]["symbol"])
        self.assertIn("loadChunksAround:(Z)V",sites[24]["symbol"])
        self.assertIn("Entity.remove:",sites[29]["symbol"])

    def test_tick_acquire_and_remove_release_bind_same_helper(self):
        tick=self.at("NuclearExplosionEntity.class","tick")
        self.assertIn("loadChunksAround:(Z)V",tick[211]["symbol"])
        self.assertIn("loadingChunks:Z",tick[206]["symbol"])
        remove=self.at("NuclearExplosionEntity.class","remove")
        self.assertEqual(remove[24]["symbol"],tick[211]["symbol"])

    def test_force_chunk_route_is_neoforge_ticket_controller(self):
        loader=self.at("NuclearExplosionEntity.class","loadChunksAround")
        self.assertIn("ACPlatform.forceChunk:",loader[88]["symbol"])
        platform=self.classes["ACPlatform.class"]["relevant_methods"]
        self.assertEqual(len([x for x in platform if x["name"]=="forceChunk"]),2)
        bydesc={x["descriptor"]:x for x in platform if x["name"]=="forceChunk"}
        entity="(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/Entity;IIZZ)V"
        self.assertIn(entity,bydesc)
        refs={x["offset"]:x["symbol"] for x in bydesc[entity]["site_anchors"]}
        self.assertIn("TicketController.forceChunk:",refs[20])
        self.assertIn(")Z",refs[20])

    def test_nbt_restores_flag_not_evidence_of_ticket_reconstruction(self):
        write=self.at("NuclearExplosionEntity.class","addAdditionalSaveData")
        read=self.at("NuclearExplosionEntity.class","readAdditionalSaveData")
        self.assertIn("WasLoadingChunks",write[1]["symbol"])
        self.assertIn("WasLoadingChunks",read[2]["symbol"])
        self.assertIn("loadingChunks",read[8]["symbol"])

    def test_other_force_chunk_callers_not_conflated_with_nuclear(self):
        self.assertIn("BeholderEyeEntity.class",self.classes)
        self.assertIn("OccultGemItem.class",self.classes)
        self.assertIn("RemoteDetonatorItem.class",self.classes)
        entity=self.at("NuclearExplosionEntity.class","loadChunksAround")
        self.assertIn("Entity;",entity[88]["symbol"])
        for cls in ("OccultGemItem.class","RemoteDetonatorItem.class"):
            self.assertIn("UUID",self.at(cls,"loadChunksAround")[44]["symbol"])


if __name__ == "__main__":
    unittest.main()
