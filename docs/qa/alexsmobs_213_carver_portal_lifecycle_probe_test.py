#!/usr/bin/env python3
"""Synthetic regression and fail-closed tests for the 2.1.13 portal auditor."""
import copy
import unittest

from alexsmobs_213_carver_portal_lifecycle_probe import (
    CARVER, PORTAL, MAX_METHODS, MAX_REFS_METHOD, PortalProbeError,
    projection, selected_method, bounded_operator_window, verify_snapshot,
)

def ins(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": operand,
            "symbol": symbol}

def method(name, rows):
    return {"header": "public void "+name+"();", "descriptor": "()V",
            "instructions": rows}

def pair():
    items = {}
    for name in ("onUseTick", "use", "onPortalOpen", "releaseUsingImpl",
                 "rayTracePortal", "getUseDuration"):
        rows = [ins(0, "return")]
        if name == "onUseTick":
            rows=[ins(0,"new","#3","class com/github/alexthe666/alexsmobs/entity/EntityVoidPortal"),
                  ins(3,"invokestatic","#4","Method Level.addFreshEntity:(LEntity;)Z"),
                  ins(6,"return")]
        items[name] = method(name, rows)
    portal = method("tick", [
        ins(0, "aload_0"),
        ins(1, "getfield", "#3", "Field lifespan:I"),
        ins(4, "ifeq", "11"),
        ins(7, "invokevirtual", "#8", "Method Entity.discard:()V"),
        ins(11, "return"),
    ])
    return {CARVER: list(items.values()), PORTAL: [portal]}

class PortalLifecycleProbeTests(unittest.TestCase):
    def test_select_exact_native_reference_and_context(self):
        m=method("tick",[ins(0,"aload_0"),ins(1,"getfield","#2","Field lifespan:I"),
                         ins(4,"ifeq","11"),ins(7,"return"),ins(11,"return")])
        p=selected_method(m)
        self.assertEqual(len(p["references"]),1)
        self.assertEqual(p["references"][0]["site"]["offset"],1)
        self.assertEqual(p["references"][0]["predecessor"]["opcode"],"aload_0")
        self.assertEqual(p["references"][0]["successor"]["opcode"],"ifeq")
        self.assertEqual(p["branches"][0]["branch_target"],11)

    def test_two_class_projection_captures_carver_and_portal(self):
        p=projection(pair())
        self.assertEqual([v["class_path"] for v in p["classes"]],[CARVER,PORTAL])
        self.assertEqual(p["classes"][0]["selected_method_count"],6)
        self.assertEqual(p["classes"][1]["selected_method_count"],1)

    def test_duplicate_offsets_are_rejected(self):
        m=method("tick",[ins(0,"return"),ins(0,"return")])
        with self.assertRaisesRegex(PortalProbeError,"duplicated/reordered"):
            selected_method(m)

    def test_reordered_offsets_are_rejected(self):
        m=method("tick",[ins(3,"return"),ins(0,"return")])
        with self.assertRaisesRegex(PortalProbeError,"duplicated/reordered"):
            selected_method(m)

    def test_bad_branch_target_rejected(self):
        m=method("tick",[ins(0,"ifne","not-an-integer"),ins(3,"return")])
        with self.assertRaisesRegex(PortalProbeError,"unparseable"):
            selected_method(m)

    def test_missing_documented_carver_member_rejected(self):
        d=pair()
        d[CARVER]=d[CARVER][1:]
        with self.assertRaisesRegex(PortalProbeError,"Carver method missing"):
            projection(d)

    def test_missing_portal_lifecycle_candidate_rejected(self):
        d=pair()
        d[PORTAL]=[method("helper",[ins(0,"return")])]
        with self.assertRaisesRegex(PortalProbeError,"lifecycle method discovery empty"):
            projection(d)

    def test_missing_link_from_carver_to_portal_rejected(self):
        d=pair()
        d[CARVER][0]["instructions"][0]["symbol"]="class SomeUnrelatedProjectile"
        with self.assertRaisesRegex(PortalProbeError,"Carver portal reference"):
            projection(d)

    def test_duplicate_signature_rejected(self):
        d=pair()
        d[PORTAL].append(copy.deepcopy(d[PORTAL][0]))
        with self.assertRaisesRegex(PortalProbeError,"duplicated native JVM"):
            projection(d)

    def test_reference_budget_rejected(self):
        rows=[ins(i*3,"getfield","#5","Field lifespan:I")
              for i in range(MAX_REFS_METHOD+1)]
        with self.assertRaisesRegex(PortalProbeError,"unbounded native portal"):
            selected_method(method("tick",rows))

    def test_method_count_budget_rejected(self):
        d=pair()
        d[PORTAL]=[method("tick"+str(i),[ins(0,"return")])
                   for i in range(MAX_METHODS+1)]
        with self.assertRaisesRegex(PortalProbeError,"unbounded selected"):
            projection(d)

    def test_bounded_operator_window_filters_unrelated_bytecode(self):
        m=method("tick",[ins(0,"iload_1"),ins(1,"iconst_1"),
                         ins(2,"isub"),ins(3,"nop"),
                         ins(4,"invokevirtual","#2","Method getLifespan:()I"),
                         ins(7,"ifgt","11"),ins(10,"return"),ins(11,"return")])
        self.assertEqual([r["opcode"] for r in bounded_operator_window(m,0,12)],
                         ["iload_1","iconst_1","isub","invokevirtual","ifgt"])

    def test_oversize_operator_window_fails_closed(self):
        m=method("tick",[ins(0,"return")])
        with self.assertRaisesRegex(PortalProbeError,"unbounded lifecycle"):
            bounded_operator_window(m,0,200)

    def test_snapshot_is_strict_and_non_promotional(self):
        a={"scope":"read-only","static_perk_contract":"NOT_CERTIFIED",
           "mutation":"NO_MUTATION"}
        b=copy.deepcopy(a)
        b["mutation"]="MUTATED"
        self.assertIs(verify_snapshot(a,a),a)
        with self.assertRaisesRegex(PortalProbeError,"snapshot drift"):
            verify_snapshot(a,b)

if __name__=="__main__":
    unittest.main()
