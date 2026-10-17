# Ice Tornado Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_ice_tornado`, `dev.xylonity.companions.common.item.book.books.IceTornadoBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_ice_tornado`
- Concrete class: `IceTornadoBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **200 ticks**
- Source-level survival acquisition: **Overworld Minion + Copper Coin random reward**

## Action surface

summons the provider tornado projectile immediately ahead of the caster.

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

## Engenharia causal para perks — Ice Tornado (source pin 1.3.4, 17/10/2026)

**Estado:** `SOURCE-CAUSALITY` no commit `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`, sem prova do efeito no runtime integrado. Identidade `companions:book_ice_tornado` já era contada uma vez.

| Eixo | Implementação observada | Estado de integração |
|---|---|---|
| Cast / spawn | `IceTornadoBook.use` server-only cria um `TornadoProjectile` ao nível Y do caster, deslocado **1 bloco** na direção **horizontal normalizada** de olhar; atribui owner e aplica cooldown mesmo em falha da factory. | `SEM_HOOK_SEGURO` para cast ou spawn de múltiplos tornados. |
| Movimento | Tornado inicializa `GROUNDY/STARTX/STARTZ/ALPHA` em synced data; no tick, muda X/Z com trajetória paramétrica dependente de `t=tickCount×0,2`, mantém altura base `GROUNDY`. Sua direção/curva não é um simples projétil em linha reta. | `SEM_HOOK_SEGURO` para velocidade/direção e range sem modificar provider. |
| Área/target | A cada tick examina `Entity` numa `getBoundingBox().inflate(1)` (AABB, não esfera), exclui entidades vinculadas usando `Util.areEntitiesLinked`, aplica push na direção para fora, módulo parametrizado por **1,4** com pequeno offset e tenta `indirectMagic` em `LivingEntity`. | `SEM_HOOK_SEGURO` para hitbox, máximo de alvos e hit interval; Mastery por `hurt` realmente aceito. |
| Dano/tipo | Config default `ICE_TORNADO_DAMAGE=3.0` em cada tentativa de dano por tick. Não há verificação local de sucesso em `hurt` antes de empurrar; Knockback/push não garante damage. | `CONFIG_NATIVE` dano global; nenhum hook de type conversion ou cap por jogador validado. |
| Lifetime/collisions | `baseLifetime()=120 ticks`; `onHit` ignora colisão com face superior/inferior de bloco, demais podem remover entidade; onExpire chama discard. Lógica de push/hurt está no método `tick` sem guard local server-only, portanto sidedness necessita QA. | `NÃO_VERIFICADO` paridade client/server, cancelamentos, unloaded chunk e persistência. |
| Cooldown/custo | Default `ICE_TORNADO_COOLDOWN=200 ticks`, redução per-piece Mage (0,15 por peça default), sem mana cobrada nesse body. | `CONFIG_NATIVE` global, perk por jogador `⛔`. |

Âncoras: [IceTornadoBook.java](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/IceTornadoBook.java#L26-L50) · [TornadoProjectile.java — fields/tick](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/TornadoProjectile.java#L32-L150) · [colisões/lifetime](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/TornadoProjectile.java#L169-L216) · [config dano](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L685-L690) · [cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L783-L788) · [owner-chain exclusions](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/util/Util.java#L187-L200).

**QA:** testar empurrão sem dano (i-frames, cancelamento), owner e aliados, vários alvos em AABB, AABB exposto a paredes e faces de blocos, corner collision, cliente/servidor, dois tornados simultâneos, spawn sem direção horizontal e performance em entidades numerosas. Não somar tick damage como novo cast ou Mastery genérica. **+0 IDs e adapters.**
