# Sentinel Saturation

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:sentinel_saturation` / `dev.higurashi.legendary_spellbooks.common.spells.fire.SentinelSaturationSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Números/comportamentos source-pinned; execução/Survival ⚠️; +0 magias.

- ID: `legendary_spellbooks:sentinel_saturation`
- School: Fire
- Levels: 1–2
- Min rarity: Legendary
- Cooldown: 60 s
- Cast-time field: 60 ticks
- Mana neutral: 400 / 500
- Spell power neutral: 6 / 12
- Phantom/cannon count: 3 / 5 from `1 + 2 × spellLevel`
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria múltiplos `DuneSentinelPhantomEntity`/cannon phantoms ao redor do cast, cada um sob lifecycle e damage rules do provider. A spell desabilita looting no seu config.

## Acquisition

Pool do Dune Sentinel: níveis 1–2, weight 10; global loot modifier usa chance 0.5. Crafting não é desabilitado no config da spell.

## Regra para o Black Arcana

Não duplicar phantoms/cannons, seus disparos ou o processamento do mesmo hit.

## Source

`SentinelSaturationSpell.java`, `DuneSentinelPhantomEntity.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast/stats | School FIRE, nível 1–2, cooldown 60s, castTime=60, mana 400+100×(nível−1), spellPower 6+6×(nível−1). | Nenhum custo adicional local; host regula mana/cooldown. |
| Geometria/fan-out | getSpawnCount=1+2×level = **3/5** DuneSentinelPhantomEntity por cast. GeometryUtils.getLinePoints em linha lateral (sideYaw), centerPos getRelativePos(caster,-5,0,0), interval e startOffset calculados no método. | Alterar número/distância por perk ⛔, verificar helpers exatos e spawn parcial. |
| Ground/lifecycle | Para cada candidato findGround(level,spawnPos,10,10); só cria phantom se não-null, atribui caster, yaw, dano power. IA, dano e duração de DuneSentinelPhantomEntity devem ser lidos para validar hit. | Não inferir DamageSource FIRE apenas pela school; entidade pode ser híbrida. |
| Alvo/área | O cast forma uma linha à frente do caster, não um projétil de target entity ou círculo. Efeitos downstream pertencem à entidade invocada. | ⛔ mudança para AOE/retarget sem hook.  |

**Âncoras de código:** [SentinelSaturationSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/fire/SentinelSaturationSpell.java#L28-L93).

**QA / fail-closed:** Testar 3/5 phantoms, carga de chunks/solo, AI e damage type, times, PvP, replay, caster offline, anti-magic. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
