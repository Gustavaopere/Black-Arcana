# RandomCurioTrade — loot de acessórios do host

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Seleção e fronteira de loot

Executa somente no servidor. Consulta o loot table **`irons_spellbooks:magic_items/basic_curios`** nos registros recarregáveis do servidor, cria contexto **EMPTY** e pega **a primeira stack** da lista retornada por `getRandomItems`. Se a lista estiver vazia ou o lado for cliente, retorna **null**. O pool, os pesos, componentes e quantidades da stack são do loot table do host/data packs; esta fábrica não escolhe uniformemente um catálogo fixo de acessórios.

Cobra **U{18,…,23} Demon Horns**, entrega a primeira stack tal como produzida pelo loot, limite **1** uso, XP **15**, priceMultiplier **0,5** (não 0,05). Sem segundo custo. Disputa um slot com arma/rune/high ink: categoria **1/4**. Não há retry para substituir uma oferta null nesse slot.

## Evidência reproduzível

`RandomCurioTrade.lambda$new$0` PC 0–61: lado/loot/contexto; 63–80: vazio/primeiro; 82–128: custo/offer/null. `HornMerchantEntity.updateTrades` PC 238–331: seleção de categoria e aceitação somente se não-null.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
