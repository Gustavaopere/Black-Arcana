#!/usr/bin/env python3
"""Seal the read-only attribute interface scope; never certify a live hook."""
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
EVENT="net/neoforged/neoforge/event/ItemAttributeModifierEvent"
BUILDER=EVENT+"$ItemAttributeModifiersBuilder"
KEY=BUILDER+"$Key"
ITEM="com/github/alexmodguy/alexscaves/server/item/"
AXES={"identity","behavior","parameters","targeting","costs","integration","validation"}

class BuilderContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((PROVIDER/"EXACT-DYNAMIC-ATTRIBUTE-CONTRACT-1.0.10.json").read_text())
        cls.report_raw=Path(os.environ["AC_ATTRIBUTE_BUILDER_REPORT"]).read_bytes()
        cls.doc=json.loads(cls.report_raw)
        cls.construction=json.loads(Path(os.environ["AC_ATTRIBUTE_CONSTRUCTION_REPORT"]).read_text())
        cls.engine=cls.doc["universal_event_classes"]
        cls.native=cls.doc["publisher_state_consumers"]

    def method(self,owner,name,source=None):
        pool=self.engine if source is None else source
        found=[m for m in pool[owner]["methods"] if m["name"]==name]
        self.assertEqual(len(found),1,(owner,name))
        return found[0]

    def pivot(self,m,offset,opcode,token=""):
        row=next((r for r in m["instructions"] if r["offset"]==offset),None)
        self.assertIsNotNone(row,(m["name"],offset))
        self.assertEqual(row["opcode"],opcode)
        self.assertIn(token,row["symbol"]+" "+row["operand"])

    def test_reproducible_seals_and_scope(self):
        self.assertEqual(hashlib.sha256(self.report_raw).hexdigest(),self.seal["reports"]["builder"]["sha256"])
        self.assertEqual(self.doc["construction_report_sha256_normalized_filename"],
                         self.seal["reports"]["construction"]["sha256"])
        self.assertEqual(set(self.seal["axes"]),AXES)
        c=self.seal["claims"]
        self.assertEqual(c["static_technical_contract"],"CERTIFIED_STATIC_7_AXES")
        for f,v in (("mutating_hook","NOT_VERIFIED"),("physical_qa","NOT_TESTED"),
                    ("perk_certification","NOT_CERTIFIED"),("runtime_dispatch","NOT_VERIFIED"),
                    ("mutation","NO_MUTATION"),("provider_universe_closed",False),
                    ("semantic_magic_roots_delta",0)):
            self.assertEqual(c[f],v)
        self.assertEqual(self.doc["scope"],"STATIC_REFERENCE_ONLY_NOT_CERTIFIED")
        self.assertEqual(set(self.engine),{EVENT,BUILDER,KEY})

    def test_builder_key_excludes_slot_operation_and_magnitude(self):
        k=self.engine[KEY]
        self.assertEqual(k["class_sha256"],self.seal["builder"]["key_class_sha256"])
        self.assertEqual([(f["name"],f["descriptor"]) for f in k["fields"]],
            [("attr","Lnet/minecraft/core/Holder;"),("id","Lnet/minecraft/resources/ResourceLocation;")])
        m=self.method(KEY,"<init>")
        self.pivot(m,1,"invokespecial",'java/lang/Record."<init>"')
        self.pivot(m,6,"putfield","Field attr:")
        self.pivot(m,11,"putfield","Field id:")
        self.assertFalse(self.seal["builder"]["key_includes_slot"])
        for name,off in (("equals",2),("hashCode",1)):
            self.pivot(self.method(KEY,name),off,"invokedynamic",name)

    def test_initial_list_and_key_map_have_distinct_semantics(self):
        m=self.method(BUILDER,"<init>")
        for off,op,tok in ((5,"new","LinkedList"),(16,"new","HashMap"),
                           (39,"invokeinterface","List.iterator"),(69,"invokeinterface","List.add"),
                           (84,"invokevirtual","Entry.attribute"),(91,"invokevirtual","AttributeModifier.id"),
                           (94,"invokespecial",'Key."<init>"'),(98,"invokeinterface","Map.put"),
                           (103,"pop",""),(104,"goto","45")):
            self.pivot(m,off,op,tok)
        self.assertTrue(self.seal["builder"]["initial_list_preserves_entries"])
        self.assertTrue(self.seal["builder"]["initial_map_put_overwrites_same_key"])

    def test_add_duplicate_key_is_refused_before_entry_creation(self):
        m=self.method(BUILDER,"addModifier")
        for off,op,tok in ((6,"invokevirtual","AttributeModifier.id"),(9,"invokespecial",'Key."<init>"'),
                           (20,"invokeinterface","Map.containsKey"),(25,"ifeq","30"),
                           (28,"iconst_0",""),(29,"ireturn",""),(36,"aload_3",""),
                           (37,"invokespecial",'Entry."<init>"'),(48,"invokeinterface","List.add"),
                           (62,"invokeinterface","Map.put"),(68,"iconst_1",""),(69,"ireturn","")):
            self.pivot(m,off,op,tok)

    def test_replace_and_remove_share_key_not_slot(self):
        m=self.method(BUILDER,"replaceModifier")
        for off,op,tok in ((9,"invokespecial",'Key."<init>"'),(20,"aload_3",""),
                           (21,"invokespecial",'Entry."<init>"'),(32,"invokeinterface","Map.containsKey"),
                           (37,"ifeq","121"),(62,"invokeinterface","List.indexOf"),(72,"if_icmpeq","92"),
                           (83,"invokeinterface","List.set"),(98,"invokeinterface","List.add"),
                           (112,"invokeinterface","Map.put"),(120,"areturn",""),
                           (127,"invokeinterface","List.add"),(141,"invokeinterface","Map.put"),
                           (147,"aconst_null","")):
            self.pivot(m,off,op,tok)
        m=self.method(BUILDER,"removeModifier")
        self.pivot(m,13,"invokeinterface","Map.remove")
        self.pivot(m,23,"ifnull","39")
        self.pivot(m,31,"invokeinterface","List.remove")
        self.assertTrue(self.seal["builder"]["replace_can_change_slot"])

    def test_builder_view_predicate_and_final_copy(self):
        m=self.method(BUILDER,"removeIf")
        self.pivot(m,5,"invokeinterface","List.removeIf")
        self.pivot(m,10,"pop")
        self.pivot(m,15,"invokeinterface","Map.values")
        self.pivot(m,21,"invokeinterface","Collection.removeIf")
        self.pivot(self.method(BUILDER,"getEntryView"),4,"invokestatic","Collections.unmodifiableList")
        m=self.method(BUILDER,"build")
        self.pivot(m,8,"invokestatic","ImmutableList.copyOf")
        self.pivot(m,12,"invokespecial",'ItemAttributeModifiers."<init>"')
        m=self.method(EVENT,"getBuilder")
        self.pivot(m,4,"ifnonnull","22")
        self.pivot(m,13,"getfield","defaultModifiers")
        self.pivot(m,19,"putfield","builder")
        self.pivot(self.method(EVENT,"getItemStack"),1,"getfield","stack:")

    def test_state_and_durability_identity_are_native_not_player_owned(self):
        g=self.native[ITEM+"GingerbreadArmorItem"]
        uses=[r for r in g["field_uses"] if "defaultAttributes:" in r["symbol"]]
        self.assertEqual([(r["method"],r["offset"],r["opcode"]) for r in uses],
                         [("<init>",125,"putfield")])
        m=g["selected_methods"][0]
        self.assertEqual(m["name"],"getOrCreateDurabilityAttributes")
        self.assertEqual(m["bootstrap_call_sites"][0]["bootstrap"]["arguments"],["gingerbread_armor.\u0001"])
        self.pivot(m,8,"invokeinterface","Map.containsKey")
        self.pivot(m,37,"fdiv")
        self.pivot(m,149,"invokeinterface","Map.put")
        self.assertEqual(set(self.native),{ITEM+n for n in ("DivingArmorItem","GingerbreadArmorItem",
            "OrtholanceItem","PrimitiveClubItem","SharpenedCandyCaneItem","SpearItem","TotemOfPossessionItem")})

    def test_individual_certificate_does_not_close_provider_or_promote_hooks(self):
        ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        e=ledger["objects"][PROVIDER.name+"/systems/dynamic-attributes.md"]
        self.assertEqual(set(e["evidence"]),AXES)
        self.assertEqual(e["status"],"COMPLETE_PERK_READY")
        self.assertEqual(e["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(e["physical_qa"],"NOT_TESTED")
        self.assertEqual(e["mutation"],"NO_MUTATION")
        self.assertNotIn(PROVIDER.name,ledger["providers"])
        inv=json.loads((PROVIDER/"INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        s=inv["integration_support_inventory"]
        prefix=s["reviewed_prefix"]
        roster=inv["remaining_family_inventory"]["item_outer_classes"]
        self.assertEqual([row["class"] for row in prefix],roster[:len(prefix)])
        self.assertEqual(prefix[4]["class"],"server/item/ACDynamicAttributeItem")
        self.assertEqual(prefix[4]["disposition"],"INDIVIDUAL_STATIC_CONTRACT_CERTIFIED")
        self.assertEqual(s["next_alphabetical_uncovered_scope"],roster[len(prefix)] if len(prefix)<len(roster) else None)
        self.assertFalse(s["family_universe_closed"])
        self.assertFalse(inv["whole_provider_catalog_closed"])
        for k in AXES:
            self.assertTrue((ROOT/e["evidence"][k]["path"]).is_file())

if __name__=="__main__":
    unittest.main()
