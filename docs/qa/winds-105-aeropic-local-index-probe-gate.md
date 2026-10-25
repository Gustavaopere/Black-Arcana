# Wind's 1.0.5 — Aeropic local-index proof probe

**State:** AUDIT PENDING EXACT-JAR RESULT. This is an independent static-evidence-only follow-up to merged PR #893. No runtime, casting, perk, modpack, or stage implementation changed.

## Reason for the experiment

The PR #893 bounded JVM abstract-stack analyzer treats javap noncompact loads/stores with explicit numeric operands (for example, aload 4 and astore 4) as unresolved locals. This is safely conservative but may hide a locally provable producer-to-receiver relationship.

The new script winds_105_aeropic_local_indices.py independently reads the original javap instruction text, matches every instruction against the prior method/offset/opcode parser, extracts exact explicit load/store indices and creates synthetic compact-style tokens only for the bounded preexisting symbolic analyzer. Normalization does not rewrite third-party code or claim that the bytecode contained the compact opcode.

## Authority and exact provider

- Wind's Spellbooks 1.0.5, publisher SHA-1 8744886899bc245ae147a44baa2b183689cec7da, not an arbitrary latest version.
- Selected callsites only: AeropicEffect.applyEffectTick and AeropicEffect.onEffectAdded, each with exactly one invocation of AbstractSpell.getRecastCount.
- Existing negative results from PR #893 remain unchanged. An observed compiled receiver candidate must be reviewed separately against the SHA-exact artifact before any documentary upgrade.
- Host Iron's 3.16.3 installed binary checksum and live override dispatch NOT VERIFIED.
- Source field, cast and same-method invocation never establish the type returned by Supplier.get or the gameplay recipient of the integer result.
- PlayerRecasts, NBT, real client/Survival and safe mutating hook remain NOT_PROVEN/NOT_TESTED.
- Fail-closed synthetic cases cover indices, aliasing, alternative supplier symbols, branches and binary identity.

## Exit criterion

Run the dedicated SHA-gated GitHub Action, inspect its symbolic JSON, document any new *verified* static conclusion in the spell dossier, verify both Black Arcana CI jobs on the final branch head, reconcile with the latest main, and only then consider merging. No automatic promotion of runtime or perks is permitted.

**Catalog:** Wind's 7/7 spell identities; nine selected scalar getters 9/9. Binary identity campaign 38/39, independent from global completion. Global magic-object lower bound >=1,856; denominator still open. Stage 06.05 remains active; real-client Stage 09 remains pending.
