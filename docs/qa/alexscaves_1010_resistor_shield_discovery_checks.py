#!/usr/bin/env python3
"""Fail-closed identity/structure gate for read-only ResistorShieldItem census.

This gate is a preliminary discovery test, not a SHA-pinned per-object
static certificate. A subsequent per-method manifestation is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314
TERMS = ("resistor_shield", "resistor", "resistance_shield")

OWNER_CLASS_SHA256 = "ffd3fddd74f8d44049886e9013de2e3d67cbd2a721015369175e8442c5044741"
PARENT = "net/minecraft/world/item/ShieldItem"
DIRECT_INTERFACES = {
    "com/github/alexmodguy/alexscaves/server/item/ACClientExtensionItem",
    "com/github/alexmodguy/alexscaves/server/item/ACEnchantableItem",
    "com/github/alexmodguy/alexscaves/server/item/ACRepairableItem",
    "com/github/alexmodguy/alexscaves/server/item/ACTickingItem",
}
OTHER_PINNED_METHODS = {
    ("acInventoryTick", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V"): (
        79, "3cec5ec860390c581f2795f6c2f128c2c1507593934eb6b40db608bf6d182b20",
    ),
    ("acExtraRepairMaterials", "()[Lnet/minecraft/world/item/Item;"): (
        15, "b1c165d8b02b3531e59afa61434eb1da01506822154ef3a4d9db9cc34f60812e",
    ),
    ("isValidRepairItem", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;)Z"): (
        13, "56ef4089abe5ca807759ea066eaab7be291dd520d357c2fab2a6de913f3fa597",
    ),
    ("initializeClient", "(Ljava/util/function/Consumer;)V"): (
        6, "3a6c2d33865c1d1707dcbd93e1f9e0bd3bd706c9817ddb988b4e0589ebb14cf4",
    ),
}

PINNED_INTERFACE_METHODS = {
    ("getEnchantmentValue", "()I"): (
        2, "d943c5fe0bd38038ce70963c73b8759ba3d76c8c00d31c1a2141268dc4e0ee0a",
        "95ef737cd8a13db65e3eb3c18e8816a5179dcbdf341309522ab00e95d5aae6d2",
    ),
    ("isEnchantable", "(Lnet/minecraft/world/item/ItemStack;)Z"): (
        8, "9cd84b0255be269f2bf50fce0095c14fa5d484831fd35063e71f4c9814aa6b4f",
        "c1c39189ff601291bec7533e758094d6e935147c1308db53adfe374b3a117a58",
    ),
}


def unique(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, ("duplicate JSON key", key)
        out[key] = value
    return out


def check(path: Path, partial_manifest_path: Path) -> None:
    seal_raw = partial_manifest_path.read_bytes()
    assert 0 < len(seal_raw) <= 100_000, "partial manifest bounds"
    seal = json.loads(seal_raw, object_pairs_hook=unique)
    assert seal["schema_version"] == 1
    assert seal["scope"] == "RESISTOR_SHIELD_PARTIAL_IDENTITY_AND_ENCHANTABILITY_ONLY"
    assert seal["owner"]["name"] == OWNER
    assert seal["artifact"] == {
        "mod_id": "alexscaves",
        "version": "1.0.10",
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
        "minecraft": "1.21.1", "java": 21,
        "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert seal["owner"]["class_sha256"] == OWNER_CLASS_SHA256
    assert seal["owner"]["parent"] == PARENT
    assert set(seal["owner"]["declared_interfaces"]) == DIRECT_INTERFACES
    assert set(seal["states"]) == {
        "catalog", "static_contract", "mutating_hook", "physical_qa",
        "mutation", "provider_universe_closed", "semantic_magic_roots_delta",
    }
    assert seal["states"] == {
        "catalog": "PARTIAL", "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION", "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }
    assert seal["prior_native_evidence"]["sha256"] == (
        "d34a655d06d65a771ea9237ef222635e159ffcfa6fe8b454ee6826ee14979e73"
    )
    assert seal["prior_native_evidence"]["size_bytes"] == 97832
    assert seal["item_registry"]["resource_id"] == "alexscaves:resistor_shield"
    assert seal["item_registry"]["field"] == "ACItemRegistry.RESISTOR_SHIELD"
    assert seal["item_registry"]["factory"] == "lambda$static$20"
    assert seal["item_registry"]["factory_code_sha256"] == (
        "6be6cb4de8570768436590ecdd12cfd11e44f1c9b8e76b7eb58a324d6b4d63ce"
    )
    assert seal["item_registry"]["factory_instruction_sha256"] == (
        "d5746049d40ac0bafdb3b78aac9a4134cba1f81838a06bb5866b30c3143402bc"
    )
    assert seal["item_registry"]["factory_instruction_count"] == 4
    assert seal["owner"]["full_method_census"] == "PENDING_NEW_DISCOVERY"
    assert seal["contract_axes"]["targeting"] == "NOT_VERIFIED"
    assert seal["contract_axes"]["costs"] == "NOT_VERIFIED"
    assert seal["resource_observation"]["paths_and_semantics"] == "NOT_VERIFIED"

    raw = path.read_bytes()
    assert 0 < len(raw) <= 16_000_000, "report bounds"
    a = json.loads(raw, object_pairs_hook=unique)
    assert a["schema_version"] == 1
    assert a["scope"] == "RESISTOR_SHIELD_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert a["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
        "size_bytes": SIZE, "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert a["owner"] == OWNER
    for key, expected in {
        "resource_census_limit": "FILENAME_MATCHES_ONLY",
        "registry_identity": "NOT_PROVEN_BY_FILENAME_ONLY",
        "typed_consumer_scan": "PUBLISHER_CLASSFILES_ONLY",
        "other_consumers_complete": False,
        "source_revision_parity": "NOT_ASSUMED",
        "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED",
        "semantic_magic_roots_certified_delta": 0,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }.items():
        assert a[key] == expected, key
    native = a["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    cls = native["targets"][OWNER]
    assert cls["class_sha256"] == OWNER_CLASS_SHA256
    assert cls["hierarchy"]["parent"] == PARENT
    assert set(cls["hierarchy"]["interfaces"]) == DIRECT_INTERFACES
    m_methods = seal["owner"]["selected_methods"]
    assert len(m_methods) == len(PINNED_INTERFACE_METHODS) == 2
    expected_in_manifest = {
        (x["name"], x["descriptor"]):
        (x["instruction_count"], x["instruction_sha256"], x["code_sha256"])
        for x in m_methods
    }
    assert expected_in_manifest == PINNED_INTERFACE_METHODS
    support_rows = seal["owner"]["support_callbacks"]
    assert len(support_rows) == len(OTHER_PINNED_METHODS) == 4
    support_fingerprints = {
        (m["name"], m["descriptor"]):
        (m["instruction_count"], m["instruction_sha256"])
        for m in support_rows
    }
    assert support_fingerprints == OTHER_PINNED_METHODS
    fingerprint = {
        (x["declaration"]["name"], x["declaration"]["descriptor"]): (
            x["instruction_count"], x["instruction_sha256"],
            x["declaration"]["code_sha256"],
        )
        for x in cls["methods"]
    }
    for identity, (count, sha) in OTHER_PINNED_METHODS.items():
        assert identity in fingerprint
        assert fingerprint[identity][:2] == (count, sha), (
            "known support callback SHA drift", identity
        )
    presentation = next(m for m in support_rows if m["name"] == "initializeClient")
    assert presentation["code_sha256"] == (
        "ab25a13fc141e9c68e695fdce843d4563c474d551d77359cefa387da179e2a9a"
    )
    assert fingerprint[("initializeClient", "(Ljava/util/function/Consumer;)V")][2] == (
        presentation["code_sha256"]
    )
    assert next(m for m in support_rows if m["name"] == "acExtraRepairMaterials")[
        "referenced_registry_fields"
    ] == ["SCARLET_NEODYMIUM_INGOT", "AZURE_NEODYMIUM_INGOT"]
    registry = cls["consumers"].get(
        "com/github/alexmodguy/alexscaves/server/item/ACItemRegistry"
    )
    assert registry is not None
    factory_codes = [
        m["declaration"]["code_sha256"] for m in registry["bodies"]
        if m["declaration"]["name"] == "lambda$static$20"
        and m["declaration"]["descriptor"] == "()Lnet/minecraft/world/item/Item;"
    ]
    assert factory_codes == [seal["item_registry"]["factory_code_sha256"]], (
        "typed registry factory SHA drift"
    )
    factory_fingerprints = [
        (m["instruction_count"], m["instruction_sha256"])
        for m in registry["bodies"]
        if m["declaration"]["name"] == "lambda$static$20"
        and m["declaration"]["descriptor"] == "()Lnet/minecraft/world/item/Item;"
    ]
    assert factory_fingerprints == [(
        seal["item_registry"]["factory_instruction_count"],
        seal["item_registry"]["factory_instruction_sha256"],
    )], "registry factory normalized instruction drift"
    for ident, signature in PINNED_INTERFACE_METHODS.items():
        assert fingerprint.get(ident) == signature, ("known SHA drift", ident)
    assert isinstance(cls["fields"], list)
    assert len(cls["methods"]) <= 60
    assert len(cls["methods"]) == sum("code_sha256" in x for x in cls["declarations"])
    ids = set()
    for method in cls["methods"]:
        d = method["declaration"]
        ident = d["name"], d["descriptor"]
        assert ident not in ids, ("duplicate method", ident)
        ids.add(ident)
        assert len(method["instruction_sha256"]) == 64
        assert method["instruction_count"] == len(method["instructions"])
    assert len(cls["consumers"]) <= 120
    assert any(name.endswith("/ACItemRegistry") for name in cls["consumers"])
    for name, info in cls["consumers"].items():
        assert isinstance(name, str) and len(info["class_sha256"]) == 64
        assert isinstance(info["sites"], list)
        for body in info["bodies"]:
            assert body["instruction_count"] == len(body["instructions"])
            assert len(body["instruction_sha256"]) == 64
    resources = a["filename_matched_resource_hashes"]
    assert isinstance(resources, dict) and len(resources) <= 200
    for path, proof in resources.items():
        assert path.endswith(".json") and any(t in path.lower() for t in TERMS)
        assert set(proof) == {"size", "sha256"}
        assert type(proof["size"]) is int and proof["size"] > 0
        assert len(proof["sha256"]) == 64
    print("PASS: pinned publisher identity, exact item class census and typed consumers")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())
    print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--partial-manifest", type=Path, required=True)
    args = p.parse_args()
    check(args.report, args.partial_manifest)
