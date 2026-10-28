# FocusSellTrade — materiais de foco

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Pool e preço

`FocusSellTrade` herda `io.redspace.ironsspellbooks.player.AdditionalWanderingTrades$SimpleTrade`. Seleção uniforme entre **7** referências, **1/7** cada: host `BLOOD_VIAL`, `LIGHTNING_BOTTLE`, `DIVINE_PEARL`, `FROZEN_BONE_SHARD`; vanilla `BLAZE_ROD`, `POISONOUS_POTATO`, `ENDER_PEARL`.

Entrega **1** item por **U{1,2} Demon Horns**, limite **12** usos, XP **5**, priceMultiplier **0,05**, sem segundo custo. É um candidato sempre solicitado pelo merchant; não confundir o item de foco comercializado com uma magia de Acolyte ou um bônus aplicado ao comprador.

## Evidência reproduzível

`FocusSellTrade.lambda$new$0` PC 0–70: sete referências e seleção; 71–120: custo/output/usos/XP. `HornMerchantEntity.updateTrades` PC 59–84: consumidor. O superclass vem da assinatura da classe no publisher.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
