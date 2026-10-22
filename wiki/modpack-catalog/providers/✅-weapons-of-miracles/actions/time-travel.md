# Time Travel

- Provider: **Weapons of Miracles** (`wom`)
- Version: `2.0.178`
- Exact physical/publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`
- Skill id: `wom:time_travel`
- Skill category: Dodge
- State: `COUNTED_EXACT`

## Semantic identity

Time Travel is a deliberate provider skill that records temporal player state involving position/health and supports the provider's return-style temporal action.

The state registration and later provider settlement are phases of one temporal semantic root, not separate spells.

## Reachability

The exact WOM Epic Skills tree includes `wom:time_travel`, closing provider-native acquisition at catalog level.

## Boundary

WOM remains authority for recorded state, eligibility, temporal return semantics and settlement. No numerical timing or resource value is inferred here.

Source: `../EXACT-2.0.178-ARTIFACT-AUDIT.md`; `../skills/SKILL-DISPOSITION-2.0.178.md`.

## Ficha técnica para perks — 2.0.178

**ID:** `wom:time_travel` · **categoria:** Dodge · **disposição mágica:** `COUNTED_EXACT`.

Mantém um registro temporal do jogador e executa retorno por uma sequência própria. O JSON de custo zero não elimina o débito explícito de stamina no método servidor.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.TIME_TRAVEL` → supplier `lambda$static$6(ResourceLocation)` → `reascer.wom.skill.dodges.TimeTravelSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/dodges/TimeTravelSkill.class`; base `yesman.epicfight.skill.dodge.DodgeSkill`. Recurso do builder **`STAMINA`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `public void executeOnServer(yesman.epicfight.skill.SkillContainer, net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lnet/minecraft/nbt/CompoundTag;)V`.
- `public yesman.epicfight.skill.Skill getPriorSkill()` · descritor JVM `()Lyesman/epicfight/skill/Skill;`.
- `public boolean isExecutableState(yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch<?>)` · descritor JVM `(Lyesman/epicfight/world/capabilities/entitypatch/player/PlayerPatch;)Z`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.event.EpicFightEventHooks$Entity.TAKE_DAMAGE_POST` |
| `executeOnServer` | `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill` |
| `isExecutableState` | `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.setStamina` |

**Estado do provider referenciado:** `TIMER`, `REGISTERED_POSITION`, `REGISTERED_HEALTH`, `COOLDOWN`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/time_travel.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `consumption` | `0.0` | `Skill.loadDatapackParameters(CompoundTag)` → campo float `consumption`; recurso do builder e gastos explícitos são descritos separadamente. |
| `xp_requirement` | `12` | Dado empacotado de progressão; não é lido pelo loader base Skill auditado. Consumidor final/override da árvore implantada NÃO VERIFICADO. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | Seleção/alcance: seguir estado de alvo, consultas e/ou animações indicadas pelo código. Distância máxima, LOS, filtros, teto de alvos e collider final **NÃO VERIFICADOS** nesta cadeia; não inferir AOE pelo nome. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | Projétil próprio, escala visual, collider, velocidade e lifetime **NÃO VERIFICADOS** na cadeia completa. Nenhuma API externa de tamanho foi homologada; para passivas/guarda/movimento não acrescentar projétil por inferência temática. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | JSON `consumption=0`, mas `executeOnServer` PCs 20–32 chama **consumeForSkill(this, STAMINA,12)** e descarta o retorno nesse ponto. Há ainda `setStamina` em `isExecutableState`; não calcular custo líquido apenas pelo JSON. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../skills/../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../skills/individual-skill-cards-2.0.178.json) · [contrato técnico](../skills/../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
