# Equilibrium Rite

## Estado

`IMPLEMENTADO / AUTOMAÇÃO VERDE / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Blood & Curses
- **Função:** transferência vital / suporte hemático

## Descrição

Transfere vida entre duas entidades vivas carregadas, respeitando limites do doador, vida faltante do receptor, tamanho solicitado e teto global de segurança.

## Targeting

- fonte e alvo devem ser entidades vivas carregadas;
- admissão do alvo é revalidada imediatamente antes da mutação;
- regras específicas de PvP/bosses dependem da policy canônica do runtime.

## Quantidades

- **Transferência solicitada:** variável, dentro do contrato.
- **Transferência efetiva:** limitada por vida disponível acima do piso seguro da fonte, vida faltante do alvo, request e hard ceiling global.
- **Valor final de gameplay:** `TBD — Stage 08` quando não fixado por configuração/runtime.

## Dano/cura

Não cria vida: o valor curado no receptor deriva da transferência efetivamente debitada/autorizada da fonte segundo o settlement canônico.

## Cooldown / cast time

`TBD — Stage 08 / host final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Segurança

- sem geração gratuita de HP;
- revalidação antes do commit;
- proteção contra over-transfer;
- nenhum segundo pipeline de healing.

## Relação com Arcana Hemática futura

É um candidato natural para consumir sangue/vida via nova economia hemática, mas o runtime atual não deve ser descrito como se já dependesse do reservatório em mB.
