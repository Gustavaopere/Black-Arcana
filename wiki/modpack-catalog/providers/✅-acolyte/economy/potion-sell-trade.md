# PotionSellTrade — poção selecionada pelo registro

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Pool dinâmico e custo

`PotionSellTrade(Potion)` aceita uma poção explícita; o merchant passa **null**. Neste caso, a fábrica seleciona uniformemente entre objetos de `BuiltInRegistries.POTION` cuja lista de efeitos **não está vazia**. Não filtra benefício/dano, escola ou namespace; o denominador depende dos registros efetivos. Se não houver candidato ou a poção continuar null, usa `Potions.AWKWARD`.

Entrega **1** `minecraft:potion` com `DataComponents.POTION_CONTENTS` apontando ao holder da poção. Para o **primeiro efeito** somente, usa amplificador `a` e quociente inteiro `d = duração / 1200`; sem efeitos, ambos são zero. Custo-base: **U{3,4} + 2a + d Demon Horns**, com divisão inteira Java (truncamento em direção a zero), sem ajuste pelos demais efeitos. Limite **3** usos, XP **1**, priceMultiplier **0,05**. Duração/amplificador não são normalizados pela classe.

A categoria disputa um slot com `ExilirSellTrade(false,false)` por shuffle de duas categorias: **1/2** cada. A posição de registros e possíveis duplicatas de efeitos não são um pool fixo de produtos garantidos.

## Evidência reproduzível

`PotionSellTrade.<init>(Potion)` PC 0–10; `lambda$new$1` PC 0–80: seleção/fallback, 81–133: primeiro efeito, 133–219: componentes e oferta; `lambda$new$0` PC 0–17: filtro. `HornMerchantEntity.updateTrades` PC 85–144: caller com null.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
