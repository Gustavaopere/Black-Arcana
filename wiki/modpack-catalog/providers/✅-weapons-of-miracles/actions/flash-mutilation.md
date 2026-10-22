# Flash Mutilation

- Provider: **Weapons of Miracles** (`wom`)
- Version: `2.0.178`
- Exact physical/publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`
- Skill id: `wom:flash_mutilation`
- Owner: `wom:nova`
- Skill category: Weapon Innate
- State: `CONDITIONAL`

## Semantic identity

Flash Mutilation is an exact-current supernatural action that performs a teleport sequence around a target followed by provider attack settlement.

Individual teleports and follow-up hits are phases of this one root.

## Owner binding

The exact weapon capability maps `wom:nova` to `wom:flash_mutilation`.

## Reachability gate

The audited exact recipe, chest-loot and provider drop surfaces do not close a normal current acquisition route for Nova.

The bounded audit intentionally does not infer global unreachability because external scripts/datapacks may exist. Therefore this root remains `CONDITIONAL`, not strict-counted.

## Boundary

WOM owns target selection, teleport sequence, attack settlement and owner state.

Source: `../EXACT-2.0.178-ARTIFACT-AUDIT.md`; `../skills/SKILL-DISPOSITION-2.0.178.md`.

## Ficha técnica para perks — 2.0.178

**ID:** `wom:flash_mutilation` · **categoria:** Weapon Innate · **disposição mágica:** `CONDITIONAL`.

Executa a sequência NOVA_FLASH_MUTILATION. A arma Nova existe no registro, mas sua aquisição normal permanece condicional no levantamento atual.

**Estado:** ⚠️ `EXACT_BINARY_LOCATORS + PACKAGED_PARAMETERS`; consumidores/constantes específicos abaixo auditados estaticamente; cadeia downstream e integração mutadora por jogador parciais. Gameplay/modpack **PENDING**.

**Proveniência:** JAR físico/publisher 2.0.178, SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; modlist RPG `ed5b65b890767b406ce41127bcb793775263c7bd`. Host binário Epic Fight **21.17.3.1**; pack **NeoForge 21.1.250 / Java 21**. [Método, hashes e limites](../skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md). Sem fonte Java exata presumida a partir de outra versão.

### Registro e código localizável

- Registrar: `reascer.wom.gameasset.WOMSkills.FLASH_MUTILATION` → supplier `lambda$static$53(ResourceLocation)` → `reascer.wom.skill.weaponinnate.FlashMutilatorSkill`. O verificador confere o vínculo ID→invokedynamic→bootstrap→supplier, não só a presença da string.
- Classe no JAR: `reascer/wom/skill/weaponinnate/FlashMutilatorSkill.class`; base `yesman.epicfight.skill.weaponinnate.WeaponInnateSkill`. Recurso do builder **`WEAPON_CHARGE`**; chamadas explícitas durante callbacks podem usar outro recurso.
- `public void executeOnServer(yesman.epicfight.skill.SkillContainer, net.minecraft.nbt.CompoundTag)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;Lnet/minecraft/nbt/CompoundTag;)V`.
- `public boolean canExecute(yesman.epicfight.skill.SkillContainer)` · descritor JVM `(Lyesman/epicfight/skill/SkillContainer;)Z`.

**Referências compiladas por método** (presença/localização, não prova de execução de todos os ramos):

Não há referência selecionada a evento/consumer ofensivo na classe concreta; isso não exclui comportamento na base, capability ou animação.

### Parâmetros empacotados e consumidor

Arquivo `data/wom/skill_parameters/flash_mutilation.json`:

| Campo | Valor RAW | Consumidor / limite |
|---|---|---|
| `consumption` | `48.0` | `Skill.loadDatapackParameters(CompoundTag)` → campo float `consumption`; recurso do builder e gastos explícitos são descritos separadamente. |
| `max_stacks` | `4` | Loader base → int `maxStackSize`; capacidade declarada, não quantidade de alvos. |

### Campos que uma perk pode precisar

| Eixo | Valor / código / limite | Integração atual |
|---|---|---|
| Dano / cura / tipo | Dano, cura, modifiers e fontes: seguir os consumidores/callbacks localizados acima. Valor final e registry DamageType completo **NÃO VERIFICADOS**; nome temático, stun e tag não determinam tipo de dano. | ⛔ novo DamageType/modifier por jogador sem contrato validado |
| Alcance / alvo / área | `executeOnServer` chama `AnimsNova.NOVA_FLASH_MUTILATION`; `canExecute` delega à base. Distância de teleporte, seleção do alvo e colisão pertencem ao pipeline da animação e NÃO foram fechadas aqui. | ⛔ retarget/single→AOE/range sem hook seguro |
| Projétil / hitbox / tamanho | A classe concreta não cria projétil diretamente; a sequência NOVA_FLASH_MUTILATION precisa de inspeção downstream para excluir/confirmar cada entidade/colisão. | ⛔ escrita em collider/escala sem contrato seguro |
| Tempo / duração / cooldown | Tempos dependem dos contadores/estados listados, animações e base. Unidades e duração efetiva/cast/cooldown final **NÃO VERIFICADOS**, salvo valor/consumidor específico acima. | ⚠️ parâmetro nativo não equivale a setter por perk |
| Custo / recurso / refund | Recurso declarado do builder: **WEAPON_CHARGE**. Parâmetros RAW e chamadas explícitas de consumo/refund acima são caminhos distintos; débito líquido e composição de listeners **NÃO VERIFICADOS**. | ⚠️ reutilizar contrato RPG só em eventos STAMINA elegíveis; NONE/COOLDOWN/WEAPON_CHARGE não recebem desconto automático |

### Contrato entre os três projetos e QA

O [RPG Skill Tree já possui hooks de stamina, dodge e dano](../skills/../../✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md). A ficha não cria bridge WOM dedicada: a incidência do hook genérico depende de `ServerPlayerPatch`, elegibilidade, recurso do evento e pipeline realmente usado. `CONSUME_SKILL` é preflight, não resultado; callbacks/FX/efeitos secundários não concedem Mastery novamente. Montantes negativos e callbacks de recuperação exigem composição auditada.

**Owners:** WOM/Epic Fight executam skill, animação, recurso e settlement; RPG controla atributos/progressão/Mastery/perks/gates; Black Arcana controla seu runtime mágico, hazards e world safety; Enshrouded controla Shroud/exposure. Não cobrar, curar, teleportar, aplicar dano ou premiar uma segunda vez a partir desta documentação.

**Pendências:** ramo executável/side/ordem/cancelamento, recursos antes/depois, atributos de player conectado, equip/unequip, reload/relog/respawn, target/LOS/PvP/claims, multiplayer, causa/proc e modpack completo. Nenhum PASS estático avança Stage 06.05 ou Stage 09 físico.

[Índice dos 64 IDs](../skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md) · [manifesto verificável](../skills/individual-skill-cards-2.0.178.json) · [contrato técnico](../skills/../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md).
