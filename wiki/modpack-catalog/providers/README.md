# Provider Catalog — organização canônica

Esta pasta é o inventário integral das capacidades mágicas do modpack e é a **única árvore canônica de providers**:

`wiki/modpack-catalog/providers/`

A antiga árvore `wiki/providers/` foi consolidada aqui e não deve ser recriada.

## Status no nome da pasta

Toda pasta de provider usa um prefixo visual que representa **somente o estado de catalogação do conteúdo mágico**, não um PASS de runtime, integração ou compatibilidade física:

- `✅` **Catalogado** — conteúdo mágico inventariado/catalogado no nível de evidência aceito pelo projeto;
- `❌` **Não catalogado** — provider mágico identificado, mas sem catálogo suficiente;
- `🟡` **Em implementação** — catalogação/normalização atualmente em andamento;
- `⚠️` **Parcial / condicionado** — existe inventário relevante, mas parte depende de config, reachability, registry incompleto ou outra validação ainda aberta;
- `⛔` **Bloqueado** — não é seguro avançar sem evidência/API/hook adicional.

Formato canônico:

`providers/<status>-<provider>/`

Exemplos:

- `providers/✅-irons-spells/`
- `providers/✅-ars-nouveau/`
- `providers/⚠️-somake-spells/`
- `providers/⚠️-traveloptics/`

Um provider pode estar `✅` no catálogo e ainda ter runtime QA, integração, balanceamento ou compatibilidade fail-closed. Da mesma forma, `⚠️` não significa que o conteúdo já confirmado deva ser descartado; significa apenas que o fechamento integral ainda depende de uma condição documentada.

## Regra principal

Cada mod/provider possui sua própria pasta:

`providers/<status>-<provider>/`

Dentro dela, a organização usa a **classificação nativa mais útil e comprovada daquele provider**. Não forçamos uma taxonomia única para todos os mods.

Um mesmo `mod id` não deve possuir duas árvores paralelas. Na Phase 2N, o conteúdo duplicado de Leyline Spellbooks foi consolidado na árvore canônica `providers/✅-leyline-spellbooks/`, preservando as fichas de spells, progressão e rifts.

### Iron's Spells e addons baseados em escolas

Usam escola como primeira subpasta quando a escola/registry membership está comprovada:

`providers/<status>-<provider>/<school>/<spell>.md`

Exemplos:

- `✅-irons-spells/blood/acupuncture.md`
- `✅-irons-spells/holy/sunbeam.md`
- `⚠️-asterism-arcanum/astral/<spell>.md`
- `✅-dreamless-spells/empty/<spell>.md`

Leyline Spellbooks permanece organizado pela evidência realmente comprovada para a versão instalada; não se inventa school/registry membership por ficha quando a evidência não a suporta.

Somake Spells permanece `⚠️` enquanto a registry exata já catalogada ainda depende do config efetivamente implantado e do fechamento de reachability objeto-a-objeto. Nomes, escolas ou disponibilidade não são promovidos além da evidência atual.

### Ars Nouveau e addons de spellcraft modular

Usam a função do spell part:

`providers/<status>-<provider>/glyphs/forms/`
`providers/<status>-<provider>/glyphs/effects/`
`providers/<status>-<provider>/glyphs/augments/`
`providers/<status>-<provider>/rituals/`
`providers/<status>-<provider>/systems/`

Cada glyph/ritual primitivo recebe seu próprio `.md`; combinações arbitrárias criadas pelo jogador não são enumeradas como spells fixos.

### Providers ritualísticos/ocultistas

Usam as categorias reais do próprio mod. Exemplos conforme auditoria:

- Goety: Focuses / rituals / brews / servants / systems;
- Malum: Spirit Rites / Geas-Pacts / spirit systems;
- Hexalia: brews / rituals / infusions;
- Toxony: harmful effects / oils / mutagens.

Subpastas só são criadas quando a categoria é comprovada no provider atual. Não inventamos classes apenas para preencher diretórios.

## Auditorias técnicas

Auditorias de source/runtime que preservam detalhes adicionais ficam dentro do próprio provider em `audits/` ou em `TECHNICAL-AUDIT.md`. Elas são evidência auxiliar; a ficha individual na classificação nativa continua sendo a referência de gameplay para cada capacidade quando sua identidade atual estiver comprovada.

No Iron's, por exemplo, auditorias source 3.16.3 antigas foram preservadas sob `✅-irons-spells/audits/` em vez de manter uma segunda árvore paralela.

## Metadados globais

Inventário corrente, política de deduplicação e fila de auditoria ficam em:

`wiki/modpack-catalog/meta/`

## Regra de proveniência

A primeira dimensão da árvore é sempre o **provider de origem**. Um addon que registra um spell Holy continua em sua pasta de addon e não é movido para `✅-irons-spells/holy/`.

Isso permite auditar simultaneamente:

1. quem fornece a capacidade;
2. qual escola/categoria ela usa;
3. se outro mod já ocupa o mesmo nicho;
4. se o Black Arcana deve integrar, adaptar ou não criar nada novo.

## Regra de cobertura

Conteúdo que já existe e não sofrerá alteração também entra no catálogo. `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA` é um estado válido e obrigatório.

Campos ainda não comprovados permanecem `NÃO VERIFICADO`.