#!/usr/bin/env python3
"""Fail-closed verification for exact upstream Galena EntityJoinLevelEvent ABI.

Only validates official NeoForge 21.1.248 or 21.1.250 declarations and provenance.
Does NOT certify spawning, inventory settlement, event firing, world safety,
mutating hook availability, runtime transformation or physical QA.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

EVENT = "net/neoforged/neoforge/event/entity/EntityJoinLevelEvent"
ENTITY = "net/neoforged/neoforge/event/entity/EntityEvent"
HOOKS = "net/neoforged/neoforge/event/EventHooks"
PINS = {
    "21.1.248": {
        "report_sha256": "002f2f736ccd9e3af35f0c4bebfac03cc58127b40cdfaad5cca70a8a964aa3c1",
        "report_bytes": 11559,
        "run_id": 45182745228,
        "job_id": 137720448259,
    },
    "21.1.250": {
        "report_sha256": "405abfa11ac03c82efbd63995ff8ccbce5596d3f1e360f5f95392762d3856d12",
        "report_bytes": 11559,
        "run_id": 45180679053,
        "job_id": 137713362339,
    },
}


def need(condition, label):
    if not condition:
        raise ValueError(label)


def unique(pairs):
    out = {}
    for k, v in pairs:
        need(k not in out, "duplicate JSON key " + k)
        out[k] = v
    return out


def load(path, maximum):
    raw = Path(path).read_bytes()
    need(0 < len(raw) <= maximum, "excessive or empty JSON evidence")
    return json.loads(raw, object_pairs_hook=unique), raw


def hash_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def validate(report, seal, *, raw=None, strict=True):
    need(report["schema_version"] == seal["schema_version"] == 1, "schema")
    upstream = report["upstream"]
    version = upstream["version"]
    need(version in PINS, "unsupported NeoForge version")
    pin = PINS[version]
    release = version.replace(".", "")
    need(report["scope"] ==
         f"GALENA_NEOFORGE_{release}_ENTITY_JOIN_ABI_DISCOVERY_ONLY" and
         seal["scope"] ==
         f"GALENA_NEOFORGE_{release}_ENTITY_JOIN_ABI_SUBCONTRACT_NOT_CERTIFIED",
         "scope")
    provenance = seal["provenance"]
    need(provenance["report_sha256"] == pin["report_sha256"] and
         provenance["report_bytes"] == pin["report_bytes"], "report source pin")
    if strict:
        need(raw is not None and len(raw) == pin["report_bytes"] and
             hash_bytes(raw) == pin["report_sha256"],
             "report exact bytes/hash mismatch")
    need(provenance["publisher"] == f"neoforge {version} official Maven",
         "upstream provenance")
    need(provenance["run_id"] == pin["run_id"] and
         provenance["job_id"] == pin["job_id"], "observational run provenance")
    need(provenance["galena_publisher_sha256"] ==
         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
         "provider publisher reference")
    need(upstream["group"] == "net.neoforged" and
         upstream["artifact"] == "neoforge" and
         upstream["version"] == version, "upstream version identity")
    for k, name in (("universal", "publisher_universal"),
                    ("sources", "publisher_sources")):
        info = upstream[k]
        need(info["filename"] == f"neoforge-{version}-" + k + ".jar" and
             info["sha256"] == provenance[name + "_sha256"] and
             info["bytes"] == provenance[name + "_bytes"] and
             info["members"] == provenance[name + "_members"],
             k + " identity or size")
    need(upstream["event_source_sha256"] == provenance["source_sha256"],
         "event source digest")
    need(set(upstream["class_sha256"]) == {EVENT, ENTITY, HOOKS},
         "unverified class identities")

    api = report["api"]
    need(set(api) == {EVENT, ENTITY, HOOKS}, "ABI class roster")
    need(set(seal["classes"]) == {EVENT, ENTITY, HOOKS},
         "sealed class roster")
    for key in (EVENT, ENTITY, HOOKS):
        spec = seal["classes"][key]
        entry = api[key]
        need(entry["owner"] == key and
             upstream["class_sha256"][key] == spec["sha256"],
             "class identity " + key)
        need(entry["method_count"] == spec["method_count"] and
             entry["unresolved_signatures"] == [],
             "method roster or parser coverage " + key)
        need(isinstance(entry["declaration"], str) and
             key.rsplit("/", 1)[-1] in entry["declaration"],
             "class declaration " + key)
        methods = entry["methods"]
        need(len(methods) <= entry["method_count"], "selected methods overflow")
        need(all(isinstance(x["declaration"], str) and
                 isinstance(x["descriptor"], str) and
                 re.fullmatch(r"\([^\n]*\)[^\n]+", x["descriptor"])
                 for x in methods), "invalid JVM signatures " + key)
        if key in (EVENT, ENTITY):
            need(len(methods) == spec["method_count"] and
                 sorted(x["descriptor"] for x in methods) ==
                 sorted(spec["required_method_descriptors"]),
                 "event or entity ABI descriptors drift " + key)

    need("ICancellableEvent" in api[EVENT]["declaration"] and
         report["candidate"]["event_declares_cancellable_interface"] is True and
         seal["classes"][EVENT]["cancellable_declared"] is True,
         "cancellable interface identity")
    em = api[EVENT]["methods"]
    need(sum("EntityJoinLevelEvent(" in x["declaration"] for x in em) == 2 and
         sum("getLevel(" in x["declaration"] for x in em) == 1 and
         sum("loadedFromDisk(" in x["declaration"] for x in em) == 1,
         "event constructor/accessor semantics")
    need(any("getEntity(" in x["declaration"] for x in api[ENTITY]["methods"]),
         "base event entity accessor")
    need(report["candidate"]["event_constructor_or_accessor_declarations"] ==
         [x["declaration"] for x in em],
         "candidate event API mismatch")
    hm = [x["declaration"] for x in api[HOOKS]["methods"]]
    need(report["candidate"]["event_hook_method_declarations"] == hm,
         "candidate EventHooks subset mismatch")
    need(not any("join" in decl.split("(", 1)[0].split()[-1].lower()
                 for decl in hm), "unexpected direct join-named EventHooks API")
    need(report["limitations"] == seal["limits"], "limitations modified")
    need(report["static_contract"] == seal["states"]["static_contract"] ==
         "NOT_CERTIFIED", "static certification promotion")
    need(report["mutating_hook"] == seal["states"]["mutating_hook"] ==
         "NOT_VERIFIED", "mutating hook promotion")
    need(report["physical_qa"] == seal["states"]["physical_qa"] ==
         "NOT_TESTED", "physical QA promotion")
    need(report["mutation"] == seal["states"]["mutation"] ==
         "NO_MUTATION", "unsafe mutation")
    need(report["provider_universe_closed"] is
         seal["states"]["provider_universe_closed"] is False,
         "provider universe falsely closed")
    need(report["semantic_magic_roots_delta"] ==
         seal["states"]["semantic_magic_roots_delta"] == 0,
         "inflated roots")
    need(set(report["limitations"]) == {
        "jar_installed_parity", "event_firing_from_transformed_minecraft",
        "provider_item_consumption_and_spawn_atomicity",
        "event_order_and_spawn_result_acceptance",
        "authoritative_post_spawn_observation", "safe_mutating_hook",
        "physical_qa",
    }, "missing explicit unverified limit")
    need(all(v in ("NOT_VERIFIED", "NOT_TESTED") for v
             in report["limitations"].values()), "unverified limit promoted")
    return len(em), api[HOOKS]["method_count"]


def adversarial(report, seal):
    cases = []
    def mutate(label, path, value):
        r = copy.deepcopy(report)
        cur = r
        for part in path[:-1]:
            cur = cur[part]
        cur[path[-1]] = value
        cases.append((label, r, seal))
    mutate("fake certified static", ["static_contract"], "CERTIFIED")
    mutate("fake safe hook", ["mutating_hook"], "VERIFIED")
    mutate("fake physical QA", ["physical_qa"], "PASSED")
    mutate("unsafe mutation", ["mutation"], "MUTATION")
    mutate("fake provider closure", ["provider_universe_closed"], True)
    mutate("fake extra spell", ["semantic_magic_roots_delta"], 1)
    mutate("fake version", ["upstream", "version"],
           "21.1.250" if report["upstream"]["version"] == "21.1.248"
           else "21.1.248")
    mutate("alter universal", ["upstream", "universal", "sha256"], "0" * 64)
    mutate("alter source", ["upstream", "event_source_sha256"], "0" * 64)
    mutate("wrong event ABI", ["upstream", "class_sha256", EVENT], "0" * 64)
    mutate("event count", ["api", EVENT, "method_count"], 5)
    mutate("event header", ["api", EVENT, "declaration"], "public class Fake;")
    mutate("unresolved signature", ["api", EVENT, "unresolved_signatures"],
           ["public missed();"])
    mutate("fake cancellable", ["candidate", "event_declares_cancellable_interface"], False)
    mutate("fake event API", ["candidate", "event_constructor_or_accessor_declarations"], [])
    mutate("fake EventHooks subset", ["candidate", "event_hook_method_declarations"], [])
    mutate("fake event fired", ["limitations", "event_firing_from_transformed_minecraft"], "VERIFIED")
    mutate("claim spawn atomicity", ["limitations", "provider_item_consumption_and_spawn_atomicity"], "VERIFIED")
    mutate("fake world safety", ["limitations", "safe_mutating_hook"], "VERIFIED")
    mutate("fake installation parity", ["limitations", "jar_installed_parity"], "VERIFIED")
    x = copy.deepcopy(report)
    x["api"][EVENT]["methods"][0]["descriptor"] = "()V"
    cases.append(("forged constructor descriptor", x, seal))
    x = copy.deepcopy(report)
    x["api"][EVENT]["methods"][2]["declaration"] = "public boolean fake();"
    cases.append(("forged accessor", x, seal))
    x = copy.deepcopy(report)
    x["api"][ENTITY]["methods"][1]["declaration"] = "public boolean fake();"
    cases.append(("forged base entity accessor", x, seal))
    x = copy.deepcopy(seal)
    x["states"]["mutating_hook"] = "VERIFIED"
    cases.append(("forged seal mutating", report, x))
    x = copy.deepcopy(seal)
    x["classes"][EVENT]["sha256"] = "0" * 64
    cases.append(("forged seal ABI digest", report, x))
    rejected = 0
    for label, r, s in cases:
        try:
            validate(r, s, strict=False)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected += 1
        else:
            raise AssertionError("forgery wrongly accepted: " + label)
    need(rejected == len(cases) and rejected >= 25, "adversarial coverage")
    return rejected


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--adversarial", action="store_true")
    args = p.parse_args()
    report, raw = load(args.report, 250_000)
    seal, _ = load(args.manifest, 100_000)
    methods, event_hooks = validate(report, seal, raw=raw)
    print("exact report bytes:", len(raw), "SHA-256:", hash_bytes(raw))
    print("event own methods:", methods, "EventHooks declared:", event_hooks)
    if args.adversarial:
        print("adversarial mutations rejected:", adversarial(report, seal))
    print("OK — API-only evidence; NO_MUTATION, static contract NOT_CERTIFIED")


if __name__ == "__main__":
    main()
