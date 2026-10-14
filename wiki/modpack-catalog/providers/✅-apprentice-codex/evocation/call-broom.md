# Call Broom

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:call_broom`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Ordinary crafting:** disabled
- **Ordinary looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 20 ticks / 1 s`
- recall-distance threshold for an unoccupied deployed broom: **8 blocks**
- requires a unique equipped provider broom resolved through `BroomCurioSupport.findUniqueEquippedBroom(...)`

## Admission

The spell is explicitly item-bound: ordinary crafting and looting are disabled. It only accepts a player caster.

Client preflight requires:

- the player is not already a passenger;
- one unique equipped provider broom can be resolved.

The server then delegates to `CallBroomDeploymentManager.validate(...)`. Exact failure states are:

- `NOT_FOUND` — no valid equipped broom;
- `RIDING` — caster is already a passenger;
- `OCCUPIED` — the relevant owned/deployed broom is currently being ridden and cannot be safely recalled/replaced.

## Provider deployment / recall transaction

When a valid deployed broom matching the equipped item already exists and is not occupied, the cast recalls it through the provider lifecycle.

Otherwise the manager:

1. recalls stale unoccupied brooms owned by the player;
2. clears stale deployment state from the equipped broom item;
3. creates the provider broom entity from that exact equipped item;
4. assigns owner and copies the item's custom name;
5. spawns the broom at the player;
6. requires the player to begin riding it successfully;
7. only then stores the deployed entity UUID on the broom item.

If entity insertion fails, the transaction returns failure. If mounting fails after insertion, the provider recalls the broom and does not leave it as a successful deployment.

## Reconciliation and automatic recall

Provider state remains tied to the equipped broom item and owner. The manager recalls or clears deployment state when appropriate on unequip, broom removal, login/logout and ownership/equipment mismatch.

`shouldRecall(...)` returns true when:

- the owner is dead;
- owner and broom are in different levels;
- the broom is being controlled by someone other than its owner;
- an unoccupied broom is more than **8 blocks** from the owner;
- the deployed entity no longer matches the uniquely equipped broom item/state.

## Performance caveat

At the exact source pin, helper paths that find all owned broom entities iterate all server levels and each level's `getAllEntities()`. That is upstream provider behavior and **must not be copied into Black Arcana**. Black Arcana's own summons/owned entities must continue using bounded/indexed ownership contracts rather than global entity scans.

## Causality and progression

Calling or recalling the broom is one provider cast. Riding distance, mounted ticks, login reconciliation or automatic recall are provider lifecycle effects and must not generate repeated spell Mastery.

Black Arcana does not own broom identity, Curios lookup, deployment UUIDs, mount persistence or recall semantics and must not create a second broom/familiar ledger.

## Deduplication

Occupies the **Curios-equipped provider broom deployment/recall spell with owner-bound mount reconciliation** niche.

## Confidence

`SOURCE-PINNED SPELL + DEPLOYMENT MANAGER / EXACT ITEM GATE+FAILURE STATES+SPAWN/MOUNT TRANSACTION+8-BLOCK RECALL+LOGIN/LOGOUT/UNEQUIP RECONCILIATION / FULL MODPACK MOUNT RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:call_broom` → `SpellRegistry.reg("call_broom", CallBroom::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.callbroom.CallBroom`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/callbroom/CallBroom.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — entidades 0.9.7.1

**Source pin declarado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. **Classes lidas:** [`callbroom/CallBroom.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/callbroom/CallBroom.java) · [`callbroom/CallBroomDeploymentManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/callbroom/CallBroomDeploymentManager.java) · [`callbroom/CallBroomDeploymentEvents.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/callbroom/CallBroomDeploymentEvents.java). O arquivo físico da modlist é 0.9.7.1; **igualdade de corpo dos métodos no bytecode compilado não foi atestada nesta etapa**. Este conteúdo é engenharia documental factual, não código incorporado.

### Cadeia de execução e recibo provider-owned

- **Validação de cast:** `CallBroomDeploymentManager.validate(ServerPlayer)` exige exatamente uma vassoura Curios elegível por `BroomCurioSupport.findUniqueEquippedBroom`, recusa player passageiro, e confronta `BroomDeploymentState.getDeployedEntityId(stack)` com UUID, owner e item correspondente. Uma vassoura já implantada e ocupada falha com `OCCUPIED`; quando livre, a ação vira `RECALL`, senão `SUMMON`.
- **Summon/recall:** `execute` retorna à própria vassoura livre via `recallWithoutItem` ou recolhe brooms antigas não ocupadas e tenta `BroomCurioSupport.createBroom`. A nova entidade recebe a pilha do equipamento, owner, nome, posição; apenas após `serverLevel.addFreshEntity` e `player.startRiding(broom,true)` bem-sucedidos grava `BroomDeploymentState.setDeployedEntity(stack,broom.getUUID())`. Se montar falhar, chama `recallWithoutItem`.
- **Longevidade:** `shouldRecall` rejeita owner morto, mudança de dimensão, passenger incorreto, distância acima de `RECALL_DISTANCE_SQ` e equipamento que deixou de corresponder. `onUnequip` faz recall e limpa a tag de deployment; `reconcileEquippedStack`, `onBroomRemoved`, `onLogout` e `onLogin` saneiam IDs e referências.
- **Ownership:** a montaria continua pertencendo ao item Curios e às entidades da vassoura, não ao runtime BA. Recast para recall e criação do veículo são dois resultados condicionais da mesma spell ID, não duas raízes para Mastery. QA: vassouras em dimensão diferente, duas Curios, mounts terceiros, logout a bordo e manipulação de stack.

### Atribuição técnica e condições para perks

- **Identidade semântica:** exatamente uma raiz `apprenticecodex:call_broom`; eventos de entidades, timers, limpeza, efeitos derivados, recursos e cooldown são de Iron's/Apprentice's, não casts BA adicionais.
- **Observabilidade:** sem boundary/receipt interoperável comprovado, ⛔ Mastery, perks ou efeitos de RPG Skill Tree que suponham cast confirmado, hit, spawn ou settlement. Não inventar API de bridge.
- **QA pendente ⚠️:** configuração efetiva, JAR físico dos métodos, dedicated/full-modpack, Survival, cross-dimension, persistência, claim/PvP e compatibilidade de inventário. Não promover Stage 06.05.
- **Clean-room:** apenas comportamento observado no source é descrito. Black Arcana conserva seu próprio casting, Corruption, Strain e WorldEffectPolicy.

[Matriz de lifecycle](../PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
