# Spirit Sight

## Estado

`IMPLEMENTADO / AUTOMAÇÃO VERDE / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Souls & Death
- **Função:** percepção/diagnóstico espiritual

## Descrição

Abre uma sessão bounded de percepção de traces espirituais fornecidos por providers autorizados, com filtros de privacidade, distância e categoria.

## Mecânica

- policy whitelist/fail-closed;
- provider IDs, dimensões, coordenadas e raio são validados;
- radius/category/privacy filtering;
- expiry da sessão;
- desaparecimento/falha do provider fecha a funcionalidade dependente;
- traces privados não autorizam disclosure de jogador oculto ou container privado.

## Malum

O provider atual reconhece apenas IDs de entidade/registry suportados e trata `malum:soul_tag_entity` como privado quando o host carrega identidade de alvo.

## Dano/custo/cooldown

- **Dano:** N/A.
- **Custo/cooldown/duração de gameplay:** `TBD — reconciliar host/config e Stage 08`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Segurança

Read-only em relação ao recurso espiritual: percepção não deve criar, consumir ou duplicar spirits por simplesmente visualizar traces.
