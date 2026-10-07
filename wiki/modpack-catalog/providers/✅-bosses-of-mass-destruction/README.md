# Bosses of Mass Destruction — 1.3.3

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 5 SUPERNATURAL ACTION ROOTS / 3 COUNTED_EXACT + 2 CONDITIONAL / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority identifies:

- physical row: **#82**;
- JAR: `BOMD-NeoForge-1.21-1.3.3.jar`;
- mod id: `bosses_of_mass_destruction`;
- runtime: `1.3.3`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `446ff63afb858ad49149d24b72541739de83d38d`.

Bosses of Mass Destruction is cross-domain for the magic catalog: its physical category is Mobs/Structures, but the exact installed artifact owns deliberate boss-summoning and supernatural traversal/restoration actions.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#515** audits CurseForge project/file `941573 / 8448640` and hard-gates the artifact against the physical pack fingerprint.

- audit HEAD: `f29e3dbadd76b729f9cba826f56516c644f1bfa2`;
- exact-artifact run: `36955037836` — **SUCCESS**;
- evidence artifact: `11206056202`;
- evidence digest: `sha256:3b756714d059e5459273a9840ae33ef9a0f2d3f432adb98f51e1719c0f48e2f1`;
- publisher SHA-1: `446ff63afb858ad49149d24b72541739de83d38d`;
- publisher SHA-256: `93da8753a00229e41c5ed399e6cf849737e7bd9b4109d5d8e4ad3a20136deb82`;
- bytes: `1,952,017`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

The exact artifact contains **763 archive entries / 287 classes / 476 resources / 94 data paths**. Exhaustive signature scanning finds only four provider item classes with direct player activation methods: Brimstone Nectar, Charged Ender Pearl, Earthdive Spear and Soul Star. Obsidilith Summoning is reached through the provider mixin on vanilla Ender Eye use.

See [`EXACT-1.3.3-ARTIFACT-AUDIT.md`](EXACT-1.3.3-ARTIFACT-AUDIT.md).

## Semantic inventory — five supernatural roots

Detailed cards:

- aggregate: [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md);
- [Obsidilith Summoning](actions/obsidilith-summoning.md);
- [Earthdive Wall Teleport](actions/earthdive-wall-teleport.md);
- [Brimstone Structure Restoration](actions/brimstone-structure-restoration.md);
- [Night Lich Summoning](actions/night-lich-summoning.md);
- [Charged Ender Pearl Teleport](actions/charged-ender-pearl-teleport.md).

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

### Strict exact-current — 3

1. **Obsidilith Summoning** — Eye of Ender used on the provider Obsidian Altar schedules and spawns the Obsidilith;
2. **Earthdive Wall Teleport** — charged Earthdive Spear use performs the provider wall-teleport action;
3. **Brimstone Structure Restoration** — Brimstone Nectar deliberately restores eligible nearby BOMD boss structures.

### Exact identities, current reachability conditioned — 2

4. **Night Lich Summoning** — Soul Star placement on the Chiseled Stone Altar network summons the Night Lich; normal Soul Star production is gated by provider config `lichConfig.summonMechanic.isEnabled`, whose deployed value is not captured;
5. **Charged Ender Pearl Teleport** — exact player-use teleport/effect action; its recipe requires `ancient_anima`, whose exact provider-native normal source is Lich entity loot, so current normal reachability inherits the unresolved Lich summon gate.

Therefore the provider contributes **+3 strict** and retains **2 conditional** supernatural roots.

## Exact acquisition/reachability

Catalog-level strict reachability is closed for:

- Obsidilith Summoning: exact packaged Obsidilith arena/worldgen surface + vanilla Eye of Ender interaction with the provider summon frame;
- Earthdive Spear: exact crafting recipe using `obsidian_heart`, `void_thorn` and a stick; exact provider data supplies Obsidian Heart in the Obsidilith arena chest and Void Thorn in Void Blossom entity loot; the exact Void Blossom summon block entity spawns the boss automatically when a player enters its arena proximity;
- Brimstone Nectar: exact shapeless recipe using only vanilla Netherite Scrap, Dragon's Breath and Ghast Tear.

Conditional reachability:

- Soul Star normal production is controlled by `lichConfig.summonMechanic.isEnabled`; exact binary default is `true`, but the deployed effective config is not available;
- Charged Ender Pearl has an exact shapeless recipe, but requires `ancient_anima`; exact provider data gives Ancient Anima through Lich entity loot, so this action remains conditional with the Lich path.

## Metric exclusions

The following exact BOMD surfaces do not create additional semantic magic identities:

- Soul Star's ordinary structure-locator use;
- automatic Void Blossom proximity spawning;
- boss AI attacks and projectiles;
- passive/environmental Levitation Block, Mob Ward and Monolith behavior;
- Obsidilith runes, boss arena blocks and other structure infrastructure;
- particles, sounds, delayed scheduler phases and downstream entity effects;
- ordinary consumables/materials and boss loot as objects by themselves.

Void Blossom spawning is explicitly not counted as a player summon: the exact block entity checks for a player within 40 blocks and automatically spawns the boss.

## Authority boundary

BOMD remains authority for summon structures, boss lifecycle, structure repair, projectile settlement, teleport settlement, loot and configuration. Black Arcana catalogs these roots but must not replay a summon, perform a second teleport, restore a structure twice or duplicate provider resource consumption.

## Runtime QA remains separate

Catalog closure does not assert complete-modpack runtime PASS. Remaining QA includes effective BOMD config, worldgen coexistence, structure presence in old/new chunks, Epic Fight/combat interactions, multiplayer summon ownership, chunk unload/restart and protection/claim behavior.

## Result

**✅ Cataloged — exact action denominator closed.**

Current BOMD semantic inventory: **5 supernatural action roots = 3 `COUNTED_EXACT` + 2 `CONDITIONAL`**.

Strict semantic delta: **+3**.
