# Iron's 1.21.1-3.16.3 — prova binária estática para Eldritch Blast e Burning Dash

**Data documental:** 2026-10-15, execução UTC já em 2026-10-16 · **Stage:** 06.05 🟡 sem promoção · **PR:** [#825](https://github.com/Gustavaopere/Black-Arcana/pull/825). Esta é uma **extensão de prova binária**, não um novo ID de magia, GameTest ou adapter.

## Artefato físico auditado

- **Run:** [GitHub Actions #38828793186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38828793186), job `inspect_published_provider_jar` (**SUCCESS**).
- **JAR publisher:** `irons_spellbooks-1.21.1-3.16.3.jar`, CurseForge file ID **8680204**; arquivo baixado no runner e conferido por **SHA-256 esperado** antes de `javap`.
- **Tamanho:** **13.890.046 bytes**.
- **SHA-256:** `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73`.
- **Java:** 21; `./gradlew catalogQaProbeJar jar` e isolamento do companion testados no mesmo workflow; **não** demonstra que as duas magias foram executadas.
- **Coletor:** [`irons_3163_recast_dash_bytecode.py`](./irons_3163_recast_dash_bytecode.py), importa apenas helpers de inspeção estática da ferramenta anterior. Prova classfiles exatos, marcadores de método/instrução e ordem local de chamadas relevantes; produz somente JSON `recast-dash-evidence.json`, sem bytecode/desassemblagem/JAR redistribuídos.
- **Artifact JSON do workflow:** `irons-3163-projectile-bytecode-bf67c9dd5ffa505f131aef3cd4b0c1289d799c4b` (ID `12016715334`), publicado junto aos relatórios existentes.

## Resultados efetivamente verificados

| Classe compilada | Caminho de bytecode confirmado | Limite |
|---|---|---|
| `spells.eldritch.EldritchBlastSpell` | `onCast` referencia `RecastInstance`, `RaycastBuilder`, `EldritchBlastVisualEntity` e `DamageSources.applyDamage` | ✅ presença das operações no método; ⚠️ ordem de eventos, cast aceito e quantidade de tiros dependem de runtime |
| `EldritchBlastSpell` | `getRecastCount` contém adição inteira, `getDamageSource` contém `setIFrames` e `indirect` | ✅ caminhos estáticos; ⚠️ **3–7** ativações vêm da fórmula source-pinned, não da simples presença do opcode de soma |
| `entity.spells.eldritch_blast.EldritchBlastVisualEntity` | `tick` lê `tickCount` e contém `discard`; `shouldBeSaved` retorna `false` | ✅ descarte e ausência de save flag identificados em bytecode; ⚠️ não provam que o cliente renderizou ou que a entidade desapareceu no tempo previsto |
| `spells.fire.BurningDashSpell` | `onCast` referencia `ImpulseCastData`, `setDeltaMovement`, `BURNING_DASH`, `invulnerableTime` e `setSpinAttackType`; `getDamageSource` referencia `setFireTicks` | ✅ instruções presentes; ⚠️ física, pacote cliente e knockback real não medidos |
| `effect.BurningDashEffect` | `applyEffectTick` referencia `DamageSources.applyDamage`, `BURNING_DASH_SPELL`, `horizontalCollision` e escreve `invulnerableTime` **depois** do call de dano; `shouldApplyEffectTickThisTick` retorna `true` | ✅ presença/ordem local binária; ⚠️ **não prova dano aceito a cada tick** nem comportamento completo dos branches e cancelamentos |

O resultado JSON reportou `PUBLISHED_JAR_BYTECODE_STATIC`, `eldritch_blast.onCast_uses_raycast_and_damage_helper=true`, `eldritch_blast.visual_shouldBeSaved_false=true`, `burning_dash.effect_writes_iframe_counter_after_damage_attempt=true`, `burning_dash.effect_tick_every_tick_returns_true=true`. Os campos de quantidade e de hits reais são deliberadamente condicionais: `SOURCE_PLUS_RUNTIME_QA_REQUIRED` e `NOT_PROVEN_BY_BINARY`.

## Separação de autoridade e gates remanescentes

✅ **Fonte fixada e publisher JAR auditado:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, mas um source pin não é substituto de build identity; esta prova de bytecode se limita às classes e métodos auditados.

⚠️ **Pendente:** hash do Iron's instalado no perfil, versão transformada do NeoForge **21.1.248**, config/perks existentes, proteção PvP/claims, tick real da effect, `SpellDamageEvent` cancelado e seu efeito no `invulnerableTime`, impacto de `setIFrames(0)` de Eldritch, render da entidade visual, ordem de cooldown e recasts, reload/servidor dedicado/cliente e GameTests.

⛔ **Bloqueado:** incrementar tiros de Eldritch Blast, aplicar modificador de `BurningDashEffect` per-target/per-tick, alterar flags `invulnerableTime`, replicar movimento ou cobrar mana novamente sem seam real, idempotência, budget e teste físico. `SpellOnCastEvent` e `SpellDamageEvent` derivados não equivalem a novas sessões de Mastery.

**Limite da contagem:** as duas identidades já estavam inventariadas. Esta prova não muda o piso **1.856 global / 1.854 escopo**, nem adiciona mais dois dossiês além dos **28/110** documentados. O Stage 06.05 não avança e a PR permanece draft.

**Clean-room:** relatório de interfaces/assinaturas e fluxo comprovado sem redistribuir implementation/bytecode/assets de terceiro.
