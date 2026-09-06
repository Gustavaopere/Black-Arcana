# Telekinesis — Iron's Spells 'n Spellbooks

## Estado

`PROVIDER-NATIVE / SOURCE AUDITADO`

## Identidade

- **ID:** `irons_spellbooks:telekinesis`
- **Escola:** Eldritch
- **Raridade mínima:** Legendary
- **Max level:** 5
- **Função:** continuous entity manipulation

## Custo e casting

- **Mana base:** 25
- **Mana por nível:** 0
- **Cooldown:** 35 s
- **Cast type:** Continuous
- **Cast duration:** `140 + 20*(level-1)` ticks
- **Alcance:** `12 + 2*(level-1)` blocos

## Efeito

O pre-cast adquire um target server-side e grava `TelekinesisData` com distância travada. A cada janela de server cast tick, o spell calcula força para manter/mover o alvo em relação à direção/posição do caster, atualiza delta movement e aplica efeitos Airborne/Antigravity em pulsos.

## Deduplicação

A Magia do Caos **não recebe uma segunda telecinese genérica**.

`Distorção Vetorial` só permanece se operar em semântica diferente, por exemplo:

- refletir/reorientar projectile já em movimento;
- inverter vetor/impulso de um evento;
- desviar trajetória em reação curta;
- manipular múltiplos vetores com budget explícito;
- integrar Sable/Create physics via adapter sem replicar o grab contínuo do Iron's.

Se uma proposta apenas pega uma entidade e a arrasta pelo ar, usar Telekinesis nativa.

## Fonte técnica

`TelekinesisSpell.java`, Iron's branch 1.21 / 3.16.3.
