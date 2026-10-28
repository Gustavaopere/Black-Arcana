# ExilirSellTrade — elixires lesser/greater

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Flags e seleção

Nome binário preservado: **`ExilirSellTrade`**. Construtor `(boolean onlyLesser, boolean onlyGreater)`; a lambda captura em ordem `onlyGreater`, `onlyLesser` (nomes de parâmetros conferidos na LocalVariableTable). Greater é selecionado se `onlyGreater=true` ou, quando `onlyLesser=false`, um `nextBoolean()` for true. Se ambos forem true, onlyGreater prevalece.

| Grupo | Referências exatas de `ItemRegistry` do host | Chance por item dentro do grupo | Custo Demon Horn | Usos | XP | Mult. |
|---|---|---:|---|---:|---:|---:|
| lesser | `EVASION_ELIXIR`, `OAKSKIN_ELIXIR`, `INVISIBILITY_ELIXIR` | 1/3 | U{2,3} | 3 | 1 | 0,05 |
| greater | `GREATER_EVASION_ELIXIR`, `GREATER_OAKSKIN_ELIXIR`, `GREATER_INVISIBILITY_ELIXIR`, `GREATER_HEALING_POTION` | 1/4 | U{3,4} | 3 | 1 | 0,05 |

Entrega uma unidade. O merchant chama `(false,false)`: **1/2 lesser, 1/2 greater**, depois seleção uniforme dentro do grupo; as sete opções não têm peso igual. Esta fábrica disputa a categoria potion/elixir **1/2** antes da seleção dos grupos. Efeito real do produto é do host.

## Evidência reproduzível

`ExilirSellTrade.<init>` PC 0–11 e LocalVariableTable: ordem das flags. `lambda$new$0` PC 0–71: pools, 73–151: decisão/seleção, 153–217: custo/offer. `HornMerchantEntity.updateTrades` PC 85–144: flags false/false e categoria.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
