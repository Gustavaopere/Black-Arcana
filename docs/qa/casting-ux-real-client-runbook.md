# Stage 05 / 05A.11 — Real-client QA execution runbook

This runbook operationalizes `docs/qa/casting-ux-manual-matrix.md`. It does not replace the matrix and does not authorize marking any row passed without an actual Minecraft client observation.

## Canonical build under test

Test the current `main` containing PR #37 or a build proven equivalent to that exact `main` revision. Record the tested commit SHA at the top of the evidence report before changing any matrix state.

The Stage 05/05A gate is manual by design. Automated CI, GameTests, screenshots from tests, code inspection and server smoke tests are supporting evidence only; they do not substitute for the client checks below.

## Result vocabulary

For every matrix row, record exactly one result:

- `PASS` — the expected behavior was directly observed in a real client;
- `FAIL` — the observed behavior contradicted the expected result; include reproduction steps and evidence;
- `BLOCKED` — the scenario could not be exercised; state the concrete blocker and do not convert it to PASS;
- `NOT APPLICABLE / CARRIED TO STAGE 09` — only for a genuinely future-only feature already allowed by the matrix closure rule.

Do not infer one configuration from another. A pass at GUI scale 2 does not prove GUI scale 4; a pass at 1920×1080 does not prove 854×480 or ultrawide.

## Evidence minimum

For visual-layout rows, capture a screenshot showing the full game viewport and the relevant Black Arcana UI. For interaction rows, use either a short recording or a concise timestamped observation log that proves the input sequence and result. For stale/reconnect rows, capture before/after state or a recording spanning the transition.

Every FAIL must include: tested SHA, client configuration relevant to the row, exact reproduction sequence, observed result, expected result, and at least one screenshot/recording when the failure is visual or input-related.

## Block A — Resolution, GUI scale and viewport containment

1. Start with the contextual HUD enabled and a spell selected so the selection panel can appear.
2. Open the radial and loadout editor separately at 854×480, 1920×1080 and 3440×1440.
3. At each supported viewport, exercise GUI scale Auto / 2 / 3 / 4 where the client permits it.
4. Hover a loadout spell with hazard metadata and show the tooltip.
5. Trigger a non-normal selected-spell hazard presentation so resistance/gate lines are visible.
6. Confirm no clipping, off-screen panel, unusable hit region or unreadable tooltip text.
7. Capture evidence for each resolution and each GUI scale actually exercised.

## Block B — Radial, cast separation and key bindings

1. Exercise radial behavior `TOGGLE`: open, select a spell, close, reopen.
2. Confirm selection alone never executes the spell.
3. Exercise radial behavior `HOLD`: hold the radial key, interact as intended, release it and verify the selector closes without stuck input.
4. Rebind radial, cast and quick-slot keys through the normal controls UI.
5. Confirm the bindings remain usable and conflicts remain discoverable through the vanilla controls surface.
6. Open inventory, chat and another `Screen`, then press Black Arcana cast inputs and verify they do not fire through the focused GUI.

## Block C — Loadout authority and tooltip

1. Open the loadout editor, change the draft, apply it, close and reopen.
2. Clear the draft, apply, and reopen again.
3. Confirm the server response remains canonical and no draft action bypasses slot/availability rules.
4. Hover a spell whose static hazard tier is normal and one whose tier is non-normal.
5. Confirm the tooltip contains only synchronized static danger tier plus minimum/recommended Arcane Resistance metadata when applicable.
6. Confirm hovering does not cast, does not request a dynamic forecast and does not claim current Arcane Resistance.
7. Repeat the tooltip check near edge rows, at 854×480 and GUI scale 4.

## Block D — HUD lifecycle and authoritative denial

1. Trigger a server-authoritative cast denial and verify the HUD displays the actual denial briefly.
2. Stop interacting and verify the Black Arcana contextual HUD disappears; no permanent resource bar or stale result remains.
3. Exercise all five HUD anchors at 0.5×, 1× and 2× HUD scale.
4. With hazard/gate lines visible, verify every anchor keeps the panel inside the viewport and readable.
5. Toggle vanilla F1/hidden GUI behavior and record whether the Black Arcana layer follows the expected vanilla HUD visibility behavior.

## Block E — Arcane Resistance forecast

For one selected non-normal spell, exercise all available threshold regions:

1. effective Arcane Resistance below minimum;
2. effective Arcane Resistance between minimum and recommended;
3. effective Arcane Resistance at or above recommended.

Confirm the HUD shows the server-authored current/minimum/recommended values and the factual state `blocked below minimum`, `below recommended` or `recommendation met`. No wording may claim that recommendation eliminates all Backlash risk.

Then make the resistance preview unavailable/incompatible when a reproducible configuration exists. The HUD must show `Unavailable` or the synchronized static fallback; it must never present a known-partial resistance value as complete.

Change armor, Curios and RPG-derived resistance sources that are present in the test instance while the spell remains selected. Confirm refresh converges without per-tick spam symptoms or visible rollback to an older result.

## Block F — Predictable read-only cast gates

Exercise each gate category only when the current test instance provides a legitimate way to create the condition:

- identity/loadout denial;
- progression denial;
- cooldown denial;
- resource-cost denial;
- all predictable gates clear;
- projection/runtime unavailable.

For a denial, confirm the separate preflight line reports only the bounded server-authored category. It must not display an invented client reason or arbitrary forecast detail.

For `CLEAR`, confirm the wording says only that no predictable gate blocks. It must not promise cast success because replay admission, target resolution, world policy and hazard preparation remain cast-time authority.

If a category cannot be produced without adding a debug bypass or changing production semantics, mark that row `BLOCKED` and record the missing fixture rather than fabricating the state.

## Block G — Reconnect, stale state and datapack reload

1. Produce visible selected-spell forecast state.
2. Disconnect and reconnect as the same player.
3. Confirm old result/loadout/HUD state does not flash before fresh server snapshots arrive.
4. Exercise a danger-profile datapack reload when available while a forecast is in use.
5. Confirm cached forecast is cleared/replaced and stale tier/threshold data cannot override the new static preflight.
6. Record the transition in one continuous capture whenever possible.

## Block H — Accessibility and client configuration

1. Exercise feedback levels `MINIMAL`, `STANDARD` and `VERBOSE`.
2. Confirm `MINIMAL` does not leave unused forecast/gate presentation traffic visible and the density of feedback follows the configured level.
3. Toggle reduced motion and reduced flashes and verify the options persist locally. Future-only effects remain subject to the matrix Stage 09 carry rule.
4. Exercise particle density 0 / 0.5 / 1 and verify the preference persists locally; do not claim effect-level compliance where no Black Arcana particle effect exists yet.
5. Reset/remove relevant client config entries through the normal supported configuration path and confirm NeoForge defaults recover safely.

## Evidence report template

Create one evidence section per matrix row with:

- Matrix row / scenario:
- Tested commit SHA:
- Minecraft / NeoForge instance identification:
- Relevant client settings:
- Steps performed:
- Observed result:
- Evidence reference:
- Result: `PASS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE / CARRIED TO STAGE 09`.

After the full run, update `docs/qa/casting-ux-manual-matrix.md` only from this recorded evidence. Do not batch-convert untouched rows to PASS.

## Closure sequence

1. Record all real-client evidence.
2. Fix every real implementation failure and rerun affected rows.
3. Update the matrix with only observed results.
4. Reconcile Stage 05 and Stage 05A numbered task status after the matrix gate is actually satisfied.
5. Run the full automated CI again on the closeout PR.
6. Only after the client gate and CI are both green may Stage 05/05A be declared complete and Stage 06 promotion be reconsidered.
