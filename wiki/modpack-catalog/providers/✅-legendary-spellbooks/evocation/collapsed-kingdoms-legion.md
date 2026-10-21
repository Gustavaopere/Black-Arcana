# Collapsed Kingdom's Legion

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:collapsed_kingdoms_legion` / `dev.higurashi.legendary_spellbooks.common.spells.evocation.CollapsedKingdomsLegionSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Números/comportamentos source-pinned; execução/Survival ⚠️; +0 magias.

- ID: `legendary_spellbooks:collapsed_kingdoms_legion`
- School: Evocation
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 120 s
- Cast-time field: 45 ticks
- Mana neutral: 180 / 220 / 260
- Spell power neutral: 8 / 12 / 16
- Summons per cast: 3
- Summoned HP: 65 / 80 / 95 each from `50 + 15 × spellLevel`
- Summoned damage seed: provider uses spell power
- Summon lifetime: 10 minutes provider-native
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Invoca uma unidade de cada tipo: Haunted Guard, Haunted Knight e Fractured Apostle. A spell registra as três entidades no lifecycle de `BaseSummonSpell`/Iron's `SummonManager`; variantes visuais de Guard/Knight dependem do nível.

## Acquisition

Pool do Possessed Paladin: níveis 1–3, weight 10.

## Regra para o Black Arcana

Não manter segundo ownership ledger, timer, despawn, damage scaling ou recompensa por permanência dos summons.

## Source

`CollapsedKingdomsLegionSpell.java`, `BaseSummonSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast/stats | School EVOCATION, níveis 1–3, cooldown 120s, castTime=45 ticks, mana 180+40×(nível−1), power 8+4×(nível−1). | Mana/school power sob Iron's. |
| Fan-out | getEntitiesToSummon retorna três fixos: SummonedHauntedGuardEntity, SummonedHauntedKnightEntity, SummonedFracturedApostleEntity, independente do nível. Não contar três casts. | Fan-out, targeting e owner mantidos pelo addon/host. |
| Setup/lifecycle | BaseSummonSpell.setupAttributes(level,power) quando ISummonedMob e SummonManager.initSummon por 12.000 ticks; RecastInstance count=2. getHealth helper=50+15×nível, dano helper igual a power. | Valores efetivos da AI e condições de spawn dependem de classes derivadas e precisam teste. |
| Comportamento condicional | settingSpawnMob customiza HauntedGuardEntity e HauntedKnightEntity quando instance-of. Revisar distinções de classe e inicialização antes de aplicar buff por família. | Sem hook de AI/target/critical damage verificado. |

**Âncoras de código:** [CollapsedKingdomsLegionSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/evocation/CollapsedKingdomsLegionSpell.java#L25-L79) · [BaseSummonSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/api/spells/BaseSummonSpell.java#L45-L81).

**QA / fail-closed:** Testar três summon variants, attrs e friendlies, outro recast, unload/death/ownership e spawn lotado. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
