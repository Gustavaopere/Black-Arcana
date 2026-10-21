#!/usr/bin/env python3
"""Pure deterministic model of the source-pinned Arrow Volley state transitions.

This is NOT a GameTest, a NeoForge simulator, or execution of publisher code.
It models only the already observed conditions in ArrowVolleyEntity.tick and
the official Mojang 1.21.1 ServerLevel.tickNonPassenger age increment.
"""
import unittest


def model_volley(level: int, max_ticks: int = 100):
    if not 1 <= level <= 6:
        raise ValueError("Only provider-defined levels 1..6")
    rows = 4 + level
    per_row = 5 + level // 2
    tick_count = 0
    emitted = []
    discarded = None
    for world_tick in range(1, max_ticks + 1):
        # Official vanilla ServerLevel.tickNonPassenger increments BEFORE entity.tick.
        tick_count += 1
        if tick_count % 5 == 0:
            emitted.append((world_tick, per_row))
        elif tick_count > rows * 5:
            discarded = world_tick
            break
    return {
        "rows": rows,
        "arrows_per_row": per_row,
        "emitted_rows": len(emitted),
        "emitted_arrows": sum(n for _, n in emitted),
        "last_row_tick": emitted[-1][0] if emitted else None,
        "discard_tick": discarded,
    }


class ArrowVolleyTickModelTest(unittest.TestCase):
    def test_all_six_spell_levels(self):
        expected = (25, 36, 42, 56, 63, 80)
        for level, total in enumerate(expected, 1):
            with self.subTest(level=level):
                x = model_volley(level)
                self.assertEqual(x["emitted_rows"], x["rows"])
                self.assertEqual(x["emitted_arrows"], total)
                self.assertEqual(x["last_row_tick"], x["rows"] * 5)
                self.assertEqual(x["discard_tick"], x["rows"] * 5 + 1)

    def test_insufficient_simulation_is_not_success(self):
        self.assertIsNone(model_volley(6, 25)["discard_tick"])

    def test_illegal_levels_are_not_silently_extrapolated(self):
        for level in (0, 7, -1):
            with self.assertRaises(ValueError):
                model_volley(level)


if __name__ == "__main__":
    unittest.main(verbosity=2)
