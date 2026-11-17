#!/usr/bin/env python3
"""SHA-exact, read-only Alex's Mobs 2.1.13 AMNetContext bridge discovery.

A class implementing AMNetContext is not evidence of authentication, dispatch
direction, session ownership, replay protection or safe mutation. This probe
produces bounded evidence, never a pass/fail approval for a gameplay adapter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods, sha_file
from alexsmobs_213_transmutation_c2s_probe import (
    BASE, CONTEXT, HANDLER, MESSAGE, MENU, SHA1, SHA256, SIZE,
    fingerprint, item, method_name, parse_class_initializer, require,
)

CONTEXT_NAME = CONTEXT.removesuffix(".class")
REGISTER_OWNER = BASE + "AlexsMobs.class"
SYMBOLS = re.compile(
    r"AMNetContext|getSender|isClientSide|enqueueWork|setPacketHandled|"
    r"MessageTransmuteFromMenu|registerMessage|registerReceiver|"
    r"PacketDistributor|RegisterPayloadHandlersEvent"
)
METHOD_NAMES = {"getSender", "isClientSide", "enqueueWork", "setPacketHandled"}
MAX_CANDIDATES = 45
MAX_REFS_PER_METHOD = 90
MAX_METHODS_PER_CLASS = 45
MAX_BOOTSTRAP = 30
MAX_REPORT_BYTES = 300000
NETWORK = BASE + "message/AMNeoNetwork.class"
ADAPTER = BASE + "message/AMNeoNetwork$1.class"
REGISTRATION = BASE + "message/AMNeoNetwork$Registration.class"
SEND = BASE + "message/AMNeoSend.class"
BRIDGE_NAMES = {
    NETWORK: {"adapt", "handle", "onRegisterPayloads", "registerMessage", "register",
              "decodePayload", "encodePayload", "wrap", "sendToServer"},
    ADAPTER: {"getSender", "isClientSide", "enqueueWork", "setPacketHandled"},
    REGISTRATION: {"handle"},
    SEND: {"registerPlay"},
}


def class_candidates(archive):
    names = archive.namelist()
    require(len(names) == len(set(names)), "duplicate JAR members")
    members = sorted(n for n in names if n.startswith(BASE) and n.endswith(".class"))
    require(1100 <= len(members) <= 1700, "unexpected physical provider class population")
    require(all(p in names for p in (CONTEXT, HANDLER, MESSAGE, MENU, REGISTER_OWNER, SEND)),
            "required native context/handler/registration classes missing")
    found = {}
    for path in members:
        data = archive.read(path)
        if b"AMNetContext" not in data and path not in (REGISTER_OWNER, SEND):
            continue
        require(data[:4] == b"\xca\xfe\xba\xbe" and
                int.from_bytes(data[6:8], "big") == 65,
                "candidate JVM classfile identity mismatch")
        found[path] = hashlib.sha256(data).hexdigest()
    require(2 <= len(found) <= MAX_CANDIDATES, "missing or unbounded context candidates")
    return found


def is_direct_implementer(javap_text):
    """Only direct interface declarations, not incidental constant-pool mentions."""
    for line in javap_text.splitlines():
        if re.match(r"^(public |protected |private |final |abstract |class |interface )", line):
            if " implements " in line and (
                "com.github.alexthe666.alexsmobs.message.AMNetContext" in line
                or "com/github/alexthe666/alexsmobs/message/AMNetContext" in line
            ):
                return True
    return False


def method_projection(method):
    rows = method["instructions"]
    matches = [
        (index, row) for index, row in enumerate(rows)
        if SYMBOLS.search(row["symbol"])
        and row["opcode"].startswith(
            ("invoke", "getfield", "putfield", "getstatic", "putstatic", "new", "ldc")
        )
    ]
    require(len(matches) <= MAX_REFS_PER_METHOD, "unbounded bridge refs in method")
    if not matches and method_name(method) not in METHOD_NAMES:
        return None
    return {
        "method": method_name(method),
        "descriptor": method["descriptor"],
        "body_sha256": fingerprint(method),
        "instruction_count": len(rows),
        "relevant_references": [
            {
                "site": item(row),
                "preceding": item(rows[i-1]) if i else None,
                "following": item(rows[i+1]) if i+1 < len(rows) else None,
            }
            for i, row in matches
        ],
    }


def bridge_windows(path, methods):
    """Bounded receiver/adapter/registration operand evidence only."""
    if path not in BRIDGE_NAMES:
        return []
    chosen = []
    for method in methods:
        if method_name(method) not in BRIDGE_NAMES[path]:
            continue
        rows = method["instructions"]
        require(len(rows) <= 65, "bridge method exceeds bounded bytecode audit window")
        chosen.append({
            "method": method_name(method),
            "descriptor": method["descriptor"],
            "body_sha256": fingerprint(method),
            "instructions": [item(row) for row in rows],
        })
    require(len(chosen) <= 10, "unbounded selected concrete bridge methods")
    return chosen


def bootstrap_candidates(verbose):
    """Select only bootstrap handles plausibly related to setup; no linkage claim."""
    tail = verbose.split("BootstrapMethods:", 1)
    if len(tail) != 2:
        return []
    section = tail[1].split("\nInnerClasses:", 1)[0]
    blocks = re.split(r"(?=^  \d+: #\d+ REF_)", section, flags=re.MULTILINE)
    out = []
    for block in blocks:
        lines = [x.strip() for x in block.splitlines() if x.strip()]
        if not lines or not re.match(r"\d+: #\d+ REF_", lines[0]):
            continue
        if not re.search(r"lambda\$setup\$|MessageTransmuteFromMenu|registerMessage", block):
            continue
        require(len(lines) <= 15, "oversize setup bootstrap entry")
        out.append([line[:230] for line in lines])
    require(len(out) <= MAX_BOOTSTRAP, "unbounded bootstrap candidates")
    return out


def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "publisher JAR hash/size drift")
    with zipfile.ZipFile(jar) as archive:
        candidates = class_candidates(archive)
    classes = []
    for path, class_sha in sorted(candidates.items()):
        dotted = path.removesuffix(".class").replace("/", ".")
        disassembly = javap(javap_bin, jar, dotted)
        methods = parse_methods(disassembly)
        initializer = parse_class_initializer(disassembly)
        if initializer:
            methods.append(initializer)
        selected = [x for m in methods if (x := method_projection(m)) is not None]
        require(len(selected) <= MAX_METHODS_PER_CLASS,
                "unbounded class-level bridge method selection")
        classes.append({
            "class_path": path,
            "class_sha256": class_sha,
            "direct_amnetcontext_implementation": is_direct_implementer(disassembly),
            "declared_methods": len(methods),
            "bridge_roster": [
                {"method": method_name(m), "descriptor": m["descriptor"],
                 "instruction_count": len(m["instructions"])}
                for m in methods
            ] if path in BRIDGE_NAMES else [],
            "bridge_operator_windows": bridge_windows(path, methods),
            "selected_methods": selected,
        })
    require(any(c["class_path"] == REGISTER_OWNER for c in classes),
            "publisher registration owner not inspected")
    verbose = subprocess.run(
        [str(javap_bin), "-classpath", str(jar), "-p", "-v",
         REGISTER_OWNER.removesuffix(".class").replace("/", ".")],
        check=False, text=True, capture_output=True, timeout=75,
    )
    require(verbose.returncode == 0 and
            0 < len(verbose.stdout) <= 4_000_000, "publisher bootstrap javap failed")
    report = {
        "schema_version": 1,
        "scope": "ALEXSMOBS_213_AMNETCONTEXT_IMPLEMENTERS_AND_SETUP_BOOTSTRAP_READONLY",
        "artifact": {
            "filename": "alexsmobs-2.1.13-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
        },
        "classes": classes,
        "direct_implementers": [c["class_path"] for c in classes
                                if c["direct_amnetcontext_implementation"]],
        "setup_bootstrap_candidates": bootstrap_candidates(verbose.stdout),
        "limitations": {
            "network_sender_authentication": "NOT_VERIFIED",
            "payload_registration_direction": "NOT_VERIFIED",
            "callback_bootstrap_linkage": "NOT_VERIFIED",
            "table_position_and_menu_session_binding": "NOT_VERIFIED",
            "choice_rejection_vs_clamping": "NOT_CERTIFIED",
            "replay_concurrent_settlement": "NOT_VERIFIED",
            "static_perk_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
        },
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf-8")) <= MAX_REPORT_BYTES,
            "oversize clean-room output")
    return report


def verify_snapshot(report, expected):
    require(report == expected, "exact AMNetContext/bootstrap snapshot drift")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    if args.snapshot:
        verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({
        "result": "SEALED" if args.snapshot else "DISCOVERY_UNSEALED",
        "candidate_classes": len(report["classes"]),
        "direct_implementers": len(report["direct_implementers"]),
        "bootstrap_candidates": len(report["setup_bootstrap_candidates"]),
        "mutation": "NO_MUTATION",
    }))


if __name__ == "__main__":
    main()
