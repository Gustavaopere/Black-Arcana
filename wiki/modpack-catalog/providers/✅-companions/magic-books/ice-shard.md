# Ice Shard Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_ice_shard`, `dev.xylonity.companions.common.item.book.books.IceShardBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_ice_shard`
- Concrete class: `IceShardBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **180 ticks**
- Source-level survival acquisition: **Overworld Minion + Copper Coin random reward**

## Action surface

launches the provider ice-shard projectile from the caster; the projectile receives the caster's recent combat target hint when available.

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

## Engenharia causal para perks — Ice Shard (source pin 1.3.4, 17/10/2026)

**Estado:** `SOURCE-CAUSALITY` no código oficial `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`. A prova física do `companions:book_ice_shard` confirma a classe/identidade, **não** os resultados de dano congelante desses projéteis; engine host e cliente pendentes.

| Eixo | Fato causal verificado | Perks e restrição |
|---|---|---|
| Ingresso / spawn | `IceShardBook.use` somente server cria **um BigIceShardProjectile** acima e lateral ao player, escala posicionamento 0,5 para right/up, escolhe direção inicial num cone de **30°** e velocidade **0,2 bloco/tick**; anexa owner. Pega como hint `getLastHurtByMob` ou `getLastHurtMob`, não retarget livre. | `SEM_HOOK_SEGURO` para velocidade, cone ou mudança de alvo por perk. |
| Fase grande / fan-out | `BigIceShardProjectile.tick` desliga gravidade, reduz velocidade por fator **0,95** até o tick **25**; neste tick tenta criar **5 SmallIceShardProjectile**, herdando owner e target sugerido, ou executa seleção de entidade no olhar **até 64 blocos**; sem alvo, pequenos seguem olhar do dono em dispersão aleatória de **8°** e velocidade inicial **0,4**. 5 projéteis filhos **não** são 5 casts. | `SEM_HOOK_SEGURO` para quantidade, targeting, lifetime e fan-out. A atribuição de dano precisa propagar owner/cast sem duplicação. |
| Small shard / homing | Em SmallIceShardProjectile: fase inicial de **20 ticks** fricção **0,95**; depois, velocidade com fricção **0,88** e aceleração **0,04** na direção do alvo ou do olhar atual do dono. Descarte explícito no tick **200** se não colidir antes. | `NÃO_VERIFICADO` hook para acceleration/turn rate/range ou limites de reaquisição. |
| Dano/tipo/status | No `SmallIceShardProjectile.onHit` de entidade, chama `hurt(indirectMagic(shard, owner), SMALL_ICE_SHARD_DAMAGE)` (default **2,5**) e então adiciona **100 ticks** de `setTicksFrozen` pelo default, **sem conferir `hurt` retornado**. Isso é um freeze por incremento no source, não prova de aplicação efetiva/PvP. | `CONFIG_NATIVE` dano e freeze globais; **⛔** perk de dano/elemento/freeze sem settlement seguro. |
| Sidedness | Fan-out do BigIceShard no tick 25 está fora de `!level.isClientSide` no corpo examinado; partículas e evento 3 têm branches client/server. Um eventual spawn no cliente não prova duas entidades autoritativas no servidor. | QA client/server obrigatório, sem perks client-owned. |
| Cooldown/custo | Default `ICE_SHARD_COOLDOWN=180 ticks`; reduz em `peças Mage × 0,15`. O livro não mostra débito direto de mana; não criar segundo recurso. | `CONFIG_NATIVE` global, adapter per-player não homologado. |

Âncoras: [IceShardBook.java](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/IceShardBook.java#L29-L76) · [BigIceShardProjectile.java — fases e 5 filhos](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/BigIceShardProjectile.java#L76-L139) · [SmallIceShardProjectile.java — homing](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/SmallIceShardProjectile.java#L67-L126) e [hit/freeze](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/SmallIceShardProjectile.java#L153-L181) · [config dano/freeze](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L727-L739) e [cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L776-L781).

**QA:** contador de cinco filhos em servidor único; owner e client ghost, direção alterada entre charge e fase 2, alvo depois de logout, perda de alvo/dimensão, dano cancelado seguido de `setTicksFrozen`, caps PvP, team check e Mastery por hit efetivo com dedup do cast pai. Nenhum hook de `DamageType` ou de transformação elemental foi demonstrado. **+0 raízes.**
