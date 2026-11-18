#!/usr/bin/env python3
"""Regression checks: sealed exact JAR and separately pinned external reference."""
import collections
import hashlib
import json
import os
from pathlib import Path
import unittest
import zipfile
from alexscaves_1010_armor_material_audit import ClassReader, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
I="com/github/alexmodguy/alexscaves/server/item/"
T=I+"ACEnchantableItem"
V="net.minecraft.world.item."
E="net/neoforged/neoforge/common/extensions/"
VALUE=("getEnchantmentValue","()I")
GUARD=("isEnchantable","(Lnet/minecraft/world/item/ItemStack;)Z")

class ExactContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((PROVIDER/"EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.json").read_text())
        cls.native_raw=Path(os.environ["AC_ENCHANTABLE_NATIVE_REPORT"]).read_bytes()
        cls.ext_raw=Path(os.environ["AC_ENCHANTABLE_BOUNDARY_REPORT"]).read_bytes()
        cls.native=json.loads(cls.native_raw)
        cls.ext=json.loads(cls.ext_raw)
        cls.p=cls.native["publisher"]
        cls.expected={I+r["owner"]:r for r in cls.seal["owners"]}

    def pivot(self,m,off,op,tok=""):
        r=next((r for r in m["instructions"] if r["offset"]==off),None)
        self.assertIsNotNone(r)
        self.assertEqual(r["opcode"],op)
        self.assertIn(tok,r["symbol"]+" "+r["operand"])

    def method(self,entry,name,desc=None):
        found=[m for m in entry["methods"] if m["declaration"]["name"]==name and
               (desc is None or m["declaration"]["descriptor"]==desc)]
        self.assertEqual(len(found),1,(name,desc))
        return found[0]

    def vanilla(self,owner,name):
        found=[m for m in self.ext["vanilla"]["classes"][V+owner]["methods"] if m["named_method"]==name]
        self.assertEqual(len(found),1,(owner,name))
        return found[0]

    def test_hash_seals_and_scope(self):
        for raw,k in ((self.native_raw,"native"),(self.ext_raw,"boundary")):
            self.assertEqual(hashlib.sha256(raw).hexdigest(),self.seal["reports"][k]["sha256"])
        self.assertEqual(self.native["artifact"],{k:v for k,v in self.seal["artifact"].items() if k!="mod_id"})
        self.assertEqual(self.p["class_entries_scanned"],1555)
        self.assertEqual(self.p["target_class_sha256"],self.seal["interface"]["sha256"])
        self.assertEqual(self.ext["native_report_sha256"],self.seal["reports"]["native"]["sha256"])
        for d in (self.native,self.ext,self.seal["claims"]):
            for k,v in (("mutation","NO_MUTATION"),("mutating_hook","NOT_VERIFIED"),
                        ("physical_qa","NOT_TESTED"),("provider_universe_closed",False)):
                self.assertEqual(d[k],v)
        self.assertEqual(self.seal["claims"]["perk_certification"],"NOT_CERTIFIED")
        self.assertEqual(self.seal["claims"]["runtime_dispatch"],"NOT_VERIFIED")
        self.assertEqual(self.seal["claims"]["semantic_magic_roots_delta"],0)
        self.assertEqual(set(self.seal["axes"]),{"identity","behavior","parameters","targeting","costs","integration","validation"})

    def test_interface_and_roster(self):
        self.assertEqual(self.p["target"],T)
        self.assertEqual(self.p["target_fields"],[])
        self.assertEqual(self.p["owner_declarations_and_bodies"][T]["hierarchy"]["interfaces"],[])
        self.assertEqual([(m["name"],m["descriptor"],m["access"]) for m in self.p["target_methods"]],
                         [tuple(m) for m in self.seal["interface"]["methods"]])
        self.assertNotIn("code_sha256",self.p["target_methods"][0])
        self.assertEqual(self.p["target_methods"][1]["code_sha256"],self.seal["interface"]["default_code_sha256"])
        self.assertEqual(set(self.p["direct_implementers"]),set(self.expected))
        self.assertEqual(self.p["inherited_implementers"],[])
        self.assertEqual(set(self.p["typed_reference_census"]),{T,*self.expected})
        self.assertEqual(self.p["member_references_by_name"],{})
        self.assertEqual(self.p["exact_signature_callsites"],{})
        self.assertEqual(set(self.p["owner_declarations_and_bodies"]),{T,*self.expected})

    def test_all_values_and_guards(self):
        entries=self.p["owner_declarations_and_bodies"]
        for owner,r in self.expected.items():
            m=self.method(entries[owner],*VALUE)
            self.assertEqual(m["declaration"]["code_sha256"],self.seal["interface"]["constant_value_code_sha256"])
            self.assertEqual(m["instruction_count"],2)
            self.pivot(m,0,"iconst_1"); self.pivot(m,1,"ireturn")
            self.assertEqual(m["declaration"]["access"],1)
            guards=[m for m in entries[owner]["declared_methods"] if m["name"]==GUARD[0]]
            self.assertEqual(len(guards),int(r["declares_count_guard"]))
            if not guards:
                self.assertEqual(entries[owner]["hierarchy"]["parent"],"net/minecraft/world/item/Item")
        for owner in [T,*[o for o,r in self.expected.items() if r["declares_count_guard"]]]:
            m=self.method(entries[owner],*GUARD)
            self.assertEqual(m["instruction_count"],8)
            self.assertEqual(m["declaration"]["code_size"],14)
            for off,op,tok in ((0,"aload_1",""),(1,"invokevirtual","ItemStack.getCount:()I"),
                               (4,"iconst_1",""),(5,"if_icmpne","12"),(8,"iconst_1",""),
                               (9,"goto","13"),(12,"iconst_0",""),(13,"ireturn","")):
                self.pivot(m,off,op,tok)

    def test_thirteen_bindings(self):
        r=self.p["registry"]
        f={m["name"]:m for m in r["constructor_factories"]}
        w={m["handles"][0]["name"]:m for m in r["clinit_bootstrap_windows"]}
        self.assertEqual(len(r["constructor_factories"]),13)
        self.assertEqual(len(r["clinit_bootstrap_windows"]),13)
        self.assertEqual(set(f),{m["factory"] for m in self.expected.values()})
        self.assertEqual(set(w),set(f))
        for owner,r in self.expected.items():
            n=r["factory"]; item=r["item_id"].split(":")[1]
            self.assertEqual(f[n]["new_owners"],[{"offset":0,"owner":owner}])
            self.assertEqual(w[n]["offset"],r["bootstrap_offset"])
            self.assertEqual(w[n]["handles"],[{"name":n,"descriptor":"()Lnet/minecraft/world/item/Item;"}])
            body=w[n]["window"]; at=next(i for i,v in enumerate(body) if v["offset"]==w[n]["offset"])
            self.assertEqual(body[at-1]["symbol"],"String "+item)
            self.assertIn("ACDeferredRegister.register:",body[at+1]["symbol"])
            self.assertIn("Field "+item.upper()+":",body[at+2]["symbol"])

    def test_native_ortholance_and_no_additional_declared_overrides(self):
        jar=Path(os.environ["AC_ENCHANTABLE_JAR"])
        verify_artifact(jar)
        names={"getEnchantmentValue","isEnchantable","supportsEnchantment","isPrimaryItemFor","canApplyAtEnchantingTable"}
        with zipfile.ZipFile(jar) as z:
            for owner,r in self.expected.items():
                reader=ClassReader(z.read(owner+".class"))
                found={(m["name"],m["descriptor"]) for m in reader.methods if m["name"] in names}
                wanted={VALUE}|({GUARD} if r["declares_count_guard"] else set())
                self.assertEqual(found,wanted,owner)
        javap=Path(os.environ["AC_ENCHANTABLE_JAVAP"])
        b=disassemble(jar,javap,I+"ACItemRegistry")[("lambda$static$110","()Lnet/minecraft/world/item/Item;")]
        self.assertEqual(b[11],("sipush","340",""))
        self.assertIn("Item$Properties.durability:(I)",b[14][2])
        self.assertIn("OrtholanceItem.",b[23][2])
        b=disassemble(jar,javap,I+"OrtholanceItem")[("<init>","(Lnet/minecraft/world/item/Item$Properties;)V")]
        self.assertIn('net/minecraft/world/item/Item."<init>":(Lnet/minecraft/world/item/Item$Properties;)V',b[2][2])

    def test_vanilla_class_gate_and_stack_gate(self):
        m=self.vanilla("Item","isEnchantable")
        self.assertEqual(m["declaration"]["code_sha256"],"801002b78fdcb3657282d200a5e63cbb17c65c05ad4b038454e1c186099b30a1")
        for off,op,tok in ((1,"invokevirtual","cuq.j:()I"),(4,"iconst_1",""),(5,"if_icmpne","22"),
                           (9,"getstatic","Field kq.d:Lkp;"),(12,"invokevirtual","cuq.b:(Lkp;)Z"),(15,"ifeq","22")):
            self.pivot(m,off,op,tok)
        m=self.vanilla("ItemStack","isEnchantable")
        self.assertEqual(m["declaration"]["code_sha256"],"726c744f1e31404ae4b3e285569fbcdc280f3d94b64416fc6e44aa8bbe28dd0f")
        for off,op,tok in ((5,"invokevirtual","cul.a:(Lcuq;)Z"),(8,"ifeq","39"),(12,"getstatic","Field kq.k:Lkp;"),
                           (23,"ifnull","37"),(27,"invokevirtual","dai.d:()Z"),(30,"ifeq","37")):
            self.pivot(m,off,op,tok)
        b=self.ext["vanilla"]["resolved_member_references"]
        for owner,offset,name in (("Item",1,"ItemStack.getMaxStackSize"),("Item",9,"DataComponents.MAX_DAMAGE"),
                                  ("ItemStack",5,"Item.isEnchantable"),("ItemStack",12,"DataComponents.ENCHANTMENTS"),
                                  ("ItemStack",27,"ItemEnchantments.isEmpty")):
            q=[r for r in b[V+owner] if r["method"]=="isEnchantable" and r["offset"]==offset]
            self.assertEqual(len(q),1)
            self.assertTrue(any(n.endswith(name) for n in q[0]["named_candidates"]))
        idn=self.ext["vanilla"]["identity"]; expected=self.seal["references"]
        self.assertEqual(idn["metadata_sha1"],expected["mojang_metadata_sha1"])
        for part,key in (("client","mojang_client"),("client_mappings","mojang_mappings")):
            for sha in ("sha1","sha256"):
                self.assertEqual(idn[part][sha],expected[key+"_"+sha])

    def test_neoforge_value_vs_eligibility(self):
        e=self.ext["neoforge_universal"]
        self.pivot(self.method(e[E+"IItemStackExtension"],"getEnchantmentValue"),15,"invokevirtual","Item.getEnchantmentValue:(Lnet/minecraft/world/item/ItemStack;)I")
        self.pivot(self.method(e[E+"IItemExtension"],"getEnchantmentValue"),6,"invokevirtual","Item.getEnchantmentValue:()I")
        m=self.method(e[E+"IItemExtension"],"supportsEnchantment")
        self.pivot(m,1,"getstatic","Items.ENCHANTED_BOOK")
        self.pivot(m,20,"invokevirtual","Enchantment.isSupportedItem:")
        m=self.method(e[E+"IItemExtension"],"isPrimaryItemFor")
        self.pivot(m,4,"getstatic","Items.BOOK")
        self.pivot(m,24,"invokevirtual","EnchantmentDefinition.primaryItems:")
        self.pivot(m,31,"invokeinterface","supportsEnchantment:")
        self.pivot(m,54,"invokevirtual","ItemStack.is:")
        for n in ("supportsEnchantment","isPrimaryItemFor"):
            self.pivot(self.method(e[E+"IItemStackExtension"],n),16,"invokevirtual","Item."+n+":")
        patches=self.native["engine"]["patches"]
        helper=next(p for p in patches if p["entry"].endswith("/EnchantmentHelper.java.patch"))
        self.assertEqual(sum(r["text"].startswith("+") and ".getEnchantmentValue();" in r["text"] for r in helper["matching_lines"]),2)
        anvil=next(p for p in patches if p["entry"].endswith("/AnvilMenu.java.patch"))
        self.assertTrue(any(r["text"].startswith("+") and "itemstack.supportsEnchantment(holder)" in r["text"] for r in anvil["matching_lines"]))

    def test_all_resources_and_tags(self):
        r=self.ext["publisher_resources"]
        self.assertEqual(r["unresolved_local_tags"],[])
        self.assertEqual(len(r["enchantments"]),51)
        self.assertEqual(len({e["id"] for e in r["enchantments"]}),51)
        self.assertTrue(all(e["primary_items"] is None for e in r["enchantments"]))
        expected={"#alexscaves:enchantable/"+v["item_id"].split(":")[1]:v["resource_count"] for v in self.expected.values()}
        expected["#alexscaves:enchantable/desolate_dagger"]=3
        self.assertEqual(collections.Counter(e["supported_items"] for e in r["enchantments"]),expected)
        self.assertEqual(set(r["direct_referenced_local_tags"]),set(expected))
        for tag,entry in r["direct_referenced_local_tags"].items():
            self.assertEqual(entry["values"],["alexscaves:"+tag.rsplit("/",1)[1]])
            self.assertFalse(entry["replace"])

    def test_ledger_and_prefix(self):
        d=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        e=d["objects"][PROVIDER.name+"/systems/enchantable-item.md"]
        self.assertEqual(set(e["evidence"]),set(self.seal["axes"]))
        self.assertEqual(e["status"],"COMPLETE_PERK_READY")
        for k,v in (("mutating_hook","NOT_VERIFIED"),("physical_qa","NOT_TESTED"),("mutation","NO_MUTATION"),
                    ("runtime_dispatch","NOT_VERIFIED"),("perk_certification","NOT_CERTIFIED")):
            self.assertEqual(e[k],v)
        self.assertNotIn(PROVIDER.name,d["providers"])
        inv=json.loads((PROVIDER/"INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        s=inv["integration_support_inventory"]; prefix=s["reviewed_prefix"]
        roster=inv["remaining_family_inventory"]["item_outer_classes"]
        self.assertEqual([r["class"] for r in prefix],roster[:len(prefix)])
        self.assertEqual(prefix[5]["class"],"server/item/ACEnchantableItem")
        self.assertEqual(prefix[5]["disposition"],"INDIVIDUAL_STATIC_CONTRACT_CERTIFIED")
        self.assertEqual(s["next_alphabetical_uncovered_scope"],roster[len(prefix)])
        self.assertFalse(s["family_universe_closed"])
        self.assertFalse(inv["whole_provider_catalog_closed"])

if __name__=="__main__":
    unittest.main()
