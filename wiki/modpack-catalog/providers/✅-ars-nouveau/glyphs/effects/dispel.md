# Dispel

- Registry ID: `ars_nouveau:glyph_dispel`
- Source class: `EffectDispel`
- School: Abjuration
- Default tier: **1**
- Default mana: **30**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Posts Ars Nouveau `DispelEvent.Pre` and honors cancellation before resolution. On living entities it removes milk-curable effects except provider-tagged deny entries, plus explicitly provider-tagged allow entries; it then invokes `IDispellable` where supported and posts `DispelEvent.Post`. Blocks/block entities implementing `IDispellable` receive the same provider dispel callback/event framing.

Compatible augments: none in the exact 5.13.1 class.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:milk_bucket` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

This is a real Ars-supported event/interface surface, but it remains Ars authority. A future Black Arcana adapter may observe/use a supported seam only after exact API-contract review; it must not reinterpret Dispel as authority over Black Arcana state, Corruption, Strain or arbitrary third-party effects.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / API CANDIDATE SEAM IDENTIFIED / RUNTIME QA PENDING`.

## Dossiê de engenharia para perks — cadeia e interfaces

- **Source pin:** [`EffectDispel.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDispel.java), Ars Nouveau 5.13.1.
- **Boundary real:** `NeoForge.EVENT_BUS.post(new DispelEvent.Pre(hit,world,shooter,spellStats,spellContext))` antes da resolução, com `isCanceled()`; `DispelEvent.Post` depois, condicionado ao ramo. Evento concreto é prova de veto/observação para **Dispel**, não de mutação universal das magias Ars. **Mob effects:** remove `EffectCures.MILK` exceto `PotionEffectTags.DISPEL_DENY`, também remove exceções `DISPEL_ALLOW`; chama `IDispellable.onDispel(shooter)` em entidades vivas. Blocos/BlockEntities `IDispellable` recebem callback próprio. **Augments:** nenhum na classe.
- **Estado:** ✅ classe exata lida; ⚠️ helpers/config real e Survival pendentes; mutabilidade via RPG Skill Tree ⛔ sem interface comprovada que altere esses parâmetros. Ars conserva authority de recursos/efeitos.
