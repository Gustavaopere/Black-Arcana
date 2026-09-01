# Stage 05 — Casting & UX Manual QA Matrix

Stage 05 baseline automated implementation checkpoint: `630db8d57a0703a1231075d68353447b8ce37add`.

Baseline automated verification:
- branch run `33182063857`: unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke all GREEN;
- post-merge main run `33182458511`: the same full pipeline GREEN.

Stage 05A.11 automated presentation checkpoint: `7c617983a266e084cacb98682e669cce561e333f`.
- workflow `33471722454`: unit tests, diff sanity, NeoForge build, JAR inspection, Foundation GameTest server and dedicated-server smoke all GREEN;
- the preceding presentation RED was captured by workflow `33471498889` before the gate/tooltip helpers existed.

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
| GUI focus | Inventory/chat/other Screen open | Cast inputs do not fire through another GUI | ⬜ PENDING |
| Loadout | Edit/apply/clear/reopen | Server response remains canonical and draft never bypasses slot/availability checks | ⬜ PENDING |
| Loadout tooltip | Hover spells with normal and non-normal hazard metadata | Tooltip shows only synchronized static danger tier/minimum/recommended metadata; it does not issue a cast, request a forecast or imply current resistance | ⬜ PENDING |
| Loadout tooltip | Small window / GUI scale 4 / edge rows | Tooltip remains readable/on-screen and does not obscure loadout interaction beyond normal vanilla tooltip behavior | ⬜ PENDING |
| Session | Disconnect/reconnect same player | Old result/loadout/HUD state does not flash before server snapshots arrive | ⬜ PENDING |
| Feedback | Authoritative denial | HUD displays actual server denial briefly, then disappears | ⬜ PENDING |
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
| F1 / hidden GUI | Toggle vanilla HUD visibility | Black Arcana layer follows expected vanilla HUD behavior | ⬜ PENDING |

## Closure rule

Stage 05 remains active until the applicable manual rows above are exercised. Rows for presentation features that do not yet exist (for example future screen motion or particles) may be carried explicitly into Stage 09 rather than falsely marked passed. Stage 05A.11 automated evidence does not substitute for these real-client checks.
