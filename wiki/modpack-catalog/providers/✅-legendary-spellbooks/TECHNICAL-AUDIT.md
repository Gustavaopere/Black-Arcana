# Legendary Spellbooks 0.3.2 — auditoria técnica

## Proveniência

- Pack: `legendary_spellbooks-1.21.1+neo-0.3.2.jar` / mod id `legendary_spellbooks` / runtime `0.3.2`.
- Source pin exato: `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.
- Branch: `1.21.1-NeoForge`.
- `gradle.properties`: `mod_version=0.3.2`, Minecraft 1.21.1, NeoForge 21.1.220.
- Dependências de desenvolvimento do pin: Iron's Spells `1.21.1-3.16.1`, Legendary Monsters CurseForge file `8241908` / 2.1.14, Curios 9.5.1.
- Pack atual: Iron's `1.21.1-3.16.3`; Legendary Monsters `legendary_monsters-2.2.2 MC 1.21.1.jar`.

Conclusão: o catálogo de registros/config do addon pode ser fechado em 30/30 no pin 0.3.2, mas a compatibilidade binária/comportamental com os dois providers atualizados continua como gate de runtime QA.

## Registry

`LSSpellRegistry` possui 30 registros ativos. `PossessedFallingSoulBladeSpell` existe no source, mas o `registerSpell(new PossessedFallingSoulBladeSpell())` está comentado; não é registro ativo.

Distribuição: Annihilation 9; Blood/dual 3; Evocation 1; Fire 3; Ice 2; Lightning 9; Nature 3.

## Authority e pipeline

- Casting, mana, cooldown, spell level, spell power, damage source e recast usam o framework do Iron's.
- A escola `legendary_spellbooks:annihilation` possui atributos e damage type próprios.
- Summons usam `SummonManager.initSummon(...)`; `BaseSummonSpell` registra 10 minutos (`20*60*10` ticks) e recast provider-native para encerramento. Black Arcana não deve manter segundo timer/ownership ledger.
- Loot de scrolls/spellbooks usa global loot modifiers do addon ligados a entidades do Legendary Monsters.
- Black Arcana deve observar/adaptar somente em boundaries comprovados; não duplicar dano, summon lifecycle, loot, afinidade, weather mutation ou efeitos.

## Fórmula de nível usada nas páginas

O framework Iron's calcula os campos neutros como:

- mana: `baseManaCost + manaCostPerLevel × (level - 1)`;
- spell power: `baseSpellPower + spellPowerPerLevel × (level - 1)` antes dos multiplicadores do caster/escola/config.

Quando o addon calcula dano por handler/entity, a página documenta a fórmula provider-native em vez de converter isso em bônus do Black Arcana.

## Loot / aprendizado

### Cloud Golem
`Cloud Rail 4–10 (w10)`, `Cloud Ring 1–4 (w10)`, `Nimbus Array 1–6 (w10)`, `Triple Nimbus Array 1–4 (w12)`, `Tornado 3–10 (w6)`, `Quad Tornado 1–4 (w11)`, `Energy Beam 1–3 (w8)`, `Thunder Fanburst 3–10 (w10)`, `Cumulo Charge 1–3 (w12)`. Também pode dropar Stormbound Grimoire (`0.5f` no modifier), Air Rune extra e Tempest Upgrade template.

### The Obliterator
`Annihilation Beam 1–3 (w10)`, `Annihilation Bomb 1–4 (w14)`, `Annihilation Shockwave 1–5 (w18)`, `Summon Flameborn Knights 1–4 (w18)`, `Annihilation Resonance 1–4 (w14)`. Também fornece Annihilator's Protocol no item loot modifier (`1.0f`).

### Outros bosses
- Annihilation Pursuer: `Release Riftwalker Predator 1–3 (w10)`, modifier chance `0.5f`.
- Frostbitten Golem: `Glacier Eruption 2–7 (w10)`, `Glacier Ringburst 1–5 (w10)`.
- Possessed Paladin: `Collapsed Kingdom's Legion 1–3`, `Possessed Soul Blade 1–3`, `Possessed Wings 1–2`, `Hematite Trishula 1–3` (todos w10).
- Ancient Guardian: `Ambush Thorns 3–10 (w10)`, chance `0.5f`.
- Lava Eater: `Flame Eater 3–6 (w10)`, `Flame Sector 1–4 (w18)`.
- Overgrown Colossus: `Overgrown Shockwave 1–4 (w10)`.
- Skeletosaurus: `Fossilized Fury 1–6 (w10)`.
- Dune Sentinel / BlastCannon: `Sentinel Saturation 1–2 (w10)`, chance `0.5f`.

`Annihilation Arrow`, `Annihilation Geyser` e `Flameborn Drift` não aparecem como SpellEntry no custom boss-scroll provider. Geyser é pré-carregado no Annihilator's Protocol; Arrow/Drift deixam crafting habilitado no config da própria spell. Não inferir outras loot tables sem evidência.

## Spellbooks especiais

### Stormbound Grimoire
- 12 slots; +200 Max Mana.
- Sunny affinity runtime: Cloud Rail +1, Cloud Ring +2, Tornado +1, Thunder Fanburst +1, Cumulo Charge +2.
- Thunder affinity runtime: Nimbus Array +1, Triple Nimbus Array +2, Energy Beam +1, Cumulo Charge +2.
- Quando chove sem trovejar e o item está ativo em Curios, o server chama `setWeatherParameters(0,6000,true,true)`.
- Lightning spell power: +15% base em tempo não-thunder; +30% em thunder.
- QA: tooltip SUNNY mostra Thunder Fanburst +2, mas `AffinityData` concede +1.

### Annihilator's Protocol
- 10 slots; +200 Max Mana; +10% Annihilation Spell Power.
- Preload: Annihilation Geyser I + Annihilation Beam III.
- `Annihilation Geyser` ainda faz gate explícito exigindo esse spellbook equipado em Curios.

## QA estático obrigatório

1. **Provider delta:** Iron's 3.16.1→3.16.3 e Legendary Monsters 2.1.14→2.2.2 precisam de smoke/runtime QA.
2. **Glacier Ringburst:** config max 4 versus loot range até 5.
3. **Stormbound tooltip:** Thunder Fanburst +2 exibido versus +1 no AffinityData SUNNY.
4. **Fossilized Fury:** guide text fala em spell power controlar quantidade; código usa `spellLevel` como count.
5. **Annihilation Resonance:** o predicado da explosão consulta `attacker.isAlliedTo(target)` para todas as entidades candidatas; testar friendly-fire e alcance real.
6. **Annihilation Beam/Geyser:** restrições de CastSource e imobilização/efeitos devem ser testadas com spellbook, scroll e command conforme o contrato.
7. **Summons:** testar ownership, friendly-fire, despawn/recast e 10-minute lifecycle contra Legendary Monsters 2.2.2.
8. **Read-only catalog:** nenhuma bridge do Black Arcana deve reproduzir weather, loot, affinity ou spell effects só para “integrar” o provider.

## Estado

`SOURCE-PINNED 0.3.2 / CATÁLOGO 30/30 COMPLETO / RUNTIME QA PENDENTE`
