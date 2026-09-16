# Provider — Iron's Spells 'n Spellbooks

## Estado da auditoria

`REGISTRY COMPLETO / PÁGINAS INDIVIDUAIS PENDENTES`

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Minecraft:** `1.21.1`
- **Versão declarada no source 1.21:** `1.21.1-3.16.3`
- **Versão do pack auditada:** `3.16.3`
- **Source auditado:** branch `1.21`, head `e4056af90302d37eb1739f5ff05020b020e6e252`
- **Registry:** `io.redspace.ironsspellbooks.api.registry.SpellRegistry`

O registry base contém **111 spells registrados** nas famílias Blood, Ender, Evocation, Fire, Holy, Ice, Lightning, Nature e Eldritch/Void.

> Esta página confirma identidade/registro. Dano, custo, cooldown, cast time, aquisição e scaling ainda devem ser extraídos por spell/config antes de serem tratados como valores canônicos da Wiki.

## Blood — 10

1. Acupuncture
2. Blood Needles
3. Blood Slash
4. Blood Step
5. Devour
6. Heartstop
7. Raise Dead
8. Ray of Siphoning
9. Wither Skull
10. Sacrifice

### Impacto na Arcana Hemática

A nova economia hemática **não pode presumir que estes spells já usam sangue como recurso** só porque pertencem à escola Blood do Iron's. O provider base usa seu próprio sistema de mana/casting salvo comportamento individual comprovado. A migração para combustível hemático zero-mana, se aprovada, exige adapter/override explícito por spell ou uma política da escola nova; nunca inferência pelo nome da escola.

## Ender — 16

1. Counterspell
2. Dragon Breath
3. Evasion
4. Magic Arrow
5. Magic Missile
6. Starfall
7. Teleport
8. Summon Ender Chest
9. Recall
10. Portal
11. Echoing Strikes
12. Black Hole
13. Summon Swords
14. Shadow Slash
15. Arcane Shackle
16. Gravity Fissure

### Duplicações já bloqueadas

- `Portal` bloqueia a criação de um segundo portal genérico para Ordem/Caos. A nova escola deve reutilizar/hostear/skin ou criar uma função semanticamente diferente.
- `Teleport` e `Recall` bloqueiam teleporte simples/recall genéricos.
- `Counterspell` bloqueia um dispel/cancel genérico sem delta.
- `Arcane Shackle` bloqueia uma contenção simples por corrente/binding sem regra adicional.
- `Black Hole`/`Gravity Fissure` devem ser comparados antes de qualquer spell de gravidade/atração de Caos/Ordem.

## Evocation — 17

1. Chain Creeper
2. Fang Strike
3. Fang Ward
4. Firecracker
5. Gust
6. Invisibility
7. Lob Creeper
8. Shield
9. Spectral Hammer
10. Summon Horse
11. Summon Vex
12. Slow
13. Arrow Volley
14. Wololo
15. Throw
16. Fang Swirl
17. Scapegoat

### Duplicações já bloqueadas

- `Shield` deve ser comparado com qualquer ward/barrier de Ordem/Divina.
- `Invisibility` bloqueia invisibilidade genérica; witchcraft masking precisa mascarar **assinatura/detector específico**, não apenas repetir invisibilidade.
- `Gust`, `Throw` e outros efeitos de força devem ser comparados antes de Caos ganhar outro push/throw genérico.

## Fire — 13

1. Blaze Storm
2. Burning Dash
3. Fireball
4. Firebolt
5. Fire Breath
6. Magma Bomb
7. Wall of Fire
8. Heat Surge
9. Flaming Strike
10. Scorch
11. Flaming Barrage
12. Fire Arrow
13. Raise Hell

### Impacto na Magia Infernal

A escola Infernal não deve virar apenas `Fire` recolorido. Fireball, breath, wall, barrage, strike, dash e magma projectile já existem. O delta Infernal deve vir de:

- fonte Nether-only / Lava Infernal;
- dano/estado infernal próprio quando aprovado;
- contratos/pactos;
- vínculo com reservatório;
- efeitos que interagem com Hell/infernal entities;
- world/VFX semantics próprias;
- integração provider-native com Cataclysm/Ignis antes de criar versões novas.

## Holy — 13

1. Angel Wings
2. Blessing of Life
3. Cloud of Regeneration
4. Fortify
5. Greater Heal
6. Guiding Bolt
7. Healing Circle
8. Heal
9. Sunbeam
10. Wisp
11. Divine Smite
12. Haste
13. Cleanse

### Duplicações já bloqueadas para Divina/Celestial

- voo/asas genérico → `Angel Wings`;
- cura simples/maior/área/regen → `Heal`, `Greater Heal`, `Healing Circle`, `Cloud of Regeneration`;
- fortificação simples → `Fortify`;
- bolt/smite holy simples → `Guiding Bolt`, `Divine Smite`;
- raio solar → `Sunbeam`;
- haste genérico → `Haste`;
- cleanse genérico → `Cleanse`.

Portanto Magia Divina/Celestial deve focar **milagres, law/holy interactions, sanctum, celestial resonance, exorcism, consecration, judgment, protection ou world/context mechanics** que não sejam apenas mais cura/dano Holy.

## Ice — 12

1. Cone of Cold
2. Frost Step
3. Ice Block
4. Icicle
5. Summon Polar Bear
6. Ray of Frost
7. Frostwave
8. Ice Spikes
9. Ice Tomb
10. Snowball
11. Frostbite
12. Blizzard

## Lightning — 10

1. Ascension
2. Chain Lightning
3. Charge
4. Electrocute
5. Lightning Bolt
6. Lightning Lance
7. Shockwave
8. Thunderstorm
9. Ball Lightning
10. Volt Strike

## Nature — 13

1. Acid Orb
2. Blight
3. Poison Arrow
4. Poison Breath
5. Poison Splash
6. Root
7. Spider Aspect
8. Firefly Swarm
9. Oakskin
10. Earthquake
11. Stomp
12. Gluttony
13. Touch Dig

### Impacto em Bruxaria/Toxony

Toxony/Hexalia não devem gerar outro `Poison Arrow/Breath/Splash` só para representar veneno. Bruxaria deve diferenciar preparação, toxicidade, mutagênicos, oils, doses, antídotos, contato/ingestão/ritual e combinações cross-mod.

## Eldritch / Void — 7

1. Abyssal Shroud
2. Sculk Tentacles
3. Sonic Boom
4. Planar Sight
5. Telekinesis
6. Eldritch Blast
7. Pocket Dimension

### Duplicações já bloqueadas

- `Telekinesis` é um spell Legendary contínuo real do Iron's; Caos não deve criar telecinese genérica. `Distorção Vetorial` precisa ser **reorientação/reflexão/impulso causal** ou outra operação que o spell nativo não cobre.
- `Planar Sight` ocupa percepção planar genérica; `Olho da Convergência` precisa ser fate/probability/divination read-only com saída diferente, não outro efeito de visão planar.
- `Pocket Dimension` já cria uma dimensão pessoal provider-owned; Black Arcana Forbidden Domains deliberadamente não deve copiá-la. Ordem/Infernal/Divine não recebem pocket dimensions próprias só por estética.

## Spells prioritários para auditoria individual por risco de duplicação

1. Portal
2. Counterspell
3. Arcane Shackle
4. Teleport
5. Recall
6. Black Hole
7. Gravity Fissure
8. Shield
9. Invisibility
10. Planar Sight
11. Telekinesis
12. Pocket Dimension
13. Raise Hell
14. Angel Wings
15. Divine Smite
16. Cleanse
17. Sunbeam
18. Healing Circle
19. Sacrifice
20. Ray of Siphoning
21. Heartstop
22. Raise Dead

## Evidência técnica já extraída

### Portal

- escola Ender;
- raridade mínima `UNCOMMON`;
- nível máximo `3`;
- cooldown `180 s`;
- mana base `200`, +`10` por nível;
- cast instantâneo;
- alcance de posicionamento `48` blocos;
- dois casts/recasts para parear endpoints;
- duração deriva de spell power;
- gerenciado por `PortalManager`/`PortalData` e possui suporte a Portal Frame;
- não pode ser lançado dentro da Pocket Dimension.

A bridge Immersive Portals deve preservar este spell/provider como owner da intenção/custo/progressão e substituir/acompanhar a apresentação/travessia conforme seu contrato validado.

### Counterspell

- Ender / Rare;
- nível máximo `1`;
- cooldown `10 s`;
- mana base `50`;
- instantâneo;
- raycast de até `80` blocos;
- dispara `CounterSpellEvent` cancelável;
- chama `AntiMagicSusceptible`, cancela casts de players/magic mobs e remove `MagicMobEffect` ativos quando permitido.

Isso é um hook central para futuras integrações de Ordem. Um novo `Dissipação Ordenada` não pode simplesmente copiar o mesmo comportamento; deve possuir alvo/semântica/gate distintos ou ser apresentação/progressão sobre este contract.

### Arcane Shackle

- Ender / Rare;
- max level `8`;
- cooldown `45 s`;
- mana base `40`, +`8`/level;
- cast time base `10` ticks;
- cria projétil de corrente com HP, lifetime e raio próprios;
- lash radius `5`;
- restraint strength `0.015`.

### Planar Sight

- Eldritch / Legendary;
- max level `3`;
- cooldown `200 s`;
- mana base `150`, +`50`/level;
- instantâneo;
- aplica efeito `PLANAR_SIGHT` por duração derivada do spell power.

### Telekinesis

- Eldritch / Legendary;
- max level `5`;
- cooldown `35 s`;
- mana base `25` e sem incremento por level;
- `CONTINUOUS`, cast time base `140` ticks + `20` por level;
- alcance `12 + 2*(level-1)`;
- seleciona entidade e aplica força server-side periodicamente.

### Pocket Dimension

- Eldritch / Legendary;
- max level `1`;
- cooldown `60 s`;
- mana `300`;
- cast time fixo `40` ticks;
- proibido em combate e de dentro da própria Pocket Dimension;
- cria/usa room pessoal e teleporta `ServerPlayer` para a dimensão provider-owned.

## Próximo passo deste provider

Criar uma página individual para cada um dos 111 spells com:

- ID real;
- default config;
- raridade/max level;
- custo/cooldown/cast type;
- fórmula de damage/heal/effect;
- aquisição/crafting/loot;
- VFX/animation/sound;
- semantic signature para dedup;
- bugs/authority concerns quando encontrados.
