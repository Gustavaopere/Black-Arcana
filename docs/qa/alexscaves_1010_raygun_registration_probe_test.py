#!/usr/bin/env python3
"""Synthetic fail-closed tests for read-only C2S candidate discovery."""
import hashlib
import unittest
from unittest.mock import patch
from alexscaves_1010_raygun_registration_probe import (
    PREFIX, PACKET, RAYGUN, RegistrationProbeError, discover_candidates,
    matching_method_refs, MAX_CANDIDATES, audit, NETWORK,
    require_native_registration_candidate
)


def bytecode(*tokens, version=65):
    return b"\xca\xfe\xba\xbe\x00\x00" + version.to_bytes(2, "big") + (
        b".".join(tokens))


class FakeArchive:
    def __init__(self, content):
        self.content = content

    def namelist(self):
        return list(self.content)

    def read(self, path):
        return self.content[path]


class RegistrationProbeSyntheticTests(unittest.TestCase):
    def fixture(self):
        return FakeArchive({
            RAYGUN: bytecode(b"UpdateItemTagMessage"),
            PACKET: bytecode(b"ACNetworkContext"),
            PREFIX + "server/message/OtherMessage.class": bytecode(b"irrelevant"),
            "othermod/Unrelated.class": bytecode(b"UpdateItemTagMessage"),
        })

    def test_exact_two_candidates_without_noise(self):
        paths = discover_candidates(self.fixture())
        self.assertEqual([p for p, _ in paths], sorted((PACKET, RAYGUN)))
        for path, digest in paths:
            self.assertEqual(digest, hashlib.sha256(self.fixture().read(path)).hexdigest())

    def test_rejects_absent_sender_or_packet(self):
        archive = self.fixture()
        del archive.content[RAYGUN]
        with self.assertRaisesRegex(RegistrationProbeError, "sender class"):
            discover_candidates(archive)

    def test_rejects_unexpected_bytecode_major(self):
        archive = self.fixture()
        archive.content[PACKET] = bytecode(b"ACNetworkContext", version=61)
        with self.assertRaisesRegex(RegistrationProbeError, "classfile major"):
            discover_candidates(archive)

    def test_rejects_duplicate_zip_member(self):
        archive = self.fixture()
        archive.namelist = lambda: list(archive.content) + [PACKET]
        with self.assertRaisesRegex(RegistrationProbeError, "duplicate ZIP"):
            discover_candidates(archive)

    def test_rejects_unbounded_candidate_population(self):
        archive = self.fixture()
        for i in range(MAX_CANDIDATES):
            archive.content[PREFIX + "server/message/Test" + str(i) + ".class"] = (
                bytecode(b"ACNetworkContext"))
        with self.assertRaisesRegex(RegistrationProbeError, "unbounded candidate"):
            discover_candidates(archive)

    def method(self, rows):
        return {"header": "public void handle()", "descriptor": "()V",
                "instructions": rows}

    def row(self, off, name, opcode="invokestatic"):
        return {"offset": off, "opcode": opcode, "operand": "#123",
                "symbol": "Method " + name + ":()V"}

    def test_literal_symbolic_refs_without_auth_claim(self):
        method = self.method([self.row(0, "UpdateItemTagMessage.handle"),
                              self.row(3, "OtherClass.unrelated"),
                              self.row(6, "ACNetworkContext.getSender")])
        item = matching_method_refs(method)
        self.assertEqual([r["offset"] for r in item["references"]], [0, 6])
        self.assertEqual(item["instruction_count"], 3)
        self.assertEqual(item["name"], "handle")
        self.assertEqual(len(item["parsed_method_sha256"]), 64)

    def test_nonmatching_method_has_no_claim(self):
        self.assertIsNone(matching_method_refs(self.method([
            self.row(0, "OtherClass.unrelated")])))

    def test_duplicate_instruction_offset_rejected(self):
        with self.assertRaisesRegex(RegistrationProbeError, "duplicate JVM"):
            matching_method_refs(self.method([
                self.row(0, "UpdateItemTagMessage.handle"),
                self.row(0, "ACNetworkContext.getSender")]))

    def test_reference_budget_rejected(self):
        with self.assertRaisesRegex(RegistrationProbeError, "unbounded per-method"):
            matching_method_refs(self.method([
                self.row(i, "UpdateItemTagMessage.handle") for i in range(71)]))

    def test_native_network_registration_candidates(self):
        records = [{"class_path": NETWORK, "methods_with_direct_symbolic_references": [
            {"name": "registerMessages"}, {"name": "lambda$registerPayloads$0"}]}]
        require_native_registration_candidate(records)

    def test_missing_native_network_registration_rejected(self):
        with self.assertRaisesRegex(RegistrationProbeError, "candidate missing"):
            require_native_registration_candidate([])

    def test_missing_second_payload_method_rejected(self):
        records = [{"class_path": NETWORK,
                    "methods_with_direct_symbolic_references": [
                        {"name": "registerMessages"}]}]
        with self.assertRaisesRegex(RegistrationProbeError, "references changed"):
            require_native_registration_candidate(records)

    def test_fail_closed_if_exact_publisher_not_available(self):
        with patch("alexscaves_1010_raygun_registration_probe.sha_file",
                   return_value=("bad", "bad", 0)):
            with self.assertRaisesRegex(RegistrationProbeError, "publisher identity"):
                audit("missing.jar", "javap", {"artifact": {}})


if __name__ == "__main__":
    unittest.main()
