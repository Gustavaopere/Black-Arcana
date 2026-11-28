# Edge Dancer

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:edge_dancer` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | sem interface adicional declarada |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `EPIC` |
| Níveis declarados | 1 (`setMaxLevel(1)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `30.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=50`, `manaCostPerLevel=0`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.edgedancer.EdgeDancer` |
| Auxiliares da mesma raiz | `EdgeDancerManager`, `EdgeDancerState`, `SpellSideEdge`, `SpellSideEdgeMirror`, `EdgeDancerEvents` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("edge_dancer", EdgeDancer::new)` |
| Config | `EPIC`, nível 1, cooldown `30.0`, `EVOCATION_RESOURCE`, `setAllowCrafting(false)`, `allowLooting()=false` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=100`, `baseManaCost=50`, `manaCostPerLevel=0`, `castTime=40` |
| Duração | `getDuration(level,caster)` → `round(1200*power/100)` ticks |
| Gate | `checkPreCastConditions` exige `SpellSideEdge.isSpellSideEdge(mainhand)` no primeiro cast |
| Recast | `getRecastCount()=2`; talismã remove cooldown no recast |
| Manager | `EdgeDancerManager.activate` cria `SpellSideEdgeMirror` no offhand e desativa Bound Sword/Bound Bow |
| Eventos | `EdgeDancerEvents`/manager validam local do espelho e desativam em slots inválidos |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. No primeiro cast, `checkPreCastConditions` exige uma `SpellSideEdge` na mão principal; em recast, o gate é o estado ativo.
2. `onCast`, quando há recast, desativa a instância anterior e chama `EdgeDancerManager.activate`.
3. `activate` desativa Bound Sword e Bound Bow, cria `SpellSideEdgeMirror` com UUID de instância a partir da arma principal e o coloca no offhand.
4. Um `RecastInstance` com duração `round(1200*power/100)` e `2` recasts é registrado; o talismã suprime o cooldown na conclusão do recast.
5. `validateActiveMirrorLocation` e os eventos desativam quando o espelho sai dos slots permitidos, a arma principal desaparece ou a instância não corresponde.
6. `deactivate` remove o espelho gerado, limpa o estado e restaura o offhand original apenas se ele havia sido sobrescrito.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | `SpellSideEdge` na mão principal |
| Duração | `round(1200*power/100)` ticks |
| Recast | `2` |
| Espelho | `SpellSideEdgeMirror` no offhand, com UUID de instância |
| Exclusividade | Bound Sword e Bound Bow desativados |
| Validação | Espelho apenas em slots permitidos; estado amarrado à arma original |

## 5. Resultado

- O espelho reflete a arma principal; não é uma segunda magia nem um projétil.
- A duração escala com poder; sem poder suficiente, o arredondamento pode resultar em duração baixa.
- A desativação é feita por eventos de inventário, não por contagem de golpes.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 100*(level-1)` | float declarado |
| Duração | `round(1200*power/100)` | ticks |
| Mana/cooldown/cast | `50` / `30.0` s / `40` ticks | host + config **NÃO VERIFICADA** |
| Recast | `2` | instâncias da mesma raiz |

## 7. Possibilidades de perks

- **A — atributo nativo:** duração responde ao poder; mana/cooldown ao `AbstractSpell`.
- **B — evento verificado:** validação de slot é proteção de estado, não hook de dano.
- **C — adapter condicionado:** mudar duração, espelho ou exclusividade exigiria substituir raiz, manager e item. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há contrato seguro para duplicar armas ou eliminar o requisito de `SpellSideEdge`. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast com SpellSideEdge → espelho no offhand → recast com duração escalada → limpeza por eventos de slot`.


## 9. Concepção de nova magia

Assinatura ocupada: "arma espelhada temporária no offhand". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, coeficientes 100/100/50/0/40, duração `round(1200*power/100)`, gate de `SpellSideEdge`, recast 2, talismã e exclusividade confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador/mana efetivos e comportamento real do espelho em combate não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- Sem `SpellSideEdge` na mão principal, o primeiro cast falha.
- O espelho é um item gerado no offhand; não é nova magia.
- Bound Sword e Bound Bow são desativados na ativação.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
