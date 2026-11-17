# Alex's Mobs 2.1.13 — AMNetContext concrete bridge + registration bootstrap

**Status:** 🟡 SHA-exact JAR discovery candidate; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

## Why this pass is necessary

The merged [Transmutation C2S audit](alexsmobs-213-transmutation-c2s-handoff.md) and [sealed snapshot](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-C2S-2.1.13.json) establish the native message, handler, sender-ID comparison, active-menu type gate and the call to `transmute(Player,int)`. They **do not** establish which concrete object implements `AMNetContext`, whether `getSender()` is bound to the authenticated network connection, or which LambdaMetafactory handles are registered for the publisher's packet.

This follow-up adds a reproducible read-only probe rather than re-certifying the previously merged message receiver.

## Physical identity and bounded procedure

- Provider: `alexsmobs`; publisher JAR previously matched to the physical modlist: `alexsmobs-2.1.13-neoforge+1.21.1.jar`; Minecraft 1.21.1, NeoForge, Java 21.
- Reconfirmation against a newer physical modlist export remains required if the sibling changes; the current GitHub tree scan did not expose an Alex's Mobs-named modlist entry. This probe never upgrades the historical fingerprint into an unqualified current-version claim.\n- Publisher artifact CurseForge project/file `1635121/8856498`; SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`; SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`; 27,452,738 bytes.
- [New auditor](alexsmobs_213_context_bridge_probe.py), [eight synthetic tests](alexsmobs_213_context_bridge_probe_test.py), [CI workflow](../.github/workflows/alexsmobs-213-context-bridge.yml).
- The auditor validates both hashes, file size, archive membership, classfile major version and bounded candidate cohort. It selects provider classfiles referencing `AMNetContext`, records only methods relevant to context/dispatch, identifies **direct** `implements AMNetContext` declarations, and extracts limited `AlexsMobs.setup` bootstrap-handle candidates.
- The generated JSON is a discovery **artifact**, not a sealed new certification. Do not mark the new evidence SHA-verified until the corresponding CI completes successfully on the publisher JAR.

## Evidence semantics / negatives

- Presence of `AMNetContext` in a class constant pool is **only a search signal**, not an implementation or caller proof.
- Direct implementation of the interface is stronger evidence but does **not** prove connection ownership, `getSender` authenticity or the absence of wrappers in external dependencies (e.g. CodxLib).
- `invokedynamic` and `BootstrapMethods` matches are **candidate** callback links; the exact `registerMessage` invocation's bootstrap indices, method handles, direction and actual execution order still require contextual reconciliation.
- No index, certificate or universe counters change from this auditor alone. The three semantic roots remain the observed denominator, with Item Transmutation ⚠️ partial/conditioned.
- Explicit outstanding negatives: sender spoofing, replay, concurrent settlement, wrong table/session, player dimension transition, choice out of range/clamp and item/XP double-processing in dedicated multiplayer.
- Black Arcana must not reapply provider-owned `Slot.set`, `giveExperienceLevels` or `postTransmute`. No perk XP discount, reroll, output or Mastery mutation can be enabled by this passive evidence.

## Next acceptance gates

1. Inspect and SHA-seal the CI JSON only after obtaining the real publisher result and reasoning about the concrete context implementation.
2. Trace the actual callback bindings and transport direction, and distinguish registered handlers from syntactic lambdas.
3. Design and run targeted negative tests for spoofing, stale menus, replay and concurrent settlement; complete physical modpack/NeoForge QA separately.
4. Only after the full individual static contract is evidenced may the certified count change; a mutating hook requires separate proof.

Stage 06 is not promoted by this catalog work. No modifications to Enshrouded or RPG Skill Tree.
