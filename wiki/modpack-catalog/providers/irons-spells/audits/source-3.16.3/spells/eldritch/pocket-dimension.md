# Pocket Dimension — Iron's Spells 'n Spellbooks

## Estado

`PROVIDER-NATIVE / SOURCE AUDITADO`

## Identidade

- **ID:** `irons_spellbooks:pocket_dimension`
- **Escola:** Eldritch
- **Raridade mínima:** Legendary
- **Max level:** 1
- **Função:** personal dimension travel

## Custo e casting

- **Mana:** 300
- **Cooldown:** 60 s
- **Cast time:** 40 ticks fixos; cast-time reduction deliberadamente não se aplica
- **Cast type:** Long

## Gates

- caster precisa ser `ServerPlayer`;
- não pode ser lançado de dentro da Pocket Dimension;
- não pode ser lançado enquanto o player estiver em combate.

## Efeito

O provider:

1. cria `PortalData` com duração de 60 s;
2. garante/gera a pocket room individual via `PocketDimensionManager`;
3. localiza o Portal Frame da room;
4. registra portal de retorno;
5. aplica cooldown de portal direto;
6. remove scroll quando aplicável;
7. muda o `ServerPlayer` de dimensão por `DimensionTransition`.

## Deduplicação

Black Arcana 07.06 Forbidden Domains é deliberadamente **outra arquitetura**: campo localizado no mundo já carregado, sem dimensão temporária/pessoal. Não deve ser refeito para imitar Pocket Dimension.

Order, Chaos, Divine e Infernal não ganham pocket dimensions próprias só por fantasia visual. Qualquer espaço especial futuro deve justificar por que a dimensão nativa do provider ou um localized domain não resolve o caso.

## Immersive Portals

A existência da bridge de Portal Spell não autoriza presumir que `Pocket Dimension` também seja automaticamente convertido para Immersive Portals. Isso exige hook/version validation específico.

## Fonte técnica

`PocketDimensionSpell.java`, Iron's branch 1.21 / 3.16.3.
