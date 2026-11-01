#!/usr/bin/env python3
"""Fail-closed catalog gate for the two nuclear DamageSource variants.

This is an evidence/status consistency check, NOT runtime/physical verification.
The exact JAR and NeoForge bytecode must still pass the existing SHA-exact CI probe.
"""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
EVIDENCE = PROVIDER / "EXACT-NEOFORGE-TICKETS-21.1.248.json"
CERTIFICATES = ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
DAMAGE_IDS = ("intentional-game-design", "nuke")
PUBLISHER_SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
NEOFORGE_SHA256 = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"


class GateError(ValueError):
    """A technical card was promoted despite unresolved safety evidence."""


def require(ok, message):
    if not ok:
        raise GateError(message)


def selected_stack(publisher_paths, suffix, name):
    records = [r for r in publisher_paths if r["class_path"].endswith(suffix)]
    require(len(records) == 1, "missing/ambiguous publisher class: " + suffix)
    methods = [m for m in records[0]["selected_methods"] if m["name"] == name]
    require(len(methods) == 1, "missing/ambiguous JVM method: " + name)
    return {i["offset"]: i for i in methods[0]["selected_stack"]}


def gate(doc, ledger, cards, provider_index, damage_index):
    """Require blocked statuses while the exact compiled ticket categories differ.

    No inference about a persistent leak is made: the mismatch is static evidence
    and live tickets, controller registration and restart remain unobserved.
    """
    require(doc["publisher"]["sha256"] == PUBLISHER_SHA256, "unexpected publisher JAR")
    require(doc["neo"]["file_sha256"] == NEOFORGE_SHA256
            and doc["neo"]["version"] == "21.1.248", "unexpected NeoForge JAR/version")
    require(doc["native_release_ticket_bucket_mismatch"]
            == "CONFIRMED_SELECTED_STATIC_BRANCHES_NOT_LIVE_RUNTIME",
            "ticket mismatch evidence changed; reevaluate the gate before promotion")
    require(doc["actual_persistent_ticket_leak"] == "NOT_OBSERVED",
            "a live leak has been claimed without separate physical evidence")
    limits = doc["limits"]
    for key, expected in {
        "allow_mutation": False, "perk_contract": "NOT_CERTIFIED",
        "safe_mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
        "runtime_ticket_success": "NOT_OBSERVED",
        "controller_registration_and_callback": "NOT_CLOSED",
        "restart_reinstate_validation": "NOT_CLOSED",
        "integrated_claims_worldeffectpolicy": "NOT_VERIFIED",
    }.items():
        require(limits[key] == expected, "unsafe safety-state promotion: " + key)
    routes = doc["publisher_boolean_paths"]
    tick = selected_stack(routes, "/NuclearExplosionEntity.class", "tick")
    remove = selected_stack(routes, "/NuclearExplosionEntity.class", "remove")
    load = selected_stack(routes, "/NuclearExplosionEntity.class", "loadChunksAround")
    adapter = selected_stack(routes, "/ACPlatform.class", "forceChunk")
    require(tick[210]["opcode"] == "iconst_1" and "loadChunksAround" in tick[211]["symbol"],
            "acquisition branch changed")
    require(remove[23]["opcode"] == "iconst_0" and "loadChunksAround" in remove[24]["symbol"],
            "release branch changed")
    require(load[86]["opcode"] == load[87]["opcode"] == "iload_1"
            and "ACPlatform.forceChunk" in load[88]["symbol"],
            "add/ticking boolean forwarding changed")
    require("TicketController.forceChunk" in adapter[20]["symbol"]
            and adapter[23]["opcode"] == "pop", "ticket controller/return semantics changed")
    for damage in DAMAGE_IDS:
        cert = PROVIDER.name + "/damage-types/" + damage + ".md"
        require(cert not in ledger["objects"], "unearned static certification: " + damage)
        text = cards[damage]
        for required in ("NOT_CERTIFIED", "NOT_VERIFIED", "NOT_TESTED", "NO_MUTATION"):
            require(required in text, "lost explicit limit in " + damage + ": " + required)
        label = "Intentional Game Design" if damage == "intentional-game-design" else "Nuke"
        row = r"^\| ⚠️ \| " + re.escape(label) + r" \| .* \| ⚠️ pendente \|"
        for index_name, index in (("provider", provider_index), ("damage-types", damage_index)):
            require(re.search(row, index, re.M) is not None,
                    "unearned green index in " + index_name + ": " + damage)
    require("NO_MUTATION" in cards["nuke"] and "NO_MUTATION" in cards["intentional-game-design"],
            "two DamageSources must not be treated as independent mutation authority")


class NuclearTicketPromotionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.ledger = json.loads(CERTIFICATES.read_text(encoding="utf-8"))
        cls.cards = {s: (PROVIDER / "damage-types" / (s + ".md")).read_text(encoding="utf-8")
                     for s in DAMAGE_IDS}
        cls.provider_index = (PROVIDER / "INDEX.md").read_text(encoding="utf-8")
        cls.damage_index = (PROVIDER / "damage-types/INDEX.md").read_text(encoding="utf-8")

    def check(self, doc=None, ledger=None, cards=None, provider_index=None, damage_index=None):
        gate(doc if doc is not None else self.doc,
             ledger if ledger is not None else self.ledger,
             cards if cards is not None else self.cards,
             provider_index if provider_index is not None else self.provider_index,
             damage_index if damage_index is not None else self.damage_index)

    def test_current_exact_snapshot_remains_explicitly_blocked(self):
        self.check()

    def test_rejects_certificate_without_new_verified_evidence(self):
        changed = copy.deepcopy(self.ledger)
        changed["objects"][PROVIDER.name + "/damage-types/nuke.md"] = {"status": "COMPLETE_PERK_READY"}
        with self.assertRaisesRegex(GateError, "unearned static certification"):
            self.check(ledger=changed)

    def test_rejects_claimed_live_ticket_leak(self):
        changed = copy.deepcopy(self.doc)
        changed["actual_persistent_ticket_leak"] = "CONFIRMED"
        with self.assertRaisesRegex(GateError, "physical evidence"):
            self.check(doc=changed)

    def test_rejects_falsely_fixed_ticket_category(self):
        changed = copy.deepcopy(self.doc)
        changed["native_release_ticket_bucket_mismatch"] = "RESOLVED"
        with self.assertRaisesRegex(GateError, "reevaluate"):
            self.check(doc=changed)

    def test_rejects_unverified_mutating_hook(self):
        changed = copy.deepcopy(self.doc)
        changed["limits"]["safe_mutating_hook"] = "VERIFIED_CONTRACT"
        with self.assertRaisesRegex(GateError, "unsafe safety-state"):
            self.check(doc=changed)

    def test_rejects_green_damage_index(self):
        changed = self.damage_index.replace("| ⚠️ | Nuke |", "| ✅ | Nuke |")
        with self.assertRaisesRegex(GateError, "unearned green index"):
            self.check(damage_index=changed)

    def test_rejects_changed_compiled_boolean_forwarding(self):
        changed = copy.deepcopy(self.doc)
        route = next(r for r in changed["publisher_boolean_paths"]
                     if r["class_path"].endswith("/NuclearExplosionEntity.class"))
        method = next(m for m in route["selected_methods"] if m["name"] == "loadChunksAround")
        next(i for i in method["selected_stack"] if i["offset"] == 87)["opcode"] = "iconst_1"
        with self.assertRaisesRegex(GateError, "boolean forwarding"):
            self.check(doc=changed)


if __name__ == "__main__":
    unittest.main()
