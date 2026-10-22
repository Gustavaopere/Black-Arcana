# Perfect Bulwark

## Ficha técnica para perks — 2.0.178

**ID:** `wom:perfect_bulwark` · **categoria:** Guard · **disposição mágica:** `EXCLUDED`.

Guarda avançada com reações defensivas e consulta espacial de entidades durante a atualização. A caixa consultada não mede sozinha o alcance efetivo do bloqueio.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.PERFECT_BULWARK` → supplier `lambda$static$10(ResourceLocation)` → `reascer.wom.skill.guard.PerfectBulwarkSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/guard/PerfectBulwarkSkill.class`; base `yesman.epicfight.skill.guard.GuardSkill`. Recurso do builder **`STAMINA`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public static yesman.epicfight.skill.guard.GuardSkill$Builder createCounterAttackBuilder()` · descritor JVM `()Lyesman/epicfight/skill/guard/GuardSkill$Builder;`.
- `public void setPenalizer(float)` · descritor JVM `(F)V`.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `public void guard(yesman.epicfight.skill.SkillContainer, yesman.epicfight.world.capabilities.item.CapabilityItem, yesman.epicfight.api.event.types.entity.TakeDamageEvent$Income, float, float, boolean)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/world/capabilities/item/CapabilityItem;Lyesman/epicfight/api/event/types/entity/TakeDamageEvent$Income;FFZ)V`.
- `protected boolean isBlockableSource(net.minecraft.world.damagesource.DamageSource, boolean)` · descritor JVM `(Lnet/minecraft/world/damagesource/DamageSource;Z)Z`.
- `protected yesman.epicfight.api.animation.AnimationManager$AnimationAccessor<? extends yesman.epicfight.api.animation.types.StaticAnimation> getGuardMotion(yesman.epicfight.skill.SkillContainer, yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>, yesman.epicfight.world.capabilities.item.CapabilityItem, yesman.epicfight.skill.guard.GuardSkill$BlockType)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;Lyesman/epicfight/world/capabilities/item/CapabilityItem;Lyesman/epicfight/skill/guard/GuardSkill$BlockType;)Lyesman/epicfight/api/animation/AnimationManager$AnimationAccessor;`.
- `public yesman.epicfight.skill.Skill getPriorSkill()` · descritor JVM `()Lyesman/epicfight/skill/Skill;`.
- `protected boolean isAdvancedGuard()` · descritor JVM `()Z`.
- `public void resetHolding(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public void startHolding(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public void holdTick(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public void onStopHolding(yesman.epicfight.skill.SkillContainer, yesman.epicfight.network.server.SPSkillFeedback)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/network/server/SPSkillFeedback;)V`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.client.event.EpicFightClientEventHooks$Entity.MODIFY_PLAYER_LIVING_MOTION_COMPOSITE`, `yesman.epicfight.api.client.event.EpicFightClientEventHooks$Control.MAPPED_MOVEMENT_INPUT_UPDATE`, `yesman.epicfight.api.event.EpicFightEventHooks$Entity.TAKE_DAMAGE_INCOME` |
| `guard` | `net.minecraft.world.damagesource.DamageTypes.MAGIC`, `net.minecraft.world.damagesource.DamageTypes.INDIRECT_MAGIC`, `net.minecraft.world.damagesource.DamageTypes.WITHER`, `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill` |
| `isBlockableSource` | `net.minecraft.world.damagesource.DamageTypes.DRAGON_BREATH`, `net.minecraft.world.damagesource.DamageTypes.FIREBALL`, `net.minecraft.tags.DamageTypeTags.IS_EXPLOSION`, `net.minecraft.tags.DamageTypeTags.IS_PROJECTILE`, `net.minecraft.world.damagesource.DamageTypes.FIREWORKS`, `net.minecraft.world.damagesource.DamageTypes.PLAYER_EXPLOSION`, `net.minecraft.world.damagesource.DamageTypes.SONIC_BOOM`, `net.minecraft.world.damagesource.DamageTypes.STING`, `net.minecraft.world.damagesource.DamageTypes.TRIDENT`, `net.minecraft.world.damagesource.DamageTypes.WITHER_SKULL`, `net.minecraft.world.damagesource.DamageTypes.UNATTRIBUTED_FIREBALL`, `yesman.epicfight.world.damagesource.EpicFightDamageTypeTags.GUARD_PUNCTURE` |
| `updateContainer` | `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill`, `net.minecraft.world.phys.AABB.ofSize`, `net.minecraft.world.entity.ai.attributes.Attributes.KNOCKBACK_RESISTANCE`, `yesman.epicfight.world.damagesource.EpicFightDamageSource.setStunType`, `net.minecraft.world.entity.LivingEntity.hurt` |
| `lambda$onInitiate$13` | `yesman.epicfight.api.animation.types.EntityState.hurt`, `yesman.epicfight.world.damagesource.EpicFightDamageTypeTags.GUARD_PUNCTURE` |

**Estado do provider referenciado:** `CHARGE`, `HOLDING_RMB`, `COOLDOWN`, `PARRYING`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/perfect_bulwark.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `xp_requirement` | `8` | Dado empacotado de progressão; não é lido pelo loader base Skill auditado. Consumidor final/override da árvore implantada NÃO VERIFICADO. |
| `penalizer` | `0.2` | `GuardSkill.loadDatapackParameters` → float `penalizer`; rotina de guarda compõe o gasto. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | `updateContainer` PCs 844–856: consulta usa `AABB.ofSize(player.position(),20,20,20)`. Dimensões totais, não raio/hitbox de guarda; filtros e ação efetiva permanecem distintos. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | Projétil próprio, escala visual, collider, velocidade e lifetime **NÃO VERIFICADOS** na cadeia completa. Nenhuma API externa de tamanho foi homologada; para passivas/guarda/movimento não acrescentar projétil por inferência temática. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | Recurso declarado do builder: **STAMINA**. Parâmetros RAW e chamadas explícitas de consumo/refund acima são caminhos distintos; débito líquido e composição de listeners **NÃO VERIFICADOS**. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../individual-skill-cards-2.0.178.json) · [contrato técnico](../../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
