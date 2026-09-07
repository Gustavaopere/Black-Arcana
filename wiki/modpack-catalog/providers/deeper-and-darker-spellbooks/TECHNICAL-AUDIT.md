# Deeper and Darker: Spellbooks 1.3.3-ver.b — technical audit

## Autoridade instalada

`darkermagic-1.3.3-1.21.1-ver.b.jar` é a autoridade de versão do pack. O runtime metadata é `1.3.3-1.21.1`; `ver.b` identifica a variante do artefato e não deve ser apagado.

Publicação exata:

- CurseForge file ID `7897469`, publicada em 2026-04-09, NeoForge 1.21.1;
- Modrinth version ID `oBllvIgO`, mesma Version B;
- changelog 1.3.3: corrige os summon spells em servidor que podiam crashar após uso;
- Version B: Warden Mage Armor = 10% Eldritch Spell Power; Version A = 5%.

## Source público e limitação

O repositório oficial `RevTheSprout/Deeper-and-Darker-Spellbooks` termina em `df242888d16e580a8f76e0d937fe50d66bbed8ed` e a branch NeoForge 1.21.1 declara `mod_version=1.3.0` e Iron's `1.21.1-3.15.0`.

Por isso:

- o source pode demonstrar a arquitetura da linha 1.21.1;
- ele **não** prova o bytecode exato 1.3.3;
- fórmulas abaixo são baseline 1.3.0 e permanecem fail-closed para integração até JAR/runtime QA 1.3.3.

## Inventário 4/4

A página pública atual do projeto declara quatro summon spells. O registry 1.3.0 possui exatamente quatro registros e os changelogs 1.3.1–1.3.3 não anunciam alteração de inventário:

- `darkermagic:summoned_warden`
- `darkermagic:summoned_shattered`
- `darkermagic:summoned_sculk_centipede`
- `darkermagic:summoned_sculk_snapper`

Status: **inventário 4/4 fechado por release + continuidade pública; IDs ainda aguardam confirmação por bytecode 1.3.3**.

## Baseline lifecycle 1.3.0

As quatro classes públicas usam:

- `SchoolRegistry.ELDRITCH_RESOURCE`;
- `PlayerRecasts`;
- `SummonedEntitiesCastData`;
- `SpellSummonEvent`;
- `SummonManager.initSummon`;
- recast count 2;
- summon time 12.000 ticks (10 min).

Como a release 1.3.3 é especificamente um fix de dedicated-server dos summons, esta área é o principal delta suspeito e não deve ser considerada bytecode-estável sem extração/QA.

## Release sequence usada como controle de mudança

- 1.3.0: port NeoForge 1.21.1; quatro summon spells já compõem o projeto.
- 1.3.1: correção de armor enchantability; sem mudança de spell inventory anunciada.
- 1.3.2: correções adicionais de armor enchantability; sem mudança de spell inventory anunciada.
- 1.3.3: fix dos summon spells em servidores; sem spell novo/removido anunciado.

## Gates para Black Arcana

- Não duplicar summon lifecycle, owner ledger, recast ou despawn enquanto o JAR 1.3.3 não for decompilado/testado.
- Não assumir que constructor/finalizeSpawn/event ordering do source 1.3.0 permaneceu idêntico; o hotfix 1.3.3 pode estar exatamente nessa região.
- Não usar `requiresLearning=false` observado no baseline como regra absoluta do runtime 1.3.3 sem bytecode.
- O pack usa Iron's 3.16.3, enquanto o source baseline compila contra 3.15.0; validar API/hook compatibility.
- Version B só muda publicamente o Eldritch Spell Power do Warden Mage Armor para 10%; não extrapolar isso para fórmulas dos summons.

## Estado final

**RELEASE 1.3.3 VER B PINADA / INVENTÁRIO 4/4 / SOURCE 1.3.0 BASELINE / BYTECODE 1.3.3 E RUNTIME QA PENDENTES.**