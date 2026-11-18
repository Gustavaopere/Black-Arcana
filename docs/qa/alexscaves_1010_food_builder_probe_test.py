#!/usr/bin/env python3
"""The seal is scoped to native construction and official external references."""
import collections
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
P="com/github/alexmodguy/alexscaves/"
I=P+"server/item/"
B=I+"ACFoodBuilder"
F="net.minecraft.world.food."
L="net.minecraft.world.entity.LivingEntity"
V="net.minecraft.world.item."

class FoodBuilderContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((PROVIDER/"EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json").read_text())
        cls.raw_native=Path(os.environ["AC_FOOD_NATIVE_REPORT"]).read_bytes()
        cls.raw_ref=Path(os.environ["AC_FOOD_REFERENCE_REPORT"]).read_bytes()
        cls.doc=json.loads(cls.raw_native);cls.ref=json.loads(cls.raw_ref)
        cls.native=cls.doc["native"];cls.consumers=cls.native["consumers"]

    def pivot(self,m,off,op,tok=""):
        r=next((r for r in m.get("pivots",m.get("instructions",[])) if r["offset"]==off),None)
        self.assertIsNotNone(r,(off,op,tok))
        self.assertEqual(r["opcode"],op)
        self.assertIn(tok,r["symbol"]+" "+r["operand"])

    def native_method(self,owner,name,desc=None):
        found=[m for m in self.consumers[owner]["selected_methods"] if m["declaration"]["name"]==name
               and (desc is None or m["declaration"]["descriptor"]==desc)]
        self.assertEqual(len(found),1,(owner,name,desc))
        return found[0]

    def vanilla(self,owner,name,args=None):
        found=[m for m in self.ref["vanilla"]["classes"][owner]["methods"] if m["named_method"]==name
               and (args is None or m["named_args"]==args)]
        self.assertEqual(len(found),1,(owner,name,args))
        return found[0]

    def test_report_hashes_and_independent_states(self):
        self.assertEqual(hashlib.sha256(self.raw_native).hexdigest(),self.seal["reports"]["native"]["sha256"])
        self.assertEqual(hashlib.sha256(self.raw_ref).hexdigest(),self.seal["reports"]["reference"]["sha256"])
        self.assertEqual(self.ref["native_sha256"],self.seal["reports"]["native"]["sha256"])
        self.assertEqual(self.doc["artifact"],{k:v for k,v in self.seal["artifact"].items() if k!="mod_id"})
        self.assertEqual(self.native["class_entries_scanned"],1555)
        self.assertEqual(self.ref["vanilla"]["identity"]["client"]["sha256"],self.seal["references"]["client_sha256"])
        self.assertEqual(self.ref["vanilla"]["identity"]["client_mappings"]["sha256"],self.seal["references"]["mappings_sha256"])
        for d in (self.doc,self.ref,self.seal["claims"]):
            for k,v in (("mutation","NO_MUTATION"),("mutating_hook","NOT_VERIFIED"),("physical_qa","NOT_TESTED"),("provider_universe_closed",False)):
                self.assertEqual(d[k],v)
        for k in ("perk_certification","runtime_dispatch"):
            self.assertIn(self.seal["claims"][k],("NOT_CERTIFIED","NOT_VERIFIED"))
        self.assertEqual(self.seal["claims"]["semantic_magic_roots_delta"],0)

    def test_complete_declared_builder_and_record(self):
        self.assertEqual(set(self.native["target_owners"]),{B,B+"$Effect"})
        a=self.consumers[B];e=self.consumers[B+"$Effect"]
        self.assertEqual(a["class_sha256"],self.seal["native"]["builder"]["sha256"])
        self.assertEqual(e["class_sha256"],self.seal["native"]["effect"]["sha256"])
        self.assertEqual(len(a["fields"]),9);self.assertEqual(len(e["fields"]),2)
        self.assertEqual({m["name"] for m in a["method_declarations"]},
                         {"<init>","<clinit>","of","nutrition","saturationMod","alwaysEat","meat","fast","bowl","sound","effect","resolve","build","food"})
        self.assertEqual({m["name"] for m in e["method_declarations"]},{"<init>","instance","probability","equals","hashCode","toString"})
        self.assertEqual(len(a["selected_methods"]),14);self.assertEqual(len(e["selected_methods"]),6)
        self.assertEqual(e["parent"],"java/lang/Record")
        self.pivot(self.native_method(B+"$Effect","<init>"),6,"putfield","instance:Ljava/util/function/Supplier;")
        self.pivot(self.native_method(B+"$Effect","<init>"),11,"putfield","probability:F")

    def test_setters_no_local_clamp_or_meat_sound_resolution(self):
        for name,op,field in (("nutrition","iload_1","nutrition:I"),("saturationMod","fload_1","saturationMod:F"),
                ("alwaysEat","iconst_1","alwaysEat:Z"),("meat","iconst_1","meat:Z"),
                ("fast","iconst_1","fast:Z"),("bowl","iconst_1","bowl:Z"),("sound","aload_1","sound:Lnet/minecraft/sounds/SoundEvent;")):
            m=self.native_method(B,name)
            self.assertEqual(m["instruction_count"],5)
            self.pivot(m,1,op);self.pivot(m,2,"putfield",field);self.pivot(m,6,"areturn")
        resolve=self.native_method(B,"resolve")
        self.assertEqual(resolve["declaration"]["code_sha256"],self.seal["native"]["builder"]["resolve_code_sha256"])
        self.assertEqual(resolve["instruction_count"],53)
        for name in ("meat:Z","sound:Lnet/minecraft/sounds/SoundEvent;"):
            self.assertFalse(any(name in r["symbol"] for r in resolve["pivots"]))
        # All typed Fieldref owners in publisher, including consumers outside the builder.
        for o,c in self.native["typed_census"].items():
            for r in c["member_refs"]:
                if r["owner"]==B and r["name"] in ("BUILT","meat","sound") and r["kind"]==9:
                    self.assertEqual(o,B)

    def test_resolve_and_identity_map(self):
        m=self.native_method(B,"resolve")
        for off,op,t in ((11,"invokevirtual","Builder.nutrition:"),(18,"invokevirtual","Builder.saturationModifier:"),
                         (26,"ifeq","34"),(30,"invokevirtual","Builder.alwaysEdible:"),(38,"ifeq","46"),
                         (42,"invokevirtual","Builder.fast:"),(50,"ifeq","61"),(54,"getstatic","Items.BOWL"),
                         (57,"invokevirtual","Builder.usingConvertsTo:"),(65,"invokeinterface","List.iterator"),
                         (77,"ifeq","114"),(92,"invokevirtual","Effect.instance:"),
                         (95,"invokeinterface","Supplier.get:"),(104,"invokevirtual","Effect.probability:"),
                         (107,"invokevirtual","Builder.effect:(Lnet/minecraft/world/effect/MobEffectInstance;F)"),
                         (111,"goto","71"),(115,"invokevirtual","Builder.build:")):
            self.pivot(m,off,op,t)
        self.pivot(self.native_method(B,"effect"),10,"invokespecial",'Effect."<init>":(Ljava/util/function/Supplier;F)V')
        self.pivot(self.native_method(B,"effect"),13,"invokeinterface","List.add")
        self.pivot(self.native_method(B,"<clinit>"),0,"new","IdentityHashMap")
        m=self.native_method(B,"build")
        self.pivot(m,1,"invokevirtual","resolve:");self.pivot(m,10,"invokeinterface","Map.put:")
        self.pivot(m,17,"areturn")
        uses=[(m["declaration"]["name"],r["offset"],r["opcode"]) for m in self.consumers[B]["selected_methods"] for r in m["pivots"] if "Field BUILT:" in r["symbol"]]
        self.assertEqual(set(uses),{("<clinit>",7,"putstatic"),("build",5,"getstatic")})
        self.pivot(self.native_method(B,"food"),2,"invokevirtual","Item$Properties.food:")

    def test_food_registry_and_direct_bridge_counts(self):
        a=self.consumers[I+"ACFoods"]
        self.assertEqual(len(a["fields"]),63)
        self.assertTrue(all(f["descriptor"]=="Lnet/minecraft/world/food/FoodProperties;" for f in a["fields"]))
        m=self.native_method(I+"ACFoods","<clinit>")
        self.assertEqual(collections.Counter(r["reference"]["name"] for r in m["typed_sites"] if r["reference"]["owner"]==B and r["opcode"].startswith("invoke")),self.seal["native"]["food_registry"]["calls"])
        calls={}
        for owner,e in self.consumers.items():
            if owner==B:continue
            n=sum(r["reference"]["owner"]==B and r["reference"]["name"]=="food" and r["opcode"]=="invokestatic" for m in e["selected_methods"] for r in m["typed_sites"])
            if n:calls[owner.rsplit("/",1)[1]]=n
        self.assertEqual(calls,self.seal["native"]["direct_food_bridge_calls"])

    def test_vanilla_food_parameters_and_clamps(self):
        m=self.vanilla(F+"FoodConstants","saturationByModifier")
        self.assertEqual([r["opcode"] for r in m["instructions"]],["iload_0","i2f","fload_1","fmul","fconst_2","fmul","freturn"])
        m=self.vanilla(F+"FoodProperties$Builder","<init>")
        self.pivot(m,5,"ldc","float 1.6f");self.pivot(m,7,"putfield")
        m=self.vanilla(F+"FoodProperties$Builder","fast")
        self.pivot(m,1,"ldc","float 0.8f");self.pivot(m,3,"putfield")
        self.pivot(self.vanilla(F+"FoodProperties$Builder","build"),8,"invokestatic","cpp.a:(IF)F")
        m=self.vanilla(F+"FoodProperties","eatDurationTicks")
        self.pivot(m,4,"ldc","float 20.0f");self.pivot(m,6,"fmul");self.pivot(m,7,"f2i")
        m=self.vanilla(F+"FoodData","add",["int","float"])
        self.pivot(m,8,"bipush","20");self.pivot(m,10,"invokestatic","(III)I");self.pivot(m,29,"invokestatic","(FFF)F")
        self.pivot(self.vanilla(F+"FoodData","eat",[F+"FoodProperties"]),9,"invokevirtual","b:(IF)V")

    def test_vanilla_eat_order_rng_and_consume(self):
        m=self.vanilla(L,"addEatEffect")
        for off,op,t in ((4,"invokevirtual","dcw.x_:()Z"),(10,"return",""),(47,"invokeinterface","ayw.i:()F"),
                         (54,"invokevirtual","cpr$b.b:()F"),(57,"fcmpg",""),(58,"ifge","71"),
                         (64,"invokevirtual","cpr$b.a:()Lbrz;"),(67,"invokevirtual","b:(Lbrz;)Z"),(70,"pop","")):
            self.pivot(m,off,op,t)
        m=self.vanilla(L,"eat",["net.minecraft.world.level.Level",V+"ItemStack",F+"FoodProperties"])
        self.pivot(m,53,"invokevirtual","(Lcpr;)V");self.pivot(m,57,"iconst_1");self.pivot(m,59,"invokevirtual","cuq.a:(ILbtn;)V")
        m=self.vanilla(V+"ItemStack","consume")
        self.pivot(m,5,"invokevirtual","btn.fL:()Z");self.pivot(m,8,"ifne","16");self.pivot(m,13,"invokevirtual","h:(I)V")
        m=self.vanilla("net.minecraft.world.entity.player.Player","eat")
        self.pivot(m,5,"invokevirtual","cpq.a:(Lcpr;)V");self.pivot(m,87,"invokespecial","btn.a:")
        self.pivot(m,107,"invokevirtual","fL:()Z");self.pivot(m,129,"invokevirtual","cuq.s:()Lcuq;")
        self.pivot(m,140,"ifne","162");self.pivot(m,158,"invokevirtual","cmw.f:(Lcuq;)Z")
        self.pivot(self.vanilla(V+"Item","use"),31,"invokevirtual","cmx.u:(Z)Z")
        self.pivot(self.vanilla(V+"Item","getUseDuration"),16,"invokevirtual","cpr.a:()I")

    def test_pinned_neoforge_boundary_and_finish_order(self):
        e=self.doc["engine"]["universal"]
        for o,off,op,t in (("IItemExtension",1,"getstatic","DataComponents.FOOD"),("IItemStackExtension",16,"invokevirtual","Item.getFoodProperties:")):
            m=next(m for m in e["net/neoforged/neoforge/common/extensions/"+o]["methods"] if m["declaration"]["name"]=="getFoodProperties")
            self.pivot(m,off,op,t)
        p=self.ref["neoforge"]["food_patch"]
        self.assertTrue(any(r["text"].startswith("+") and "this(() -> effect, probability)" in r["text"] for r in p["lines"]))
        self.assertTrue(any(r["text"].startswith("+") and "new MobEffectInstance(this.effectSupplier.get())" in r["text"] for r in p["lines"]))
        m=next(m for m in self.ref["neoforge"]["methods"] if m["declaration"]["name"]=="onItemUseFinish")
        self.pivot(m,18,"invokeinterface","IEventBus.post");self.pivot(m,26,"invokevirtual","Finish.getResultStack:")
        patch=next(p for p in self.doc["engine"]["patches"] if p["entry"].endswith("/LivingEntity.java.patch"))
        self.assertTrue(any("EventHooks.onItemUseFinish" in r["text"] and "this.useItem.finishUsingItem" in r["text"] for r in patch["food_reference_lines"]))

    def test_ledger_and_open_prefix(self):
        d=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        e=d["objects"][PROVIDER.name+"/systems/food-builder.md"]
        self.assertEqual(set(e["evidence"]),set(self.seal["axes"]))
        self.assertEqual(e["status"],"COMPLETE_PERK_READY")
        for k in ("mutation","mutating_hook","physical_qa","runtime_dispatch","perk_certification"):
            self.assertEqual(e[k],self.seal["claims"][k])
        self.assertNotIn(PROVIDER.name,d["providers"])
        inv=json.loads((PROVIDER/"INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        s=inv["integration_support_inventory"];roster=inv["remaining_family_inventory"]["item_outer_classes"];prefix=s["reviewed_prefix"]
        self.assertEqual([r["class"] for r in prefix],roster[:len(prefix)])
        self.assertEqual(prefix[6]["class"],"server/item/ACFoodBuilder")
        self.assertEqual(prefix[6]["disposition"],"INDIVIDUAL_STATIC_CONTRACT_CERTIFIED")
        self.assertEqual(s["next_alphabetical_uncovered_scope"],roster[len(prefix)] if len(prefix)<len(roster) else None)
        self.assertFalse(s["family_universe_closed"]);self.assertFalse(inv["whole_provider_catalog_closed"])

if __name__=="__main__":
    unittest.main()
