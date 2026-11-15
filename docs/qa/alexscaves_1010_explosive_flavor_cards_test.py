#!/usr/bin/env python3
"""Read-only Explosive Flavor static certificate and publisher identity gate.

The native gumball profile is replayed on the exact publisher JAR in CI.
These tests bind an individual enchantment to that already audited JVM graph,
without claiming a mutating hook, accepted damage, or physical gameplay QA.
"""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
import zipfile
from pathlib import Path

from alexscaves_1010_action_contract_audit import (
    load_manifest, validate_cards, validate_structure,
)

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314
SHOT = PREFIX + "server/item/ShotGumItem.class"
GUMBALL = PREFIX + "server/entity/item/GumballEntity.class"
REGISTRY = PREFIX + "server/enchantment/ACEnchantmentRegistry.class"
COMPAT = PREFIX + "server/misc/ACCompat.class"
ENCHANTMENT = "data/alexscaves/enchantment/explosive_flavor.json"
TAG = "data/alexscaves/tags/item/enchantable/shot_gum.json"
RESOURCE_SHAS = {
    ENCHANTMENT: "2da6cbf1a482c69cb268a65667a4b25ea402bc3d9c7b055ef2bd7e5d8f2d08e8",
    TAG: "3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d",
}
META = {
    "description": {"translate": "enchantment.alexscaves.explosive_flavor"},
    "supported_items": "#alexscaves:enchantable/shot_gum",
    "weight": 1, "max_level": 1,
    "min_cost": {"base": 1, "per_level_above_first": 16},
    "max_cost": {"base": 41, "per_level_above_first": 10},
    "anvil_cost": 8, "slots": ["mainhand"],
}


def unique_pairs(rows):
    result = {}
    for key, value in rows:
        if key in result:
            raise ValueError("duplicate publisher JSON key: " + key)
        result[key] = value
    return result


def method(manifest, owner, name):
    matches = [x for x in manifest["classes"][owner]["methods"] if x["name"] == name]
    if len(matches) != 1:
        raise ValueError("ambiguous or absent JVM method: " + owner + "." + name)
    return matches[0]


def pivot(manifest, owner, name, offset, opcode, fragment=""):
    matches = [x for x in method(manifest, owner, name)["anchors"] if x["offset"] == offset]
    if len(matches) != 1:
        raise ValueError("absent/duplicate JVM offset: " + name + "@" + str(offset))
    anchor = matches[0]
    if anchor["opcode"] != opcode or fragment not in (
        anchor["symbol"] + " " + anchor["operand"]
    ):
        raise ValueError("native causal pivot drift: " + name + "@" + str(offset))
    return anchor


def audit_publisher(jar: Path):
    """Verify physical class/resource bytes, publisher JSON, and token owners."""
    h1 = hashlib.sha1()
    h256 = hashlib.sha256()
    size = 0
    with jar.open("rb") as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(data)
            h1.update(data)
            h256.update(data)
    if (size, h1.hexdigest(), h256.hexdigest()) != (SIZE, SHA1, SHA256):
        raise ValueError("wrong publisher artifact, refusing individual seal")
    with zipfile.ZipFile(jar) as z:
        if len(z.namelist()) != len(set(z.namelist())):
            raise ValueError("duplicate ZIP members")
        seal = load_manifest(PROVIDER / "EXACT-EXPLOSIVE-FLAVOR-CAUSAL-1.0.10.json")
        for resource, expected in RESOURCE_SHAS.items():
            raw = z.read(resource)
            if hashlib.sha256(raw).hexdigest() != expected:
                raise ValueError("publisher resource mismatch: " + resource)
        meta = json.loads(z.read(ENCHANTMENT), object_pairs_hook=unique_pairs)
        tag = json.loads(z.read(TAG), object_pairs_hook=unique_pairs)
        if meta != META or "alexscaves:shot_gum" not in tag.get("values", []):
            raise ValueError("physical enchantment metadata or shot_gum tag drift")
        for owner, expected in seal["compiled_sha256"].items():
            if hashlib.sha256(z.read(owner)).hexdigest() != expected:
                raise ValueError("publisher class drift: " + owner)
        token_owners = sorted(
            name for name in z.namelist()
            if name.startswith(PREFIX) and name.endswith(".class")
            and b"EXPLOSIVE_FLAVOR" in z.read(name)
        )
        if not {REGISTRY, SHOT}.issubset(token_owners):
            raise ValueError("compiled EXPLOSIVE_FLAVOR owner not found")
    print("PUBLISHER_EXPLOSIVE_FLAVOR_1.0.10 VERIFIED_EXACT_BINARY")
    print("compiled_token_owners=" + json.dumps(token_owners))
    print("NO_MUTATION NOT_VERIFIED NOT_TESTED")


class ExplosiveFlavorStaticContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = load_manifest(PROVIDER / "EXACT-EXPLOSIVE-FLAVOR-CAUSAL-1.0.10.json")
        cls.m = load_manifest(PROVIDER / "EXACT-GUMBALL-CONTRACTS-1.0.10.json")
        validate_structure(cls.m, profile="gumball")
        validate_cards(cls.m, PROVIDER, profile="gumball")

    def check(self, owner, name, offset, opcode, fragment=""):
        return pivot(self.m, owner, name, offset, opcode, fragment)

    def test_scope_identity_and_binary_reuse(self):
        s, m = self.seal, self.m
        self.assertEqual(s["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(s["semantic_role"], "SHOT_GUM_GUMBALL_MODIFIER_NOT_NEW_CAST")
        self.assertEqual(s["enchantment"], "alexscaves:explosive_flavor")
        self.assertEqual(s["artifact"], {
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
        })
        self.assertEqual((m["artifact_sha1"], m["artifact_sha256"],
                          m["artifact_size_bytes"]), (SHA1, SHA256, SIZE))
        self.assertEqual(m["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual((m["mutating_hook"], m["physical_qa"]),
                         ("NOT_VERIFIED", "NOT_TESTED"))
        for key, digest in RESOURCE_SHAS.items():
            self.assertEqual(m["resources"][key], digest)
            self.assertEqual(s["resource_sha256"][key], digest)
        for key, digest in s["compiled_sha256"].items():
            self.assertEqual(m["classes"][key]["sha256"], digest)
        self.assertEqual(s["static_contract"]["mutation"], "NO_MUTATION")
        self.assertFalse(s["limits"]["provider_universe_closed"])
        self.assertEqual(s["limits"]["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(s["limits"]["physical_qa"], "NOT_TESTED")

    def test_registry_and_enchant_level_are_native(self):
        self.check(REGISTRY, "<clinit>", 455, "ldc_w", "explosive_flavor")
        self.check(REGISTRY, "<clinit>", 458, "invokestatic", "key:")
        self.check(REGISTRY, "<clinit>", 461, "putstatic", "EXPLOSIVE_FLAVOR:")
        self.check(COMPAT, "enchantLevel", 1, "invokevirtual", "ItemStack.getEnchantments:")
        self.check(COMPAT, "enchantLevel", 42, "invokeinterface", "Holder.is:")

    def test_positive_level_changes_one_native_loop_and_speed(self):
        for off, op, frag in (
            (83, "iconst_5", ""), (84, "if_icmpne", "553"),
            (89, "ifeq", "553"),
            (172, "getstatic", "EXPLOSIVE_FLAVOR:"),
            (175, "invokestatic", "ACCompat.enchantLevel:"),
            (178, "ifle", "185"), (181, "iconst_1", ""),
            (185, "iconst_0", ""), (186, "istore", "11"),
            (291, "iconst_0", ""), (294, "iload", "16"),
            (296, "iload", "11"), (298, "ifeq", "305"),
            (301, "iconst_1", ""), (305, "iconst_2", ""),
            (306, "if_icmpge", "518"),
            (448, "invokevirtual", "GumballEntity.setExplosive:"),
            (468, "ldc_w", "float 0.5f"),
            (474, "ldc_w", "float 1.5f"),
            (477, "ldc_w", "float 5.0f"),
            (480, "invokevirtual", "shootFromRotation:"),
            (492, "ldc_w", "float 4.0f"),
            (495, "invokevirtual", "setDamage:"),
            (499, "invokevirtual", "Level.isClientSide:"),
            (502, "ifne", "512"),
            (508, "invokevirtual", "Level.addFreshEntity:"),
            (512, "iinc", "16, 1"), (515, "goto", "294"),
        ):
            self.check(SHOT, "acInventoryTick", off, op, frag)
        self.assertEqual(self.seal["static_contract"]["primary_gumball_attempts_explosive"], 1)
        self.assertEqual(self.seal["static_contract"]["primary_gumball_attempts_baseline"], 2)
        self.assertEqual(self.seal["static_contract"]["initial_hit_damage_request"], 4)

    def test_ammo_debit_and_bouncy_limit_remain_independent(self):
        for off, op, frag in (
            (188, "iconst_4", ""), (190, "getstatic", "BOUNCY_BALL:"),
            (196, "iconst_2", ""), (197, "imul", ""), (198, "iadd", ""),
            (518, "aload_3", ""), (533, "invokevirtual", "Player.isCreative:"),
            (539, "aload_1", ""), (544, "iconst_1", ""),
            (545, "isub", ""), (547, "invokestatic", "Math.max:"),
            (550, "invokestatic", "setGumballsLeft:"),
        ):
            self.check(SHOT, "acInventoryTick", off, op, frag)
        self.assertLess(508, 518)
        self.check(SHOT, "use", 66, "iconst_1")
        self.check(SHOT, "use", 67, "invokevirtual", "ItemStack.shrink:")
        self.check(SHOT, "use", 80, "iconst_4")
        self.check(SHOT, "use", 81, "invokestatic", "setGumballsLeft:")

    def test_explosive_stop_requires_bounce_gate(self):
        for off, op, frag in (
            (3, "invokevirtual", "getBounces:"),
            (7, "invokevirtual", "getMaximumBounces:"),
            (10, "iconst_1", ""), (11, "isub", ""),
            (12, "if_icmple", "38"),
            (16, "invokevirtual", "isExplosive:"),
            (19, "ifeq", "38"),
            (23, "getstatic", "Vec3.ZERO:"),
            (26, "invokevirtual", "setDeltaMovement:"),
            (34, "invokevirtual", "setBounces:"),
            (37, "return", ""),
        ):
            self.check(GUMBALL, "bounceFromDirection", off, op, frag)

    def test_explosion_is_server_only_and_deferred(self):
        for off, op, frag in (
            (176, "invokevirtual", "isExplosive:"),
            (179, "ifeq", "294"),
            (183, "invokevirtual", "getBounces:"),
            (187, "invokevirtual", "getMaximumBounces:"),
            (190, "if_icmplt", "294"),
            (197, "ldc", "float 20.0f"),
            (200, "ifle", "253"),
            (207, "invokevirtual", "Level.isClientSide:"),
            (210, "ifne", "263"),
            (218, "invokevirtual", "getOwner:"),
            (229, "ldc2_w", "double 0.5d"),
            (237, "fconst_2", ""),
            (238, "iconst_0", ""),
            (239, "getstatic", "ExplosionInteraction.NONE:"),
            (242, "invokevirtual", "Level.explode:"),
            (247, "invokevirtual", "discard:"),
            (255, "getfield", "explodeProgress:"),
            (258, "fconst_1", ""), (259, "fadd", ""),
            (260, "putfield", "explodeProgress:"),
        ):
            self.check(GUMBALL, "tick", off, op, frag)
        self.assertEqual(self.seal["static_contract"]["explosion_gate"],
                         "isExplosive AND getBounces()>=getMaximumBounces() AND explodeProgress>20F")

    def test_split_children_do_not_certify_owner_or_additional_casts(self):
        for off, op, frag in (
            (139, "invokevirtual", "Entity.hurt:"),
            (142, "pop", ""),
            (143, "aload_0", ""),
            (147, "ifeq", "349"),
            (155, "iconst_3", ""), (156, "if_icmpge", "345"),
            (174, "invokestatic", "ACCompat.createEntity:"),
            (223, "invokevirtual", "isExplosive:"),
            (229, "ldc2_w", "double 0.699999988079071d"),
            (235, "ldc2_w", "double 1.5d"),
            (289, "iconst_0", ""), (290, "invokevirtual", "setSplitsOnHit:"),
            (299, "invokevirtual", "setDamage:"),
            (317, "invokevirtual", "setExplosive:"),
            (326, "invokevirtual", "setMaximumBounces:"),
            (335, "invokevirtual", "Level.addFreshEntity:"),
            (345, "aload_0", ""), (346, "invokevirtual", "discard:"),
        ):
            self.check(GUMBALL, "onHitEntity", off, op, frag)
        source = method(self.m, GUMBALL, "onHitEntity")["anchors"]
        self.assertFalse(any("setOwner:" in row["symbol"] for row in source))

    def test_entity_synced_flag_does_not_prove_nbt_restore(self):
        self.check(GUMBALL, "defineSynchedData", 73, "getstatic", "EXPLOSIVE:")
        self.check(GUMBALL, "defineSynchedData", 76, "iconst_0")
        for method_name, native in (("addAdditionalSaveData", "CompoundTag.putInt:"),
                                    ("readAdditionalSaveData", "setColor:")):
            rows = method(self.m, GUMBALL, method_name)["anchors"]
            self.assertEqual(
                {x["symbol"] for x in rows if x["symbol"].startswith("String ")},
                {"String Color"}
            )
            self.assertTrue(any(native in x["symbol"] for x in rows))
            self.assertFalse(any("EXPLOSIVE" in x["symbol"] for x in rows))

    def test_negative_pivot_drift_rejected(self):
        altered = json.loads(json.dumps(self.m))
        point = next(a for a in method(altered, SHOT, "acInventoryTick")["anchors"]
                     if a["offset"] == 298)
        point["opcode"] = "ifne"
        with self.assertRaisesRegex(ValueError, "native causal pivot drift"):
            pivot(altered, SHOT, "acInventoryTick", 298, "ifeq", "305")
        with self.assertRaisesRegex(ValueError, "duplicate publisher JSON"):
            json.loads('{"max_level":1,"max_level":2}', object_pairs_hook=unique_pairs)
        altered = json.loads(json.dumps(self.m))
        point = next(a for a in method(altered, GUMBALL, "tick")["anchors"]
                     if a["offset"] == 242)
        point["symbol"] = "Method no.explode:"
        with self.assertRaisesRegex(ValueError, "native causal pivot drift"):
            pivot(altered, GUMBALL, "tick", 242, "invokevirtual", "Level.explode:")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--jar":
        audit_publisher(Path(sys.argv[2]))
    else:
        unittest.main()
