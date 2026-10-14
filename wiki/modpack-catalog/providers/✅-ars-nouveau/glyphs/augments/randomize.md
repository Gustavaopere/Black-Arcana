# Randomize

- Registry ID: `ars_nouveau:glyph_randomize`
- Source class: `AugmentRandomize`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **1**
- Default mana: **0**

## Source-pinned behavior

Marks Ars Nouveau spell stats as randomized. Compatible glyphs define the resulting behavior. The exact provider description specifically identifies block-selection randomization for glyphs such as Place Block and Exchange, using blocks available through the provider's spell context/hotbar behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:pink_carpet` ×2.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns the randomization algorithm and compatible-glyph interpretation. Black Arcana randomness must remain server-owned, deterministic where required for replay/tests, and bounded independently.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentRandomize.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentRandomize.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** overload de `applyModifiers(builder,part,hit,world,shooter,context)` retorna `builder.randomize()`; default mana 0, tier I. A classe não implementa um RNG global nem retorna um valor de chance.
- **Consumidores comprovados:** `EffectBreak` usa `world.random.nextFloat() < count(Randomize)*0.25F` para **pular** alguns candidatos; `EffectPlaceBlock` usa `InventoryManager.extractRandomItem` em vez de `extractItem`. Ambas são semânticas diferentes.
- **Perks:** exigir RNG server-side, limites e previsão clara da semântica por receptor; nenhum hook de alterar semente/roll externo foi verificado.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
