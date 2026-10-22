# Avatar of Might

- Provider: **Weapons of Miracles** (`wom`)
- Version: `2.0.178`
- Exact physical/publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`
- Skill id: `wom:avatar_of_might`
- Skill category: Identity
- State: `COUNTED_EXACT`

## Semantic identity

Avatar of Might is a deliberate charged provider action whose exact disposition closes a shockwave plus temporary defensive/stun-immunity state.

Charge handling, shockwave settlement and the temporary state are phases/effects of one supernatural root rather than separate spell identities.

## Reachability

The exact WOM Epic Skills tree includes `wom:avatar_of_might`, closing provider-native acquisition at catalog level.

## Boundary

WOM owns charge eligibility, shockwave behavior, status duration and all resource/cooldown settlement. No tuning value is inferred here.

Source: `../EXACT-2.0.178-ARTIFACT-AUDIT.md`; `../skills/SKILL-DISPOSITION-2.0.178.md`.

## Ficha técnica para perks — 2.0.178

**ID:** `wom:avatar_of_might` · **categoria:** Identity · **disposição mágica:** `COUNTED_EXACT`.

Ação de impacto com preparação/estado e reação ligada a TAKE_DAMAGE_INCOME. O callback possui débito explícito de stamina, consulta de entidades e imunidade a stun.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.AVATAR_OF_MIGHT` → supplier `lambda$static$38(ResourceLocation)` → `reascer.wom.skill.identity.AvatarOfMightSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/identity/AvatarOfMightSkill.class`; base `yesman.epicfight.skill.Skill`. Recurso do builder **`NONE`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void onInitiate(yesman.epicfight.skill.SkillContainer, yesman.epicfight.api.event.EntityEventListener)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lyesman/epicfight/api/event/EntityEventListener;)V`.
- `public void updateContainer(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)V`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

| Método/callback | Eventos, consumidores e fronteiras encontrados |
|---|---|
| `onInitiate` | `yesman.epicfight.api.event.EpicFightEventHooks$Entity.TAKE_DAMAGE_INCOME` |
| `lambda$onInitiate$0` | `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.setStamina`, `yesman.epicfight.skill.Skill$Resource.STAMINA`, `yesman.epicfight.world.capabilities.entitypatch.player.PlayerPatch.consumeForSkill`, `yesman.epicfight.registry.entries.EpicFightMobEffects.STUN_IMMUNITY`, `net.minecraft.world.entity.player.Player.removeEffect`, `net.minecraft.world.entity.player.Player.addEffect`, `yesman.epicfight.world.damagesource.EpicFightDamageSource.setStunType`, `net.minecraft.world.phys.AABB.ofSize`, `net.minecraft.world.entity.ai.attributes.Attributes.KNOCKBACK_RESISTANCE` |

**Estado do provider referenciado:** `COOLDOWN`, `TIMER`. Não é API pública de mutação externa.

### Parâmetros empacotados e consumidor

**Sem JSON próprio** `data/wom/skill_parameters/avatar_of_might.json` no JAR exato. Ausência não significa custo zero ou falta de estado: consultar construtor, callbacks e base.

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | `lambda$onInitiate$0` PCs 417–429: `AABB.ofSize(player.position(),20,20,20)` para consulta. São dimensões totais da caixa (±10 por eixo), não raio esférico 20, nem colisão/hit garantido. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | Projétil próprio, escala visual, collider, velocidade e lifetime **NÃO VERIFICADOS** na cadeia completa. Nenhuma API externa de tamanho foi homologada; para passivas/guarda/movimento não acrescentar projétil por inferência temática. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | Sem JSON próprio. Em `lambda$onInitiate$0`, PCs 110–122, existe chamada **consumeForSkill(this, STAMINA, 12)**; o retorno é descartado nesse ponto. Isso não prova gasto bem-sucedido nem direito a reward. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../skills/../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../skills/individual-skill-cards-2.0.178.json) · [contrato técnico](../skills/../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
