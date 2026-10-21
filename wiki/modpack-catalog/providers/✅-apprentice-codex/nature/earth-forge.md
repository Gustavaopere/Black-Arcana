# Earth Forge

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:earth_forge`
- **School:** Nature
- **Levels:** 1
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 100`
- `spellPowerPerLevel = 0`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 0`

Target range:

`8 * spellPower / 100` blocks.

Placement radius parameter:

`max(1, 1 + floor(spellPower / 100))`.

Sneaking forces radius to **1**, yielding the single-block mode described by the provider guide.

## Server placement plan

Before cast, the provider resolves a validated block face, derives a center point and enumerates only positions allowed by `EarthForgePlacementRules.canReplaceWithDirt(...)`. Center, effect direction and radius are serialized into cast data.

On cast, the plan is reconstructed against **current world state** rather than blindly trusting the pre-cast list, then submitted as an `EarthForgeJob`.

## Exact bounded job

`EarthForgeJob`:

- waits 2 ticks before the first placement;
- places the center first;
- places at most **one dirt block every 2 game ticks** thereafter;
- randomizes remaining target order;
- rechecks replaceability immediately before each placement;
- ends when all candidates are consumed.

For a valid ServerPlayer owner, dirt placement is performed through `BlockTools.useItemOnBlockByPlayerMainHand(...)` with a Dirt stack, preserving player-interaction/loader protection semantics. Only non-player/no-longer-valid-player fallback uses direct `setBlockAndUpdate` after provider replacement checks.

## What it does

Provider guide semantics: create a flat patch of dirt at line of sight; sneaking reduces it to one block.

## World safety

This provider spell already has a bounded asynchronous placement job and player interaction path. Black Arcana must not wrap the same cast in a second placement loop. BA-originated terrain creation still requires `WorldEffectPolicy` and equivalent budgets.

## Deduplication

Occupies the **bounded dirt-plane construction** niche.

## Confidence

`SOURCE-PINNED SPELL + PLACEMENT JOB / NON-PLAYER FALLBACK POLICY + MODPACK PROTECTION QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:earth_forge` → `SpellRegistry.reg("earth_forge", EarthForge::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.earthforge.EarthForge`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/earthforge/EarthForge.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — 0.9.7.1 (audit de source, 2026-10-13)

**Prova rastreável:** [`earthforge/EarthForge.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/earthforge/EarthForge.java) · [`earthforge/EarthForgeJob.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/earthforge/EarthForgeJob.java) · [`earthforge/EarthForgeJobManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/earthforge/EarthForgeJobManager.java) · [`earthforge/EarthForgePlacementRules.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/earthforge/EarthForgePlacementRules.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (declara 0.9.7.1); o JAR físico da modlist tem identidade/versionamento corroborados, **sem equivalência dos corpos compilados demonstrada**.

### Scheduler da alteração de terreno

- **Pré-cast e plano:** `EarthForge` resolve alvo de bloco/facing no host, filtra posições por `EarthForgePlacementRules.canReplaceWithDirt` e serializa o centro e a direção. No cast servidor, recria o plano contra estado corrente do mundo e entrega a um `EarthForgeJob`; listas antigas não autorizam escrita cega.
- **Ordem e velocidade:** `EarthForgeJob` inicia com `nextPlaceGameTime=currentGameTime+2` e executa **uma tentativa a cada dois game ticks**, primeiro o centro, depois posições aleatórias removidas de `randomTargets`. Define `complete=true` quando o centro foi tentado e a lista esgotou, mesmo se alguma tentativa não produziu bloco.
- **Admissão no momento do efeito:** `tryPlace` chama novamente `EarthForgePlacementRules.canReplaceWithDirt(level.getBlockState(pos))`, de forma que o bloco pode ser rejeitado se mudou desde a preparação. Quando possui `ServerPlayer` ainda válido, `tryPlaceDirt` usa `BlockTools.useItemOnBlockByPlayerMainHand(...,new ItemStack(Items.DIRT),effectDirection.getOpposite())` e confirma bloco DIRT. Somente se o jogador foi removido/inexistente usa fallback `level.setBlockAndUpdate` direto.
- **Risco específico de safety:** o fallback de no-owner não demonstra a mesma proteção de interações do caminho com `BlockTools`. É pendência de QA para invalidação do caster no meio do job e claims de terceiros. Não presumir que WorldEffectPolicy do BA tenha sido invocado pelo addon.
- **Perks:** a fila e cada posição processada são filhos da mesma ação `earth_forge`; a conclusão do job não é novo cast, e a experiência não pode ser multiplicada pelo número de tentativas sem recibo externo homologado.

### Perfil para integração de perks e QA

- **A / atributo e rank:** stats e estado de Iron's/Codex são lidos do provider, sem sobrescrita automática. Valores efetivos dependem de configuração e outros mods.
- **B / causalidade:** raiz `apprenticecodex:earth_forge`, mantendo eventos, tarefas e recursos da cadeia sob authority externa; não atribuir Mastery por cada callback de efeito secundário.
- **C/D / política:** nenhuma API/hook de RPG Skill Tree homologada pela simples presença desses métodos. **⛔** fail-closed para adapter e **⚠️** QA da versão instalada (JAR, host, Survival, servidor, multiplayer, dependências opcionais e claims).
- **Clean-room:** somente especificação factual própria; não transplantar implementação upstream.

[Matriz causal desta etapa](../PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md).
