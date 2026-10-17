# Legendary Spellbooks — catálogo canônico

## Engenharia de perks por spell — 17/10/2026

**Barra do provider (identidades): 30/30 = 100% ✅. Barra de fichas com engenharia causal aprofundada nesta série: 10/30 = 33,33% 🟡**, com **20 fichas restantes** no padrão source-located de targeting, geometria, hitbox, quantidade, tempo, dano, tipo e causalidade. [Matriz e backlog](PERK-CAUSAL-ENGINEERING-MATRIX-0.3.2.md) · [prova binária de 30/30](EXACT-BINARY-SPELLS-0.3.2.md).

Nesta tranche foram aprofundadas **Annihilation Resonance, Annihilation Beam, Annihilation Shockwave, Annihilation Geyser, Glacier Ringburst, Fossilized Fury, Energy Beam, Possessed Soul Blade, Flame Sector e Cumulo Charge**. O código-fonte fixo é `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; a identidade compilada 0.3.2 é SHA-exata, mas lógica dos handlers/entidades e runtime com Iron's 3.16.3 / Legendary Monsters 2.2.2 ainda exigem validação física.

**Diferenças que importam para perks:** Resonance usa AABB inflate(3) enquanto UI mostra radius(4); Shockwave mostra distância externa diferente da última onda posicionada; Soul Blade constrói até 54 lâminas e muda de escola por nível; Flame Sector consulta `FLAME_EATER_SPELL` ao construir o damage source; Cumulo Charge usa `mobAttack` e aplica STUN sem verificar sucesso do dano; Glacier Ringburst pode tentar até 84 spikes. **São findings SOURCE_CAUSALITY, não bugs físicos confirmados.** Nenhum adapter foi implementado ou homologado, nenhum spell adicional foi contado, nenhuma Stage promovida.

**Barra global: —%** porque o denominador total dos mods/objetos permanece aberto. Piso do checkpoint mais recente: **1.856 semânticos / 1.854 estritos**; números diferentes no material histórico abaixo permanecem evidência do estágio anterior e não substituem o checkpoint atual.

## Atualização binária exata — 13/10/2026

✅ [Dossiê 30/30](EXACT-BINARY-SPELLS-0.3.2.md), [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) **SUCCESS**. CurseForge `8255715`, **510127 bytes**, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5` idêntico ao JAR físico #372: **30** instâncias registradas sem branches em `LSSpellRegistry`, IDs/solo classes extraídos dos campos `ResourceLocation`, escolas compiladas inspecionadas. Confiança de identidade estática `COUNTED_EXACT`; **21/39 exatos / 18/39 pendentes**, +0 raízes, mínimo 1857/1855 inalterado. A fonte pinada abaixo permanece autoridade documental para mecânicas; gameplay, configuração, Iron's 3.16.3, Legendary Monsters 2.2.2 e Survival seguem **⚠️**.


## Estado

- Mod ID: `legendary_spellbooks`
- JAR instalado: `legendary_spellbooks-1.21.1+neo-0.3.2.jar`
- Versão instalada: `0.3.2`
- Runtime alvo: NeoForge 1.21.1
- Provider base: Iron's Spells 'n Spellbooks
- Provider de conteúdo associado: Legendary Monsters
- Source pin: `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` (`1.21.1-NeoForge`, `mod_version=0.3.2`)
- Catálogo: **30/30 spells ativos documentados e binariamente verificados (`COUNTED_EXACT` somente registro estático)**
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
