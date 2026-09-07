# Glacier Ringburst

- ID: `legendary_spellbooks:glacier_ringburst`
- School: Ice
- Config levels: 1–4
- Min rarity: Epic
- Cooldown: 12 s
- Cast-time field: 20 ticks
- Mana neutral: 100 / 110 / 120 / 130
- Spell power neutral: 3 / 5 / 7 / 9
- Ring count: 3 / 4 / 5 / 6
- Spikes per ring: 8 / 10 / 12 / 14 from the provider's final-ring formula
- Ring radius sequence: `1.5 + ringIndex × 1.75`
- Warmup: `ringIndex × 2` ticks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria ondas concêntricas de ice spikes, com warmup crescente por anel. A spell desabilita looting e mantém toda a resolução no provider.

## Acquisition

O loot provider do Frostbitten Golem declara `Glacier Ringburst 1–5 (w10)`, apesar de a config da classe fixar `maxLevel=4`.

## QA obrigatório

A faixa de loot até nível 5 conflita estaticamente com o max level 4 da spell. Não normalizar para 4 ou 5 por suposição; o comportamento efetivo do roll/scroll precisa de runtime QA na versão instalada.

## Regra para o Black Arcana

Fail-closed para qualquer integração que dependa de um suposto nível 5 até o runtime resolver a discrepância. Não duplicar ice spikes.

## Source

`GlacierRingburstSpell.java`, `LSSpellScrollLootProvider.java` @ source pin 0.3.2.
