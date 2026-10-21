# Summon Flameborn Knights

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:summon_flameborn_knights`, classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.SummonFlamebornKnightsSpell`; [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) / [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Parâmetros efetivos e Survival ⚠️, +0 raízes.

- ID: `legendary_spellbooks:summon_flameborn_knights`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–5
- Min rarity: Legendary
- Cooldown: 240 s
- Long cast field: 60 ticks
- Mana neutral: 250 / 300 / 350 / 400 / 450
- Spell power neutral: 8 / 11 / 14 / 17 / 20
- Summons: 1 Flameborn Guard + 1 Flameborn Warrior
- Guard HP: 56 / 64 / 72 / 80 / 88
- Warrior HP: 60 / 70 / 80 / 90 / 100
- Summon lifetime: 10 minutes provider-native
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Invoca duas entidades próprias e registra ambas pelo `SummonManager` do Iron's. O recast/lifecycle pertence ao provider; `BaseSummonSpell` cria o ledger de entidades e o recast de encerramento.

## Acquisition

Pool do The Obliterator: níveis 1–4, weight 18. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não criar segundo ownership timer, segundo despawn ou recompensa por tick de summon.

## Source

`SummonFlamebornKnightsSpell.java`, `BaseSummonSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast / níveis | Rarity LEGENDARY; 1–5; cooldown 240 s; castTime 60 ticks; mana 250+50×(nível−1); power neutro 8+3×(nível−1). | Alteração de mana/cooldown e school via host Iron's; não duplicar. |
| Quantidade real | getEntitiesToSummon retorna exatamente duas entidades (SummonedFlamebornGuardEntity e SummonedFlamebornWarriorEntity), independentemente de spellLevel; não são duas magias. | Fan-out per-caster sem hook ⛔. |
| Lifetime/recast | BaseSummonSpell usa 12.000 ticks de duração padrão, SummonManager.initSummon e RecastInstance com getRecastCount=2; novo spawn ocorre só quando não há recast ativo. | Provider owns recasts, cleanup, player data e entidade; Mastery não deve premiar por segundos de vida. |
| Atributos/targets | Helpers getHealth: warrior=50+10×level; guard=48+8×level. getDamage(power)=power. BaseSummonSpell chama setupAttributes em ISummonedMob; AI, hitbox, DamageSource e resultado real das entidades exigem análise downstream. | Sem patch de atributos de mobs por perk sem contract/QA. |

**Âncoras de código:** [SummonFlamebornKnightsSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/SummonFlamebornKnightsSpell.java#L26-L85) · [BaseSummonSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/api/spells/BaseSummonSpell.java#L20-L81).

**QA / fail-closed:** Medir atributos efetivos nas duas entidades, equipe, owner/kill credit, três cenários recast, timer 10min, reload e desconexão. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
