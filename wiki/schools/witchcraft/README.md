# Bruxaria Integrada

## Estado

`CONCEITO / PESQUISA — PLANO DE INTEGRAÇÃO`

## Objetivo

Dar valor real à bruxaria como um caminho de preparação, conhecimento, ingredientes, rituais e consequências — não apenas uma coleção de poções vanilla com nomes novos.

A base preferencial é **Hexalia**, porque já fornece witchery, plantas, Salt, Ritual Table, Hex Focus, Small Cauldron, brewing, enchanted plants, Mutavis/Morphora, elemental nodes, idols e ferramentas temáticas. Black Arcana deve integrar providers ao redor dessa base em vez de substituí-la.

## Providers e papéis

### Hexalia — núcleo de bruxaria

Provider-native para:

- coleta/refino de ervas;
- Mortar & Pestle;
- Athame;
- Ritual Table/Brazier;
- Nature's Rituals;
- Celestial Infusion;
- elemental nodes;
- Mutavis/Morphora;
- Small Cauldron e brews;
- Foul/Purifying/Frost/Searing-style delivery quando presente;
- idols de purificação/clima;
- enchanted plants e efeitos próprios.

Essas features devem ser catalogadas como mecânicas do Hexalia, não recriadas como spells Black Arcana.

### Toxony — toxicologia, mutagênicos e óleos

Toxony é extremamente útil, mas como braço de **alquimia ofensiva e mutação**, não como substituto do Hexalia.

Provider-native para:

- Toxicity;
- mutagens e buffs semipermanentes;
- oils para armas/uso ofensivo;
- plantas/materiais de laboratório;
- monster-hunting chemistry;
- compat com Vampirism;
- mutagens que alteram School Spell Power do Iron's.

Black Arcana não deve copiar a barra de Toxicity nem fabricar mutagens equivalentes. Bruxaria pode usar receipts/hooks desses efeitos se a API provar o resultado causal.

### Eidolon

Provider preferencial para alquimia ocultista, símbolos, altares, braseiros, teurgia/necromancia e ritos persistentes quando a receita pedir esse tipo de liturgia.

### Malum

Provider de spirits/runes/Spirit Rites. Spirits só entram em bruxaria como ingrediente real quando forem consumidos/validados pela API/provider; não transformar genericamente qualquer kill em 'spirit essence'.

### Goety

Soul Energy, brewing, rituais e summons continuam provider-owned. Integração deve compor efeitos sem duplicar Soul Energy ou necromancia.

### Vampirism/Bloodlines

Sangue real pode ser ingrediente hemático quando a bridge tiver semântica e ownership seguros. Bruxaria não deve transformar a barra de sangue do Vampirism em mana universal.

### Ars Nouveau / Iron's

Podem fornecer efeitos mágicos a serem incorporados a preparações somente por integração verificável. A poção não deve 'fingir' que lançou um spell se nenhum hook causal existir.

### HerbalBrews e culinária

HerbalBrews já cobre gathering → drying → brewing de chá/café. Deve permanecer como sistema culinário/consumível; ingredientes podem ter compat de receita, mas a Bruxaria não deve absorver todo chá como poção mágica.

## Loop principal

`PREPARAR → INFUNDIR → ESTABILIZAR → ESCOLHER DELIVERY → PAGAR CONSEQUÊNCIA`

### 1. Preparar

Coletar/cultivar plantas, minerais, sangue, spirits, toxinas e catalisadores provider-native.

### 2. Infundir

Combinar no equipamento correto. O recipiente não precisa aceitar qualquer item arbitrário: receitas são data-driven e allowlisted.

### 3. Estabilizar

Misturas poderosas exigem temperatura, ordem de ingredientes, stirring, ritual, lua/tempo, node elemental, catalyst ou outro gate. Receita inválida pode produzir mistura estragada/provider-native em vez de efeito aleatório infinito.

### 4. Delivery

Possíveis formas, somente quando houver suporte real:

- beber;
- splash/cloud;
- sac/frasco arremessável;
- oil em arma;
- incense/fumaça;
- idol/totem;
- ward/ritual de área;
- cursed object;
- coating de projétil;
- alimento/infusão específica.

### 5. Consequência

Potência vem com custo: Toxicity, materiais raros, consumo de blood/spirit, duração de preparo, corrupção, risco ritual ou cooldown de infraestrutura. Não usar todas as consequências ao mesmo tempo; cada receita declara a sua.

## Sistema de efeitos compostos

O objetivo não é criar `Black Arcana Poison II`. A receita deve referenciar um efeito/provider real.

Exemplo conceitual:

`Hexalia brew base + Toxony oil component + Malum spirit catalyst`

pode produzir uma preparação nova **somente** se o resultado tiver uma mecânica combinada que não exista isoladamente. Cada componente mantém provenance e consumo próprios.

## Tags semânticas

Criar uma camada data-driven para ingredientes, não conversões universais:

- `witchcraft/herb`;
- `witchcraft/catalyst`;
- `witchcraft/hematic`;
- `witchcraft/toxin`;
- `witchcraft/mutagen`;
- `witchcraft/spirit`;
- `witchcraft/holy_reagent`;
- `witchcraft/infernal_reagent`;
- `witchcraft/astral_reagent`;
- `witchcraft/ritual_focus`.

A tag diz que um item pode participar de receitas aprovadas; não autoriza consumo de capabilities/provider state sem adapter.

## Progressão proposta

1. Herbologia e ferramentas básicas Hexalia.
2. Brewing e sacs.
3. Elemental nodes/rituais.
4. Alquimia composta com Toxony/Eidolon.
5. Infusões de blood/spirit/holy/infernal com gates reais.
6. Maldições, wards e preparações de alto risco.
7. Grand Rituals/Grand Brews com infraestrutura e receitas únicas.

## VFX e apresentação

Caldeirões precisam mostrar cor, vapor e intensidade conforme estado da receita. Ingredientes podem gerar motes/sigils específicos por provider. Falha deve ser visualmente legível. Cloud/splash precisa manter cor e partículas distinguíveis por escola/efeito.

## Segurança e anti-abuso

- receitas allowlisted/data-driven;
- nenhuma combinação arbitrária de dois effects para gerar exponencialmente milhões de estados;
- caps de duração/amplifier;
- PvP e boss policies;
- sem duplicação de item/capability ao falhar;
- consumo transacional em rituais caros;
- world mutation via World Safety;
- provider ausente ou hook ambíguo = receita desabilitada/fail-closed.

## QA conhecido a revalidar

Logs históricos do pack registraram warnings de modelos ausentes em assets do Toxony 0.10.7. Como a exigência visual deste projeto é alta, qualquer conteúdo Toxony exposto por Bruxaria precisa de revalidação no cliente atual antes de ser considerado visualmente aprovado; não presumir que o warning histórico continua nem que foi resolvido.

## Catálogo necessário

Antes de desenhar receitas cross-mod em massa, extrair:

- todos os brews, sacs, idols, enchanted plants, rituals e transmutations de Hexalia;
- todos os mutagens, oils, toxins e effects de Toxony;
- alquimia/rituais relevantes de Eidolon;
- Spirit Rites/componentes de Malum;
- brewing/rituais de Goety;
- efeitos de Vampirism/Bloodlines;
- efeitos/glyphs/spells candidatos de Ars/Iron's;
- consumíveis mágicos de outros addons.

Só depois disso a matriz de combinações será aprovada.
