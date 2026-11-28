# Catch Flame

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:catch_flame` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `CatchFlameImpactEntity` e `CatchFlameServerConfig`/`CatchFlameLoaderHooks` pertencem à raiz; `ThermalSunderedLogic` é consumidor compartilhado com Thermal Slice |
| Escola | `SchoolRegistry.FIRE_RESOURCE` (Fire) |
| Raridade mínima declarada | `UNCOMMON` |
| Níveis declarados | 1–8 (`setMaxLevel(8)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `0.5 s` |
| Recurso | Mana do Iron's (`baseManaCost=10`, `manaCostPerLevel=3`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.catchflame.CatchFlame` |
| Auxiliares da mesma raiz | `CatchFlameImpactEntity`, `CatchFlameLoaderHooks`, `CatchFlameServerConfig`, `DamageTypes.CATCH_FLAME`, `DamageTypes.CATCH_FLAME_PENETRATE` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("catch_flame", CatchFlame::new)` |
| Config | `UNCOMMON`, nível 8, cooldown `0.5`, `FIRE_RESOURCE`, `CastType.LONG` |
| Coeficientes | <init>: `baseSpellPower=800`, `spellPowerPerLevel=75`, `baseManaCost=10`, `manaCostPerLevel=3`, `castTime=10` |
| Dano | `getDamage` → `power/100 * damageMultiplier(CATCH_FLAME)` |
| Queima | `getBurnDuration` → `max((spellLevel-1)*20, 10)` ticks |
| Alcance | `getRange() = 3.0F`; raycast de `Block.OUTLINE` com largura `0.0` |
| Volume | `AABB(impact,impact).inflate(0.5)`; `BLOCK_SURFACE_EPSILON=1.0E-4` desloca a origem de linha de visão |
| Ignição | `allowSpellDispenserIgnition=true`, `allowNonPlayerIgnition=false` em `CatchFlameServerConfig` |
| Partículas | `FIRE_PARTICLE_COUNT=6`; `CatchFlameImpactEntity` dura `2` ticks no servidor e não é salvo |

Bytecode: scratch/fire5_evidence/javap1011_fire6.txt (`javap -classpath <JAR> -p -s -c`, 28 classes, 1.095.867 bytes, EXIT=0, SHA-256 `F5491A50DCF3A8F7EBF1E9C035EFE0723490C97475DE501FC3AF6C1580E17EDB`, SHA-1 `53C2C327705603172618C84CFFEFC41412683190`); decompilação de apoio: scratch/fire5_sources.txt (fontes Vineflower 1.12.0 das cinco raízes legadas e auxiliares, 188.994 bytes, SHA-256 `F8BE6DF48A22522FC1B23FBA362D8FD0F2637A2759D65739F25A723A2903A448`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCast` executa no servidor: resolve alvo, tenta ignição de bloco, afeta entidades, gera partículas e cria o `CatchFlameImpactEntity`.
2. `resolveCastTarget` parte do olho, usa `getViewVector(1.0F)` e raycast de `3.0` blocos; entidade válida vira impacto direto, bloco registra posição/face e ausência de alvo vira ponto a `3.0` blocos.
3. `affectEntities` usa AABB inflada `0.5`, `resolveUniqueCombatTargets`, interseção de hitbox, `isValidCombatTarget` e `RaycastTools.hasLineOfSight` com origem deslocada pela normal da face.
4. O dano usa `CATCH_FLAME` quando a vítima não está queimando e `CATCH_FLAME_PENETRATE` quando `getRemainingFireTicks() > 0`; `KnockbackTypes.DEFAULT`.
5. Se o dano foi aplicado, `ThermalSunderedLogic.extendFromSuccessfulFireDamage` atualiza `ThermalSundered` e a queima é elevada a `max((level-1)*20,10)` ticks quando menor.
6. `tryIgnition` exige bloco e face, config habilitada, `mayInteract` e `mayUseItemAt`; usa `FLINT_AND_STEEL.useOn` ou `EssenceSmokerBlockEntity.ignite(gameTime)` com hook adicional.
7. A entidade de impacto apenas reproduz partículas no cliente uma vez e é descartada no servidor no tick `2`.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Entidade em raycast de `3.0` blocos ou volume de impacto ao redor do ponto |
| Filtro | `CombatTools.isValidCombatTarget` contra o combat actor resolvido (owner remoto quando aplicável) |
| Geometria | AABB isotrópica de raio `0.5` no impacto; linha de visão com deslocamento `1.0E-4` para fora da face |
| Dano | `CATCH_FLAME` ou `CATCH_FLAME_PENETRATE`, conforme fogo restante na vítima |
| Ignição de bloco | Config `allowSpellDispenserIgnition=true` e `allowNonPlayerIgnition=false`, portas adicionais `mayInteract`/`mayUseItemAt`/loader hook |
| Tempo | Impacto visual `2` ticks; sem AOE persistente |
| Persistência | Nenhuma entidade persistente; `shouldBeSaved=false` no impacto |

## 5. Resultado

- Dano direto curto com transição de tipo de dano para alvos já em chamas.
- A queima é status vanilla aplicado como `setRemainingFireTicks`, com piso `10` ticks.
- `ThermalSundered` é efeito compartilhado com Thermal Slice; aqui ele é apenas estendido após dano bem-sucedido, não aplicado do zero.
- Ignição de blocos é efeito separado, condicionado por config e permissão; não é uma nova magia.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `800 + 75*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `power/100 * damageMultiplier(CATCH_FLAME)` — config **NÃO VERIFICADA** |
| Queima | `max((level-1)*20, 10)` ticks; piso `10` no nível 1 |
| Mana | `10 + 3*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `0.5` s declarado; efetivo **NÃO VERIFICADO** |
| Cast time | `10` ticks no construtor, com `CastType.LONG` |
| Alcance | `3.0` blocos, constante estática consumida no raycast |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde a `getSpellPower`; duração de queima depende apenas do nível efetivo.
- **B — evento verificado:** `ThermalSunderedEvents` reage a `LivingDamageEvent.Post` por `ON_FIRE`, mas é extensão de efeito, não mutador de parâmetros da magia.
- **C — adapter condicionado:** alterar alcance, tipo de dano ou regras de ignição exigiria substituir o fluxo de cast e os gates de permissão. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar o impacto em AOE persistente ou Ignição ilimitada sem duplicar dano/efeito. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast longo → raycast 3 blocos → dano CATCH_FLAME/CATCH_FLAME_PENETRATE em AABB 0.5 → queima e extensão de ThermalSundered → ignição condicionada de bloco → impacto visual 2 ticks`.

## 9. Concepção de nova magia

Assinatura ocupada: chama de curto alcance que alterna tipo de dano contra alvos em chamas e pode acender blocos sob regras de configuração. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `800/75/10/3/10`, `UNCOMMON/8/0.5`, alcance `3.0`, AABB `0.5`, burn `max((level-1)*20,10)`, dois tipos de dano, config de ignição e impacto `2` ticks confirmados no bytecode 1.0.1.1.
- ✅ `ThermalSunderedLogic.extendFromSuccessfulFireDamage` e o deslocamento `1.0E-4` da origem de linha de visão confirmados.
- ⚠️ configuração efetiva de `allowSpellDispenserIgnition`/`allowNonPlayerIgnition`, multiplicador e mana/cooldown instalados permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, ignição real, dispenser ou essence smoker.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: chama de curto alcance que alterna tipo de dano contra alvos em chamas e pode acender blocos sob regras de configuração. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
