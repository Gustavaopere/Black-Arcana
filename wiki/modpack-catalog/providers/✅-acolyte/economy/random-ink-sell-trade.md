# RandomInkSellTrade — tintas em dois grupos

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Contrato e probabilidades

No construtor sem argumentos, `onlyHighRarity=false`. O overload booleano escolhe dois grupos; cada item no grupo tem peso igual **1/2**:

| Grupo | Referências exatas do host | Custo-base em Demon Horns | Usos | XP | Multiplicador |
|---|---|---|---:|---:|---:|
| normal (`false`) | `INK_UNCOMMON`, `INK_RARE` | `4 × InkItem.getRarity().getValue() + U{1,2}` | 3 | 5 | 0,05 |
| alto (`true`) | `INK_EPIC`, `INK_LEGENDARY` | `2 + 4 × rarityValue + U{1,2}` | 2 | 5 | 0,05 |

Entrega uma tinta escolhida. Os valores numéricos de raridade são do host e não devem ser convertidos em uma tabela fixa sem verificar essa versão de Iron's.

O merchant adiciona sempre um candidato normal. O grupo alto disputa um slot uniforme entre **4** categorias (curio, arma, rune, high ink): chance de categoria **1/4**, depois **1/2** por tinta. Normal e alto são fábricas separadas, sem cooldown nem conversão de uma tinta na outra.

## Evidência reproduzível

- `RandomInkSellTrade.<init>()` PC 0–5; overload `(boolean)` PC 0–10.
- `lambda$new$0` PC 0–72: grupos e seleção; 73–113: custo/usos; 115–154: output, XP e multiplicador.
- `HornMerchantEntity.updateTrades` PC 145–170 e 238–331: consumidores.

## Boundary, persistência e testes

A fábrica cria ofertas, não aplica o efeito do produto nem registra uma magia. Iron's permanece proprietário de suas magias/itens/loot; Acolyte possui a política de seleção e preço. O débito, a entrega de stack e a UI passam ao merchant vanilla. Não há hook mutador homologado, API estável prometida ou autorização técnica para duplicar rewards/consumo. Nomes/assinaturas são alvos candidatos de observação `NOT_VERIFIED`.

Os preços aqui são custos-base construídos, sem prometer o preço efetivo do menu após regras externas. Limite de usos é o `maxUses` da oferta; não é cooldown. Nenhuma fábrica implementa timer de refresh/restock ou persistência própria. Ver [Horn Merchant](../entities/horn-merchant.md) para geração, esgotamento, XP e save. Não supor reposição diária.

`NOT_TESTED`: hash do instalado, boot dedicado, geração com registros efetivos, pool vazio, esgotamento, débito/entrega/XP uma única vez, preço efetivo, relog/reload, dois jogadores e proteção. A análise binária não certifica o runtime montado.
