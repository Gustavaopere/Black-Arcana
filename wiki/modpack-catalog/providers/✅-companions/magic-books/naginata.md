# Naginata Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_naginata`, `dev.xylonity.companions.common.item.book.books.NaginataBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_naginata`
- Concrete class: `NaginataBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **140 ticks**
- Source-level survival acquisition: **dedicated provider recipe**

## Action surface

targets along the player's look trace and calls down provider naginata projectiles; crouch input changes the firing pattern without minting a second action identity.

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

## Engenharia causal para perks — Naginata (source pin 1.3.4, 17/10/2026)

**Evidência:** leitura da fonte pública `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`. `COUNTED_EXACT` do JAR físico valida a identidade da Magic Book, não equivalência byte-a-byte dos auxiliares nem o resultado de ataque em servidor.

### Matriz por eixo

| Eixo | Fato source-pinned | Status de hook |
|---|---|---|
| Ingresso / alvo inicial | `NaginataBook.use` somente server; **80 blocos** de projeção do olhar, AABB de seleção de entity `inflate(2.0)`, filtro `!Util.areEntitiesLinked`. Tenta `ProjectileUtil.getEntityHitResult` primeiro; **apenas se não encontrar entidade** faz raycast de bloco `ClipContext.Block.COLLIDER`. Se ambos falham, **nenhuma naginata é criada**, mas o cooldown ainda é aplicado. | `SEM_HOOK_SEGURO` para aumentar range, redirecionar ou converter single-target em AOE. `inflate(2.0)` da consulta não é hitbox da naginata. |
| Seleção e obstáculos | Havendo entityHit, usa posição da entidade sem uma checagem local subsequente de bloco no mesmo ramo. **Risco hipotético** de adquirir alvo atrás de obstáculo, dependente de como `ProjectileUtil` resolve o segmento e candidatos; não afirmar exploit sem teste. | `NÃO_VERIFICADO` LOS seguro como boundary de perks. |
| Modo sem crouch | Invoca até **6** `HolinessNaginataProjectile` a partir de origem **20–30 blocos acima do alvo**, offsets X/Z aleatórios no intervalo aproximado **±15 blocos**, velocidade inicial **1,5–2,0 blocos/tick** em direção ao target. | `SEM_HOOK_SEGURO` para alterar número de projéteis, spread, velocidade, altitude e limite de fan-out. |
| Modo crouch | Invoca até **2** projéteis, offsets X/Z **±10 blocos**, mesma faixa de altitude e velocidade fixa **3,35 blocos/tick**; é **variante da mesma raiz mágica**, não um segundo spell ID. | `SEM_HOOK_SEGURO` para modificar padrão por perk sem novo boundary provider. |
| Dano/tipo | `HolinessNaginataProjectile.onHitEntity` usa `damageSources().indirectMagic(projectile, owner ou projectile)` com config default `NAGINATA_DAMAGE=8`. Marca `dealtDamage=true` **antes** de chamar `hurt`; `findHitEntity` suprime hits posteriores se já marcado. Não houve prova de dano aceito em entidade, nem de cap por cast. | `CONFIG_NATIVE` dano global; perk individual por evento/settlement é `NÃO_VERIFICADO`; não aplicar Mastery ao simples spawn. |
| Colisão/visual | Classe herda `ThrownTrident`. `getBoundingBoxForCulling().inflate(10)` afeta **culling visual**, não comprova aumento da AABB física de hit. `setInvisible(true)` no spawn, alternância de visibilidade nos primeiros ticks. | `N/A` para interpretar culling como hitbox; **SEM_HOOK_SEGURO** para dimensão de colisão. |
| Lifecycle | `tickDespawn` descarta quando `inGroundTime >= timeToDespawn`; `timeToDespawn` é sorteado server-side **120–299 ticks** no construtor. Sem prova nesta ficha de persistência do contador entre save/reload ou contagem de ticks em voo. | `NÃO_VERIFICADO` durabilidade/cleanup de entidade/reload. |
| Cooldown/custo | Default `NAGINATA_COOLDOWN=140 ticks`; reduz em função da **contagem de peças Mage**, com default 0,15 por peça; ausência de pagamento explícito de mana no corpo do livro não prova que o modpack não modifica recursos. | `CONFIG_NATIVE` valores globais; `SEM_HOOK_SEGURO` cooldown per-caster. |

### Fontes, testes e limites

- [NaginataBook.java — 44–71](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/NaginataBook.java#L44-L71): targeting, range, cooldown e fallback de bloco; [padrões — 76–108](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/NaginataBook.java#L76-L108): spread/quantidade/velocidade. A factory pode falhar e produzir menos projéteis; os números acima são tentativas de spawn.
- [HolinessNaginataProjectile.java — 40–69](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/HolinessNaginataProjectile.java#L40-L69) e [impacto — 123–136](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/HolinessNaginataProjectile.java#L123-L136): owner-linked filtering, culling, despawn e dano, sem double-hit por projétil no caminho `dealtDamage`.
- [CompanionsConfig.java — cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L748-L753) e [NAGINATA_DAMAGE](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L900-L905); [Util.hasFullSetOn](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/util/Util.java#L260-L274): defaults e contador de armor pieces.
  
**QA prioritário:** alvo entre mob e parede; entidade vista atrás de bloco; modo crouch vs normal; seis impactos coincidentes e invulnerability frames; cancelamento de `hurt`, PvP/party/owner-chain, spawn em chunks não carregados, efeitos de unload/restart, teto Y, dispersão e lag, além de atribuição de Mastery no hit realmente aceito. Não transformar seis projectiles em seis casts independentes nem impor policy Black Arcana em provider externo. **+0 IDs; integração RPG ⛔.**
