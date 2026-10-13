# Ars Nouveau — Intangible

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_intangible`
- Display name: Intangible
- School: Manipulation
- Default tier: 3
- Default mana cost: 30
- Compatible augments: Amplify, Dampen, Extend Time, Reduce Time (`glyph_duration_down`), Pierce, AOE
- Source default duration: 3 s
- Source default Extend Time increment: 1 s

## Provider-native behavior

Intangible replaces eligible non-air blocks with Ars `Intangible Air`, storing the original block-state id in the tile so the block can later return. Blocks with block entities, blacklisted blocks, unharvestable blocks and claim-denied positions are skipped. AOE/Pierce expand coverage; Amplify/Dampen change harvest hardness eligibility.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:phantom_membrane` ×3 + `#c:ender_pearls` ×2.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this temporary block-phasing/restoration ledger. Black Arcana must not reuse Ars' temporary-block storage as its own rollback authority or duplicate restoration. Independent Black Arcana phasing remains governed by `WorldEffectPolicy` and Black Arcana-owned persistence/compare-and-set restoration.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectIntangible`).

## Engenharia de perks — evidência de execução individual

- **Classe versionada:** [`EffectIntangible.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectIntangible.java) no Ars Nouveau 5.13.1.
- **Blocos elegíveis:** `SpellUtil.calcAOEBlocks` combina AOE/Pierce; rejeita block entity, air, `INTANGIBLE_BLACKLIST`, insuficiente harvest e `!destroyRespectsClaim`.
- **Persistência reversível:** guarda `Block.getId(state)`, muda bloco para `INTANGIBLE_AIR` e, quando `IntangibleAirTile` está presente, define `stateID=id` e `maxLength=duration*20`. `duration=(int)(GENERIC_INT.get()+EXTEND_TIME.get()*getDurationMultiplier())` em segundos, defaults 3 e 1.
- **Perks:** duração de estado de mundo e política de restauração dependem de `IntangibleAirTile`, não apenas do glyph. Não criar outra camada de air/restoration; mundo Black Arcana próprio requer WorldEffectPolicy.
- **Status:** ✅ code pin/identidade; ⚠️ downstream, config e Survival pendentes; mutação por RPG perk só pode ocorrer via [eventos reais](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e adapter validado, não por inferência temática.
