# OreSellTrade — minério por Dark Horn

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Pool e custo

Seleção uniforme entre **3** entradas (**1/3** dentro da categoria). Entrega **1** unidade; moeda **Dark Horn**, XP **10**, priceMultiplier **0,05**, sem segundo custo.

| Referência exata | Custo Dark Horn | Max uses |
|---|---:|---:|
| `Items.NETHERITE_INGOT` | 1 | 3 |
| `ItemRegistry.MITHRIL_SCRAP` (Iron's) | 1 | 5 |
| `ItemRegistry.MITHRIL_INGOT` (Iron's) | 3 | 3 |

`OreEntry(Item,int cost,int maxUses)` não possui campo count; o output usa a stack padrão de uma unidade. A categoria disputa o slot escuro com upgrade orb, **1/2** cada; chance de cada minério por geração **1/6**. O preço não é convertido em Demon Horns.

## Evidência reproduzível

`OreSellTrade.lambda$new$0` PC 0–51: entradas, 52–73: escolha, 74–120: moeda/output/uses/XP. `OreEntry.<init>` PC 0–19: ordem cost/maxUses. `HornMerchantEntity.updateTrades` PC 332–410: slot de categoria.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
