# Magic Conch — Summon Deep Ones

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:magic_conch`
- Trigger: charged use/release
- State: `COUNTED_EXACT`

## Semantic identity

The provider settles one temporary allied Deep One group summon for the user. Deep One, Deep One Knight and Deep One Mage are participants or variants of this same root rather than separate summon identities.

## Exact acquisition

Exact provider data closes Magic Conch through Deep One Knight barter loot.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles and sounds remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Contrato causal do Magic Conch — fonte pública fixada (não homologado no JAR físico)

**Teto de evidência (2026-10-28).** As identidades são `COUNTED_EXACT` pelo relatório de auditoria da versão instalada `alexscaves` 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Os parâmetros abaixo resultam de inspeção **read-only** do fonte público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`; a igualdade binária desse commit com o JAR físico **não foi demonstrada**. Rotular esses parâmetros `SOURCE_SNAPSHOT_ONLY`, e **não** `COMPLETE_PERK_READY`. Configs efetivas, chamadas packet/runtime, hooks mutadores e QA física permanecem `NOT_VERIFIED`.

| Parâmetro / seam | Evidência method-pinned do snapshot |
|---|---|
| Entrada | `MagicConchItem.use` inicia `startUsingItem`; `releaseUsing` calcula carga por `getUseDuration(stack)-useTimeLeft`; o default de `getUseDuration` é **1200 ticks**, mas é limite de uso, não duração obrigatória de carga |
| Gatilho mínimo | Só entra no bloco de custos/spawn/cooldown com **carga >25 ticks**. O som é chamado antes da condição; som isolado não prova invocação bem-sucedida |
| Famílias de invocados | `DEEP_ONE`, `DEEP_ONE_KNIGHT`, `DEEP_ONE_MAGE`: limites-base **3/2/1** no snapshot (`nextInt(1)` sempre retorna zero para bound válido 1). Tentativas de spawn são **até 99 por família**, não garantia de 6 participantes |
| Encantamento CHARTING_CALL | Altera limites pela amostragem `nextInt(Math.max(level-1,2))`, `nextInt(Math.max(level-2,0))`, `nextInt(Math.max(level-3,0))`. **Risco de bound zero:** para alguns níveis positivos as duas últimas expressões podem resultar em zero; o contrato exato e possível falha do RNG devem ser auditados no JAR e testados com níveis 1–4 antes de qualquer perk de quantidade |
| Tempo e cooldown | `time=1200+400*level(LASTING_MORALE)` ticks, entregue a `setSummonedBy(summoner,time)` e a `ACCompat.addCooldown(player,stack,time)`; o valor é comum no método, mas duração real depende do lifecycle da entidade e do pack |
| Posição / mundo | `summonDeepOne` amostra X/Z com deslocamentos inteiros **-10..9**, começa **7 blocos acima** e busca terreno pela coluna; aceita água ou superfície válida, exige `checkSpawnObstruction` antes de `addFreshEntity`. Falhas deixam o limite de quantidade não alcançado |
| Custo e consequências | No ramo sem `TAXING_BELLOW`, o item usa **1 unidade de durabilidade**. Com `TAXING_BELLOW`, reduz `DamageValue` em 1 até zero e registra `hurtRelations`; se houver pelo menos um summon, aplica **-2 reputation** apenas via `lastSummonedDeepOne.addReputation` |
| Ownership | `setSummonedBy`, `finalizeSpawn` e `copyTarget` são provider-owned; três tipos de Deep One formam **uma ação**, não três novos feitiços |

### Gating de integração

Não transformar `getUseDuration=1200` em tempo de cast obrigatório, nem contabilizar tentativas de `summonDeepOne` como sucessos. O cálculo de limite `CHARTING_CALL` merece regressão para `level=0,1,2,3,4` no JAR exato: o snapshot contém um potencial `nextInt(0)`, **não um crash confirmado no modpack**. Perks de quantidade/duração exigem hook pré-spawn provider-native, limites server-side, gate de invocações, deduplicação do dono e não duplicação de custo/reputação. **⛔ Fail-closed** enquanto essa seam não estiver verificada.

**Fontes:** [`MagicConchItem.use/releaseUsing/summonDeepOne`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/MagicConchItem.java); [relatório de identidade exata](../EXACT-1.0.10-ARTIFACT-AUDIT.md).
