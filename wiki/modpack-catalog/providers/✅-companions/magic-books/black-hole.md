# Black Hole Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_black_hole`, `dev.xylonity.companions.common.item.book.books.BlackHoleBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_black_hole`
- Concrete class: `BlackHoleBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **160 ticks**
- Source-level survival acquisition: **provider injection into vanilla chest-table loot**

## Action surface

launches the provider black-hole projectile forward from the caster.

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

## Engenharia causal para perks — Black Hole (source pin 1.3.4, 17/10/2026)

**Evidência:** `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f` lido diretamente. JAR 1.3.4 SHA idêntico ao catálogo **para a identidade**; os valores auxiliares são `SOURCE-CAUSALITY` e ainda exigem confrontação binária/QA com KnightLib 2.0.1.

### Matriz por eixo

| Eixo | Comportamento observado | Mutabilidade por RPG |
|---|---|---|
| Ingresso | `BlackHoleBook.use`, apenas server, cria `BLACK_HOLE_PROJECTILE`, posição olho + **0,5 bloco** no olhar, owner player e `shootFromRotation(..., 0.8f, 0)`. Aplica cooldown mesmo quando a factory retorna `null` — branch de fonte, não falha de jogo reproduzida. | `SEM_HOOK_SEGURO` para alterações de spawn/velocidade, que requerem ABI e autorização do provider. |
| Movimento / tempo | Projectile inicia com `GRAVITY=0.03f`, amortecimento da velocidade **0,99** por tick; trava em colisão de bloco, contato com solo ou `tickCount >= 20`. Depois mantém velocidade zero e continua atração. `baseLifetime()` retorna **100 ticks**, sujeito ao settlement herdado de KnightLib. | `SEM_HOOK_SEGURO` para duration, launch speed ou posição de travamento. |
| Área / alvos | Busca `LivingEntity` numa **AABB ampliada** pelo `ATTRACT_RADIUS`; default **12 blocos**. Exclusão por `Util.areEntitiesLinked` (mesmo owner-chain/equipe). Não há teste explícito de LOS ou claims nesse método. A busca AABB é ampla, mas o cálculo de força zera para distância maior/igual ao raio. | `CONFIG_NATIVE` do raio global; `SEM_HOOK_SEGURO` para ampliar por caster ou modificar política de facção. |
| Força / periodicidade | A cada tick de atração, calcula `linear=max(0,(R-dist)/R)`, velocidade desejada `normalize(toCenter) × linear² × BLACK_HOLE_ATTRACTION_SPEED`, e interpola velocidade da entidade com fator **0,15**; speed default **1,45**. O source executa essa rotina também sem um gate server-only dentro de `attractNearbyEntities`; authority de física/client precisa prova. | `CONFIG_NATIVE` para velocidade global; nenhum seam per-player validado. |
| Dano/tipo/status | No método desta classe, atração altera movimento; **não há chamada `hurt` direta**. Pode haver consequências ambientais não verificadas, mas não se deve calcular XP/Mastery por dano imaginado de Black Hole. | `N/A` para damage multiplier direto desse efeito; dano indireto em gameplay é `NÃO_VERIFICADO`. |
| Cooldown/custos | Default `BLACK_HOLE_COOLDOWN=160 ticks`. Aplicação com redução por **número de peças Mage** × `MAGE_SET_COOLDOWN_REDUCTION=0,15` por peça. Nenhuma cobrança explícita de mana no `use` examinado. | `CONFIG_NATIVE` global; sem substituição ou cobrança paralela de recursos. |
| Config/lifecycle | `ATTRACT_RADIUS` é um **static final** inicializado a partir da config na inicialização da classe; não afirmar que reload de config atualiza o raio de entidades/classes já carregadas. `TICKCOUNT` sincronizado começa em 0 e `getTickCount()` é distinto de `Entity.tickCount`; seu avanço deve ser comprovado no lifecycle completo. | `NÃO_VERIFICADO` hot reload, persistência, client parity e owner. |

### Âncoras e QA

- [BlackHoleBook.java — 24–50](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/BlackHoleBook.java#L24-L50): spawn, owner, velocidade e cooldown.
- [BlackHoleProjectile.java — 36–70](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/BlackHoleProjectile.java#L36-L70), [tick/movimento — 74–154](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/BlackHoleProjectile.java#L74-L154) e [atração/lifetime — 156–186](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/BlackHoleProjectile.java#L156-L186): campos sincronizados, travamento, curva e filtragem.
- [CompanionsConfig.java — radius/speed](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L713-L725) e [cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L741-L746); [Util.areEntitiesLinked](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/util/Util.java#L187-L200), [armadura](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/util/Util.java#L260-L274).

**Riscos de gameplay:** a busca por alvos é executada repetidamente no tick e tem potencial de custo proporcional às entidades no cubo; cap, limites negativos, owner e dimensão precisam teste. Verificar servidor dedicado, client, PvP, claims, choque com outros sistemas de movimento, estados de time counter, recast e unload; simulação de atração não é prova de dano. **+0 identidades; adapters RPG não implementados.**
