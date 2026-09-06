# Vector Reversal

## Estado

`CANÔNICO EM main / IMPLEMENTADO / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Space & Displacement
- **Função:** controle vetorial/impulso

## Descrição

Aplica deslocamento/impulso direcional bounded a um conjunto pequeno de entidades vivas explicitamente fornecidas, após autorização individual.

## Regras confirmadas

- direção finita e não nula;
- máximo de quatro alvos distintos por aplicação;
- admission/revalidation canônica;
- multipliers semânticos para players/bosses;
- velocidade final hard-clamped;
- autorização parcial: alvo negado não invalida outros independentes já autorizados.

## Hard ceilings

- **Máximo de alvos:** `4`.
- **Velocidade resultante máxima:** `2,5 blocos/tick`.

Esses são limites absolutos de segurança.

## Custo / cooldown / cast time

`TBD — Stage 08 / host final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Dano

O runtime documentado é de deslocamento/impulso; não inventar dano adicional sem contrato explícito.
