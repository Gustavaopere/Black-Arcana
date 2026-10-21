# Stone Spikes Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_stone_spikes`, `dev.xylonity.companions.common.item.book.books.StoneSpikesBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_stone_spikes`
- Concrete class: `StoneSpikesBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **140 ticks**
- Source-level survival acquisition: **End Minion + End Coin random reward**

## Action surface

creates a forward ground-spike pattern with a central row and two angled side rows.

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

## Engenharia causal para perks — Stone Spikes (fonte 1.3.4, 17/10/2026)

**Estado:** `SOURCE-CAUSALITY` em `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`, sem prova de paridade de corpos de método com JAR físico ou comportamento em jogo. O catálogo permanece uma única identidade `companions:book_stone_spikes`.

| Eixo | Fatos verificáveis em código | Mutabilidade RPG |
|---|---|---|
| Geometria/spawn | `StoneSpikesBook.use` gera **três fileiras**: uma frontal com **10** candidatos, duas laterais rotacionadas **±30°** com **3** cada (**16 tentativas de spawn**, sujeito à factory). Espaçamento por fileira de **1,5 blocos** a partir de 1,5. Não é um cone AOE nativo nem 16 spells independentes. | `SEM_HOOK_SEGURO` para contagem, ângulo, comprimento ou largura. |
| Temporalidade | Primeira espícula de cada fileira é criada imediatamente; demais programadas com `TickScheduler.scheduleBoth(level, ..., i*2)`. A criação e agendamento no método de livro **não estão sob guard server-only**, só o cooldown está; precisa diferenciar duplicação cliente/servidor e semântica KnightLib. | `NÃO_VERIFICADO` listener confiável por cast; nunca contar cada spawn como novo cast. |
| Local do solo/custo | `findSpikeH` varre blocos verticalmente desde o Y inicial até max/min build height (ordem depende de pitch), procurando primeiro collision shape não-vazio, ou utiliza Y original caso não encontre. **Até 16 scans verticais** por cast; limites de chunk/claims/solidez precisam QA. | `SEM_HOOK_SEGURO` para expor range vertical/perf sem alterar algoritmo provider-native. |
| Área de acerto | Cada `StoneSpikeProjectile.tick` examina entidades em `getBoundingBox().inflate(0.3)` e testa owner+linked exclusion. Não confundir aumento da AABB de busca com tamanho físico do projétil. Pode alcançar **várias** entidades por tick e repetir tentativas ao longo de vários ticks. | `SEM_HOOK_SEGURO` para hitbox, target cap e recast. |
| Dano/tipo | `hurt(indirectMagic(spike,owner), STONE_SPIKE_DAMAGE)`, default config **4.0**. Um roll de **25%** tenta POISON se não houver efeito, por **20..99 ticks**, amplifier 0. No corpo examinado, o roll acontece **sem conferir se `hurt` retornou true**. | `CONFIG_NATIVE` magnitude global; `NÃO_VERIFICADO` para dano/poison por perk; XP deve distinguir proc de dano aceito. |
| Lifetime / lado | `baseLifetime=36 ticks`. O corpo `tick` invoca lógica de `hurt` e POISON **sem guard server-only local**; partículas em tick 5 usam ServerLevel e remoção é explícita ao expirar. | `NÃO_VERIFICADO` sides, armor/PvP/claims e custo de loops por segundo. |
| Cooldown | Default `STONE_SPIKES_COOLDOWN=140 ticks`; desconto default 0,15 por peça da armadura Mage, não um perk RPG. Sem mana explicitamente cobrada nesse corpo. | `CONFIG_NATIVE` global, hook individual ⛔. |

Âncoras: [StoneSpikesBook.java — use/spawns](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/StoneSpikesBook.java#L32-L89) · [findSpikeH](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/StoneSpikesBook.java#L90-L104) · [StoneSpikeProjectile.java — tick/dano/status](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/StoneSpikeProjectile.java#L29-L76) · [lifetime](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/StoneSpikeProjectile.java#L86-L95) · [config dano](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L692-L697) · [config cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L797-L802).

**QA e segurança:** testar construção com teto, caverna, bedrock e chunks não carregados; 16 candidatas e scans verticais em servidor lotado; injeção client-server do scheduler; vários alvos/iframes/status; friendly/PvP, world protection e reload. Não presumir WorldEffectPolicy Black Arcana aplicada ao projectile provider-native. **+0 raízes semânticas e adapters.**
