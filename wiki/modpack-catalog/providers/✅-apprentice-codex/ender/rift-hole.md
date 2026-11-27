# Rift Hole

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:rift_hole` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interface | `IClientBlockTargetingSpell` |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.EPIC` |
| Níveis | 1–3 (`DefaultConfig.setMaxLevel(3)`) |
| Tipo de cast | `CastType.INSTANT` (com `castTime=30` no construtor; ver §3) |
| Cooldown declarado | `10.0` s |
| Recurso | Mana do Iron's (`baseManaCost=150`, `manaCostPerLevel=50`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.rifthole.RiftHole` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("rift_hole", RiftHole::new)` |
| Config | `RiftHole.config` (`EPIC`, nível 3, cooldown `10.0`) |
| Coeficientes | `RiftHole.<init>()`: `baseSpellPower=100`, `spellPowerPerLevel=25`, `baseManaCost=150`, `manaCostPerLevel=50`, `castTime=30` |
| Constantes | `DURATION_TICKS=200`, `TUNNEL_RADIUS=1` |
| Alcance | `RiftHole.getRange(int,LivingEntity)` → `8 + 8*power/100` |
| Profundidade | `getTunnelDepth(int,LivingEntity)` → `max(1, floor(range))` |
| Cliente | `getClientBlockTargetingRange(...)` → `getRange(...)` |
| Recast | `RiftHole.getRecastCount(...)` → `2` |
| Gate de cast | `RiftHole.checkPreCastConditions(...)`: recast ativo fecha; senão exige dimensão permitida e `buildTunnelPlan` com alvo válido |
| Dados de cast | `RiftHole.RiftHoleCastData` (`createOpenCastData(UUID.randomUUID(), tunnelPlan)`, `createCloseCastData()`) |
| Planejamento | `buildTunnelPlan(...)`, `BlockTargetingHelper.getValidatedPendingTarget(...)` |
| Abertura/fechamento | `openTunnel(...)`, `closeTunnel(...)`, `onRecastFinished(...)` |
| Segurança | `RiftHoleBlockSafety.isTargetBlock`, `passesCommonChecks`, `isTunnelFullBlock`, `canReplace`, `hasUnsafeRestoreBehavior` |
| Tag | `TagRegistry.Blocks.RIFT_HOLE_TUNNEL_DENYLIST` |
| Entidade de bloco | `RiftHoleBlockEntity` (`originalState`, `casterUuid`, `tunnelUuid`, `expireGameTime`, `matchesTunnel`) |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `castTime=30` existe como campo, mas `getCastType()` retorna `CastType.INSTANT`. A ficha registra ambos literalmente; **o timing apresentado ao jogador não foi verificado em runtime** — não afirmar que o campo é consumido.
2. Sem recast ativo, `checkPreCastConditions` exige `ApprenticeCodexServerConfig.isRiftHoleDimensionAllowed(level.dimension().location())` e `buildTunnelPlan`: valida o alvo via `BlockTargetingHelper.getValidatedPendingTarget`, exige `RiftHoleBlockSafety.isTargetBlock(hitPos)` e plano não vazio; grava `RiftHoleCastData.createOpenCastData(UUID.randomUUID(), plano)`.
3. Com recast ativo cujo cast data é `RiftHoleCastData` com túnel, converte para `createCloseCastData()` e o cast fecha o túnel.
4. `onCast` em `ServerLevel`: `isCloseCast` → `closeTunnel` + `removeActiveRecast`; `isOpenCast` → `openTunnel`, que cria `RecastInstance(..., 200 ticks, castData.copy())`.
5. `onRecastFinished` fecha o túnel; `onServerCastComplete` reseta/limpa `additionalCastData`.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alcance de targeting | `8 + 8*power/100` blocos; nominal **16 / 18 / 20** nos níveis 1–3 sem modificadores |
| Profundidade do túnel | `max(1, floor(range))` blocos a partir do alvo validado |
| Seção transversal | `TUNNEL_RADIUS=1` no plano, resultando em até **3×3** posições, sujeitas às checagens de segurança |
| Duração | `DURATION_TICKS=200` ticks (10 s) |
| Recast | `2`, usado para reabrir/fechar dentro da sessão |
| Dimensões | gate `ApprenticeCodexServerConfig.isRiftHoleDimensionAllowed`; conteúdo **NÃO VERIFICADO** |
| Perfil do bloco | `isTunnelFullBlock` exige collision shape de bloco cheio; shapes não cúbicos não passam |

A abertura pode ser **parcial**: `openTunnel` reavalia `canReplace` no estado atual de cada posição e só substitui as elegíveis. Não afirmar túnel completo garantido.

## 5. Critérios de substituição e restauração

- `passesCommonChecks`: rejeita ar, estados substituíveis, `TagRegistry.Blocks.RIFT_HOLE_TUNNEL_DENYLIST`, fluidos e `getDestroySpeed < 0`.
- `canReplace`: acrescenta exclusão de BlockEntity existente, `PushReaction != NORMAL`, saída analógica e `isSignalSource`.
- `openTunnel`: coloca `BlockRegistry.RIFT_HOLE` e, no `RiftHoleBlockEntity`, grava `originalState`, `casterUuid`, `tunnelUuid` e `expireGameTime = gameTime + 200`.
- `closeTunnel`: percorre em ordem reversa e exige ainda bloco `RIFT_HOLE` e `matchesTunnel(tunnelId)` antes de restaurar `getOriginalState()`. Se o mundo mudou, não força restauração de bloco estranho.
- Expiração autônoma da block entity é consequência do mesmo ciclo de vida; não é um novo cast.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 25*(level-1)` | float; `getSpellPower` do host |
| Mana | `150 + 50*(level-1)` | Iron's mana |
| Alcance | `8 + 8*power/100` | blocos |
| Profundidade | `max(1, floor(range))` | blocos |
| Duração | `200` | ticks |
| Recast | `2` | Iron's recast |
| Cooldown | `10.0` s | `DefaultConfig` |
| `castTime` | `30` | campo; `CastType.INSTANT` no `getCastType()` |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power/mana/cooldown via `AbstractSpell`; o alcance responde ao spell power.
- **B — evento verificado:** `checkPreCastConditions`, `openTunnel` e `closeTunnel` são fluxos do provider; não há API de mutação segura demonstrada para alterar raio/profundidade/restauração.
- **C — adapter condicionado:** qualquer mudança de geometria ou política de blocos exigiria substituir `buildTunnelPlan`, `RiftHoleBlockSafety` e a block entity com contrato de restauração por UUID. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há hook comprovado para tornar o túnel permanente, ignorar a denylist ou duplicar a restauração sem risco de corromper estado. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um plano de túnel → abertura parcial com estado por bloco → recast/timeout → restauração por tunnel UUID`.

A mutação do mundo é provider-owned e liquidada pelo addon. Black Arcana não deve reaplicar abertura/restauração via segunda `WorldEffectPolicy` transaction. Uma mecânica BA equivalente exigiria política própria e gap semântico real.

## 9. Concepção de nova magia

Assinatura ocupada: "túnel temporário limitado com restauração stateful por bloco". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, alcance/profundidade, seção 3×3, duração, recast, gates e critérios de restauração confirmados no bytecode 1.0.1.1.
- ⚠️ Conteúdo da denylist, config de dimensão e o uso efetivo de `castTime=30` em runtime não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor real, unload/reload de chunks, alteração de bloco por terceiros, claims ou PvP.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- `castTime=30` + `CastType.INSTANT` é uma contradição aparente a resolver por QA, não valor a "corrigir" no paper.
- A restauração só casa se `matchesTunnel(tunnelUuid)` for verdadeiro; não reprocessar por terceiros.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
