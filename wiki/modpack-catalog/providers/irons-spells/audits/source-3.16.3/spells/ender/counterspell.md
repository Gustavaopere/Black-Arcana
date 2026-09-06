# Counterspell — Iron's Spells 'n Spellbooks

## Estado

`PROVIDER-NATIVE / SOURCE AUDITADO`

## Identidade

- **ID:** `irons_spellbooks:counterspell`
- **Escola:** Ender
- **Raridade mínima:** Rare
- **Max level:** 1
- **Função:** antimagic / cast cancellation / effect removal

## Custo e casting

- **Mana:** 50
- **Cooldown:** 10 s
- **Cast:** Instant
- **Raycast máximo:** 80 blocos

## Pipeline

1. raycast server/gameplay encontra alvo elegível via `Utils.validAntiMagicTarget`;
2. publica `CounterSpellEvent(caster, target)` no NeoForge Event Bus;
3. se o evento não for cancelado, aplica comportamento de antimagic conforme a interface do alvo;
4. `AntiMagicSusceptible` recebe `onAntiMagic`;
5. players têm cast atual cancelado e recasts removidos por razão `COUNTERSPELL`;
6. `IMagicEntity` tem cast cancelado;
7. em living entities, efeitos derivados de `MagicMobEffect` são removidos.

## Limites semânticos

Este spell já cobre o **counterspell genérico** do Iron's. A Arcana da Ordem não deve criar outro spell que faça a mesma sequência com outra cor.

Candidatos futuros precisam de delta, por exemplo:

- ward anti-cast por área;
- counter de categoria específica;
- `Ruptura de Fonte` que interrompa um link/resource causal específico sem limpar todos os efeitos mágicos;
- reflection/return com provenance verificável.

## Integrações

O evento público `CounterSpellEvent` é um hook potencialmente importante para Black Arcana e addons. Qualquer bridge deve respeitar cancelamento e não executar segunda liquidação em paralelo.

## Fonte técnica

`CounterspellSpell.java`, Iron's branch 1.21 / 3.16.3.
