# Release Riftwalker Predator

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:release_riftwalker_predator`, classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.ReleaseRiftwalkerPredatorSpell`; [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) / [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Parâmetros efetivos e Survival ⚠️, +0 raízes.

- ID: `legendary_spellbooks:release_riftwalker_predator`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 500 s
- Long cast field: 100 ticks
- Mana neutral: 700 / 750 / 800
- Spell power neutral: 15 / 18 / 21
- Summon HP: 160 / 180 / 200
- Summon: 1 `SummonedAnnihilationPursuerEntity`
- Summon lifetime: 10 minutes provider-native
- Crafting: desabilitado
- Looting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Materializa um pursuer próprio do addon e o registra no lifecycle de summons do Iron's. Tracking/rift behavior continua autoridade do provider/Legendary Monsters.

## Acquisition

Pool do Annihilation Pursuer: níveis 1–3, weight 10; modifier chance 0.5.

## Regra para o Black Arcana

Não duplicar tracking, teleporte dimensional, ownership ou summon duration.

## Source

`ReleaseRiftwalkerPredatorSpell.java`, `BaseSummonSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Admissão | Níveis 1–3; cooldown 500 s; castTime 100 ticks; mana 700+50×(nível−1); spell power 15+3×(nível−1). | Gates de Iron's continuam provider-native. |
| Quantidade / posicionamento | getEntitiesToSummon retorna **uma** SummonedAnnihilationPursuerEntity para todo nível; getSpawnOffset retorna caster.getLookAngle().scale(-1) = deslocamento um bloco para trás na orientação atual. | Não deduzir alcance de ataque ou raio a partir de offset. |
| Atributos/lifecycle | Helper getHealth=140+20×nível e getDamage(power)=power; BaseSummonSpell configura ISummonedMob, initSummon 12.000 ticks e recast 2. Companheiro é provider-owned. | Sem adapter para duplicar summon, modificar HP por spawn ou cobrar segunda mana. |
| Hit / alvo | Dano real, velocidade, perseguição, factions e DamageType são propriedades da entidade/host ainda não medidas no pack. | ⚠️ downstream condicionado; ⛔ target/range modification sem seam. |

**Âncoras de código:** [ReleaseRiftwalkerPredatorSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/ReleaseRiftwalkerPredatorSpell.java#L22-L61) · [BaseSummonSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/api/spells/BaseSummonSpell.java#L20-L81).

**QA / fail-closed:** Validar colocação atrás do player, queda no vazio, números HP/ataque, owner em logout, recast, PvP, caps, persistência e despawn. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
