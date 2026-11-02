#!/usr/bin/env python3
"""Synthetic classfile-annotation tests; not a physical modpack QA substitute."""
import copy
import struct
import unittest
from ftbchunks_2101_blockstate_mixin_probe import (
    AuditError, Buffer, Classfile, verify_seal, SCOPE
)

def u2(n):return struct.pack(">H",n)
def u4(n):return struct.pack(">I",n)

def make_class(*, annotated=True, duplicate_annotation=False, target_method=True,
               invalid_magic=False, extra=b""):
    cp=[]
    def utf(value):
        b=value.encode()
        cp.append(b"\x01"+u2(len(b))+b)
        return len(cp)
    def cls(idx):
        cp.append(b"\x07"+u2(idx))
        return len(cp)
    name=utf("sample/BlockStateMixin")
    this=cls(name)
    obj_name=utf("java/lang/Object")
    super_cls=cls(obj_name)
    method_name=utf("testMethod")
    desc=utf("()V")
    code_name=utf("Code")
    ann_attr=utf("RuntimeVisibleAnnotations")
    ann_name=utf("Lorg/spongepowered/asm/mixin/Mixin;")
    element_name=utf("targets")
    value=utf("net.minecraft.world.level.block.state.BlockBehaviour$BlockStateBase")
    inject_ann=utf("Lorg/spongepowered/asm/mixin/injection/Inject;")
    class_annotation=(u2(ann_name)+u2(1)+u2(element_name)+b"s"+u2(value))
    class_ann_attr=u2(ann_attr)+u4(2+len(class_annotation)) + u2(1)+class_annotation
    method_annotation=u2(inject_ann)+u2(0)
    method_ann_bytes=u2(1)+method_annotation
    method_ann_attr=u2(ann_attr)+u4(len(method_ann_bytes))+method_ann_bytes
    code_bytes=b"\xb1"
    code_attr_value=u2(0)+u2(1)+u4(len(code_bytes))+code_bytes+u2(0)+u2(0)
    code_attr=u2(code_name)+u4(len(code_attr_value))+code_attr_value
    attrs=code_attr+(method_ann_attr if target_method else b"")
    method=u2(1)+u2(method_name)+u2(desc)+u2(1+int(target_method))+attrs
    annotations=(class_ann_attr if annotated else b"")
    return ((b"\x00\x00\x00\x00" if invalid_magic else b"\xca\xfe\xba\xbe")+
            u2(0)+u2(61)+u2(len(cp)+1)+b"".join(cp)+
            u2(0x21)+u2(this)+u2(super_cls)+u2(0)+u2(0)+
            u2(1)+method+u2(int(annotated))+annotations+extra)

class BlockStateMixinMetadataTests(unittest.TestCase):
    def test_classfile_annotations_and_method_code_hash(self):
        j=Classfile(make_class()).summary()
        self.assertEqual(j["method_count"],1)
        self.assertEqual(j["field_count"],0)
        self.assertIn("Lorg/spongepowered/asm/mixin/Mixin;",j["annotation_types"])
        self.assertIn("Lorg/spongepowered/asm/mixin/injection/Inject;",j["annotation_types"])
        self.assertEqual(j["methods"][0]["code"]["bytecode_size"],1)
        self.assertEqual(j["class_annotations"][0]["annotation"]["elements"]["targets"],
                         "net.minecraft.world.level.block.state.BlockBehaviour$BlockStateBase")

    def test_no_methods_marked_injection_without_annotation(self):
        j=Classfile(make_class(target_method=False)).summary()
        self.assertEqual(j["methods"][0]["annotations"],[])
        self.assertEqual(len(j["class_annotations"]),1)

    def test_wrong_magic_fails_closed(self):
        with self.assertRaisesRegex(AuditError,"JVM magic"):
            Classfile(make_class(invalid_magic=True))

    def test_truncated_classfile_fails_closed(self):
        with self.assertRaisesRegex(AuditError,"truncated"):
            Classfile(make_class()[:-4])

    def test_extra_bytes_fails_closed(self):
        with self.assertRaisesRegex(AuditError,"trailing bytes"):
            Classfile(make_class(extra=b"x"))

    def test_unsupported_constant_tag_rejected(self):
        raw=bytearray(make_class())
        raw[10]=99
        with self.assertRaisesRegex(AuditError,"constant pool tag"):
            Classfile(raw)

    def test_annotation_is_optional_not_automatic_injection(self):
        j=Classfile(make_class(annotated=False,target_method=False)).summary()
        self.assertEqual(j["annotation_types"],[])

    def test_manifest_drift_rejected(self):
        report={"scope":SCOPE,"class":{"annotations":[]}}
        self.assertTrue(verify_seal(report,copy.deepcopy(report)))
        bad=copy.deepcopy(report)
        bad["class"]["annotations"].append("invented")
        with self.assertRaisesRegex(AuditError,"seal drift"):
            verify_seal(report,bad)

    def test_wrong_scope_rejected(self):
        with self.assertRaisesRegex(AuditError,"scope"):
            verify_seal({"scope":SCOPE},{"scope":"other"})

    def test_buffer_read_bounds(self):
        b=Buffer(b"\x01\x02")
        self.assertEqual(b.u2(),258)
        with self.assertRaisesRegex(AuditError,"truncated"):
            b.u1()

if __name__=="__main__":
    unittest.main()
