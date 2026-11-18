#!/usr/bin/env python3
"""Regression assertions over the exact-JAR construction discovery report."""
import json
import os
from pathlib import Path
import unittest

P="com/github/alexmodguy/alexscaves/"
I=P+"server/item/"
E="net/neoforged/neoforge/common/extensions/"
EXPECTED={
 "primitive_club":(40,"PrimitiveClubItem"),
 "limestone_spear":(45,"LimestoneSpearItem"),
 "extinction_spear":(49,"ExtinctionSpearItem"),
 "diving_helmet":(99,"DivingArmorItem"),
 "diving_chestplate":(100,"DivingArmorItem"),
 "diving_leggings":(101,"DivingArmorItem"),
 "diving_boots":(102,"DivingArmorItem"),
 "ortholance":(110,"OrtholanceItem"),
 "totem_of_possession":(126,"TotemOfPossessionItem"),
 "sharpened_candy_cane":(172,"SharpenedCandyCaneItem"),
 "gingerbread_helmet":(187,"GingerbreadArmorItem"),
 "gingerbread_chestplate":(188,"GingerbreadArmorItem"),
 "gingerbread_leggings":(189,"GingerbreadArmorItem"),
 "gingerbread_boots":(190,"GingerbreadArmorItem"),
 "frostmint_spear":(192,"FrostmintSpearItem")
}

class ConstructionEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(Path(os.environ["AC_ATTRIBUTE_CONSTRUCTION_REPORT"]).read_text())
        cls.native=cls.doc["provider"]["native_owners"]
        cls.engine=cls.doc["engine_reference"]["universal"]

    def method(self, owner, name, desc=None, engine=False):
        pool=self.engine if engine else self.native
        found=[m for m in pool[owner]["methods"]
               if m["name"]==name and (desc is None or m["descriptor"]==desc)]
        self.assertEqual(len(found),1,(owner,name,desc))
        return found[0]

    def pivot(self,m,offset,opcode,token=""):
        row=next((r for r in m["instructions"] if r["offset"]==offset),None)
        self.assertIsNotNone(row,(m["name"],offset))
        self.assertEqual(row["opcode"],opcode)
        self.assertIn(token,row["symbol"]+" "+row["operand"])

    def test_authority_and_noncertification(self):
        self.assertEqual(self.doc["provider"]["census_class_count"],1555)
        self.assertEqual(self.doc["provider"]["publisher_artifact"]["sha256"],
                         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(self.doc["engine_reference"]["version"],"21.1.250")
        self.assertEqual(self.doc["scope"],"BOUNDED_CONSTRUCTION_DISCOVERY_NOT_CERTIFIED")
        self.assertEqual(self.doc["mutation"],"NO_MUTATION")
        self.assertFalse(self.doc["provider_universe_closed"])
        self.assertEqual(self.doc["physical_qa"],"NOT_TESTED")

    def test_weapon_additive_modifiers(self):
        for name,damage,speed,offsets in (
            ("OrtholanceItem",5.0,-2.4000000953674316,(10,20,23,34,44,47,62)),
            ("SharpenedCandyCaneItem",3.0,4.0,(10,20,23,34,44,47,62)),
            ("TotemOfPossessionItem",2.0,-2.4000000953674316,(28,38,41,52,62,65,80))):
            m=self.method(I+name,"<init>")
            a,b,c,d,e,f,g=offsets
            for offset,opcode,token in (
                (a,"getstatic","Attributes.ATTACK_DAMAGE"),(b,"ldc2_w",f"double {damage}d"),
                (c,"getstatic","ADD_VALUE"),(d,"getstatic","Attributes.ATTACK_SPEED"),
                (e,"ldc2_w",f"double {speed}d"),(f,"getstatic","ADD_VALUE"),
                (g,"putfield","defaultModifiers")):
                self.pivot(m,offset,opcode,token)
        m=self.method(I+"SpearItem","<init>")
        for off,op,tok in ((12,"getstatic","ATTACK_DAMAGE"),(22,"dload_2",""),
                            (23,"getstatic","ADD_VALUE"),(35,"getstatic","ATTACK_SPEED"),
                            (45,"ldc2_w","double -3.0d"),(48,"getstatic","ADD_VALUE"),
                            (64,"putfield","defaultModifiers")):
            self.pivot(m,off,op,tok)
        for name,value in (("LimestoneSpearItem",3.0),("FrostmintSpearItem",5.0),
                           ("ExtinctionSpearItem",8.0)):
            m=self.method(I+name,"<init>")
            self.pivot(m,2,"ldc2_w",f"double {value}d")
            self.pivot(m,5,"invokespecial",'SpearItem."<init>"')

    def test_diving_and_gingerbread_initialization(self):
        m=self.method(I+"DivingArmorItem","<init>")
        for off,op,tok in ((52,"getstatic","Attributes.ARMOR:"),(63,"invokevirtual","ACArmorMaterial.defense"),
                           (78,"getstatic","LEGGINGS"),(81,"if_acmpne","113"),
                           (85,"invokestatic","ACPlatform.swimSpeedAttribute"),(97,"ldc2_w","double 0.5d"),
                           (100,"getstatic","ADD_VALUE"),(114,"getstatic","CHESTPLATE"),
                           (117,"if_acmpne","145"),(121,"getstatic","ARMOR_TOUGHNESS"),
                           (131,"invokevirtual","ACArmorMaterial.toughness"),(151,"ifle","179"),
                           (155,"getstatic","KNOCKBACK_RESISTANCE"),(184,"putfield","divingArmorAttributes")):
            self.pivot(m,off,op,tok)
        m=self.method(I+"GingerbreadArmorItem","<init>")
        for off,op,tok in ((22,"new","HashMap"),(29,"putfield","gingerbreadDurabilityDependentAttributes"),
                           (40,"invokevirtual","ACArmorMaterial.defense"),(43,"putfield","acDefense"),
                           (98,"getstatic","MOVEMENT_SPEED"),(106,"ldc2_w","double 0.1d"),
                           (109,"getstatic","ADD_MULTIPLIED_BASE"),(125,"putfield","defaultAttributes")):
            self.pivot(m,off,op,tok)
        m=self.method(I+"PrimitiveClubItem","<init>")
        self.pivot(m,27,"invokevirtual","getStatsForEnchantmentLevel")
        self.pivot(m,30,"aastore")

    def test_registry_factory_bindings(self):
        r=self.doc["provider"]["registry"]
        factories={m["name"]:m for m in r["factories"]}
        windows={name:w for w in r["clinit_bootstrap_windows"] for name in w["factory_names"]}
        self.assertEqual(set(factories),{"lambda$static$"+str(v[0]) for v in EXPECTED.values()})
        self.assertEqual(set(windows),set(factories))
        self.assertEqual(len(r["clinit_bootstrap_windows"]),len(EXPECTED))
        for item,(number,owner) in EXPECTED.items():
            name="lambda$static$"+str(number)
            self.pivot(factories[name],0,"new",I+owner)
            w=windows[name]
            self.assertEqual(w["factory_names"],[name])
            at=next(i for i,row in enumerate(w["window"]) if row["offset"]==w["offset"])
            self.assertEqual(w["window"][at-1]["symbol"],"String "+item)
            self.assertEqual(w["window"][at+1]["opcode"],"invokevirtual")
            self.assertIn("ACDeferredRegister.register:",w["window"][at+1]["symbol"])
            self.assertEqual(w["window"][at+2]["opcode"],"putstatic")
            self.assertIn("Field "+item.upper()+":",w["window"][at+2]["symbol"])

    def test_bootstraps_bind_provider_and_super_fallback(self):
        names={"DivingArmorItem","GingerbreadArmorItem","OrtholanceItem","PrimitiveClubItem",
               "SharpenedCandyCaneItem","SpearItem","TotemOfPossessionItem"}
        for name in names:
            m=self.method(I+name,"getDefaultAttributeModifiers")
            b=m["bootstrap_call_sites"]
            self.assertEqual([x["offset"] for x in b],[1,9])
            args=[next(a["reference"] for a in x["bootstrap"]["arguments"]
                       if isinstance(a,dict) and "reference" in a) for x in b]
            self.assertEqual(args[0][1],I+name)
            self.assertEqual(args[0][2][1],"acModifiers")
            fallback=args[1][2][1]
            self.assertEqual(fallback,"lambda$getDefaultAttributeModifiers$"+("1" if name=="TotemOfPossessionItem" else "0"))
            self.assertEqual(args[1][1],I+name)
            self.method(I+name,fallback)
        for n in ("lambda$itemAttributes$0","lambda$itemAttributes$1"):
            m=self.method(P+"server/misc/ACCompat",n)
            self.pivot(m,4,"invokevirtual","ItemAttributeModifiers$Builder.add:")
        m=self.method(P+"server/misc/ACCompat","attributeModifier")
        self.pivot(m,8,"invokestatic","ResourceLocation.fromNamespaceAndPath")
        self.pivot(m,11,"dload_3")
        self.pivot(m,14,"invokespecial",'AttributeModifier."<init>"')

    def test_pinned_external_component_precedence(self):
        m=self.method(E+"IItemStackExtension","getAttributeModifiers",engine=True)
        for off,op,tok in ((6,"getstatic","DataComponents.ATTRIBUTE_MODIFIERS"),(9,"getstatic","ItemAttributeModifiers.EMPTY"),
                           (23,"invokeinterface","List.isEmpty"),(28,"ifeq","50"),
                           (46,"invokevirtual","Item.getDefaultAttributeModifiers:(Lnet/minecraft/world/item/ItemStack;)"),
                           (57,"invokestatic","CommonHooks.computeModifiedAttributes")):
            self.pivot(m,off,op,tok)
        m=self.method(E+"IItemExtension","getDefaultAttributeModifiers",engine=True)
        self.pivot(m,6,"invokevirtual","Item.getDefaultAttributeModifiers:()")
        patch=next(x for x in self.doc["engine_reference"]["patches"] if x["entry"].endswith("ItemStack.java.patch"))
        added=[x["text"].strip() for x in patch["matching_lines"] if x["text"].startswith("+")]
        self.assertEqual(sum("this.getAttributeModifiers().forEach(" in x for x in added),2)

if __name__=="__main__":
    unittest.main()
