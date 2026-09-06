# Threshold Gate

## Estado

`CANÔNICO EM main / IMPLEMENTADO / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Space & Displacement
- **Função:** portal/transferência espacial

## Descrição

Mantém um par de thresholds server-authoritative para transferir entidades vivas elegíveis entre endpoints seguros dentro da mesma dimensão permitida e já carregada.

## Regras confirmadas

- identidade estável do par e contexto de owner;
- mesma dimensão permitida e carregada;
- sem force-loading;
- safe-destination admission e revalidação antes do settlement;
- consentimento explícito ao mover outro jogador;
- throughput bounded;
- cleanup de lifecycle;
- `ServerPlayer` usa caminho de teleport apropriado.

## Hard ceiling

- **Throughput máximo absoluto:** `32 transferências/segundo`.

Esse é um teto técnico de segurança, **não necessariamente o valor final de gameplay**. Stage 08 pode usar valor menor.

## Custo / cooldown / cast time

`TBD — Stage 08 / host final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Dano

N/A.

## Segurança

- não move blocks/block entities;
- não force-load;
- destination authority é do Black Arcana, mesmo quando outro provider hospeda o cast;
- unknown/missing protection authority falha fechado.
