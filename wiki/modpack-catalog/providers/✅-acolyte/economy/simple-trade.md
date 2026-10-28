# SimpleTrade / SimpleSell — infraestrutura de ofertas

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Identidade e consumidores

`AdditionalWanderingHornTrades` é a classe de agrupamento, sem tabela de trades estática própria. `SimpleTrade implements VillagerTrades.ItemListing` encapsula um `BiFunction<Entity,RandomSource,MerchantOffer>` e `getOffer` retorna sua aplicação. Pode retornar null; não acrescenta filtro, preço ou validação. `of(BiFunction)` cria o wrapper. Não é um item registrável ou magia.

`SimpleSell(int maxTrades, ItemStack output, int minPrice, int maxPrice)` usa preço em Demon Horn igual a `max(1, inteiro inclusivo entre minPrice e maxPrice)`, entrega a stack fornecida, limite de usos `maxTrades`, XP **0** e priceMultiplier **0,05**. Não clona explicitamente a stack nem valida a ordem dos limites nos métodos locais. Não há caller de `new SimpleSell` no conjunto de classes provider auditado; é uma superfície presente, sem oferta do merchant comprovada por sua mera existência.

FocusSellTrade e RuneSellTrade herdam o **SimpleTrade do host Iron's**, enquanto os outros wrappers documentados nesta árvore usam o SimpleTrade de Acolyte. Não intercambiar estes owners.

## Evidência reproduzível

- `AdditionalWanderingHornTrades.<init>` PC 0–4: agrupamento.
- `SimpleTrade.<init>` PC 0–9; `of` PC 0–8; `getOffer(Entity,RandomSource)` PC 0–14: delegação.
- `SimpleSell.<init>` PC 0–14 e `lambda$new$0` PC 0–45: argumentos, preço e oferta.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
