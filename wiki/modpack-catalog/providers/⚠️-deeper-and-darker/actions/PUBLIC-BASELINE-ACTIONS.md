# Deeper and Darker 1.4.1 — public/source baseline action cards

Status: `3 PUBLIC+SOURCE SUPERNATURAL ROOTS / PHYSICAL EXACTNESS OPEN / ALL +0 STRICT`

These are clean-room behavior cards for the official public 1.4.1 artifact, corroborated against exact upstream tag `v1.4.1` / commit `f7ba235d078411a1165a8cac184adfe0ccc8cebe`.

They are **not** asserted as the exact installed-pack denominator because the physical SHA-1 `83f7edd0...` differs from every official public artifact tested and from the clean source rebuild produced by NON-MERGE PR #573.

## 1. Otherside Portal Activation

- owner item: `deeperdarker:heart_of_the_deep`;
- public/source implementation seam: `WardenHeartItem.useOn(...)`;
- trigger: player uses the Heart adjacent to a valid reinforced-deepslate portal frame in Overworld/Otherside;
- settlement: provider validates the frame and calls its Otherside portal `spawnPortal(...)` path;
- public acquisition: provider Warden loot modifier;
- semantic type: supernatural portal-creation/traversal setup;
- public/source baseline state: `BASELINE_PRESENT`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

Portal collision/travel after creation and destination-side portal generation are consequences of this action, not additional spell identities. `WardenHeartItem.inventoryTick(...)` only supplies heartbeat presentation behavior and is not a second action.

## 2. Sonorous Staff Sonic Boom

- owner item: `deeperdarker:sonorous_staff`;
- public/source implementation seam: `SonorousStaffItem.use(...)` + `releaseUsing(...)`;
- trigger: hold/use and release;
- settlement: provider projects a sonic-boom line, applies sonic damage/knockback, durability use and cooldown;
- public acquisition: exact shaped recipe;
- modifiers: `Volume` and `Reverberation` alter damage/range of the same release action rather than minting new actions;
- semantic type: discrete supernatural staff attack;
- public/source baseline state: `BASELINE_PRESENT`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

The four provider enchantments visible in the exact source — `Catalysis`, `Sculk Smite`, `Volume`, and `Reverberation` — remain enchantment/modifier surfaces under the semantic ledger, not four standalone spells.

## 3. Soul Elytra Boost

- owner item: `deeperdarker:soul_elytra`;
- public/source implementation seam: BOOST keybind -> server payload `deeperdarker:soul_elytra_boost` / `SoulElytraBoostPacket`;
- trigger: dedicated client BOOST keybind;
- server admission: player must be fall-flying, chest slot must contain Soul Elytra, item must not be on cooldown, and provider config must not disable the action;
- settlement: provider creates its firework-style boost and applies the configured Soul Elytra cooldown;
- exact-source config default: `soulElytraCooldown = 600` ticks;
- exact-source disable value: `soulElytraCooldown = -1`;
- deployed pack config: `NOT VERIFIED`;
- semantic type: discrete supernatural equipment/flight action;
- public/source baseline state: `BASELINE_PRESENT / CONFIG_CONDITIONAL`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

The ordinary `SoulElytraItem.inventoryTick(...)` path is presentation/state support and does not mint another semantic identity.

## Excluded adjacent surfaces

- `SculkTransmitterItem` and its TRANSMIT keybind — remote inventory/block interaction utility;
- `AncientCompassItem` — structure locator;
- `SoulElytraItem.inventoryTick(...)` — presentation/cooldown feedback;
- `WardenArmorItem.inventoryTick(...)` — passive effect suppression;
- boats/flower interactions — ordinary item placement;
- portal traversal after activation — downstream lifecycle;
- `Catalysis`, `Sculk Smite`, `Volume`, `Reverberation` — enchantments/modifiers excluded by the semantic-magic metric.

## Source-reproduction evidence

NON-MERGE PR #573 / run `37201343546` rebuilt the exact upstream tag successfully:

- source-build SHA-1: `23a498b9d80db87c6f81fe40584a0bc04bc80661`;
- official publisher SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- physical pack SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

All three hashes differ.

The source build and official publisher JAR have the same 2,668 file paths. Of those, 2,408 file contents are identical and 260 differ. The semantic-difference filter finds only three Otherside portal asset resources and no source-only/publisher-only semantic path.

This strengthens the three-root baseline but does not close the unmatched physical JAR.

## Accounting

- public/source supernatural roots: **3**;
- exact-current physical roots proven: **0**;
- exact-current physical denominator: **UNKNOWN**;
- strict contribution: **+0**;
- provider state: **⚠️ partial / physical denominator open**.
