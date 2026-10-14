# Companion Trunk

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:companion_trunk`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 10`
- `spellPowerPerLevel = 10`
- `baseManaCost = 10`
- `manaCostPerLevel = 0`
- `castTime = 0`
- companion health: `round(spellPower)`

## Provider lifecycle

On the server the spell delegates to `CompanionTrunkManager.toggle(...)`. The provider therefore owns whether the companion is created, dismissed, persisted or otherwise transitioned; the spell itself only supplies the computed health value and the player identity.

## Causality and progression

Toggling the companion is one provider cast. Autonomous companion behavior after creation is not a stream of new player casts. RPG/Black Arcana must not award cast progression for passive companion ticks or manager-side maintenance.

## Deduplication

Occupies the **toggleable owner-bound trunk companion whose health scales with Evocation spell power** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+HEALTH FORMULA+SERVER TOGGLE / COMPANION INVENTORY+AI+PERSISTENCE DETAILS REQUIRE MANAGER AUDIT`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:companion_trunk` → `SpellRegistry.reg("companion_trunk", CompanionTrunk::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.companiontrunk.CompanionTrunk`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/companiontrunk/CompanionTrunk.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — entidades 0.9.7.1

**Source pin declarado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. **Classes lidas:** [`companiontrunk/CompanionTrunk.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/companiontrunk/CompanionTrunk.java) · [`companiontrunk/CompanionTrunkManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/companiontrunk/CompanionTrunkManager.java) · [`companiontrunk/CompanionTrunkEvents.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/companiontrunk/CompanionTrunkEvents.java) · [`companiontrunk/CompanionTrunkEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/companiontrunk/CompanionTrunkEntity.java). O arquivo físico da modlist é 0.9.7.1; **igualdade de corpo dos métodos no bytecode compilado não foi atestada nesta etapa**. Este conteúdo é engenharia documental factual, não código incorporado.

### Cadeia de execução e recibo provider-owned

- **Toggle e identidade:** `CompanionTrunk.onCast` chama `CompanionTrunkManager.toggle`, que lê `COMPANION_TRUNK_STATE` no `CodexSpellData`. `activate` normaliza entidades com owner UUID, define `state.active`, vida máxima validada e UUID do baú gerenciado. `ensureActive` recupera um tronco gerenciado quando o estado continua ativo e o jogador está vivo; não gera um novo cast.
- **Proteção do inventário contra despawn:** `tryDeactivate` consulta `Capabilities.getCompanionTrunkInventoryOrNull(player)`. Se houver itens, não despawna o armazenamento: quando o baú está longe, tenta `recallNearOwner` e retorna `false`; perto, informa impossibilidade de recolher. Apenas com inventário vazio descarta os baús do owner e limpa estado.
- **Morte e extração:** `deactivateBecauseOwnerDied` faz `dropAllContentsAndDiscard` dos baús encontrados; quando nenhum está carregado, `dropStoredInventory` percorre slots do armazenamento owner-scoped, extrai stacks e chama `Containers.dropItemStack`. Depois zera estado. `onTrunkDestroyed` limpa o estado apenas quando a entidade destruída corresponde ao UUID gerenciado (ou referência indisponível).
- **Lifecycle:** `CompanionTrunkEvents` registra `PlayerTickEvent.Post`, login, logout, troca de dimensão e `LivingDeathEvent`, delegando o gerenciamento da entidade e armazenamento ao addon. É obrigatório diferenciar remoção da entidade de perda/extravio de conteúdo e testar save/relog, host restart, drop duplicado e entidades duplicadas.
- **Boundary:** o baú gerenciado e os itens persistidos são do provider. RPG/BA não podem criar um segundo inventário, gerar XP por slot ou sincronizar estado de forma independente.

### Atribuição técnica e condições para perks

- **Identidade semântica:** exatamente uma raiz `apprenticecodex:companion_trunk`; eventos de entidades, timers, limpeza, efeitos derivados, recursos e cooldown são de Iron's/Apprentice's, não casts BA adicionais.
- **Observabilidade:** sem boundary/receipt interoperável comprovado, ⛔ Mastery, perks ou efeitos de RPG Skill Tree que suponham cast confirmado, hit, spawn ou settlement. Não inventar API de bridge.
- **QA pendente ⚠️:** configuração efetiva, JAR físico dos métodos, dedicated/full-modpack, Survival, cross-dimension, persistência, claim/PvP e compatibilidade de inventário. Não promover Stage 06.05.
- **Clean-room:** apenas comportamento observado no source é descrito. Black Arcana conserva seu próprio casting, Corruption, Strain e WorldEffectPolicy.

[Matriz de lifecycle](../PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
