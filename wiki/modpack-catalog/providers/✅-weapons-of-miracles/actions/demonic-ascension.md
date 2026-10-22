# Demonic Ascension

- Provider: **Weapons of Miracles** (`wom`)
- Version: `2.0.178`
- Exact physical/publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`
- Skill id: `wom:demonic_ascension`
- Owner: `wom:antitheus`
- Skill category: Weapon Innate
- State: `COUNTED_EXACT`

## Semantic identity

Demonic Ascension is a deliberate demonic possession/ascension action with provider teleport/effect/entity lifecycle.

Teleportation, effects and spawned/provider-managed entities are consequences of this same root.

## Reachability

The exact artifact closes `wom:antitheus` through a provider smithing recipe, so current catalog reachability is closed.

## Boundary

WOM owns possession/ascension state, teleport/effect/entity lifecycle and all resource settlement.

Source: `../EXACT-2.0.178-ARTIFACT-AUDIT.md`; `../skills/SKILL-DISPOSITION-2.0.178.md`.

## Ficha técnica para perks — 2.0.178

**ID:** `wom:demonic_ascension` · **categoria:** Weapon Innate · **disposição mágica:** `COUNTED_EXACT`.

Ativa estado de ascensão/possessão da Antitheus e suas rotinas de blink, puxão, disparo e black hole. Recursos, entidades e teleporte têm caminhos distintos.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.DEMONIC_ASCENSION` → supplier `lambda$static$42(ResourceLocation)` → `reascer.wom.skill.weaponinnate.DemonicAscensionSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/weaponinnate/DemonicAscensionSkill.class`; base `yesman.epicfight.skill.weaponinnate.WeaponInnateSkill`. Recurso do builder **`WEAPON_CHARGE`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `public void onInitiateClient(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public void onRemoveClient(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public void executeOnServer(yesman.epicfight.skill.SkillContainer, net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lnet/minecraft/nbt/CompoundTag;)V`.
- `public void cancelOnServer(yesman.epicfight.skill.SkillContainer, net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lnet/minecraft/nbt/CompoundTag;)V`.
- `public boolean resourcePredicate(yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>, yesman.epicfight.api.event.types.player.SkillCastEvent)` · descritor JVM `(Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;Lyesman/epicfight/api/event/types/player/SkillCastEvent;)Z`.
- `public boolean canExecute(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)Z`.
- `public boolean isExecutableState(yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>)` · descritor JVM `(Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;)Z`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public yesman.epicfight.skill.weaponinnate.WeaponInnateSkill registerPropertiesToAnimation()` · descritor JVM `()Lyesman/epicfight/skill/weaponinnate/WeaponInnateSkill;`.
- `public yesman.epicfight.skill.Skill registerPropertiesToAnimation()` · descritor JVM `()Lyesman/epicfight/skill/Skill;`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.event.EpicFightEventHooks$Player.CONSUME_SKILL`, `yesman.epicfight.api.event.EpicFightEventHooks$Entity.DELIVER_DAMAGE_POST`, `yesman.epicfight.api.event.EpicFightEventHooks$Animation.ATTACK_PHASE_END`, `yesman.epicfight.api.event.EpicFightEventHooks$Animation.START_ACTION` |
| `onInitiateClient` | `yesman.epicfight.api.client.event.EpicFightClientEventHooks$Entity.MODIFY_PLAYER_LIVING_MOTION_COMPOSITE` |
| `executeOnServer` | `yesman.epicfight.api.event.EpicFightEventHooks$Player.CONSUME_SKILL` |
| `resourcePredicate` | `yesman.epicfight.api.event.EpicFightEventHooks$Player.CONSUME_SKILL`, `yesman.epicfight.skill.SkillContainer.setMaxDuration`, `yesman.epicfight.skill.SkillContainer.setMaxResource`, `net.minecraft.world.entity.player.Player.setHealth`, `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill`, `setConsumptionSynchronize` |
| `updateContainer` | `net.minecraft.world.entity.LivingEntity.teleportTo`, `yesman.epicfight.world.damagesource.EpicFightDamageSource.setStunType`, `net.minecraft.world.effect.MobEffects.WITHER`, `yesman.epicfight.world.damagesource.EpicFightDamageTypeTags.WEAPON_INNATE`, `net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_DAMAGE`, `net.minecraft.world.level.Level.addFreshEntity`, `net.minecraft.world.entity.player.Player.heal`, `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill`, `net.minecraft.world.entity.LivingEntity.removeEffect`, `net.minecraft.world.entity.LivingEntity.hurt`, `net.minecraft.world.entity.player.Player.setHealth`, `yesman.epicfight.world.capabilities.entitypatch.player.ServerPlayerPatch.setStamina`, `setConsumptionSynchronize`, `net.minecraft.world.phys.AABB.ofSize`, `net.minecraft.world.entity.ai.attributes.Attributes.KNOCKBACK_RESISTANCE`, `net.minecraft.world.entity.LivingEntity.addEffect`, `net.minecraft.world.effect.MobEffects.SLOW_FALLING`, `net.minecraft.world.entity.player.Player.addEffect`, `net.minecraft.world.effect.MobEffects.MOVEMENT_SPEED` |
| `lambda$onInitiate$3` | `yesman.epicfight.world.damagesource.EpicFightDamageSource.setStunType`, `net.minecraft.world.entity.player.Player.hurt` |
| `lambda$onInitiate$1` | `net.minecraft.world.effect.MobEffects.WITHER`, `net.minecraft.world.entity.LivingEntity.hurt`, `net.minecraft.world.entity.player.Player.heal`, `net.minecraft.world.entity.LivingEntity.removeEffect`, `yesman.epicfight.world.damagesource.EpicFightDamageSource.setStunType`, `net.minecraft.world.entity.player.Player.hurt` |

**Estado do provider referenciado:** `TIMER`, `ACTIVE`, `ASCENDING`, `LAPSE`, `HOLDING_RMB`, `DARKNESS_TARGET_HITED`, `SHOOT`, `ZOOM_COOLDOWN`, `ZOOM`, `DARKNESS_TARGET`, `DARKNESS_ACTIVATE_PORTAL`, `DARKNESS_PORTAL_TIMER`, `DARKNESS_TARGET_VEC`, `DARKNESS_TARGET_REAPED`, `DARKNESS_PORTAL_VEC`, `SHOOT_COOLDOWN`, `DARKNESS_PORTAL_ANGLE`, `BLACKHOLE_TIMER`, `BLACKHOLE_ACTIVE`, `BLACKHOLE_VEC`, `PARTICLE`, `WITHERCATHARSIS`, `SERIUS_FOCUS_COOLDOWN`, `SERIUS_FOCUS`, `WITHERAFTEREFFECT`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/demonic_ascension.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `consumption` | `666.0` | `Skill.loadDatapackParameters(CompoundTag)` → campo float `consumption`; recurso do builder e gastos explícitos são descritos separadamente. |
| `max_duration` | `13340` | Loader base → campo int `maxDuration`; configuração do contador, não segundos garantidos de efeito. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | `updateContainer` PCs 4230–4247: consulta em BLACKHOLE_VEC com `AABB.ofSize(...,50,50,50)`; a caixa tem ±25 por eixo. Há teleporte e filtros adicionais; não equivale a raio de dano 50. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | `updateContainer` contém criação de entidade e `Level.addFreshEntity`, além de teleporte/dano. Entidade ofensiva, dimensões, velocidade, lifetime e collider final precisam de auditoria downstream; não confundir com tamanho do VFX. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | Recurso declarado do builder: **WEAPON_CHARGE**. Parâmetros RAW e chamadas explícitas de consumo/refund acima são caminhos distintos; débito líquido e composição de listeners **NÃO VERIFICADOS**. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../skills/../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../skills/individual-skill-cards-2.0.178.json) · [contrato técnico](../skills/../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
