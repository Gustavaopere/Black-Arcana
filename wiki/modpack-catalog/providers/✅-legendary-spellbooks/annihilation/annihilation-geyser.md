# Annihilation Geyser

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, identidade estática `legendary_spellbooks:annihilation_geyser` / classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationGeyserSpell` — [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Valores/custos descritos da fonte continuam **⚠️ sem validação runtime/Survival**; +0 raízes.

- ID: `legendary_spellbooks:annihilation_geyser`
- School: `legendary_spellbooks:annihilation`
- Level: 1
- Min rarity: Legendary
- Cooldown: 60 s
- Cast: Long, 120 ticks; minimum effective field observado no provider: 60 ticks
- Mana neutral: 500
- Spell power neutral: 30
- Duration reported by spell UI: 50 ticks / 2.5 s
- Radius: 8 blocks
- Crafting: desabilitado
- CastSource: somente Spellbook
- Extra gate: exige `Annihilator's Protocol` equipado em Curios
- Looting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Durante o cast, o provider cria o poço gravitacional/pull; na resolução surge o geyser de Annihilation. A spell possui dois gates próprios: source de spellbook e presença do spellbook exclusivo em Curios.

## Acquisition

`Annihilator's Protocol` é item loot do The Obliterator e vem pré-carregado com Geyser I.

## Regra para o Black Arcana

Fail-closed se o item/gate provider-native não puder ser consultado; nunca permitir casting alternativo por bônus genérico.

## Source

`AnnihilationGeyserSpell.java`, `AnnihilatorsProtocolSpellbookItem.java` @ source pin 0.3.2.
