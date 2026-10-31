#!/usr/bin/env python3
"""SHA-exact selected Gumball split ownership and ShotGum enchantment audit.

This is bounded interoperability evidence, not reconstructed proprietary source,
a mutating hook, actual save/reload or physical player/modpack validation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import (
    GumballStateProbeError, name_of, summarize, strict_pairs
)

CLASSES = (
    (BASE + "server/entity/item/GumballEntity.class", "onHitEntity",
     "(Lnet/minecraft/world/phys/EntityHitResult;)V",
     [86, 139, 144, 155, 156, 174, 290, 299, 308, 317, 326, 335, 346]),
    (BASE + "server/item/ShotGumItem.class", "acInventoryTick",
     "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V",
     [138, 141, 144, 151, 155, 158, 161, 168,
      172, 175, 178, 185, 188, 190, 193, 196,
      205, 316, 434, 441, 448, 480, 487, 495, 508]),
    (BASE + "server/misc/ACCompat.class", "createEntity",
     "(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/Entity;",
     []),
)

PINNED = {
    "GumballEntity.class": "343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535",
    "ShotGumItem.class": "08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238",
}
MUST_CALL = {
    "GumballEntity.class": (
        "ACCompat.createEntity:", "setSplitsOnHit:", "setDamage:",
        "setTargetsOnBounce:", "setExplosive:", "setMaximumBounces:",
        "addFreshEntity:", "splitsOnHit:",
    ),
    "ShotGumItem.class": (
        "ACEnchantmentRegistry.TARGETED_RICOCHET:",
        "ACEnchantmentRegistry.TRIPLE_SPLIT:",
        "ACEnchantmentRegistry.EXPLOSIVE_FLAVOR:",
        "ACEnchantmentRegistry.BOUNCY_BALL:",
        "ACCompat.enchantLevel:",
        "GumballEntity.setTargetsOnBounce:",
        "GumballEntity.setSplitsOnHit:",
        "GumballEntity.setExplosive:",
        "GumballEntity.setMaximumBounces:",
    ),
    "ACCompat.class": (),
}


def key_anchor(instruction):
    return {key: instruction[key] for key in ("offset", "opcode", "operand", "symbol")}


def collect(jar: Path, javap_bin: str):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise GumballStateProbeError("publisher jar drift")
    results = []
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise GumballStateProbeError("duplicate jar entries")
        for path, name, descriptor, offsets in CLASSES:
            raw = archive.read(path)
            digest = hashlib.sha256(raw).hexdigest()
            filename = path.rsplit("/", 1)[-1]
            if filename in PINNED and PINNED[filename] != digest:
                raise GumballStateProbeError("pinned class SHA drift")
            methods = parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
            selected = [m for m in methods if name_of(m) == name
                        and m["descriptor"] == descriptor]
            if len(selected) != 1:
                raise GumballStateProbeError("missing/ambiguous selected method " + filename)
            method = selected[0]
            if len(method["instructions"]) > 1000:
                raise GumballStateProbeError("unexpected selected method size")
            summary = summarize(method, offsets + ([197, 198, 199] if filename == "ShotGumItem.class" else []))
            refs = summary["symbolic_references"]
            for reference in MUST_CALL[filename]:
                if not any(reference in x["symbol"] for x in refs):
                    raise GumballStateProbeError("missing symbolic call: " + reference)
            if filename == "GumballEntity.class":
                if any("setOwner:" in x["symbol"] for x in refs):
                    raise GumballStateProbeError("new owner propagation in split method")
                if not any("ACCompat.createEntity:" in x["symbol"] for x in refs):
                    raise GumballStateProbeError("child factory changed")
            if filename == "ACCompat.class":
                # Detect exactly which allocation/initialization path is used.
                # Owner assignment is not inferred from an absent direct call.
                if len(refs) > 100:
                    raise GumballStateProbeError("helper symbolic reference budget")
            results.append({
                "class_path": path, "class_sha256": digest,
                "selected_method": {
                    "name": name,
                    "descriptor": descriptor,
                    "parsed_method_sha256": summary["parsed_method_sha256"],
                    "instruction_count": summary["instruction_count"],
                    "symbols": refs, "branches": summary["branches"],
                    "constants": summary["numeric_constants"],
                    "selected_windows": summary["selected_windows"],
                },
            })
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_GUMBALL_SPLIT_FACTORY_AND_SHOTGUM_ENCHANT_GATES",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "classes": results,
        "limits": {
            "runtime_effectiveness": "NOT_TESTED",
            "owner_chain_including_indirect_hooks": "NOT_PROVEN",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "full_method_bytecode_exported": False,
            "cross_provider_contract": "NOT_PROVEN",
        },
    }


def projection(evidence):
    """Small, deterministic sealed evidence; no complete method reproduction."""
    classes = []
    for cls in evidence["classes"]:
        meth = cls["selected_method"]
        essential = []
        filename = cls["class_path"].rsplit("/", 1)[-1]
        if filename in {"GumballEntity.class", "ShotGumItem.class"}:
            required = CLASSES[0][3] if filename == "GumballEntity.class" else CLASSES[1][3]
            all_refs = meth["symbols"] + meth["branches"] + meth["constants"]
            for offset in required:
                matching = [x for x in all_refs if x["offset"] == offset]
                if len(matching) != 1:
                    raise GumballStateProbeError("missing sealed offset " + str(offset))
                essential.append(key_anchor(matching[0]))
        elif filename == "ACCompat.class":
            essential = meth["symbols"]
        chain = []
        if filename == "ShotGumItem.class":
            window = next(w for w in meth["selected_windows"] if w["at"] == 198)
            chain_offsets = (188, 190, 193, 196, 197, 198, 199)
            chain = [x for x in window["instructions"] if x["offset"] in chain_offsets]
            if [x["opcode"] for x in chain] != [
                "iconst_4", "getstatic", "invokestatic", "iconst_2",
                "imul", "iadd", "istore",
            ]:
                raise GumballStateProbeError("enchantment bounce formula changed")
        classes.append({
            "class_path": cls["class_path"],
            "class_sha256": cls["class_sha256"],
            "name": meth["name"],
            "descriptor": meth["descriptor"],
            "parsed_method_sha256": meth["parsed_method_sha256"],
            "instruction_count": meth["instruction_count"],
            "essential_anchors": essential,
            "arithmetic_chain": chain,
        })
    return {
        "schema_version": evidence["schema_version"],
        "scope": evidence["scope"],
        "artifact": evidence["artifact"],
        "classes": classes,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--snapshot")
    args = parser.parse_args()
    result = collect(Path(args.jar), args.javap)
    sealed = projection(result)
    if args.snapshot:
        expected = json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                              object_pairs_hook=strict_pairs)
        if sealed != expected:
            raise GumballStateProbeError("sealed split/enchantment snapshot mismatch")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True)
                   + "\n", encoding="utf8")
    print("GUMBALL_SPLIT_ENCHANT_BEGIN")
    print(json.dumps(sealed, sort_keys=True, separators=(",", ":")))
    print("GUMBALL_SPLIT_ENCHANT_END")
    print("NO_MUTATION NO_PHYSICAL_QA")


if __name__ == "__main__":
    main()
