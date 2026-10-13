# Energy Beam

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:energy_beam`, classe `dev.higurashi.legendary_spellbooks.common.spells.lightning.EnergyBeamSpell` ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179); [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md)). Valores e mecânicas source-pinned; runtime/Survival ⚠️; +0 raízes.

- ID: `legendary_spellbooks:energy_beam`
- School: Lightning
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 45 s
- Cast-time field: 45 ticks
- Mana neutral: 400 / 450 / 500
- Spell power neutral: 25 / 30 / 35
- Beam duration: 50 / 60 / 70 ticks
- CastSource: somente Spellbook; scroll falha explicitamente
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Durante o casting o provider aplica movimento vertical ao caster e, na resolução, cria o Energy Beam com lifetime `min(40 + 10 × spellLevel,80)`. Damage/ticks/motion são provider-owned.

## Acquisition

Pool do Cloud Golem: níveis 1–3, weight 8.

## Regra para o Black Arcana

Não contornar o gate de CastSource, não criar um segundo beam tick e não reaplicar o impulso vertical.

## Source

`EnergyBeamSpell.java` @ source pin 0.3.2.
