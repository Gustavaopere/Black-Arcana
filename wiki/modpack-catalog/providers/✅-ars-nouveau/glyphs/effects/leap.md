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

## Auditoria de contrato estático — mobilidade e controle (25/10/2026)

**✅ Contrato técnico source-pinned completo desta ficha; ⛔ hook mutador de perks `NOT_VERIFIED`; ⚠️ QA físico `NOT_TESTED`.** A marca ✅ aqui é de documentação estática, não de comportamento comprovado no cliente ou integração executável.

| Campo necessário à perk | Comportamento real no source fixo e condicionamentos |
|---|---|
| Identidade | Ars Nouveau `5.13.1`, `ars_nouveau:glyph_leap`, classe `EffectLeap`, escola Elemental Air, tier I. [Fonte exata](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLeap.java), [IDs binários SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, causalidade e recebedor | `onResolveEntity` obtém entidade do hit. Config `force_ground` (`NERF`) default **false** aborta apenas quando o alvo é o caster e este está fora do chão; não é um gate geral de todas as entidades. Para `LivingEntity`, vetor `entity.getLookAngle()` e `bonus=max(0,base+ampScalar×ampMultiplier)`; para não-living, `getLookVector(shooter,spellContext)` e bônus **sem clamp para zero**. Depois **substitui** `setDeltaMovement` e zera `fallDistance`. `onResolveBlock` com Sensitive retorna; sem Sensitive cria `EnchantedFallingBlock` na grade e define seu vetor pela orientação do wrapped caster com `ShapersFocus`. |
| Parâmetros, fórmulas e caps | Config defaults `base=1,5`, `ampScalar=1,0`, `force_ground=false`. Amplify, Dampen, AOE, Pierce e Sensitive são compatíveis; Sensitive cap default 1. `getLookVector` usa rotação de `RotatingTurretTile`, estado `FACING` de `BasicSpellTurretTile`/`RuneTile`, ou `shooter.getLookAngle()`; orientação da entidade-alvo living não é necessariamente a do caster. AOE/Pierce expandem apenas o ramo de blocos, não adicionam área ao golpe em entidade. |
| Alvo/target, geometria, projétil, dano e duração | Alvo `EntityHitResult`: motion direção do olhar da própria entidade viva; alvo não-vivo usa direção do caster tile/shooter. Alvo `BlockHitResult`: blocos convertidos em entidades `EnchantedFallingBlock` mediante retorno não nulo. Sem DamageType, tamanho de projétil ou duração próprios: o estado de movimento do Minecraft é downstream. |
| Custos, aprendizado e cooldown | Mana default **25**, tier I, recipe default `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` ×3, XP default **27**, starter default **não**. [Acquisition compilada 85/85](../../ACQUISITION.md). Custo final/cooldown/consumidor da magia composta continuam no Ars. |
| Integração/authority | Não aplicar o mesmo modificador ao movimento de living e não-living ignorando clamp, nem reinterpretar `force_ground` como permissão de voo do jogador. Ars controla movimento, conversion/permissions e ShapersFocus; Black Arcana não duplica world mutation nem cast; nenhum hook RPG/Black Arcana validado. O RPG Skill Tree fornece perks/progressão mas não assume o `SpellResolver` Ars; Black Arcana só controla seu casting, world policy e riscos internos. APIs de mutação externa não estão comprovadas para este ramo. |
| Validação/proveniência | `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID e classe de registro**, não equivalência de todo classfile/source. Config efetiva, edge-cases, claims, multiplayer e modpack QA **NOT_TESTED**. |

**Gate explícito:** alteração de versão/config, eventos, claims, targeting ou vector motion exige revalidação. Sem Mastery por packet/partícula/tick ou bloco secundário; sem segunda mana, reexecução de efeitos ou Stage promovido.
