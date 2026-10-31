#!/usr/bin/env python3
"""Synthetic fail-closed regression tests for exact NeoForge ticket contract."""
import hashlib
import json
import unittest
from pathlib import Path

from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_neoforge_ticket_contract_probe import (
    NEOFORGE_VERSION, NEO_CLASSES, evidence, mhash, seal,
)

def i(offset, symbol="", opcode="invokevirtual"):
    return {"offset":offset,"opcode":opcode,"operand":"#123","symbol":symbol}

def m(*ins):
    return {"header":"public void synthetic()","descriptor":"()V","instructions":list(ins)}

class NeoTicketSyntheticTests(unittest.TestCase):
    def test_expected_version_exact(self):
        self.assertEqual(NEOFORGE_VERSION,"21.1.248")
        self.assertIn("TicketController.class",NEO_CLASSES)
        self.assertIn("ForcedChunkManager.class",NEO_CLASSES)
        self.assertIn("ForcedChunkManager$TicketTracker.class",NEO_CLASSES)

    def test_bytecode_offset_duplication_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate JVM offset"):
            evidence(m(i(1),i(1)))

    def test_selected_boolean_argument_window(self):
        obj=evidence(m(i(0,"Method Other.a:()V"),i(1,"Method TicketController.forceChunk:()Z")))
        self.assertEqual(obj["total_cue_sites"],1)
        self.assertFalse(obj["anchors_truncated"])
        self.assertEqual(obj["anchors"][0]["at"],1)
        self.assertEqual([x["offset"] for x in obj["anchors"][0]["window"]],[0,1])

    def test_nonmatching_method_has_no_sites(self):
        obj=evidence(m(i(7,"Method java/lang/Math.max:(II)I")))
        self.assertEqual(obj["anchors"],[])

    def test_method_sha_changes_with_offset(self):
        self.assertNotEqual(mhash(m(i(1))),mhash(m(i(2))))

    def test_snapshot_key_duplicate_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"version":1,"version":2}',object_pairs_hook=strict_pairs)

    def test_seal_drops_context_without_dropping_anchor(self):
        x={"schema_version":1,"scope":"test","publisher":{},"neo":{},
           "provider_adapter_static_sha256":"x","provider_force_ticket_calls":[],
           "neoforge_class_count":1,"neoforge_classes":[{
                "class_path":"TicketController.class","class_sha256":"sha",
                "declared_method_count":1,"method_roster":[],
                "selected_methods":[{
                    "name":"forceChunk","descriptor":"()Z",
                    "instructions":4,"method_sha256":"m","total_cue_sites":1,
                    "anchors_truncated":False,
                    "anchors":[{"at":4,"instruction":i(4,"Method forceChunk:()Z"),
                                "window":[i(3),i(4),i(5)]}]
                }]
           }],"limits":{"allow_mutation":False}}
        s=seal(x)
        method=s["neoforge_classes"][0]["selected_methods"][0]
        self.assertEqual([v["offset"] for v in method["site_anchors"]],[4])
        self.assertNotIn("window",method)


class ExactNeoForgeTicketSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).resolve().parents[2] / (
            "wiki/modpack-catalog/providers/✅-alexs-caves-continued/"
            "EXACT-NEOFORGE-TICKETS-21.1.248.json")
        cls.doc=json.loads(path.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
        cls.classes={r["class_path"].rsplit("/",1)[-1]:r
                     for r in cls.doc["neoforge_classes"]}

    def selected(self,cls,name,descriptor=None):
        items=[m for m in self.classes[cls]["selected_methods"]
               if m["name"]==name and
               (descriptor is None or m["descriptor"]==descriptor)]
        self.assertEqual(len(items),1)
        return items[0]

    def sites(self,cls,name,descriptor=None):
        return {x["offset"]:x["symbol"] for x in
                self.selected(cls,name,descriptor)["site_anchors"]}

    def test_neo_exact_maven_artifact_and_limits(self):
        self.assertEqual(self.doc["neo"]["version"],"21.1.248")
        self.assertEqual(self.doc["neo"]["file_sha256"],
                         "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5")
        self.assertEqual(self.doc["neo"]["size_bytes"],3551268)
        self.assertEqual(self.doc["neoforge_class_count"],6)
        self.assertEqual(self.doc["publisher"]["sha256"],
                         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertFalse(self.doc["limits"]["allow_mutation"])
        self.assertEqual(self.doc["limits"]["physical_qa"],"NOT_TESTED")

    def test_entity_overload_maps_to_uuid_by_compiled_descriptor(self):
        desc="(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/Entity;IIZZ)Z"
        m=self.selected("TicketController.class","forceChunk",desc)
        self.assertEqual(m["instructions"],10)
        self.assertEqual(m["method_sha256"],
                         "0a785309c86c8d97e9788a25081adb25673aa28eda2f5e55783871d066f50783")
        x={v["offset"]:v["symbol"] for v in m["site_anchors"]}
        self.assertIn("Entity.getUUID",x[3])
        self.assertIn("Ljava/util/UUID;IIZZ)Z",x[13])

    def test_uuid_overload_delegates_to_forced_manager(self):
        desc="(Lnet/minecraft/server/level/ServerLevel;Ljava/util/UUID;IIZZ)Z"
        m=self.selected("TicketController.class","forceChunk",desc)
        x={v["offset"]:v["symbol"] for v in m["site_anchors"]}
        self.assertIn("ForcedChunkManager.forceChunk:",x[32])

    def test_forced_manager_persists_changed_tracker_and_calls_chunk_api(self):
        desc=("(Lnet/minecraft/server/level/ServerLevel;"
              "Lnet/minecraft/resources/ResourceLocation;Ljava/lang/Comparable;"
              "IIZZLnet/minecraft/server/level/TicketType;"
              "Ljava/util/function/Function;)Z")
        m=self.selected("ForcedChunkManager.class","forceChunk",desc)
        self.assertEqual(m["instructions"],74)
        self.assertEqual(m["method_sha256"],
                         "541b1e4e1988a40e14b9e479b0ce089ea3ec3db448d637c03b55a099cb7e9570")
        x={v["offset"]:v["symbol"] for v in m["site_anchors"]}
        self.assertIn("getDataStorage",x[30])
        self.assertIn("getChunk:",x[117])
        self.assertIn("setDirty:",x[145])
        self.assertIn("forceChunk:",x[159])
        subdesc=("(Lnet/minecraft/server/level/ServerLevel;"
                 "Lnet/minecraft/world/level/ChunkPos;"
                 "Lnet/minecraft/server/level/TicketType;"
                 "Lnet/neoforged/neoforge/common/world/chunk/ForcedChunkManager$TicketOwner;ZZ)V")
        sub=self.sites("ForcedChunkManager.class","forceChunk",subdesc)
        self.assertIn("addRegionTicket:",sub[15])
        self.assertIn("removeRegionTicket:",sub[31])

    def test_saved_tickets_have_reinstate_callback_path(self):
        desc=("(Lnet/minecraft/server/level/ServerLevel;"
              "Lnet/minecraft/world/level/ForcedChunksSavedData;)V")
        refs=self.sites("ForcedChunkManager.class","reinstatePersistentChunks",desc)
        self.assertIn("getEntityForcedChunks",refs[106])
        self.assertIn("reinstatePersistentChunks:",refs[113])
        m=self.sites("ForcedChunkManager.class","lambda$reinstatePersistentChunks$6")
        self.assertIn("TicketController.callback:",m[114])
        self.assertIn("TicketHelper",m[118])
        self.assertIn("validateTickets:",m[140])
        self.assertIn("removeAllTickets",self.sites(
            "TicketHelper.class","removeAllTickets",
            "(Ljava/util/UUID;)V")[9])

    def test_controller_registration_is_separate_from_provider_registration(self):
        regs=self.selected("RegisterTicketControllersEvent.class","register")
        self.assertEqual(regs["descriptor"],
                         "(Lnet/neoforged/neoforge/common/world/chunk/TicketController;)V")
        self.assertIn("RegisterTicketControllersEvent.class",self.classes)
        self.assertEqual(self.doc["limits"]["controller_registration_and_callback"],
                         "NOT_CLOSED")



    def test_compiled_provider_add_and_remove_pass_same_flag_twice(self):
        paths={r["class_path"].rsplit("/",1)[-1]:r for r in
               self.doc["publisher_boolean_paths"]}
        nuc={x["name"]:x for x in paths["NuclearExplosionEntity.class"]["selected_methods"]}
        def by_at(m):
            return {x["offset"]:(x["opcode"],x["operand"],x["symbol"])
                    for x in m["selected_stack"]}
        tick=by_at(nuc["tick"]);rem=by_at(nuc["remove"]);load=by_at(nuc["loadChunksAround"])
        self.assertEqual(tick[210][0],"iconst_1")
        self.assertIn("loadChunksAround",tick[211][2])
        self.assertEqual(rem[23][0],"iconst_0")
        self.assertIn("loadChunksAround",rem[24][2])
        self.assertEqual(load[86][0],"iload_1")
        self.assertEqual(load[87][0],"iload_1")
        self.assertIn("ACPlatform.forceChunk",load[88][2])
        ac=by_at(paths["ACPlatform.class"]["selected_methods"][0])
        self.assertEqual(ac[16][:2],("iload","4"))
        self.assertEqual(ac[18][:2],("iload","5"))
        self.assertIn("TicketController.forceChunk",ac[20][2])
        self.assertEqual(ac[23][0],"pop")

    def test_compiled_uuid_controller_switches_entity_ticket_type(self):
        desc="(Lnet/minecraft/server/level/ServerLevel;Ljava/util/UUID;IIZZ)Z"
        site=self.sites("TicketController.class","forceChunk",desc)
        self.assertIn("ENTITY_TICKING",site[18])
        self.assertIn("ForcedChunkManager.ENTITY:",site[24])
        self.assertIn("ForcedChunkManager.forceChunk",site[32])

    def test_ticket_tracker_has_distinct_ticking_and_plain_maps(self):
        cls="ForcedChunkManager$TicketTracker.class"
        selection=self.selected(cls,"getTickets","(Z)Ljava/util/Map;")
        self.assertEqual(selection["method_sha256"],
                         "92ded3124a30ce90720339d2fc879dfbfc08e33c376fdc03570122f750ba05a9")
        sites=self.sites(cls,"getTickets","(Z)Ljava/util/Map;")
        self.assertIn("tickingChunks",sites[5])
        self.assertIn("chunks:",sites[12])
        desc="(Lnet/neoforged/neoforge/common/world/chunk/ForcedChunkManager$TicketOwner;JZ)Z"
        add=self.selected(cls,"add",desc)
        rem=self.selected(cls,"remove",desc)
        self.assertEqual(add["method_sha256"],
                         "b08776a0342a948ebd1db8f13776aa9400277c2b34753002ddcade7b2396446d")
        self.assertEqual(rem["method_sha256"],
                         "3ed7002a78ed399d27f7b86764600b940a64312c10ad336899bc2f01bd013e25")
        self.assertIn("getTickets:",self.sites(cls,"add",desc)[3])
        self.assertIn("getTickets:",self.sites(cls,"remove",desc)[3])

    def test_static_ticket_bucket_mismatch_is_not_a_live_leak_claim(self):
        self.assertEqual(self.doc["native_release_ticket_bucket_mismatch"],
                         "CONFIRMED_SELECTED_STATIC_BRANCHES_NOT_LIVE_RUNTIME")
        self.assertEqual(self.doc["actual_persistent_ticket_leak"],"NOT_OBSERVED")
        self.assertEqual(self.doc["limits"]["restart_reinstate_validation"],"NOT_CLOSED")

if __name__=="__main__":
    unittest.main()
