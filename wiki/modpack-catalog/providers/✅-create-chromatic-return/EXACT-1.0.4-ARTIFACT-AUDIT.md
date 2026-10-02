# Create: Chromatic Return 1.0.4 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ENCHANTMENT + CHARM SURFACE CLOSED`

## Identity gate

- physical JAR: `createchromaticreturn-1.0.4-neoforge-1.21.1.jar`;
- mod id: `createchromaticreturn`;
- publisher version: `1.0.4`;
- embedded runtime metadata: `1.0.0`;
- physical SHA-1: `be588d9e76ba1ce1a0556354c15fcc19d7fda133`;
- CurseForge project/file: `503784 / 8578225`.

NON-MERGE PR #530 run `37012907385` succeeded with exact physical/publisher equality.

- audit HEAD: `d86a68780e02507a169aa5e6573e56c36dce3012`;
- evidence artifact: `11228870754`;
- artifact digest: `sha256:c05a202b0e60799931bf6c91dc4902e87f823ab3dcbaabcf508aac9857c6fedb`;
- publisher SHA-256: `ae0042a1c10b5606ab2a9908465e058eecbaa1be2e7d98084886d8b73b846c67`;
- bytes: `285,356`.

## Bounded archive inventory

- entries: **493**;
- classes: **78**;
- resources: **415**;
- provider data JSONs: **253**;
- semantic-like paths selected by broad charm/flight/enchant/effect filters: **96**.

## Registry/resource magic-keyword result

`spell=0 · magic=0 · ritual=0 · ability=0 · mana=0 · arcane=0 · glyph=0`

Positive keywords are limited to equipment/enchantment domains: `charm=66`, `flight=3`, `enchant=11`.

## Exact player-driven enchant application

Direct bytecode inspection closes exactly three infused-book application branches:

- Durasteel Book -> `createchromaticreturn:durable`;
- Industrium Book -> `createchromaticreturn:wrenching`;
- Silkstrum Book -> `createchromaticreturn:super_silk_touch`.

Each branch checks the exact provider book in the off-hand, crouch state and compatible main-hand tool, replaces/consumes the infused book into a normal book and calls the vanilla ItemStack enchantment application path with the provider enchantment holder.

Exact provider recipes close acquisition for all three infused books.

These are retained in the catalog as **excluded enchantment-application utilities** rather than promoted to semantic spell/action identities.

## Exact passive charm surface

Provider Curios/tick seams apply equipment state while charms are carried/equipped. The exact artifact exposes provider effects and procedures for Creative Flight, mobility/combat potion effects, extra charm slots and related gear state.

`MultipliteFlightMobEffect` ticks provider flight state; this is not a cast/ritual root. Other charm effects are likewise passive/equipment-triggered.

## Semantic result

- standalone spell IDs: **0**;
- ritual/glyph/ability roots: **0**;
- deliberate enchant-application utilities: **3 EXCLUDED**;
- passive charm/effect families: **EXCLUDED**;
- independent semantic magic objects: **0**.

Disposition: **`ZERO_SEMANTIC_ENCHANT_GEAR_INFRA`**.

## Clean-room boundary

The durable catalog retains hashes, counts, IDs and behavior-level classification only. It does not redistribute the JAR, implementation bodies, assets or upstream localization beyond minimal identity evidence.
