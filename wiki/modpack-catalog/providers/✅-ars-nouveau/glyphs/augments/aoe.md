# AOE

- Registry ID: `ars_nouveau:glyph_aoe`
- Source class: `AugmentAOE`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **35**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's AOE spell stat. Compatible glyphs interpret the stat to expand their affected area around a target.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:firework_star`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns this AOE stat and its per-glyph interpretation. Black Arcana area geometry remains explicitly server-bounded and cannot inherit an unbounded Ars radius contract.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Mapeamento de perk para Codex — transformação real

- **Source pin:** [`AugmentAOE.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAOE.java) no Ars Nouveau 5.13.1.
- **Transformação exata:** `applyModifiers` chama `builder.addAOE(1.0)`. `getDefaultManaCost=35`, tier II. **Interpretação:** o glyph receptor decide a geometria, p.ex. `EffectBreak` usa `SpellUtil.calcAOEBlocks`, `EffectFreeze` calcula AOE e depois examina seis vizinhos por posição e `EffectExplosion` usa o multiplicador para intensidade. **Perks:** +1 AOE do Ars não representa +1 bloco de raio universal; sem analisar o consumidor e seus caps/work budgets, mutação externa da área continua ⛔.
- **Bridge:** `source identified / mutation hook NOT VERIFIED / provider-owned`. Não implementar segundo `SpellStats` no Black Arcana, nem usar atributos RPG sem seam verificado. Testes em modpack/Survival PENDING.
