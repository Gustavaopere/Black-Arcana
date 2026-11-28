# Slash Blade

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:slash_blade` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<SlashBladeKatanaEntity>`) |
| Interfaces | `GeoEntity`, `ISwordTrailEntity` na katana; `DamageTypes.SLASH_BLADE` pertence à raiz |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `COMMON` |
| Níveis declarados | 1–10 (`setMaxLevel(10)`) |
| Tipo de cast | `configurado pelo host (`castTime=15`)` |
| Cooldown declarado | `1.5 s` |
| Recurso | Mana do Iron's (`baseManaCost=10`, `manaCostPerLevel=3`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.slashblade.SlashBlade` |
| Auxiliares da mesma raiz | `SlashBladeKatanaEntity`, `HorizontalOrientedBox`, `OrientedBoxHit`, `DamageTypes.SLASH_BLADE` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("slash_blade", SlashBlade::new)` |
| Config | `COMMON`, nível 10, cooldown `1.5`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=400`, `spellPowerPerLevel=50`, `baseManaCost=10`, `manaCostPerLevel=3`, `castTime=15` |
| Dano | `getDamage` → `power/100 * damageMultiplier(SLASH_BLADE)` |
| Penetração | `getBlockPenetrationDamageMultiplierPercent` → `clamp(20 + level*5, 10, 90)`%; multiplicador `/100` |
| Alcance | `getRange()` → `SlashBladeKatanaEntity.getAttackDepth()` = `5.0` |
| Caixa | `HorizontalOrientedBox(position, getLookAngle(), 2.75, 0.75, 4.5)` |
| Dano aplicado | `hitsHorizontalOrientedBox` → `createCombatDamageSource(DamageTypes.SLASH_BLADE)` + `CombatTools.applySpellDamage` |
| Bloqueio | `blockOccluded()` → dano × multiplicador e `KnockbackTypes.NO_KNOCKBACK`; sem bloqueio → dano cheio e `DEFAULT` |
| NBT | `Damage`, `BlockPenetrationDamageMultiplier` (setter clamp `0..1`) |

Bytecode: scratch/javap1011_evocation7.txt (`javap -classpath <JAR> -p -s -c`, 94 classes, EXIT=0, SHA-256 `AF225F42FA1A0295D7339542D49620FBA0D0BE6599147EEDF69B75744730DB41`); decompilação de apoio: scratch/evocation7_sources.txt (46 fontes Vineflower 1.12.0, SHA-256 `05090319D9206171C8C4C38ED1A33479F0F1313F9135B5D70146F5559EB80DB1`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCast` cria a katana, define `setDamage(getDamage(...))` e `setBlockPenetrationDamageMultiplier(...)`.
2. No standby, `setStandby` dispara animação e define `ANIMATION_SPEED=1.5 * max(1, castTimeSpeedScale)`; `SHOW_TRAIL=false`.
3. `slash()` exige dono vivo: `refreshAttackPose` move a katana por `moveToCollisionLimitedStandbyPosition` desde `calculateBehindPosition(owner,0,0,-0.75)` até `getStandbyPosition()` (`calculateBehindPosition(owner,-0.5,0,-0.75)`), iguala a rotação à do dono e dispara `quickdraw`. A constante `FOLLOW_FORWARD_OFFSET=0.5` existe, mas não é consumida nesse método.
4. `ANIMATION_SPEED=3.0`, `SHOW_TRAIL=true`, `lifeTick=10` e `isSlashed=true`; a caixa `2.75 × 0.75 × 4.5` é testada com `hitsHorizontalOrientedBox`, excluindo o dono.
5. Cada `OrientedBoxHit` aplica dano via `DamageTypes.SLASH_BLADE`; bloqueios recebem `damage * blockPenetrationDamageMultiplier` e `NO_KNOCKBACK`.
6. `tickOnServer` decrementa `lifeTick` após o corte e descarta a katana ao chegar a zero; sem dono, descarta imediatamente.
7. `getStandbyPosition` usa `calculateBehindPosition(owner,-0.5,0,-0.75)`.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Entidades em `HorizontalOrientedBox(position, look, 2.75, 0.75, 4.5)`, exceto o dono |
| Filtro | `CombatTools.isValidCombatTarget(e, owner)` |
| Geometria | Meia-largura `2.75`, meia-altura `0.75`, profundidade `4.5`; `getAttackDepth=5.0` é o alcance declarado |
| Bloqueio | `blockOccluded()` reduz o dano ao multiplicador e suprime knockback |
| Tempo | `10` ticks de `lifeTick` após o corte |
| Projétil | Nenhum; dano direto na caixa orientada |
| Persistência | NBT `Damage` e `BlockPenetrationDamageMultiplier`; katana é entidade supervisionada |

## 5. Resultado

- Dano direto em caixa orientada; tipo `DamageTypes.SLASH_BLADE`.
- A penetração é um multiplicador de dano para alvos ocultos por bloco, não um segundo dano ou projétil.
- Knockback é `DEFAULT` sem bloqueio e `NO_KNOCKBACK` com bloqueio; `KATANA_SLASH` e `PLAYER_ATTACK_SWEEP` são feedback.
- Sem cura, status, invocação múltipla ou AOE persistente (`N/A` com justificativa).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `400 + 50*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `power/100 * damageMultiplier(SLASH_BLADE)` — config **NÃO VERIFICADA** |
| Penetração | `clamp(20 + level*5, 10, 90)`% → multiplicador `0.1..0.9` |
| Alcance | `5.0` (`getAttackDepth`), enquanto a caixa física usa profundidade `4.5` |
| Mana | `10 + 3*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `1.5` s declarado |
| Cast time | `15` ticks no construtor |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde ao poder; penetração depende do nível, não de atributos.
- **B — evento verificado:** `ISwordTrailEntity`/`GeoEntity` são apresentação, não contrato de mutação.
- **C — adapter condicionado:** alterar geometria, penetração ou knockback exigiria substituir `SlashBladeKatanaEntity` com risco de duplicar dano. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar o corte em AOE persistente ou alterar a caixa sem duplicar casting. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast → katana em standby → slash em caixa 2.75×0.75×4.5 → dano SLASH_BLADE com penetração/knockback condicionais → descarte em 10 ticks`.


## 9. Concepção de nova magia

Assinatura ocupada: katana conjurada com corte em caixa orientada e penetração de bloco. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `400/50/10/3/15`, dano `power/100*multiplier`, penetração `clamp(20+level*5,10,90)%`, caixa `2.75/0.75/4.5`, `getAttackDepth=5.0`, animação `1.5`/`3.0`, NBT e ramos de bloqueio confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador instalado, mana/cooldown efetivos e comportamento real contra blocos permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, bloqueio real ou modificação da katana.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: katana conjurada com corte em caixa orientada e penetração de bloco. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
