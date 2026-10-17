# Heal Ring Magic Book

**Prova física Java21 (2026-10-13):** ✅ `COUNTED_EXACT` — `companions:book_heal_ring`, `dev.xylonity.companions.common.item.book.books.HealRingBook` (subclasse real de `AbstractMagicBook`), [auditoria #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) e [dossiê SHA-exato](../EXACT-BINARY-MAGIC-BOOKS-1.3.4.md). Item mágico provider-native, não spell Iron's. Cooldown, cast e aquisição continuam source-pinned/Survival ⚠️; +0 identidade nova.

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_heal_ring`
- Concrete class: `HealRingBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_EXACT` (**identidade estática somente**)
- Strict contribution: `1`
- Source-default cooldown: **200 ticks**
- Source-level survival acquisition: **End Minion + End Coin random reward**

## Action surface

creates the provider healing-ring projectile/effect at the caster.

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

## Engenharia causal para perks — Heal Ring (fonte 1.3.4, 17/10/2026)

**Estado:** `SOURCE-CAUSALITY` no commit `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`; identidade SHA-exata e cooldown default não equivalem a cura efetivamente medida no modpack.

| Eixo | Mecânica causal no source | Fronteira de perk |
|---|---|---|
| Spawn / dono | `HealRingBook.use` cria `HEAL_RING_PROJECTILE` **somente no servidor**, na posição do player com `setOwner(player)` e `addFreshEntity`. Cooldown é aplicado mesmo com factory `null`. | `SEM_HOOK_SEGURO` para múltiplos anéis, posição alternativa ou healing projectile re-spawn. |
| Alvo / geometria | Ao trigger, `HealRingProjectile` escolhe **todas** `LivingEntity` em `owner.getBoundingBox().inflate(2)`; é **AABB**, não esfera raio 2; não filtra equipe, hostilidade ou vínculo no método. | `SEM_HOOK_SEGURO` para excluir hostis/expandir área por perk sem provider API. |
| Momento / duração | `hasHealed` começa false. Quando `tickCount % 10 == 0` e ainda false, realiza uma rodada e marca true; **máximo uma rodada local por entidade anel**. `baseLifetime()=23 ticks`. Não há serializer local demonstrado para `hasHealed`; reload e exatamente-once precisam teste. | `SEM_HOOK_SEGURO` para duração/taxa de pulses. Não presumir cura cada 10 ticks. |
| Cura e inversão | Se `e.isInvertedHealAndHarm()`, chama `hurt(indirectMagic(ring,owner), HEAL_RING_HEALING)`; caso contrário chama `e.heal(HEAL_RING_HEALING)`. Config default `HEAL_RING_HEALING=6.0` **health points**; efeito real limitado pelo dano/HP faltante e resistência/eventos. | `CONFIG_NATIVE` para magnitude global; boost por usuário **NÃO_VERIFICADO**. Mastery deve contar cura efetiva e dano aceito separadamente, não tentativa. |
| Sidedness / sync | O bloco local de cura/dano **não testa `!level.isClientSide`**; partículas possuem `instanceof ServerLevel`, mas execução efetiva em ambos os lados depende de engine/entidade. Esse é um risco de duplicação de observação, não bug comprovado. | **⛔** não disparar perks client-side. |
| Cooldown/custos | Default `HEAL_RING_COOLDOWN=200 ticks`, multiplicado por `1 - (peças Mage × 0,15)`. O `use` não debitou mana explicitamente. | `CONFIG_NATIVE` global; não criar custo transacional duplicado no Black Arcana. |

Âncoras: [HealRingBook.java — 26–47](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/item/book/books/HealRingBook.java#L26-L47) · [HealRingProjectile.java — 34–72](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/HealRingProjectile.java#L34-L72) · [baseLifetime](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/entity/projectile/HealRingProjectile.java#L91-L100) · [valor cura](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L706-L711) · [cooldown](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/config/CompanionsConfig.java#L769-L774) · [armor pieces](https://github.com/Xylonity/Companions/blob/95c9445e1514648418064ea90b5c373e81375d2f/common/src/main/java/dev/xylonity/companions/common/util/Util.java#L260-L274).

**QA de aceitação:** LivingEntity com HP total/parcial, undead/entidades invertidas, aliados e hostis, duas ativações simultâneas, recast, chunk unload, death/logout do dono, delay e servidor dedicado. Recompensa de Mastery somente por delta de HP ou dano pós-settlement observável; nenhum hook seguro foi homologado. **+0 novas magias.**
