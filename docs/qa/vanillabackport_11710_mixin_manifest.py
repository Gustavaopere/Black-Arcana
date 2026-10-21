#!/usr/bin/env python3
"""Fail-closed NeoForge mixin declaration audit on SHA-pinned Vanilla Backport JAR.

Checks packaged NeoForge TOML, exact Mixin JSON, and declared class entries.
Does NOT execute the Mixin transformer, prove injections applied at runtime,
certify multiplayer, or enable external perk mutations.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path
import sys
import tomllib
import unittest
from zipfile import ZipFile, BadZipFile

from vanillabackport_11710_mobility_bytecode import publisher_identity

TOML_PATH = "META-INF/neoforge.mods.toml"
MIXIN_PATH = "vanillabackport.mixins.json"
MIXIN_PACKAGE = "com.blackgear.vanillabackport.core.mixin"
SERVER_MIXINS = {
    "common.entities.EntityMixin": "net.minecraft.world.entity.Entity",
    "common.entities.LivingEntityMixin": "net.minecraft.world.entity.LivingEntity",
    "common.attributes.RangedAttributeMixin": "net.minecraft.world.entity.ai.attributes.RangedAttribute",
}
CLASS_ROOT = "com/blackgear/vanillabackport/core/mixin/"

def verify_manifest_text(mods_toml: bytes, config_json: bytes, names: set[str]):
    try:
        meta = tomllib.loads(mods_toml.decode("utf-8"))
        conf = json.loads(config_json.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("MIXIN_METADATA_PARSE_FAILURE: "+str(exc)) from exc

    mods = meta.get("mods", [])
    exact_mods = [m for m in mods if isinstance(m,dict) and m.get("modId")=="vanillabackport"]
    if len(exact_mods)!=1:
        raise ValueError(f"NEOFORGE_MOD_ID_MISSING_OR_AMBIGUOUS: {len(exact_mods)}")
    actual_version = exact_mods[0].get("version")
    if actual_version != "1.1.7.10":
        raise ValueError(f"NEOFORGE_MOD_VERSION_DRIFT: {actual_version!r}")

    mixin_entries = [m.get("config") for m in meta.get("mixins", [])
                     if isinstance(m,dict)]
    if mixin_entries.count(MIXIN_PATH) != 1:
        raise ValueError(f"NEOFORGE_MIXIN_CONFIG_NOT_UNIQUE: {mixin_entries!r}")
    if conf.get("package") != MIXIN_PACKAGE:
        raise ValueError("MIXIN_PACKAGE_DRIFT")
    if conf.get("required") is not True or conf.get("compatibilityLevel")!="JAVA_21":
        raise ValueError("MIXIN_REQUIRED_OR_JAVA_LEVEL_DRIFT")
    if conf.get("injectors",{}).get("defaultRequire") != 1:
        raise ValueError("MIXIN_DEFAULT_REQUIRE_DRIFT")

    active=conf.get("mixins")
    client=conf.get("client")
    if not isinstance(active,list) or not isinstance(client,list):
        raise ValueError("MIXIN_SIDE_LIST_INVALID")
    if len(active)!=len(set(active)) or len(client)!=len(set(client)):
        raise ValueError("MIXIN_DUPLICATE_DECLARATION")
    for relative, target in SERVER_MIXINS.items():
        if active.count(relative) != 1 or relative in client:
            raise ValueError("SERVER_MOBILITY_MIXIN_MISSING_OR_CLIENT_ONLY: "+relative)
        classfile=CLASS_ROOT+relative.replace(".","/")+".class"
        if classfile not in names:
            raise ValueError("DECLARED_MOBILITY_MIXIN_CLASS_MISSING: "+classfile)
    if MIXIN_PATH not in names or TOML_PATH not in names:
        raise ValueError("DECLARED_MIXIN_RESOURCES_MISSING")

    if meta.get("modLoader") != "javafml":
        raise ValueError("NEOFORGE_MODLOADER_DRIFT")
    deps=meta.get("dependencies",{}).get("vanillabackport",[])
    required_deps=[v for v in deps if isinstance(v,dict) and v.get("type")=="required"]
    actual_dep_ids={v.get("modId") for v in required_deps}
    expected_ranges={
        "neoforge":"[21.1,)",
        "minecraft":"[1.21.1,)",
        "platform":"[1.3.3,)",
    }
    if not set(expected_ranges).issubset(actual_dep_ids):
        raise ValueError("REQUIRED_NEOFORGE_PROVIDER_DEPS_MISSING: "+repr(actual_dep_ids))
    for dep, expected_range in expected_ranges.items():
        matches=[v for v in required_deps if v.get("modId")==dep]
        if len(matches)!=1 or matches[0].get("versionRange") != expected_range:
            raise ValueError(f"REQUIRED_DEP_VERSION_RANGE_DRIFT: {dep}")
        if matches[0].get("side")!="BOTH":
            raise ValueError(f"REQUIRED_DEP_SIDE_DRIFT: {dep}")
    return {
        "declaration_status":"PACKAGED_NEOFORGE_MIXIN_CONFIG_DECLARED",
        "mod_id":"vanillabackport",
        "mod_version":actual_version,
        "loader_config":TOML_PATH,
        "mixin_config":MIXIN_PATH,
        "required":True,
        "compatibility_level":"JAVA_21",
        "default_require":1,
        "required_dependencies":{k:expected_ranges[k] for k in sorted(expected_ranges)},
        "declared_common_mixins":[
            {"class":MIXIN_PACKAGE+"."+rel,
             "target_in_source":target,
             "class_file_present":True,
             "listed_in_common_mixins":True,
             "runtime_applied":"NOT_VERIFIED"}
            for rel,target in SERVER_MIXINS.items()
        ],
        "important_limit":"class presence plus config link is not proof of successful mixin transformation at run time"
    }

def verify_archive(jar:Path):
    identity=publisher_identity(jar)
    with ZipFile(jar) as z:
        files=set(z.namelist())
        if TOML_PATH not in files:
            raise ValueError("NEOFORGE_MODS_TOML_MISSING")
        if MIXIN_PATH not in files:
            raise ValueError("MIXIN_JSON_MISSING")
        report=verify_manifest_text(z.read(TOML_PATH),z.read(MIXIN_PATH),files)
    return {
        "status":"PASS_VANILLABACKPORT_11710_MIXIN_MANIFEST_BOUNDARY",
        "publisher":identity,
        "evidence_class":"EXACT_PUBLISHER_PACKAGED_CONFIG_AND_CLASS_PRESENCE",
        "manifest":report,
        "limitations":[
            "Does not prove Java Mixin annotation target or bytecode injection was applied.",
            "Does not execute NeoForge/Platform loader bootstrap or check modpack mixin conflicts.",
            "Does not prove same SHA is installed on user machine.",
            "Does not certify player travel, bouncing, item equipment, or any perk API."
        ],
        "deviations":[]
    }

class ManifestRegression(unittest.TestCase):
    @staticmethod
    def fixture(*, remove:str|None=None, client_only:bool=False,
                version:str="1.1.7.10", duplicate:bool=False,
                default_require:int=1, required:bool=True):
        toml=(
            'modLoader = "javafml"\n'
            '[[mods]]\nmodId = "vanillabackport"\nversion = "'+version+'"\n'
            '[[mixins]]\nconfig = "'+MIXIN_PATH+'"\n'
            '[[dependencies.vanillabackport]]\nmodId = "neoforge"\ntype = "required"\nversionRange = "[21.1,)"\nside = "BOTH"\n'
            '[[dependencies.vanillabackport]]\nmodId = "minecraft"\ntype = "required"\nversionRange = "[1.21.1,)"\nside = "BOTH"\n'
            '[[dependencies.vanillabackport]]\nmodId = "platform"\ntype = "required"\nversionRange = "[1.3.3,)"\nside = "BOTH"\n'
        ).encode()
        active=list(SERVER_MIXINS)
        client=[]
        if remove:
            active.remove(remove)
            if client_only:client.append(remove)
        if duplicate:
            active.append(active[0])
        conf={
            "required":required,
            "package":MIXIN_PACKAGE,
            "compatibilityLevel":"JAVA_21",
            "mixins":active,
            "client":client,
            "injectors":{"defaultRequire":default_require}
        }
        names={TOML_PATH,MIXIN_PATH,*[
            CLASS_ROOT+x.replace(".","/")+".class" for x in SERVER_MIXINS
        ]}
        return toml,json.dumps(conf).encode(),names

    def test_manifest_accepts_expected_common_and_required_mixins(self):
        args=self.fixture()
        d=verify_manifest_text(*args)
        self.assertEqual(len(d["declared_common_mixins"]),3)
    def test_missing_entity_mixin_rejected(self):
        with self.assertRaisesRegex(ValueError,"SERVER_MOBILITY_MIXIN_MISSING"):
            verify_manifest_text(*self.fixture(remove="common.entities.EntityMixin"))
    def test_mixin_client_only_rejected(self):
        with self.assertRaisesRegex(ValueError,"SERVER_MOBILITY_MIXIN_MISSING"):
            verify_manifest_text(*self.fixture(remove="common.entities.LivingEntityMixin",client_only=True))
    def test_wrong_version_rejected(self):
        with self.assertRaisesRegex(ValueError,"NEOFORGE_MOD_VERSION_DRIFT"):
            verify_manifest_text(*self.fixture(version="1.2.0"))
    def test_duplicate_mixin_rejected(self):
        with self.assertRaisesRegex(ValueError,"MIXIN_DUPLICATE_DECLARATION"):
            verify_manifest_text(*self.fixture(duplicate=True))
    def test_default_require_zero_rejected(self):
        with self.assertRaisesRegex(ValueError,"MIXIN_DEFAULT_REQUIRE_DRIFT"):
            verify_manifest_text(*self.fixture(default_require=0))
    def test_not_required_rejected(self):
        with self.assertRaisesRegex(ValueError,"MIXIN_REQUIRED_OR_JAVA_LEVEL_DRIFT"):
            verify_manifest_text(*self.fixture(required=False))
    def test_missing_mixin_class_rejected(self):
        t,j,n=self.fixture()
        n.remove(CLASS_ROOT+"common/attributes/RangedAttributeMixin.class")
        with self.assertRaisesRegex(ValueError,"DECLARED_MOBILITY_MIXIN_CLASS_MISSING"):
            verify_manifest_text(t,j,n)
    def test_missing_required_loader_dependency_rejected(self):
        t,j,n=self.fixture()
        t=t.replace(b'modId = "platform"',b'modId = "optionalplatform"')
        with self.assertRaisesRegex(ValueError,"REQUIRED_NEOFORGE_PROVIDER_DEPS_MISSING"):
            verify_manifest_text(t,j,n)
    def test_platform_minimum_version_range_drift_rejected(self):
        t,j,n=self.fixture()
        t=t.replace(b'versionRange = "[1.3.3,)"',b'versionRange = "[1.3.2,)"')
        with self.assertRaisesRegex(ValueError,"REQUIRED_DEP_VERSION_RANGE_DRIFT"):
            verify_manifest_text(t,j,n)
    def test_required_dependency_wrong_side_rejected(self):
        t,j,n=self.fixture()
        t=t.replace(b'side = "BOTH"', b'side = "CLIENT"', 1)
        with self.assertRaisesRegex(ValueError,"REQUIRED_DEP_SIDE_DRIFT"):
            verify_manifest_text(t,j,n)
    def test_wrong_publisher_identity_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as root:
            f=Path(root)/"incorrect.jar"
            f.write_bytes(b"not-jar")
            with self.assertRaisesRegex(ValueError,"PUBLISHER_SIZE_DRIFT"):
                verify_archive(f)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--jar",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.self_test:
        r=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(ManifestRegression))
        return 0 if r.wasSuccessful() else 1
    if not args.jar or not args.output:
        ap.error("--jar and --output required")
    try:
        d=verify_archive(args.jar)
    except (OSError, ValueError, BadZipFile) as exc:
        d={"status":"FAIL_CLOSED","deviations":[str(exc)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":d["status"],"deviations":d["deviations"]}))
    return 0 if d["status"]=="PASS_VANILLABACKPORT_11710_MIXIN_MANIFEST_BOUNDARY" else 2

if __name__=="__main__":
    sys.exit(main())
