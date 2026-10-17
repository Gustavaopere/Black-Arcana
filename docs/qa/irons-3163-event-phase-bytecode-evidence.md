# Iron's 3.16.3 — bytecode de dano cancelado e fases de recast

**Data (local):** 15/10/2026 · **Pipeline UTC:** 16/10/2026 · **Prova:** ✅ bytecode estático no JAR publicado, ⚠️ NeoForge transformado/GameTest pendentes · **Stage 06.05:** 🟡 · [PR #825](https://github.com/Gustavaopere/Black-Arcana/pull/825).

## Provenance binária

- **Run Java 21:** [GitHub Actions #38830097297](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38830097297), job `inspect_published_provider_jar`, **SUCCESS**. Houve duas falhas anteriores corretas de **coletor QA**: [#38829616023](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38829616023) detectou overload/bridge `serializeNBT`; [#38829881467](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38829881467) detectou lógica de timeout gerada pelo compilador em métodos sintéticos `lambda$tick$`, não inteiramente em `tick`. **Não foram falhas de gameplay do Iron's.**
- **Arquivo:** `irons_spellbooks-1.21.1-3.16.3.jar`, CurseForge file ID `8680204`, **13.890.046 bytes**, SHA-256 `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73` conferido antes do disassembly.
- **Coletor:** [`irons_3163_event_phase_bytecode.py`](./irons_3163_event_phase_bytecode.py), autoteste de fail-closed PASS; usa `javap -p -c` em 6 classes do JAR. Os resultados são metadados/booleans no JSON `event-phase-evidence.json`, sem publicação de JAR ou trecho desassemblado.
- **Fonte pinned de suporte:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`. Conferir também o dossiê [cancelamento/recast](../../wiki/modpack-catalog/providers/✅-irons-spells/audits/CAUSAL-PERKS-DAMAGE-CANCEL-AND-RECAST-SESSION-3.16.3.md).

## Resultado da inspeção compilada

| Objeto | Achado corroborado | Limitação |
|---|---|---|
| `BurningDashEffect.applyEffectTick` | `DamageSources.applyDamage` seguido de **`pop`** da resposta booleana e, no mesmo caminho local, de `putfield invulnerableTime` **sem branch intermediário** | ✅ `LOCAL_FALLTHROUGH_ONLY`. Não prova `LivingDamageEvent.Post`, dano aceito, efeito final em todos os mods ou imunidade efetiva no mundo |
| `DamageSources.applyDamage` | Presença de `SpellDamageEvent`, `isCanceled`, resistência e `hurt`; o cancelamento anterior a `hurt` é comprovado na fonte source-pinned | ✅ símbolos compilados; ⚠️ sequência exata do mundo transformado e policy de listeners externos não homologadas |
| `AbstractSpell.castSpell` | Ordem de referências `hasRecastForSpell` → `SpellOnCastEvent` → `onCast` → `decrementRecastCount` | ✅ posição relativa no método compilado. A prova do branch de cobrança por recast depende de fonte e QA: **`SOURCE_AND_BYTECODE_BRANCH_QA_PENDING`** |
| `EldritchBlastSpell.onCast` | Consulta ao recast, instalação de `RecastInstance` e raycast | ✅ marcador binário; ⚠️ 3–7 ativações são **configuração/source**, não contagem de eventos in-game |
| `PlayerRecasts` | Registra novas sessões, consome cargas, reseta `remainingTicks`, verifica timeout por lambda sintética | ✅ `CLASS_WIDE_SYNTHETIC_LAMBDA_MARKERS`; não significa que a ordem de timeout foi demonstrada por eventos live |
| `RecastInstance.serializeNBT` | Persistência de `remainingRecasts`, `totalRecasts`, `ticksToLive`, `ticksRemaining` | ✅ campos binários; ⚠️ source não declara token UUID de sessão; teste de restart/relog ainda pendente |

**Detalhe importante — proveniência do coletor:** `RecastInstance.serializeNBT` possui uma ponte do compilador e a assinatura concreta que retorna `CompoundTag`; a inspeção passou após restringir o método pelo tipo de retorno e testar o erro anterior. O timeout de `PlayerRecasts.tick` usa lambdas sintéticas, portanto o resultado é explicitamente **class-wide**, não alegação de bytecode linear inteiro em `tick`.

## Decisões de interoperabilidade

**Burning Dash:** `SpellDamageEvent` significa tentativa anterior ao `hurt`, não dano pós-processado; o efeito pode alcançar o write de invulnerabilidade depois de um `applyDamage` negado. **⛔** Não creditar Mastery de acerto, não redisparar o dano para contornar cancelamentos, não assumir que `setFireTicks(80)` foi aplicado após tentativa vetada.

**Eldritch Blast:** um evento `SpellOnCastEvent` pode representar raiz ou uma ativação derivada. Sem identificador de sessão canônico público/contrato validado, **⛔** não emitir XP da sessão raiz por cada recast, não usar `(playerUUID,spellId)` como ID infalível de sessão em logout/relog, não reaplicar mana/cooldown por evento.

**Pendências físicas obrigatórias:** hash do JAR instalado e do NeoForge efetivo no perfil; eventos `SpellDamageEvent` cancelados com leitura de `invulnerableTime`; `LivingDamageEvent.Post`; teste de recasts nos níveis 1–5 com 80 ticks nominais, timeout, NBT/relog, client packet e cooldown; proteção PvP/teams/claims e servidor dedicado. Sem tais linhas não há aprovação de adapter ou promoção de Stage 06.05.

**Contagem semântica preservada:** 110 magias Iron's já inventariadas, **28/110 dossiês individuais**, mínimo global **1.856 objetos / 1.854 em escopo**, total global desconhecido. Esta auditoria é transversal, **não** cria novo spell ID.

**Clean-room:** somente classes, métodos e estados de fronteira; nenhuma implementação ou recurso de terceiro reproduzido.
