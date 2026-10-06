# Deeper and Darker 1.4.1 — public/source baseline action cards

Status: `3 PUBLIC+SOURCE SUPERNATURAL ROOTS / QUANTITATIVE SOURCE CONTRACT RECORDED / PHYSICAL EXACTNESS OPEN / ALL +0 STRICT`

These are clean-room behavior cards for the official public 1.4.1 artifact, corroborated against exact upstream tag `v1.4.1` / commit `f7ba235d078411a1165a8cac184adfe0ccc8cebe`.

They are **not** asserted as the exact installed-pack denominator because the physical SHA-1 `83f7edd0...` differs from every official public artifact tested and from the clean source rebuild produced by NON-MERGE PR #573. Quantitative values below are public/source baseline values, not deployed-byte claims.

Individual action files:

- [Otherside Portal Activation](otherside-portal-activation.md)
- [Sonorous Staff Sonic Boom](sonorous-staff-sonic-boom.md)
- [Soul Elytra Boost](soul-elytra-boost.md)

These files are a materialization of the same three baseline roots and add **+0** to the current strict numerator.

## 1. Otherside Portal Activation

- owner item: `deeperdarker:heart_of_the_deep`;
- public/source implementation seam: `WardenHeartItem.useOn(...)`;
- semantic type: supernatural portal-creation/traversal setup;
- public/source baseline state: `BASELINE_PRESENT`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

### Exact item and admission contract

Exact 1.4.1 item registration defines Heart of the Deep as stack size **1**, rarity **RARE**, and fire resistant.

`WardenHeartItem.useOn(...)` admits the action only when the user is a player in either the **Overworld** or **Otherside**, then evaluates the block position adjacent to the clicked face.

The exact `OthersidePortalBlock.OthersidePortalShape` validator requires:

- reinforced deepslate frame;
- interior width: **2–21 blocks**;
- interior height: **2–21 blocks**;
- the broader shape/lifecycle validator accepts interior cells that are air or already occupied by Otherside portal blocks.

For **new Heart activation**, `OthersidePortalBlock.isPortal(...)` additionally requires `numPortalBlocks == 0`; any pre-existing Otherside portal block in the selected frame prevents a new portal spawn through this action.

The player-facing activation path does **not** read `othersidePortalWidth` / `othersidePortalHeight`; those config fields are therefore not projected onto this action card.

### Settlement

On successful portal creation:

- provider creates the portal blocks;
- plays the Sculk Catalyst bloom sound at provider-selected volume/pitch;
- non-creative player loses the Heart of the Deep;
- creative player retains it;
- action returns success.

If the frame cannot spawn a portal, the use fails and this path does not consume the item.

### Acquisition

Exact generated 1.4.1 loot data adds exactly **1** `deeperdarker:heart_of_the_deep` to the vanilla Warden loot-table context through the provider's `deeperdarker:add` loot modifier (`min = 1`, `max = 1`).

### Adjacent non-action behavior

`WardenHeartItem.inventoryTick(...)` can emit Warden heartbeat presentation sounds when `wardenHeartPulses` is enabled. Exact source default is `true`; this pulse is presentation/state behavior and is **not** counted as another supernatural action.

Portal collision/travel after creation and destination-side portal generation are consequences of this root, not additional spell identities.

## 2. Sonorous Staff Sonic Boom

- owner item: `deeperdarker:sonorous_staff`;
- public/source implementation seam: `SonorousStaffItem.use(...)` + `releaseUsing(...)`;
- semantic type: discrete supernatural staff attack;
- public/source baseline state: `BASELINE_PRESENT`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / +0`.

### Exact item contract

Exact 1.4.1 registration defines:

- durability: **320**;
- rarity: **RARE**;
- repair item: `deeperdarker:soul_crystal`.

The exact `#deeperdarker:sonic_weapon` item tag contains only `deeperdarker:sonorous_staff`.

### Trigger and charge state

- ordinary use starts the charge/use state;
- release executes the sonic attack;
- maximum exposed use duration: **72,000 ticks**.

The item writes a presentation flag named `charged` after **128 ticks** of continuous use. That threshold drives charged presentation/foil state; the source does **not** use it as a release-admission gate.

Let `t` be ticks actually used before release, `V` the Volume enchantment level, and `R` the Reverberation enchantment level.

Exact generated enchantment data defines Volume max level **4** and Reverberation max level **3**.

### Damage formula

Pre-distance damage is:

`round(50 × (1 + V/4) / (1 + 16 / exp(0.06 × t)))`

Therefore damage increases with charge time; Volume scales the numerator; asymptotic source damage approaches **50** at Volume 0 and **100** at Volume 4.

### Range formula

Scan range is:

`min(80, round(4.5 × (1 + 2R/3) × ln(t + 1)))`

- hard range cap: **80 blocks**;
- Reverberation increases effective range;
- Reverberation does not mint a second action identity.

### Propagation and targets

The attack scans forward from the player's eye position one block-step at a time.

- scan stops at the first non-air block that can occlude;
- caster is excluded;
- living entities intersecting a per-step AABB expanded by **0.4** blocks are eligible;
- multiple living entities may be hit across the line scan.

Distance-adjusted damage is:

`round(baseDamage × (1 - (1/3) × (i/range)^2))`

where `i` is the current scan distance index.

The attack uses the sonic-boom damage source and applies directional push scaled by the target's knockback resistance.

### Settlement

Every executed release settles:

- staff durability damage: **1**;
- item-used stat increment;
- provider staff sound;
- item cooldown: **20 ticks**.

### Acquisition

Exact shaped recipe ingredients are Heart of the Deep, Soul Crystal and Sculk Bone, with pattern:

- ` CH`
- ` BC`
- `B  `

Result: **1 Sonorous Staff**.

### Enchantment relationship

`Volume` and `Reverberation` modify this same release action and are not separate spell identities.

The other exact-source Deeper and Darker enchantments remain enchantment mechanics rather than standalone castable roots:

- `Catalysis` — max level **3**, post-attack environment-catalysis effect;
- `Sculk Smite` — max level **5**, adds **2.5 damage per level** against the provider's sensitive entity tag.

## 3. Soul Elytra Boost

- owner item: `deeperdarker:soul_elytra`;
- public/source implementation seam: BOOST keybind -> server payload `deeperdarker:soul_elytra_boost` / `SoulElytraBoostPacket`;
- semantic type: discrete supernatural equipment/flight action;
- public/source baseline state: `BASELINE_PRESENT / CONFIG_CONDITIONAL`;
- strict current-pack state: `OPEN_PHYSICAL_ARTIFACT / DEPLOYED_CONFIG_UNKNOWN / +0`.

### Exact item contract

Exact 1.4.1 registration defines:

- durability: **956**;
- rarity: **UNCOMMON**;
- chest armor attribute: **+3 armor**;
- repair item: `deeperdarker:soul_crystal`.

### Acquisition

Exact shaped recipe ingredients are Sculk Bone, Soul Crystal, Soul Dust and a vanilla Elytra, with pattern:

- `BCB`
- `DED`
- `B B`

Result: **1 Soul Elytra**.

### Network/action identity

Exact source payload ID is `deeperdarker:soul_elytra_boost`. The server handler is the provider-owned settlement seam for the boost.

### Config contract

Exact 1.4.1 COMMON config key:

- `soulElytraCooldown`;
- source default: **600 ticks**;
- valid range: **-1..12000**;
- `-1`: disables the boost action.

The deployed pack loads `config/deeperdarker-common.toml`, but the effective value is not retained in available evidence. Exact deployed enablement therefore remains unknown.

See [`../DEPLOYED-CONFIG-CHECKPOINT.md`](../DEPLOYED-CONFIG-CHECKPOINT.md).

### Server admission

When not disabled by config, the handler requires:

- player is fall-flying;
- chest armor slot contains Soul Elytra;
- Soul Elytra is not currently on cooldown.

If `soulElytraCooldown == -1`, the handler returns without spawning a boost.

### Settlement

On admission:

- provider creates a vanilla `FireworkRocketEntity` attached to the player using a plain Firework Rocket item stack;
- rocket entity is added to the level;
- Soul Elytra receives item cooldown equal to the effective `soulElytraCooldown` value.

The ordinary `SoulElytraItem.inventoryTick(...)` path only displays cooldown state client-side and does not mint another semantic action.

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
