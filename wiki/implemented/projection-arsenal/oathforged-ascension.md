# Oathforged Ascension

## Estado

`IMPLEMENTADO / CANÔNICO COMO PRIMITIVAS DE ALOCAÇÃO — PROVIDER PROGRESSION DEFERRED`

## Tipo

Não é tratado como spell de dano. É uma mecânica/progression seam do domínio Projection & Arsenal.

## Mecânica confirmada

O runtime canônico expõe primitivas determinísticas de alocação e ledger para pontos de Ascension. Ele **não** inventa uma moeda de progressão do provider nem afirma settlement de host não verificado.

## Hard ceiling

- `MAX_ASCENSION_POINTS = 20`.

Esse valor é teto técnico do ledger, não curva final de progressão.

## Obtenção

`TBD — Stage 08 / RPG Skill Tree / provider contract`.

## Efeito

Especializações futuras podem alterar profiles/comportamentos de projeção abaixo dos hard ceilings. Nenhum cliente pode atribuir pontos de forma autoritativa.

## Segurança

- ledger server-authoritative;
- pontos bounded;
- nenhuma moeda sintética se o provider não expuser causalidade;
- integração de mastery precisa preservar provenance.

## VFX/HUD

`TBD — progression UI`. Não confundir com um cast ativo.
