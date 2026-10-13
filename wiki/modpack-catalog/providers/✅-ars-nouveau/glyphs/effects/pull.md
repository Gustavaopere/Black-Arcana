# Pull

- Registry ID: `ars_nouveau:glyph_pull`
- Source class: `EffectPull`
- School: Elemental Air
- Default tier: **1**
- Default mana: **15**
- Default entity velocity config: **1.0** base + **0.5** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Pull moves entity targets toward the caster. On block targets it can convert harvestable blocks into Ars enchanted falling-block entities and give them motion relative to the hit face. Sensitive disables block pulling.

Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive. Sensitive is limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:fishing_rod`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns Pull motion and block conversion. Black Arcana displacement remains server-owned and any block movement remains under `WorldEffectPolicy` and bounded work.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Código exato:** [`EffectPull.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPull.java), Ars 5.13.1.
- **Entity motion:** forma vetor da posição da entidade para shooter e define `deltaMovement=normalize(shooter.position-target.position)*scalar`; scalar default `GENERIC_DOUBLE=1.0` + `AMP_VALUE=0.5*ampMultiplier`, sem clamp de sinal neste método.
- **Blocos e direção:** Sensitive interrompe. Sem Sensitive, `SpellUtil.calcAOEBlocks` + `canBlockBeHarvested` e `EnchantedFallingBlock.fall`; se criado, `setMotion` usa `scalar=0.5+random(-0.05..0.05)+0.3*ampMultiplier` multiplicado pelo **normal da face atingida**, somando 0.1 ao Y. **Não** usa o vetor target→caster na branch bloco; ShapersFocus pode propagar.
- **Perks:** aumentar Pull de entidade não dá a mesma modificação de movimento de bloco. Separar scalar por path, loaded chunks e work budget; nenhum hook de bloco garantido por seta em SpellStats.
- **Estado:** ✅ assinatura/source; ⚠️ integração de plugins proteção, configs e gameplay pending; ⛔ nenhum adapter RPG testado nem permissão para duplicar a cadeia causal/perk/mastery.
