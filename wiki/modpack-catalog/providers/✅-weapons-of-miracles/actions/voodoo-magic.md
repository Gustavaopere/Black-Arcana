# Voodoo Magic

- Provider: **Weapons of Miracles** (`wom`)
- Version: `2.0.178`
- Exact physical/publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`
- Skill id: `wom:voodoo_magic`
- Skill category: Identity
- State: `COUNTED_EXACT`

## Semantic identity

Voodoo Magic is a deliberate player-driven provider action that performs a health↔stamina conversion lifecycle while the provider input/state requirements are satisfied.

Exact WOM evidence distinguishes this from registered passive skills: the provider reads deliberate player input/state and settles the conversion as an active causal action.

## Reachability

The exact WOM Epic Skills tree includes `wom:voodoo_magic`, closing provider-native acquisition at catalog level.

## Boundary

WOM owns eligibility, conversion direction/amount, resource settlement and timing. Black Arcana catalogs the action identity and must not duplicate health or stamina settlement.

Source: `../EXACT-2.0.178-ARTIFACT-AUDIT.md`; `../skills/SKILL-DISPOSITION-2.0.178.md`.

## Ficha técnica para perks — 2.0.178

**ID:** `wom:voodoo_magic` · **categoria:** Identity · **disposição mágica:** `COUNTED_EXACT`.

Liga saúde e stamina por input/estado e eventos de consumo. Há chamadas com montante negativo para fluxo de recuperação, além de alteração direta de saúde.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.VOODOO_MAGIC` → supplier `lambda$static$32(ResourceLocation)` → `reascer.wom.skill.identity.VoodooMagicSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/identity/VoodooMagicSkill.class`; base `yesman.epicfight.skill.Skill`. Recurso do builder **`NONE`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.event.EpicFightEventHooks$Player.CONSUME_SKILL` |
| `updateContainer` | `net.minecraft.world.entity.player.Player.setHealth`, `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill`, `net.minecraft.world.entity.player.Player.heal` |
| `lambda$onInitiate$0` | `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill` |

**Estado do provider referenciado:** `HOLDING_RMB`, `TIMER`, `REGISTERED_HEALTH`, `CONSUMPTION_VALUE`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/voodoo_magic.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `xp_requirement` | `12` | Dado empacotado de progressão; não é lido pelo loader base Skill auditado. Consumidor final/override da árvore implantada NÃO VERIFICADO. |
| `attribute_modifiers` | `[{"attribute":"epicfight:stamina_regen","name":"voodo_magic_stamina_null","uuid":"05e61b67-4531-4127-b973-9f572acede5c","operation":"multiply_total","amount":0.0}]` | Loader base → ATTRIBUTE_ENTRY_CODEC/AttributeModifier.MAP_CODEC. Forma legada name/uuid/operation; aceitação/aplicação deste registro específico NÃO VERIFICADA. Não afirmar bônus ativo. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | `updateContainer` contém `Player.setHealth` e `Player.heal`, com REGISTERED_HEALTH. Custo de saúde e cura seguem ramificações próprias; não converter em mana ou emitir progressão a cada variação. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | Seleção/alcance: seguir estado de alvo, consultas e/ou animações indicadas pelo código. Distância máxima, LOS, filtros, teto de alvos e collider final **NÃO VERIFICADOS** nesta cadeia; não inferir AOE pelo nome. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | Projétil próprio, escala visual, collider, velocidade e lifetime **NÃO VERIFICADOS** na cadeia completa. Nenhuma API externa de tamanho foi homologada; para passivas/guarda/movimento não acrescentar projétil por inferência temática. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | `updateContainer` inclui `consumeForSkill(..., STAMINA, -1,5)` (PC 409), além de montantes calculados. `lambda$onInitiate$0` exige STAMINA, skill diferente de this, stamina insuficiente e jogador fora de Creative; chama `consumeForSkill(this, STAMINA, -event.amount×0,8)` (PC 64). Exclui a própria skill do callback. O sibling RPG normaliza montantes negativos com max(0,amount); **composição/ordem e recuperação efetiva NÃO VERIFICADAS**. Não aplicar um segundo desconto/refund. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../skills/../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../skills/individual-skill-cards-2.0.178.json) · [contrato técnico](../skills/../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
