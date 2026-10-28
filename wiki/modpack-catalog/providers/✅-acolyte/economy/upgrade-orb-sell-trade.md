# UpgradeOrbSellTrade — upgrade orbs por Dark Horn

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Pool e custo

Seleção uniforme entre **12** referências do `ItemRegistry` de Iron's: `UPGRADE_ORB`, `FIRE_UPGRADE_ORB`, `ICE_UPGRADE_ORB`, `LIGHTNING_UPGRADE_ORB`, `HOLY_UPGRADE_ORB`, `ENDER_UPGRADE_ORB`, `BLOOD_UPGRADE_ORB`, `EVOCATION_UPGRADE_ORB`, `COOLDOWN_UPGRADE_ORB`, `PROTECTION_UPGRADE_ORB`, `MANA_UPGRADE_ORB`, `NATURE_UPGRADE_ORB`. A lista aqui é conjunto de identidades de campo, sem prometer semântica do item por nome.

Entrega **1** unidade por **U{3,4} Dark Horns**, limite **2** usos, XP **10**, priceMultiplier **0,05**. Cada orb tem chance **1/12** dentro da categoria; a categoria disputa um slot uniforme com minério (**1/2**), logo **1/24** por referência em uma geração de merchant.

## Evidência reproduzível

`UpgradeOrbSellTrade.lambda$new$0` PC 0–180: pool e seleção; 181–229: preço, moeda e oferta. `HornMerchantEntity.updateTrades` PC 332–410: slot de categoria.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
