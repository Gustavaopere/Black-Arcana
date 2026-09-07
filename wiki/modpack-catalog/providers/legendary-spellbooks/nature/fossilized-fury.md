# Fossilized Fury

- ID: `legendary_spellbooks:fossilized_fury`
- School: Nature
- Levels: 1–6
- Min rarity: Epic
- Cooldown: 180 s
- Cast-time field: 80 ticks
- Mana neutral: 100 / 135 / 170 / 205 / 240 / 275
- Spell power neutral: 4 / 5 / 6 / 7 / 8 / 9
- Summoned Skeloraptors: 1 / 2 / 3 / 4 / 5 / 6 — **count = spellLevel no source 0.3.2**
- Summoned HP: 25 / 30 / 35 / 40 / 45 / 50 from `20 + 5 × spellLevel`
- Summoned damage seed: provider uses spell power
- Summon lifetime: 10 minutes provider-native
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Invoca `SummonedSkeloraptorEntity` e registra cada entidade no `BaseSummonSpell`/Iron's `SummonManager`. A quantidade é controlada pelo spell level na implementação auditada.

## Acquisition

Pool do Skeletosaurus: níveis 1–6, weight 10.

## QA obrigatório

A descrição/guide text do provider afirma que maior spell power aumenta o número de raptors, mas `FossilizedFurySpell` itera `for (i < spellLevel)`. O código do pin é a authority estática; validar se a build instalada mantém essa semântica e corrigir apenas no provider/upstream se desejado.

## Regra para o Black Arcana

Não reinterpretar spell power como summon count em bridge própria, não criar segundo summon lifecycle e não conceder progressão contínua pela permanência dos raptors.

## Source

`FossilizedFurySpell.java`, `BaseSummonSpell.java`, `SummonedSkeloraptorEntity.java` @ source pin 0.3.2.
