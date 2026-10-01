# BetterEnd 21.0.34 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / RITUAL DENOMINATOR CLOSED`

## Identity gate

The current physical sibling dossier identifies:

- `BetterEnd-21.0.34.jar`;
- mod id `betterend`;
- SHA-1 `149b73179ea63bf777315a7c850b2eba65c554bd`.

NON-MERGE PR #497 downloads CurseForge File `1422294 / 8610367` and fails before semantic inspection unless its SHA-1 equals the physical fingerprint.

Final bounded audit:

- HEAD: `f296d3fde0ebb01a85a4b6aa7e3f46a0c5dbaa92`;
- run: `36901757754` — SUCCESS;
- artifact: `11182076262`;
- artifact digest: `sha256:9e7b92ddea636bb52349df6ab865a3efb7c12646ad1f4fa256ffb6561c4e1dce`;
- publisher SHA-1: `149b73179ea63bf777315a7c850b2eba65c554bd`;
- publisher SHA-256: `45befc75466153f2f62d8c17a790b58ce794a4216ea152fc21190aa9dc40a440`;
- bytes: `97,673,585`.

Result: exact publisher/physical equality is proven.

## Bounded archive inventory

- archive entries: **10,430**;
- classes: **682**;
- non-class resources: **9,748**;
- `data/betterend/**` paths: **3,146**;
- ritual-like bounded paths: **90**.

No third-party JAR bytes are committed to Black Arcana.

## Exact Infusion Ritual inventory

The audit parses every provider recipe JSON and selects entries whose recipe type is `betterend:infusion`.

- exact infusion recipes: **48**;
- unique recipe IDs: **48**;
- invalid recipe JSONs: **0**;
- unique result item IDs: **10**;
- duplicate recipe IDs: **0**.

Thirty-nine recipes produce enchanted books; nine produce BetterEnd items/equipment. Repeated `minecraft:enchanted_book` output is not semantic duplication because the recipe IDs encode distinct enchantment rituals.

Exact bytecode closes the provider control seam: `InfusionRitual` queries `InfusionRecipe.TYPE`, an accepted recipe supplies the ritual duration, completion assembles that exact recipe, and the provider settles the result back to the Infusion Pedestal.

Therefore the 48 packaged IDs are 48 distinct provider ritual identities rather than ordinary crafting aliases.

## Exact Eternal Ritual inventory

The audit disassembles `EternalRitual`, `EternalPedestal`, `EternalPedestalEntity`, `EndPortals`, the Eternal Portal structure surface and provider ritual synchronization.

Exact facts:

- Eternal Pedestal accepts provider-configured portal-key items;
- pedestal activation invokes or links one `EternalRitual`;
- `EternalRitual.checkStructure(Player)` validates the frame/pedestal arrangement;
- all ritual pedestals must resolve the same accepted item;
- `activatePortal(Player, Item)` resolves a portal ID from that item and performs provider-owned portal activation/generation;
- ritual linkage/state is persisted and synchronized provider-side.

`EndPortals.loadPortals()` reads `config/betterend/portals.json`. Missing, invalid-top-level or empty configuration regenerates a non-empty default. The exact default is one Overworld entry keyed by `betterend:eternal_crystal`.

Multiple configured portal entries parameterize the same Eternal Ritual mechanism and therefore do not create multiple semantic identities.

## Reachability evidence

The exact JAR contains:

- `data/betterend/structure/portal/eternal_portal.nbt`;
- BetterEnd Eternal Portal worldgen resources;
- Infusion Pedestal recipe/loot resources;
- `betterend:eternal_crystal` as an exact `betterend:infusion` recipe;
- guide/advancement resources for the Infusion lifecycle.

These close catalog-level provider reachability. Exact deployed portal destination/key configuration remains runtime/config QA.

## Semantic disposition

- 48 packaged Infusion Ritual recipes: **48 `COUNTED_EXACT`**;
- Eternal Portal Ritual: **1 `COUNTED_EXACT`**;
- ordinary recipes/processes, passive effects, worldgen and portal aftermath: **EXCLUDED**.

Total BetterEnd semantic surface: **49**.

## Clean-room boundary

The durable catalog retains identifiers, hashes, counts, recipe IDs/result IDs and concise factual control-flow classifications required for cataloging/deduplication. It does not redistribute the JAR, source implementation bodies, assets or localization prose.
