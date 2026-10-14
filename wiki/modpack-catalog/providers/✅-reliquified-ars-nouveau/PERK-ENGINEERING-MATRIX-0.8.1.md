# Reliquified Ars Nouveau 0.8.1 — matriz de engenharia inicial das 19 habilidades

**Estado:** 19/19 raízes de `AbilityTemplate.builder` com identidade física `COUNTED_EXACT` comprovada no [audit #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129). **3/19** agora com execução Java source-located detalhada. Fonte declarada 0.8.1: `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`; JAR instalado `reliquified_ars_nouveau-1.21.1-0.8.1.jar`, SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579`. Corpo compilado/QA não testados.

| Habilidade (root única) | Fonte | Contrato causal |
|---|---|---|
| [Echo Spell / Archmage Glove](abilities/archmage-glove.md) — `multicasted` | `items/hands/ArchmageGloveItem` | `SpellCastEvent` + `AugmentMulticast` após form, filhos `(i+1)*5` ticks, custo dos filhos `0` no evento, refill e proteção condicionais |
| [Arcane Reserve / Mana Ring](abilities/mana-ring.md) — `resonance` | `items/ring/ManaRingItem` | `MaxManaCalcEvent`, `ManaRegenCalcEvent`, `LivingHealEvent`, `SpellCostCalcEvent.Pre`, `PlayerTickEvent.Post`; dívida persistida/repagamento |
| [Last Will / Ring of Last Will](abilities/ring-of-last-will.md) — `last_will` | `items/ring/RingOfLastWillItem` | `LivingIncomingDamageEvent` cancela hit potencialmente fatal, `RewindEvent` 60 ticks, cooldown e vingança por UUID, synergy `EntityDummy` |

**Não supercontabilizar:** multicast filhos e refund; mana do Ars e dívida do anel; rewind e vingança não constituem novas identidades raízes nem transferem ownership para Black Arcana. Eventos públicos usados pelo provider não são automaticamente adapter homologado de RPG Skill Tree.

**Gates:** 16 outras raízes exigem dossiê de comportamento; config, binário compilado, multiplayer, custos, Survival e teste de interação com Ars 5.13.1/Relics 0.12.8 permanecem **⚠️**; integração de perks/Mastery **⛔**. Alterações somente documentais. Nenhum Stage runtime foi promovido.

[Índice do provider](README.md) · [Padrão editorial](../../meta/PERK-READY-TECHNICAL-STANDARD.md) · [Ledger global](../../meta/PERK-READY-COVERAGE-LEDGER.md).
