# Legendary Spellbooks — catálogo canônico

## Estado

- Mod ID: `legendary_spellbooks`
- JAR instalado: `legendary_spellbooks-1.21.1+neo-0.3.2.jar`
- Versão instalada: `0.3.2`
- Runtime alvo: NeoForge 1.21.1
- Provider base: Iron's Spells 'n Spellbooks
- Provider de conteúdo associado: Legendary Monsters
- Source pin: `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` (`1.21.1-NeoForge`, `mod_version=0.3.2`)
- Catálogo: **30/30 spells ativos documentados**
- Estado no Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

A modlist atual confirma o artefato `0.3.2`. O source pin acima declara a mesma versão e registra exatamente 30 spells ativos. A classe `PossessedFallingSoulBladeSpell` existe no source, porém sua linha de registro está comentada em `LSSpellRegistry`; ela é artefato não ativo e não entra no total.

## Inventário ativo por escola

### Annihilation — 9
1. [Annihilation Arrow](annihilation/annihilation-arrow.md)
2. [Annihilation Beam](annihilation/annihilation-beam.md)
3. [Annihilation Bomb](annihilation/annihilation-bomb.md)
4. [Annihilation Shockwave](annihilation/annihilation-shockwave.md)
5. [Annihilation Resonance](annihilation/annihilation-resonance.md)
6. [Annihilation Geyser](annihilation/annihilation-geyser.md)
7. [Summon Flameborn Knights](annihilation/summon-flameborn-knights.md)
8. [Release Riftwalker Predator](annihilation/release-riftwalker-predator.md)
9. [Flameborn Drift](annihilation/flameborn-drift.md)

### Blood / dual-school — 3
1. [Possessed Soul Blade](blood/possessed-soul-blade.md) — Evocation nos níveis 1–2; Blood nos níveis 3–4
2. [Hematite Trishula](blood/hematite-trishula.md)
3. [Possessed Wings](blood/possessed-wing.md)

### Evocation — 1
1. [Collapsed Kingdom's Legion](evocation/collapsed-kingdoms-legion.md)

### Fire — 3
1. [Flame Eater](fire/flame-eater.md)
2. [Flame Sector](fire/flame-sector.md)
3. [Sentinel Saturation](fire/sentinel-saturation.md)

### Ice — 2
1. [Glacier Eruption](ice/glacier-eruption.md)
2. [Glacier Ringburst](ice/glacier-ringburst.md)

### Lightning — 9
1. [Cloud Rail](lightning/cloud-rail.md)
2. [Cloud Ring](lightning/cloud-ring.md)
3. [Nimbus Array](lightning/nimbus-array.md)
4. [Triple Nimbus Array](lightning/triple-nimbus-array.md)
5. [Thunder Fanburst](lightning/thunder-fanburst.md)
6. [Tornado](lightning/tornado.md)
7. [Quad Tornado](lightning/quad-tornado.md)
8. [Energy Beam](lightning/energy-beam.md)
9. [Cumulo Charge](lightning/cumulo-charge.md)

### Nature — 3
1. [Ambush Thorns](nature/ambush-thorns.md)
2. [Overgrown Shockwave](nature/overgrown-shockwave.md)
3. [Fossilized Fury](nature/fossilized-fury.md)

## Escola Annihilation

`legendary_spellbooks:annihilation` é uma escola real do provider. Ela registra atributo próprio de spell power, resistência própria, foco/tag própria e damage type `ANNIHILATION` do Legendary Monsters. Black Arcana não deve reclassificar seus spells como Ender/Fire nem recriar um segundo pipeline de dano/resistência.

## Aquisição e progressão provider-native

`LSSpellScrollLootProvider` liga pools de scrolls a bosses específicos do Legendary Monsters: Cloud Golem, The Obliterator, Annihilation Pursuer, Frostbitten Golem, Possessed Paladin, Ancient Guardian, Lava Eater, Overgrown Colossus, Skeletosaurus e Dune Sentinel. As páginas individuais preservam os ranges/weights declarados no provider.

Dois spellbooks especiais também fazem parte da progressão:

- **Stormbound Grimoire:** drop do Cloud Golem; possui 12 slots, +200 Max Mana, afinidades Lightning dependentes do clima e força chuva existente a virar tempestade quando equipado em Curios.
- **Annihilator's Protocol:** drop garantido do The Obliterator no data provider; possui 10 slots, +200 Max Mana, +10% Annihilation Spell Power e vem pré-carregado com `Annihilation Geyser I` e `Annihilation Beam III`.

## Deltas e QA obrigatórios

O source `0.3.2` compila contra Iron's `3.16.1` e Legendary Monsters `2.1.14`; o pack atual usa Iron's `3.16.3` e Legendary Monsters `2.2.2`. O inventário/config estático do addon permanece source-pinned, mas integração runtime deve ser validada contra o par atual.

Divergências estáticas registradas:

- `Glacier Ringburst` tem `maxLevel=4`, enquanto o loot provider do Frostbitten Golem declara faixa `1–5`; o comportamento efetivo do nível 5 requer runtime QA.
- `StormboundSpellbookItem` concede +1 nível a `Thunder Fanburst` no mapa SUNNY, mas o tooltip constrói a linha como +2; runtime authority é o `AffinityData`, e a divergência visual precisa ser testada.
- o guia de `Fossilized Fury` diz que maior spell power aumenta o número de raptors, enquanto a implementação cria `spellLevel` raptors; o código é a authority do pin.
- `AnnihilationResonanceHandler` filtra a explosão usando `!attacker.isAlliedTo(target)` em vez de testar cada entidade candidata; friendly-fire/eligibility ao redor do alvo exige runtime QA.

Ver [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).
