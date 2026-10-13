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
