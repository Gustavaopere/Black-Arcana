# Fire's Ender Expansion — catálogo canônico

## Estado

- Mod ID: `firesenderexpansion`
- JAR instalado: `firesenderexpansion-2.4.1.jar`
- Runtime alvo: NeoForge 1.21.1
- Provider base: Iron's Spells 'n Spellbooks
- Escola dos 11 registros ativos: `irons_spellbooks:ender`
- Catálogo: **11/11 spells ativos documentados**
- Source pin: `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`

O pin foi escolhido porque o commit de 2026-05-30 é `Incremented Version` e declara `mod_version=2.4.1`, coincidindo com o JAR instalado. Commits posteriores que continuaram usando o mesmo version string não são tratados como autoridade para este catálogo.

## Registry ativo 2.4.1

1. [Arcane Slice](ender/arcane-slice.md)
2. [Aspect of the Shulker](ender/aspect-of-the-shulker.md)
3. [Hollow Crystal](ender/hollow-crystal.md)
4. [Dimensional Adaptation](ender/dimensional-adaptation.md)
5. [Obsidian Rod](ender/obsidian-rod.md)
6. [Infinite Void](ender/infinite-void.md)
7. [Dragon's Fury](ender/dragons-fury.md)
8. [Gate of Ender](ender/gate-of-ender.md)
9. [Displacement Cage](ender/displacement-cage.md)
10. [Binary Stars](ender/binary-stars.md)
11. [Scintillating Stride](ender/scintillating-stride.md)

## Contracts provider-native de maior relevância

- dano que escala inversamente com a mana atual do alvo;
- proc ofensivo por spell damage com Shulker Bullet;
- cristal carregável/recast com quebra, anti-magic e detonação tardia;
- adaptação dimensão → efeito data-driven;
- channeled anti-teleport + conversão de Ancient Debris;
- domain real com transporte dimensional, clash, sure-hit e buffs/debuffs próprios;
- melee Ender que combina spell power + weapon damage;
- chuva de armas via portais com modos normal/target/hail;
- prisão por boundary que usa o pipeline canônico de spell teleport;
- dois projectiles homing com debuffs distintos baseados em buffs;
- dash com retorno à posição/dimensão registrada.

Esses contracts pertencem ao provider. Bridges do Black Arcana não devem recriar dano, teleport, domain transport, recast lifecycle, effects, projectile eligibility ou buffs em paralelo.

## QA estático relevante

- O source 2.4.1 declara Iron's `1.21.1-3.15.6`, enquanto o pack usa `1.21.1-3.16.3`; compatibilidade prática exige runtime QA.
- `BinaryStarEntity` contém a fase de teleport/slam AoE somente como código comentado; ela não faz parte do contract ativo deste pin.
- `NovaBurnEffect` calcula `5 × buffs benéficos × amplifier`, porém a Nova Star aplica Nova Burn sem amplifier explícito (amplifier 0); o caminho estático provider-native resulta em dano 0 e precisa de runtime QA.
- `ScintillatingStrideSpell` não possui filtro provider-side explícito de self/allies no loop da explosão; a elegibilidade efetiva depende do pipeline de dano e precisa de runtime QA.
- `InfiniteVoidEffect` possui fallback para Overworld `(0,100,0)` se a posição original não estiver registrada corretamente; é uma failure mode que deve ser testada.

Ver [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).