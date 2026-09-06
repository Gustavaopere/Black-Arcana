# Construção — Reservatório Hemático

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

## Fantasia

Uma estrutura física escalável que pode tornar-se enorme. O tamanho aumenta a **capacidade potencial**, mas não cria sangue.

Exemplo: uma câmara de `70.000 mB` contendo `50 mB` continua quase vazia e o HUD mostra `50 / 70.000`.

## Requisitos de design

- validação server-authoritative da estrutura;
- capacidade derivada de blocos/volume válidos, com hard ceiling de servidor;
- conteúdo persistente separado da geometria;
- break/rebuild não duplica conteúdo;
- resize deve preservar conteúdo até a nova capacidade, com policy explícita para excesso;
- chunks não devem ser force-loaded pelo simples fato de conter sangue;
- acesso remoto exige vínculo/bridge explicitamente permitido;
- input/output de fluidos deve evitar duplo pipeline com outros mods.

## Visual

A construção deve comunicar fisicamente quanto sangue contém: tanque/câmara, fluid surface/volume, tubulação e foco ritual podem escalar visualmente. Renderização é client-side; quantidade real continua server-owned.

## Materiais/receita

`TBD — design de progressão`.

## Capacidade por bloco

`TBD — Stage 08 / performance`. Não fixar antes de testar persistência, networking e tamanho máximo aceitável.
