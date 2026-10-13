# Accelerate

- Registry ID: `ars_nouveau:glyph_accelerate`
- Source class: `AugmentAccelerate`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **10**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's acceleration modifier. Provider glyphs that declare Accelerate compatible interpret that stat; Projectile uses it to increase projectile velocity.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:powered_rail` + `minecraft:sugar` + `minecraft:clock`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns augment compatibility, acceleration semantics and effective configured cost. Black Arcana must not treat this modifier as a universal projectile-speed API.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentAccelerate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAccelerate.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers(SpellStats.Builder,AbstractSpellPart)` chama `builder.addAccelerationModifier(1.0F)`; custo default 10, tier II.
- **Consumidor comprovado:** `MethodProjectile.summonProjectiles` usa `velocity=Math.max(0.1f,0.75f+spellStats.getAccMultiplier()/2)`. O +1.0 do operador contribui +0.5 à expressão de velocidade quando não há outros modificadores, **não** +1 bloco/tick universal.
- **Perks:** velocidade e quantidade de projéteis são variáveis distintas. Respeitar `getCompatibleAugments` da Form e permitir apenas bridges com assinatura verificável.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
