#!/usr/bin/env python3
"""Read-only minimal dedicated server bootstrap gate, never gameplay acceptance.

Official NeoForge 21.1.250 + Platform 1.3.3 + Vanilla Backport 1.1.7.10.
Log observations are insufficient to prove specific mixin transforms, hook
availability, active potion modifiers, or complete 589-mod profile.
No third-party source/assets are reused or uploaded.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import unittest

SUCCESS = re.compile(r"\bDone \([\d.]+s\)! For help, type \"help\"",re.I)
ERROR = re.compile(r"(?:Exception in thread|Error loading mods|ModLoadingException|MixinApplyError|InjectionError|Critical injection failure|FATAL.+(?:exception|mixin|error)|MixinTransformerError)", re.I)
LOADED = re.compile(r"(?:mod loading complete|Loading Minecraft .* with NeoForge|NeoForge.*21\.1\.250)",re.I)

def analyze(log: str, exit_code: int):
    completed=bool(SUCCESS.search(log))
    fatal=ERROR.search(log)
    names={name:bool(re.search(name,log,re.I)) for name in
           ("vanillabackport","platform","neoforge")}
    # A printed basename is NOT runtime registration by itself.
    mixin_mentions=sorted(set(re.findall(
        r"\b(?:EntityMixin|LivingEntityMixin|RangedAttributeMixin)\b",log)))
    plugin_load_notes=[name for name in ("vanillabackport.mixins.json",)
                       if name in log.lower()]
    markers={
        "server_reached_done":completed,
        "fatal_error_pattern":fatal.group(0) if fatal else None,
        "neoforge_startup_line_observed":bool(LOADED.search(log)),
        "mod_names_mentioned_in_log":names,
        "declared_mixin_config_mentioned_in_log":plugin_load_notes,
        "mixin_handler_class_names_mentioned_in_log":mixin_mentions,
    }
    if not completed:status="FAIL_CLOSED_SERVER_NOT_READY"
    elif fatal is not None:status="FAIL_CLOSED_SERVER_FATAL_SIGNAL"
    elif exit_code not in (0,124,143):status="FAIL_CLOSED_UNEXPECTED_EXIT_STATUS"
    elif not names["vanillabackport"] or not names["platform"]:
        status="FAIL_CLOSED_PROVIDER_NAMES_NOT_OBSERVED"
    else:status="PASS_VB_11710_MINIMAL_NEOFORGE_211250_BOOTSTRAP"
    return {
        "status":status,
        "evidence_class":"ISOLATED_MINIMAL_DEDICATED_SERVER_STARTUP_LOG_ONLY",
        "environment":{
            "minecraft":"1.21.1","neoforge":"21.1.250","platform":"1.3.3",
            "vanilla_backport":"1.1.7.10","server_variant":"dedicated/headless",
            "no_user_modpack":True,"no_user_world":True
        },
        "observations":markers,
        "exit_code":exit_code,
        "runtime_mixin_injection_applied":"NOT_VERIFIED",
        "runtime_spells_and_boots":"NOT_TESTED",
        "limitations":[
            "A Done line means minimal server startup only, not client or player QA.",
            "Mod name in a log does not prove successful attribute modifier application.",
            "Mixin verbose logging does not independently prove selector ordinal targets.",
            "No full modpack, Iron's Spellbooks, Backported Spellbooks, actual installed SHA, relog or multi-player.",
            "No external hook or permission to mutate provider-owned magic and movement runtime."
        ],
        "deviations":[] if status.startswith("PASS_") else [status],
    }

class Test(unittest.TestCase):
    @staticmethod
    def log():
        return (
           "[main/INFO] Loading Minecraft 1.21.1 with NeoForge 21.1.250\n"
           "[mod/INFO] Loaded mods vanillabackport 1.1.7.10 platform 1.3.3\n"
           '[Server thread/INFO] Done (8.761s)! For help, type "help"\n'
        )
    def test_success_bounded(self):
        self.assertTrue(analyze(self.log(),124)["status"].startswith("PASS_"))
    def test_false_if_boot_not_done(self):
        self.assertEqual(analyze(self.log().replace("Done (8.761s)!","not done"),124)["status"],
                         "FAIL_CLOSED_SERVER_NOT_READY")
    def test_fatal_after_done_rejected(self):
        self.assertEqual(analyze(self.log()+"MixinApplyError: failed\n",124)["status"],
                         "FAIL_CLOSED_SERVER_FATAL_SIGNAL")
    def test_missing_platform_rejected(self):
        self.assertEqual(analyze(self.log().replace("platform","library"),124)["status"],
                         "FAIL_CLOSED_PROVIDER_NAMES_NOT_OBSERVED")
    def test_wrong_exit_rejected(self):
        self.assertEqual(analyze(self.log(),1)["status"],
                         "FAIL_CLOSED_UNEXPECTED_EXIT_STATUS")
    def test_success_does_not_claim_mixin_applied(self):
        self.assertEqual(analyze(self.log()+"Mixing EntityMixin\n",124)[
                         "runtime_mixin_injection_applied"],"NOT_VERIFIED")
    def test_success_does_not_claim_gameplay(self):
        self.assertEqual(analyze(self.log(),0)["runtime_spells_and_boots"],"NOT_TESTED")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--log",type=Path)
    ap.add_argument("--exit-code",type=int)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.self_test:
        success=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Test))
        return 0 if success.wasSuccessful() else 1
    if args.log is None or args.exit_code is None or args.output is None:
        ap.error("--log, --exit-code and --output are required")
    try:
        report=analyze(args.log.read_text(encoding="utf-8",errors="replace"),
                       args.exit_code)
    except OSError as exc:
        report={"status":"FAIL_CLOSED_LOG_UNREADABLE","deviations":[str(exc)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"],
                      "observations":report.get("observations",{})}))
    return 0 if report["status"]=="PASS_VB_11710_MINIMAL_NEOFORGE_211250_BOOTSTRAP" else 2

if __name__=="__main__":
    sys.exit(main())
