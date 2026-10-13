# Split

- Registry ID: `ars_nouveau:glyph_split`
- Source class: `AugmentSplit`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **3**
- Default mana: **20**

## Source-pinned behavior

Adds additional simultaneous projectiles where a compatible Form implements Split. Projectile explicitly consumes the Split count to create more projectile entities, each carrying the subsequent spell effects.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:relay_splitter` + `ars_nouveau:wilden_spike` + `minecraft:stonecutter`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Split count, projectile spawning and compatible-glyph rules. Black Arcana projectile counts remain bounded by its own effect/work budgets and must not inherit Ars behavior implicitly.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Mapeamento de perk para Codex — transformação real

- **Source pin:** [`AugmentSplit.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentSplit.java) no Ars Nouveau 5.13.1.
- **Implementação exata:** `AugmentSplit` não sobrescreve `applyModifiers` neste source; a contagem é lida por consumidores com `spellStats.getBuffCount(AugmentSplit.INSTANCE)`. `getDefaultManaCost=20`, tier III. **Forma consumidora comprovada:** `MethodProjectile.summonProjectiles` cria `1+count(Split)` entidades `EntityProjectileSpell` no cast padrão e também no overload em blocos. **Perks:** cada projétil carrega effects posteriores; duplicar cast/settlement não é o mesmo que Split. Limites reais de compatibilidade dependem de `getCompatibleAugments` e config do glyph receptor.
- **Bridge:** `source identified / mutation hook NOT VERIFIED / provider-owned`. Não implementar segundo `SpellStats` no Black Arcana, nem usar atributos RPG sem seam verificado. Testes em modpack/Survival PENDING.
