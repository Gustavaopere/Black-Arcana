# Decelerate

- Registry ID: `ars_nouveau:glyph_decelerate`
- Source class: `AugmentDecelerate`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **5**

## Source-pinned behavior

Adds **-0.5** to Ars Nouveau's acceleration modifier. Compatible provider glyphs interpret that value; Projectile uses it to reduce projectile velocity.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:soul_sand` + `minecraft:cobweb` + `minecraft:clock`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns compatible-glyph selection, acceleration semantics and configured mana cost. This is not a Black Arcana-wide speed modifier.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentDecelerate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDecelerate.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.addAccelerationModifier(-0.5F)`; custo default 5, tier II.
- **Consumo:** `MethodProjectile` usa `velocity=Math.max(0.1f,0.75f+getAccMultiplier()/2)`; um Decelerate contribui −0.25 no termo antes do piso de 0.1 (mantidos os demais modificadores).
- **Perks:** velocidade menor não equivale a maior duração de entidade, controle temporal nem penetração; o lifetime default do Projectile permanece configurável por outro campo.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
