# Provider Catalog — organização canônica

Esta pasta é o inventário integral das capacidades mágicas do modpack.

## Regra principal

Cada mod/provider possui sua própria pasta:

`providers/<provider>/`

Dentro dela, a organização usa a **classificação nativa mais útil e comprovada daquele provider**. Não forçamos uma taxonomia única para todos os mods.

### Iron's Spells e addons baseados em escolas

Usam escola como primeira subpasta:

`providers/<provider>/<school>/<spell>.md`

Exemplos:

- `irons-spells/blood/acupuncture.md`
- `irons-spells/holy/sunbeam.md`
- `asterism-arcanum/astral/<spell>.md`
- `dreamless-spells/empty/<spell>.md`

### Ars Nouveau e addons de spellcraft modular

Usam a função do spell part:

`providers/<provider>/glyphs/forms/`
`providers/<provider>/glyphs/effects/`
`providers/<provider>/glyphs/augments/`
`providers/<provider>/rituals/`
`providers/<provider>/systems/`

Cada glyph/ritual primitivo recebe seu próprio `.md`; combinações arbitrárias criadas pelo jogador não são enumeradas como spells fixos.

### Providers ritualísticos/ocultistas

Usam as categorias reais do próprio mod. Exemplos previstos conforme auditoria:

- Goety: Focuses / rituals / brews / servants / systems;
- Malum: Spirit Rites / Geas-Pacts / spirit systems;
- Hexalia: brews / rituals / infusions;
- Toxony: harmful effects / oils / mutagens.

Subpastas só são criadas quando a categoria é comprovada no provider atual. Não inventamos classes apenas para preencher diretórios.

## Regra de proveniência

A primeira dimensão da árvore é sempre o **provider de origem**. Um addon que registra um spell Holy continua em sua pasta de addon e não é movido para `irons-spells/holy/`.

Isso permite auditar simultaneamente:

1. quem fornece a capacidade;
2. qual escola/categoria ela usa;
3. se outro mod já ocupa o mesmo nicho;
4. se o Black Arcana deve integrar, adaptar ou não criar nada novo.

## Regra de cobertura

Conteúdo que já existe e não sofrerá alteração também entra no catálogo. `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA` é um estado válido e obrigatório.

Campos ainda não comprovados permanecem `NÃO VERIFICADO`.
