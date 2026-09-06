# Arcane Shackle — Iron's Spells 'n Spellbooks

## Estado

`PROVIDER-NATIVE / SOURCE AUDITADO`

## Identidade

- **ID:** `irons_spellbooks:arcane_shackle`
- **Escola:** Ender
- **Raridade mínima:** Rare
- **Max level:** 8
- **Função:** restraint / containment projectile

## Custo e casting

- **Mana base:** 40
- **Mana por nível:** +8
- **Cooldown:** 45 s
- **Cast time base:** 10 ticks
- **Cast type:** Long

## Efeito

Cria `ArcaneShackleProjectile`, configurado com:

- chain HP: `15 * entityPowerMultiplier`;
- chain lifetime: `100 + spellPower * 20` ticks;
- lash radius: 5 blocos;
- restraint strength: 0.015.

O projétil é lançado na direção do caster e passa a representar a corrente/controle do provider.

## Deduplicação

Bloqueia um novo spell cuja única função seja “prender alvo com corrente mágica”.

`Prisão Poliédrica` de Ordem só permanece como candidato se o volume/lei de contenção, condições de escape, proteção/PvP e interação com teleporte/cast forem realmente distintos desta corrente.

Bindings espirituais/demoníacos de Witchcraft/Binding também não devem copiar Arcane Shackle; precisam vincular identidade/entidade/recurso ou recipiente persistente, não apenas aplicar restraint.

## Fonte técnica

`ArcaneShackleSpell.java`, Iron's branch 1.21 / 3.16.3.
