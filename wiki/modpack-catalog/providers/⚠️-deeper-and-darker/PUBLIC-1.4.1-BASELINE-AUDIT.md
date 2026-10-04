# Deeper and Darker 1.4.1 — public baseline artifact audit

Status: `PUBLIC 1.4.1 BASELINE ENUMERATED / EXACT SOURCE TAG CORROBORATED / PHYSICAL RELATION OTHER_VERIFIED / NOT EXACT-CURRENT`

## Physical authority

- physical JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

## Official publisher artifacts tested

NON-MERGE PR #517 tested GitHub release `v1.4.1`, Modrinth `TuD0Zvi3`, and CurseForge project/file `659011 / 8201775`. All three produce the same bytes:

- SHA-1 `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256 `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- size `3,906,057` bytes.

Therefore `publisher_sha1 != physical_sha1`. Relation: **`OTHER_VERIFIED_PUBLISHER_DIFFERS_FROM_PHYSICAL`**.

### Retained installation-origin evidence

A retained CurseForge instance-metadata snapshot records the original installation as project **659011**, File **8201775**, filename `deeperdarker-neoforge-1.21.1-1.4.1.jar`, SHA-1 `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`, and length **3,906,057 bytes**. At the snapshot point CurseForge reports the entry as unmodified/non-working-copy/non-fuzzy.

The later physical modlist measures the same filename/runtime/byte-length lineage as SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

Disposition: **the current physical artifact is locally byte-different from the originally installed official File 8201775**. This rules out treating the mismatch as an alternate official publisher artifact, but it does not reveal the changed archive entries and therefore does not close the exact-current semantic denominator.

Local logs from the associated compatibility-work window record Deeper and Darker `PlayerMixin` / `ServerPlayerMixin` redirect conflicts with NeoVitae around container `stillValid(...)` handling. Later retained logs show Deeper and Darker applying `ContainerMenuMixin` `stillValid(...)` injections to vanilla container menus instead of those conflicting player redirects. This is a concrete compatibility-change signal, but it is not equated with the current physical JAR's complete byte delta without raw-byte comparison.

## Successful publisher-baseline audit

- branch/head: `audit/deeper-and-darker-1.4.1-exact-artifact-2026-10-02@8b4cd6b1f60805397f29af9d9d660abf508a7df6`;
- workflow run: `36959073485` — SUCCESS;
- evidence artifact: `11206937200`;
- evidence digest: `sha256:b103afe2dd4b52780acf54682ddcca4b6df484df9ad9cf7accd218e443fb8b1f`.

Public artifact inventory:

- archive entries: **2,900** including directory entries;
- classes: **207**;
- resources: **2,693**;
- `data/deeperdarker/**` paths: **1,126**.

## Exact source-tag reproduction audit

Official upstream tag `v1.4.1` resolves to `KyaniteMods/DeeperAndDarker@f7ba235d078411a1165a8cac184adfe0ccc8cebe`.

NON-MERGE PR #573 rebuilt that exact pin with Java 21:

- branch/head: `audit/deeper-and-darker-1.4.1-source-repro-2026-10-04@6919b34fd0186028f4618cc108bcc273e79e518f`;
- workflow run: `37201343546` — SUCCESS;
- evidence artifact: `11303191470`;
- evidence digest: `sha256:33ccbde9972a32b0272abdb9018254ef0bff00c39df6743eeecd57e2597e91ca`;
- rebuilt SHA-1: `23a498b9d80db87c6f81fe40584a0bc04bc80661`;
- rebuilt SHA-256: `8d9dd572306c2e3dc1d1a4508ed599547c423df65f6558915d42360fb76e2f29`;
- rebuilt size: `3,904,543` bytes.

The rebuilt artifact differs from both the physical SHA-1 `83f7...` and publisher SHA-1 `b609...`.

Normalized file-content comparison between rebuilt source and publisher artifact, excluding ZIP directory entries:

- source file entries: **2,668**;
- publisher file entries: **2,668**;
- identical-content entries: **2,408**;
- changed-content entries: **260**;
- source-only entries: **0**;
- publisher-only entries: **0**.

The semantic-path filter over the 260 differences returns only three Otherside portal asset resources:

- `assets/deeperdarker/models/block/otherside_portal_ew.json`;
- `assets/deeperdarker/models/block/otherside_portal_ns.json`;
- `assets/deeperdarker/textures/block/otherside_portal.png.mcmeta`.

No source-only or publisher-only semantic path appears. This corroborates the public action-family inventory without closing the unmatched physical artifact.

See [`SOURCE-1.4.1-REPRO-AUDIT.md`](SOURCE-1.4.1-REPRO-AUDIT.md).

## Exhaustive top-level item activation index

The public binary audit found only these item classes with ordinary Java activation/tick surfaces:

- `AncientCompassItem` — `inventoryTick`;
- `DDBoatItem` — `use`;
- `LilyFlowerItem` — `useOn`;
- `SculkTransmitterItem` — `use`, `useOn`;
- `SonorousStaffItem` — `use`, `releaseUsing`, `inventoryTick`;
- `SoulElytraItem` — `inventoryTick`;
- `WardenArmorItem` — `inventoryTick`;
- `WardenHeartItem` — `useOn`, `inventoryTick`.

The audit additionally identified network/input surfaces outside item overrides. `SoulElytraBoostPacket` is the important semantic one: the client BOOST keybind sends this payload to the server, which validates fall-flying, equipped Soul Elytra, cooldown/config, then creates the provider boost and cooldown.

The exact source pin independently corroborates those three action families:
`WardenHeartItem.useOn(...)`, `SonorousStaffItem.releaseUsing(...)`, and `SoulElytraBoostPacket` behind the BOOST keybind.

## Semantic baseline disposition

Public/source supernatural actions: **3**.

1. Heart of the Deep / Otherside Portal Activation — supernatural traversal setup/portal creation.
2. Sonorous Staff Sonic Boom — deliberate charged sonic attack.
3. Soul Elytra Boost — deliberate keybound supernatural equipment action.

Explicit exclusions:

- Ancient Compass locator;
- Sculk Transmitter remote interaction;
- ordinary boat/flower placement;
- Warden Armor passive state;
- Soul Elytra presentation tick;
- portal traversal/exit generation downstream of portal creation;
- `Catalysis`, `Sculk Smite`, `Volume`, `Reverberation` enchantments/modifiers.

## Soul Elytra config condition

The exact source defines `soulElytraCooldown` with default **600 ticks** and permits `-1` to disable the boost.

The deployed pack config value is not versioned in the sibling repository, so that eligibility remains unresolved independently of the larger physical-JAR blocker.

## Public acquisition evidence

The exact public-release data/source closes:

- Warden loot modifier -> `deeperdarker:heart_of_the_deep`;
- shaped recipe -> `deeperdarker:sonorous_staff`;
- advancement progression around Warden/entering Otherside.

These routes describe the **public/source baseline only**. They are not promoted as exact physical pack reachability while the installed JAR remains byte-different.

## Strict disposition

`PUBLIC_SOURCE_BASELINE_3 / PHYSICAL_DENOMINATOR_OPEN / +0 STRICT`.

The public release and exact source tag now mutually corroborate the three action families, but Black Arcana must not claim `3/3 exact-current` until the physical `83f7...` artifact is directly inspected or matched to an artifact with the same fingerprint.
