# Fortune / Luck

- Registry ID: `ars_nouveau:glyph_fortune`
- Source class: `AugmentFortune`
- Source display name: `Luck`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **80**

## Source-pinned behavior

Increases relevant drop chances for compatible provider behavior, including mobs killed through the provider damage path and blocks broken through Break. It is declared incompatible with Extract.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:rabbit_foot`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns its loot/fortune calculations and compatible-glyph semantics. Black Arcana must preserve provider causal identity and must not double-apply external Fortune/Looting-style rewards.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentFortune.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentFortune.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `AugmentFortune` não sobrescreve `applyModifiers` em 5.13.1; mana default 80, tier II, ID de registry `glyph_fortune` embora display `Luck`.
- **Break:** `getBuffCount(AugmentFortune.INSTANCE)` determina nível de `FORTUNE` aplicado à ferramenta simulada quando o item ainda não o tem nesse nível; limite default da `EffectBreak`: 4. Outros consumos de loot dependem de classes de efeito específicas (não presumir chance universal de drop).
- **Perks:** não dar double drops ao RPG por evento de break/hit; preservar incompatibilidade semântica com Extract.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
