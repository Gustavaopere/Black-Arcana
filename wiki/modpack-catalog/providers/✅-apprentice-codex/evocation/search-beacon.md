# Search Beacon

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:search_beacon` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | sem interface adicional na raiz; entidade `PathfinderMob`/`GeoEntity` e serviço de busca pertencem à mesma raiz |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `EPIC` |
| Níveis declarados | 1–3 (`setMaxLevel(3)`) |
| Tipo de cast | `INSTANT` |
| Cooldown declarado | `60.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=100`, `manaCostPerLevel=40`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.searchbeacon.SearchBeacon` |
| Auxiliares da mesma raiz | `SearchBeaconEntity`, `SearchBeaconSummoning`, `SearchBeaconSearchService`, `SearchBeaconState`, `SearchBeaconRefundManager`, `SearchBeaconTargetManager` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("search_beacon", SearchBeacon::new)` |
| Config | `EPIC`, nível 3, cooldown `60.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=80`, `spellPowerPerLevel=80`, `baseManaCost=100`, `manaCostPerLevel=40`, `castTime=0` |
| Alcance | `getInitialRange = round(getSpellPower)*8`; `getAdditionalRangePerItem = round(getSpellPower)`; `getBaseRange = round(power)` |
| Serviço | `CHUNK_PADDING=2`, `MAX_SEARCH_RANGE=5000`, `SEARCH_STEPS_PER_TICK=48`; `clampRange` limita a `0..5000` |
| Reembolso | `shouldRefundOfferedItems(result)` → `result == null || isEmpty() || !hasUnknownStructures()` |
| Entidade | `WIDTH=0.7F`, `HEIGHT=1.45F`, `SEARCH_RESOLVE_TICKS=60`, `OFFER_CHECK_INTERVAL_TICKS=4`, `REOFFER_COOLDOWN_TICKS=100`, `OFFER_PICKUP_RANGE=0.85`, `ALL_PHASE_DISCARD_DISTANCE_SQR=1024.0` |
| Aceite de itens | `getMaxAcceptedItemCount`: `1 + ceil((5000-initial)/additional)` quando `additional>0` e `initial<5000`, senão `1` |
| Estado | `SearchBeaconState`: `searched_structures`, `traversed_structures`, `pending_instant_brazier_uuid`, `pending_instant_brazier_stack` |
| Guarda | `SearchBeaconSummoning.validate`: `Failure.ALREADY_ACTIVE` se houver pingente ou farol ativo; `CANNOT_PLACE` se não houver posição |

Bytecode: scratch/javap1011_evocation7.txt (`javap -classpath <JAR> -p -s -c`, 94 classes, EXIT=0, SHA-256 `AF225F42FA1A0295D7339542D49620FBA0D0BE6599147EEDF69B75744730DB41`); decompilação de apoio: scratch/evocation7_sources.txt (46 fontes Vineflower 1.12.0, SHA-256 `05090319D9206171C8C4C38ED1A33479F0F1313F9135B5D70146F5559EB80DB1`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `checkPreCastConditions` valida somente em `ServerLevel`/`ServerPlayer`; falha envia action bar vermelha (`already_active` ou `cant_place`) e retorna `false`.
2. `onCast` chama `SearchBeaconSummoning.summonFromSpell(level, owner, initialRange, additionalRangePerItem)` e então `super.onCast`.
3. A entidade percorre fases com `SEARCH_RESOLVE_TICKS=60` e avança `SEARCH_STEPS_PER_TICK=48` por tick; `CHUNK_PADDING=2` delimita a varredura de chunks.
4. A cada `OFFER_CHECK_INTERVAL_TICKS=4` a entidade absorve `ItemEntity` em `boundingBox.inflate(0.85)`; `getAcceptedItemCount` limita o total aceito e `getSearchRangeForCount` converte itens em alcance.
5. `getMaxAcceptedItemCount` usa `Math.positiveCeilDiv((5000-initial), additional)` e acrescenta o item inicial; o alcance é limitado por `clampRange`.
6. Ao concluir, `shouldRefundOfferedItems` devolve itens quando não há estrutura desconhecida; o estado guarda estruturas pesquisadas/atravessadas.
7. `ALL_PHASE_DISCARD_DISTANCE_SQR=1024.0` (32 blocos) e `REOFFER_COOLDOWN_TICKS=100` limitam reofertas; nenhum dano é aplicado.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Nenhuma entidade de combate; alvo é posição de summon e itens oferecidos |
| Posição de summon | `resolveSummonPosition`; falha produz `CANNOT_PLACE` |
| Alcance | Inicial `8*round(power)`, por item `round(power)`, limitado a `5000` |
| Geometria da entidade | `0.7 × 1.45` blocos (`PathfinderMob`) |
| Coleta de itens | `inflate(0.85)` a cada `4` ticks; distância mínima horizontal `0.1` |
| Descarte | `1024.0` distância ao quadrado (32 blocos) em todas as fases; reoferta com `100` ticks |
| Persistência | `SearchBeaconState` guarda estruturas e brazier pendente; `SearchBeaconRefundManager` guarda reembolso |

## 5. Resultado

- Utilitário de busca: **sem dano, cura, status, projétil, knockback ou tipo de dano** (`N/A` com justificativa: apenas summon, busca de estruturas e devolução de itens).
- Itens oferecidos são absorvidos e podem ser devolvidos; o consumo é de itens do jogador, não mana adicional.
- `Failure.ALREADY_ACTIVE` impede farol duplo enquanto houver entidade ou reembolso pendente.
- `SearchBeaconState` persiste conhecimento de estruturas e estado de brazier instantâneo; `SearchBeaconRefundManager` controla devolução.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `80 + 80*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Alcance inicial | `8 * round(getSpellPower)` blocos |
| Alcance por item | `round(getSpellPower)` blocos |
| Teto de busca | `5000` blocos (`clampRange`), com `CHUNK_PADDING=2` |
| Throughput | `48` etapas por tick; resolução em `60` ticks |
| Itens aceitos | `1 + positiveCeilDiv(5000 - initial, additional)`, no máximo até o teto |
| Mana | `100 + 40*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `60.0` s declarado |

## 7. Possibilidades de perks

- **A — atributo nativo:** alcance inicial e por item derivam de `getSpellPower`; nada mais responde a atributos de forma demonstrada.
- **B — evento verificado:** `SearchBeaconSummoning.validate` e `SearchBeaconState` são fluxos do provider, não hook de modificação de parâmetros.
- **C — adapter condicionado:** alterar `MAX_SEARCH_RANGE`, `SEARCH_STEPS_PER_TICK` ou as fases exigiria substituir serviço e entidade com risco de busca global/per-tick. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para alterar o teto de busca ou o consumo de itens sem duplicar reembolso. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast → valida farol único → summon → itens aumentam alcance (≤5000) → busca em 48 etapas/tick → resultado ou reembolso → estado persistido`.


## 9. Concepção de nova magia

Assinatura ocupada: farol que busca estruturas usando itens como alcance adicional, com reembolso condicionado. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `80/80/100/40/0`, alcance `8*power`/`power`, teto `5000`, `48` etapas/tick, constantes da entidade, aceite de itens, reembolso e estado confirmados no bytecode 1.0.1.1.
- ⚠️ poder e mana efetivos e a lista de estruturas alvo (`SearchBeaconTargetList`), condicionada a config/datapack, permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, busca real em mundo, portais ou reembolso observado.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: farol que busca estruturas usando itens como alcance adicional, com reembolso condicionado. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
