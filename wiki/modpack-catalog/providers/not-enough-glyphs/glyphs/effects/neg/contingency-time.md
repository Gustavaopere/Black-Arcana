# Contingency: Expire

- Registry: `not_enough_glyphs:contingency_time`
- Class: `ExpireContingency`; Sauce-backed
- Status: enabled
- Trigger: Sauce contingency expiration; source explicitly says forceful dispel does not trigger it.
- Config construction uses inherited duration helpers with arguments 60 / 30 / 200; unit semantics are left to the Sauce/Ars base rather than reinterpreted.
- Acquisition: Abjuration Essence + Repeater + Clock.
- Boundary: provider timer/contingency authority; no BA duplicate scheduler.