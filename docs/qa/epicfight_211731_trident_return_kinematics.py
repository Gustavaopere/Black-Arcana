#!/usr/bin/env python3
"""Bounded exact-publisher Epic Fight trident return movement bytecode QA.

Confirms the contiguous javap opcode and operand sequence, not running
gameplay, player presence, owner validity or the executed movement speed.
No JAR or third-party implementation is embedded or redistributed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import unittest

from epicfight_211731_trident_causal import inspect as inspect_publisher, javap, blocks, instructions

CLASS = "yesman.epicfight.world.capabilities.projectile.ThrownTridentPatch"

# One fixed sequence from the SHA-pinned 21.17.3.1 tickEnd() method.
# The second column is a required operand ("" accepts any constant-pool ID).
# All opcodes from tickCount loading through setPos are covered, with no gaps.
SPEC = """
getfield|ThrownTrident.tickCount:I
aload_0|
getfield|Field returnTick:I
isub|
bipush|10
isub|
iconst_0|
invokestatic|Math.max:(II)I
istore_1|
aload_0|
getfield|Field original:
checkcast|ThrownTrident
invokevirtual|ThrownTrident.getOwner:
invokevirtual|Entity.getEyePosition:
aload_0|
getfield|Field original:
checkcast|ThrownTrident
invokevirtual|ThrownTrident.position:
invokevirtual|Vec3.subtract:
astore_2|
aload_2|
invokevirtual|Vec3.length:
dstore_3|
iload_1|
i2d|
ldc2_w|double 2.0d
invokestatic|Math.pow:(DD)D
ldc2_w|double 5.0E-4d
dmul|
iload_1|
i2d|
ldc2_w|double 0.05d
dmul|
invokestatic|Math.abs:(D)D
dadd|
ldc2_w|double 10.0d
dload_3|
invokestatic|Math.min:(DD)D
invokestatic|Math.min:(DD)D
dstore|5
aload_2|
invokevirtual|Vec3.normalize:
dload|5
invokevirtual|Vec3.scale:
astore|7
aload_0|
getfield|Field original:
checkcast|ThrownTrident
new|Vec3
dup|
dconst_0|
dconst_0|
dconst_0|
invokespecial|Vec3."<init>":(DDD)V
invokevirtual|ThrownTrident.setDeltaMovement:
aload_0|
getfield|Field original:
checkcast|ThrownTrident
invokevirtual|ThrownTrident.position:
astore|8
aload_0|
getfield|Field original:
checkcast|ThrownTrident
aload|8
getfield|Vec3.x:D
aload|7
getfield|Vec3.x:D
dadd|
aload|8
getfield|Vec3.y:D
aload|7
getfield|Vec3.y:D
dadd|
aload|8
getfield|Vec3.z:D
aload|7
getfield|Vec3.z:D
dadd|
invokevirtual|ThrownTrident.setPos:(DDD)V
"""
EXPECTED = [tuple(s.split("|", 1)) for s in SPEC.strip().splitlines()]

def matches(op, expected):
    _, code, tail = op
    required_opcode, token = expected
    if code != required_opcode:
        return False
    # Numeric locals and bipush are matched exactly, not by substring.
    if code in {"bipush", "aload", "dload", "dstore", "astore"} and token:
        return tail.strip() == token
    return token in tail

def verify(ops):
    if not 200 <= len(ops) <= 450:
        raise ValueError("tickEnd method size changed")
    windows = [i for i in range(len(ops)-len(EXPECTED)+1)
               if all(matches(ops[i+j], pattern)
                      for j, pattern in enumerate(EXPECTED))]
    if len(windows) != 1:
        raise ValueError("movement opcode/operand sequence not found exactly once")
    at = windows[0]
    selected = ops[at:at+len(EXPECTED)]
    pcs = [pc for pc,_,_ in selected]
    if pcs != sorted(set(pcs)):
        raise ValueError("invalid opcode PCs")
    return {
        "status": "PASS_EXACT_TRIDENT_RETURN_KINEMATICS_BOUNDED",
        "evidence_class": "EXACT_PUBLISHER_ORDERED_CONTIGUOUS_COMPILED_OPERANDS",
        "method": CLASS + ".tickEnd()",
        "first_pc": pcs[0],
        "last_pc": pcs[-1],
        "checked_instructions": len(EXPECTED),
        "formula_supported_by_opcode_sequence": {
            "elapsed_ticks": "max(trident.tickCount - returnTick - 10, 0)",
            "offset": "owner.eyePosition - trident.position",
            "distance": "length(offset)",
            "step_requested": "min(pow(t,2)*0.0005 + abs(t*0.05), min(10.0,distance))",
            "position_update": "trident.setPos(currentPosition + normalize(offset)*step_requested)",
            "previous_delta_movement": "explicitly zeroed using Vec3(0,0,0)",
        },
        "bounded_inference": "requested per-tick movement cannot exceed min(10,distance) in the verified expression, assuming finite coordinates",
        "limitations": [
            "No player, attack, tick telemetry or owner-null cases executed.",
            "This proof does not certify route length, total recall duration, hitbox radius, target count or real per-tick displacement.",
            "Other systems may alter the entity after this method; physics and world collisions were not tested.",
            "Source 21.17.3 explains the stack expression; the operand/order verification is of exact publisher 21.17.3.1."
        ]
    }

def exact_tick_end(disasm):
    options = [instructions(code) for header,code in blocks(disasm)
               if header == "public void tickEnd();"]
    if len(options) != 1:
        raise ValueError("missing or duplicate exact tickEnd method")
    return options[0]

class Tests(unittest.TestCase):
    @staticmethod
    def fixture():
        # Test only the scanner in a synthetic method-sized instruction list.
        ins = [(i*3, "nop", "") for i in range(110)]
        for j,(opcode,token) in enumerate(EXPECTED):
            ins.append(((j+110)*3, opcode, token))
        ins.extend([((i+len(ins))*3,"nop","") for i in range(18)])
        return ins
    def test_positive_window(self):
        self.assertEqual(verify(self.fixture())["status"],
                         "PASS_EXACT_TRIDENT_RETURN_KINEMATICS_BOUNDED")
    def test_changed_delay(self):
        x=self.fixture()
        i=next(i for i,(_,op,t) in enumerate(x) if op=="bipush" and t=="10")
        x[i]=(x[i][0],"bipush","9")
        with self.assertRaisesRegex(ValueError,"sequence"):
            verify(x)
    def test_changed_quadratic_constant(self):
        x=self.fixture()
        i=next(i for i,(_,op,t) in enumerate(x) if "5.0E-4d" in t)
        x[i]=(x[i][0],op,"double 0.0004d")
        with self.assertRaisesRegex(ValueError,"sequence"):
            verify(x)
    def test_swapped_mins(self):
        x=self.fixture()
        idx=next(i for i,(_,op,t) in enumerate(x) if op=="dload_3")
        x[idx]=(x[idx][0],"dstore_3","")
        with self.assertRaisesRegex(ValueError,"sequence"):
            verify(x)
    def test_missing_position_set(self):
        x=self.fixture()
        i=next(i for i,(_,op,t) in enumerate(x) if "setPos:" in t)
        x[i]=(x[i][0],"invokevirtual","Other.setPos:")
        with self.assertRaisesRegex(ValueError,"sequence"):
            verify(x)
    def test_no_method(self):
        with self.assertRaisesRegex(ValueError,"missing or duplicate"):
            exact_tick_end("class Empty{}")
    def test_wrong_size(self):
        with self.assertRaisesRegex(ValueError,"size changed"):
            verify([(0,"nop","")])
    def test_duplicate_sequence(self):
        x=self.fixture()
        # Keep PCs monotonically increasing; a second contiguous duplicate must fail.
        y=x + [(x[-1][0]+3*(j+1), op, token)
               for j,(op,token) in enumerate(EXPECTED)]
        with self.assertRaisesRegex(ValueError,"exactly once"):
            verify(y)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--jar",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        test=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if test.wasSuccessful() else 1
    if not a.jar or not a.output:
        p.error("--jar and --output are required")
    try:
        publisher=inspect_publisher(a.jar)
        out=verify(exact_tick_end(javap(a.jar,CLASS)))
        out["publisher_sha1"]=publisher["sha1"]
        out["publisher_sha256"]=publisher["sha256"]
        out["publisher_gate"]=publisher["status"]
    except (OSError,ValueError) as exc:
        out={"status":"FAIL_CLOSED","deviations":[str(exc)]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],"deviations":out.get("deviations",[])}))
    return 0 if out["status"]=="PASS_EXACT_TRIDENT_RETURN_KINEMATICS_BOUNDED" else 2

if __name__=="__main__":
    sys.exit(main())
