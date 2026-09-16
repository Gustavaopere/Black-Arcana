# Stage 05 / 05A.11 — Real-client QA execution runbook

This runbook operationalizes `docs/qa/casting-ux-manual-matrix.md`. It does not replace the matrix and does not authorize marking any row passed without an actual Minecraft client observation.

## Canonical build under test

Use the Black Arcana JAR published by the latest successful `main` Black Arcana CI run for the exact commit being tested. After unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server and dedicated-server smoke all pass, the `main` workflow publishes a short-lived GitHub Actions artifact named `black-arcana-<full commit SHA>` containing `build/libs/black_arcana-*.jar`.

Canonical QA artifacts are published from `main` only and retained for 7 days. Feature-branch and pull-request runs still exercise the full automated gate but do not publish a canonical real-client artifact. Download the artifact for the exact `main` SHA, extract its archive, place the contained Black Arcana JAR in the target Minecraft 1.21.1 / NeoForge test instance `mods/` directory, and record that exact SHA at the top of the evidence report before changing any matrix state.

If the artifact for the required SHA has expired or is unavailable, rerun CI for the current exact `main` revision when appropriate or build that exact recorded SHA locally. Do not silently substitute a different revision. Artifact availability proves only build delivery after the automated gate; it is not real-client evidence and does not make any manual matrix row PASS.

The Stage 05/05A gate is manual by design. Automated CI, GameTests, screenshots from tests, code inspection and server smoke tests are supporting evidence only; they do not substitute for the client checks below.

Use the removable deterministic datapack fixture in `docs/qa/fixtures/stage05-real-client/` when exercising hazard thresholds, the normal/non-normal tooltip controls, Arcane Resistance 0/15/30 states, legitimate Iron cooldown/cost gate states and danger-profile reload/stale-forecast behavior. The fixture does not create PASS evidence by itself and must not be shipped as production gameplay data.

## Result vocabulary

For every matrix row, record exactly one result:

- `PASS` — the expected behavior was directly observed in a real client;
- `FAIL` — the observed behavior contradicted the expected result; include reproduction steps and evidence;
- `BLOCKED` — the scenario could not be exercised; state the concrete blocker and do not convert it to PASS;
- `NOT APPLICABLE / CARRIED TO STAGE 09` — only for a genuinely future-only feature already allowed by the matrix closure rule.

Do not infer one configuration from another. A pass at GUI scale 2 does not prove GUI scale 4; a pass at 1920×1080 does not prove 854×480 or ultrawide.

## Evidence minimum

For visual-layout rows, capture a screenshot showing the full game viewport and the relevant Black Arcana UI. For interaction rows, use either a short recording or a concise timestamped observation log that proves the input sequence and result. For stale/reconnect rows, capture before/after state or a recording spanning the transition. For authority-isolation rows, record the relevant server-owned state/outcome before and after each client-only change so a presentation difference cannot be mistaken for a gameplay-state change. For cast-result correlation, the evidence must positively link a known emitted cast to its authoritative result rather than proving only that an unrelated selection was not used.

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
5. Confirm the rebound mappings are usable and conflicts remain discoverable through the vanilla controls surface.
6. Fully restart the Minecraft client through the normal launcher/instance flow, return to the same test instance, and confirm those rebound mappings persist and remain usable. Record the before/restart/after sequence; a same-session rebind is not sufficient for the persistence row.
7. Open inventory, chat and another `Screen`, then press Black Arcana cast inputs and verify they do not fire through the focused GUI.

## Block C — Loadout authority and tooltip

1. Open the loadout editor, change the draft, apply it, close and reopen.
2. Clear the draft, apply, and reopen again.
3. Confirm the server response remains canonical and no draft action bypasses slot/availability rules.
4. Hover a spell whose static hazard tier is normal and one whose tier is non-normal.
5. Confirm the tooltip contains only synchronized static danger tier plus minimum/recommended Arcane Resistance metadata when applicable.
6. Confirm hovering does not cast, does not request a dynamic forecast and does not claim current Arcane Resistance.
7. Repeat the tooltip check near edge rows, at 854×480 and GUI scale 4.

## Block D — HUD lifecycle, authoritative denial and cast-result correlation

1. Trigger a server-authoritative cast denial and verify the HUD displays the actual denial briefly.
2. For the correlation row, emit a known cast A and positively identify both the emitted cast identity and the authoritative result for that same cast using an already-supported observation surface. If the current production client/logging exposes canonical `castId` values, record A's emitted `castId` and the returned result's `castId` and require equality. If IDs are not directly observable, use an existing spell-specific correlated presentation/effect that unambiguously proves the result belongs to A. Do not add a production debug bypass solely for QA.
3. Before A's result is presented, change the selected spell to distinguishable spell B where the timing is safely reproducible. Confirm A's result remains attributed to A's matching context and is not relabeled as B.
4. Separately exercise an unmatched/generic result path if the production runtime exposes one safely; confirm it remains generic rather than inventing a spell identity.
5. If neither a canonical ID observation nor another unambiguous positive correlation surface exists in the exact campaign, record the correlation row `BLOCKED`; a generic-only presentation is not sufficient for PASS.
6. Stop interacting and verify the Black Arcana contextual HUD disappears; no permanent resource bar or stale result remains.
7. Exercise all five HUD anchors at 0.5×, 1× and 2× HUD scale.
8. With hazard/gate lines visible, verify every anchor keeps the panel inside the viewport and readable.
9. Toggle vanilla F1/hidden GUI behavior and record whether the Black Arcana layer follows the expected vanilla HUD visibility behavior.

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

If a category cannot be produced without adding a debug bypass or changing production semantics, mark that row `BLOCKED` and record the missing fixture rather than fabricating the state. The Stage 05 fixture deliberately supports legitimate `CLEAR`, `COOLDOWN` and `COST` states; its documented `PROGRESSION`, identity/loadout and unavailable limitations must remain `BLOCKED` when the production runtime cannot produce them naturally.

## Block G — Reconnect, stale state and datapack reload

1. Produce visible selected-spell forecast state.
2. Disconnect and reconnect as the same player.
3. Confirm old result/loadout/HUD state does not flash before fresh server snapshots arrive.
4. Exercise the fixture's alternate Iron danger profile while a forecast is in use.
5. Run `/reload` and confirm cached forecast is cleared/replaced and stale tier/threshold data cannot override the new static preflight.
6. Record the transition in one continuous capture whenever possible.

## Block H — Accessibility, client configuration and authority isolation

1. Exercise feedback levels `MINIMAL`, `STANDARD` and `VERBOSE`.
2. Confirm `MINIMAL` does not leave unused forecast/gate presentation traffic visible and the density of feedback follows the configured level.
3. Toggle reduced motion and reduced flashes and verify the options persist locally. Future-only effects remain subject to the matrix Stage 09 carry rule.
4. Exercise particle density 0 / 0.5 / 1 and verify the preference persists locally; do not claim effect-level compliance where no Black Arcana particle effect exists yet.
5. Reset/remove relevant client config entries through the normal supported configuration path and confirm NeoForge defaults recover safely.
6. Enumerate the gameplay-authority dimensions applicable to the exact candidate and current Stage 05 test content: resource cost, cooldown, progression gate, target admission, Arcane Danger settlement and world settlement. For each applicable dimension, create an equivalent before/after case with the same server-owned inputs except for Black Arcana client-only presentation/config preferences. Record the authoritative state/outcome before and after and require equality of gameplay semantics.
7. A dimension with no legitimate operation in the exact campaign is documented as not applicable to that candidate's available Stage 05 test content with the concrete reason; this does not prove that dimension generally. A dimension that should be applicable but cannot be produced or observed is unresolved and makes the authority-isolation row `BLOCKED`, not PASS.
8. The authority-isolation matrix row is `PASS` only after every applicable dimension has direct before/after evidence. Do not use one cost/cooldown case to stand in for progression, targeting, Arcane Danger or world settlement when those dimensions are applicable.
9. Interact with radial/HUD/forecast/gate presentation without performing a new authoritative gameplay action and verify that those surfaces do not mutate the underlying synchronized hazard, gate or resource state.

Do not claim that a preference is gameplay-safe merely because the UI looks unchanged. Physical observations supplement the deterministic `ClientConfigAuthorityContractTest`; they do not permit unexercised applicable authority dimensions to be silently inferred as PASS.

## Block I — Canonical 16-slot loadout reachability

1. Establish a legitimate server-accepted Black Arcana loadout containing all 16 canonical slots. Do not manufacture client-only entries or bypass server availability checks merely to populate the row.
2. Reopen/reconnect as needed and confirm the synchronized client still reflects the server-owned 16-slot loadout before testing selection.
3. Using the supported radial paging/selection path, deliberately reach and select every slot `0..15` at least once. Direct quick-cast mappings cover only their supported subset and are not a substitute for proving slots `8..15` reachable.
4. For each page transition, confirm focus/selection remains within the synchronized loadout and cannot advance to a forged seventeenth slot or substitute another spell identity.
5. Confirm selection of each slot changes presentation/selected intent only. Do not count a selection as successful if it implicitly casts.
6. Record one continuous interaction capture when practical, or a timestamped slot-by-slot observation log proving all 16 slots were reached on the exact campaign candidate.

If a legitimate 16-entry server-owned loadout cannot be created with the current production content/fixture, attempt the row and record `BLOCKED` with the concrete availability limitation. Do not add a production bypass solely to make the QA row executable.

## Block J — Current-modpack provider coexistence authority

Before this block, re-read the actual physical modlist for the tested instance and record the exact installed versions. The planning baseline includes Iron's Spells 'n Spellbooks `1.21.1-3.16.3`, Spell Actionbar `1.1.4`, Epic Fight `21.17.3.1`, EFIS Compat `3.1.0` and Controlling `19.0.5`; treat those as the tested versions only when the physical instance still matches them.

### Iron's-hosted Black Arcana probe

1. Invoke the supported Iron's-hosted `black_arcana:irons_integration_probe` once through its normal provider host surface.
2. Capture enough evidence to identify the single physical/provider invocation and the resulting Black Arcana result/context.
3. Confirm the invocation produces at most one Black Arcana root cast/result; no duplicate Black Arcana effect/result/cooldown settlement may appear from one host action.
4. Record the relevant Iron's mana state before and after the invocation. Confirm the observed debit corresponds to the one Black Arcana transactional probe cost and that no additional provider-native mana deduction is applied in parallel.
5. Confirm the Black Arcana cooldown settles once and that no second provider-native cooldown is stacked onto the hosted transaction.
6. Repeat only as needed to distinguish one-settlement behavior from ordinary later invocations; do not infer one-root semantics from animation count alone.

### Epic Fight / EFIS authority isolation

1. With Epic Fight/EFIS present, establish a reproducible Black Arcana cast whose ordinary server-owned gates are satisfied.
2. Repeat the same Black Arcana operation while changing only the relevant client combat/animation mode/state where the installed version permits it.
3. Confirm Epic Fight/EFIS client state does not become Black Arcana cast-legality authority. A cosmetic or animation difference may be recorded separately, but it must not silently allow or deny a cast that the Black Arcana server runtime otherwise treats identically.

### Optional-provider failure boundary

Where a safe reproducible profile exists, start the dependent feature with its optional provider absent or demonstrably incompatible and confirm only that dependent feature fails closed: no client/server crash, no duplicate/free fallback, and no unrelated Black Arcana casting failure.

In that provider-absent/incompatible profile, exercise every required core keyboard/mouse path that the chosen Black Arcana operation can legitimately use: open radial, radial selection/close, cast selected and open/edit loadout. Also exercise each quick-cast mapping intentionally bound for the campaign; quick-cast mappings that remain deliberately unbound are not promoted to required controls. Confirm none of these core paths silently requires a provider/controller integration.

If a required core path cannot be exercised because of the missing provider even though the Black Arcana operation itself does not require that provider, the row is `FAIL`. If provider absence/incompatibility cannot be exercised safely at all without changing production semantics, record the matrix row `BLOCKED` with the concrete reason. Do not infer a physical PASS from dedicated-server CI or static optional-classloading tests.

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
