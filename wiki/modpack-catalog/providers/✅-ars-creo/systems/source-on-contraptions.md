# Source on Create contraptions

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Ars Creo registers Ars Source Jar and Creative Source Jar as `SourceInfo` types and exposes the moving contraption through an Ars `ISpecialSourceProvider`.

Normal Source is read from the jar NBT, maxes at 10,000 per registered normal jar in this source implementation and is added/removed directly from the contraption's serialized block info. The aggregate `ContraptionSource` sums the registered Source blocks and uses the maximum transfer rate among them.

A Creative Source Jar causes `hasInfiniteSource()` to return true. `SourceUtilMixin` then special-cases Ars source search/take logic for this provider.

`SourceJarBehavior` adds one provider per moving contraption to Ars `SourceManager` and removes it when movement stops.

Authority remains Ars Source. Black Arcana must not create a parallel moving-resource cache or second deduction.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** mod ID `ars_creo`, JAR instalado documentado `ars_creo-1.21.1-5.4.0.jar`, SHA-1 `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Código da versão `5.4.0`: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2` (**SOURCE_CAUSALITY**, sem equivalência binária completa nem QA do pack). Hosts: Ars Nouveau `5.13.1`, Create `6.0.10`. **Ars Creo não registra glyph próprio: +0 IDs novos.**

**Source em contraptions — proveniência e limite** — efeito do provider externo/integração Create, não nova raiz mágica.

| Eixo | Mecanismo no source pinado | Limite de perk |
|---|---|---|
| Provedor/registrar | SourceJarBehavior.startMoving/tick chama `addIfMissing` somente servidor e não adiciona provider duplicado para mesma entity; `stopMoving` procura um `ContraptionSourceProvider` correspondente e remove. Lifecycle é de Create/Ars SourceManager. | ⛔ Não criar cache/ledger paralelo de Source para perks e não registrar múltiplos providers por contraption. |
| Inventário/escala | ContraptionSource.getSource e getMaxSource somam `SourceInfo` de `contraption.getBlocks().values()`; getTransferRate usa **máximo** das taxas (não soma). JAR normal tem `maxSource=10.000`, `transferRate=10.000`, Source inicial lido do NBT do bloco. | Varredura bounded pelo número de blocos da contraption, mas chamada repetida pode ser custosa; não ler a cada tick externo. |
| Debit/credito | ContraptionSource.addSource/removeSource percorrem SourceInfo e aplicam `min(room,remaining)` ou `min(source,remaining)`, retornando Source total após operação. JAR Source local atualiza NBT `SourceJarTile.SOURCE_TAG`; alteração visual do fill ocorre nas mudanças de estado. | Owner de Source permanece Ars/Create; Mastery não usa cada NBT change como cast. |
| Creative/infinito | CreativeSourceJarInfo registra valor nominal **1.000.000** mas não altera saldo em remove/add e `hasInfiniteSource()` é true. SourceUtilMixin intercepta `takeSourceMultiple` e restitui valores já debitados em outros providers `takenFrom` antes de devolver o provider criativo. | Não converter 'infinite source' em mana infinita para Black Arcana, nem replicar o refund. |
| Risco de configuração | Sem contrato observável de capacidade per-caster/por perk ou setter de Source transacional de terceiro; presença de Creative Jar pode alterar selection de supplier. | ⛔ alteração externa de maxSource/transferRate/priority sem interface real; validar host SourceUtil 5.13.1. |

**Âncoras verificáveis:** [SourceJarBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/SourceJarBehavior.java#L12-L44) · [ContraptionSource.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/source/ContraptionSource.java#L17-L88) · [SourceJarInfo.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/source/SourceJarInfo.java#L14-L71) · [CreativeSourceJarInfo.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/source/CreativeSourceJarInfo.java#L7-L47) · [SourceUtilMixin.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/mixin/SourceUtilMixin.java#L18-L34) · [ContraptionUtils.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/ContraptionUtils.java#L41-L59).

**Aceitação pendente:** Contraption de 0/1/N jars, dois SourceManager events, motion start/stop/relog, Creative Jar junto a JAR comum, débito com Source externo e refund, performance com centenas de blocos, source negativo/corrompido e convergência visual do fill. O RPG Skill Tree não controla o runtime Ars/Create. **0 adapters homologados, +0 IDs de magia.**
