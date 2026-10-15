#!/usr/bin/env python3
"""Synthetic-only tests of log classification. Never counted as game observations."""
import unittest

from irons_3163_arrow_volley_observation_check import evaluate

TAG = "[BLACK_ARCANA_ARROW_VOLLEY_QA]"
UUID = "00000000-0000-4000-8000-000000000001"


def simulated_log(level=1, **overrides):
    rows, per_row = 4 + level, 5 + level // 2
    count = rows * per_row
    props = {
        "controller": UUID,
        "status": "LEFT_LEVEL",
        "observed_ticks": rows * 5,
        "join_game_tick": 0,
        "first_age": 1,
        "last_age": rows * 5,
        "age_monotonic": "true",
        "candidate_joins": count,
        "confirmed_present_at_post": count,
        "ambiguous_joins": 0,
        "candidate_budget_exceeded": "false",
        "leave_seen": "true",
        "removal": "DISCARDED",
        "join_counts_per_tick": "{" + ", ".join(
            f"{tick*5}={per_row}" for tick in range(1, rows + 1)) + "}",
        "unmatched_global": 0,
        "ambiguous_global": 0,
    }
    props.update(overrides)
    return TAG + " type=end " + " ".join(f"{k}={v}" for k, v in props.items())


class ArrowVolleyObservationParserTests(unittest.TestCase):
    def test_each_level_synthetic_trace(self):
        for level in range(1, 7):
            with self.subTest(level=level):
                result = evaluate(simulated_log(level), level)
                self.assertEqual("TRACE_CONSISTENT_NOT_GAMETEST", result["result"])
                self.assertEqual([], result["fail_reasons"])

    def test_rejects_ambiguous_attribution(self):
        result = evaluate(simulated_log(1, ambiguous_joins=1), 1)
        self.assertIn("AMBIGUOUS_OWNER_PROXIMITY", result["fail_reasons"])

    def test_rejects_rejected_or_short_lived_spawns(self):
        result = evaluate(simulated_log(1, confirmed_present_at_post=22), 1)
        self.assertIn("COUNT_NOT_CONFIRMED", result["fail_reasons"])

    def test_rejects_missing_controller_leave(self):
        result = evaluate(simulated_log(1, status="WINDOW_EXPIRED",
                                        leave_seen="false"), 1)
        self.assertIn("NO_CONFIRMED_LEAVE_EVENT", result["fail_reasons"])

    def test_rejects_wrong_join_pattern(self):
        result = evaluate(simulated_log(1,
            join_counts_per_tick="{5=10, 10=5, 15=5, 20=5, 25=0}"), 1)
        self.assertIn("ROW_PATTERN_MISMATCH", result["fail_reasons"])

    def test_rejects_shifted_start_ticks(self):
        # Row gaps remain valid but the first emission is one tick too late.
        result = evaluate(simulated_log(1,
            join_counts_per_tick="{6=5, 11=5, 16=5, 21=5, 26=5}"), 1)
        self.assertIn("ROW_START_OFFSET_MISMATCH", result["fail_reasons"])

    def test_rejects_controller_first_seen_late(self):
        result = evaluate(simulated_log(1, first_age=9), 1)
        self.assertIn("CONTROLLER_OBSERVATION_INCOMPLETE", result["fail_reasons"])

    def test_rejects_missing_initial_age_samples(self):
        result = evaluate(simulated_log(1, observed_ticks=3), 1)
        self.assertIn("CONTROLLER_OBSERVATION_INCOMPLETE", result["fail_reasons"])

    def test_rejects_late_controller_discard(self):
        result = evaluate(simulated_log(1, last_age=70), 1)
        self.assertIn("CONTROLLER_DISCARD_AGE_MISMATCH", result["fail_reasons"])

    def test_rejects_missing_join_game_tick(self):
        line = simulated_log(1)
        line = line.replace("join_game_tick=0 ", "")
        with self.assertRaises(ValueError):
            evaluate(line, 1)

    def test_rejects_budget_overflow(self):
        result = evaluate(simulated_log(6,
            candidate_budget_exceeded="true"), 6)
        self.assertIn("CANDIDATE_BUDGET_EXCEEDED", result["fail_reasons"])

    def test_rejects_empty_real_log(self):
        with self.assertRaises(ValueError):
            evaluate("The server started\n", 1)

    def test_rejects_unselected_multiple_sessions(self):
        with self.assertRaises(ValueError):
            evaluate(simulated_log() + "\n" + simulated_log(), 1)

    def test_controller_filter(self):
        log = simulated_log(1) + "\n" + simulated_log(1,
            controller="00000000-0000-4000-8000-000000000002")
        self.assertEqual("TRACE_CONSISTENT_NOT_GAMETEST",
                         evaluate(log, 1, controller=UUID)["result"])

    def test_illegal_level_fails_closed(self):
        with self.assertRaises(ValueError):
            evaluate(simulated_log(), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
