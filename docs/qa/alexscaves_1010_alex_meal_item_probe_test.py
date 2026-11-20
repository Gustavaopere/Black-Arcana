#!/usr/bin/env python3
"""Exact AlexMealItem evidence replay; no transformed engine execution."""
import hashlib
import json
import os
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
class AlexMealContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((DIR/"EXACT-ALEX-MEAL-ITEM-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
        cls.raw=Path(os.environ["AC_MEAL_REPORT"]).read_bytes()
        cls.report=json.loads(cls.raw)
        cls.native=cls.report["native"]
    def test_report(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),self.seal["native_report_sha256"])
        self.assertEqual(self.report["artifact"],self.seal["artifact"])
        for k in ("class_sha256","parent","interfaces","fields","descendants","typed_census","consumers","resources"):
            self.assertEqual(self.native[k],self.seal[k])
        self.assertEqual([{k:m[k] for k in ("declaration","instruction_count","instruction_sha256")} for m in self.native["methods"]],self.seal["methods"])
        self.assertEqual({k:self.native["factory"][k] for k in ("declaration","instruction_count","instruction_sha256")},self.seal["factory"])
    def test_own_constructor_and_tooltip(self):
        methods={m["declaration"]["name"]:{r["offset"]:r for r in m["instructions"]} for m in self.native["methods"]}
        self.assertEqual(set(methods),{"<init>","appendHoverText"})
        ctor=methods["<init>"]
        self.assertIn("ACFoods.ALEX_MEAL",ctor[8]["symbol"])
        self.assertIn("ACFoodBuilder.food",ctor[11]["symbol"])
        self.assertIn("RARITY_RAINBOW",ctor[14]["symbol"])
        self.assertEqual(ctor[20]["opcode"],"iconst_1")
        self.assertIn("stacksTo",ctor[21]["symbol"])
        self.assertIn("Item.appendHoverText",methods["appendHoverText"][30]["symbol"])
    def test_food_and_reference_crosswalk(self):
        food=json.loads((DIR/"EXACT-FOODS-DISCOVERY-1.0.10.json").read_text(encoding="utf8"))
        field=next(f for f in food["fields"] if f["field"]=="ALEX_MEAL")
        self.assertEqual(field,self.seal["food_field"])
        self.assertEqual((field["nutrition"],field["saturation_modifier"]),(40,5))
        self.assertEqual(field["flags"],[{"name":"bowl"}])
        self.assertEqual([(e["supplier"],e["probability"]) for e in field["effects"]],[("lambda$static$44",1),("lambda$static$45",1)])
        cert=json.loads((DIR/"EXACT-FOODS-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
        self.assertEqual(cert["reports"],self.seal["food_reference_reports"])
        self.assertEqual(self.native["factory"]["declaration"]["code_sha256"],"e559a38fd03a5f06618574de17f28978ef49c402eaa1abe4c78b8f5ae583a84f")
    def test_recipe_and_fail_closed(self):
        recipe=self.native["resources"]["data/alexscaves/recipe/alex_meal.json"]["json"]
        self.assertEqual(recipe["type"],"minecraft:crafting_shapeless")
        self.assertEqual(recipe["result"]["id"],self.seal["resource_id"])
        self.assertEqual(len(recipe["ingredients"]),7)
        self.assertEqual(sum(i["item"]=="alexscaves:gingerbread_crumbs" for i in recipe["ingredients"]),2)
        for k,v in {"mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","provider_universe_closed":False}.items():
            self.assertEqual(self.seal[k],v)
            self.assertEqual(self.report[k],v)
if __name__=="__main__":unittest.main()
