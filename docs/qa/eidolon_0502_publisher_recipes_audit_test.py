#!/usr/bin/env python3
"""Clean-room recipe identity, exclusion and fail-closed SHA fixtures."""
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("eidolon_0502_publisher_recipes_audit",HERE/"eidolon_0502_publisher_recipes_audit.py")
aud=importlib.util.module_from_spec(spec)
spec.loader.exec_module(aud)

def fake_jar(missing=None,override=None,extra=None):
    result=io.BytesIO()
    override=override or {}
    with zipfile.ZipFile(result,"w") as z:
        z.writestr("META-INF/neoforge.mods.toml",'modLoader="javafml"\n[[mods]]\nmodId="eidolon_repraised"\n')
        for stem in sorted(aud.CHANTS):
            path=aud.RECIPE_ROOT+stem+".json"
            if path==missing: continue
            doc={"type":"eidolon_repraised:chant","id":"eidolon_repraised:"+stem,
                 "signs":[{"sign":"eidolon_repraised:flame"},{"sign":"eidolon_repraised:sacred"}]}
            z.writestr(path,json.dumps(override.get(path,doc)))
        for stem in sorted(aud.CONVERSIONS):
            path=aud.RECIPE_ROOT+stem+".json"
            if path==missing: continue
            doc={"type":"eidolon_repraised:chant_conversion","input":{"item":"minecraft:coal"},
                 "output":{"id":"minecraft:stick","count":1}}
            z.writestr(path,json.dumps(override.get(path,doc)))
        for stem in sorted(aud.RITUALS):
            path=aud.RECIPE_ROOT+"rituals/"+stem+".json"
            if path==missing: continue
            doc={"type":aud.ritual_type(stem),"reagent":{"item":"minecraft:coal"},"pedestal_items":[]}
            if stem in aud.GENERIC: doc["ritual"]="eidolon_repraised:"+stem
            if stem in aud.SUMMONS:
                doc["output"]=("eidolon_repraised:" if stem in {"summon_wraith","summon_slimy_slug","summon_raven"} else "minecraft:")+stem.removeprefix("summon_")
                doc["count"]=3 if stem in {"summon_husk","summon_drowned","summon_slimy_slug","summon_raven"} else 1
            if stem in aud.CRAFTING:
                doc["result"]={"id":"eidolon_repraised:synthetic"}
                doc["health_requirement"]=20
            if stem in aud.LOCATION:
                doc["structure"]="eidolon_repraised:catacombs"
            z.writestr(path,json.dumps(override.get(path,doc)))
        if extra:
            for p,v in extra.items():z.writestr(p,json.dumps(v))
    return result.getvalue()

class PhysicalEidolonRecipeAuditTest(unittest.TestCase):
    def test_clean_room_manifest_18_24_4(self):
        with zipfile.ZipFile(io.BytesIO(fake_jar())) as z:
            out=aud.scan(z)
        self.assertEqual((18,24,4,42),
            (len(out["normal_chants"]),len(out["ritual_recipes"]),
             len(out["conversion_dependencies"]),out["semantic_magic_roots"]))
        self.assertEqual(10,out["ritual_type_counts"]["eidolon_repraised:ritual_brazier"])
        self.assertEqual(11,out["ritual_type_counts"]["eidolon_repraised:ritual_brazier_summoning"])
        self.assertEqual(2,out["ritual_type_counts"]["eidolon_repraised:ritual_brazier_crafting"])
        self.assertEqual(1,out["ritual_type_counts"]["eidolon_repraised:ritual_brazier_location"])
        self.assertNotIn("undead_lure",out["normal_chants"])
        self.assertNotIn("basic_incense",out["normal_chants"])
    def test_default_one_count_may_be_omitted_but_triple_count_may_not(self):
        one=aud.RECIPE_ROOT+"rituals/summon_skeleton.json"
        with zipfile.ZipFile(io.BytesIO(fake_jar(override={one:{
             "type":"eidolon_repraised:ritual_brazier_summoning",
             "reagent":{"item":"minecraft:coal"},"pedestal_items":[],
             "output":"minecraft:skeleton"}}))) as z:
            self.assertEqual(42,aud.scan(z)["semantic_magic_roots"])
        triple=aud.RECIPE_ROOT+"rituals/summon_raven.json"
        with zipfile.ZipFile(io.BytesIO(fake_jar(override={triple:{
             "type":"eidolon_repraised:ritual_brazier_summoning",
             "reagent":{"item":"minecraft:coal"},"pedestal_items":[],
             "output":"eidolon_repraised:raven"}}))) as z:
            with self.assertRaisesRegex(aud.AuditError,"summon output/count mismatch"):
                aud.scan(z)

    def test_missing_summon_cannot_be_inferred_from_10_prototypes(self):
        with zipfile.ZipFile(io.BytesIO(fake_jar(missing=aud.RECIPE_ROOT+"rituals/summon_raven.json"))) as z:
            with self.assertRaisesRegex(aud.AuditError,"rituals identities mismatch"): aud.scan(z)
    def test_extra_chant_rejected(self):
        name=aud.RECIPE_ROOT+"unexpected.json"
        with zipfile.ZipFile(io.BytesIO(fake_jar(extra={name:{"type":"eidolon_repraised:chant","id":"eidolon_repraised:unexpected","signs":[]}}))) as z:
            with self.assertRaisesRegex(aud.AuditError,"unknown packaged chants identity"):aud.scan(z)
    def test_dummy_spell_not_promoted_to_chant(self):
        path=aud.RECIPE_ROOT+"basic_incense.json"
        with zipfile.ZipFile(io.BytesIO(fake_jar(extra={path:{"type":"eidolon_repraised:chant","id":"eidolon_repraised:basic_incense","signs":[]}}))) as z:
            with self.assertRaises(aud.AuditError):aud.scan(z)
    def test_wrong_chant_provider_id(self):
        path=aud.RECIPE_ROOT+"dark_prayer.json"
        value={"type":"eidolon_repraised:chant","id":"eidolon_repraised:wrong","signs":[{"sign":"eidolon_repraised:wicked"}]*3}
        with zipfile.ZipFile(io.BytesIO(fake_jar(override={path:value}))) as z:
            with self.assertRaisesRegex(aud.AuditError,"chant runtime ID/type mismatch"):aud.scan(z)
    def test_wrong_summon_entity_identity(self):
        path=aud.RECIPE_ROOT+"rituals/summon_raven.json"
        value={"type":"eidolon_repraised:ritual_brazier_summoning","reagent":{"item":"minecraft:coal"},
               "pedestal_items":[],"count":3,"output":"minecraft:raven"}
        with zipfile.ZipFile(io.BytesIO(fake_jar(override={path:value}))) as z:
            with self.assertRaisesRegex(aud.AuditError,"summon output/count mismatch"):aud.scan(z)
    def test_noninstalled_archive_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/aud.JAR_NAME
            p.write_bytes(fake_jar())
            self.assertNotEqual(hashlib.sha1(p.read_bytes()).hexdigest(),aud.SHA1)
            with self.assertRaisesRegex(aud.AuditError,"SHA-1"):aud.audit(p)

if __name__=="__main__":
    unittest.main()
