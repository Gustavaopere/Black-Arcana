# Fire Mark Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_fire_mark`, `dev.xylonity.companions.common.item.book.books.FireMarkBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_fire_mark`
- Concrete class: `FireMarkBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **140 ticks**
- Source-level survival acquisition: **Nether Minion + Nether Coin random reward**

## Action surface

places a provider Fire Mark ring at a looked-at block within the source-defined trace range, with caster-position fallback.

## Registration closure

The exact 1.3.4 source pin registers this item directly in `CompanionsItems` as a concrete `AbstractMagicBook` subclass. No mod-presence/config branch around the nine Magic Book registrations was found.

## Acquisition boundary

The route above is closed at source/catalog level. Effective assembled-pack loot, recipe/datapack mutation, probabilities and deployed config remain runtime QA.

## Soul Mage deduplication

Soul Mage can consume/equip the same Magic Book identity. Its AI goal reuses this action and does not mint a second semantic object.

## Authority boundary

Companions! remains authority for activation, cooldown/config settlement and any projectile/effect/state created by this action. Black Arcana must not replay the provider's damage, healing, summon/projectile or cooldown settlement.

## Evidence boundary

The source-default cooldown and action description are factual metadata from the pinned provider inventory, not deployed-pack measurements. Runtime attribution, protection behavior, multiplayer behavior and lifecycle remain separate QA.

Source: `../SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md`.

## Engenharia causal para perks — Fire Mark (fonte 1.3.4, 17/10/2026)

**Estado da prova:** `SOURCE-CAUSALITY` em `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`; o JAR físico valida identidade estática, não execução desses auxiliares. `FIRE_MARK_RING_PROJECTILE` é efeito filho, **não** um décimo Magic Book.

| Eixo | Parâmetro e cadeia verificados no código-fonte | Mutabilidade por perk |
|---|---|---|
| Targeting / range | `FireMarkBook.use` faz raycast de **blocos** `COLLIDER` sem fluidos até **50 blocos**. Se houver bloco atingido e posição dentro de 50 blocos do olho, tenta colocar o anel no centro X/Z do bloco e Y+1. Sem sucesso, faz **fallback na posição do caster**. Não é target entity, nem AOE centrada no primeiro mob. | `SEM_HOOK_SEGURO` para redirecionar, aumentar alcance ou trocar bloco por entity. |
| Lado de execução | Criação do `FireMarkRingProjectile` ocorre **fora do guard server-only** no próprio `use`; o guard `!isClientSide` abrange somente cooldown. Entity spawn client+server, duplicações visuais/transitórias e event forwarding exigem QA em cliente real. | `NÃO_VERIFICADO` como ponto de cast autoritativo externo. |
| Área e frequência | `FireMarkRingProjectile.tick` consulta, **server-only**, entidades em AABB X/Z **±RADIUS**, Y **±1**. Config default `FIRE_MARK_EFFECT_RADIUS=2.5`, mas campo `RADIUS` é avaliado no construtor da entidade; não é distância esférica. Verifica `!Util.areEntitiesLinked`; aplica `FIRE_MARK` apenas se alvo ainda não tem o efeito. | `CONFIG_NATIVE` para raio global; sem hook per-caster validado. |
| Duração/status | Debuff `FIRE_MARK` com duração aleatória **100..399 ticks**, amplifier 0, e `baseLifetime()=30 ticks` no anel; a repetição em ticks não gera uma magia nova nem garante novo efeito em alvo já marcado. `FireMarkProjectile` separado é componente visual que segue portador com esse efeito; não é a entidade criada diretamente pelo livro. | `SEM_HOOK_SEGURO` para duração/amplificador e geração de marca secundária. |
| Cooldown/custos | Default `FIRE_MARK_COOLDOWN=140 ticks`, reduzido por **número de peças Mage** × 0,15 cada; sem mana/XP diretamente debitados no corpo do livro examinado. | `CONFIG_NATIVE` para valores globais; `NÃO_VERIFICADO` preço de runtime por outros handlers. |
| Dano/tipo | O anel aplica status no método examinado, sem `hurt` direto. Danos associados ao status e demais processos devem ser rastreados no handler do efeito, não imputados ao cast inicial. | `NÃO_VERIFICADO` dano downstream; sem converter tipo de dano neste hook. |

Âncoras: [FireMarkBook.java](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/FireMarkBook.java#L29-L68) · [FireMarkRingProjectile.java](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/FireMarkRingProjectile.java#L22-L56) · [FireMarkProjectile.java](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/FireMarkProjectile.java#L26-L64) · [config raio](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L699-L704) · [config cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L762-L767).

**QA priorizado:** observar spawn client/server e fallback de raycast sem bloco; checar verticalidade da área, recast, alvos protegidos, refresh do status, descarga de chunk, configuração efetiva e aplicação downstream de `FIRE_MARK`. Não premiar Mastery a cada tick do anel. **+0 identidades novas, +0 adapters.**
