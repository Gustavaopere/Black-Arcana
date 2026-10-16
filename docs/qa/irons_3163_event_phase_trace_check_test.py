#!/usr/bin/env python3
"""Synthetic-only cases: never a provider GameTest or physical measurement."""
import unittest
from irons_3163_event_phase_trace_check import assess, EXPECTED_SHA

PROVENANCE = ("[BLACK_ARCANA_ARROW_VOLLEY_QA] type=provider_fingerprint "
              "mod_id=irons_spellbooks status=OBSERVED "
              "file=irons_spellbooks-1.21.1-3.16.3.jar "
              "bytes=13890046 sha256=" + EXPECTED_SHA + " expected_match=true")
HEAD = "[BLACK_ARCANA_PHASE_QA] "
ROOT = (HEAD + "type=cast actor_slot=1 session_slot=1 "
        "classification=ROOT_CANDIDATE prior_recast=false tick=100 "
        "original_level=1 event_level_snapshot=1")
RECAST = (HEAD + "type=cast actor_slot=1 session_slot=1 "
          "classification=RECAST_CANDIDATE prior_recast=true tick=105 "
          "original_level=1 event_level_snapshot=1")
FOLLOWUP = (HEAD + "type=cast_followup actor_slot=1 session_slot=1 tick=100 "
            "recast_after=true mana_after_snapshot=80")
DAMAGE = (HEAD + "type=damage_followup attempt_slot=1 actor_slot=1 "
          "target_slot=1 tick=101 cancelled_event_snapshot=true "
          "post_hits=0 ambiguous=false iframe_at_event=0 iframe_at_post_tick=20")


def report(*events, fingerprint=PROVENANCE):
    return assess("\n".join([fingerprint, *events]))


class SyntheticEventPhaseTests(unittest.TestCase):
    def test_valid_candidate_root_and_damage_observation(self):
        result = report(ROOT, FOLLOWUP, DAMAGE)
        self.assertEqual("TRACE_CLASSIFIED_NOT_GAMETEST", result["result"])
        self.assertEqual(1, result["candidate_sessions"])

    def test_recast_not_a_second_root(self):
        result = report(ROOT, RECAST, FOLLOWUP)
        self.assertEqual(1, result["candidate_sessions"])
        self.assertEqual(2, result["cast_events"])
        self.assertEqual([], result["issues"])

    def test_missing_cast_followup_fails_closed(self):
        trace = report(ROOT, RECAST, FOLLOWUP)
        self.assertIn("MISSING_CAST_FOLLOWUP", trace["issues"])

    def test_wrong_followup_actor_fails_closed(self):
        bad = FOLLOWUP.replace("actor_slot=1", "actor_slot=2")
        trace = report(ROOT, bad)
        self.assertIn("FOLLOWUP_ACTOR_MISMATCH", trace["issues"])

    def test_duplicate_damage_attempt_id_fails_closed(self):
        trace = report(ROOT, FOLLOWUP, DAMAGE, DAMAGE)
        self.assertIn("DUPLICATE_DAMAGE_ATTEMPT", trace["issues"])

    def test_cancel_snapshot_with_post_hit_is_not_clean_evidence(self):
        bad = DAMAGE.replace("post_hits=0", "post_hits=1")
        trace = report(ROOT, FOLLOWUP, bad)
        self.assertIn("CANCEL_SNAPSHOT_POST_HIT_CONFLICT", trace["issues"])

    def test_missing_root_fails_closed(self):
        result = report(RECAST, FOLLOWUP)
        self.assertIn("MISSING_ROOT_FOR_RECAST", result["issues"])

    def test_orphan_recast_fails_closed(self):
        trace = RECAST.replace("session_slot=1", "session_slot=0").replace(
            "classification=RECAST_CANDIDATE", "classification=UNLINKED_RECAST")
        result = report(trace)
        self.assertIn("UNLINKED_RECAST_CANNOT_CREDIT_ROOT", result["issues"])

    def test_duplicate_root_fails_closed(self):
        result = report(ROOT, ROOT, FOLLOWUP)
        self.assertIn("SESSION_REQUIRES_EXACTLY_ONE_ROOT", result["issues"])

    def test_actor_collision_fails_closed(self):
        swapped = RECAST.replace("actor_slot=1", "actor_slot=2")
        result = report(ROOT, swapped, FOLLOWUP)
        self.assertIn("SESSION_ACTOR_CHANGED", result["issues"])

    def test_modified_fingerprint_fails_closed(self):
        result = report(ROOT, FOLLOWUP, fingerprint=PROVENANCE.replace(
            "expected_match=true", "expected_match=false"))
        self.assertIn("PROVIDER_FINGERPRINT_UNVERIFIED", result["issues"])

    def test_ambiguous_hits_fail_closed(self):
        result = report(ROOT, FOLLOWUP, DAMAGE.replace(
            "ambiguous=false", "ambiguous=true"))
        self.assertIn("AMBIGUOUS_HIT_CORRELATION", result["issues"])

    def test_multi_post_hit_fails_closed(self):
        result = report(ROOT, FOLLOWUP, DAMAGE.replace("post_hits=0", "post_hits=2"))
        self.assertIn("MULTIPLE_POST_HITS_IN_ONE_ATTEMPT", result["issues"])

    def test_no_events_fail_closed(self):
        result = report()
        self.assertIn("NO_OBSERVED_PHASE_EVENTS", result["issues"])

    def test_missing_required_field_must_raise(self):
        bad = ROOT.replace("prior_recast=false ", "")
        with self.assertRaises(ValueError):
            report(bad, FOLLOWUP)

    def test_nonmonotonic_recast_time_fails_closed(self):
        bad = RECAST.replace("tick=105", "tick=99")
        result = report(ROOT, bad, FOLLOWUP)
        self.assertIn("NONMONOTONIC_CAST_TIME", result["issues"])

    def test_inconsistent_recast_state_fails_closed(self):
        bad = RECAST.replace("prior_recast=true", "prior_recast=false")
        result = report(ROOT, bad, FOLLOWUP)
        self.assertIn("RECAST_WITHOUT_PROVIDER_STATE", result["issues"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
