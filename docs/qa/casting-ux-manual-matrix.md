# Stage 05 — Casting & UX Manual QA Matrix

Stage 05 baseline automated implementation checkpoint: `630db8d57a0703a1231075d68353447b8ce37add`.

Baseline automated verification:
- branch run `33182063857`: unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke all GREEN;
- post-merge main run `33182458511`: the same full pipeline GREEN.

Stage 05A.11 automated presentation checkpoint: `7c617983a266e084cacb98682e669cce561e333f`.
- workflow `33471722454`: unit tests, diff sanity, NeoForge build, JAR inspection, Foundation GameTest server and dedicated-server smoke all GREEN;
- the preceding presentation RED was captured by workflow `33471498889` before the gate/tooltip helpers existed.

Stage 05 real-client fixture checkpoint: PR #39 merged to `main` at `06f0a9a495b6fe6576da75f673800a94af14dab0`.
- post-merge workflow `33501635945`: unit tests, diff sanity, NeoForge build, JAR inspection, Foundation GameTest server and dedicated-server smoke all GREEN;
- `docs/qa/fixtures/stage05-real-client/` provides removable deterministic controls for hazard thresholds, Arcane Resistance 0/15/30, legitimate CLEAR/COOLDOWN/COST gates and stale-profile reload checks;
- fixture availability does **not** change any manual result by itself. Every row below remains PENDING until direct client evidence is recorded.

Stage 05 small-viewport preflight hardening checkpoint: PR #57 merged to `main` at `f2bb9a19db92d869e4443b2047ad1c913f8d2a29`.
- final PR head `01a77eab641896173585b66c6310662d820c9f0c` passed workflow `34010736078` (#1169);
- exact-SHA post-merge workflow `34010968124` (#1170) passed JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical artifact publication;
- canonical artifact `black-arcana-f2bb9a19db92d869e4443b2047ad1c913f8d2a29`, artifact ID `9982472491`, SHA-256 `1ba6949ceb04f261646548b6d99a158f4f40211a5017ca1911c0e1a732f86cdb`;
- responsive loadout/radial geometry and wrapped authoritative HUD text are automated preflight evidence only. They do **not** mark the 854×480, GUI-scale, denial, hazard/gate or anchor rows PASS without direct client observation.

Canonical real-client build delivery: successful `main` CI publishes a 7-day GitHub Actions artifact named `black-arcana-<full commit SHA>` only after the full automated runtime gate succeeds. Use the artifact matching the exact SHA recorded in the evidence report. Artifact availability is delivery infrastructure only and does **not** change any manual PENDING row.

Execution procedure and evidence requirements are in `docs/qa/casting-ux-real-client-runbook.md`.

This document deliberately does **not** mark visual/manual rows as passed. They must be exercised in a real Minecraft client before Stage 05 task files receive ✅.

## Manual matrix

| Area | Scenario | Expected | State |
|---|---|---|---|
| Resolution | 854×480 / small window | Radial, loadout editor and contextual HUD remain readable and on-screen | ⬜ PENDING |
| Resolution | 1920×1080 | Default layout remains compact and unobtrusive | ⬜ PENDING |
| Resolution | 3440×1440 ultrawide | HUD anchor and radial remain centered/anchored correctly | ⬜ PENDING |
| GUI scale | Auto / 2 / 3 / 4 | No clipping, overlap or unusable hit regions; hazard/gate HUD lines and loadout tooltip remain readable | ⬜ PENDING |
| Radial | `TOGGLE` | Opens/closes predictably; selection never casts by itself | ⬜ PENDING |
| Radial | `HOLD` | Releasing radial key closes selector without stuck input | ⬜ PENDING |
| Input | Rebind radial/cast/quick slots | Conflicts are discoverable through vanilla controls and bindings remain usable | ⬜ PENDING |
| Input persistence | Rebind radial/cast/quick slots, restart the client, then reuse them | Rebound mappings persist across the normal client restart and remain usable; no required Black Arcana action silently falls back to a provider-only input path | ⬜ PENDING |
| GUI focus | Inventory/chat/other Screen open | Cast inputs do not fire through another GUI | ⬜ PENDING |
| Loadout | Edit/apply/clear/reopen | Server response remains canonical and draft never bypasses slot/availability checks | ⬜ PENDING |
| Loadout bound | Legitimate synchronized 16-slot loadout | Every canonical slot `0..15` remains reachable through supported selection/radial paging; paging/selection never exceeds the synchronized server-owned loadout and never forges another spell identity | ⬜ PENDING |
| Loadout tooltip | Hover spells with normal and non-normal hazard metadata | Tooltip shows only synchronized static danger tier/minimum/recommended metadata; it does not issue a cast, request a forecast or imply current resistance | ⬜ PENDING |
| Loadout tooltip | Small window / GUI scale 4 / edge rows | Tooltip remains readable/on-screen and does not obscure loadout interaction beyond normal vanilla tooltip behavior | ⬜ PENDING |
| Session | Disconnect/reconnect same player | Old result/loadout/HUD state does not flash before server snapshots arrive | ⬜ PENDING |
| Feedback | Authoritative denial | HUD displays actual server denial briefly, then disappears | ⬜ PENDING |
| Result correlation | Authoritative result arrives while another spell is currently selected | Presentation attributes the result only through the matching emitted `castId` context; it never guesses that the currently selected spell produced an unrelated/unmatched result | ⬜ PENDING |
| Feedback | Idle player | No permanent Black Arcana resource bar or stale result remains visible | ⬜ PENDING |
| HUD | All five anchors at 0.5×, 1×, 2× | Panel stays inside viewport and text remains readable with the extra preflight line | ⬜ PENDING |
| Hazard HUD | Effective Arcane Resistance below minimum / between minimum and recommended / at-or-above recommended | Selected dangerous spell shows server-authored current/minimum/recommended values and factual threshold status: blocked below minimum / below recommended / recommendation met; no wording implies that recommendation eliminates all Backlash risk | ⬜ PENDING |
| Hazard HUD | Predictable identity/loadout, progression, cooldown and resource-cost denials | Separate preflight line shows only the bounded server-authored gate category; it never invents or exposes arbitrary client-derived denial detail | ⬜ PENDING |
| Hazard HUD | Predictable gates all clear | Text says that no predictable gate blocks; it does not claim the cast is guaranteed because replay, target, world policy and hazard preparation remain cast-time authority | ⬜ PENDING |
| Hazard HUD | Gate projection/runtime unavailable | Preflight gate line is unavailable or absent according to the synchronized response; the client never substitutes a locally guessed gate result | ⬜ PENDING |
| Hazard HUD | Preview provider unavailable/incompatible | HUD shows `Unavailable` or static danger fallback; it never presents a partial resistance value as complete | ⬜ PENDING |
| Hazard HUD | Change armor/Curios/RPG resistance while selected | Refresh converges to the current server-authored projection without per-tick packet spam or stale lower request-id rollback | ⬜ PENDING |
| Hazard HUD | Datapack danger-profile reload or reconnect | Cached forecast is cleared/replaced; an in-flight forecast whose tier/thresholds no longer match current static preflight cannot override the new resistance or gate presentation | ⬜ PENDING |
| Accessibility | `MINIMAL`, `STANDARD`, `VERBOSE` | Feedback density follows client preference only; `MINIMAL` does not generate unused forecast/gate traffic | ⬜ PENDING |
| Accessibility | reduced motion / reduced flashes | Flags persist locally; future effects must honor them when such effects exist | ⬜ PENDING |
| Accessibility | particle density 0 / 0.5 / 1 | Preference persists locally; future Black Arcana particles must consume the multiplier | ⬜ PENDING |
| Client config | Missing/reset config entries | NeoForge defaults recover safely | ⬜ PENDING |
| Client authority isolation | Change Black Arcana presentation/config preferences and interact with HUD/radial/forecast surfaces under equivalent server-owned cast conditions | Preferences and presentation may reshape local UX only; they do not alter cost, cooldown, progression, target admission, Arcane Danger/world settlement or mutate underlying hazard/gate/resource state | ⬜ PENDING |
| F1 / hidden GUI | Toggle vanilla HUD visibility | Black Arcana layer follows expected vanilla HUD behavior | ⬜ PENDING |
| Provider coexistence | Iron's-hosted `black_arcana:irons_integration_probe` | One provider invocation produces at most one Black Arcana root cast/result; Black Arcana transactional cost and cooldown settle exactly once; Iron's native mana/cooldown are not additionally charged for the hosted transaction | ⬜ PENDING |
| Provider coexistence | Epic Fight / EFIS present during Black Arcana casting | Client combat/animation state never becomes Black Arcana cast-legality authority; casting remains server-authoritative | ⬜ PENDING |
| Optional providers | Required optional provider absent/incompatible where reproducible | Only the dependent feature fails closed; no crash, duplicate/free fallback, or unverified hard dependency is introduced; core Black Arcana keyboard/mouse casting remains usable when the chosen operation does not require that provider | ⬜ PENDING |

## Closure rule

Stage 05 remains active until the applicable manual rows above are exercised. Rows for presentation features that do not yet exist (for example future screen motion or particles) may be carried explicitly into Stage 09 rather than falsely marked passed. Stage 05A.11 automated evidence does not substitute for these real-client checks.
