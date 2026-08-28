# Estado atual e fronteira de implementação

## Estágios concluídos

No checkpoint desta wiki:

- **00 Foundation** — concluído e verificado;
- **01 Reference Catalog** — concluído; 53 observáveis e 32 candidate specifications congelados como entrada de design;
- **02 Arcana Core** — concluído;
- **03 Integration Layer** — concluído;
- **04 World Safety** — concluído;
- **05 Casting & UX** — código mergeado e CI automatizado verde, porém o stage continua ativo porque a matriz manual real de cliente ainda não foi executada por completo.

Stages 06–09 não são conteúdo canônico atual.

## O que existe de fato hoje

O runtime já possui:

- ingresso server-authoritative para casts;
- proteção contra replay;
- gate de progressão;
- cooldowns persistentes e charge pools;
- resolução server-side de alvo;
- reserva/commit/refund transacional de custos;
- política de efeitos no mundo;
- scheduling limitado de trabalho;
- loadout persistente e sincronizado;
- radial client-only;
- cast do slot selecionado e quick casts;
- HUD contextual e feedback autoritativo;
- preferências client-only de apresentação;
- integrações preparadas/conectadas com Iron's Spells 'n Spellbooks, Ars Nouveau, Malum e Eidolon;
- infraestrutura de proteção de chunks, destinos, entidades e mutações temporárias.

## O que NÃO deve ser descrito como conteúdo jogável final

Os 32 candidate specifications do catálogo de referência **não equivalem a 32 feitiços disponíveis**.

O datapack atual contém somente material técnico/probe necessário às integrações, incluindo `eidolon_integration_probe.json`. O catálogo de candidatos serve como especificação para os próximos stages.

Portanto, ainda não são canônicos como catálogo jogável completo:

- Rituals (Stage 06);
- Blood, souls, projection, displacement e forbidden domains (Stage 07);
- knowledge/mastery/progression final (Stage 08);
- presets e balanceamento final;
- efeitos visuais futuros associados a `particleDensity`, `reducedMotion` e `reducedFlashes` quando não houver um efeito correspondente já implementado.

## Autoridade

A interface de cliente nunca decide o resultado do cast. Radial, HUD e seleção de slot são apresentação/intenção; toda conjuração termina no pipeline server-authoritative congelado no Arcana Core.
