#!/usr/bin/env python3
"""SHA-exact Tremorzilla normal-control-flow graph inspection (read-only).

Builds intra-method normal edges from javap instructions, explicitly excluding
exception-table edges, dynamic dispatch, runtime mixins, policy and side effects.
A call dominating a site means invocation precedes all *normal CFG paths* to
that site, never that its return value authorizes that effect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_tremorzilla_beam_probe import CLASS, CLASS_SHA, method_name, method_digest

SELECTED = (
    ("breakBlocksAround", "(Lnet/minecraft/world/phys/Vec3;FZZF)Z",
     "1212f9fdad485fe769e934ef7048ae21cf022edbce480e7b795089b2bbb39371"),
    ("tickBreath", "()V",
     "22d4de159e1a792b620bd117ffdfca70ef3a42e1395cbb4216ae6e480cd2eeec"),
    ("canEntityBeHurtByBeam",
     "(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/phys/Vec3;)Z",
     "13e05b91afaf21aee584377aab719dfa8b3d18b8096dce18797d259910af854c"),
)

ANCHORS = {
    "breakBlocksAround": {
        "guards": ((12, "ACPlatform.canEntityGrief:"), (22, "Level.isClientSide:")),
        "sites": ((249, "Level.destroyBlock:"), (268, "ACCompat.onBlockExploded:"),
                  (296, "ACCompat.createEntity:"), (349, "Level.addFreshEntity:")),
    },
    "tickBreath": {
        "guards": ((4, "Level.isClientSide:"), (393, "Level.clip:")),
        "sites": ((525, "breakBlocksAround:"), (552, "hurtEntitiesAround:"),
                  (578, "hurtEntitiesAround:"), (620, "breakBlocksAround:")),
    },
    "canEntityBeHurtByBeam": {
        "guards": ((37, "Level.clip:"),),
        "sites": ((40, "BlockHitResult.getType:"),),
    },
}
MAX_METHOD_INSTRUCTIONS = 2400
MAX_REPORT_BYTES = 30000


class NormalCFGError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise NormalCFGError(message)


def normal_edges(instructions):
    """Full normal bytecode edges; fail closed for unparsed/switch transfers."""
    require(1 <= len(instructions) <= MAX_METHOD_INSTRUCTIONS,
            "invalid normal CFG instruction count")
    offsets = [op["offset"] for op in instructions]
    require(offsets == sorted(set(offsets)), "unordered/duplicate offsets")
    universe = set(offsets)
    graph = {}
    terminal = ("return", "ireturn", "areturn", "lreturn",
                "freturn", "dreturn", "athrow")
    unsupported = ("tableswitch", "lookupswitch", "jsr", "jsr_w", "ret", "wide")
    for ix, op in enumerate(instructions):
        name = op["opcode"]
        offset = op["offset"]
        require(name not in unsupported, "unparsed JVM transfer opcode: " + name)
        next_offset = offsets[ix + 1] if ix + 1 < len(offsets) else None
        branches = name.startswith("if") or name in ("goto", "goto_w")
        if branches:
            dest = op["operand"].strip()
            require(re.fullmatch(r"\d+", dest) is not None,
                    "non-numeric JVM branch target at " + str(offset))
            target = int(dest)
            require(target in universe, "missing branch target at " + str(offset))
            edges = [target]
            if name.startswith("if"):
                require(next_offset is not None, "conditional branch without fallthrough")
                edges.append(next_offset)
        elif name in terminal:
            edges = []
        else:
            require(next_offset is not None, "unterminated method CFG")
            edges = [next_offset]
        graph[offset] = sorted(set(edges))
    return graph


def traverse(graph, start, *, forbidden=None):
    if start == forbidden:
        return set()
    reached, stack = set(), [start]
    while stack:
        here = stack.pop()
        if here in reached or here == forbidden:
            continue
        require(here in graph, "CFG vertex missing")
        reached.add(here)
        stack.extend(graph[here])
    return reached


def dominators(graph, start):
    """Normal intraprocedural dominators, including loops/backedges."""
    reachable = traverse(graph, start)
    predecessors = {v: set() for v in reachable}
    for src in reachable:
        for dst in graph[src]:
            if dst in reachable:
                predecessors[dst].add(src)
    dom = {v: ({start} if v == start else set(reachable)) for v in reachable}
    for _ in range(len(reachable) + 1):
        changed = False
        for vertex in sorted(reachable):
            if vertex == start:
                continue
            pred = predecessors[vertex]
            require(bool(pred), "reachable vertex lacks predecessor")
            intersection = set.intersection(*(dom[p] for p in pred))
            result = {vertex} | intersection
            if result != dom[vertex]:
                dom[vertex], changed = result, True
        if not changed:
            return dom
    raise NormalCFGError("normal CFG dominator convergence bound exceeded")


def verify_anchor(insns, offset, symbol_fragment):
    hits = [i for i in insns if i["offset"] == offset]
    require(len(hits) == 1 and hits[0]["opcode"].startswith("invoke")
            and symbol_fragment in hits[0]["symbol"],
            "normal CFG JVM callsite drift at " + str(offset))


def analyze_method(method):
    name = method_name(method)
    require(name in ANCHORS, "unexpected normal CFG method")
    graph = normal_edges(method["instructions"])
    entry = method["instructions"][0]["offset"]
    reachable = traverse(graph, entry)
    dom = dominators(graph, entry)
    anchors = ANCHORS[name]
    for offset, fragment in (*anchors["guards"], *anchors["sites"]):
        verify_anchor(method["instructions"], offset, fragment)
        require(offset in reachable, "sealed JVM callsite unreachable: " + str(offset))
    sites = []
    for offset, symbol in anchors["sites"]:
        guards = []
        for guard_offset, guard_symbol in anchors["guards"]:
            result = guard_offset in dom[offset]
            without = offset in traverse(graph, entry, forbidden=guard_offset)
            require(result == (not without),
                    "normal CFG dominance and bypass disagree")
            guards.append({
                "guard_offset": guard_offset,
                "guard_symbol": guard_symbol,
                "dominates_normal_paths": result,
                "bypass_normal_path_exists": without,
            })
        sites.append({"site_offset": offset, "site_symbol": symbol, "guards": guards})
    backedges = sum(1 for src, dsts in graph.items() for dst in dsts if dst <= src)
    return {
        "name": name,
        "descriptor": method["descriptor"],
        "method_sha256": method_digest(method),
        "instruction_count": len(graph),
        "normal_edge_count": sum(len(v) for v in graph.values()),
        "normal_backedge_count": backedges,
        "sites": sites,
    }


def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "exact publisher JAR SHA and size mismatch")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate publisher ZIP members")
        require(hashlib.sha256(archive.read(CLASS)).hexdigest() == CLASS_SHA,
                "exact Tremorzilla class digest mismatch")
    methods = parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    require(len(methods) == 116, "unexpected selected publisher class method count")
    chosen = []
    for name, descriptor, sha in SELECTED:
        found = [m for m in methods
                 if (method_name(m), m["descriptor"]) == (name, descriptor)]
        require(len(found) == 1 and method_digest(found[0]) == sha,
                "SHA-exact Tremorzilla JVM signature or method digest drift")
        chosen.append(analyze_method(found[0]))
    result = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_NORMAL_INTRAMETHOD_CFG_NO_EXCEPTIONS",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_path": CLASS, "class_sha256": CLASS_SHA,
        "methods": chosen,
        "limits": {
            "exception_table_edges": "NOT_MODELED",
            "dynamic_dispatch_and_transformations": "NOT_MODELED",
            "guard_return_value_semantics": "NOT_PROVEN",
            "claims_and_world_protection": "NOT_VERIFIED",
            "native_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "static_perk_certification": "NOT_CERTIFIED",
        },
    }
    require(len(json.dumps(result, sort_keys=True).encode()) <= MAX_REPORT_BYTES,
            "bounded normal CFG evidence budget exceeded")
    return result



def verify_sealed_snapshot(report, sealed):
    """No substitution of identities, CFG edges/guards, or QA certification."""
    expected_keys = ("schema_version", "scope", "artifact", "class_path",
                     "class_sha256", "methods", "limits")
    require(set(report) == set(expected_keys), "unexpected normal CFG report schema")
    require(set(sealed) == set(expected_keys), "unexpected normal CFG sealed schema")
    require(report == sealed, "exact normal CFG guard digest, edge or status drift")
    require(report["scope"] == "SHA_EXACT_1010_NORMAL_INTRAMETHOD_CFG_NO_EXCEPTIONS",
            "unverified expanded CFG scope")
    require(report["limits"]["exception_table_edges"] == "NOT_MODELED"
            and report["limits"]["guard_return_value_semantics"] == "NOT_PROVEN"
            and report["limits"]["claims_and_world_protection"] == "NOT_VERIFIED"
            and report["limits"]["mutation"] == "NO_MUTATION"
            and report["limits"]["static_perk_certification"] == "NOT_CERTIFIED"
            and report["limits"]["physical_qa"] == "NOT_TESTED",
            "unsupported authority or certification claim")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()
    r = audit(args.jar, args.javap)
    verify_sealed_snapshot(r, json.loads(args.manifest.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for method in r["methods"]:
        print("NORMAL_CFG_METHOD=" + method["name"] + " sha=" + method["method_sha256"]
              + " vertices=" + str(method["instruction_count"])
              + " edges=" + str(method["normal_edge_count"])
              + " backedges=" + str(method["normal_backedge_count"]))
        for site in method["sites"]:
            print("NORMAL_CFG_SITE=" + method["name"] + " " + json.dumps(site, sort_keys=True))
    print("NORMAL_CFG_ONLY; NO_GUARD_SEMANTICS; NO_MUTATION; NO_PHYSICAL_QA")


if __name__ == "__main__":
    main()
