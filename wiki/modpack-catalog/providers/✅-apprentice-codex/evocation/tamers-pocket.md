# Tamer's Pocket

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:tamers_pocket`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 4 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 20 ticks`
- interaction range: **8 blocks**
- stored-pet count is read from provider capability state `TAMERS_POCKET_STATE`

## Provider lifecycle

Pre-cast is server-player-only and locks one of three provider modes into serializable cast data: withdraw a looked-at owned pet, withdraw nearby owned pets as an area operation, or deploy stored pets to prevalidated positions. The cast then executes against those locked UUIDs/positions.

The exact source stores multiple pets; this is not a one-pet pocket. Entity serialization, ownership checks and deployment safety remain provider-owned.

## Causality and progression

Withdrawing several pets in one area cast remains one player cast. Stored pets do not become Black Arcana familiars merely because they are persisted by this spell. A future Binding integration must preserve each provider pet identity and avoid a second summon/storage lifecycle.

## Deduplication

Occupies the **owner-pet withdrawal, persistent pocket storage and later safe redeployment** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+RANGE+MULTI-PET MODES+SERVER-LOCKED CAST DATA / STORAGE LIMIT+ENTITY SERIALIZATION+DEPLOYMENT SAFETY DETAILS REQUIRE FULL CLASS/STATE AUDIT`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:tamers_pocket` → `SpellRegistry.reg("tamers_pocket", TamersPocket::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.tamerspocket.TamersPocket`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/tamerspocket/TamersPocket.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — entidades 0.9.7.1

**Fonte lida:** [`tamerspocket/TamersPocket.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/tamerspocket/TamersPocket.java) · [`tamerspocket/TamersPocketSync.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/tamerspocket/TamersPocketSync.java) · [`tamerspocket/TamersPocketSyncEvents.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/tamerspocket/TamersPocketSyncEvents.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` alinhado à release declarada 0.9.7.1. Versão e SHA do JAR são da modlist física; **corpos de bytecode destes métodos não foram provados como equivalentes ao source**.

### Execução, persistência e efeitos secundários

- **Pré-cast e três modos:** `TamersPocket.buildCastData(ServerPlayer)` prioriza pet vivo visado por look target e bloqueia o UUID em `WITHDRAW_SINGLE`. Sem alvo, se `TAMERS_POCKET_STATE.getStoredPetCount()<=0`, reúne UUIDs de pets próprios próximos em `WITHDRAW_AREA`. Quando já existem pets armazenados, busca lugares válidos e preenche `DEPLOY` com posições bloqueadas. Falha ao encontrar pets/lugares retorna `null` com mensagem; não é cast de captura consumado.
- **Retirada condicionada a owner real:** `withdrawLockedPets` re-resolve cada UUID no servidor; só captura `LivingEntity` viva e `isOwnedPetBy(pet,player)`. `capturePet` desassocia passengers/riding, salva tipo de entidade, NBT `saveWithoutId`, horário e display name com entry UUID próprio. Só então faz `pet.discard()` e grava as entries no `TAMERS_POCKET_STATE` do provider, sincronizando ao client.
- **Restauração:** `deployStoredPets` calcula `attemptCount=min(storedPets.size(), lockedDeployPositions.size())`; tenta `EntityType.loadEntityRecursive`, reposiciona, exige `ensureOwnedByCaster` e `level.tryAddFreshEntityWithPassengers(pet)`. Apenas entries cujos spawns retornaram sucesso são removidas do armazenamento por ID; pets falhos permanecem na lista. Aplica cura derivada do tempo armazenado `max(0,(currentGameTime-storedGameTime)/1200)`.
- **Risco:** NBT de terceiros, owner invalidado, pet de mod com passengers, capacidade, reentrância, restart e dimensões podem alterar semântica. A sequência de gravação e descarte exige teste de falhas/crash para excluir duplicação/perda; o source sozinho não certifica transação atômica. Não transferir pets ao runtime BA nem criar progressão por cada spawn.

### Boundary para perks e QA

- **Raiz:** `apprenticecodex:tamers_pocket`, já contabilizada no registry 83/83. Spawn, cleanup, tick, drop, item handling e efeitos causais **não** são novos casts contáveis.
- **Autoridade:** Iron's mantém escola, casting, mana e recast padrão; Apprentice's Codex detém entidades, itens e efeitos auxiliares; Black Arcana mantém apenas sua própria pipeline de magia/rituais, política de efeitos de mundo, Corruption e Strain.
- **Bloqueio:** ⛔ nenhuma API ou bridge de Mastery/perks confirmada para executar intervenções seguras; não deduzir rewards de eventos locais.
- **Pendências:** ⚠️ equivalência source/JAR, configuração, servidor dedicado com modpack real, multiplayer/PvP, inventários de terceiros, proteção de claims, save/reload e edge cases de entidades. Nenhuma prova de QA físico do provider nesta atualização.

[Matriz de lifecycle](../PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
