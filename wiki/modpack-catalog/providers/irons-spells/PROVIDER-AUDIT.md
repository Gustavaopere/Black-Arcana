# Iron's Spells 'n Spellbooks — Current Spell Catalog

Status: `NAMES COMPLETE FROM CURRENT OFFICIAL PUBLIC CATALOG; QUANTITATIVE NORMALIZATION IN PROGRESS`

- Current JAR: `irons_spellbooks-1.21.1-3.16.3.jar`
- Mod id: `irons_spellbooks`
- Runtime version: `1.21.1-3.16.3`
- Provider class: `ENGINE / PRIMARY PROVIDER`
- Primary resource authority: Iron's mana/casting pipeline.
- Current public documentation baseline: Iron's official spell catalog and changelog for the 3.16.x line.

## Catalog rules

The spell names below are factual identifiers from the current public provider catalog. Black Arcana does not copy provider prose. Numeric fields are normalized only when confirmed by current public documentation or the installed JAR/config through a permitted validation path.

Current official catalog enumerates **110 spell entries across 9 schools**.

## Blood — 10

- `Acupuncture`
- `Blood Needles`
- `Blood Slash`
- `Blood Step`
- `Devour`
- `Heartstop`
- `Raise Dead`
- `Ray Of Siphoning`
- `Sacrifice`
- `Wither Skull`

## Eldritch — 7

- `Abyssal Shroud`
- `Eldritch Blast`
- `Planar Sight`
- `Pocket Dimension`
- `Sculk Tentacles`
- `Sonic Boom`
- `Telekinesis`

## Ender — 16

- `Arcane Shackle`
- `Black Hole`
- `Counterspell`
- `Dragon's Breath`
- `Echoing Strikes`
- `Evasion`
- `Gravity Fissure`
- `Magic Arrow`
- `Magic Missile`
- `Portal`
- `Recall`
- `Shadow Slash`
- `Starfall`
- `Summon Ender Chest`
- `Summon Swords`
- `Teleport`

## Evocation — 17

- `Arrow Volley`
- `Chain Creeper`
- `Fang Strike`
- `Fang Swirl`
- `Fang Ward`
- `Firecracker`
- `Gust`
- `Invisibility`
- `Lob Creeper`
- `Scapegoat`
- `Shield`
- `Slow`
- `Spectral Hammer`
- `Summon Horse`
- `Summon Vex`
- `Throw`
- `Wololo`

## Fire — 13

- `Blaze Storm`
- `Burning Dash`
- `Fire Arrow`
- `Fire Breath`
- `Fireball`
- `Firebolt`
- `Flaming Barrage`
- `Flaming Strike`
- `Heat Surge`
- `Magma Bomb`
- `Raise Hell`
- `Scorch`
- `Wall Of Fire`

## Holy — 12

- `Angel Wings`
- `Blessing Of Life`
- `Cleanse`
- `Divine Smite`
- `Fortify`
- `Greater Heal`
- `Guiding Bolt`
- `Haste`
- `Heal`
- `Healing Circle`
- `Sunbeam`
- `Wisp`

## Ice — 12

- `Blizzard`
- `Cone Of Cold`
- `Frost Step`
- `Frostbite`
- `Frostwave`
- `Ice Block`
- `Ice Spikes`
- `Ice Tomb`
- `Icicle`
- `Ray Of Frost`
- `Snowball`
- `Summon Polar Bear`

## Lightning — 10

- `Ascension`
- `Ball Lightning`
- `Chain Lightning`
- `Charge`
- `Electrocute`
- `Lightning Bolt`
- `Lightning Lance`
- `Shockwave`
- `Thunderstorm`
- `Volt Strike`

## Nature — 13

- `Acid Spit`
- `Aspect Of The Spider`
- `Blight`
- `Earthquake`
- `Firefly Swarm`
- `Gluttony`
- `Oakskin`
- `Poison Arrow`
- `Poison Splash`
- `Poison Spray`
- `Root`
- `Stomp`
- `Touch Dig`

## Immediate deduplication relevance

This section is only a routing note for later capability comparison; it is not the final Phase 2 deduplication matrix.

- **Chaos candidates:** existing Iron's already covers telekinesis, black-hole/gravity control, spatial displacement, planar/pocket-space utility, projectiles, storms and several chaotic-looking area attacks. Chaos must therefore be defined by its rules/entropy/probability/reality semantics rather than by duplicating these visuals.
- **Order candidates:** Iron's already covers counterspelling, shielding, shackling/root-like control, haste/slow, portals, recall and substantial Holy support. Order needs law/seal/geometry/constraint semantics with a real delta.
- **Binding candidates:** Iron's already contains Arcane Shackle, summon systems, Sacrifice, Raise Dead and multiple controlled summons. Black Arcana binding must remain the typed relationship/resource-routing layer rather than a renamed summon spell family.
- **Divine/Celestial candidates:** the Holy school already provides healing, cleansing, fortification, haste, holy offense, flight and persistent healing zones. Any new Divine/Celestial catalog must deduplicate against this school first.
- **Infernal candidates:** Fire already provides bolts, breath, projectiles, walls, fields, shockwaves and mobility. Infernal identity cannot be only stronger/redder fire.
- **Witchcraft/toxic candidates:** Nature already provides poison, blight, armor reduction, roots and several ecological/earth effects; Hexalia/Toxony still need their own catalog before a Witchcraft delta can be approved.

## Quantitative ingestion status

The official current spell page exposes, per spell where applicable, level range, cooldown, mana, cast type, rarity and quantitative effect fields. Those values will be normalized into per-capability records in subsequent Phase 2 commits. Until a row is normalized, no number should be copied from an older guide or assumed from memory.

### Verified examples from the current public catalog

| Spell | School | Levels | Cooldown | Mana | Cast type | Key verified quantitative behavior |
|---|---|---:|---:|---:|---|---|
| Acupuncture | Blood | 1–10 | 20 s | 25–70 | Instant | 2 damage; 5–14 projectiles; heals caster for 25% of delivered damage |
| Blood Slash | Blood | 1–5 | 10 s | 25–45 | Instant | 10–14 damage; heals 15% of delivered damage |
| Heartstop | Blood | 1–5 | 120 s | 100–140 | Instant | 10–16 s effect; deferred backlash equals 50% of damage accumulated during the invulnerability window |
| Ray Of Siphoning | Blood | 1–10 | 15 s | 8–17 | Continuous | 1–3.25 damage; 12-block range; heals for 100% of delivered damage |
| Telekinesis | Eldritch | 1–5 | 35 s | 25 | Continuous | 12–20-block range; forced entity movement/kinetic interaction |
| Arcane Shackle | Ender | 1–8 | 45 s | 40–96 | Long | 15 HP chain objects; 11–25 s duration; 5-block listed range |
| Black Hole | Ender | 1–6 | 120 s | 300–800 | Long | 2 AOE damage; 6–16-block radius; pull/crush field |
| Gravity Fissure | Ender | 1–5 | 45 s | 150–250 | Long | 3.5-block radius; 3–7 s duration; pull field with no direct damage |
| Portal | Ender | 1–3 | 180 s | 200–220 | Instant | 48-block cast range; 5–9 minute portal duration |
| Shield | Evocation | 1–10 | 8 s | 35–80 | Instant | 15–105 HP stationary barrier |
| Scapegoat | Evocation | 1–3 | 45 s | 30–60 | Instant | 12-block taunt range; 20–40 HP decoy |
| Angel Wings | Holy | 1–5 | 120 s | 80–160 | Instant | 10–50 s temporary elytra-style flight |
| Healing Circle | Holy | 1–10 | 25 s | 40–130 | Long | 0.5–2.75 AOE healing; 5-block radius; 10 s duration |
| Thunderstorm | Lightning | 1–8 | 120 s | 70–140 | Long | 8–15 damage; 20-block radius; 20–34 s duration |
| Root | Nature | 1–10 | 35 s | 45–72 | Long | 5–14 s root; listed 40 HP for the root object |

## Provenance note

Iron's repository source is not treated as an implementation reference by default. This catalog uses the public official Wiki/changelog and the current installed mod identity. Source-derived implementation work would require exact-license compatibility plus the Black Arcana provenance ledger gate.
