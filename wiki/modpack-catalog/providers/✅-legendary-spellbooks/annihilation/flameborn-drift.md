# Flameborn Drift

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:flameborn_drift`, classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.FlamebornDriftSpell`; [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) / [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Parâmetros efetivos e Survival ⚠️, +0 raízes.

- ID: `legendary_spellbooks:flameborn_drift`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–7
- Min rarity: Rare
- Cooldown: 8 s
- Mana neutral: 120 / 130 / 140 / 150 / 160 / 170 / 180
- Spell power neutral: 4 / 5 / 6 / 7 / 8 / 9 / 10
- Dash power formula: `2.0 + 0.1 × spellPower`
- Flameborn-dash effect: 12 ticks
- Invulnerable time assigned: 15 ticks
- Extra HP-damage field: `0.25 × spellLevel` as exposed by the spell UI/code path
- Crafting: habilitado no config
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Dash forward envolto em green fire; collision with a creature stops the dash and resolves the provider's AoE. Grounded casts add a small upward component. Spin/dash state and collision damage are provider-native.

## Acquisition

Não aparece no custom boss-scroll provider; crafting não é desabilitado.

## Regra para o Black Arcana

Não somar outro impulso, janela de invulnerabilidade ou collision AoE ao mesmo cast.

## Source

`FlamebornDriftSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast / custo | Nível 1–7; cooldown 8s, mana base 120+10 por nível, spell power 4+(nível−1); a classe auditada não atribui castTime próprio. Mecanismo de CastSource definido no host. | Não inventar tempo de cast ou tipo de dano por tooltip. |
| Direção / velocidade | Dash vector = caster.getLookAngle()×(2+0.1×getSpellPower(level,caster)); se onGround, adiciona Y+0.2. No server onCast grava ImpulseCastData e setDeltaMovement; onClientCast replica direção do ImpulseCastData. | Mecanismo de movimento sujeito a validação com claims/collision/anti-cheat e atributos RPG; mutabilidade per-user ⛔. |
| Efeitos/lifecycle | Adiciona FLAMEBORN_DASH_EFFECT por 12 ticks (amplifier=level), define invulnerableTime=15 e SpinAttackType FLAMEBORN do host. | Não inferir imunidade universal nem manipular i-frames da fonte por perk. |
| Dano/tipo | getHPDamage(level)=level×0.25f é helper para guia e efeitos downstream; o método onCast não chama hurt. Collision hit e cálculo de dano pertencem ao handler de dash, não homologado aqui. | NÃO VERIFICADO impact amount/target/area; Mastery não premiar por movimento apenas como dano. |

**Âncoras de código:** [FlamebornDriftSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/FlamebornDriftSpell.java#L27-L86).

**QA / fail-closed:** Testar parede, queda, movimento do cliente vs servidor, dano no dash/hit real, invulnerableTime, PvP/força e interplay com Epic Fight. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
