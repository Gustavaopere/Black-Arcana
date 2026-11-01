# Alex's Caves Continued 1.0.10 — nuclear ticket safety acceptance (PENDING)

**Purpose:** translate the SHA-exact static finding into reproducible, non-destructive
acceptance gates for the two observed DamageSources,
`alexscaves:intentional_game_design` and `alexscaves:nuke`.
This is a **test plan, not an executed QA report**. No runtime success, physical
reproduction, ticket leak or mitigation is asserted.

## Authority and source seal

| Input | Exact evidence / required pin |
| --- | --- |
| Minecraft / loader / Java | 1.21.1 / NeoForge 21.1.248 / Java 21 |
| Publisher artifact | `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| NeoForge universal | `neoforge-21.1.248-universal.jar`, SHA-256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5` |
| Binary proof | [TicketController vs publisher manifest](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NEOFORGE-TICKETS-21.1.248.json) |
| Static probe | [Existing Java 21 + JAR-exact workflow](../../.github/workflows/alexscaves-1010-neoforge-tickets.yml) |
| Promotion regression | [Fail-closed tests](alexscaves_1010_nuclear_ticket_promotion_gate_test.py) |
| Variant cards | [Intentional Game Design](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types/intentional-game-design.md) and [Nuke](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types/nuke.md) |

The exact compiled path presently forwards `add=true,ticking=true` during the
force request and `add=false,ticking=false` during attempted removal. The
selected NeoForge branches use separate `ENTITY_TICKING` and `ENTITY`
ticket categories. This is a **confirmed static branch mismatch**, not
a physically observed persistent leak. The platform adapter discards the
boolean returned by `TicketController.forceChunk`.

## Safe environment prerequisites

Perform exclusively on a **disposable dedicated-server test world**, with
backups and permission to observe server internals. Before spawning any nuclear
object, record the actual modlist, JAR hashes, config, dimension, view distance,
gamerules, controller registration and available chunk-ticket diagnostics.
Do not reproduce on a production world or bypass claims, protections or
`WorldEffectPolicy`. Instrumentation must be read-only; it must not alter the
provider's code or forge tickets. If the server's ticket state cannot be
measured, mark the corresponding row **NOT_TESTED**, not PASS.

## Physical and integration acceptance matrix

| ID | Controlled observation | Required evidence for PASS |
| --- | --- | --- |
| NT-01 | Resolve the publisher's ticket controller registration and `LoadingValidationCallback` in the exact runtime | Registered controller ID, callback identity/absence and runtime log; no assumption from a class name |
| NT-02 | Spawn exactly one intentional variant by the already documented `SackOfSatingItem` path, and one normal nuclear explosion in **separate restored worlds** | Actual `INTENTIONAL_GAME_DESIGN`, `SIZE`, `NO_GRIEFING`, dimension, entity UUID, server config and producer trigger; verify that the second path did not silently set the intentional flag |
| NT-03 | With chunk-ticket diagnostics, observe requests on the acquisition path and removal path of one entity | For each affected `(dimension, owner UUID, chunk x/z, ticket category)`, capture before/after sets and return values; distinguish **requested** from **accepted** changes |
| NT-04 | Repeat the same experiment with destruction/griefing disabled through supported native controls, and after normal entity removal | Show whether the chunk-force branch was reached; inspect both `ENTITY` and `ENTITY_TICKING` buckets; verify any remaining tickets with attribution, not by loaded-chunk appearance alone |
| NT-05 | Reload/restart from a saved test copy; separately exercise crash recovery only with disposable backup | Verify `WasLoadingChunks`, persistent `ForcedChunksSavedData`, ticket recovery validation and removal/retention after lifecycle transitions |
| NT-06 | Test target/hit attribution in a controlled multi-player setup where permitted | Distinguish the **single** `LivingEntity.hurt` call from either DamageSource choice, rejected damage and post-damage `IRRADIATED`; no guessed player owner, PvP or Mastery |
| NT-07 | Verify any proposed bounded integration against claims, budgets and native control | Demonstrate a real version-verified boundary, maximum affected chunk count, bounded per-tick world work, cleanup under all exit paths, deduplication, rollback/abort, and server-only authority |

Every row requires a test date, tester, commit/build and exact artifact hashes,
reproduction commands, expected vs observed behavior, original logs, and the
final outcome `PASS`, `FAIL`, `BLOCKED` or `NOT_TESTED`.
Record the **specific ticket category and return value**; a chunk remaining
loaded is insufficient evidence of a persistent ticket. A server log is not a
substitute for replayable evidence.

## Release and catalog decision gate

The current consolidated catalog can certify **only the two static technical
contracts** when the jointly sealed nuclear manifest, the seven evidence axes,
the exact card hashes and the ledger/index states agree. The runtime finding in
the original TicketController snapshot remains unchanged:

- `native_release_ticket_bucket_mismatch=CONFIRMED_SELECTED_STATIC_BRANCHES_NOT_LIVE_RUNTIME`;
- `actual_persistent_ticket_leak=NOT_OBSERVED`;
- `mutating_hook=NOT_VERIFIED`;
- `physical_qa=NOT_TESTED`;
- `NO_MUTATION` for size, AoE, damage scaling, blocks, radiation, chunk loading,
  costs/procs, attribution and perks.

The automatic guard retains all exact artifact, mismatch, boolean forwarding and
runtime-state checks for both pending and static-only catalog states. Promotion
requires **both** nuclear cards, a valid literal `nuclear` family/roster,
checksummed current files and supplied text, complete seven-axis evidence and
indexes whose hook and physical-QA columns remain pending. A standalone green
row, partial pair, missing/changed seal or claimed physical success is rejected.
The consolidated manifest, gate, ledger and indexes are reviewed together in
one audited PR; the historical binary evidence is not rewritten.

**NT-01 through NT-07 remain NOT_TESTED.** The additional static inspection of
provider controller registration/callback bodies does not substitute for their
actual execution in an exact server, restart validation or ticket observation.
No native ticket category mismatch is declared fixed. A successful static CI
pass does not certify any row of the physical matrix and does not establish a
persistent leak. Mutating perk/runtime authorization remains blocked until its
own native boundary, protections/budgets and applicable physical acceptance are
independently verified.
