# MiscSellTrade — vinte ofertas de materiais

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Pool e seleção

`MiscEntry(Item item,int count,int cost,int maxUses)` é um record de dados. As referências `ItemRegistry.*` abaixo pertencem a Iron's. Todas as ofertas usam Demon Horn como custo, XP **5**, priceMultiplier **0,05**, sem segundo custo. `createOffer` recebe uma entrada e produz uma oferta; `getOffer` isolado escolhe uma entrada uniforme (**1/20**).

O merchant não usa esse `getOffer`: copia as **20** entradas, chama `Collections.shuffle` e cria ofertas das primeiras **2**, sem reposição. Assim cada entrada tem chance de inclusão **2/20=10%** por geração, com dependência entre as duas escolhas. Não há pesos adicionais.

| Produto/referência | Quantidade | Custo Demon Horn | Max uses |
|---|---:|---:|---:|
| `minecraft:fire_charge` | 3 | 1 | 12 |
| `minecraft:amethyst_shard` | 4 | 1 | 16 |
| `minecraft:rabbit_foot` | 1 | 1 | 4 |
| `minecraft:phantom_membrane` | 1 | 2 | 6 |
| `minecraft:pufferfish` | 1 | 1 | 8 |
| `minecraft:ominous_bottle` | 1 | 4 | 2 |
| `minecraft:golden_apple` | 1 | 5 | 3 |
| `minecraft:slime_ball` | 4 | 1 | 12 |
| `minecraft:armadillo_scute` | 2 | 4 | 6 |
| `minecraft:dragon_breath` | 3 | 8 | 2 |
| `minecraft:wind_charge` | 7 | 2 | 10 |
| `minecraft:fermented_spider_eye` | 2 | 1 | 8 |
| `minecraft:skeleton_skull` | 1 | 6 | 1 |
| `minecraft:experience_bottle` | 12 | 3 | 10 |
| `minecraft:soul_lantern` | 3 | 1 | 12 |
| `ItemRegistry.ARCANE_ESSENCE` | 5 | 1 | 12 |
| `ItemRegistry.HOGSKIN` | 1 | 1 | 8 |
| `ItemRegistry.ARCANE_INGOT` | 1 | 2 | 1 |
| `minecraft:magma_cream` | 2 | 1 | 10 |
| `minecraft:ghast_tear` | 1 | 3 | 4 |

A ominous bottle desta oferta é uma stack comum; nenhum `OMINOUS_BOTTLE_AMPLIFIER=4` é escrito aqui. O componente especial pertence ao brewing com Dark Horn, uma superfície diferente.

## Evidência reproduzível

`MiscSellTrade.<clinit>` PC 0–380: 20 entradas; `MiscEntry.<init>` PC 0–25: ordem count/cost/maxUses. `getOffer` PC 0–30 e `createOffer` PC 0–49: oferta. `HornMerchantEntity.updateTrades` PC 10–58: shuffle e duas entradas sem repetição.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
