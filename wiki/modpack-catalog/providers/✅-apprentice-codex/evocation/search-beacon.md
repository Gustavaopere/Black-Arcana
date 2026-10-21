# Search Beacon

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:search_beacon`
- **Iron's school:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 60 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 80`
- `spellPowerPerLevel = 80`
- `baseManaCost = 100`
- `manaCostPerLevel = 40`
- `castTime = 0`
- base search unit: `round(spellPower)`
- initial search distance: `base search unit * 8`
- additional distance per consumed item: `base search unit`
- absolute maximum search distance is delegated to `SearchBeaconSearchService.getMaxSearchRange()` and is not invented here

## Provider lifecycle

Server-side pre-cast validates placement/summoning through `SearchBeaconSummoning.validate(...)`, including rejection when a beacon is already active. A successful cast delegates the search workflow to `SearchBeaconSummoning.summonFromSpell(...)` with the computed initial and per-item ranges.

## Causality and progression

The structure-location workflow is provider-owned. Repeated internal search steps or extra range purchased with items are not independent casts or divination milestones unless a real provider event exposes them as such.

## Deduplication

Directly occupies the **provider-native structure-search beacon with spell-power-scaled initial range and item-funded range extension** niche. Black Arcana Familiars & Divination must not add a generic structure locator without a materially different contract.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+RANGE FORMULAS+SERVER SUMMON VALIDATION / MAX SEARCH CAP+ITEM CONSUMPTION+SEARCH SERVICE DETAILS REQUIRE SERVICE AUDIT`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:search_beacon` → `SpellRegistry.reg("search_beacon", SearchBeacon::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.searchbeacon.SearchBeacon`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/searchbeacon/SearchBeacon.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — entidades 0.9.7.1

**Fonte lida:** [`searchbeacon/SearchBeacon.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/searchbeacon/SearchBeacon.java) · [`searchbeacon/SearchBeaconEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/searchbeacon/SearchBeaconEntity.java) · [`searchbeacon/SearchBeaconSearchService.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/searchbeacon/SearchBeaconSearchService.java) · [`searchbeacon/SearchBeaconRefundManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/searchbeacon/SearchBeaconRefundManager.java) · [`searchbeacon/SearchBeaconTargetManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/searchbeacon/SearchBeaconTargetManager.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` alinhado à release declarada 0.9.7.1. Versão e SHA do JAR são da modlist física; **corpos de bytecode destes métodos não foram provados como equivalentes ao source**.

### Execução, persistência e efeitos secundários

- **Fases e custo de objeto oferecido:** `SearchBeaconEntity.tick` mantém posição ancorada e avança `IDLE → ARMED → SEARCHING → RESULT` segundo estado, oferta e resultado. Entidade sem owner vivo é descartada, e um `reservesInstantBrazier` sem reserva correspondente via `SearchBeaconRefundManager.matches(owner,beaconUuid)` é invalidado. `absorbOfferedItem` lê targets por `SearchBeaconTargetManager.getDefinition(stack)`, aceita somente itens compatíveis com a oferta atual e ajusta `searchRange` pelo total aceito.
- **Busca com orçamento:** `SearchBeaconSearchService.createSession` resolve alvos pela definição do datapack e placements de structures do nível; compartilha `processedStarts` por structure contra múltiplos placement hits. `SEARCH_STEPS_PER_TICK=48`, `SearchSession.advance(level,maxSteps)` distribui steps entre tarefas e só conclui quando nenhuma tarefa resta. O limite de raio vem de `clampRange`, não da duração arbitrária da sessão.
- **Reserva e retorno:** `SearchBeaconRefundManager.reserve(owner,beaconUuid,stack)` salva **um stack de count=1 serializado** em `SEARCH_BEACON_STATE` e marca dirty. `consume`, `refund`, `recoverPending` e `recover` passam por `claimPendingInstantBrazier(expectedBeaconUuid)` para impedir claim duplicada na rotina local. O item vai a `owner.getInventory().placeItemBackInInventory` nos caminhos de recuperação. A rota de oferta consome o reservation na transição para SEARCHING.
- **Distinção necessária:** o reembolso do instant brazier e o consumo de itens oferecidos são estados econômicos diferentes; `SearchBeaconSearchService.shouldRefundOfferedItems` trata `null`, vazio e `hasUnknownStructures` de modo específico. Não inferir reembolso universal de todas as ofertas, sucesso da busca ou chunk loading de todo alvo.
- **Risco:** search usa generator state/structure data; QA de datapacks, valores efetivos de cap/step budget, morte/logout com refund pendente, estrutura desconhecida e concorrência de beacons é obrigatória. Não atribuir Mastery por cada structure indexada nem iniciar busca paralela BA.

### Boundary para perks e QA

- **Raiz:** `apprenticecodex:search_beacon`, já contabilizada no registry 83/83. Spawn, cleanup, tick, drop, item handling e efeitos causais **não** são novos casts contáveis.
- **Autoridade:** Iron's mantém escola, casting, mana e recast padrão; Apprentice's Codex detém entidades, itens e efeitos auxiliares; Black Arcana mantém apenas sua própria pipeline de magia/rituais, política de efeitos de mundo, Corruption e Strain.
- **Bloqueio:** ⛔ nenhuma API ou bridge de Mastery/perks confirmada para executar intervenções seguras; não deduzir rewards de eventos locais.
- **Pendências:** ⚠️ equivalência source/JAR, configuração, servidor dedicado com modpack real, multiplayer/PvP, inventários de terceiros, proteção de claims, save/reload e edge cases de entidades. Nenhuma prova de QA físico do provider nesta atualização.

[Matriz de lifecycle](../PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
