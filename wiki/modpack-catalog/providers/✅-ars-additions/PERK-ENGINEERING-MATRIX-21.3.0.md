# Ars Additions 21.3.0 — matriz de engenharia de perks (5 raízes)

Status: ✅ **3/3 glifos + 2/2 rituais** com ficha individual, classe e callsites source-pinned. ⚠️ API host Ars 5.13.1, JAR runtime, config e QA condicionados. ⛔ adapter RPG não implementado.

Versão física: `ars_additions-1.21.1-21.3.0.jar`, SHA-1 `ce2440b606acb20b79a42bf7c6c24d163c93241f`; source `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`. O build baseline público referencia Ars 5.11.2.1298 enquanto pack usa Ars 5.13.1 — compatibilidade de execução é assunto separado de identificação.

| Ficha | Classe / cadeia verificável | Risco para perks |
|---|---|---|
| [Mark](glyphs/mark.md) | `EffectMark`; salva `MARK_DATA` (GlobalPos/entity UUID) no Reliquary; jogador recebe MARKED | Never mirror reference store ou contar potion + mark em dobro |
| [Recall](glyphs/recall.md) | `MethodRecall`; valida Reliquary, ServerLevel e MarkData; `mark.cast` executa resolve/debit downstream | Remote target não é gate bypass; cost/durability têm authority do addon |
| [Retaliate](glyphs/retaliate.md) | `MethodRetaliate`; `caster.getKillCredit` seleciona target; `resolver.onResolveEffect` | Descrição 5s não é guard demonstrado no método |
| [Arcane Permanence](rituals/arcane-permanence.md) | `RitualChunkLoading`; tickets `(2*radius+1)^2`, source repeat interval e `ChunkLoadingData` | Black Arcana no-force-load; jamais estender tickets por perk |
| [Locate Structure](rituals/locate-structure.md) | `RitualLocateStructure`; recipe gate, `LocateUtil.locateCenter`, WAYFINDER, refunds | não duplicar lookups, item debit/refund ou autorização de teleporte |

**Semântica de tokens/custo:** Ars Nouveau host é dono do SpellResolver/mana; Ars Additions é dono dos seus estados/itens/tickets/rituais. `EffectResolveEvent.Pre` do host pode existir mas não comprova intervenção segura nas classes do addon; nenhum hook de ledger da RPG Skill Tree foi testado.

**Validação para execução futura:** inspecionar assinaturas efetivamente carregadas no host 5.13.1, timeouts/reloads/chunk tickets, fallback de target, caster fake/turret e exatamente-uma-concessão de Mastery. Não inferir JAR equivalência source-code a partir da tag de versão.

[README](README.md) · [padrão global](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
