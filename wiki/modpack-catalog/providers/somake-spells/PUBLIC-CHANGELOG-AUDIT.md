# Somake Spells — auditoria pública da linha 1.0.x

Scope: releases NeoForge 1.21.1 publicadas pelo próprio projeto. Esta auditoria registra somente o que os changelogs afirmam; ausência de uma nota não é prova de permanência, remoção ou implementação interna.

## 1.0.8-fix — File ID 8417850 — 2026-07-12

Artefato instalado: `somakespells-1.0.8-1.21.1-fix.jar`.

Mudança pública:

- pequeno fix nas Elemental Charges de **Symmetry** e **Spirit**;
- o publisher especifica que elas não estavam aplicando seus buffs.

Conclusões seguras:

- Symmetry Charge e Spirit Charge pertencem à superfície 1.0.8-fix;
- o fix comprova um bug de aplicação de buffs e sua correção;
- buffs exatos, stacks, duração, resource/state model e hook continuam não verificados.

## 1.0.8 — File ID 8399369 — 2026-07-09

### Ritual system

- necklaces Soul Fire e Infernal Fire, antes sem receita, passam a integrar progressão ritual;
- ritual realizado no **Altar of Ignis** de Cataclysm cercado por pedestais;
- o próprio publisher recomenda JEI para consulta de recipe/progression.

### Itens/progressão citados

- Grimoires off-hand com progressão semelhante aos books e escolha de path Blood (`Profane`) ou Holy (`Sanctum`);
- Ignitium Staff com upgrade ritual para Soul Fire e Infernal Fire;
- Archangel's Staff — Holy;
- Withered Rose Staff — Blood, com unique spell;
- Copper Glove — no estado desta release é apenas uma craftable `sword`; integração futura mencionada pelo publisher não é comportamento atual;
- Fragmented Sword I/II/III, evoluído pela Upgrade Forge;
- Soul Fire / Infernal Fire Rune, Upgrade Orb, Rod e powder.

### Spells novos

- Ritual Flame — Fire;
- Custodia Caeli — Holy;
- Bloody Legacy — escola não explicitada no item;
- Fragmented Requiem — Blood;
- The Rose's Secret — Blood;
- Jingle Bell — `Melody/Evocation` no changelog NeoForge 1.21.1.

### Alterações

- Chain Connection movido de Evocation para Aqua;
- Fire Orbs refeito no impacto;
- spell damage passa a respeitar element spell-power attributes quando alterados por config;
- novos Fire Damage e Ice Damage usados por elemental charges e que não ignoram armor;
- Ignis Shield refeito para comportamento ofensivo-defensivo com retaliação ao ser atingido;
- UI da Upgrade Forge melhorada;
- correções envolvendo elemental charges sem Mowzie's Mobs.

### Compatibilidade

- Magic From the East deixa de ser obrigatório; se presente, seus spells seguem disponíveis para Symmetry; se ausente, a maioria deles torna-se ice-based segundo o publisher;
- Born in Chaos deixa de ser obrigatório; se presente, ritual progression alcança Infernal Fire; se ausente, termina em Soul Fire;
- Better Combat recebe compatibilidade para swords e staffs.

Estado físico do pack atual:

- Magic From the East — não localizado;
- Born in Chaos 1.7.6 — presente;
- Better Combat — não localizado.

Esses fatos permitem determinar apenas o caminho **publicamente esperado** de compatibilidade; runtime QA continua pendente.

## 1.0.7 — File ID 8003379 — 2026-04-28

- Sound Spells / Sound Attributes migrados para `Melodic` por mudança do ecossistema Tunes 'n Tomes;
- Fire Orbs recebeu rework;
- Mowzie's Mobs adicionado como dependência opcional naquele release.

Spells introduzidos:

- Guardian Connetion — Holy;
- Blessed Connetion — Holy;
- Cursed Connection — Blood;
- Chain Connection — Evocation naquele release, posteriormente Aqua em 1.0.8;
- Bloodmark — Blood;
- Water Control — Aqua;
- Firestorm Vortex — Fire.

O publisher diz que Guardian/Blessed/Cursed Connection exigiam Mowzie's Mobs para disponibilidade em 1.0.7. O pack atual contém Mowzie's Mobs 1.8.2, mas o gate interno exato 1.0.8-fix não foi auditado.

## 1.0.6 — File ID 7914098 — 2026-04-12

- novo progression system para tier books com objetivos por tier e avanço quest-style;
- nova **Upgrade Forge** para upgrade de recipes de books e outros itens futuros;
- books temporários renomeados para identidades finais;
- stats de tier books rebalanceados;
- Tier 3 books ganham affinity bonus para spells específicos.

Aqua:

- Tsunami removido;
- Tidal Grasp → Ceraunus Grasp;
- Tidal Dash → Ceraunus Dash.

Migração importante publicada: os books foram completamente refeitos e jogadores podiam perder books/spells equipados se atualizassem sem removê-los antes.

## 1.0.5 — File ID 7788053 — 2026-03-21

Weapons com crafts naquele release:

- Trumpet Axe — Sound;
- Totem Dagger — Evocation;
- Tide Piercer — Aqua;
- Sculkborn Axe — Eldritch;
- Scorn — Blood;
- Centuri — Blood;
- Radiant Judgment — Holy;
- Monolith Swrod — Geo, grafia do changelog;
- Mirrored Edge — Symmetry;
- Last Mourning — Evocation.

Weapons sem craft naquele release:

- Plague Light Saber;
- Exo Light Saber;
- FrostFlow Light Saber;
- Flare Light Saber;
- Plague Dual Saber;
- Exo Dual Saber;
- FrostFlow Dual Saber;
- Flare Dual Saber.

Configs novos incluem Missionary Rain removal, All Element Overrides e Somake Weapons/Items config.

Craftability/availability atual dessas armas não é inferida a partir de 1.0.5.

## 1.0.4 — File ID 7753287 — 2026-03-13

- balance/armor/effect/weapon configs;
- Geomancer armor from Mowzie's Mobs;
- Abyssium localization;
- Elemental Ghosts de todos os elementos, explicitamente sem natural spawn naquele release;
- charge texture swirls corrigidos;
- Summon Damage adicionado a Evocation Fortitude (`Evocation Charge`).

O estado de spawn dos Elemental Ghosts em 1.0.8-fix permanece não verificado.

## 1.0.3 — 2026-03-02

- correção de tag que fazia books falharem quando Geomancy e FamiliarsLib não estavam presentes.

Isto demonstra histórico de optional-provider hardening; não prova a implementação atual do loader gate.

## 1.0.2 — File ID 7689777 — 2026-02-28

Material público cita:

- Lightning Dagger;
- Storm Scriptures Spell Book (`Simple`);
- Aquamancer Spell Book recipe;
- ingots/plates/cores para crafts/futuro;
- vários weapon configs;
- skill descriptions;
- fixes de enchant tags.

Não há inventário completo de spells nessa nota.

## 1.0.1 — 2026-02-24

- Rock Sword, com requisito de Geomancy naquela linha;
- Hollow Sword;
- recipes/tags;
- fixes de crash quando Familiars/Geomancy não estavam presentes.

## 1.0.0 — 2026-02-13

A release pública 1.21.1 não oferece changelog suficiente para reconstruir o registry inicial. Nenhum nome é inventado para preencher esse vazio.

## Regra de promoção para o catálogo atual

Um item histórico só é marcado `CURRENT-LINE DIRECT` quando 1.0.8/1.0.8-fix o cita diretamente ou quando uma transformação explícita de 1.0.8 o referencia. Todo o restante conserva release de origem e `CURRENT REGISTRY UNVERIFIED`.

Esse critério impede que um changelog cumulativo incompleto vire falsamente um registry inventory.