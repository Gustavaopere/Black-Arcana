#!/usr/bin/env python3
"""Clean-room, SHA-exact Somake 1.0.9 mid-filter guard probe.

Reports only derived boolean/path facts, never vendor code, bytecode or assets.
Every failed assumption is NOT_PROVED; no gameplay/adapter approvals follow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_radius_consumers import (
    native_isvalidtarget_early_guards,
    native_isvalidtarget_branch_edges,
    certify_exact_native_target_cfg_109,
)

METHOD="isValidTarget"
DESC="(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"
CLASS="com.somake.somakespells.entity.FuneralBloomControllerEntity"
ALLY={
    "Method net/minecraft/world/entity/LivingEntity.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z",
    "Method net/minecraft/world/entity/Entity.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z",
}
def fail(reason: str, **facts)->dict:
    return {"status":"NOT_PROVED","reason":reason,**facts}

def load_slot(op:str):
    if re.fullmatch(r"aload_[0-3]",op):
        return int(op[-1])
    return None

def middle_guard(declared:list[tuple[str,str,list[str]]])->dict:
    """Certify only branches at JVM instruction indices 12 and 16.

    The rest of the method and actor roles are NOT inferred. Structural
    conditions are evaluated against the previous strict 41-opcode CFG gate.
    """
    matches=[body for name,desc,body in declared if name==METHOD and desc==DESC]
    if len(matches)!=1:return fail("missing_or_ambiguous_exact_method",match_count=len(matches))
    rows=opcode_rows(matches[0])
    if len(rows)!=41:return fail("unexpected_instruction_count",instruction_count=len(rows))
    ops=[op for _,op,_,_ in rows]
    if [ops[i] for i in [12,16,17,18]]!=["ifnull","ifeq","iconst_0","ireturn"]:
        return fail("branch_or_rejection_shape_changed",
                    branch_12=ops[12],branch_16=ops[16],
                    false_literal=ops[17],false_return=ops[18])
    # Both conditional branches must jump over the *same* immediate false
    # return and land on the existing continuation instruction #19.
    if any(rows[i][2].split(" ",1)[0]!=str(rows[19][0]) for i in (12,16)):
        return fail("branch_destinations_not_shared_continuation")
    if rows[8][1]!="if_acmpne" or rows[8][2].split(" ",1)[0]!=str(rows[11][0]):
        return fail("early_identity_branch_does_not_enter_middle_filter")
    reference=load_slot(ops[11])
    receiver=load_slot(ops[13])
    argument=load_slot(ops[14])
    summary={
        "null_test_operand_local":reference,
        "allied_receiver_local":receiver,
        "allied_argument_local":argument,
        "allied_invocation_symbol":rows[15][3] if ops[15].startswith("invoke") else None,
        "null_branch_skips_false_return":True,
        "nonallied_branch_skips_false_return":True,
        "false_on_nonnull_and_allied":True,
    }
    if reference is None or receiver is None or argument is None:
        return fail("middle_object_operands_not_direct_locals",**summary)
    if ops[15]!="invokevirtual" or rows[15][3] not in ALLY:
        return fail("native_alliance_invocation_not_exact",**summary)
    if len({rows[i][0] for i in (8,11,12,13,14,15,16,17,18,19)})!=10:
        return fail("duplicate_jvm_offsets")
    # Refuse unmodelled jumps into the middle guarded window.
    middle_pcs={r[0] for r in rows[11:19]}
    for i,(_,op,operand,_) in enumerate(rows):
        if i in (8,12,16):continue
        if op.startswith(("if","goto","jsr")):
            target=operand.split(" ",1)[0] if operand else ""
            if not target.isdecimal():return fail("unknown_branch_target")
            if int(target) in middle_pcs:return fail("outside_jump_to_middle_guard",from_instruction=i)
        if op in ("tableswitch","lookupswitch","ret","wide"):
            return fail("unsupported_control_instruction",index=i)
    return {
        "status":"PROVED_NATIVE_NONNULL_AND_ALLIED_REJECTS",
        "instruction_count":len(rows),
        "null_test_operand_local":reference,
        "allied_receiver_local":receiver,
        "allied_argument_local":argument,
        "ally_call":"LivingEntity.isAlliedTo(Entity):boolean",
        "skip_false_return_branches":["ifnull","ifeq"],
        "shared_continuation_index":19,
        "rejection_value":False,
        "logic":"if reference is non-null AND receiver.isAlliedTo(argument) is true, return false",
        "boundary":"Actor roles, other branches, PvP, gameplay and hook mutability NOT proved",
    }

def inspect(jar:Path)->dict:
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("wrong Somake 1.0.9 filename/size")
    sha=hashlib.sha1(jar.read_bytes()).hexdigest()
    if sha!=SHA1:raise GateError("Somake JAR hash mismatch")
    with zipfile.ZipFile(jar) as archive:
        members=archive.namelist()
        if len(members)!=len(set(members)):raise GateError("duplicate archive member")
        if CLASS.replace(".","/")+".class" not in members:raise GateError("native controller class missing")
        mods=archive.read("META-INF/neoforge.mods.toml")
        if len(mods)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",mods):
            raise GateError("wrong mod id")
    p=subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),CLASS],
                     capture_output=True,text=True,timeout=60,check=False)
    if p.returncode or len(p.stdout)>1_400_000:
        raise GateError("javap failure/unbounded output")
    declared=sections(p.stdout)
    edges=native_isvalidtarget_branch_edges(declared)
    early=native_isvalidtarget_early_guards(declared)
    certify_exact_native_target_cfg_109(edges,early)
    result=middle_guard(declared)
    return {
        "sha1":sha,"version":"1.0.9","mod_id":"somakespells",
        "previous_exact_cfg":"PASS_6_BRANCH_EDGES_AND_3_EARLY_REJECTIONS",
        "middle_guard":result,
        "constraints":"Static clean-room analysis only; NOT provider-loaded gameplay, mutator API or perk",
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",required=True,type=Path)
    a.add_argument("--output",required=True,type=Path)
    args=a.parse_args()
    evidence=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_NATIVE_MIDDLE_GUARDS",json.dumps(evidence["middle_guard"],sort_keys=True))
    print("SOMAKE_PREVIOUS_CFG",evidence["previous_exact_cfg"],evidence["sha1"])
if __name__=="__main__":
    main()
