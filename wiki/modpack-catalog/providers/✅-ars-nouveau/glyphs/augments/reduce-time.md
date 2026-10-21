# Reduce Time

- Registry ID: `ars_nouveau:glyph_duration_down`
- Source class: `AugmentDurationDown`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **15**

## Source-pinned behavior

Adds **-1.0** to Ars Nouveau's duration modifier. Compatible timed glyphs interpret that reduced duration.

The 1.21.1/5.13.1 source deliberately retains the registry path `glyph_duration_down`; an upstream comment only proposes a key rename for 1.22. This catalog therefore preserves the installed-line ID rather than normalizing it to the display name.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:clock` + `minecraft:glowstone_dust`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars duration semantics remain provider-owned. Black Arcana must not alter its own cooldown or hazard durations through this glyph unless a future explicit integration contract says so.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentDurationDown.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDurationDown.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Identidade exata:** registry `ars_nouveau:glyph_duration_down` (não `glyph_reduce_time`); class `AugmentDurationDown` e `applyModifiers=builder.addDurationModifier(-1.0d)`; default mana 15, tier II.
- **Ramo condicional:** em `EffectHarm`, a **presença** de Duration Down também troca dano instantâneo por Poison. Em `IPotionEffect`, duração após a alteração depende do produto `extendSeconds * getDurationInTicks()` e do cast context; não interpretar como desconto fixo em ticks universal.
- **Perks:** respeitar recipe/limites/config do receptor e impedir duração negativa ou bypass quando uma magia Black Arcana criar seu próprio contrato.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
