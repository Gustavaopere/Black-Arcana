# Ars Nouveau — Exchange

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_exchange`
- Display name: Exchange
- School: Manipulation
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Amplify, Dampen, Pierce, AOE, Randomize

## Provider-native behavior

On entities, Exchange swaps caster and target positions, subject to teleport support/event checks. On blocks, it replaces matching target blocks with block items extracted from the Ars inventory manager while recovering the replaced block through silk-touch-like harvesting semantics. Randomize can select random eligible block items; AOE/Pierce expand the target set.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:emerald_block` + `#c:ender_pearls` ×2.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns both entity-position swapping and this inventory-backed block exchange transaction. Black Arcana should not clone a generic swap spell or double-consume/return blocks when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectExchange`).

## Dossiê de engenharia para perks — cadeia e interfaces

- **Source pin:** [`EffectExchange.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExchange.java), Ars Nouveau 5.13.1.
- **Entidades:** `onResolveEntity` rejeita `TELEPORTING_NOT_SUPPORTED` e `FakePlayer`; verifica `EventHooks.onEnderTeleport` separadamente em caster e alvo, de modo que um dos movimentos pode ser cancelado sem cancelar o outro (troca não necessariamente atômica). **Blocos:** `SpellUtil.calcAOEBlocks` com AOE/Pierce, equivalência de `origState.getBlock()`, harvest/protection, extração de `BlockItem` via `InventoryManager` (Randomize altera seleção); `attemptPlace` simula Silk Touch, quebra com `BlockUtil.breakExtraBlock`, coloca state, atualiza tags/components e diminui stack em sucesso. **Perks:** block volume exige budget e inventário consistente; sem segundo loot ou segundo teleporte.
- **Estado:** ✅ classe exata lida; ⚠️ helpers/config real e Survival pendentes; mutabilidade via RPG Skill Tree ⛔ sem interface comprovada que altere esses parâmetros. Ars conserva authority de recursos/efeitos.
