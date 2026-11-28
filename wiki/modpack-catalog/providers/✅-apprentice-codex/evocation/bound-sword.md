# Bound Sword

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:bound_sword` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | sem interface adicional declarada |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1 (`setMaxLevel(1)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `30.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=50`, `manaCostPerLevel=150`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.boundsword.BoundSword` |
| Auxiliares da mesma raiz | `BoundSwordManager`, `BoundSwordState`, `BoundSwordItem`, `BoundSwordEvents` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("bound_sword", BoundSword::new)` |
| Config | `RARE`, nível 1, cooldown `30.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=50`, `baseManaCost=50`, `manaCostPerLevel=150`, `castTime=30` |
| Dano | `getWeaponDamage` → `(3 + 3*power/100) * SUMMON_DAMAGE * damageMultiplier(BOUND_SWORD)` |
| Duração/recast | `getDuration()=2400` ticks; `getRecastCount()=2` |
| Dual wield | `hasDualWieldCompat()` = `ModList.isLoaded("bettercombat") || ModList.isLoaded("epicfight")`; `forceTryDualWield = !hasRecast && compat && isShiftKeyDown()` |
| Ativação | `BoundSwordManager.activate`: desativa Bound Bow/Edge Dancer, copia mãos, cria espadas, substitui slots e registra recast |
| Talismã | `Greater Conjurer's Talisman` remove o cooldown após o recast |
| Eventos | `BoundSwordEvents` desativa em logout, morte, dimensão e slots inválidos, restaurando a mão secundária original |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onServerPreCast` calcula `forceTryDualWield` quando não há recast ativo, o compat está presente e Shift está pressionado; o valor viaja no `BoundSwordCastData` (buffer e NBT).
2. `onCast` desativa a instância anterior quando há recast e chama `BoundSwordManager.activate(...,getWeaponDamage(...),forceTryDualWield)`.
3. `BoundSwordManager.activate` desativa Bound Bow e Edge Dancer, copia mão principal e secundária física, e gera a espada da mão principal.
4. A espada secundária é gerada somente com compat e (`forceTryDualWield` ou mão secundária física vazia); a mão original é guardada no estado para restauração.
5. `RecastInstance` de `2400` ticks com `2` recasts é registrado; talismã remove cooldown no recast.
6. `onRecastFinished` desativa sem remover o recast; os eventos restauram o offhand original em logout, morte, dimensão e violação de slot.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Nenhum; equipamento nas mãos do jogador |
| Duração | `2400` ticks |
| Recast | `2` |
| Dano | `(3 + 3*power/100) * SUMMON_DAMAGE * multiplier` |
| Dual wield | Exige `bettercombat` ou `epicfight` ativos |
| Gate do segundo cast | `!hasRecast && compat && Shift` |
| Exclusividade | Bound Bow e Edge Dancer desativados |
| Restauração | Offhand original salvo somente quando a espada secundária é gerada |

## 5. Resultado

- A espada é um item gerado; o dano é atributo de item calculado no cast e capturado na criação.
- A geração da segunda espada é condicionada a mods externos; sem compat, o fluxo permanece de uma mão.
- A restauração depende do estado `BoundSwordState`; sem geração do offhand, nada é sobrescrito.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 50*(level-1)` | float declarado |
| Dano da espada | `(3 + 3*power/100) * SUMMON_DAMAGE * damageMultiplier(BOUND_SWORD)` | atributo de item |
| Mana/cooldown/cast | `50+150*(level-1)` / `30.0` s / `30` ticks | host + config **NÃO VERIFICADA** |
| Compat | `ModList.isLoaded(...)` | presença de mod, não habilidade de ataque |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde a poder e `SUMMON_DAMAGE`; dual wield depende de mods instalados.
- **B — evento verificado:** Shift é lido no pre-cast; não é um hook mutador de dano.
- **C — adapter condicionado:** alterar dano da espada, duração ou regras de dual wield exigiria substituir raiz, manager e item com restauração de slots. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura para aumentar o número de espadas além do par ou remover a dependência de compat. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast → espada(s) conjuradas com dano calculado → recast de 2400 ticks → restauração das mãos`.


## 9. Concepção de nova magia

Assinatura ocupada: "arma conjurada temporária com dual wield condicionado a mods externos". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, fórmula `(3+3*power/100)*SUMMON_DAMAGE*multiplier`, duração 2400, recast 2, gate de compat/Shift e restauração confirmados no bytecode 1.0.1.1.
- ⚠️ valor de `SUMMON_DAMAGE`, multiplicador instalado e comportamento real com Better Combat/Epic Fight não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- Dual wield exige `bettercombat` ou `epicfight`; Shift só força o segundo cast.
- O dano é capturado no cast e escrito no item, não recalculado por swing.
- Bound Bow e Edge Dancer são desativados na ativação.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
