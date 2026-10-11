# BetterEnd 21.0.34 — Infusion Ritual `betterend:quick_charge_book`

Estado: **✅ catalogado / `COUNTED_EXACT`** — identidade e resultado confirmados no artefato BetterEnd 21.0.34; **⚠️ execução em Survival e parâmetros individuais não verificados**.

## Ficha de identidade

- **Recipe ID:** `betterend:quick_charge_book`.
- **Recipe type:** `betterend:infusion` (ritual de Infusion Pedestal, não spell registry de Iron's ou Ars).
- **Resultado — item ID:** `minecraft:enchanted_book`.
- **Família editorial:** livro encantado (uma das 39 receitas distintas).
- **Posição no inventário exato:** 35/48 (ordinal editorial, não prioridade de execução).
- **Confidence:** `COUNTED_EXACT`, inventário 48/48 de recipes do tipo `betterend:infusion`.
- **Contribuição incremental desta ficha:** **+0 novas identidades**; já incluída nas 48 infusões e 49 rituais BetterEnd do ledger.

## Contrato de execução comprovado

O provider `betterend` possui o ciclo `InfusionRitual`: busca uma receita `betterend:infusion`, usa a duração definida pela receita aceita, monta seu resultado e o devolve ao Infusion Pedestal. Identidade, matching, duração, consumo, estado do pedestal e settlement pertencem ao BetterEnd.

O item de saída comum `minecraft:enchanted_book` **não** autoriza colapsar as 39 receitas em uma só. Este recipe ID é independente. O encantamento, nível e componentes/NBT efetivamente gravados no livro não foram extraídos para esta ficha.

## Limites de evidência e interoperabilidade

- **Ingredientes de entrada, quantidades e arranjo dos pedestais:** **NÃO VERIFICADO individualmente** nesta materialização; consultar dados provider-native antes de descrever a receita jogável.
- **Tempo exato desta receita:** **NÃO VERIFICADO individualmente**; a duração é controlada pela receita BetterEnd, sem valor inventado.
- **Desbloqueio, configuração efetivamente implantada e obtenção em Survival:** **⚠️ PENDENTE de teste no modpack real**.
- **API/hook para observar conclusões:** **NÃO VERIFICADO**. Sem contrato real, Black Arcana permanece `fail-closed`, não replica pedestal, custo, output, ritual ou eventos.
- **Proveniência exata:** `BetterEnd-21.0.34.jar`, mod ID `betterend`, SHA-1 físico/publicador `149b73179ea63bf777315a7c850b2eba65c554bd`; CurseForge File `8610367`, auditoria física exata já documentada. Nenhum código, asset ou recipe JSON de terceiros é redistribuído.

**Referências:** [inventário dos 48 IDs e resultados](../INFUSION-RITUAL-CATALOG.md) · [auditoria binária exata](../../EXACT-21.0.34-ARTIFACT-AUDIT.md) · [provider e ownership](../../README.md).
