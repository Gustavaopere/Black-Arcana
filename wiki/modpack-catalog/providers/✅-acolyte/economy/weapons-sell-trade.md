# WeaponsSellTrade — armas e spellbooks do host

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Pool e preço

Seleção uniforme entre **11** entradas (**1/11** dentro da categoria), sem encantamento ou preenchimento de spell customizado neste método. Todas entregam **1** unidade, limite **1** uso, XP **10**, priceMultiplier **0,05**. O record interno `MiscEntry` armazena item/count/cost/maxUses. Todas as referências são de Iron's `ItemRegistry`.

| Referência de produto | Custo Demon Horn |
|---|---:|
| `ItemRegistry.MAGEHUNTER` | 16 |
| `ItemRegistry.SPELLBREAKER` | 25 |
| `ItemRegistry.AMETHYST_RAPIER` | 23 |
| `ItemRegistry.ICE_STAFF` | 20 |
| `ItemRegistry.LIGHTNING_ROD_STAFF` | 23 |
| `ItemRegistry.ARTIFICER_STAFF` | 18 |
| `ItemRegistry.GRAYBEARD_STAFF` | 15 |
| `ItemRegistry.ROTTEN_SPELL_BOOK` | 22 |
| `ItemRegistry.GOLD_SPELL_BOOK` | 15 |
| `ItemRegistry.IRON_SPELL_BOOK` | 11 |
| `ItemRegistry.COPPER_SPELL_BOOK` | 8 |

A categoria disputa um slot com curio/rune/high ink: chance **1/4**, então **1/44** por entrada em uma geração normal de merchant. Ser um spellbook/staff não transfere ownership da magia para Acolyte; as propriedades e os usos dos produtos pertencem ao host.

## Evidência reproduzível

`WeaponsSellTrade.lambda$new$0` PC 0–266: 11 entradas, 267–288: escolha uniforme, 289–339: oferta. `WeaponsSellTrade$MiscEntry.<init>` PC 0–25: campos. `HornMerchantEntity.updateTrades` PC 238–331: slot de categoria.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
