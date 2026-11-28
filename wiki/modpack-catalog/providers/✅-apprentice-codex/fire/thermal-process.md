# Thermal Process

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:thermal_process` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<ThermalProcessThrowerEntity>`) |
| Interfaces | `ICraftsmansDelightAffectedSpell`, `IMagiAgentSuitAffectedSpell`; efeito `ThermalProcessing` e ponte Create pertencem à raiz |
| Escola | `SchoolRegistry.FIRE_RESOURCE` (Fire) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1–3 (`setMaxLevel(3)`) |
| Tipo de cast | `CONTINUOUS` |
| Cooldown declarado | `20.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=10`, `manaCostPerLevel=5`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.thermalprocess.ThermalProcess` |
| Auxiliares da mesma raiz | `ThermalProcessThrowerEntity`, `ThermalProcessThrowerRenderer`, `effect.ThermalProcessing`, `CreateExposedItemProcessingBridge`, `ProcessingRecipeDenylist` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("thermal_process", ThermalProcess::new)` |
| Config | `RARE`, nível 3, cooldown `20.0`, `FIRE_RESOURCE`, `CastType.CONTINUOUS` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=150`, `baseManaCost=10`, `manaCostPerLevel=5`, `castTime=200` |
| Dano | `getDamage(power)` → `(0.5 + 1.5*power/100) * damageMultiplier(THERMAL_PROCESS)` |
| Processamento | `getBurnItemPerSecond` → `2*power/100`, com `CraftsmansDelight.applyProcessSpeedBonus` quando habilitado |
| Alcance | `getRange() = 12.0F`; `raycastFromEye(owner, range, 0.5, ...)` |
| Feixe | `ATTACK_START_DELAY_TICKS=10`, `ATTACK_SAMPLE_STEP=0.2`, `ATTACK_RADIUS=0.25`, `FIRE_OFFSET=0.65` |
| Itens | `ITEM_PROCESS_INTERVAL_TICKS=20`, `ITEM_PROCESS_RADIUS=0.5`, orçamento `pendingItemProcessBudget` |
| Efeito | `ThermalProcessing`: `BASE_DURATION_TICKS=40`, `MAX_AMPLIFIER=5`, `IGNITE_TICKS=240` |
| Mobilidade | `isCraftsmansDelightCastingMobilityEnabled()` retorna `true`; bônus do Curio é provider-owned |

Bytecode: scratch/fire5_evidence/javap1011_fire6.txt (`javap -classpath <JAR> -p -s -c`, 28 classes, 1.095.867 bytes, EXIT=0, SHA-256 `F5491A50DCF3A8F7EBF1E9C035EFE0723490C97475DE501FC3AF6C1580E17EDB`, SHA-1 `53C2C327705603172618C84CFFEFC41412683190`); decompilação de apoio: scratch/fire5_sources.txt (fontes Vineflower 1.12.0 das cinco raízes legadas e auxiliares, 188.994 bytes, SHA-256 `F8BE6DF48A22522FC1B23FBA362D8FD0F2637A2759D65739F25A723A2903A448`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCastNoWeapon` cria o thrower com dano, alcance e velocidade de processamento; aplica mobilidade de Craftsman's Delight quando habilitada.
2. `tickOnServer` segue `calculateBehindPosition(owner,-0.5,0.7,-0.25)`, mira via `raycastFromEye` com raio `0.5` e, após `10` ticks de startup, chama `fireBeam`.
3. `fireBeam` inicia em `position + look*0.65`, termina no bloco ou em `12.0` blocos, cria `DamageTypes.THERMAL_PROCESS` e recalcula dano quando `spellLevel > 0`.
4. `RaycastTools.sampleBeamHits(level, start, end, 0.25, 0.2, ...)` aplica dano com `NO_KNOCKBACK`; em sucesso, `applyOrUpdateThermalProcessing`.
5. `applyOrUpdateThermalProcessing` exige `!isFireResistant`, incrementa o amplificador até `5`, aplica `ThermalProcessing` por `40` ticks e, no amplificador `5`, chama `igniteForSeconds(12.0F)` (`240` ticks).
6. A cada `20` ticks, `processBeamItems` adiciona `burnItemPerSecond` ao orçamento, processa itens na ordem de distância e usa `CreateExposedItemProcessingBridge.processBlocks` para blocos Create quando sobra orçamento.
7. `tryBuildProcessingResult` usa `ProcessingRecipeDenylist.findThermalProcessRecipe`, `SingleRecipeInput` e `AbstractCookingRecipe.assemble`, respeitando `maxProcessCount`.
8. `ThermalProcessing.applyEffectTick` só executa quando `duration == 1` e reaplica o efeito com amplificador reduzido em um; `addEffect` na aplicação não sobrescreve efeitos (`false,true,true`).

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Entidades ou `ItemEntity` amostrados ao longo do feixe de até `12.0` blocos |
| Filtro | `e != thrower && e != owner && CombatTools.isValidCombatTarget`; `ItemEntity` é alvo de processamento |
| Geometria | amostragem `ATTACK_RADIUS=0.25` com passo `0.2`; itens usam AABB inflada `0.5` |
| Dano | `DamageTypes.THERMAL_PROCESS`, `KnockbackTypes.NO_KNOCKBACK`, dano recalculado por `getSpellPower` |
| Efeito | `ThermalProcessing` 40 ticks; multiplicador de velocidade `-0.1*amplificador` e armadura `-2*(amplificador-1)` |
| Ignição | Amplificador `5` aplica 240 ticks de fogo; efeito exige alvo não resistente a fogo |
| Tempo | startup `10` ticks, processamento a cada `20` ticks |
| Persistência | NBT com `Damage`, `Range`, `BurnItemPerSecond`, `PendingItemProcessBudget` e `StartupTick`; itens processados são marcados por UUID/identidade |

## 5. Resultado

- Dano de feixe contínuo com efeito `ThermalProcessing` acumulativo por amplificador.
- Processamento de itens é uma segunda função da mesma raiz, com orçamento por `20` ticks e receitas culinárias permitidas pela denylist do provider.
- `CraftsmansDelight.applyProcessSpeedBonus` pode alterar a velocidade efetiva; o bônus real depende do equipamento e da config, ambos `NÃO VERIFICADOS`.
- Sem invocação múltipla, projétil independente ou cura (`N/A` com justificativa: o thrower é uma arma conjurada fixa).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 150*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `(0.5 + 1.5*power/100) * damageMultiplier(THERMAL_PROCESS)` — config **NÃO VERIFICADA** |
| Itens/s | `2*power/100`, antes de eventual bônus de Craftsman's Delight |
| Mana | `10 + 5*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `20.0` s declarado; efetivo **NÃO VERIFICADO** |
| Cast time | `200` ticks no construtor, com `CastType.CONTINUOUS` |
| Alcance | `12.0` blocos, consumido em `raycastFromEye` e no comprimento do feixe |
| Efeito | `40` ticks base, amp máx `5`, ignição `240` ticks no amp `5` |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano e itens/s respondem a `getSpellPower`; o Curio Craftsman's Delight já altera processamento e mobilidade por contrato provider-owned.
- **B — evento verificado:** `ThermalProcessing.applyEffectTick` é um tick de efeito interno, não um hook externo de mutação.
- **C — adapter condicionado:** alterar a amostragem do feixe, orçamento de itens ou regras de receita exigiria substituir o thrower e a ponte Create. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar o feixe em AOE persistente ou duplicar processamento sem duplicar dano/itens. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast contínuo → thrower em standby → startup 10 ticks → feixe 12 blocos com amostragem 0.25/0.2 → dano THERMAL_PROCESS + ThermalProcessing → processamento de itens a cada 20 ticks e ponte Create`.

## 9. Concepção de nova magia

Assinatura ocupada: feixe contínuo que combina dano, debuff escalonado e processamento de itens/receitas. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `100/150/10/5/200`, `RARE/3/20.0`, dano `(0.5+1.5*power/100)*multiplier`, `2*power/100` itens/s, alcance `12`, startup `10`, intervalo `20`, constantes de geometria e efeito `40/5/240` confirmados no bytecode 1.0.1.1.
- ✅ `applyOrUpdateThermalProcessing`, `resolveCurrentDamage`, denylist de receitas e ponte Create confirmados.
- ⚠️ bônus efetivo de Craftsman's Delight, multiplicador instalado, mana/cooldown e receitas do pack permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, processamento real, Create, mobilidade ou PvP.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: feixe contínuo que combina dano, debuff escalonado e processamento de itens/receitas. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
