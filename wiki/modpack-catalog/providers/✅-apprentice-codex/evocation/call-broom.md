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
- `castTime = 20 ticks / 1 s`
- recall-distance threshold for an unoccupied deployed broom: **8 blocks**
- requires a unique equipped provider broom resolved through `BroomCurioSupport.findUniqueEquippedBroom(...)`

## Admission

The spell is explicitly item-bound: ordinary crafting and looting are disabled. It only accepts a player caster.

Client preflight requires:

- the player is not already a passenger;
- one unique equipped provider broom can be resolved.

The server then delegates to `CallBroomDeploymentManager.validate(...)`. Exact failure states are:

- `NOT_FOUND` — no valid equipped broom;
- `RIDING` — caster is already a passenger;
- `OCCUPIED` — the relevant owned/deployed broom is currently being ridden and cannot be safely recalled/replaced.

## Provider deployment / recall transaction

When a valid deployed broom matching the equipped item already exists and is not occupied, the cast recalls it through the provider lifecycle.

Otherwise the manager:

1. recalls stale unoccupied brooms owned by the player;
2. clears stale deployment state from the equipped broom item;
3. creates the provider broom entity from that exact equipped item;
4. assigns owner and copies the item's custom name;
5. spawns the broom at the player;
6. requires the player to begin riding it successfully;
7. only then stores the deployed entity UUID on the broom item.

If entity insertion fails, the transaction returns failure. If mounting fails after insertion, the provider recalls the broom and does not leave it as a successful deployment.

## Reconciliation and automatic recall

Provider state remains tied to the equipped broom item and owner. The manager recalls or clears deployment state when appropriate on unequip, broom removal, login/logout and ownership/equipment mismatch.

`shouldRecall(...)` returns true when:

- the owner is dead;
- owner and broom are in different levels;
- the broom is being controlled by someone other than its owner;
- an unoccupied broom is more than **8 blocks** from the owner;
- the deployed entity no longer matches the uniquely equipped broom item/state.

## Performance caveat

At the exact source pin, helper paths that find all owned broom entities iterate all server levels and each level's `getAllEntities()`. That is upstream provider behavior and **must not be copied into Black Arcana**. Black Arcana's own summons/owned entities must continue using bounded/indexed ownership contracts rather than global entity scans.

## Causality and progression

Calling or recalling the broom is one provider cast. Riding distance, mounted ticks, login reconciliation or automatic recall are provider lifecycle effects and must not generate repeated spell Mastery.

Black Arcana does not own broom identity, Curios lookup, deployment UUIDs, mount persistence or recall semantics and must not create a second broom/familiar ledger.

## Deduplication

Occupies the **Curios-equipped provider broom deployment/recall spell with owner-bound mount reconciliation** niche.

## Confidence

`SOURCE-PINNED SPELL + DEPLOYMENT MANAGER / EXACT ITEM GATE+FAILURE STATES+SPAWN/MOUNT TRANSACTION+8-BLOCK RECALL+LOGIN/LOGOUT/UNEQUIP RECONCILIATION / FULL MODPACK MOUNT RUNTIME QA PENDING`