# RuneSellTrade — runas do host

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Pool e preço

Herda o `AdditionalWanderingTrades$SimpleTrade` de **Iron's**. Pool uniforme de **12** referências do `ItemRegistry` do host: `BLANK_RUNE`, `BLOOD_RUNE`, `COOLDOWN_RUNE`, `ENDER_RUNE`, `EVOCATION_RUNE`, `FIRE_RUNE`, `HOLY_RUNE`, `ICE_RUNE`, `LIGHTNING_RUNE`, `MANA_RUNE`, `NATURE_RUNE`, `PROTECTION_RUNE`.

Entrega **1** runa por **U{7,…,12} Demon Horns**, limite **3** usos, XP **5**, priceMultiplier **0,05**. Peso de cada runa **1/12** dentro da categoria. A categoria disputa o slot curio/arma/rune/high ink (**1/4**), portanto uma referência tem chance **1/48** por geração, sem afirmar o efeito final do produto.

## Evidência reproduzível

`RuneSellTrade.lambda$new$0` PC 0–180: pool e escolha; 181–231: preço/output/offer. `HornMerchantEntity.updateTrades` PC 238–331: slot. Superclass conferido na assinatura binária.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
