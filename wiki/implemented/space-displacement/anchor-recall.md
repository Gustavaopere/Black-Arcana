# Anchor Recall

## Estado

`CANÔNICO EM main / IMPLEMENTADO / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Space & Displacement
- **Função:** recall espacial de projétil

## Descrição

Permite recall owner-attributed de um projétil para um contexto de âncora previamente capturado, sujeito a idade, alcance e segurança do destino.

## Regras confirmadas

- identidade de projétil e owner explícitas;
- mesma dimensão permitida e carregada por padrão;
- idade e alcance bounded;
- destino revalidado no settlement;
- cleanup em logout/server stop;
- sem recall cross-dimensional inferido;
- sem force-load.

## Hard ceilings

- **Idade máxima absoluta do projétil:** `600 ticks`.
- **Distância máxima absoluta:** `128 blocos`.

São tetos técnicos, não valores finais obrigatórios de Stage 08.

## Custo / cooldown / cast time

`TBD — Stage 08 / host final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Dano

N/A diretamente; o projétil preserva sua própria autoridade de dano.
