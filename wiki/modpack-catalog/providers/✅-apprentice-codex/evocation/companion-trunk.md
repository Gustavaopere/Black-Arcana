# Companion Trunk

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:companion_trunk` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | sem interface adicional declarada |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1 (`setMaxLevel(1)`) |
| Tipo de cast | `INSTANT` |
| Cooldown declarado | `0.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=10`, `manaCostPerLevel=0`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.companiontrunk.CompanionTrunk` |
| Auxiliares da mesma raiz | `CompanionTrunkManager`, `CompanionTrunkEntity`, `CompanionTrunkInventory`, `CompanionTrunkState` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("companion_trunk", CompanionTrunk::new)` |
| Config | `RARE`, nível 1, cooldown `0.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=10`, `spellPowerPerLevel=10`, `baseManaCost=10`, `manaCostPerLevel=0`, `castTime=0` |
| HP do baú | `getCompanionHealth(level,caster)` → `round(power)`; `Math.max(1.0, maxHealth)` no manager |
| Manager | `DEFAULT_MAX_HEALTH=20.0`, `MANUAL_RECALL_MIN_DISTANCE_SQR=4.0`, `SUMMON_SEARCH_RADIUS=3`, `SUMMON_Y_OFFSETS={0,1,-1,2,-2}` |
| Entidade | `PathfinderMob`/`GeoEntity`/`Container`/`MonarchBondHealingTarget`; `WIDTH=0.95`, `HEIGHT=1.1`, follow `3.0/1.75`, teleporte `24.0` |
| Inventário | `CompanionTrunkInventory` ligado ao estado do jogador; `ChestMenu` na interação |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `CompanionTrunk.onCast` (somente servidor e `ServerPlayer`) chama `CompanionTrunkManager.toggle(serverPlayer, round(getSpellPower(...)))`.
2. `toggle` chama `activate` se não há estado ativo; caso contrário tenta `tryDeactivate`.
3. `activate` normaliza o HP com `Math.max(1.0,maxHealth)`, executa `normalizeOwnedTrunks` e grava `maxHealth` e `trunkUuid` no `CompanionTrunkState`.
4. O spawn procura posição livre em raio `3` com offsets Y `{0,1,-1,2,-2}`; a entidade segue o dono e teleporta quando necessário.
5. `tryDeactivate` exige distância² ≥ `4.0` para recolha manual, normaliza baús possuídos e restaura o inventário via `CompanionTrunkInventory`.
6. `MonarchBondHealingTarget` permite cura externa; a interação abre `ChestMenu` vinculado ao inventário persistente do jogador.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Nenhum; estado do próprio jogador |
| HP | `round(power)`, mínimo `1.0` no manager |
| Recolha manual | distância² ≥ `4.0` (≈ `2` blocos) |
| Busca de spawn | raio `3`, offsets Y `0,1,-1,2,-2` |
| Follow | inicia em `3.0`, para em `1.75`, teleporte em `24.0` |
| Dimensões | `0.95 × 1.1` |

## 5. Resultado

- Um baú por jogador é normalizado; estados órfãos são removidos pelo manager.
- O inventário é uma capacidade do jogador, não um container de mundo independente.
- A recolha exige distância mínima para evitar conflito com a interação de abrir o baú.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `10 + 10*(level-1)` | float declarado |
| HP | `round(power)`, `max(1.0,maxHealth)` | pontos de vida |
| Mana/cooldown/cast | `10` / `0.0` s / `0` ticks | host + config **NÃO VERIFICADA** |
| Recolha | `4.0` distância² | threshold do manager |

## 7. Possibilidades de perks

- **A — atributo nativo:** HP responde ao poder; mana/cooldown ao `AbstractSpell`.
- **B — evento verificado:** follow/teleporte são comportamento da entidade, não contrato de modificação.
- **C — adapter condicionado:** mudar HP, raio de spawn, distância de recolha ou capacidade de inventário exigiria substituir manager, entidade e estado. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura para transformar o baú em container compartilhado ou remover o gate de distância. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast → toggle do estado → spawn/recolha de um baú por jogador → inventário persistente`.


## 9. Concepção de nova magia

Assinatura ocupada: "baú companheiro com inventário e recolha manual". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, coeficientes 10/10/10/0/0, HP `round(power)`, constantes 20/4/3/Y-offsets e dimensões da entidade confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador/mana efetivos, persistência real do inventário e follow em portais não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- HP é `round(power)`, com piso `1.0` no manager.
- `4.0` é distância²; `3` é o raio de busca de spawn.
- O inventário pertence ao jogador via capability.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
