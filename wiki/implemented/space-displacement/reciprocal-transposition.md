# Reciprocal Transposition

## Estado

`CANÔNICO EM main / IMPLEMENTADO / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Space & Displacement
- **Função:** troca espacial transacional

## Descrição

Troca atomicamente dois endpoints de entidades carregadas elegíveis após validar consentimento, fingerprints dos endpoints, proteção e segurança dos dois destinos.

## Regras confirmadas

- endpoints distintos;
- consentimento host/server explícito;
- mesma dimensão carregada;
- fingerprints capturados e rechecados;
- ambos destinos validados/revalidados;
- throughput owner-scoped bounded;
- settlement/rollback por teleport apropriado;
- ItemEntity preserva stack existente sem clone/consumo;
- blocks/block entities não participam.

## Hard ceiling

- **Máximo absoluto:** `16 trocas/segundo`.

Teto técnico; Stage 08 pode balancear abaixo.

## Custo / cooldown / cast time

`TBD — Stage 08 / host final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Dano

N/A.
