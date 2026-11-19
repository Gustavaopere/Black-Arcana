#!/usr/bin/env python3
"""Read-only SHA-exact ACFoods static contract, preserving the discovery seal.

The certified object is the native preset container and its finite construction
and field-read boundary. It is not 63 certified foods, a registry lifecycle,
accepted effect application, or an installed/transformed engine execution.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import zipfile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, load_seal, require, rows,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_foods_probe import (
    BUILDER, EFFECT_DESC, TARGET, cp_index, inspect as discover, literal,
)

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json"
DISCOVERY = "EXACT-FOODS-DISCOVERY-1.0.10.json"
BUILDER_SEAL = "EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json"
PREREQUISITES = {
    DISCOVERY: "8ae2d247b7a3f9210d1060c20f5172d0c157bbcaffad7071ae2302eff9a107c8",
    BUILDER_SEAL: "504735467770d52d75c99e7081bfb2a962e5dde0dfa32d884dfdab2e85a6473c",
}
COMPAT = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
EFFECT_BRIDGE = "(Lnet/minecraft/world/effect/MobEffect;)Lnet/minecraft/core/Holder;"
EFFECT_CTOR = "(Lnet/minecraft/core/Holder;I)V"
SOUNDS = {"SOYLENT_GREEN": (291, "HONEY_DRINK"),
          "PURPLE_SODA_BOTTLE": (1375, "GENERIC_DRINK"),
          "HOT_CHOCOLATE_BOTTLE": (1467, "GENERIC_DRINK")}
CLAIMS = {
    "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
    "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
    "static_technical_contract": "CERTIFIED_STATIC_7_AXES",
    "runtime_dispatch": "NOT_VERIFIED", "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED", "perk_certification": "NOT_CERTIFIED",
    "mutation": "NO_MUTATION", "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}
AXES = {
    "identity": "Publisher 1.0.10 hashes/size and all 63 public static final fields, 48 methods and 1555-class typed consumer census; the object is ACFoods, not registered foods or new magical roots.",
    "behavior": "Complete straight-line initializer constructs 63 builder presets and resolves 46 supplier bodies through the separately certified builder; 121 direct external field reads delimit the native consumer boundary, not execution of complete consumers.",
    "parameters": "Every nutrition int, IEEE-754 binary32 saturation/probability operand, native flag, sound field operand, supplier holder field and duration is recorded. Two-argument effect constructors do not explicitly pass an amplifier. No final entity values are inferred.",
    "targeting": "No targeting, victim selection, projectile, AOE or direct effect application occurs in ACFoods. Supplier bodies construct payloads; the entity consuming food and accepted status application belong to separately identified external boundaries.",
    "costs": "No mana, cooldown, stack decrement or resource settlement occurs in the preset container. Static construction is not ingestion or a per-player perk transaction. FoodBuilder's separately pinned reference describes nominal food/use formulas without proving installed execution.",
    "integration": "Custom suppliers obtain their native effect and call ACCompat.effect; the full finite bridge wraps it with the built-in registry. Vanilla holders, direct field reads and the pinned FoodBuilder certificate are recorded separately from complete registry/item/block/engine behavior and hook safety.",
    "validation": "Reproduces the immutable discovery report; reconciles every field, supplier and direct typed read; verifies full bodies/operands and exact float bits; deterministic seal comparison, negative semantic regressions and read-only CLI. Runtime and physical QA remain unverified.",
}
BOUNDARIES = {
    "certified_object": "ACFoods preset construction and finite native payload/field-read boundary",
    "food_item_registry_bindings": "NOT_CERTIFIED",
    "complete_food_item_or_block_behavior": "NOT_CERTIFIED",
    "effect_application_acceptance": "NOT_VERIFIED",
    "downstream_effect_lifecycle": "NOT_CERTIFIED_BY_THIS_OBJECT",
    "amplifier_default": "NOT_INFERRED_FROM_TWO_ARGUMENT_NATIVE_CONSTRUCTOR",
    "sound_and_meat_runtime_effect": "NO_RESOLVE_READ_IN_PINNED_BUILDER_SCOPE",
    "external_reference": "PINNED_FOOD_BUILDER_CERTIFICATE_NOT_INSTALLED_RUNTIME",
    "reflection_and_transformed_classes": "NOT_CLOSED",
    "shared_static_configuration_mutation": "NOT_AUTHORIZED",
}


def prerequisites(provider=PROVIDER):
    result = {}
    for name, sha in PREREQUISITES.items():
        raw = (provider / name).read_bytes()
        require(digest(raw) == sha, "prerequisite seal drift: " + name)
        result[name] = load_seal(provider / name)
    return result


def f32_value(value):
    raw = struct.pack(">f", value)
    return {"bits_hex": raw.hex(), "value": struct.unpack(">f", raw)[0]}


def numeric(reader, row, kind):
    """Resolve JVM immediate/CP values; javap's decimal is a display only."""
    index = cp_index(row["operand"])
    if row["opcode"] in ("ldc", "ldc_w"):
        require(index is not None, "numeric constant-pool operand absent")
        tag, raw = reader.pool[index]
        if kind == "float":
            require(tag == 4, "float constant-pool type drift")
            result = {"bits_hex": raw, "value": struct.unpack(">f", bytes.fromhex(raw))[0]}
        else:
            require(tag == 3, "integer constant-pool type drift")
            result = int.from_bytes(bytes.fromhex(raw), "big", signed=True)
    else:
        value = literal(row)
        require((kind == "float" and row["opcode"].startswith("fconst_")) or
                (kind == "int" and (row["opcode"].startswith("iconst_") or
                                    row["opcode"] in ("bipush", "sipush"))),
                "numeric immediate type drift")
        result = f32_value(value) if kind == "float" else value
    return result


def validate_supplier(method, reader):
    """Close the two observed causal payload shapes; no inferred application."""
    seq = method["instructions"]
    opcodes = [r["opcode"] for r in seq]
    vanilla = ["new", "dup", "getstatic", None, "invokespecial", "areturn"]
    native = ["new", "dup", "getstatic", "invokeinterface", "checkcast",
              "invokestatic", None, "invokespecial", "areturn"]
    expected = vanilla if len(seq) == 6 else native
    require(len(seq) == len(expected) and
            all(want is None or actual == want for want, actual in zip(expected, opcodes)),
            "supplier straight-line construction shape drift")
    require(seq[0]["symbol"] == "class net/minecraft/world/effect/MobEffectInstance",
            "supplier payload class drift")
    holder = reader.resolve(cp_index(seq[2]["operand"]))
    require(holder[0] == 9, "supplier holder is not a field")
    _, holder_owner, (_, holder_name, holder_desc) = holder
    if len(seq) == 6:
        require(holder_owner == "net/minecraft/world/effect/MobEffects" and
                holder_desc == "Lnet/minecraft/core/Holder;", "vanilla effect holder drift")
        source = "VANILLA_HOLDER_FIELD"
    else:
        require(holder_owner == "com/github/alexmodguy/alexscaves/server/potion/ACEffectRegistry" and
                holder_desc == "Ljava/util/function/Supplier;", "native effect supplier field drift")
        require(seq[3]["symbol"] == "InterfaceMethod java/util/function/Supplier.get:()Ljava/lang/Object;" and
                seq[4]["symbol"] == "class net/minecraft/world/effect/MobEffect" and
                seq[5]["symbol"] == "Method " + COMPAT + ".effect:" + EFFECT_BRIDGE,
                "native effect supplier/holder bridge drift")
        source = "NATIVE_SUPPLIER_THEN_ACCOMPAT_HOLDER"
    require(seq[-2]["symbol"] == 'Method net/minecraft/world/effect/MobEffectInstance."<init>":' + EFFECT_CTOR,
            "effect constructor descriptor drift")
    duration = numeric(reader, seq[-3], "int")
    require(duration > 0, "effect duration must be positive in observed payloads")
    return {"holder_source": source, "field_owner": holder_owner,
            "field_name": holder_name, "field_descriptor": holder_desc,
            "duration_ticks": duration, "constructor_descriptor": EFFECT_CTOR,
            "amplifier_argument": "NOT_EXPLICIT", "supplier_instruction_count": len(seq),
            "constructor_offset": seq[-2]["offset"],
            "code_sha256": method["declaration"]["code_sha256"],
            "instruction_sha256": method["instruction_sha256"]}


def validate_bridge(method):
    seq = method["instructions"]
    require([(r["offset"], r["opcode"]) for r in seq] ==
            [(0, "getstatic"), (3, "aload_0"), (4, "invokeinterface"), (9, "areturn")],
            "finite effect bridge shape drift")
    require(seq[0]["symbol"] == "Field net/minecraft/core/registries/BuiltInRegistries.MOB_EFFECT:Lnet/minecraft/core/Registry;" and
            seq[2]["symbol"] == "InterfaceMethod net/minecraft/core/Registry.wrapAsHolder:(Ljava/lang/Object;)Lnet/minecraft/core/Holder;",
            "finite effect bridge dispatch drift")


def validate_contract(report, prior):
    require(report["claims"] == CLAIMS and report["axes"] == AXES and report["boundaries"] == BOUNDARIES,
            "contract authority/safety scope drift")
    require(report["artifact"] == {"mod_id": "alexscaves", "version": "1.0.10",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE}, "contract artifact drift")
    require(report["prerequisites"]["seal_sha256"] == PREREQUISITES,
            "contract prerequisite identity drift")
    discovery = prior[DISCOVERY]
    require(report["discovery_report_sha256"] == discovery["native_report_sha256"],
            "discovery report not reproduced")
    native = report["native"]
    require(native["class_entries_scanned"] == 1555 and
            native["class_sha256"] == discovery["class_sha256"], "native identity drift")
    require(native["initializer_instruction_count"] == 606 and
            native["builder_call_counts"] == discovery["builder_calls"], "initializer/call census drift")
    require(len(native["methods"]) == 48 and len(native["supplier_profiles"]) == 46,
            "full method or supplier roster drift")
    require(len(native["field_profiles"]) == 63 and
            set(native["field_profiles"]) == {r["field"] for r in discovery["fields"]},
            "preset field roster drift")
    require(set(native["supplier_profiles"]) == set(discovery["suppliers"]),
            "supplier name roster drift")
    method_map = {(r["declaration"]["name"], r["declaration"]["descriptor"]): r
                  for r in native["methods"]}
    require(len(method_map) == 48 and set(method_map) ==
            {(name, EFFECT_DESC) for name in discovery["suppliers"]} | {("<init>", "()V"), ("<clinit>", "()V")},
            "complete declared body roster drift")
    require(all(m["instruction_count"] == len(m["instructions"]) and
                m["instruction_sha256"] == digest(canonical(m["instructions"]).encode())
                for m in native["methods"]), "full method row/hash coverage drift")
    require(all(not r["declaration"].get("exception_handlers") and
                not any(row["opcode"].startswith("if") or row["opcode"] in
                        ("goto", "goto_w", "tableswitch", "lookupswitch", "athrow", "monitorenter")
                        for row in r["instructions"]) for r in native["methods"]),
            "preset/supplier branch, handler or monitor drift")
    require(native["constructor_only_object_init"] is True, "constructor boundary drift")
    for old in discovery["fields"]:
        f = native["field_profiles"][old["field"]]
        require(f["nutrition"] == old["nutrition"] and f["write_offset"] == old["write_offset"] and
                f["segment_sha256"] == old["segment_sha256"], "field construction identity drift")
        require(f["saturation_modifier"] == f32_value(old["saturation_modifier"]),
                "exact saturation operand drift")
        require(f["flags"] == [r["name"] for r in old["flags"]], "field flag order drift")
        require(len(f["effects"]) == len(old["effects"]), "field payload count drift")
        for effect, previous in zip(f["effects"], old["effects"]):
            require(effect["supplier"] == previous["supplier"] and
                    effect["call_offset"] == previous["offset"] and
                    effect["bootstrap_index"] == previous["bootstrap_index"] and
                    effect["probability"] == f32_value(previous["probability"]),
                    "field effect order/probability/bootstrap drift")
            supplier = native["supplier_profiles"][effect["supplier"]]
            require({k: effect[k] for k in supplier} == supplier,
                    "field payload supplier causality drift")
        sound = f["sound"]
        if old["field"] in SOUNDS:
            offset, name = SOUNDS[old["field"]]
            require(sound == {"offset": offset, "owner": "net/minecraft/sounds/SoundEvents",
                    "field": name, "descriptor": "Lnet/minecraft/sounds/SoundEvent;"},
                    "sound operand/offset drift")
        else:
            require(sound is None, "unexpected sound field")
    for name, profile in native["supplier_profiles"].items():
        old = discovery["suppliers"][name]
        require(profile["field_owner"] + "." + profile["field_name"] == old["field"] and
                profile["duration_ticks"] == old["ticks"] and
                profile["constructor_descriptor"] == old["constructor"] and
                profile["amplifier_argument"] == "NOT_EXPLICIT" and
                profile["code_sha256"] == old["code_sha256"] and
                profile["instruction_sha256"] == old["instruction_sha256"],
                "supplier payload/reference identity drift")
    boundary = native["direct_field_read_boundary"]
    require(set(boundary) == set(discovery["consumers"]) and len(boundary) == 8,
            "direct field consumer owner census drift")
    actual = {owner: [{"method": m["method"], "descriptor": m["descriptor"],
                     "instruction_sha256": m["instruction_sha256"],
                     "sites": [{k: site[k] for k in ("field", "offset", "opcode")}
                               for site in m["sites"]]} for m in data["methods"]]
              for owner, data in boundary.items()}
    require(actual == discovery["consumers"], "direct field-read site crosswalk drift")
    sites = [site for data in boundary.values() for m in data["methods"] for site in m["sites"]]
    require(len(sites) == 121 and all(s["opcode"] == "getstatic" for s in sites) and
            {s["field"] for s in sites} == set(native["field_profiles"]),
            "direct field-read count/opcode/coverage drift")
    require(native["effect_holder_bridge"]["owner"] == COMPAT, "effect bridge owner drift")
    validate_bridge(native["effect_holder_bridge"]["method"])


def inspect_contract(jar, javap, prior=None):
    prior = prior or prerequisites()
    native = discover(jar, javap)
    discovery_report = {"schema": "AC_FOODS_DISCOVERY_V1", "scope": "DISCOVERY_NOT_CERTIFIED",
        "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "native": native, "mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED", "provider_universe_closed": False}
    reproduced = digest(canonical(discovery_report).encode())
    require(reproduced == prior[DISCOVERY]["native_report_sha256"], "pinned discovery reproduction failed")
    with zipfile.ZipFile(jar) as archive:
        rd = ClassReader(archive.read(TARGET + ".class"))
        compat_raw = archive.read(COMPAT + ".class")
        compat_reader = ClassReader(compat_raw)
        compat_methods = disassemble(jar, javap, COMPAT)
        bridge = summarize(compat_reader, ("effect", EFFECT_BRIDGE), compat_methods[("effect", EFFECT_BRIDGE)])
        validate_bridge(bridge)
        methods = [native["constructor"], native["initializer"],
                   *native["supplier_methods"].values()]
        methods.sort(key=lambda m: (m["declaration"]["name"], m["declaration"]["descriptor"]))
        suppliers = {name: validate_supplier(method, rd)
                     for name, method in sorted(native["supplier_methods"].items())}
        init = native["initializer"]["instructions"]
        row_index = {r["offset"]: i for i, r in enumerate(init)}
        profiles = {}
        for field, conf in sorted(native["configurations"].items()):
            calls = conf["builder_calls"]
            n = next(c for c in calls if c["name"] == "nutrition")
            m = next(c for c in calls if c["name"] == "saturationMod")
            sound_call = [c for c in calls if c["name"] == "sound"]
            sound = None
            if sound_call:
                require(len(sound_call) == 1, "multiple sound operands")
                source = init[row_index[sound_call[0]["offset"]] - 1]
                require(source["opcode"] == "getstatic", "sound operand producer drift")
                tag, owner, (_, name, desc) = rd.resolve(cp_index(source["operand"]))
                require(tag == 9, "sound operand is not a field")
                sound = {"offset": source["offset"], "owner": owner, "field": name, "descriptor": desc}
            effects = []
            for e in conf["effects"]:
                source = init[row_index[e["offset"]] - 1]
                effects.append({"supplier": e["supplier"], "call_offset": e["offset"],
                    "bootstrap_index": e["bootstrap_index"], "probability": numeric(rd, source, "float"),
                    **suppliers[e["supplier"]]})
            profiles[field] = {"nutrition": numeric(rd, init[row_index[n["offset"]] - 1], "int"),
                "saturation_modifier": numeric(rd, init[row_index[m["offset"]] - 1], "float"),
                "flags": [c["name"] for c in calls if c["name"] not in
                          ("of", "nutrition", "saturationMod", "effect", "build")],
                "sound": sound, "effects": effects, "write_offset": conf["write_offset"],
                "segment_sha256": conf["segment_sha256"]}
        ctor = native["constructor"]["instructions"]
        ctor_safe = [r["opcode"] for r in ctor] == ["aload_0", "invokespecial", "return"] and \
            ctor[1]["symbol"] == 'Method java/lang/Object."<init>":()V'
        report = {"schema_version": 1, "schema": "AC_FOODS_STATIC_CONTRACT_V1",
            "artifact": {"mod_id": "alexscaves", "version": "1.0.10", "sha1": SHA1,
                         "sha256": SHA256, "size_bytes": SIZE},
            "claims": CLAIMS, "axes": AXES, "boundaries": BOUNDARIES,
            "prerequisites": {"seal_sha256": PREREQUISITES,
                "builder_report_references": prior[BUILDER_SEAL]["reports"],
                "limit": "Verified committed prerequisites; external engine reports are not rerun or equated to installed execution by this native audit."},
            "discovery_report_sha256": reproduced,
            "native": {"class_entries_scanned": native["class_entries_scanned"],
                "class_roster_sha256": native["class_roster_sha256"],
                "class_sha256": native["target_class_sha256"],
                "initializer_instruction_count": native["initializer"]["instruction_count"],
                "builder_call_counts": native["builder_call_counts"],
                "methods": methods, "constructor_only_object_init": ctor_safe,
                "field_profiles": profiles, "supplier_profiles": suppliers,
                "direct_field_read_boundary": {owner: {k: v for k, v in data.items() if k != "bootstraps"}
                                               for owner, data in native["consumers"].items()},
                "typed_census": {owner: {"typed_reference_count": len(data["typed"]),
                                          "member_reference_count": len(data["references"])}
                                 for owner, data in native["typed_census"].items()},
                "effect_holder_bridge": {"owner": COMPAT, "class_sha256": digest(compat_raw), "method": bridge}}}
    validate_contract(report, prior)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--seal", type=Path, default=SEAL)
    args = parser.parse_args()
    require(not args.output.exists() and args.output.suffix == ".json", "new JSON output required")
    before = {p: digest(p.read_bytes()) for p in (args.jar, args.javap, args.seal,
              *(PROVIDER / name for name in PREREQUISITES))}
    report = inspect_contract(args.jar, args.javap)
    require(report == load_seal(args.seal), "committed static contract does not reproduce")
    require(all(digest(path.read_bytes()) == sha for path, sha in before.items()), "audit input changed")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical(report), encoding="utf8")
    print(canonical({"result": "PASS", "report_sha256": digest(args.output.read_bytes()),
        "fields": len(report["native"]["field_profiles"]),
        "suppliers": len(report["native"]["supplier_profiles"]),
        "methods": len(report["native"]["methods"]), "claims": CLAIMS}).strip())


if __name__ == "__main__":
    main()
