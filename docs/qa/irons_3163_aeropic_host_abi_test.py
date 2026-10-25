#!/usr/bin/env python3
"""Synthetic fail-closed cases: publisher hash/identity vs compiled recast ABI."""
import unittest

import irons_3163_aeropic_host_abi as host

def publisher():
    return {
        "id":host.VERSION_ID,"project_id":host.PROJECT_ID,
        "version_number":host.HOST_VERSION,
        "game_versions":["1.21.1"],"loaders":["neoforge"],
        "files":[{"filename":host.HOST_NAME,
                  "url":host.OFFICIAL_URL,
                  "size":host.EXPECTED_BYTES,
                  "primary":True,
                  "hashes":{"sha1":"a"*40,"sha512":"b"*128}}]
    }

def signatures(name:str):
    if name=="abstract_spell":
        return """public class io.redspace.ironsspellbooks.api.spells.AbstractSpell {
  public int getRecastCount(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)I
}"""
    if name=="player_recasts":
        return """public class io.redspace.ironsspellbooks.capabilities.magic.PlayerRecasts {
  public boolean addRecast(io.redspace.ironsspellbooks.capabilities.magic.RecastInstance, io.redspace.ironsspellbooks.api.magic.MagicData);
    descriptor: (Lio/redspace/ironsspellbooks/capabilities/magic/RecastInstance;Lio/redspace/ironsspellbooks/api/magic/MagicData;)Z
  public boolean hasRecastForSpell(java.lang.String);
    descriptor: (Ljava/lang/String;)Z
  public void decrementRecastCount(java.lang.String);
    descriptor: (Ljava/lang/String;)V
}"""
    if name=="recast_instance":
        return """public class io.redspace.ironsspellbooks.capabilities.magic.RecastInstance {
  public io.redspace.ironsspellbooks.capabilities.magic.RecastInstance(java.lang.String, int, int, int, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.spells.ICastDataSerializable);
    descriptor: (Ljava/lang/String;IIILio/redspace/ironsspellbooks/api/spells/CastSource;Lio/redspace/ironsspellbooks/api/spells/ICastDataSerializable;)V
}"""
    return """public class io.redspace.ironsspellbooks.api.magic.MagicData {
  public void doSomething();
    descriptor: ()V
}"""

class HostAbiTests(unittest.TestCase):
    def test_metadata_authoritative_sha(self):
        data=host.validate_publisher_metadata(publisher())
        self.assertEqual("b"*128,data["sha512"])
    def test_wrong_mod_project_rejected(self):
        d=publisher();d["project_id"]="other"
        with self.assertRaises(host.EvidenceError):host.validate_publisher_metadata(d)
    def test_wrong_release_rejected(self):
        d=publisher();d["version_number"]="1.20.1-3.16.3"
        with self.assertRaises(host.EvidenceError):host.validate_publisher_metadata(d)
    def test_wrong_file_url_rejected(self):
        d=publisher();d["files"][0]["url"]="https://example.org/fake.jar"
        with self.assertRaises(host.EvidenceError):host.validate_publisher_metadata(d)
    def test_wrong_size_rejected(self):
        d=publisher();d["files"][0]["size"]=host.EXPECTED_BYTES+1
        with self.assertRaises(host.EvidenceError):host.validate_publisher_metadata(d)
    def test_missing_sha512_rejected(self):
        d=publisher();d["files"][0]["hashes"].pop("sha512")
        with self.assertRaises(host.EvidenceError):host.validate_publisher_metadata(d)
    def test_duplicate_file_rejected(self):
        d=publisher();d["files"].append(d["files"][0].copy())
        with self.assertRaises(host.EvidenceError):host.validate_publisher_metadata(d)
    def test_host_recast_abi(self):
        x=host.declarations(signatures("abstract_spell"),"abstract_spell")
        self.assertEqual("(ILnet/minecraft/world/entity/LivingEntity;)I",x["getRecastCount"]["descriptor"])
    def test_recast_capability_three_calls(self):
        self.assertEqual(3,len(host.declarations(signatures("player_recasts"),"player_recasts")))
    def test_host_recast_instance_ctor(self):
        self.assertIn("<init>",host.declarations(signatures("recast_instance"),"recast_instance"))
    def test_bare_constructor_name_equivalent(self):
        cls=host.NEEDED["recast_instance"]
        text=signatures("recast_instance").replace(
            "public "+cls+"(", "public RecastInstance(")
        self.assertIn("<init>",host.declarations(text,"recast_instance"))

    def test_static_recast_getter_rejected(self):
        s=signatures("abstract_spell").replace("public int getRecastCount","public static int getRecastCount")
        with self.assertRaises(host.EvidenceError):host.declarations(s,"abstract_spell")
    def test_abstract_recast_getter_rejected(self):
        s=signatures("abstract_spell").replace("public int getRecastCount","public abstract int getRecastCount")
        with self.assertRaises(host.EvidenceError):host.declarations(s,"abstract_spell")
    def test_wrong_descriptor_rejected(self):
        s=signatures("abstract_spell").replace("(ILnet/minecraft/world/entity/LivingEntity;)I","(I)I")
        with self.assertRaises(host.EvidenceError):host.declarations(s,"abstract_spell")
    def test_missing_method_rejected(self):
        s=signatures("player_recasts").replace("decrementRecastCount","anotherMethod")
        with self.assertRaises(host.EvidenceError):host.declarations(s,"player_recasts")
    def test_ambiguous_overload_rejected(self):
        s=signatures("abstract_spell").replace("}","  public int getRecastCount(int);\n    descriptor: (I)I\n}")
        with self.assertRaises(host.EvidenceError):host.declarations(s,"abstract_spell")

if __name__=="__main__":
    unittest.main()
