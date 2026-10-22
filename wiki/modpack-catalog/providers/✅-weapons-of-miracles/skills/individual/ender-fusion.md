# Ender Fusion

## Ficha técnica para perks — 2.0.178

**ID:** `wom:ender_fusion` · **categoria:** Weapon Innate · **disposição mágica:** `EXCLUDED`.

Opera a Enderblaster em modo de duas mãos, com seleção de disparos, reload e caminho próprio de consumo. Declara cooldown interno, distinto do JSON de stacks.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.ENDER_FUSION` → supplier `lambda$static$48(ResourceLocation)` → `reascer.wom.skill.weaponinnate.EnderFusionSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/weaponinnate/EnderFusionSkill.class`; base `yesman.epicfight.skill.weaponinnate.ConditionalWeaponInnateSkill`. Recurso do builder **`WEAPON_CHARGE`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `public void onInitiateClient(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public void onRemoveClient(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public net.minecraft.network.protocol.common.custom.CustomPacketPayload getExecutionPacket(yesman.epicfight.skill.SkillContainer, net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lnet/minecraft/nbt/CompoundTag;)Lnet/minecraft/network/protocol/common/custom/CustomPacketPayload;`.
- `public void executeOnServer(yesman.epicfight.skill.SkillContainer, net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lnet/minecraft/nbt/CompoundTag;)V`.
- `public boolean isExecutableState(yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>)` · descritor JVM `(Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;)Z`.
- `public boolean resourcePredicate(yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>, yesman.epicfight.api.event.types.player.SkillCastEvent)` · descritor JVM `(Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;Lyesman/epicfight/api/event/types/player/SkillCastEvent;)Z`.
- `public yesman.epicfight.skill.weaponinnate.WeaponInnateSkill registerPropertiesToAnimation()` · descritor JVM `()Lyesman/epicfight/skill/weaponinnate/WeaponInnateSkill;`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.
- `public yesman.epicfight.skill.Skill registerPropertiesToAnimation()` · descritor JVM `()Lyesman/epicfight/skill/Skill;`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.event.EpicFightEventHooks$Animation.START_ACTION` |
| `onInitiateClient` | `yesman.epicfight.api.client.event.EpicFightClientEventHooks$Entity.MODIFY_PLAYER_LIVING_MOTION_COMPOSITE` |
| `executeOnServer` | `yesman.epicfight.api.event.EpicFightEventHooks$Player.CONSUME_SKILL` |
| `resourcePredicate` | `yesman.epicfight.api.event.EpicFightEventHooks$Player.CONSUME_SKILL`, `yesman.epicfight.skill.SkillContainer.setMaxDuration`, `yesman.epicfight.skill.SkillContainer.setMaxResource` |
| `updateContainer` | `yesman.epicfight.skill.SkillContainer.setMaxResource` |

**Estado do provider referenciado:** `NOFALLDAMAGE`, `COOLDOWN`, `COMBO`, `ZOOM`, `HOLDING_RMB`, `SHOOT`, `RELOAD_COOLDOWN`, `TIMER`, `SIDE`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/ender_fusion.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `consumption` | `12.0` | `Skill.loadDatapackParameters(CompoundTag)` → campo float `consumption`; recurso do builder e gastos explícitos são descritos separadamente. |
| `max_stacks` | `24` | Loader base → int `maxStackSize`; capacidade declarada, não quantidade de alvos. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | Seleção/alcance: seguir estado de alvo, consultas e/ou animações indicadas pelo código. Distância máxima, LOS, filtros, teto de alvos e collider final **NÃO VERIFICADOS** nesta cadeia; não inferir AOE pelo nome. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | Classe seleciona ENDERBLASTER_TWOHAND_*; spawn, collider e lifetime precisam seguir as animações/entidades. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Campo binário `private static final int cooldown = 40`; `updateContainer` mantém estado e recurso. A presença do campo não prova duração efetiva universal nem unidade em segundos. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | Recurso declarado do builder: **WEAPON_CHARGE**. Parâmetros RAW e chamadas explícitas de consumo/refund acima são caminhos distintos; débito líquido e composição de listeners **NÃO VERIFICADOS**. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../individual-skill-cards-2.0.178.json) · [contrato técnico](../../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
