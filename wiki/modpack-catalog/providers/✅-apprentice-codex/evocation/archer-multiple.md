# Archer Multiple

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:archer_multiple` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | sem interface adicional declarada |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1–5 (`setMaxLevel(5)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `30.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=70`, `manaCostPerLevel=30`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.archermultiple.ArcherMultiple` |
| Auxiliares da mesma raiz | `ArcherMultipleBowEntity`, `ArcherMultipleEvents`, `ArcherMultipleCastData` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("archer_multiple", ArcherMultiple::new)` |
| Config | `RARE`, nível 5, cooldown `30.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=200`, `spellPowerPerLevel=50`, `baseManaCost=70`, `manaCostPerLevel=30`, `castTime=30` |
| Dano | `getDamage(int,LivingEntity)` → `power/100 * damageMultiplier(ARCHER_MULTIPLE)` |
| Quantidade/alcance | `getSummonCount()=4`, `getDuration()=600` ticks, `getRecastCount()=2`, pre-cast `Utils.preCastTargetHelper(...,64,1.0F,false)` |
| Arcos | `ArcherMultipleBowEntity`: `CHARGE_TICK=15`, `COOLDOWN_TICK=8`, `DELAY_FIRST_AUTO_LOCK_ON_SHOT_TICK=10`, `KEEP_LOCK_ON_TICK_FOR_CHANGE_TARGET=60`, `KEEP_LOCK_ON_TICK_IN_LOST_LOR=20`, `KEEP_FIRE_CONTINUE_TICK=40` |
| Auto-alvo | `RaycastTools.findNearestEntityInForwardBox(...,24.0,8.0,8.0,...)` |
| Dano do arco | `createCombatDamageSource(DamageTypes.ARCHER_MULTIPLE)` + `CombatTools.applySpellDamage(...,KNOCKBACK.DEFAULT)` |
| Estado/ciclo | `ArcherMultipleCastData`: UUIDs dos arcos + `ResourceLocation` da dimensão; `ArcherMultipleEvents` aplica `USER_CANCEL` em login/logout/troca de dimensão e `DEATH` na morte |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `checkPreCastConditions` tenta preencher `TargetEntityCastData` em até `64` blocos com `preCastTargetHelper(...,1.0F,false)`. Se não houver alvo, envia a mensagem `spell_target_none`, mas **retorna `true`**: o cast prossegue sem alvo prioritário e a busca automática dos arcos assume o alvo.
2. `onCast` lê `TargetEntityCastData`, cria quatro `ArcherMultipleBowEntity` via `EntityRegistry.ARCHER_MULTIPLE_BOW`, aplica `setPriorityTarget` e `setDamage(getDamage(...))`.
3. Cada arco segue o dono em formação (`getFormationPosition`) e recarrega com `15` ticks de carga + `8` ticks de cooldown; dispara somente com `target.isAlive()` e, quando aplicável, `invulnerableTime<=0`.
4. Sem alvo prioritário, a cada `10` ticks a busca automática usa a caixa frontal `24.0×8.0×8.0`; perda de linha de visão limpa o `autoTarget`, e a troca de alvo mantém disparo por `40` ticks.
5. `ArcherMultipleCastData` registra UUIDs e dimensão, serializando em buffer e NBT; `removeBow` encerra o estado quando a lista esvazia.
6. `ArcherMultipleEvents` cancela com `USER_CANCEL` em login, logout e mudança de dimensão; a morte do dono cancela com `DEATH`; a limpeza também cobre arcos em outras dimensões.
7. Recast (`2`) reinicia o ciclo sem criar uma quinta magia; a duração de `600` ticks é o prazo da supervisão.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo inicial | Entidade válida em até `64` blocos via `preCastTargetHelper` |
| Auto-alvo | Caixa frontal `24.0` (frente) × `8.0` × `8.0`, `CombatTools.isValidCombatTarget` + `canBeHostileToMe` |
| Arcos | `4` entidades persistentes em formação ao redor do dono |
| Carga/cadência | `15` ticks de carga, `8` ticks de cooldown por disparo |
| Troca de alvo | `60` ticks sem alvo prioritário liberam busca; `20` ticks sem LoS descartam o alvo automático |
| Continuidade | `40` ticks de `keepFireContinueTick` ao trocar de alvo |
| Duração/recast | `600` ticks e `2` recasts |

## 5. Resultado

- Cada arco aplica dano direto ao alvo via `DamageTypes.ARCHER_MULTIPLE`; não há projétil independente.
- `HIT_SEQUENCE` e `HIT_POSITION_X/Y/Z` sincronizam o feedback visual.
- O estado é amarrado a UUID + dimensão; a limpeza cobre dimensões diferentes do dono.
- `USER_CANCEL`/`DEATH` encerram todos os arcos da raiz; componentes não são objetos semânticos separados.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `200 + 50*(level-1)` | float declarado; host multiplica por atributos/config |
| Dano por flecha | `power/100 * damageMultiplier(ARCHER_MULTIPLE)` | config **NÃO VERIFICADA** |
| Mana | `70 + 30*(level-1)` | Iron's mana |
| Cooldown | `30.0` s | `DefaultConfig` |
| Cast time | `30` ticks | campo, `CastType.LONG` |
| Quantidade | `4` arcos | constante do provider |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano por flecha e mana respondem ao poder via `AbstractSpell`; número de arcos é constante.
- **B — evento verificado:** `ArcherMultipleEvents` é execução do provider, mas cancelamento não é um contrato de modificação de parâmetros.
- **C — adapter condicionado:** mudar quantidade, formação ou lógica de lock-on exigiria substituir `ArcherMultiple` e `ArcherMultipleBowEntity` com sincronia de UUID/dimensão. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura para transformar quatro arcos em AOE persistente ou alterar a janela de troca de alvo. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast → um alvo → quatro arcos supervisionados por UUID/dimensão → disparos com carga/cooldown → cancelamento por evento`.


## 9. Concepção de nova magia

Assinatura ocupada: "volley de arcos conjurados com lock-on e recast". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, 4 arcos, 600 ticks, recast 2, constantes dos arcos, caixa frontal 24/8/8, dano via `ARCHER_MULTIPLE`, UUID/dimensão e cancelamentos confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador instalado, mana/cooldown efetivos e comportamento em portais/lag não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- `getSummonCount()=4` e `getDuration()=600` são do provider, não do host.
- Auto-alvo é caixa frontal; o alvo do cast é raycast de `64` blocos.
- Login/logout/dimensão usam `USER_CANCEL`; morte usa `DEATH`.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
