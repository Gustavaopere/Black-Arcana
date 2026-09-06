# Sympathetic Wound

## Estado

`IMPLEMENTADO / AUTOMAÇÃO VERDE / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Blood & Curses
- **Função:** vínculo ofensivo / dano espelhado bounded

## Descrição

Cria uma relação de dano derivado entre entidades elegíveis. Parte do dano é propagada de forma controlada, com provenance explícita e proteção contra recursão.

## Mecânica

- damage type/marker dedicado impede recursão;
- provenance propagada é explícita;
- existem tetos por evento e por lifetime;
- player-target é negado por padrão no contrato atual;
- target admission é canônica;
- cross-link recursion é bloqueada.

## Dano

- **Percentual/valor propagado:** `TBD — reconciliar runtime / Stage 08`.
- **Hard ceilings:** existem no contrato; valores exatos devem ser extraídos do código antes de publicação final.
- derived damage não deve reentrar como dano direto comum do domínio.

## Cooldown / cast time

`TBD — Stage 08 / host final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Relação com a futura Magia Vincular

É uma evidência técnica importante para links persistentes, provenance e anti-recursion, mas não deve ser confundida com o sistema geral `CONJURADOR ⇄ VÍNCULO ⇄ FONTE` até esse sistema ser implementado.
