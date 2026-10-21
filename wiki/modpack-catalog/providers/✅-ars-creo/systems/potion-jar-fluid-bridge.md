# Potion Jar ↔ Create potion-fluid bridge

State: `SOURCE-PINNED 5.4.0 / ROUNDING QA PENDING`

Ars Creo registers NeoForge `Capabilities.FluidHandler.BLOCK` on the Ars Nouveau Potion Jar BlockEntityType, backed by `PotionTank`.

Exact conversion constants:

- Ars potion units -> mB: `2.5`;
- mB -> Ars potion units: `0.4`.

Capacity is `int(maxFill * 2.5)`. Fill/drain use ceiling when converting mB back into jar units. Only Create's Potion source fluid with `POTION_CONTENTS` accepted by the Ars jar is valid.

This is a capability adapter, not a second potion inventory. The Ars Potion Jar remains authority for potion type/count; Create/NeoForge fluid transport owns transfer requests.

Rounding at small transfer sizes and interaction with other fluid handlers require runtime QA.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** mod ID `ars_creo`, JAR instalado documentado `ars_creo-1.21.1-5.4.0.jar`, SHA-1 `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Código da versão `5.4.0`: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2` (**SOURCE_CAUSALITY**, sem equivalência binária completa nem QA do pack). Hosts: Ars Nouveau `5.13.1`, Create `6.0.10`. **Ars Creo não registra glyph próprio: +0 IDs novos.**

**Potion Jar ↔ Create — conversão transacional** — efeito do provider externo/integração Create, não nova raiz mágica.

| Eixo | Mecanismo no source pinado | Limite de perk |
|---|---|---|
| Capacidade/tipos | `PotionTank` representa `FluidTank` com capacity `(int)(jar.getMaxFill()×2.5)`; só aceita Create POTION source, `POTION_CONTENTS` presente e `jar.canAccept(...)`. FluidStack retornado deriva de `PotionFluidHandler.getFluidFromPotion(jar.getData(),...)`. | Não criar inventário BA ou novo tipo de poção; Jar Ars é authority. |
| Proporção | `POTION_TO_MB=2.5`, `MB_TO_POTION=0.4`; getFluidAmount faz cast int de jarAmount×2.5; preenchimento e remoção usam `Mth.ceil(mB×0.4)`. Ex.: pedido 1 mB corresponde a **1 unidade Ars** debitada/creditada, cujo equivalente nominal é 2.5 mB. | Rounding é source; não tratar conversão como 1:1 ou arredondamento simétrico. |
| Simulate fill | Simulação devolve `min(capacity,requested)` quando jar vazia, senão `min(capacity-getFluidAmount(),requested)`; não altera jar. | Sem prova de que execução consome a mesma quantidade que foi simulada. |
| Execute fill/observação | Com jar vazia: `amountToAdd=ceil(requested×0.4)` e `jar.add(data,amountToAdd)` então retorna **requested**; com conteúdo: calcula `filled=capacity-getFluidAmount` mas chama `jar.add(data,ceil(requested×0.4))` **antes** de reduzir `filled` se requested<filled. O corpo não limita amountToAdd pelo filled e não testa retorno de jar.add. | ⚠️ possível discrepância de mB retornados vs unidades alteradas; `jar.canAccept`/jar.add podem impor limites no host. Testar sem alegar duplicação/overflow comprovados. |
| Drain | drain(maxDrain) limita a getFluidAmount, obtém FluidStack e na execução chama `jar.remove(ceil(drained×0.4))`. Não há clamp negativo local para maxDrain (depende host). | ⚠️ teste atômico de 1,2,3,5 mB, SIMULATE/EXECUTE, cap e modo da máquina. |
| Segurança de automação | Capacidade é snapshot na construção do wrapper; não há papel de progressão/Target/Hitbox/DamageType. Alterações no jar ocorrem em entidades/fluido de terceiros. | ⛔ não adicionar perks de duplicação, storage externo ou refund no wrapper. |

**Âncoras verificáveis:** [PotionTank.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/common/PotionTank.java#L14-L105) · [CreateCompat.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/CreateCompat.java#L30-L49).

**Aceitação pendente:** Matriz (jar vazia, quase cheia, cheia, mistura incompatível; mB 1,2,3,4,5,capacity±1; simulate→execute, drain→fill, automação Create repetida); provar conservação das unidades e rejeição completa, sem física duplicada no RPG. O RPG Skill Tree não controla o runtime Ars/Create. **0 adapters homologados, +0 IDs de magia.**
