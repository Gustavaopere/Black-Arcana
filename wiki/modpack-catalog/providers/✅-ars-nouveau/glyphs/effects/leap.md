# Ars Nouveau — Leap

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_leap`
- Display name: Leap
- School: Elemental Air
- Default tier: 1
- Default mana cost: 25
- Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive
- Source default base movement scalar: 1.5
- Source default Amplify scalar: +1.0
- Source default `force_ground`: false

## Provider-native behavior

Leap sets target motion in its look direction and resets fall distance. It can also convert eligible block targets into Ars `EnchantedFallingBlock` entities and launch them; Sensitive suppresses block movement. Tile casters derive direction from their configured facing/rotation.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau already owns a directional launch/mobility primitive. Black Arcana should not clone generic leap/launch traversal; any mobility spell must have a materially different forbidden-magic identity and preserve server-owned targeting/movement validation.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectLeap`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectLeap.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLeap.java) do Ars 5.13.1.
- **Admissão self:** config `NERF/force_ground` default false; se true, ao mirar caster a partir do ar (`!shooter.onGround()`), retorna sem impulso. `LivingEntity` usa a própria direção `getLookAngle()` e `bonus=max(0,GENERIC_DOUBLE+AMP_VALUE*ampMultiplier)`; defaults 1.5 e 1.0. Não-living usa `getLookVector(shooter,context)` sem clamp zero nessa atribuição.
- **Mira de turret:** `getLookVector` troca direção padrão por `RotatingTurretTile.getShootAngle` ou `FACING` de `BasicSpellTurretTile`/`RuneTile`. Movimento é **set**, não soma ao delta anterior, e zera fallDistance.
- **Block path:** Sensitive cancela; caso contrário percorre AOE/Pierce, cria `EnchantedFallingBlock.fall` e impõe vetor*bonus, propagando ShapersFocus. Perks de mobilidade precisam distinguir salto próprio de lançamento de blocos e respeitar gate de force_ground carregado.
- **Estado:** ✅ origem e lógica source-pinned; ⚠️ helpers, itens externos e runtime QA pendentes; ⛔ adapter de perks do RPG sem teste nem contrato para duplo settlement. Ars conserva mana, inventário e efeitos.
