#!/usr/bin/env python3
"""Synthetic fail-closed gates for inherited Minecraft engine discovery."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from alexscaves_1010_arrow_inherited_engine_probe import (
    require,pin_build_files,method_evidence,unique_candidates
)

def m(instructions):
    return {"header":"public void onHitEntity();",
            "descriptor":"()V","instructions":instructions}

def ins(at,op,symbol="",operand=""):
    return {"offset":at,"opcode":op,"symbol":symbol,"operand":operand}

class Tests(unittest.TestCase):
    def test_method_digest_and_causal_refs(self):
        data=method_evidence(m([ins(0,"aload_0"),ins(1,"invokevirtual","Method hurt:()Z"),
            ins(4,"ifeq","","10"),ins(7,"fconst_1"),ins(8,"return")]))
        self.assertEqual(data["instruction_count"],5)
        self.assertEqual(data["branch_count"],1)
        self.assertEqual(data["numeric_operand_count"],1)
        self.assertEqual(len(data["relevant_symbolic_refs"]),1)

    def test_duplicate_offsets_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            method_evidence(m([ins(0,"aload_0"),ins(0,"return")]))

    def test_oversized_method_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"oversized"):
            method_evidence(m([ins(i,"nop") for i in range(2501)]))

    def test_relevant_call_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"too many"):
            method_evidence(m([ins(i,"invokevirtual","Method getOwner:()V")
                               for i in range(151)]))

    def test_unique_candidates_deduplicated(self):
        a={"path":Path("x.jar"),"class_digests":{"abstract_arrow":"a","projectile":"b"}}
        b={"path":Path("y.jar"),"class_digests":{"projectile":"b","abstract_arrow":"a"}}
        c={"path":Path("z.jar"),"class_digests":{"abstract_arrow":"c","projectile":"b"}}
        self.assertEqual(len(unique_candidates([a,b,c])),2)

    def test_classpath_disambiguation(self):
        from alexscaves_1010_arrow_inherited_engine_probe import select_from_compile_classpath
        with TemporaryDirectory() as d:
            p=Path(d)
            a=p/"a.jar"
            b=p/"b.jar"
            from zipfile import ZipFile
            from alexscaves_1010_arrow_inherited_engine_probe import CLASSES
            for path,byte in ((a,b"a"),(b,b"b")):
                with ZipFile(path,"w") as z:
                    for member in CLASSES.values():
                        z.writestr(member,byte)
            values=[]
            (p/"compile.txt").write_text(str(a)+"\n",encoding="utf8")
            selected=select_from_compile_classpath(values,p/"compile.txt")
            import hashlib
            self.assertEqual(selected["class_digests"]["abstract_arrow"],
                             hashlib.sha256(b"a").hexdigest())
            (p/"compile.txt").write_text(str(a)+"\n"+str(b)+"\n",encoding="utf8")
            with self.assertRaisesRegex(ValueError,"multiple distinct"):
                select_from_compile_classpath(values,p/"compile.txt")

    def test_gradle_pins_exact(self):
        with TemporaryDirectory() as d:
            p=Path(d)
            (p/"gradle.properties").write_text(
                "minecraft_version=1.21.1\nneo_version=21.1.248\n")
            (p/"build.gradle").write_text(
                "id 'net.neoforged.moddev' version '2.0.144'")
            self.assertEqual(pin_build_files(p)["neoforge"],"21.1.248")
            (p/"gradle.properties").write_text(
                "minecraft_version=1.21.1\nneo_version=21.1.247\n")
            with self.assertRaisesRegex(ValueError,"NeoForge version drift"):
                pin_build_files(p)

if __name__=="__main__":
    unittest.main()
