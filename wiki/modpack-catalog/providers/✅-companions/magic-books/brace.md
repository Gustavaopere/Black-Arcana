# Brace Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_brace`, `dev.xylonity.companions.common.item.book.books.BraceBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_brace`
- Concrete class: `BraceBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **160 ticks**
- Source-level survival acquisition: **Nether Minion + Nether Coin random reward**

## Action surface

launches the provider Brace projectile along the caster's look direction.

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

## Engenharia causal para perks — Brace (source pin 1.3.4, 17/10/2026)

**Estado:** `SOURCE-CAUSALITY` de `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`. `companions:book_brace` permanece uma raiz provider-native; múltiplos rebotes são etapas da mesma execução, não magias novas.

| Eixo | Mecanismo observado | Situação da perk |
|---|---|---|
| Ingresso/velocidade | `BraceBook.use` server-only cria um `BraceProjectile` em **eyePos + 0,3×look**, owner player, velocidade inicial **0,75×look + velocidade do player**. Erro de factory ainda aplica cooldown. | `SEM_HOOK_SEGURO` para speed, tamanho, spawn e direção por personagem. |
| Movimento/colisão | `BraceProjectile.tick` usa gravidade por tick **0,03** e multiplicador de velocidade **0,98**. Compara distância de entity hit e block hit, toma a colisão mais próxima e executa movimento ou reflexão. Fonte possui nota de TODO sobre blocks não detectados consistentemente: **hipótese upstream**, não bug reproduzido. | `NÃO_VERIFICADO` extensão segura no resolvedor de colisão. |
| Alvo/chain | Primeiro hit em `LivingEntity` válida usa `!Util.areEntitiesLinked` e `hitEntities` para impedir repetição do mesmo **entity ID por projectile**. Após hit, procura a próxima `LivingEntity` viva e mais próxima numa AABB `inflate(10)`; até **5 impactos de entidades** (MAX_BOUNCES). `hitEntities` é lista local de IDs, persistência não demonstrada. | `SEM_HOOK_SEGURO` para salto/target/radius; não multiplicar Mastery por bounce sem confirmação de damage. |
| Dano/status | `hurt(indirectMagic(projectile, owner), BRACE_PROJECTILE_DAMAGE)` (default **4.0**) e `igniteForSeconds` com sorteio **1..9 s**, **sem checar resultado de `hurt`** antes do ignite/contador de impactos. Isso condiciona perks de burning/on-hit a QA de dano efetivo. | `CONFIG_NATIVE` dano global; damage type e status per-player `⛔` sem seam. |
| Block bounce | Faces verticais da colisão são refletidas com damping vertical **0,6**, e faces laterais com damping horizontal **0,7**. `blockBounces` chega a 5 e zera velocidade refletida, mas **não é o mesmo contador** que `entityBounces` usado para descarte antecipado; lifetime ainda se aplica. | `SEM_HOOK_SEGURO` para duração/rebotes; verificar colisão em cantos e travamento. |
| Lifecycle | `baseLifetime()=200 ticks`; terminação se `tickCount > getLifetime()` ou `entityBounces >= 5`. `handleEntityHit` também descarta quando não há próximo alvo. O body do `tick` não contém um guard server-only geral, logo sidedness e sincronismo pendem de teste. | `NÃO_VERIFICADO` QA per-game-tick, reload e dedup. |
| Cooldown | Default `BRACE_COOLDOWN=160 ticks`, descontado por contagem de peças Mage × 0,15. Não há débito explícito de mana no `use`. | `CONFIG_NATIVE` global, `SEM_HOOK_SEGURO` per-player. |

Âncoras: [BraceBook.java — 24–56](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/BraceBook.java#L24-L56) · [BraceProjectile.java — física e interseções](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/BraceProjectile.java#L33-L95) · [hit/chain](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/BraceProjectile.java#L99-L161) · [block bounce e descarte](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/BraceProjectile.java#L166-L229) · [config cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L755-L760) e [damage](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L935-L940).

**QA prioritário:** exatamente-once de dano real, alvo descartado antes de `hurt`, efeitos em i-frames/cancelamento, team/owner, cinco entity bounces vs cinco block bounces, chunk unload/respawn com ID reciclado, speed herdada do player, client/server e possível bypass por raio de aquisição ao longo da cadeia. Não criar cinco ações mágicas pela cadeia do mesmo projectile. **+0 identidade mágica e +0 adapters.**
