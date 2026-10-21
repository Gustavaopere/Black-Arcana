#!/usr/bin/env python3
"""Synthetic Java 21 fixture tests, not evidence of physical provider behavior."""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "apprentice_audit", HERE / "apprentice_codex_binary_audit.py"
)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

FIXTURES = {
    "arcanebeam/ArcaneBeamEntity.java": """
package jp.aquafactory.apprenticecodex.spell.arcanebeam;
public class ArcaneBeamEntity {
    public int tickCount;
    public void tick() { if (tickCount % 5 != 0) damageHitTarget(null); }
    private void damageHitTarget(Object world) { }
}
""",
    "uniteluna/UniteLunaMoonEntity.java": """
package jp.aquafactory.apprenticecodex.spell.uniteluna;
public class UniteLunaMoonEntity {
    public void onAntiMagic(Object magic) { explodeByAntiMagic(); }
    private void explodeByAntiMagic() { applyBurstDamage(3.0f); }
    private void applyBurstDamage(float multiplier) { }
}
""",
    "paletteshift/PaletteShiftReceptionEvent.java": """
package jp.aquafactory.apprenticecodex.spell.paletteshift;
class PaletteShiftReceptionEvent {
    static class SpellPreCastEvent { void setCanceled(boolean value) { } }
    public static void onSpellPreCast(SpellPreCastEvent event) {
        applyPastelAffinity(); event.setCanceled(true);
    }
    private static void applyPastelAffinity() { }
}
""",
    "manamending/ManaMending.java": """
package jp.aquafactory.apprenticecodex.spell.manamending;
public class ManaMending {
    public static class ManaMendingCastData {
        private Object targetStack;
        public boolean matchesTarget(Object stack) { return targetStack == stack; }
    }
}
""",
}


class ExactClassfileAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.jar = self.root / module.EXPECTED_JAR
        source_files = []
        for path, source in FIXTURES.items():
            destination = self.root / "src" / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(source, encoding="utf-8")
            source_files.append(destination)
        classes = self.root / "classes"
        classes.mkdir()
        subprocess.run(
            ["javac", "-d", str(classes), *map(str, source_files)],
            check=True, capture_output=True, text=True, timeout=25,
        )
        with zipfile.ZipFile(self.jar, "w") as archive:
            archive.writestr(
                "META-INF/neoforge.mods.toml",
                '[[mods]]\nmodId="apprenticecodex"\nversion="0.9.7.1"\n',
            )
            for cls in classes.rglob("*.class"):
                archive.write(cls, cls.relative_to(classes).as_posix())
        self.sha = hashlib.sha1(self.jar.read_bytes()).hexdigest()

    def test_shape_checks_pass_on_synthetic_bytecode_only(self):
        report = module.audit_jar(self.jar, expected_sha1=self.sha)
        self.assertEqual("PASS", report["result"])
        self.assertEqual(4, len(report["checks"]))
        self.assertEqual(
            "EXACT_HASH_CLASSFILE_OPCODE_SHAPE_NOT_RUNTIME_QA",
            report["evidence_class"],
        )
        self.assertIn("live gameplay", report["not_proven"])
        self.assertEqual(self.sha, report["sha1"])

    def test_strict_installed_digest_rejects_test_fixture(self):
        with self.assertRaisesRegex(module.EvidenceError, "SHA-1 mismatch"):
            module.audit_jar(self.jar)

    def test_wrong_mod_id_rejected(self):
        with zipfile.ZipFile(self.jar) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        entries["META-INF/neoforge.mods.toml"] = b'[[mods]]\nmodId="differentmod"'
        with zipfile.ZipFile(self.jar, "w") as archive:
            for name, data in entries.items():
                archive.writestr(name, data)
        with self.assertRaisesRegex(module.EvidenceError, "metadata"):
            module.audit_jar(
                self.jar, expected_sha1=hashlib.sha1(self.jar.read_bytes()).hexdigest()
            )

    def test_invalid_zip_rejected(self):
        self.jar.write_bytes(b"not-a-zip")
        with self.assertRaises(zipfile.BadZipFile):
            module.audit_jar(
                self.jar, expected_sha1=hashlib.sha1(self.jar.read_bytes()).hexdigest()
            )

    def test_symlink_rejected(self):
        target = self.root / "other.jar"
        target.write_bytes(self.jar.read_bytes())
        self.jar.unlink()
        self.jar.symlink_to(target)
        with self.assertRaisesRegex(module.EvidenceError, "non-symlink"):
            module.audit_jar(self.jar, expected_sha1=self.sha)

    def test_missing_opcode_fails_closed(self):
        outputs = {
            key: subprocess.run(
                ["javap", "-c", "-p", "-classpath", str(self.jar), cls],
                capture_output=True, text=True, check=True,
            ).stdout
            for key, cls in module.CLASSES.items()
        }
        altered = {**outputs, "beam": outputs["beam"].replace("irem", "idiv")}
        checks = module.inspect_bytecode(altered)
        self.assertEqual(
            "UNPROVEN_OR_MISMATCH",
            checks["beam_remainder_nonzero_damage_path"]["status"],
        )
        self.assertEqual("PASS", checks["moon_antimagic_triggers_boosted_burst"]["status"])
        self.assertEqual("PASS", checks["mending_itemstack_reference_identity"]["status"])

    def test_no_javap_output_never_passes(self):
        checks = module.inspect_bytecode({key: "" for key in module.CLASSES})
        self.assertTrue(all(check["status"] != "PASS" for check in checks.values()))


if __name__ == "__main__":
    unittest.main()
