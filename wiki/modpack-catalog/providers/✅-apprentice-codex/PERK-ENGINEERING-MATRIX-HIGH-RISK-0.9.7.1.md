# Apprentice's Codex 0.9.7.1 — primeira matriz de engenharia causal de alto risco

**Data:** 2026-10-13. **Resultado incremental:** 8 dossiês adicionais desta etapa, elevando a cobertura causal profunda de **6/83 para 14/83**. As 83/83 identidades já estavam catalogadas; o denominador global não muda (**+0**). **69/83** ainda aguardam este grau de engenharia; é diferente de identidade não catalogada.

**Autoridades:** modlist sibling atual `apprentice_codex-0.9.7.1+mc1.21.1.jar`, `modid=apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`; versão publicamente declarada pelo source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. O JAR instalado não foi inspecionado byte-a-byte para as implementações destes handlers; evidência neste lote é **source-located**. Iron's 3.16.3 detém mana, escolas, cast e cooldowns base; o addon detém as ações/entidades próprias.

| Spell ID | Dossiê causal | Source exato de efeitos/limites | Principal risco de integração |
|---|---|---|---|
| `apprenticecodex:anchor_blink` | [Anchor Blink](ender/anchor-blink.md) | `AnchorBlinkDaggerEntity.tryBlink/canStandAt`; 60 ticks anchor, 40 ticks pós-blink | Recibo duplo arremesso/blink, world border, estado de proteção |
| `apprenticecodex:rift_hole` | [Rift Hole](ender/rift-hole.md) | `RiftHole.openTunnel/closeTunnel`, `RiftHoleBlockSafety.canReplace`; UUID de túnel | Mundo/claims, reconciliação de blocos mutados por terceiros |
| `apprenticecodex:remote_eye` | [Remote Eye](ender/remote-eye.md) | `RemoteEyeBodyControlEvent.onPlayerTick`; anchor e NBT time repair | Corpo imobilizado, morte/relog/dimensão, câmera não-autoritativa |
| `apprenticecodex:auto_magnet` | [Auto Magnet](ender/auto-magnet.md) | `AutoMagnetFamiliarEntity.collectNearbyDrops`, manager, ticks 2 | Cobrança uma vez por lote de itens; XP orbs separadas, pickup |
| `apprenticecodex:linear_build` | [Linear Build](evocation/linear-build.md) | `LinearBuild.placeLine/tryPlaceAt` e item-sources | Mana apenas por bloco aceito, rollback local se consumeOne falha |
| `apprenticecodex:earth_forge` | [Earth Forge](nature/earth-forge.md) | `EarthForgeJob.tick/tryPlaceDirt`, placement rules | Job 1 tentativa/2 ticks e fallback direto quando owner inválido |
| `apprenticecodex:force_field` | [Force Field](holy/force-field.md) | `ForceFieldDefenseEvent.onLivingAttack`, `neutralizeProjectile`, mana debit | Intercepto no scan e no evento, priority HIGHEST, pagamento uma vez |
| `apprenticecodex:demicreator_wings` | [Demi-creator Wings](ender/demicreator-wings.md) | `DemicreatorWingsManager.isInsideCoreArea/stripGrantedFlight`, lifecycle | Gate X/Z sem Y nesse método; risco de revogação concorrente de `mayfly` |

## Notas de implementação de perks e segurança

- **Perk A — estatísticas:** cada spell tem levels e scalings registrados nas fichas originais; valores do source são fórmulas/defaults, não proof de configuração efetiva.
- **Perk B — identidade causal:** o cast Iron's, recast, manager job, projétil, coleta, impacto, controle de voo e limpeza devem preservar o mesmo nexo de causalidade. O observador não pode tratar um efeito como segundo cast independente. Não há token interoperável de cast validado com o RPG nesta etapa.
- **Perk C — recursos, transações, autoridade:** mana é de Iron's; custos adicionais de blocos e coleta são exclusivamente provider-native. WorldEffectPolicy BA governa **efeitos criados por BA**, não deve executar de novo o efeito externo já liquidado.
- **Perk D — limites e integridade:** área, timers, chunk/claim checks, logout/relog, NBT, proteção PvP, fuga de alcance e eventos cross-mod requerem QA próprio. Algumas superfícies estão em `ForceFieldDefenseEvent`, `EarthForgeJob` e outros helpers, não apenas na classe da spell.
- **⚠️ Parcial/condicionado:** source pin alinhado à release declarada, sem prova de equivalência dos métodos ao JAR físico ou GameTest do provider.
- **⛔ Bloqueado:** nenhum adapter de Mastery/perks/atributos confirmado e implementado; fail-closed até contrato real. Sem Stage 06.05 promotion.

**Escopo da mudança:** 8 fichas existentes atualizadas, este índice, README do provider e ledger global: documentação somente, **0 Java** e **0 raízes semânticas adicionais**.

[Registry 83/83](README.md) · [Regras de interoperabilidade](INTEGRATION-RULES.md) · [Padrão técnico](../../meta/PERK-READY-TECHNICAL-STANDARD.md) · [Ledger global](../../meta/PERK-READY-COVERAGE-LEDGER.md).
