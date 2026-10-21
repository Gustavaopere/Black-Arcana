# Rift Hole

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:rift_hole`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 10 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 25`
- `baseManaCost = 150`
- `manaCostPerLevel = 50`
- source field `castTime = 30 ticks` while `getCastType()` returns `INSTANT`; exact player-facing timing should therefore be confirmed in runtime rather than assuming the field is consumed
- open duration: `200 ticks = 10 s`
- recast count: `2`
- tunnel radius on the plane: `1`, producing a potential **3×3** cross-section
- targeting range: `8 + 8 * spellPower / 100`
- tunnel depth: `floor(range)`, minimum 1

At default unmodified spell power, nominal ranges are **16 / 18 / 20 blocks** for levels 1–3.

## Server-authoritative world mutation

The provider requires a server-validated block target and rejects disallowed dimensions. It constructs a tunnel plan, applying a provider safety predicate before replacing each eligible block.

For every replaced position it stores the original block state in the provider `RiftHoleBlockEntity`, plus caster/tunnel identity and expiry time. Recast or timeout closes the tunnel by restoring only provider blocks belonging to the matching tunnel UUID.

This is a bounded temporary world mutation with an explicit restore path; it is not a permanent excavation spell.

## Safety boundary

`RIFT_HOLE_TUNNEL_DENYLIST` exists in the exact provider tag registry, and `RiftHoleBlockSafety` remains provider authority for what may be replaced.

Black Arcana must not reapply this mutation or restoration through a second `WorldEffectPolicy` transaction after the provider has settled it. A Black Arcana-originated portable-hole mechanic would still require its own policy and must demonstrate a real semantic gap.

## Causality

Opening, active recast state and closing belong to one provider tunnel lifecycle. Closing/restoration is cleanup, not a new spell/progression event.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **temporary bounded portable tunnel with stateful block restoration** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT RANGE+DURATION+CROSS-SECTION+RESTORE IDENTITY / CAST-TYPE-vs-CAST-TIME RUNTIME UX + DENYLIST CONTENT + PACK QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:rift_hole` → `SpellRegistry.reg("rift_hole", RiftHole::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.rifthole.RiftHole`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/rifthole/RiftHole.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — 0.9.7.1 (audit de source, 2026-10-13)

**Prova rastreável:** [`rifthole/RiftHole.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/rifthole/RiftHole.java) · [`rifthole/RiftHoleBlockSafety.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/rifthole/RiftHoleBlockSafety.java) · [`rifthole/RiftHoleBlockEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/rifthole/RiftHoleBlockEntity.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, mod ID `apprenticecodex`. Identidade e versão do JAR são da modlist física; **não há prova de equivalência de cada corpo de método com o JAR compilado**.

### Critérios exatos de substituição e reparação

- **Admissão de bloco:** `RiftHoleBlockSafety.passesCommonChecks` rejeita ar, estados substituíveis, a tag `TagRegistry.Blocks.RIFT_HOLE_TUNNEL_DENYLIST`, fluidos e `getDestroySpeed<0`. `isTunnelFullBlock` exige collision shape de bloco cheio, portanto escadas e outras shapes não cúbicas não passam. O alvo inicial e o corpo do túnel compartilham checagens comuns, mas podem levar a resultados parciais diferentes.
- **Restauração segura:** `canReplace` acrescenta exclusão de BlockEntity, reação de pistão diferente de `PushReaction.NORMAL`, bloco com saída analógica ou `isSignalSource`. São checagens do **provider**, não equivalentes a um hook geral de claims.
- **Abertura:** `openTunnel` percorre posições de `RiftHoleCastData`, testa `canReplace` novamente no estado **atual**, coloca `BlockRegistry.RIFT_HOLE` e, quando obtém `RiftHoleBlockEntity`, grava estado anterior, caster UUID, tunnel UUID e `expireGameTime=gameTime+DURATION_TICKS`. Depois cria `RecastInstance` com os dados copiados; a abertura pode ser parcialmente aplicada quando posições deixam de ser elegíveis.
- **Fechamento:** `closeTunnel` processa posições em ordem reversa, exigindo ainda o bloco `RIFT_HOLE` e `matchesTunnel(tunnelId)` na block entity antes de repor `getOriginalState()`. Se o mundo mudou, esse fechamento deliberadamente **não força** a restauração de um bloco estranho. Expiração própria do `RiftHoleBlockEntity` deve ser verificada separadamente.
- **Boundary:** cada bloco substituído é consequência do cast `rift_hole`; recast/timeout/restore são cleanup. Exigir testes de unload, chunks, BlockEntity, alteração de bloco por terceiros, denylist datapack e proteção de claims; não executar novamente o túnel pelo `WorldEffectPolicy` do Black Arcana.

### Perfil para integração de perks e QA

- **A / stats e rank:** ler apenas os atributos declarados no host Iron's e os state objects que o addon expõe; stat dinâmica e duração efetiva exigem ambiente, item e configuração. Nenhuma alteração de mana/cooldown do Iron's por Black Arcana.
- **B / causalidade:** uma ação primária `apprenticecodex:rift_hole`; filhos, efeitos retardados, limpeza ou automação pertencem à raiz do provider. Sem `cast UUID`/contrato de retorno validado, o BA e RPG não devem inferir reward do resultado observado.
- **C/D / segurança:** ⛔ adapter de Mastery/perks enquanto inexistir contrato seguro. ⚠️ QA: servidor real, replay, NBT/relog, cross-dimension, compat opcional, ordenação e anti-double-processing. Não houve GameTest do provider nesta auditoria.
- **Clean-room:** análise factual e documentação próprias; código upstream não foi incorporado.

[Matriz causal desta etapa](../PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md).
