# IKeepInventoryEntity — morte, inventário e Curios

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`IKeepInventoryEntity.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/IKeepInventoryEntity.java) — `entity/mobs/IKeepInventoryEntity.java`
- [`AcesSpellUtilsServerEvents.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java) — `events/AcesSpellUtilsServerEvents.java`
- [`ASAttachmentRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttachmentRegistry.java) — `registries/ASAttachmentRegistry.java`
- [`PlayerMixin.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/mixins/server/PlayerMixin.java) — `mixins/server/PlayerMixin.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`IKeepInventoryEntity` declara `range = 128`. Em `LivingDeathEvent` de `ServerPlayer`, Ace consulta `LivingEntity` numa caixa `entity.getBoundingBox().inflate(IKeepInventoryEntity.range * 2)` e, para cada marcador encontrado, grava `keep_inv_on_death = !gamerule keepInventory`. Não há teste explícito adicional de alive, owner, aliado, linha de visão ou causador da morte; `killer` é lido e não usado. Se não encontrar marcador, não há ramo que zere flag anterior ([morte][keep-death]).

A attachment Boolean começa false, usa `Codec.BOOL` e `copyOnDeath()`. XP é cancelado e Curios recebe override `ALWAYS_KEEP` com predicado universal quando `ServerPlayer` tem flag true. O mixin cancela `Player.dropEquipment` no HEAD sob a mesma flag. Essas etapas reconsultam a flag, sem refazer proximidade ou gamerule ([attachment][keep-attachment], [XP/Curios][keep-drops], [mixin][keep-mixin]).

`PlayerEvent.Clone` exige morte e original `ServerPlayer` com flag true; substitui o inventário do novo pelo original, copia `experienceLevel`, `totalExperience`, `experienceProgress` e score, e remove attachment dos dois. A cópia explícita de inventário/XP é distinta de `copyOnDeath` da flag; os handlers não declaram prioridade especial nem transação entre marcação, drops e clone ([clone][keep-clone]).

## Targeting, geometria, custos e duração

Jogador morto e entidades `IKeepInventoryEntity` próximas; a busca observada é AABB inflado 256 blocos em cada direção, não prova de raio euclidiano de 128.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Lifecycle/reatribuição e perda de itens devem ser testados em death + clone + respawn + multiplayer; incluir flag anterior sem marcador, gamerule true, eventos cancelados e ordem de Curios/clone no host. Não fazer segunda cópia, cancelar drops duas vezes ou assumir que `range` é distância efetiva radial. Não interpretar como resurrection/cast.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**

[keep-death]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L817-L840
[keep-attachment]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttachmentRegistry.java#L12-L16
[keep-drops]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L758-L785
[keep-mixin]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/mixins/server/PlayerMixin.java#L11-L22
[keep-clone]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L787-L815
