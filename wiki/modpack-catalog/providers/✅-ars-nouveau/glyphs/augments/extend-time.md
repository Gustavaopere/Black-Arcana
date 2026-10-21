# Extend Time

- Registry ID: `ars_nouveau:glyph_extend_time`
- Source class: `AugmentExtendTime`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **10**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's duration modifier. Compatible effects use that stat for provider-owned duration behavior, including effects, summons and other timed spell results.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:clock` + `#c:storage_blocks/redstone`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Duration scaling is provider-owned. Black Arcana durations/cooldowns remain separate server-owned policy values and cannot be silently multiplied by this Ars stat.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentExtendTime.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentExtendTime.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.addDurationModifier(1.0)`; custo default 10, tier II.
- **Regra de efeitos com `IPotionEffect`:** `ticks=baseSeconds*20+extendSeconds*SpellStats.getDurationInTicks()`, com `getDurationInTicks=(int)(20*durationMultiplier)`. `Harm` usa a presença de Extend Time para **trocar dano direto por Poison**, de modo que não é apenas um bônus de duração.
- **Perks:** não alongar cooldown/ritual/estado de outra autoridade por analogia; verificar a regra específica do receptor.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
