#!/usr/bin/env python3
"""Discover Mixin's exported post-transform classfiles in an isolated test server.

Read-only diagnostic, not proof that every handler was injected or called.
Do not upload third-party classfiles or decompiled material. Output is bounded
JSON metadata and concise method-name excerpts, fail-closed for missing exports.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

CLASSES = {
    "Entity":"net/minecraft/world/entity/Entity.class",
    "LivingEntity":"net/minecraft/world/entity/LivingEntity.class",
    "RangedAttribute":"net/minecraft/world/entity/ai/attributes/RangedAttribute.class",
}
IDENTIFIERS = (
    "vb$", "vanillabackport", "mda87957",
    "RestituteMovementAfterCollisions", "applyAirDrag", "handleMovementFriction",
    "earlyCapture", "fixKnockbackResistanceRange", "createLivingAttributes",
)

def inspect(root:Path):
    exports = root / ".mixin.out" / "class"
    output={"status":"DISCOVERY_ONLY_POST_MIXIN_EXPORTS",
            "scope":"minimal dedicated NeoForge 21.1.250 + Platform 1.3.3 + Vanilla Backport 1.1.7.10",
            "mixin_export_root":".mixin.out/class",
            "target_classfiles":{},
            "limitations":[
                "An exported target is classfile data after Mixin processing in this minimal server.",
                "Presence alone does not prove all injection handlers, ordinals, callbacks or invocation occurred.",
                "Not the complete 589-mod profile; no real player or Slime Aspect/Boots exercise.",
                "Do not infer public hook or right to mutate provider-owned values.",
            ], "deviations":[]}
    for label,relative in CLASSES.items():
        f=exports/relative
        if not f.is_file():
            raise ValueError("MIXIN_POST_EXPORT_CLASS_MISSING:"+relative)
        data=f.read_bytes()
        if len(data)<150 or data[:4] != bytes.fromhex("cafebabe"):
            raise ValueError("MIXIN_POST_EXPORT_INVALID_CLASS:"+relative)
        named=relative[:-6].replace("/",".")
        p=subprocess.run(["javap","-p","-c","-s","-classpath",str(exports),named],
            text=True,capture_output=True,check=True)
        lines=p.stdout.splitlines()
        # Indented javap declaration headers from the exported post-mixin target.
        method_headers=[x.strip()[:160] for x in lines
            if re.match(r"^  (?:public|protected|private|static|final|synchronized|native|\w+ ).*\([^)]*\);\s*$",x)]
        selected=[x for x in method_headers if any(key.lower() in x.lower() for key in IDENTIFIERS)]
        # Method call excerpts are diagnostics; not proof of semantic invocation in gameplay.
        invocations=[x.strip()[:165] for x in lines
            if ("// Method " in x or "// InterfaceMethod " in x)
            and any(key.lower() in x.lower() for key in IDENTIFIERS)]
        item={
            "path":relative,
            "sha256":hashlib.sha256(data).hexdigest(),
            "bytes":len(data),
            "method_header_count":len(method_headers),
            "selected_method_headers":selected[:45],
            "selected_invoke_lines":invocations[:35],
            "selected_method_header_total":len(selected),
            "selected_invoke_total":len(invocations),
        }
        output["target_classfiles"][label]=item
        print("POST_MIXIN_TARGET="+label+" SHA256="+item["sha256"]+
              " METHODS="+str(len(method_headers))+
              " CANDIDATES="+str(len(selected)))
        for name in selected[:22]:
            print("POST_MIXIN_HANDLER_HEADER["+label+"]="+name)
        for call in invocations[:12]:
            print("POST_MIXIN_HANDLER_INVOKE["+label+"]="+call)
    return output

class Regression(unittest.TestCase):
    def test_missing_export_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,"MIXIN_POST_EXPORT_CLASS_MISSING"):
                inspect(Path(tmp))
    def test_invalid_class_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/".mixin.out"/"class"/CLASSES["Entity"]
            p.parent.mkdir(parents=True)
            p.write_bytes(b"not a class file"*20)
            with self.assertRaisesRegex(ValueError,"MIXIN_POST_EXPORT_INVALID_CLASS"):
                inspect(Path(tmp))
    def test_exact_class_set(self):
        self.assertEqual(len(CLASSES),3)
        self.assertEqual(len(set(CLASSES.values())),3)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Regression)
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    if args.root is None or args.output is None:
        p.error("--root and --output are required")
    try:
        report=inspect(args.root)
    except (OSError,ValueError,subprocess.CalledProcessError) as e:
        report={"status":"FAIL_CLOSED_EXPORT_PROBE","deviations":[str(e)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"]}))
    return 0 if report["status"]=="DISCOVERY_ONLY_POST_MIXIN_EXPORTS" else 2

if __name__ == "__main__":
    sys.exit(main())
