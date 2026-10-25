# Blink

- Registry ID: `ars_nouveau:glyph_blink`
- Source class: `EffectBlink`
- School: Manipulation
- Default tier: **3**
- Default mana: **50**
- Default distance config: **8** + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Blink supports several Ars-owned teleport paths. Self use attempts a forward teleport with safe-space checks. Entity use can consume Warp Scroll location data from the caster context/offhand, including dimension-aware provider warping where the stored data permits it. Turret/Rune caster contexts can source Warp Scroll data from adjacent inventory behavior. Entities tagged as not supporting teleport are rejected, and Ender-style teleport events can veto relevant warp paths.

Compatible augments: Amplify, Dampen.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `#c:ender_pearls` ×4.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Blink/Warp Scroll/portal teleport semantics. Black Arcana must not duplicate generic Blink/Warp ownership; any Black Arcana displacement remains server-validated under its destination-recovery, protection and loaded-chunk contracts.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectBlink.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBlink.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectBlink` no Ars 5.13.1, método `onResolveEntity`.
- **Alcance self:** `GENERIC_INT.get()+AMP_VALUE.get()*ampMultiplier`, defaults 8 e 3.0; `blinkForward` procura destino horizontal e `isValidTeleport` exige três posições verticais não-oclusivas. **Alvos:** rejeita tag `TELEPORTING_NOT_SUPPORTED`; `TileCaster` tenta Warp Scroll do inventário; self usa `blinkForward`; player real pode warp outro alvo com scroll na offhand ou, sem scroll, teletransportar o **caster** ao hit; Rune tem ramo próprio. **Teleport:** `warpEntity` usa `EventHooks.onEnderTeleport` cancelável para LivingEntity e `PortalTile` para resolução de dimensão; as admissões completas são provider-owned. **Perks:** alcance self não é permissão para warp interdimensional ou terceiros.
- **Limite de integração:** ✅ fonte estática identificada; ⚠️ parâmetros condicionados à configuração carregada; ⛔ nenhum hook externo de mutação verificado. Mana, targeting e settlement pertencem a Ars; RPG Skill Tree não substitui o resolver. Gameplay/Survival e adapter real: PENDING.

## Auditoria de contrato estático — mobilidade e controle (25/10/2026)

**✅ Contrato técnico source-pinned completo desta ficha; ⛔ hook mutador de perks `NOT_VERIFIED`; ⚠️ QA físico `NOT_TESTED`.** A marca ✅ aqui é de documentação estática, não de comportamento comprovado no cliente ou integração executável.

| Campo necessário à perk | Comportamento real no source fixo e condicionamentos |
|---|---|
| Identidade | Ars Nouveau `5.13.1`, `ars_nouveau:glyph_blink`, classe `EffectBlink`, escola Manipulation, tier III. [Fonte exata](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBlink.java), [IDs binários SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, causalidade e recebedor | `onResolveEntity` recusa entidades tagueadas `TELEPORTING_NOT_SUPPORTED`, calcula `distance=GENERIC_INT+AMP_VALUE*getAmpMultiplier()`, e distingue `TileCaster` com Warp Scroll de inventário, self, jogador real com scroll na offhand, jogador sem scroll e `CasterType.RUNE`. No ramo self executa `blinkForward`; `onResolveBlock` tenta `warpEntity(shooter,...)` apenas após `isValidTeleport` no bloco adjacente. `warpEntity` com Warp Scroll usa `PortalTile.getServerLevel` e `PortalTile.teleportEntityTo`; os overloads próprios não são idênticos. |
| Parâmetros, fórmulas e caps | Defaults source-config **distância 8 + 3,0×amp**; apenas Amplify/Dampen compatíveis. `blinkForward` usa vetor horizontal do olhar e procura uma posição que não oclua `pos`, `pos.above()` e `pos.above(2)`. `getForward` faz uma busca pelo espaço com loop `i` de `distance` a `0`, partindo de um `oldVec` já deslocado por `distance`; **não assumir que a busca representa limite radial uniforme**, nem que a checagem de oclusão prova chunks carregados, claims, colisão total ou segurança para entidades grandes. A geometria do Warp Scroll segue as coordenadas do item, não esta fórmula de distância. |
| Alvo/target, geometria, projétil, dano e duração | `EntityHitResult` permite self/caster e outras entidades apenas nos ramos apropriados; para player real sem scroll, a implementação `teleportTo` do **caster** à coordenada do hit não é um warp gratuito do alvo. `BlockHitResult` tem fluxo próprio; Rune e turret têm caminhos próprios. Sem projétil, dano ou AoE intrínsecos. Teleporte entre dimensões depende de `WarpScrollData.canTeleportWithDim` e `PortalTile`. |
| Custos, aprendizado e cooldown | Mana default **50**, tier III, recipe default `ars_nouveau:manipulation_essence` + `#c:ender_pearls` ×4, XP default **160**, starter default **não**. [Acquisition compilada 85/85](../../ACQUISITION.md). Custo final/cooldown/consumidor da magia composta continuam no Ars. |
| Integração/authority | `EventHooks.onEnderTeleport` pode cancelar warps com `LivingEntity`, mas `blinkForward`, scroll e overload de bloco não devem ser equiparados a um hook único de perks. Nunca bypassar restrições de viagem, anti-cheat, permissionamento ou world safety do provider, nem reexecutar teleporte após falha; `SpellResolver` e pagamento continuam Ars-owned. O RPG Skill Tree fornece perks/progressão mas não assume o `SpellResolver` Ars; Black Arcana só controla seu casting, world policy e riscos internos. APIs de mutação externa não estão comprovadas para este ramo. |
| Validação/proveniência | `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID e classe de registro**, não equivalência de todo classfile/source. Config efetiva, edge-cases, claims, multiplayer e modpack QA **NOT_TESTED**. |

**Gate explícito:** alteração de versão/config, eventos, claims, targeting ou vector motion exige revalidação. Sem Mastery por packet/partícula/tick ou bloco secundário; sem segunda mana, reexecução de efeitos ou Stage promovido.
