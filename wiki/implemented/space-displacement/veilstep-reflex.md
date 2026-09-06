# Veilstep Reflex

## Estado

`CANÔNICO EM main / IMPLEMENTADO / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Space & Displacement
- **Função:** mobilidade defensiva/reflex teleport

## Descrição

Executa um teleporte reflexo owner-scoped para uma posição segura entre candidatos bounded, consumindo estado de charge/cooldown controlado pelo servidor.

## Regras confirmadas

- bounded safe-position candidate search;
- sem force-load de destino;
- charge/cooldown server-owned;
- cleanup em logout/server stop;
- destinos protegidos, colidindo, fluid-unsafe, vehicle-unsafe ou inválidos falham fechado.

## Hard ceiling

- **Máximo de candidatos de posição segura:** `64`.

Não confundir esse teto técnico com número de usos/cargas de gameplay.

## Custo / cooldown / charges

`TBD — reconciliar runtime/config e Stage 08`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Dano

N/A.
