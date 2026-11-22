#!/usr/bin/env python3
"""SHA-exact fail-closed checks for the NeoForge 21.1.248 write-chain JVM ABI.

This reads publisher/distributed JAR *reports*, not live or transformed classes.
A successful static check never certifies a Gazing Pearl hook or durable save.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCOPE = "NEOFORGE_211248_SAVEDDATA_WRITE_LAMBDA_IOWORKER_DISTRIBUTED_ONLY"
PINNED = {
    "storage": ("net/minecraft/world/level/storage/DimensionDataStorage",
                "6316f03f8ff914c9d7f26fd91359ae98af449f7894e423a2209144e7181e3993"),
    "saved_data": ("net/minecraft/world/level/saveddata/SavedData",
                   "b55a20a77d7f3d4a69c7af79240d6bf14cfa4c7536414a70543030631b265310"),
    "worker": ("net/neoforged/neoforge/common/IOUtilities",
               "3c4cfda19b620562486ca18af3d7c095c94a54c31d1028bf8e5d9860952e115a"),
}
STATES = {
    "static_contract": "NOT_CERTIFIED",
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION",
    "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}
ENGINE = {
    "minecraft_version": "1.21.1",
    "neoforge_version": "21.1.248",
    "installer_sha256": "68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c",
    "neoforge_server_sha256": "1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",
    "neoforge_server_bytes": 5675624,
    "minecraft_srg_sha256": "26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",
    "minecraft_srg_bytes": 14246609,
    "modlauncher_loaded_bytes": "NOT_OBSERVED",
}
WORKER_ARCHIVE = {
    "relative_path": "net/neoforged/neoforge/21.1.248/neoforge-21.1.248-universal.jar",
    "bytes": 3551268,
    "sha256": "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5",
}


def pairs_unique(pairs):
    out = {}
    for k, v in pairs:
        assert k not in out, ("duplicate JSON key", k)
        out[k] = v
    return out


def load(path, limit):
    raw = Path(path).read_bytes()
    assert 0 < len(raw) <= limit, ("unbounded evidence", path)
    return raw, json.loads(raw, object_pairs_hook=pairs_unique)


def normalized_sha(value):
    s = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return hashlib.sha256(s.encode("utf8")).hexdigest()


def method(row, name, descriptor=None):
    found = [x for x in row["selected_methods"]
             if x["declaration"]["name"] == name
             and (descriptor is None or x["declaration"]["descriptor"] == descriptor)]
    assert len(found) == 1, ("JVM executable not unique", row["owner"], name)
    return found[0]


def pivot(row, name, descriptor, offset, opcode, symbol="", operand=None):
    m = method(row, name, descriptor)
    found = [x for x in m["instructions"] if x["offset"] == offset]
    assert len(found) == 1, ("JVM pivot offset missing", row["owner"], name, offset)
    x = found[0]
    assert x["opcode"] == opcode, ("JVM opcode changed", row["owner"], name, offset)
    assert symbol in x["symbol"], ("JVM target changed", row["owner"], name, offset)
    if operand is not None:
        assert x["operand"] == operand, ("JVM operand changed", row["owner"], name, offset)
    return x


def check(path_report: Path, path_manifest: Path):
    raw, report = load(path_report, 200_000)
    _, seal = load(path_manifest, 16_000)
    assert report["schema_version"] == seal["schema_version"] == 1
    assert report["scope"] == seal["scope"] == SCOPE
    assert (seal["evidence"]["run_id"],seal["evidence"]["artifact_id"]) == (
        45020412060,14753915176)
    assert len(raw) == seal["evidence"]["report_bytes"]
    assert hashlib.sha256(raw).hexdigest() == seal["evidence"]["report_sha256"]
    assert report["engine"] == seal["engine"] == ENGINE
    assert report["modlauncher_loaded"] == seal["limits"]["modlauncher_loaded"] == "NOT_OBSERVED"
    assert report["installed_modpack_parity"] == seal["limits"]["installed_modpack_parity"] == "NOT_VERIFIED"
    assert report["io_completion_durability"] == seal["limits"]["io_completion_durability"] == "NOT_VERIFIED"
    assert seal["limits"]["queued_task_failure_behavior"] == "NOT_VERIFIED"
    assert seal["limits"]["writeNbtCompressed_body"] == "NOT_AUDITED"
    assert seal["limits"]["sync_client"] == "NOT_TESTED"
    for k, value in STATES.items():
        assert report[k] == seal["states"][k] == value
    assert set(seal["states"]) == set(STATES)
    assert set(report["classes"]) == set(seal["classes"]) == set(PINNED)

    for key, (owner, digest) in PINNED.items():
        r = report["classes"][key]
        exp = seal["classes"][key]
        assert r["owner"] == exp["owner"] == owner
        assert r["class_sha256"] == exp["class_sha256"] == digest
        assert r["class_major"] == 65
        assert r["declared_method_count"] == exp["declared_method_count"]
        assert r["source_archive"] == exp["source_archive"]
        assert r["archive_metadata"] == exp["archive_metadata"]
        if key == "worker":
            assert r["source_archive"] == "NEOFORGE_211248_INSTALLED_LIBRARY"
            assert r["archive_metadata"] == WORKER_ARCHIVE
            assert [x["name"] for x in r["fields"]] == exp["fields"]
        else:
            assert r["source_archive"] == "NEOFORGE_OVERLAY"
            assert r["archive_metadata"] is None
        assert len(r["selected_methods"]) == len(exp["methods"])
        for item, m in zip(r["selected_methods"], exp["methods"]):
            decl = item["declaration"]
            assert (decl["name"], decl["descriptor"]) == (m["name"], m["descriptor"])
            assert decl["code_sha256"] == m["code_sha256"]
            assert item["instruction_count"] == m["instruction_count"] == len(item["instructions"])
            assert item["instruction_sha256"] == m["instruction_sha256"]
            assert normalized_sha(item["instructions"]) == item["instruction_sha256"]
            offsets = [x["offset"] for x in item["instructions"]]
            assert offsets == sorted(set(offsets)), "duplicate/out-of-order JVM offsets"
        if key == "saved_data":
            declarations = r["non_executable_declarations"]
            assert len(declarations) == 1
            assert declarations[0]["name"] == "save"
            assert declarations[0]["access"] & 0x0400
            assert "code_sha256" not in declarations[0]
        else:
            assert r["non_executable_declarations"] == []

    for key, cpi, bootstrap, linked_name, linked_desc in (
        ("storage", 223, 2, "lambda$save$1",
         "(Ljava/lang/String;Lnet/minecraft/world/level/saveddata/SavedData;)V"),
        ("saved_data", 44, 0, "lambda$save$0",
         "(Lnet/minecraft/nbt/CompoundTag;Ljava/io/File;)V"),
    ):
        cls, expected = report["classes"][key], seal["classes"][key]["bootstrap"]
        bs = cls["save_lambda_bootstrap"]
        assert bs["cp_index"] == expected["cp_index"] == cpi
        assert bs["bootstrap_index"] == expected["bootstrap_index"] == bootstrap
        assert bs["offset"] == expected["caller_offset"] == (5 if key=="storage" else 49)
        assert bs["bootstrap_table_count"] == expected["bootstrap_table_count"]
        assert bs["bootstrap_table_sha256"] == expected["bootstrap_table_sha256"]
        assert bs["operand"] == "#%d, 0"%cpi
        entry = bs["entry"]
        assert entry["handle"]["reference_kind"] == 6
        assert entry["handle"]["reference"][1] == "java/lang/invoke/LambdaMetafactory"
        assert entry["handle"]["reference"][2][1] == "metafactory"
        assert len(entry["arguments"]) == 3
        linked = bs["linked_local"]
        assert linked["name"] == expected["lambda"] == linked_name
        assert linked["descriptor"] == linked_desc
        assert linked["handle"]["reference_kind"] == expected["reference_kind"] == 5
        assert linked["handle"]["reference"][1] == cls["owner"]
        assert linked["handle"]["reference"][2][1:] == [linked_name,linked_desc]
        assert entry["arguments"][1] == linked["handle"]
        assert method(cls,linked_name,linked_desc)["declaration"]["code_sha256"] == linked["code_sha256"]

    storage,saved,worker = (report["classes"][x] for x in ("storage","saved_data","worker"))
    for owner, method_name, desc, off, op, token, operand in (
        (storage,"save","()V",5,"invokedynamic","InvokeDynamic #2:accept:","#223, 0"),
        (storage,"save","()V",10,"invokeinterface","Map.forEach:",None),
        (storage,"lambda$save$1",None,1,"ifnull","","17"),
        (storage,"lambda$save$1",None,7,"invokevirtual","getDataFile:",None),
        (storage,"lambda$save$1",None,14,"invokevirtual","SavedData.save:",None),
        (saved,"save",None,1,"invokevirtual","isDirty:",None),
        (saved,"save",None,4,"ifeq","","62"),
        (saved,"save",None,40,"invokevirtual","CompoundTag.copy:",None),
        (saved,"save",None,49,"invokedynamic","InvokeDynamic #0:run:","#44, 0"),
        (saved,"save",None,54,"invokestatic","IOUtilities.withIOWorker:",None),
        (saved,"save",None,59,"invokevirtual","setDirty:(Z)V",None),
        (saved,"lambda$save$0",None,2,"invokevirtual","java/io/File.toPath:",None),
        (saved,"lambda$save$0",None,5,"invokestatic","IOUtilities.writeNbtCompressed:",None),
        (saved,"lambda$save$0",None,11,"astore_3","",None),
        (saved,"lambda$save$0",None,19,"invokeinterface","Logger.error:",None),
        (worker,"<clinit>","()V",28,"invokestatic","CompletableFuture.completedFuture:",None),
        (worker,"<clinit>","()V",31,"putstatic","saveDataTasks:",None),
        (worker,"withIOWorker","(Ljava/lang/Runnable;)V",0,"getstatic","saveDataTasks:",None),
        (worker,"withIOWorker","(Ljava/lang/Runnable;)V",4,"invokestatic","Util.ioPool:",None),
        (worker,"withIOWorker","(Ljava/lang/Runnable;)V",7,"invokevirtual","CompletableFuture.thenRunAsync:",None),
        (worker,"withIOWorker","(Ljava/lang/Runnable;)V",10,"putstatic","saveDataTasks:",None),
        (worker,"withIOWorker","(Ljava/lang/Runnable;)V",13,"return","",None),
    ):
        pivot(owner,method_name,desc,off,op,token,operand)

    expected_handler = [{"start":0,"end":8,"target":11,"catch":"java/io/IOException"}]
    assert method(saved,"lambda$save$0")["declaration"]["exception_handlers"] == expected_handler
    assert seal["classes"]["saved_data"]["lambda_exception_handler"] == expected_handler
    assert method(worker,"withIOWorker")["declaration"]["exception_handlers"] == []
    assert method(worker,"withIOWorker")["instruction_count"] == 6
    assert all(i["opcode"] not in ("monitorenter","monitorexit")
               and not any(k in i["symbol"] for k in
                           ("CompletableFuture.join:","CompletableFuture.get:"))
               for i in method(worker,"withIOWorker")["instructions"])
    assert method(saved,"save")["declaration"]["exception_handlers"] == []
    print("PASS: exact 21.1.248 SaveData write lambdas, async worker and IOException handler")
    print("REPORT_SHA256",hashlib.sha256(raw).hexdigest())
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED ASYNC_SETTLEMENT_NOT_VERIFIED")


if __name__ == "__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--report",type=Path,required=True)
    cli.add_argument("--manifest",type=Path,required=True)
    args=cli.parse_args()
    check(args.report,args.manifest)
