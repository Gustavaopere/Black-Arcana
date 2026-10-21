# Bound Sword

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:bound_sword`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 50`
- `manaCostPerLevel = 150`
- `castTime = 30 ticks`
- duration: `2400 ticks = 120 s`
- recast count: `2`
- weapon damage: `(3 + 3 * spellPower / 100) * SUMMON_DAMAGE attribute * providerDamageMultiplier`

## Provider lifecycle

The first cast activates provider-owned bound-sword state through `BoundSwordManager`. A later recast deactivates it. The provider can optionally attempt a dual-wield compatibility path when the real compat is present and the player deliberately crouches during initial pre-cast.

Greater Conjurer's Talisman behavior is provider-native: on manual deactivation/recast the spell may remove its own cooldown according to the provider's existing talisman contract.

## Causality and progression

The temporary weapon session is one cast lifecycle. Physical swings made while the bound sword is active are not automatically new spell casts. Any RPG bridge must distinguish provider activation from downstream melee-hit causality and avoid double credit with combat systems.

## Deduplication

Occupies the **two-minute provider-bound summoned melee weapon with summon-damage scaling and optional dual-wield compatibility** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DURATION+RECAST+WEAPON DAMAGE / BOUND ITEM STATS+DUAL-WIELD COMPAT DETAILS REQUIRE MANAGER QA`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:bound_sword` → `SpellRegistry.reg("bound_sword", BoundSword::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.boundsword.BoundSword`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/boundsword/BoundSword.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — entidades 0.9.7.1

**Source pin declarado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. **Classes lidas:** [`boundsword/BoundSword.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/boundsword/BoundSword.java) · [`boundsword/BoundSwordManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/boundsword/BoundSwordManager.java) · [`boundsword/BoundSwordEvents.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/boundsword/BoundSwordEvents.java). O arquivo físico da modlist é 0.9.7.1; **igualdade de corpo dos métodos no bytecode compilado não foi atestada nesta etapa**. Este conteúdo é engenharia documental factual, não código incorporado.

### Cadeia de execução e recibo provider-owned

- **Sessão recast e exclusão mútua:** `BoundSwordManager.activate` desativa previamente `BoundSword`, `BoundBow` e `EdgeDancer` do player, exige `CodexSpellData` e gera `instanceId=UUID.randomUUID()`. Copia itens originais da mão principal e offhand, cria `BoundSwordItem` com este UUID e dano fornecido pela spell, substitui a mão principal e, condicionalmente, offhand.
- **Compatibilidade dual wield:** `hasDualWieldCompat` inspeciona `ModList.get().isLoaded` para Better Combat ou Epic Fight. `shouldGenerateOffhandSword` depende desse gate e de offhand física vazia ou flag explícita, **não** é garantia de duas armas para qualquer jogador. O estado persistido guarda stacks originais, UUID da sessão, presença do offhand gerado e dano, seguido de `RecastInstance` de Iron's.
- **Revalidação anti-extravio:** `validateActiveSwordLocation` em tick verifica UUID válido, contagem de espadas geradas em slots permitidos, e ausência em slots de armor. Se falha, chama `deactivate(player,true)`; esta remove geradas por `instanceId`, reseta `BOUND_SWORD_STATE`, tenta restaurar stacks originais, remove recast e sincroniza. `BoundSwordEvents` também desativa em morte, login, logout e troca de dimensão.
- **Risco:** prevenção de dupe depende das regras concretas de inventário/packet e compat de combate. Não inferir segurança de outros containers sem inspeção; testar cursor de inventory menu, dual wield, modded slots, mudança de arma e reinício. Cada golpe não é nova spell e a mana de cast é de Iron's.

### Atribuição técnica e condições para perks

- **Identidade semântica:** exatamente uma raiz `apprenticecodex:bound_sword`; eventos de entidades, timers, limpeza, efeitos derivados, recursos e cooldown são de Iron's/Apprentice's, não casts BA adicionais.
- **Observabilidade:** sem boundary/receipt interoperável comprovado, ⛔ Mastery, perks ou efeitos de RPG Skill Tree que suponham cast confirmado, hit, spawn ou settlement. Não inventar API de bridge.
- **QA pendente ⚠️:** configuração efetiva, JAR físico dos métodos, dedicated/full-modpack, Survival, cross-dimension, persistência, claim/PvP e compatibilidade de inventário. Não promover Stage 06.05.
- **Clean-room:** apenas comportamento observado no source é descrito. Black Arcana conserva seu próprio casting, Corruption, Strain e WorldEffectPolicy.

[Matriz de lifecycle](../PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
