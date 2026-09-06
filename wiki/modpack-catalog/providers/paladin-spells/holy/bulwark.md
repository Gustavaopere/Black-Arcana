# Bulwark

## Estado

`EXTERNAL PROVIDER / INSTALLED — QA REQUIRED`

## Identidade

- **ID:** `paladin_spells:bulwark`
- **Escola:** Holy (Iron's)
- **Raridade mínima:** Rare
- **Nível máximo:** 10
- **Função:** defesa / amplificação de armor
- **Cast type:** Instant
- **Cast animation:** `SELF_CAST_ANIMATION`

## Descrição provider

Pretende aumentar a armadura do caster com base no spell power. O effect é beneficial e usa coloração dourada.

## Custo e casting — source 1.21.1

- `baseManaCost = 30`
- `manaCostPerLevel = 10`
- `baseSpellPower = 15`
- `spellPowerPerLevel = 5`
- `castTime = 0`
- **Cooldown:** `45 s`

A mana efetiva final deve ser calculada pelo Iron's instalado; não reconstruir fórmula sem auditar o `AbstractSpell` correspondente.

## Efeito

O spell calcula:

`bonusPercent = getSpellPower(level, caster)`

`amplifier = round(bonusPercent * 10)`

`durationSeconds = min(5 + 15 * getSpellPower / 100, 35)`

Aplica `BULWARK_EFFECT` ao próprio caster.

## QA / possível defeito upstream

`BulwarkEffect` registra um modifier em `Attributes.ARMOR`, operação `ADD_MULTIPLIED_TOTAL`, com amount `0.0`. A auditoria não encontrou handler server-side adicional de Bulwark no conjunto de events do branch 1.21. Isso torna o aumento real de armor duvidoso até teste do JAR/config efetivamente instalado.

Estado funcional para integração: `NÃO USAR COMO AUTORIDADE DE ARMOR SEM LIVE VALIDATION`.

## Aquisição/aprendizado

`TBD — Iron's generic spell acquisition / modpack config`. O addon não fornece loot data próprio no source auditado.

## Dano

Nenhum dano direto na classe do spell.

## Targeting

Self.

## VFX

Feedback original é essencialmente spell animation/effect. Para a linguagem Divina proposta, candidato a reforço visual com halo/placas geométricas/armadura luminosa, sem alterar mecânica provider-native.

## Deduplicação

Qualquer novo spell Divino cujo único efeito seja “aumentar armor por algum tempo” deve ser tratado como sobreposição alta/exata com Bulwark e não aprovado sem delta real.
