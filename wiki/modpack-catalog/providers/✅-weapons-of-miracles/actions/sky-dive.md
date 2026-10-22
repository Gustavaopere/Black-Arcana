# Sky Dive

- Provider: **Weapons of Miracles** (`wom`)
- Version: `2.0.178`
- Exact physical/publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`
- Skill id: `wom:agony_plunge`
- Owner: `wom:agony`
- Skill category: Weapon Innate
- State: `COUNTED_EXACT`

## Semantic identity

Sky Dive is the deliberate supernatural action owned by Agony: the provider performs its aerial disappearance/reposition/levitation and dive sequence as one causal root.

Individual relocation phases, levitation, animation, effects and hit settlement are downstream phases rather than separate spell identities.

## Reachability

Exact current provider data closes Agony through WOM chest-loot injection, so this root is catalog-reachable and strict-counted.

## Boundary

WOM remains authority for activation, movement sequence, resource/cooldown state and combat settlement.

Source: `../EXACT-2.0.178-ARTIFACT-AUDIT.md`; `../skills/SKILL-DISPOSITION-2.0.178.md`.

## Ficha técnica para perks — 2.0.178

**ID:** `wom:agony_plunge` · **categoria:** Weapon Innate · **disposição mágica:** `COUNTED_EXACT`.

Sky Dive seleciona fases de deslocamento/mergulho da arma Agony e trata alvo, altura e controle de recursos em rotinas próprias.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.AGONY_PLUNGE` → supplier `lambda$static$40(ResourceLocation)` → `reascer.wom.skill.weaponinnate.SkyDiveSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/weaponinnate/SkyDiveSkill.class`; base `yesman.epicfight.skill.weaponinnate.WeaponInnateSkill`. Recurso do builder **`WEAPON_CHARGE`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `public void executeOnServer(yesman.epicfight.skill.SkillContainer, net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lnet/minecraft/nbt/CompoundTag;)V`.
- `public boolean resourcePredicate(yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>, yesman.epicfight.api.event.types.player.SkillCastEvent)` · descritor JVM `(Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;Lyesman/epicfight/api/event/types/player/SkillCastEvent;)Z`.
- `public boolean isExecutableState(yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>)` · descritor JVM `(Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;)Z`.
- `public boolean canExecute(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)Z`.
- `public yesman.epicfight.skill.weaponinnate.WeaponInnateSkill registerPropertiesToAnimation()` · descritor JVM `()Lyesman/epicfight/skill/weaponinnate/WeaponInnateSkill;`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public yesman.epicfight.skill.Skill registerPropertiesToAnimation()` · descritor JVM `()Lyesman/epicfight/skill/Skill;`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.event.EpicFightEventHooks$Entity.DELIVER_DAMAGE_INCOME`, `yesman.epicfight.api.event.EpicFightEventHooks$Player.COMBO_ATTACK`, `yesman.epicfight.api.event.EpicFightEventHooks$Animation.START_ACTION` |
| `executeOnServer` | `yesman.epicfight.registry.entries.EpicFightMobEffects.STUN_IMMUNITY`, `net.minecraft.world.entity.player.Player.addEffect`, `net.minecraft.world.phys.AABB.ofSize`, `net.minecraft.world.entity.ai.attributes.Attributes.KNOCKBACK_RESISTANCE`, `net.minecraft.world.effect.MobEffects.SLOW_FALLING` |
| `resourcePredicate` | `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill` |
| `lambda$onInitiate$2` | `net.minecraft.world.effect.MobEffects.SLOW_FALLING`, `net.minecraft.world.entity.player.Player.addEffect` |
| `lambda$onInitiate$1` | `net.minecraft.world.effect.MobEffects.SLOW_FALLING`, `net.minecraft.server.level.ServerPlayer.addEffect` |
| `lambda$onInitiate$0` | `yesman.epicfight.registry.entries.EpicFightMobEffects.STUN_IMMUNITY`, `net.minecraft.world.effect.MobEffects.LEVITATION`, `net.minecraft.server.level.ServerPlayer.addEffect`, `net.minecraft.world.effect.MobEffects.SLOW_FALLING`, `net.minecraft.world.entity.LivingEntity.addEffect`, `net.minecraft.world.entity.LivingEntity.removeEffect`, `net.minecraft.server.level.ServerPlayer.removeEffect` |

**Estado do provider referenciado:** `ACTIVE`, `STACK`, `ATTACKS`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/agony_plunge.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `consumption` | `100.0` | `Skill.loadDatapackParameters(CompoundTag)` → campo float `consumption`; recurso do builder e gastos explícitos são descritos separadamente. |
| `max_stacks` | `3` | Loader base → int `maxStackSize`; capacidade declarada, não quantidade de alvos. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | `executeOnServer` chama `AABB.ofSize` no PC 286 com dimensões derivadas de variável local; LOS, limite de alvo e geometria final de mergulho NÃO VERIFICADOS. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | Projétil próprio, escala visual, collider, velocidade e lifetime **NÃO VERIFICADOS** na cadeia completa. Nenhuma API externa de tamanho foi homologada; para passivas/guarda/movimento não acrescentar projétil por inferência temática. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | Recurso declarado do builder: **WEAPON_CHARGE**. Parâmetros RAW e chamadas explícitas de consumo/refund acima são caminhos distintos; débito líquido e composição de listeners **NÃO VERIFICADOS**. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../skills/../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../skills/individual-skill-cards-2.0.178.json) · [contrato técnico](../skills/../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
