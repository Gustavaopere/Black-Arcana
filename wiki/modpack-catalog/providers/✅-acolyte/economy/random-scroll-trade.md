# RandomScrollTrade — scroll de magia do host

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Trigger e seleção

`RandomScrollTrade(SpellFilter)` mantém filtro, uma stack `ItemRegistry.SCROLL`, segundo custo **vazio**, maxTrades **1**, XP **5**, priceMultiplier **0,05**, qualidade padrão **[0,1]**. O overload `(SpellFilter,float minQuality,float maxQuality)` substitui somente os limites.

`getOffer(Entity, RandomSource)` chama `SpellFilter.getRandomSpell(random)`. Se o retorno for `SpellRegistry.none()`, retorna **null**. O pool final, exclusões e pesos do filtro pertencem à versão/configuração de Iron's instalada; a construção com filtro vazio de configuração não fixa uma lista de spells de Acolyte.

Para máximo de nível `M` do spell escolhido, o nível é inteiro uniforme **inclusivo** entre `1 + trunc(M × minQuality)` e `1 + trunc((M−1) × maxQuality)`. O custo-base é **3 × rarityValue(spell, nível) + U{3,4} Demon Horns**. A fábrica não normaliza/limita os parâmetros de qualidade, não cobra mana de cast e não lança a magia: usa `ISpellContainer.createScrollContainer(spell, nível, stack)` para preencher a stack do host.

O merchant cria sempre um candidato com qualidade **[0; 0,25]** e cria outro com **[0,3; 0,8]** quando `nextFloat()<0,7`. O segundo é chance **70%**, não uma segunda oferta garantida. Nulls são removidos ao final da geração. O construtor guarda uma stack reutilizada por instância; reutilizar uma fábrica em chamadas adicionais não é um hook imutável certificado.

## Evidência reproduzível

- `RandomScrollTrade.<init>(SpellFilter)` PC 0–62; overload PC 0–15: defaults e qualidade.
- `getOffer` PC 0–17: seleção/none; PC 18–64: nível/container; PC 65–132: raridade/preço/offer.
- `HornMerchantEntity.updateTrades` PC 171–237 e 411–420; bootstrap #1 → `Objects.isNull`: consumidores e limpeza.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
