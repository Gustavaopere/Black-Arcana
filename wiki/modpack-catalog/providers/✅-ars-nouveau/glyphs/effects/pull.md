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

## Auditoria de contrato estático — mobilidade e controle (25/10/2026)

**✅ Contrato técnico source-pinned completo desta ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A marca ✅ aqui é de documentação estática, não de comportamento comprovado no cliente ou integração executável.

| Campo necessário à perk | Comportamento real no source fixo e condicionamentos |
|---|---|
| Identidade | Ars Nouveau `5.13.1`, `ars_nouveau:glyph_pull`, classe `EffectPull`, escola Elemental Air, tier I. [Fonte exata](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPull.java), [IDs binários SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, causalidade e recebedor | `onResolveEntity` calcula `normalize(shooter.position−target.position)` e **substitui** o delta por `direção×(base+ampScalar×ampMultiplier)`, marcando `hurtMarked`; não preserva velocidade prévia. No ramo de bloco, Sensitive aborta; sem Sensitive usa `SpellUtil.calcAOEBlocks`, exige `canBlockBeHarvested`, cria `EnchantedFallingBlock` quando possível e chama `setMotion`/`ShapersFocus`. |
| Parâmetros, fórmulas e caps | Defaults configuráveis para **entidade**: `base=1,0`, `ampScalar=0,5`. Para o **bloco**, `setMotion` utiliza escalar `0,5 + ParticleUtil.inRange(-0,05,0,05) + 0,3×ampMultiplier`, multiplicado pelo **vetor normal da face atingida**, com `+0,1` no eixo Y — **não** pela direção alvo→caster. Com fonte fixada não inferir seed determinística nem alcance radial. Amplify, Dampen, AOE, Pierce e Sensitive compatíveis; Sensitive cap default 1. |
| Alvo/target, geometria, projétil, dano e duração | `EntityHitResult` vetor para shooter; `BlockHitResult` conversão de bloco e impulso pela face do impacto. Nenhum alvo em área por si no ramo entity; AOE/Pierce cobrem apenas posições na grid block. DamageType/duração/vida de projétil não têm valores próprios da classe. |
| Custos, aprendizado e cooldown | Mana default **15**, tier I, recipe default `minecraft:fishing_rod`, XP default **27**, starter default **não**. [Acquisition compilada 85/85](../../ACQUISITION.md). Custo final/cooldown/consumidor da magia composta continuam no Ars. |
| Integração/authority | Não tratar os dois scalars como um atributo compartilhado de perk, nem reproduzir `EnchantedFallingBlock` ou recompensa de acerto por bloco. Nenhuma garantia source de clamp anti-overflow, proteção global ou ordem de hook externo, portanto fail-closed. O RPG Skill Tree fornece perks/progressão mas não assume o `SpellResolver` Ars; Black Arcana só controla seu casting, world policy e riscos internos. APIs de mutação externa não estão comprovadas para este ramo. |
| Validação/proveniência | `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID e classe de registro**, não equivalência de todo classfile/source. Config efetiva, edge-cases, claims, multiplayer e modpack QA **NOT_TESTED**. |

**Gate explícito:** alteração de versão/config, eventos, claims, targeting ou vector motion exige revalidação. Sem Mastery por packet/partícula/tick ou bloco secundário; sem segunda mana, reexecução de efeitos ou Stage promovido.
