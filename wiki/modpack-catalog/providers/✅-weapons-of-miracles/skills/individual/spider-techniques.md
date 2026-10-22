# Spider Techniques

## Ficha técnica para perks — 2.0.178

**ID:** `wom:spider_techniques` · **categoria:** Mover · **disposição mágica:** `EXCLUDED`.

Mantém deslocamento em paredes, input de pulo e estado de wall running/glide. A atualização possui débitos explícitos de stamina.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.SPIDER_TECHNIQUES` → supplier `lambda$static$28(ResourceLocation)` → `reascer.wom.skill.mover.SpiderTechniquesSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/mover/SpiderTechniquesSkill.class`; base `yesman.epicfight.skill.Skill`. Recurso do builder **`NONE`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void loadDatapackParameters(net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lnet/minecraft/nbt/CompoundTag;)V`.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `private boolean valideBlock(net.minecraft.world.level.block.state.BlockState, net.minecraft.core.BlockPos, net.minecraft.world.level.Level)` · descritor JVM `(Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/Level;)Z`.
- `public boolean canExecute(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)Z`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.event.EpicFightEventHooks$Player.COMBO_ATTACK`, `yesman.epicfight.api.client.event.EpicFightClientEventHooks$Control.MAPPED_MOVEMENT_INPUT_UPDATE`, `yesman.epicfight.api.event.EpicFightEventHooks$Entity.TAKE_DAMAGE_INCOME` |
| `updateContainer` | `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.registry.entries.EpicFightAttributes.STAMINA_REGEN`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill` |
| `lambda$onInitiate$2` | `net.minecraft.tags.DamageTypeTags.IS_FALL` |

**Estado do provider referenciado:** `WALL_GLIDE`, `TIMER`, `WALL_RUNNING`, `TIMER_REFRESH`, `JUMP_KEY_UP`, `ANGLE`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/spider_techniques.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `xp_requirement` | `0` | Dado empacotado de progressão; não é lido pelo loader base Skill auditado. Consumidor final/override da árvore implantada NÃO VERIFICADO. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | Seleção/alcance: seguir estado de alvo, consultas e/ou animações indicadas pelo código. Distância máxima, LOS, filtros, teto de alvos e collider final **NÃO VERIFICADOS** nesta cadeia; não inferir AOE pelo nome. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | Projétil próprio, escala visual, collider, velocidade e lifetime **NÃO VERIFICADOS** na cadeia completa. Nenhuma API externa de tamanho foi homologada; para passivas/guarda/movimento não acrescentar projétil por inferência temática. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | `loadDatapackParameters(CompoundTag)` chama o loader base e depois grava **consumption=0,2**; `updateContainer` tem chamadas explícitas `consumeForSkill(..., STAMINA, ...)`. O JSON empacotado só contém xp_requirement; não adicionar ficticiamente consumption ao arquivo original. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../individual-skill-cards-2.0.178.json) · [contrato técnico](../../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
