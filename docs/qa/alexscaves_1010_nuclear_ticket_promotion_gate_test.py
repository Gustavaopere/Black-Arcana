#!/usr/bin/env python3
"""Fail-closed catalog gate for the two nuclear DamageSource variants.

This is an evidence/status consistency check, NOT runtime/physical verification.
The exact JAR and NeoForge bytecode must still pass the existing SHA-exact CI probe.
"""
import copy
import hashlib
import json
import re
import unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest, validate_structure, validate_cards

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
EVIDENCE = PROVIDER / "EXACT-NEOFORGE-TICKETS-21.1.248.json"
CERTIFICATES = ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
CONTRACT = PROVIDER / "EXACT-NUCLEAR-CONTRACTS-1.0.10.json"
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


def gate(doc, ledger, cards, provider_index, damage_index, static_contract=None):
    """Preserve the exact runtime blocker; allow only a fully sealed static scope.

    Status promotion requires both cards and the independently audited nuclear
    contract. No ticket fix, live leak, physical acceptance or mutation follows.
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
        "unload_crash_and_dimension_transition": "NOT_TESTED",
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
    keys = {damage: PROVIDER.name + "/damage-types/" + damage + ".md" for damage in DAMAGE_IDS}
    present = {damage for damage, key in keys.items() if key in ledger["objects"]}
    require(not present or present == set(DAMAGE_IDS), "unearned static certification: partial nuclear pair")
    if present:
        require(static_contract is not None, "unearned static certification: missing consolidated seal")
        try:
            validate_structure(static_contract, profile="nuclear")
            validate_cards(static_contract, PROVIDER, profile="nuclear")
        except (ValueError, OSError, KeyError, TypeError) as error:
            raise GateError("unearned static certification: invalid consolidated seal") from error
        expected_fields = {
            "status": "COMPLETE_PERK_READY", "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
            "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR", "version": "1.0.10",
            "artifact_sha1": static_contract["artifact_sha1"],
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
        }
        axes = {"identity", "behavior", "parameters", "targeting", "costs", "integration", "validation"}
        for damage, key in keys.items():
            cert = ledger["objects"][key]
            require(isinstance(cert, dict) and all(cert.get(k) == v for k, v in expected_fields.items()),
                    "unearned static certification: incomplete or unsafe record: " + damage)
            relative = "damage-types/" + damage + ".md"
            require(static_contract["cards"][relative] == hashlib.sha256(cards[damage].encode("utf-8")).hexdigest(),
                    "unearned static certification: card text drift: " + damage)
            evidence = cert.get("evidence", {})
            require(isinstance(evidence, dict) and set(evidence) == axes, "unearned static certification: missing evidence axis: " + damage)
            for item in evidence.values():
                require(isinstance(item, dict) and set(item) == {"path", "reason"}
                        and item["path"] == "wiki/modpack-catalog/providers/" + key
                        and isinstance(item["reason"], str) and bool(item["reason"].strip()),
                        "unearned static certification: wrong evidence path/reason: " + damage)
    for damage in DAMAGE_IDS:
        text = cards[damage]
        required_state = "STATIC_TECHNICAL_CATALOG_ONLY" if present else "NOT_CERTIFIED"
        for required in (required_state, "NOT_VERIFIED", "NOT_TESTED", "NO_MUTATION"):
            require(required in text, "lost explicit limit in " + damage + ": " + required)
        if present:
            for required in ("CONFIRMED_SELECTED_STATIC_BRANCHES_NOT_LIVE_RUNTIME", "NOT_OBSERVED"):
                require(required in text, "lost explicit ticket mismatch limit: " + damage)
        label = "Intentional Game Design" if damage == "intentional-game-design" else "Nuke"
        status, contract = ("✅", "✅ certificado") if present else ("⚠️", "⚠️ pendente")
        for index_name, index in (("provider", provider_index), ("damage-types", damage_index)):
            rows = []
            for line in index.splitlines():
                if not line.strip().startswith("|"):
                    continue
                cells = [value.strip() for value in line.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[1] == label:
                    rows.append(cells)
            require(len(rows) == 1 and len(rows[0]) == 6
                    and rows[0][0] == status
                    and rows[0][3:] == [contract, "⚠️ não verificado", "⚠️ não testado"],
                    "unearned green index or runtime status in " + index_name + ": " + damage)



class NuclearTicketPromotionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.ledger = json.loads(CERTIFICATES.read_text(encoding="utf-8"))
        cls.cards = {s: (PROVIDER / "damage-types" / (s + ".md")).read_text(encoding="utf-8")
                     for s in DAMAGE_IDS}
        cls.provider_index = (PROVIDER / "INDEX.md").read_text(encoding="utf-8")
        cls.damage_index = (PROVIDER / "damage-types/INDEX.md").read_text(encoding="utf-8")
        cls.static_contract = load_manifest(CONTRACT) if CONTRACT.exists() else None

    def check(self, doc=None, ledger=None, cards=None, provider_index=None, damage_index=None,
              static_contract="CURRENT"):
        if static_contract == "CURRENT":
            static_contract = self.static_contract
        gate(doc if doc is not None else self.doc,
             ledger if ledger is not None else self.ledger,
             cards if cards is not None else self.cards,
             provider_index if provider_index is not None else self.provider_index,
             damage_index if damage_index is not None else self.damage_index,
             static_contract=static_contract)

    def test_current_snapshot_keeps_runtime_blocked_with_consistent_catalog_state(self):
        self.check()

    def test_rejects_certificate_without_new_verified_evidence(self):
        changed = copy.deepcopy(self.ledger)
        changed["objects"][PROVIDER.name + "/damage-types/nuke.md"] = {"status": "COMPLETE_PERK_READY"}
        with self.assertRaisesRegex(GateError, "unearned static certification"):
            self.check(ledger=changed, static_contract=None)

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
        ledger = copy.deepcopy(self.ledger)
        for damage in DAMAGE_IDS:
            ledger["objects"].pop(PROVIDER.name + "/damage-types/" + damage + ".md", None)
        with self.assertRaisesRegex(GateError, "unearned green index"):
            cards = {damage: "NOT_CERTIFIED NOT_VERIFIED NOT_TESTED NO_MUTATION" for damage in DAMAGE_IDS}
            self.check(ledger=ledger, cards=cards, damage_index=changed, static_contract=None)

    def test_current_static_scope_has_both_cards_and_a_consolidated_manifest(self):
        self.assertIsNotNone(self.static_contract)
        for damage in DAMAGE_IDS:
            self.assertIn(PROVIDER.name + "/damage-types/" + damage + ".md", self.ledger["objects"])
        self.check()

    def test_pending_pair_remains_valid_without_a_static_manifest(self):
        ledger = copy.deepcopy(self.ledger)
        for damage in DAMAGE_IDS:
            ledger["objects"].pop(PROVIDER.name + "/damage-types/" + damage + ".md", None)
        cards = {damage: "NOT_CERTIFIED NOT_VERIFIED NOT_TESTED NO_MUTATION" for damage in DAMAGE_IDS}
        def pending(index):
            for label in ("Intentional Game Design", "Nuke"):
                lines = index.splitlines()
                for number, line in enumerate(lines):
                    if "| " + label + " |" in line:
                        lines[number] = line.replace("| ✅ |", "| ⚠️ |", 1).replace("✅ certificado", "⚠️ pendente")
                index = "\n".join(lines)
            return index
        self.check(ledger=ledger, cards=cards, provider_index=pending(self.provider_index),
                   damage_index=pending(self.damage_index), static_contract=None)

    def test_rejects_partial_static_pair_or_missing_axis(self):
        for mutation in ("partial", "axis", "reason", "path", "hook", "qa"):
            ledger = copy.deepcopy(self.ledger)
            key = PROVIDER.name + "/damage-types/nuke.md"
            cert = ledger["objects"][key]
            if mutation == "partial": ledger["objects"].pop(key)
            elif mutation == "axis": cert["evidence"].pop("costs")
            elif mutation == "reason": cert["evidence"]["costs"]["reason"] = " "
            elif mutation == "path": cert["evidence"]["costs"]["path"] = "outside.md"
            elif mutation == "hook": cert["mutating_hook"] = "VERIFIED"
            else: cert["physical_qa"] = "PASS"
            with self.subTest(mutation=mutation), self.assertRaisesRegex(GateError, "unearned static certification"):
                self.check(ledger=ledger)

    def test_rejects_manifest_tampering_and_card_text_drift(self):
        for key, value in (("catalog_family", "OTHER"), ("physical_qa", "PASS"),
                           ("provider_universe_closed", True)):
            manifest = copy.deepcopy(self.static_contract)
            manifest[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(GateError, "unearned static certification"):
                self.check(static_contract=manifest)
        cards = dict(self.cards)
        cards["nuke"] += "\nchanged after seal\n"
        with self.assertRaisesRegex(GateError, "card text drift"):
            self.check(cards=cards)

    def test_rejects_green_runtime_index_even_with_static_certificate(self):
        changed = self.damage_index.replace("⚠️ não testado", "✅ testado")
        with self.assertRaisesRegex(GateError, "runtime status"):
            self.check(damage_index=changed)

    def test_rejects_duplicate_or_extra_column_index_rows(self):
        row = next(line for line in self.damage_index.splitlines() if "| Nuke |" in line)
        for changed in (self.damage_index + "\n" + row,
                        self.damage_index.replace(row, row + " extra |")):
            with self.subTest(changed=changed[-120:]), self.assertRaisesRegex(GateError, "runtime status"):
                self.check(damage_index=changed)

    def test_rejects_claimed_unload_crash_or_transition_acceptance(self):
        changed = copy.deepcopy(self.doc)
        changed["limits"]["unload_crash_and_dimension_transition"] = "PASS"
        with self.assertRaisesRegex(GateError, "unsafe safety-state"):
            self.check(doc=changed)

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
