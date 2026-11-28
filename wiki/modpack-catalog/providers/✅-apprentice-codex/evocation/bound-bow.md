# Bound Bow

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:bound_bow` |
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
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.boundbow.BoundBow` |
| Auxiliares da mesma raiz | `BoundBowManager`, `BoundBowState`, `BoundBowItem`, `BoundBowEvents` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("bound_bow", BoundBow::new)` |
| Config | `RARE`, nível 1, cooldown `30.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=50`, `baseManaCost=50`, `manaCostPerLevel=150`, `castTime=30` |
| Poder do arco | `POWER_START_SPELL_POWER=130`, `POWER_SPELL_POWER_STEP=30`; `power<130 → 0`, senão `1+floor((power-130)/30)`, clamp por `boundBowMaxPowerEnchantmentLevel()` |
| Duração/recast | `getDuration()=2400` ticks; `getRecastCount()=2` |
| Ativação | `BoundBowManager.activate`: desativa Bound Sword/Edge Dancer, copia e guarda a mão principal, cria `BoundBowItem` com UUID, substitui a mão, adiciona recast e sincroniza |
| Recurso capturado | `AttributeRegistry.SUMMON_DAMAGE` capturado no cast e passado a `BoundBowItem.create(...)` |
| Talismã | `Greater Conjurer's Talisman` remove o cooldown após o recast (`removeCooldown`) |
| Eventos | `BoundBowEvents` desativa em logout, morte, troca de dimensão e violações de slot |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `checkPreCastConditions` exige `Player`; `onCast` verifica se já há recast ativo e, em caso afirmativo, chama `BoundBowManager.deactivate(serverPlayer,true)` antes de reativar.
2. `BoundBowManager.activate` desativa mutually exclusive Bound Sword e Edge Dancer, copia `getMainHandItem()` para o estado, calcula `getPowerLevel(...)` e captura `SUMMON_DAMAGE`.
3. `BoundBowItem.create(instanceId,powerLevel,registryAccess,summonDamageMultiplier)` produz o arco; a mão principal é substituída e o estado sincronizado ao cliente.
4. Um `RecastInstance` com `2400` ticks e `2` recasts é registrado; o talismã, quando equipado, remove o cooldown no recast.
5. `onRecastFinished` chama `deactivate(player,false)` (sem remover o recast) e só aplica a conclusão padrão quando não há talismã; sem talismã, o recast termina normalmente.
6. `BoundBowEvents` desativa o arco em logout, morte, troca de dimensão, clique/slot inválido e quando o item esperado sai dos slots permitidos; o item original é restaurado.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Nenhum; equipamento na mão principal do jogador |
| Duração | `2400` ticks no `RecastInstance` |
| Recast | `2`, com reativação no segundo cast |
| Nível de poder | `0` abaixo de `130`; `1+floor((power-130)/30)` acima; cap em `ApprenticeCodexServerConfig.boundBowMaxPowerEnchantmentLevel()` |
| Exclusividade | Bound Sword e Edge Dancer são desativados |
| Estado | UUID de instância + mão original + multiplicador de `SUMMON_DAMAGE` |

## 5. Resultado

- O arco é um item gerado na mão principal; o ataque é o vanilla/Iron's modificado pelo `BoundBowItem`, não um projétil próprio catalogado nesta raiz.
- O custo de forge de flecha vem de `boundBowForgeArrowManaCost()`, lido apenas como informação; o efeito efetivo permanece `NÃO VERIFICADO`.
- A desativação restaura a mão original e sincroniza o estado; o recast é uma reativação da mesma raiz.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 50*(level-1)` | float declarado |
| Power level | `power<130 ? 0 : clamp(1+floor((power-130)/30),0,maxConfig)` | nível de encantamento do arco |
| Duração | `2400` ticks | recast |
| Mana/cooldown/cast | `50+150*(level-1)` / `30.0` s / `30` ticks | host + config **NÃO VERIFICADA** |
| `SUMMON_DAMAGE` | atributo do Iron's capturado no cast | multiplicador, valor efetivo **NÃO VERIFICADO** |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power altera o nível de poder; `SUMMON_DAMAGE` é capturado do host.
- **B — evento verificado:** os eventos de slot/morte/dimensão protegem o estado, mas não modificam parâmetros.
- **C — adapter condicionado:** mudar o cap, a duração ou a identidade do item exigiria substituir `BoundBow`, `BoundBowManager` e o item, com restauração de mão. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há contrato seguro para transformar o arco em arma de área, eliminar a exclusividade com Bound Sword/Edge Dancer ou alterar o custo de forge. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast → arco vinculado na mão principal com nível de poder → recast de 2400 ticks → restauração da mão original`.


## 9. Concepção de nova magia

Assinatura ocupada: "arma conjurada temporária com power level escalonado". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, constantes 130/30, duração 2400, recast 2, captura de `SUMMON_DAMAGE`, exclusividade e talismã confirmados no bytecode 1.0.1.1.
- ⚠️ cap efetivo do config, custo de forge de flecha e comportamento real de recast não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- `power<130` gera nível `0`; o cap vem de `boundBowMaxPowerEnchantmentLevel()`.
- `SUMMON_DAMAGE` é capturado no cast, não lido a cada disparo.
- Bound Sword e Edge Dancer são desativados na ativação.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
