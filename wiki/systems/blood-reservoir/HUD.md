# HUD do Reservatório Hemático

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

## Objetivo

Representar separadamente **capacidade estrutural** e **sangue atualmente armazenado**.

Exemplo:

`50 / 70.000 mB`

Visual conceitual:

`[x______________]`

O preenchimento corresponde a `stored_mB / capacity_mB`, sem normalização enganosa para uma barra "sempre cheia". Com 50 mB em 70.000 mB, a barra fica praticamente vazia.

## Regras

- não há regeneração passiva;
- o HUD deve receber snapshot server-authored;
- cliente não calcula ou concede sangue;
- capacidade e conteúdo são valores distintos;
- operações em trânsito/reservadas para um cast devem possuir estado explícito para evitar gasto duplo;
- valores devem usar formatação legível (`70.000 mB` em PT-BR) sem perder precisão interna;
- se a fonte ficar indisponível ou o vínculo quebrar, a UI deve refletir fail-closed em vez de manter recurso fantasma.

## Extensão futura

Para múltiplas fontes vinculadas, a interface pode mostrar um resumo total e, ao expandir, cada fonte individual com tipo, alcance/status e recurso disponível. Essa visualização não altera a prioridade de consumo, que permanece server-owned.
