#!/usr/bin/env python3
"""SHA-exact fail-closed Rainbounce Boots native discovery verifier.

Pins unmodified report hash, complete item owner, typed class consumers,
material registry identity, 5 JSON resource hashes and causal bytecode
anchors. Does NOT certify an executable perk, hook, engine effects or QA.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/RainbounceBootsItem"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314


def unique_pairs(pairs):
    result = {}
    for key, val in pairs:
        assert key not in result, "duplicate JSON key: " + key
        result[key] = val
    return result


def read(path: Path, maximum: int):
    raw = path.read_bytes()
    assert 0 < len(raw) <= maximum, "unexpected report size"
    return json.loads(raw, object_pairs_hook=unique_pairs), hashlib.sha256(raw).hexdigest()


def seal_method(method):
    d = method["declaration"]
    return {
        "name": d["name"], "descriptor": d["descriptor"],
        "instruction_count": method["instruction_count"],
        "instruction_sha256": method["instruction_sha256"],
    }


def opcode_text(method):
    return " ".join(
        row["opcode"] + " " + row["operand"] + " " + row["symbol"]
        for row in method["instructions"]
    )


def check(path: Path, manifest: Path) -> None:
    d, d_hash = read(path, 16_000_000)
    m, _ = read(manifest, 100_000)
    assert d_hash == m["report"]["sha256"], "publisher evidence hash drift"
    assert d["schema_version"] == m["schema_version"] == 1
    assert d["scope"] == m["scope"] == "RAINBOUNCE_BOOTS_NATIVE_DISCOVERY_NOT_CERTIFIED"
    expected_artifact = {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
        "size_bytes": SIZE, "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert d["artifact"] == m["artifact"] == expected_artifact
    assert d["owner"] == m["owner"] == OWNER
    assert d["registry_candidate_not_individually_certified"] == "rainbounce_boots"
    assert d["source_revision_parity"] == "NOT_ASSUMED"
    for key, expected in (
        ("other_consumers_complete", False),
        ("provider_universe_closed", False),
        ("static_contract", "NOT_CERTIFIED"),
        ("semantic_magic_roots_certified_delta", 0),
        ("mutating_hook", "NOT_VERIFIED"),
        ("physical_qa", "NOT_TESTED"),
        ("mutation", "NO_MUTATION"),
    ):
        assert d[key] == expected, key

    assert m["limits"] == {
        "status": "PARTIAL", "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION", "provider_universe_closed": False,
        "other_consumers_complete": False, "magic_roots_added": 0,
        "engine_movement_effectiveness": "NOT_VERIFIED",
        "mixin_injection_runtime_application": "NOT_VERIFIED",
    }
    assert m["static_behavior"] == {
        "registry_item": "alexscaves:rainbounce_boots",
        "registry_factory": "ACItemRegistry.lambda$static$174",
        "registered_armor_type": "BOOTS",
        "required_equipment_slot": "FEET",
        "callback": "EntityMixin.ac_move",
        "effect_method": "RainbounceBootsItem.onEntityLand",
        "minimum_abs_fall_displacement_exclusive": 0.2,
        "strong_bounce_boundary_exclusive": 0.42,
        "weak_bounce_multiplier": 0.7,
        "strong_bounce_multiplier": 1.05,
        "tag_reduced_bounce_multiplier": 0.15000000596046448,
        "has_sugar_rush_horizontal_factor": 1.2,
        "no_sugar_rush_horizontal_factor": 1.9,
        "player_world_side_guarantee": "NOT_VERIFIED",
        "no_new_magic_cast": True,
    }

    native = d["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    owner = native["targets"][OWNER]
    spec = m["native_class"]
    assert owner["class_sha256"] == spec["sha256"]
    assert owner["hierarchy"]["parent"] == spec["parent"]
    assert owner["hierarchy"]["interfaces"] == spec["interfaces"]
    assert not owner["in_jar_ancestors"]
    assert len(owner["fields"]) == spec["fields"] == 0
    assert len(owner["declarations"]) == spec["declarations"] == 4
    assert len(owner["methods"]) == spec["code_methods"] == 4
    assert len(owner["methods"]) == sum(
        "code_sha256" in value for value in owner["declarations"]
    )
    assert len(owner["consumers"]) == spec["typed_consumer_owners"] == 4
    assert [seal_method(x) for x in owner["methods"]] == spec["methods"]
    for method in owner["methods"]:
        assert method["instruction_count"] == len(method["instructions"])

    assert set(owner["consumers"]) == set(m["consumers"])
    for cname, record in m["consumers"].items():
        actual = owner["consumers"][cname]
        assert actual["class_sha256"] == record["class_sha256"], cname
        assert len(actual["sites"]) == record["sites"], cname
        assert [seal_method(x) for x in actual["bodies"]] == record["methods"], cname

    assert d["filename_matched_resource_hashes"] == m["resources"]
    assert len(m["resources"]) == 5
    for name, record in m["resources"].items():
        assert name.endswith(".json") and "rainbounce" in name.lower()
        assert set(record) == {"sha256", "size"}
        assert len(record["sha256"]) == 64
        assert type(record["size"]) is int and record["size"] > 0

    own = {x["declaration"]["name"]: opcode_text(x) for x in owner["methods"]}
    assert "rainbounce_boots.png" in own["getArmorTexture"]
    callback = own["onEntityLand"]
    for marker in (
        "Vec3.y", "Math.abs", "double 0.42d", "float 1.05f",
        "float 0.7f", "isSuppressingBounce", "float 0.2f",
        "getOnPosLegacy", "REDUCE_RAINBOUNCE_BOOTS_EFFECT_ON",
        "0.15000000596046448d", "SUGAR_RUSH", "float 1.2f",
        "float 1.9f", "Vec3.multiply", "Vec3.add",
        "setDeltaMovement", "fallDistance", "RAINBOUNCE_BOOTS_BOUNCE",
        "PLAYER_RAINBOW", "ParticleTypes.CLOUD", "RandomSource.nextInt",
        "RandomSource.nextFloat", "addParticle",
    ):
        assert marker in callback, ("Rainbounce.onEntityLand", marker)

    caller = owner["consumers"][
        "com/github/alexmodguy/alexscaves/mixin/EntityMixin"]["bodies"][0]
    call_text = opcode_text(caller)
    for marker in ("LivingEntity", "EquipmentSlot.FEET", "RAINBOUNCE_BOOTS",
                   "ItemStack.is", "RainbounceBootsItem.onEntityLand"):
        assert marker in call_text, ("EntityMixin.ac_move", marker)
    reg = owner["consumers"][
        "com/github/alexmodguy/alexscaves/server/item/ACItemRegistry"]["bodies"][0]
    reg_text = opcode_text(reg)
    for marker in ("RAINBOUNCE_ARMOR_MATERIAL", "ArmorItem$Type.BOOTS",
                   "RainbounceBootsItem"):
        assert marker in reg_text, ("ACItemRegistry.lambda$static$174", marker)

    print("PASS: exact Rainbounce owner, EntityMixin and render consumers, "
          "resource SHA256 census; STATIC_DISCOVERY_ONLY NO_MUTATION")
    print("REPORT_SHA256", d_hash)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()
    check(args.report, args.manifest)
