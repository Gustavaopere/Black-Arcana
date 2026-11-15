#!/usr/bin/env python3
"""Fail-closed static Enveloping Bubble 1.0.10 causal crosswalk.

Reuses SHA-exact publisher manifests; does not add a cast, hook or physical QA.
The CI workflow independently replays all three manifests against JAR 8856293.
"""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from alexscaves_1010_action_contract_audit import (
    load_manifest, validate_cards, validate_structure,
)

REPO = Path(__file__).resolve().parents[2]
PROVIDER = REPO / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
RESOURCE = "data/alexscaves/enchantment/enveloping_bubble.json"
TAG = "data/alexscaves/tags/item/enchantable/sea_staff.json"
SEA = PREFIX + "server/item/SeaStaffItem.class"
BOLT = PREFIX + "server/entity/item/WaterBoltEntity.class"
REGISTRY = PREFIX + "server/enchantment/ACEnchantmentRegistry.class"


def method(manifest, owner, name):
    matched = [m for m in manifest["classes"][owner]["methods"] if m["name"] == name]
    if len(matched) != 1:
        raise ValueError("missing/ambiguous exact owner method: " + owner + "." + name)
    return matched[0]


def anchor(manifest, owner, name, offset, *, opcode, fragment=""):
    m = method(manifest, owner, name)
    matched = [a for a in m["anchors"] if a["offset"] == offset]
    if len(matched) != 1:
        raise ValueError("missing/duplicate native anchor: " + name + "@" + str(offset))
    row = matched[0]
    if row["opcode"] != opcode or fragment not in (row["operand"] + " " + row["symbol"]):
        raise ValueError("native causal anchor drift: " + name + "@" + str(offset))
    return row


class EnvelopingBubbleStaticContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((PROVIDER / "EXACT-ENVELOPING-BUBBLE-CAUSAL-1.0.10.json").read_text(encoding="utf8"))
        cls.manifests = {}
        for name, profile in (("actions", "actions"), ("triple", "triple_splash"),
                              ("effects", "effects")):
            filename = {
                "actions": "EXACT-TECHNICAL-CONTRACTS-1.0.10.json",
                "triple": "EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.json",
                "effects": "EXACT-EFFECT-CONTRACTS-1.0.10.json",
            }[name]
            m = load_manifest(PROVIDER / filename)
            validate_structure(m, profile=profile)
            validate_cards(m, PROVIDER, profile=profile)
            cls.manifests[name] = m

    def test_identity_reuses_three_exact_publisher_scopes(self):
        s = self.seal
        self.assertEqual(s["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["enchantment"], "alexscaves:enveloping_bubble")
        self.assertEqual(s["semantic_role"], "SEA_STAFF_WATER_BOLT_MODIFIER_NOT_NEW_CAST")
        self.assertEqual(s["artifact"], {"sha1": SHA1, "sha256": SHA256, "size_bytes": 75279314})
        for m in self.manifests.values():
            self.assertEqual((m["artifact_sha1"], m["artifact_sha256"]), (SHA1, SHA256))
            self.assertEqual(m["mutating_hook"], "NOT_VERIFIED")
            self.assertEqual(m["physical_qa"], "NOT_TESTED")
        actions, triple = self.manifests["actions"], self.manifests["triple"]
        self.assertEqual(actions["resources"][RESOURCE], s["resource_sha256"][RESOURCE])
        self.assertEqual(actions["resources"][TAG], s["resource_sha256"][TAG])
        self.assertEqual(triple["resources"][TAG], s["resource_sha256"][TAG])
        for owner, digest in s["compiled_sha256"].items():
            self.assertEqual(triple["classes"][owner]["sha256"], digest)
        effect_names = set(self.manifests["effects"]["classes"])
        self.assertIn(PREFIX + "server/potion/BubbledEffect.class", effect_names)
        self.assertIn("tick", [m["name"] for m in
                              self.manifests["effects"]["classes"][
                                  PREFIX + "server/potion/BubbledEffect.class"]["methods"]])
        self.assertEqual(s["limits"]["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(s["limits"]["physical_qa"], "NOT_TESTED")
        self.assertEqual(s["limits"]["provider_universe_closed"], False)

    def test_rng_is_once_per_native_bolt_in_server_spawn_loop(self):
        m = self.manifests["triple"]
        anchor(m, SEA, "use", 75, opcode="invokevirtual", fragment="Level.isClientSide:")
        anchor(m, SEA, "use", 78, opcode="ifne", fragment="355")
        anchor(m, SEA, "use", 97, opcode="getstatic", fragment="TRIPLE_SPLASH")
        anchor(m, SEA, "use", 100, opcode="invokestatic", fragment="ACCompat.enchantLevel")
        anchor(m, SEA, "use", 116, opcode="iload", fragment="10")
        anchor(m, SEA, "use", 274, opcode="getstatic", fragment="ENVELOPING_BUBBLE")
        anchor(m, SEA, "use", 277, opcode="invokestatic", fragment="ACCompat.enchantLevel")
        anchor(m, SEA, "use", 280, opcode="ifle", fragment="297")
        anchor(m, SEA, "use", 289, opcode="invokeinterface", fragment="RandomSource.nextBoolean")
        anchor(m, SEA, "use", 294, opcode="invokevirtual", fragment="setBubbling:")
        anchor(m, SEA, "use", 345, opcode="invokevirtual", fragment="Level.addFreshEntity:")
        anchor(m, SEA, "use", 349, opcode="iinc", fragment="10, 1")
        anchor(m, SEA, "use", 352, opcode="goto", fragment="116")
        anchor(m, SEA, "use", 381, opcode="invokestatic", fragment="ACCompat.hurtAndBreak")
        self.assertLess(116, 274)
        self.assertLess(294, 345)
        self.assertLess(345, 381)
        anchor(m, PREFIX + "server/misc/ACCompat.class", "enchantLevel",
               42, opcode="invokeinterface", fragment="Holder.is:")
        anchor(m, PREFIX + "server/misc/ACCompat.class", "enchantLevel",
               51, opcode="invokeinterface", fragment="getIntValue:")

    def test_damage_accepted_before_status_request_and_packet_not_accepted_effect(self):
        m = self.manifests["triple"]
        anchor(m, BOLT, "damageMobs", 27, opcode="invokevirtual", fragment="mobProjectile:")
        for offset in (35, 38, 41):
            anchor(m, BOLT, "damageMobs", offset, opcode="ldc2_w", fragment="double 2.0d")
        anchor(m, BOLT, "damageMobs", 101, opcode="instanceof", fragment="DeepOneBaseEntity")
        for offset in (96, 104, 117, 126):
            anchor(m, BOLT, "damageMobs", offset, opcode="ifne", fragment="216")
        anchor(m, BOLT, "damageMobs", 136, opcode="ldc_w", fragment="float 3.0f")
        anchor(m, BOLT, "damageMobs", 139, opcode="invokestatic", fragment="ACCompat.hurt:")
        anchor(m, BOLT, "damageMobs", 142, opcode="ifeq", fragment="216")
        anchor(m, BOLT, "damageMobs", 146, opcode="invokevirtual", fragment="isBubbling:")
        anchor(m, BOLT, "damageMobs", 149, opcode="ifeq", fragment="216")
        anchor(m, BOLT, "damageMobs", 172, opcode="sipush", fragment="200")
        anchor(m, BOLT, "damageMobs", 178, opcode="invokevirtual", fragment="LivingEntity.addEffect:")
        anchor(m, BOLT, "damageMobs", 181, opcode="pop")
        anchor(m, BOLT, "damageMobs", 213, opcode="invokestatic", fragment="sendMSGToAll:")
        self.assertEqual(self.seal["static_contract"]["debff_duration_ticks"], 200)

    def test_sync_nbt_and_child_copy_are_downstream_of_same_cast(self):
        m = self.manifests["triple"]
        for name in ("setBubbling", "isBubbling", "readAdditionalSaveData",
                     "addAdditionalSaveData"):
            self.assertIn(name, [x["name"] for x in m["classes"][BOLT]["methods"]])
        anchor(m, BOLT, "onRicochetHit", 254, opcode="invokevirtual", fragment="isBubbling:")
        anchor(m, BOLT, "onRicochetHit", 257, opcode="invokevirtual", fragment="setBubbling:")
        anchor(m, BOLT, "readAdditionalSaveData", 8, opcode="invokevirtual", fragment="setBubbling:")
        anchor(m, BOLT, "addAdditionalSaveData", 8, opcode="invokevirtual", fragment="CompoundTag.putBoolean:")
        self.assertEqual(self.seal["limits"]["multiplayer_packet_authorization"], "NOT_VERIFIED")
        self.assertEqual(self.seal["static_contract"]["mutation"], "NO_MUTATION")

    def test_negative_causal_mutation_fails_closed(self):
        m = copy.deepcopy(self.manifests["triple"])
        self.assertIn("ENVELOPING_BUBBLE",
                      anchor(m, SEA, "use", 274, opcode="getstatic")["symbol"])
        a = method(m, SEA, "use")["anchors"]
        next(x for x in a if x["offset"] == 280)["opcode"] = "ifgt"
        with self.assertRaisesRegex(ValueError, "causal anchor drift"):
            anchor(m, SEA, "use", 280, opcode="ifle", fragment="297")


if __name__ == "__main__":
    unittest.main()
