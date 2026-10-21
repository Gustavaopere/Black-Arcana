# Ars Nouveau — Craft

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_craft`
- Display name: Craft
- School: Manipulation
- Default tier: 1
- Default mana cost: 50
- Compatible augments: none

## Provider-native behavior

Opens a remote crafting menu for a real player caster. Ars provides a crafting menu whose validity is not tied to remaining near a workstation.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:crafting_table`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

This provider already owns generic remote crafting. Black Arcana should not add another plain crafting-access spell unless the mechanic materially changes into a forbidden-magic contract rather than duplicating utility.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCraft`).

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectCraft.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCraft.java), Ars Nouveau 5.13.1.
- **Admissão:** `onResolve(HitResult,...,shooter,...)` abre menu somente se `shooter instanceof Player` **e** `isNotFakePlayer(shooter)`; não há branch por alvo nem resultado de craft associado ao glyph.
- **UI real:** `SimpleMenuProvider` instancia `CustomWorkbench extends CraftingMenu` com `ContainerLevelAccess.create(player.world,player.blockPosition())`. O override `CustomWorkbench.stillValid(Player)` retorna sempre `true`: a validade do menu não depende da proximidade de uma mesa. Sem augments; mana default 50.
- **Perks:** evento de cast/menu aberto não comprova crafting efetivo, remoção de ingredientes nem concessão de receita. Não reimplementar inventário, nem recompensar Mastery por cada clique de crafting sob a identidade do spell.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.
