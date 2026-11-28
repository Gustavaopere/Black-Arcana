# Thermal Slice

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:thermal_slice` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<ThermalSliceKatanaEntity>`) |
| Interfaces | `IMulticastUnsupportedSpell`; katana `GeoEntity`/`ISwordTrailEntity`, `ThermalSliceMovementEvent`, `ThermalSunderedLogic/Events` e `ThermalSundered` pertencem à raiz |
| Escola | `SchoolRegistry.FIRE_RESOURCE` (Fire) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1–5 (`setMaxLevel(5)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `6.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=40`, `manaCostPerLevel=10`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.thermalslice.ThermalSlice` |
| Auxiliares da mesma raiz | `ThermalSliceKatanaEntity`, `ThermalSliceMovementEvent`, `ThermalSunderedLogic`, `ThermalSunderedEvents`, `effect.ThermalSundered`, `DamageTypes.THERMAL_SLICE` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("thermal_slice", ThermalSlice::new)` |
| Config | `RARE`, nível 5, cooldown `6.0`, `FIRE_RESOURCE`, `CastType.LONG`, `canBeInterrupted()=false` |
| Coeficientes | <init>: `baseSpellPower=500`, `spellPowerPerLevel=200`, `baseManaCost=40`, `manaCostPerLevel=10`, `castTime=10` |
| Dano | `getDamage` → `power/100 * damageMultiplier(THERMAL_SLICE)` |
| Alcance informativo | `getRange()` → `ThermalSliceKatanaEntity.getAttackDepth() = 4.2` |
| Caixa real | `HorizontalOrientedBox(position, look, 0.5, 1.5, 4.0)` com literal `4.0`; `ATTACK_DEPTH=4.0` e `getAttackDepth()=4.2` são grandezas distintas |
| Dash | `DASH_DURATION_TICKS=4`, `DASH_DISTANCE=3.5`, estado `THERMAL_SLICE_STATE` em `CodexSpellData` |
| Efeito | amp `clamp(level-1,0,4)`, `ThermalSundered` `60` ticks e extensão para `100` ticks |
| Katana | `STAY_SLASHED_TICK=12`, `ATTACK_HALF_WIDTH=0.5`, `ATTACK_HALF_HEIGHT=1.5`, `FOLLOW_FORWARD_OFFSET=0.2` declarado |
| Resistência | `ThermalSundered`: `FIRE_MAGIC_RESIST` `-0.1*(clamp+1)`, máx `4` |

Bytecode: scratch/fire5_evidence/javap1011_fire6.txt (`javap -classpath <JAR> -p -s -c`, 28 classes, 1.095.867 bytes, EXIT=0, SHA-256 `F5491A50DCF3A8F7EBF1E9C035EFE0723490C97475DE501FC3AF6C1580E17EDB`, SHA-1 `53C2C327705603172618C84CFFEFC41412683190`); decompilação de apoio: scratch/vf_apprentice1011/.../thermalslice/ e effect/ (sete fontes Vineflower 1.12.0 SHA-exatas, SHA-256 individuais `B4FC1E141EFEED22CCF4B2A39882FAC4684B0471664BB4D6DA2E1A939DA7814A`, `D3CA2923655978B45A7D82046FB2ABDFFBC6760027F26938BEB5BACA1CB2D889`, `9596D21FE4577780512B39E2D8DC8D7BC6E9FBAFCAE0C6ABB9847340D47229C1`, `78C077DD6F90730040918AC7817DF5224777EEDDAB299A67038E31F9B4D5284A`, `CE7923F7C2AEA10F7E77750B0FA4704B15297004E6482BD249DD0BFB6B887929`, `CB95A98A5F97093DFB7D991B3E1AC60841D188F543F38839CB324158F58EF556` e `803087994EE5FA9C7674DF78F71670E1DD3E771C3AB8B554FDA13EE28ED4D3AE`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCastNoWeapon`/`onInitialCastWithWeapon` gravam dano e amplificador na katana; `onCastTickWithWeapon` ajusta a animação de standby pelo `castTimeSpeedScale`.
2. `onCastCompleteWithWeapon`: cast cancelado libera a arma; caso contrário tenta `ThermalSliceMovementEvent.startDash(entity, weapon.getId())` e só chama `weapon.slash(level)` se o dash não iniciar.
3. `startDash` exige `Player` vivo e sem passageiro, grava 4 ticks, distância `3.5`, origem/destino e o id da katana no estado persistente do jogador.
4. `PlayerTickEvent.Pre` interpola X/Z para o destino; `Post` finaliza ao atingir `4` ticks ou `horizontalCollision`, zerando apenas o movimento horizontal e chamando `blade.slash` no servidor.
5. `slash` usa caixa orientada `0.5 × 1.5 × 4.0`, cria `DamageTypes.THERMAL_SLICE`, define `lifeTick=12`, trail ativo e animação `1.5`, e aplica dano a alvos válidos não ocultos.
6. Após dano bem-sucedido em `LivingEntity`, `ThermalSunderedLogic.applyFromThermalSlice` exige `!CombatTools.isFireResistant` e aplica `ThermalSundered` com no mínimo `60` ticks e amplificador clampado.
7. `ThermalSunderedEvents.onLivingDamage` estende o efeito para `100` ticks em `LivingDamageEvent.Post` servidor quando o dano é positivo e a fonte é `DamageTypes.ON_FIRE`.
8. katana é descartada quando `lifeTick` chega a zero; sem dono, descarta imediatamente.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Entidades na caixa orientada horizontal de meia-largura `0.5`, meia-altura `1.5` e profundidade `4.0`, exceto o dono |
| Filtro | `CombatTools.isValidCombatTarget` em `hitsHorizontalOrientedBox` |
| Oclusão | `hit.blockOccluded()` suprime dano e aplicação de `ThermalSundered` |
| Alcance declarado | `getAttackDepth()=4.2` é informativo; a caixa real usa o literal `4.0`, e nenhum consumidor de `ATTACK_DEPTH=4.0` foi identificado no corpo examinado |
| Knockback | `KnockbackTypes.DEFAULT` no dano direto |
| Dash | Apenas `Player`, 4 ticks, 3.5 blocos, interrompido por `horizontalCollision`; movimento vertical preservado |
| Efeito | `ThermalSundered` 60 ticks inicial, 100 ticks em dano de fogo, amp máx 4 |
| Persistência | katana serializa `Damage` e `ThermalSunderedAmplifier`; dash vive em `CodexSpellData` |

## 5. Resultado

- Dano direto em caixa orientada e debuff `ThermalSundered`, sem projétil.
- `ThermalSundered` reduz `FIRE_MAGIC_RESIST` em `-0.1*(amplificador+1)`, de `-10%` a `-50%` nos amplificadores `0..4`.
- A extensão do efeito por fogo é causalmente separada: `Catch Flame` e `Thermal Process` também a consomem, mas não criam uma nova magia.
- Sem cura, invocação múltipla ou AOE persistente (`N/A` com justificativa: a caixa é instantânea e a katana é descartada).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `500 + 200*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `power/100 * damageMultiplier(THERMAL_SLICE)` — config **NÃO VERIFICADA** |
| Amplificador | `clamp(level-1,0,4)` |
| Mana | `40 + 10*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `6.0` s declarado; efetivo **NÃO VERIFICADO** |
| Cast time | `10` ticks no construtor; `canBeInterrupted=false` |
| Dash | `4` ticks e `3.5` blocos; `FOLLOW_FORWARD_OFFSET=0.2` declarado, mas `getStandbyPosition` usa `(-0.2,0,-0.75)` |
| Efeito | `60` ticks inicial, `100` ticks após dano de fogo, resistência `-10%*(clamp+1)` |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde a `getSpellPower`; o amplificador de `ThermalSundered` depende do nível efetivo.
- **B — evento verificado:** `PlayerTickEvent.Pre/Post` e `LivingDamageEvent.Post` são callbacks reais, mas não expõem mutador de parâmetros do cast.
- **C — adapter condicionado:** alterar caixa, dash ou amplificador exigiria substituir katana/estado/eventos com risco de duplicar dano. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar o corte em AOE persistente ou alterar a resistência sem duplicar efeito. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast longo não interrompível → dash 4 ticks/3.5 blocos ou slash imediato → caixa 0.5×1.5×4.0 → dano THERMAL_SLICE → ThermalSundered 60/100 ticks com redução de FIRE_MAGIC_RESIST → katana descartada em 12 ticks`.

## 9. Concepção de nova magia

Assinatura ocupada: corte com katana conjurada, dash curto e debuff de resistência a fogo compartilhado. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `500/200/40/10/10`, `RARE/5/6.0`, dano `power/100*multiplier`, amp `clamp(level-1)`, caixa `0.5/1.5/4.0`, `getAttackDepth=4.2` informativo, dash `4/3.5`, `ThermalSundered` `60/100/4` e gating por fogo confirmados no bytecode e nas fontes SHA-exatas.
- ✅ `ThermalSunderedLogic.applyFromThermalSlice`, `ThermalSunderedEvents` e `FIRE_MAGIC_RESIST` `-0.1*(clamp+1)` confirmados.
- ⚠️ `ATTACK_DEPTH=4.0` e `FOLLOW_FORWARD_OFFSET=0.2` são constantes declaradas; a caixa usa o literal `4.0` e `getStandbyPosition` usa `-0.2`.
- ⚠️ multiplicador instalado, mana/cooldown efetivos, dash em cliente real e resistência efetiva permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, dash real ou teste de effect stack.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: corte com katana conjurada, dash curto e debuff de resistência a fogo compartilhado. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
