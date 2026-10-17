# Ars Portals on moving contraptions

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Ars Creo registers movement + collision behavior for the existing Ars Nouveau Portal Block and marks Portal/Ritual blocks movement-allowed through Create's movement check.

Portal destination data is reconstructed from stored NBT (`warp`, dimension id, rotation/display/horizontal fields). Entity transfer delegates to Ars `PortalTile.teleportEntityTo` rather than implementing a second teleport engine.

The behavior ignores the contraption entity itself and processes entities occupying the moving portal cell through tick/new-position and moving-collision paths.

This proves moving Ars portal support, not Black Arcana displacement authorization. Cross-dimensional safety, claims and full-pack portal-addon interaction remain runtime QA.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** mod ID `ars_creo`, JAR instalado documentado `ars_creo-1.21.1-5.4.0.jar`, SHA-1 `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Código da versão `5.4.0`: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2` (**SOURCE_CAUSALITY**, sem equivalência binária completa nem QA do pack). Hosts: Ars Nouveau `5.13.1`, Create `6.0.10`. **Ars Creo não registra glyph próprio: +0 IDs novos.**

**Portais móveis — teleporte e status** — efeito do provider externo/integração Create, não nova raiz mágica.

| Eixo | Mecanismo no source pinado | Limite de perk |
|---|---|---|
| Destino/state | PortalData é recriado do NBT de movimento: `warp` BlockPos, `dim` string, `xRot/yRot` float, `display` e `horizontal`; guarda um `HashSet<Entity>` local não usado para dedup explícito no método auditado. | Não transformar informação de destino em target validado de Black Arcana; dimensões/claims provider-owned. |
| Scan e trigger | visitNewPosition consulta entidades em `new AABB(pos)`; tick consulta `new AABB(BlockPos.containing(context.position))`, ambos somente servidor, e colisão também chama `PortalBehavior.handleEntity`. Não há intervalo de cooldown explícito em handleEntity. | Risco potencial de ações repetidas em vários callbacks; validar com contador observado, não inferir recast seguro. |
| Filtro | Ignora exatamente a entidade da própria contraption; as demais passam à tentativa de teleport sem filtro player/mob no corpo da bridge. | Atributos/target type de perk não alteram quem entra no portal sem hook de PortalTile. |
| Teleport | Se server, `warpPos != null`, `dimID != null`, chama `PortalTile.teleportEntityTo(entity, getServerLevel(dim),warpPos,rotationVec)`; somente sucesso não-null aciona som e partículas. Não mede sucesso via evento BA. | Sem segundo `teleportEntity` ou Mastery apenas por contato AABB. |
| FallDistance e nulidade | `entity.fallDistance=0` executa ao sair do método independentemente de a tentativa de teleporte ter retornado sucesso; `getServerLevel(dimID)` é passada à operação de host antes do guard `serverWorld==null` pós-sucesso. Ambos são **achados de fluxo source**, não bugs em jogo comprovados. | ⚠️ QA contato sem destino/resolver dimension inválida, atravessamento sem teleporte, fall damage; fail-closed. |

**Âncoras verificáveis:** [PortalBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/PortalBehavior.java#L26-L89) · [PortalMovingInteraction.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/PortalMovingInteraction.java#L9-L18) · [CreateCompat.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/CreateCompat.java#L38-L48).

**Aceitação pendente:** Cross-dimension (destino válido, missing, dimensão descarregada), jogadores/animais/projéteis, portal parado e atravessamento múltiplo, duplicates tick+collision, claims/proteção, fallDistance antes/depois, retry após cancelamento, reload e portal de outro addon. O RPG Skill Tree não controla o runtime Ars/Create. **0 adapters homologados, +0 IDs de magia.**
