# Call Broom

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:call_broom`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Ordinary crafting:** disabled
- **Ordinary looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 20 ticks`
- requires a unique equipped provider broom resolved through `BroomCurioSupport.findUniqueEquippedBroom(...)`

## Provider lifecycle

The spell is explicitly item-only: ordinary crafting and looting are disabled. Client preflight checks that the player is not already a passenger and can resolve exactly one equipped broom. Server pre-cast delegates to `CallBroomDeploymentManager.validate(...)`; failures distinguish no broom from a mount/recall state that cannot safely execute.

A successful server cast delegates the actual deployment/recall transition to `CallBroomDeploymentManager.execute(...)`. The provider owns broom identity, Curios lookup, mount state and movement/deployment semantics.

## Causality and progression

Calling or recalling the broom is one provider cast. Riding distance, mounted ticks or repeated movement must not generate spell Mastery merely because the vehicle originated from a spell.

## Deduplication

Occupies the **Curios-equipped broom deployment/recall spell with provider mount-state validation** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+ITEM-ONLY ACQUISITION+CURIO REQUIREMENT+SERVER VALIDATION / BROOM DEPLOYMENT POSITION+PERSISTENCE+MOUNT DETAILS REQUIRE MANAGER AUDIT`