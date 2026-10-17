# Possessed Wings

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:possessed_wing`, classe `dev.higurashi.legendary_spellbooks.common.spells.blood.PossessedWingSpell`; [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) / [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Parâmetros efetivos e Survival ⚠️, +0 raízes.

- ID: `legendary_spellbooks:possessed_wing`
- School: Blood
- Levels: 1–2
- Min rarity: Legendary
- Cooldown: 240 s
- Cast-time field: 20 ticks
- Mana neutral: 250 / 275
- Effect duration: 400 / 800 ticks = 20 / 40 s
- Effect amplifier: 0 / 1
- Movement Speed: +10% total while the effect is active
- Step Height: +0.25 while active
- Jump handler: adds `0.25 × amplifier` vertical motion; therefore +0 at level 1 and +0.25 at level 2
- Direct-hit rider: attacks by the affected living caster apply Legendary Monsters `Soul Fracture` through the provider handler
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Aplica `POSSESSED_WING_EFFECT` com nível convertido para amplifier `level-1`. `PossessedWingEffect` owns the movement/step modifiers; `PossessedWingHandler` owns the direct-damage Soul Fracture rider and jump impulse.

A localização/visual do provider representa as asas do Lost Paladin, mas o catálogo técnico não infere uma segunda mecânica de voo quando o boundary observado nestes handlers não a demonstra.

## Acquisition

Pool do Possessed Paladin: níveis 1–2, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não aplicar Soul Fracture por um segundo evento, não somar outro jump impulse e não duplicar modifiers de movimento/step height.

## Source

`PossessedWingSpell.java`, `PossessedWingEffect.java`, `PossessedWingHandler.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast / economia | Spell ID físico singular possessed_wing; níveis 1–2, cooldown 240s, castTime 20, mana base 250+25×(nível−1), school BLOOD. | Não contar display plural como outro spell ID; mana/cast Iron's. |
| Aplicação/duração | onCast cria MobEffectInstance(POSSESSED_WING_EFFECT, 20×level×20 ticks =400/800 ticks, amplifier=level−1). | A duração é 20s/40s a 20TPS, não criação de entidade Wing por esse método. |
| Atributos | PossessedWingEffect herda MagicMobEffect e adiciona MOVEMENT_SPEED +0.1 ADD_MULTIPLIED_TOTAL e STEP_HEIGHT +0.25 ADD_VALUE. | Efeito/attrs provider-owned; perks RPG não sobrepor UUID/modifier. |
| Target/dano/área | Self-buff sem hitbox, projétil ofensivo, DamageType, raycast ou hurt local. Outras capacidades de voar/wing downstream não homologadas aqui. | N/A dano e AOE; ⛔ movimento extra sem contrato. |

**Âncoras de código:** [PossessedWingSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/blood/PossessedWingSpell.java#L23-L51) · [PossessedWingEffect.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/effects/PossessedWingEffect.java#L9-L13).

**QA / fail-closed:** Verificar níveis/efeitos efetivos, stacking de velocidade com Epic Fight, respawn, fim do timer, apresentação no cliente, hot reload. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
