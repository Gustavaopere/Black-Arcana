#!/usr/bin/env python3
"""SHA-exact, fail-closed official NeoForge 21.1.248 SavedData JVM checks.

The NeoForge --installServer distribution is not the ModLauncher transformed
runtime and is not proof of I/O settlement or Gazing Pearl certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNERS = {
    "storage": "net/minecraft/world/level/storage/DimensionDataStorage",
    "saved_data": "net/minecraft/world/level/saveddata/SavedData",
    "factory": "net/minecraft/world/level/saveddata/SavedData$Factory",
}
STATES = {
    "static_contract": "NOT_CERTIFIED",
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION",
    "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}
SCOPE = "GAZING_PEARL_OFFICIAL_NEOFORGE_211248_SAVEDDATA_DISTRIBUTED_ABI_ONLY"
STORAGE_SIG = "(Lnet/minecraft/world/level/saveddata/SavedData$Factory;Ljava/lang/String;)Lnet/minecraft/world/level/saveddata/SavedData;"
SAVED_FILE = "(Ljava/io/File;Lnet/minecraft/core/HolderLookup$Provider;)V"
READ_TAG = "(Ljava/lang/String;Lnet/minecraft/util/datafix/DataFixTypes;I)Lnet/minecraft/nbt/CompoundTag;"


def pairs_unique(pairs):
    result = {}
    for key, val in pairs:
        assert key not in result, ("JSON duplicate key", key)
        result[key] = val
    return result


def load(path: Path, max_len: int):
    data = path.read_bytes()
    assert 0 < len(data) <= max_len, ("unbounded report/manifest", path)
    return data, json.loads(data, object_pairs_hook=pairs_unique)


def canonical_sha(obj) -> str:
    normalized = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return hashlib.sha256(normalized.encode("utf8")).hexdigest()


def body_of(row, name, descriptor=None):
    matches = [x for x in row["selected_methods"]
               if x["declaration"]["name"] == name and
               (descriptor is None or x["declaration"]["descriptor"] == descriptor)]
    assert len(matches) == 1, ("missing/ambiguous JVM method", row["owner"], name, descriptor)
    return matches[0]


def pivot(row, name, descriptor, offset, opcode, symbol="", operand=None):
    method = body_of(row, name, descriptor)
    instructions = [x for x in method["instructions"] if x["offset"] == offset]
    assert len(instructions) == 1, ("JVM offset missing", row["owner"], name, offset)
    ins = instructions[0]
    assert ins["opcode"] == opcode, ("JVM opcode changed", row["owner"], name, offset)
    assert symbol in ins["symbol"], ("JVM semantic target changed", row["owner"], name, offset)
    if operand is not None:
        assert ins["operand"] == operand, ("JVM branch/operand drift", name, offset)
    return ins


def check(report_path: Path, manifest_path: Path):
    raw, report = load(report_path, 350_000)
    _, seal = load(manifest_path, 30_000)
    assert report["scope"] == seal["scope"] == SCOPE
    assert report["schema_version"] == seal["schema_version"] == 1
    assert hashlib.sha256(raw).hexdigest() == seal["evidence"]["report_sha256"]
    assert len(raw) == seal["evidence"]["report_bytes"]
    assert seal["evidence"]["run_id"] == 45016249706
    assert seal["evidence"]["artifact_id"] == 14751558128
    assert report["native"]["artifacts"] == seal["artifact"]
    assert report["native"]["artifacts"]["modlauncher_loaded_bytes"] == "NOT_OBSERVED"
    assert report["native"]["artifacts"]["minecraft_version"] == "1.21.1"
    assert report["native"]["artifacts"]["neoforge_version"] == "21.1.248"
    assert report["installed_modpack_engine_bytes"] == "NOT_VERIFIED"
    assert report["publisher_engine_callsite"] == (
        "ACPlatform.computeIfAbsent -> DimensionDataStorage.computeIfAbsent")
    for k, v in STATES.items():
        assert report[k] == seal["states"][k] == v
    assert len(seal["states"]) == len(STATES)
    assert seal["limits"] == {
        "exact_server_dist_not_loaded": True,
        "installed_modpack_engine_bytes": "NOT_VERIFIED",
        "data_file_physical_qa": "NOT_TESTED",
        "io_worker_settlement": "NOT_VERIFIED",
        "client_sync": "NOT_TESTED",
        "potential_other_mod_transforms": "NOT_VERIFIED",
    }

    classes = report["native"]["classes"]
    assert set(classes) == set(seal["classes"]) == set(OWNERS)
    for label, owner in OWNERS.items():
        row, expected = classes[label], seal["classes"][label]
        assert row["owner"] == expected["owner"] == owner
        assert row["source_archive"] == expected["source_archive"] == "NEOFORGE_OVERLAY"
        assert row["class_major"] == 65
        assert row["class_sha256"] == expected["class_sha256"]
        assert row["not_transformed_runtime"] is True
        assert row["declared_method_count"] == expected["declared_method_count"]
        assert [field["name"] for field in row["fields"]] == expected["fields"]
        assert len(row["selected_methods"]) == row["selected_method_count"] == len(expected["methods"])
        assert len(row["non_executable_declarations"]) == len(expected["non_executable_declarations"])
        for declaration, compact in zip(row["non_executable_declarations"], expected["non_executable_declarations"]):
            assert {k: declaration[k] for k in ("name", "descriptor", "access")} == compact
            assert "code_sha256" not in declaration
            assert declaration["access"] & 0x0400, "abstract declaration not abstract"
        assert [(m["declaration"]["name"], m["declaration"]["descriptor"])
                for m in row["selected_methods"]] == [
                    (m["name"], m["descriptor"]) for m in expected["methods"]]
        for method, compact in zip(row["selected_methods"], expected["methods"]):
            decl = method["declaration"]
            assert decl["code_sha256"] == compact["code_sha256"]
            assert method["instruction_count"] == compact["instruction_count"]
            assert len(method["instructions"]) == method["instruction_count"]
            assert method["instruction_sha256"] == compact["instruction_sha256"]
            assert canonical_sha(method["instructions"]) == compact["instruction_sha256"]
            offs = [r["offset"] for r in method["instructions"]]
            assert offs == sorted(set(offs)), "malformed instruction offset ordering"
    storage = classes["storage"]
    saved = classes["saved_data"]
    factory = classes["factory"]

    # Cache miss → load (with null cache sentinel) → fallback construction.
    for name, descriptor, offset, opcode, sym, arg in (
        ("computeIfAbsent", STORAGE_SIG, 3, "invokevirtual", "get:", None),
        ("computeIfAbsent", STORAGE_SIG, 8, "ifnull", "", "13"),
        ("computeIfAbsent", STORAGE_SIG, 17, "invokeinterface", "Supplier.get:", None),
        ("computeIfAbsent", STORAGE_SIG, 31, "invokevirtual", "set:", None),
        ("get", STORAGE_SIG, 5, "invokeinterface", "Map.get:", None),
        ("get", STORAGE_SIG, 15, "ifnonnull", "", "57"),
        ("get", STORAGE_SIG, 23, "invokeinterface", "Map.containsKey:", None),
        ("get", STORAGE_SIG, 28, "ifne", "", "57"),
        ("get", STORAGE_SIG, 33, "invokevirtual", "Factory.deserializer:", None),
        ("get", STORAGE_SIG, 37, "invokevirtual", "Factory.type:", None),
        ("get", STORAGE_SIG, 41, "invokevirtual", "readSavedData:", None),
        ("get", STORAGE_SIG, 51, "invokeinterface", "Map.put:", None),
        ("set", None, 6, "invokeinterface", "Map.put:", None),
        ("save", "()V", 10, "invokeinterface", "Map.forEach:", None),
    ):
        pivot(storage,name,descriptor,offset,opcode,sym,arg)

    read = body_of(storage, "readSavedData")
    handlers = read["declaration"]["exception_handlers"]
    assert handlers == [{"start":0,"end":54,"target":58,"catch":"java/lang/Exception"}], (
        "readSavedData error swallow boundary changed")
    for off, op, token, arg in (
        (9, "invokevirtual", "File.exists:", None),
        (12, "ifeq", "", "55"),
        (29, "invokevirtual", "readTagFromDisk:", None),
        (37, "ldc", "String data", None),
        (46, "invokeinterface", "BiFunction.apply:", None),
        (54, "areturn", "", None),
        (58, "astore", "", "4"),
        (73, "aconst_null", "", None),
        (74, "areturn", "", None),
    ):
        pivot(storage,"readSavedData",None,off,op,token,arg)
    for off, op, token, arg in (
        (43, "ifeq", "", "59"),
        (51, "invokestatic", "NbtIo.readCompressed:", None),
        (72, "invokestatic", "NbtIo.read:", None),
        (107, "aload_2", "", None),
        (108, "ifnull", "", "139"),
        (131, "invokevirtual", "DataFixTypes.update:", None),
        (139, "aload", "", "8"),
        (210, "invokestatic", "IOUtilities.withIOWorker:", None),
    ):
        pivot(storage,"readTagFromDisk",READ_TAG,off,op,token,arg)

    # Dirty flag is required to serialize and IOUtilities is called before
    # setDirty(false), not proof of a completed durable write.
    for name, descriptor, off, op, token, arg in (
        ("isDirty","()Z",1,"getfield","dirty:Z",None),
        ("setDirty","()V",1,"iconst_1","",None),
        ("setDirty","()V",2,"invokevirtual","setDirty:(Z)",None),
        ("setDirty","(Z)V",2,"putfield","dirty:Z",None),
        ("save",SAVED_FILE,1,"invokevirtual","isDirty:",None),
        ("save",SAVED_FILE,4,"ifeq","","62"),
        ("save",SAVED_FILE,27,"invokevirtual","save:(Lnet/minecraft/nbt/CompoundTag;",None),
        ("save",SAVED_FILE,54,"invokestatic","IOUtilities.withIOWorker:",None),
        ("save",SAVED_FILE,58,"iconst_0","",None),
        ("save",SAVED_FILE,59,"invokevirtual","setDirty:(Z)",None),
    ):
        pivot(saved,name,descriptor,off,op,token,arg)
    assert body_of(saved,"save",SAVED_FILE)["declaration"]["exception_handlers"] == [], (
        "SavedData.save acquired a local exception handler")

    for name, descriptor, off, op, token, arg in (
        ("<init>","(Ljava/util/function/Supplier;Ljava/util/function/BiFunction;)V",
         3,"aconst_null","",None),
        ("<init>","(Ljava/util/function/Supplier;Ljava/util/function/BiFunction;)V",
         4,"invokespecial",'"<init>":',None),
        ("<init>","(Ljava/util/function/Supplier;Ljava/util/function/BiFunction;Lnet/minecraft/util/datafix/DataFixTypes;)V",
         6,"putfield","constructor:",None),
        ("<init>","(Ljava/util/function/Supplier;Ljava/util/function/BiFunction;Lnet/minecraft/util/datafix/DataFixTypes;)V",
         11,"putfield","deserializer:",None),
        ("<init>","(Ljava/util/function/Supplier;Ljava/util/function/BiFunction;Lnet/minecraft/util/datafix/DataFixTypes;)V",
         16,"putfield","type:",None),
        ("deserializer",None,1,"getfield","deserializer:",None),
        ("type",None,1,"getfield","type:",None),
    ):
        pivot(factory,name,descriptor,off,op,token,arg)

    print("PASS: exact 21.1.248 distributed SavedData cache/load/datafix/dirty/save JVM pivots")
    print("REPORT_SHA256",hashlib.sha256(raw).hexdigest())
    print("NOT_LOADED_RUNTIME NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()
    check(args.report,args.manifest)
