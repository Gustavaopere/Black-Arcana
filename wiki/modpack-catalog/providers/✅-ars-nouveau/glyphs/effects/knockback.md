# Knockback

- Registry ID: `ars_nouveau:glyph_gust`
- Source class: `EffectKnockback`
- Display name: `Knockback`
- School: Elemental Air
- Default tier: **1**
- Default mana: **15**
- Default strength config: **1.5** base + **1.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Knocks entities according to provider caster orientation/position and target knockback resistance. On blocks it can convert affected blocks into Ars enchanted falling-block entities and move them. Sensitive prevents the block-moving path. Extract changes entity knockback direction to be away from the caster rather than following the caster look direction.

Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive, Extract. Sensitive is limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:piston` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns `glyph_gust` motion/block conversion. Black Arcana movement remains server-validated and block movement remains subject to its own world-safety policy and bounded work.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectKnockback.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectKnockback.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectKnockback` no Ars Nouveau 5.13.1.
- **Registry real:** `ars_nouveau:glyph_gust`, embora a ficha se chame Knockback e a classe seja `EffectKnockback`. Preservar esse ID na documentação/implementação.
- **Magnitude:** `strength=GENERIC_DOUBLE.get()+AMP_VALUE.get()*getAmpMultiplier()` com defaults 1.5 e 1.0. Para LivingEntity, multiplica por `1-KNOCKBACK_RESISTANCE`; se strength<=0 não aplica o impulso. No horizontal usa metade da velocidade atual menos vetor normalizado*strength. No vertical para alvo no chão usa `min(0.4,vy/2+strength)`, senão mantém vy.
- **Direção:** se `AugmentExtract` presente, vetor de `caster.getPosition().subtract(target.position())`; outro branch depende da rotação do `LivingCaster`, `RotatingTurretTile`, `BasicSpellTurretTile` ou `RuneTile`. O cálculo muda por tipo de invocador, portanto não adotar apenas yaw do jogador.
- **Blocos:** Sensitive faz abort; sem Sensitive seleciona AOE/Pierce por `SpellUtil.calcAOEBlocks` e cria `EnchantedFallingBlock.fall`, aplica knockback e `ShapersFocus.tryPropagateEntitySpell` em cada sucesso. Direitos sobre blocos pertencem ao provider; adapter não duplica entidades.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.
