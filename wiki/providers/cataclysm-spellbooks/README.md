# Cataclysm: Spellbooks — catálogo do provider

## Estado

`EXTERNAL PROVIDER / INSTALLED 1.1.13 — PUBLIC SOURCE BASELINE 1.1.11 — CURRENT-JAR EXTRACTION REQUIRED`

## Versão instalada

- JAR: `cataclysm_spellbooks-1.1.13-1.21.jar`
- Minecraft/loader: NeoForge 1.21.1
- release pública: 02/09/2026, beta
- release notes: updated arts, more spells ported, bug fixes, new boss.

## Limitação de evidência

O repositório público oficial 1.21.1 ainda declara `mod_version=1.1.11-1.21` e seu histórico público de código não acompanha a publicação 1.1.13. Portanto:

- nomes/arquitetura da 1.1.11 são úteis como **baseline de deduplicação**;
- números da 1.1.11 NÃO são canonizados como valores da 1.1.13;
- qualquer custo/dano/cooldown final da instalação atual exige extração do JAR 1.1.13 ou runtime/config do pack.

## Escopo público atual

A página atual do mod declara **65 spells** no total e escolas novas Abyssal e Technomancy, além de spells distribuídos em escolas do Iron's.

O catálogo completo de 65 entradas será construído a partir da versão instalada, não apenas da árvore pública antiga.

## Ignis/Fire — baseline público 1.1.11

O registry público contém pelo menos estas implementações Fire ligadas à fantasia de Ignis:

1. `Incineration`
2. `Infernal Strike`
3. `Conjure Ignited Reinforcement`
4. `Hellish Blade`
5. `Bone Storm`
6. `Bone Pierce` / Blazing Bone Spit
7. `Ashen Breath`
8. `Abyss Fireball`
9. `Tectonic Tremble`

Há ainda conceitos comentados no source antigo, como Avatar of Flame, Infernal Inhalation e Scorched Earth, que NÃO devem ser tratados como spells atuais até comprovação no JAR 1.1.13.

## Aquisição dos Ignis spells — baseline

`AbstractIgnisSpell` do source público antigo:

- `allowLooting() = false`;
- `canBeCraftedBy(player)` exige `Cataclysm BURNING_ASHES` no inventário via `Ace's Spell Utils`.

Isso estabelece uma identidade provider-native forte: progressão Ignis baseada em Burning Ashes. A Wiki não deve substituir isso por uma receita Black Arcana sem motivo.

## Relação com a nova Magia Infernal

A Magia Infernal proposta deve **integrar e reaproveitar** esses spells quando cobrirem o papel pretendido. A nova Lava Infernal serve para conteúdo novo de alto nível/infrastructure, não para obrigar todos os spells Cataclysm existentes a abandonar a economia provider-native.

Exemplos de sobreposição já bloqueados:

- linha/erupção de pilares infernais → comparar primeiro com Incineration;
- projectile/incinerator + marca → Infernal Strike;
- vertical locking blade → Hellish Blade;
- radial blazing bone barrage → Bone Storm;
- single blazing bone projectile → Bone Pierce;
- cone/breath de cinzas → Ashen Breath;
- impacto sísmico vulcânico → Tectonic Tremble.

## QA baseline

A source tree 1.1.11 possui construções suspeitas/bugs claros que podem ter sido corrigidos em 1.1.13. Exemplo: `IncinerationSpell` contém `if (isSoul);` imediatamente antes de um bloco de spawn, tornando esse bloco incondicional em Java. O changelog da 1.1.13 afirma genericamente 'fixed bugs', mas não prova quais correções entraram.

Por isso nenhum número baseline vira balanceamento canônico atual.

## Próximo passo obrigatório

1. obter/extrair o JAR 1.1.13 efetivamente usado pelo pack;
2. listar os 65 spell IDs atuais;
3. extrair class/config de cada spell;
4. comparar com 1.1.11 para detectar novos/alterados/removidos;
5. individualizar todos os spells relevantes;
6. fechar matriz de colisão com Infernal, Divine, Chaos, Order e demais escolas.
