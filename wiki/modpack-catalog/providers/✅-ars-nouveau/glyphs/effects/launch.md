# Launch

- Registry ID: `ars_nouveau:glyph_launch`
- Source class: `EffectLaunch`
- School: Elemental Air
- Default tier: **1**
- Default mana: **30**
- Default vertical strength config: **0.8** base + **0.25** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Adds upward motion to entity targets and resets their fall distance. On blocks it may convert provider-calculated blocks into enchanted falling-block entities and launch them; Sensitive disables the block-moving path.

Compatible augments: Amplify, Dampen, AOE, Sensitive, Pierce. Sensitive is limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:rabbit_hide` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns Launch motion and falling-block conversion. Black Arcana launch/movement remains server-authoritative, and any Black Arcana block movement must pass world-safety and bounded-work gates.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectLaunch.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLaunch.java) do Ars 5.13.1.
- **Entity velocity:** `onResolveEntity` usa `setDeltaMovement(old.add(0,GENERIC_DOUBLE+AMP_VALUE*ampMultiplier,0))`; defaults base 0.8 e amp scalar 0.25. Sinaliza `hurtMarked` e zera `fallDistance`.
- **Block velocity:** sem Sensitive percorre `SpellUtil.calcAOEBlocks` e cria `EnchantedFallingBlock.fall`; no sucesso, soma componente vertical `(GENERIC_DOUBLE*0.6)+AMP_VALUE*ampMultiplier` (default base 0.48 + amp*0.25), distinto do valor aplicado à entidade viva; propaga ShapersFocus. Sensitive aborta esse ramo.
- **Perks:** movimento de entidade, mutação de bloco e prevenção de queda têm resultados separados; não duplicar execução de `EnchantedFallingBlock` e requerer QoS de world effects em magias Black Arcana.
- **Estado:** ✅ origem e lógica source-pinned; ⚠️ helpers, itens externos e runtime QA pendentes; ⛔ adapter de perks do RPG sem teste nem contrato para duplo settlement. Ars conserva mana, inventário e efeitos.

## Auditoria de contrato estático — mobilidade e controle (25/10/2026)

**✅ Contrato técnico source-pinned completo desta ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A marca ✅ aqui é de documentação estática, não de comportamento comprovado no cliente ou integração executável.

| Campo necessário à perk | Comportamento real no source fixo e condicionamentos |
|---|---|
| Identidade | Ars Nouveau `5.13.1`, `ars_nouveau:glyph_launch`, classe `EffectLaunch`, escola Elemental Air, tier I. [Fonte exata](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLaunch.java), [IDs binários SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, causalidade e recebedor | `onResolveEntity` soma ao delta anterior apenas `(0,base+ampScalar×ampMultiplier,0)`, marca `hurtMarked` e zera `fallDistance`, sem verificar se o alvo é LivingEntity. Ramo de bloco com Sensitive aborta; sem Sensitive usa `SpellUtil.calcAOEBlocks`, `EnchantedFallingBlock.fall`, soma delta Y do bloco e chama `ShapersFocus.tryPropagateEntitySpell` após conversão bem-sucedida. |
| Parâmetros, fórmulas e caps | Defaults `base=0,8`, `ampScalar=0,25`. **Entidade**: ΔY=0,8+0,25×ampMultiplier. **Bloco convertido**: ΔY=0,8×0,6+0,25×ampMultiplier=0,48+0,25×ampMultiplier. Ambos são aditivos à velocidade existente; nenhum clamp de sinal nesta classe. Amplify, Dampen, AOE, Pierce e Sensitive compatíveis; Sensitive cap default 1. |
| Alvo/target, geometria, projétil, dano e duração | `EntityHitResult` altera entidade atingida; `BlockHitResult` pode transformar blocos em `EnchantedFallingBlock` e dar impulso vertical. AOE/Pierce só expandem o conjunto de posições do ramo de bloco. Não há DamageType, raio de impacto, vida de projétil ou duração configurada neste Effect. |
| Custos, aprendizado e cooldown | Mana default **30**, tier I, recipe default `ars_nouveau:air_essence` + `minecraft:rabbit_hide` ×3, XP default **27**, starter default **não**. [Acquisition compilada 85/85](../../ACQUISITION.md). Custo final/cooldown/consumidor da magia composta continuam no Ars. |
| Integração/authority | Nunca transformar um único evento de Launch com vários falling blocks em vários casts/ganhos de XP. Checagem de blocos, chunk, claims, entidade gerada e rollback dependem do executor e QA real; não afirmar que `WorldEffectPolicy` do Black Arcana governa implicitamente o Ars. O RPG Skill Tree fornece perks/progressão mas não assume o `SpellResolver` Ars; Black Arcana só controla seu casting, world policy e riscos internos. APIs de mutação externa não estão comprovadas para este ramo. |
| Validação/proveniência | `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID e classe de registro**, não equivalência de todo classfile/source. Config efetiva, edge-cases, claims, multiplayer e modpack QA **NOT_TESTED**. |

**Gate explícito:** alteração de versão/config, eventos, claims, targeting ou vector motion exige revalidação. Sem Mastery por packet/partícula/tick ou bloco secundário; sem segunda mana, reexecução de efeitos ou Stage promovido.
