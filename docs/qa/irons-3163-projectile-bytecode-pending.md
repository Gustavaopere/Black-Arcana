# Iron's Spells 1.21.1-3.16.3 — prova binária de projéteis, com QA de runtime pendente

**Data:** 2026-10-15 · **Stage:** 06.05 🟡 sem promoção · **Escopo:** evidência compilada do provider, sem integrar/alterar o runtime Black Arcana.

## Artefato e cadeia de verificação

- **Provider / mod ID:** Iron's Spells 'n Spellbooks / `irons_spellbooks`.
- **Publisher:** CurseForge projeto `855414`, file ID **`8680204`**, `irons_spellbooks-1.21.1-3.16.3.jar` (MC 1.21.1 NeoForge).
- **Pipeline da PR draft #825:** [GitHub Actions run #38811661659](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38811661659), job `inspect_published_provider_jar` ID `116686121166`, **SUCCESS** (2026-10-15); `setup-java@v5`, Java `21.0.12.1`.
- **Tamanho observado no runner:** `13.890.046` bytes.
- **SHA-256 calculado no download:** `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73`.
- **Fluxo reprodutível da branch:** [workflow](../../.github/workflows/irons-3163-projectile-bytecode.yml), [coletor](./irons_3163_projectile_bytecode.py); `python3 docs/qa/irons_3163_projectile_bytecode.py --self-test` PASS antes do download, e o coletor obteve relatório JSON em `build/irons-3163/evidence.json`.
- **Artefato CI:** `irons-3163-projectile-bytecode-854ef574b540473bffad4817e1aa6c1dd100d3e7` (ID `12008199060`), contém **somente o relatório JSON**, não o JAR de terceiro.
- **Fonte de apoio não-binarizada:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` (source pinned separado de build publicada). O bytecode é agora evidência superior **dos quatro métodos efetivamente inspecionados**. Não afirmar que todos os demais métodos da tag upstream são idênticos aos do JAR.

**Limitação de integridade:** o SHA-256 acima foi calculado no JAR publicado baixado no runner, **não cotejado com SHA-1/SHA-256 de um arquivo instalado no modpack**. Logo não há correspondência binária do perfil certificada. O ID do CurseForge especifica a origem declarada; o workflow não fixa um hash preexistente independente, portanto o resultado não deve ser descrito como verificação *preapproved hash equality*.

## Complemento Mojang 1.21.1 — correção da hipótese de tickCount

A [GitHub Actions #38814378449](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38814378449), **SUCCESS**, executou o coletor [`minecraft_1211_entity_tick_proof.py`](./minecraft_1211_entity_tick_proof.py). A rotina recuperou o manifesto de versão oficial Mojang **1.21.1**, validou SHA-1 dos downloads conforme a versão publicada, extraiu o JAR interno do servidor e resolveu `ServerLevel.tickNonPassenger(Entity)` com os **mapeamentos oficiais**. Os valores observados são:

| Propriedade | Evidência |
|---|---|
| Official Mojang server bundle SHA-1 | `59353fb40c36d304f2035d51e7d6e6baa98dc05c` |
| Bundle bytes | `51.627.615` |
| Mojang official mappings SHA-1 | `03f8985492bda0afc0898465341eb0acef35f570` |
| Embedded official server SHA-256 | `c301de10f575027d13eac18c7f34409d60648cf56a35d566aa1f530ff617840a` |
| `tickNonPassenger` reads/writes Entity.tickCount | **true / true** |
| Writes `tickCount` BEFORE invoking `Entity.tick()` | **true** |
| Vanilla verdict | `WORLD_TICK_INCREMENTS_ENTITY_AGE` |

**Retificação técnica obrigatória:** o JAR do Iron's 3.16.3 **não** chama `super.tick()` em `ArrowVolleyEntity.tick`, mas **o servidor vanilla Minecraft 1.21.1 incrementa o contador no world tick**. Logo, o suposto `tickCount` congelado e a hipótese de spawn indefinido fundada **somente** na ausência de `super.tick()` não se sustentam no ciclo vanilla inspecionado. A constatação anterior era uma hipótese de fonte incompleta, não bug provado.

[Modelo determinístico de seis níveis](./irons_3163_arrow_volley_tick_model_test.py) — baseado no fluxo observado `tickCount % 5 == 0` ou descarte quando `tickCount > rows×5`, com incremento vanilla antes de `tick()` — prevê, **sem executar o jogo**, os pares `nível: flechas / descarte em tick`: `1:25/26, 2:36/31, 3:42/36, 4:56/41, 5:63/46, 6:80/51`. Este teste é um **modelo original de interoperabilidade**, não transcrição nem execução do código do Iron's.

**Continuam pendentes:** prova do `ServerLevel` transformado por NeoForge **21.1.248**, comportamento real de 25–80 spawns com permissões/chunks, `EntityTickEvent` de terceiros, lifecycle de carregamento/descarte, fingerprint do JAR **instalado**, GameTest e servidor dedicado. Nenhum perk que altera count está liberado sem hook provider-native e limites de efeito. **Status:** ✅ bytecode oficial vanilla + Iron's publicado, ⚠️ NeoForge/pack em execução, ⛔ alteração de projéteis de terceiro sem contrato.

## Provas compiladas e interpretação

| Classe do JAR | Sinal observado em `javap -p -c` | Estado |
|---|---|---|
| `entity.spells.ArrowVolleyEntity` | `tick()` lê `tickCount`, **não chama `super.tick()` e não escreve diretamente `tickCount`** | ✅ provado no JAR Iron's; o incremento vanilla anterior a `tick()` foi provado depois em Mojang 1.21.1; ⚠️ NeoForge e gameplay pendentes |
| `entity.spells.small_magic_arrow.SmallMagicArrow` | `shoot(Vec3)` usa `setDeltaMovement` sem `getSpeed()`; `onHitEntity` referencia `ARROW_VOLLEY_SPELL` | ✅ provado para o caminho compilado; ⚠️ danos e hits aceitos não medidos |
| `entity.mobs.SummonedSkeleton` | Herda diretamente de `net.minecraft.world.entity.monster.Skeleton`; **não declara `performRangedAttack`** | ✅ prova da ausência de override local; ⚠️ classe vanilla/NeoForge e `DamageSource` de flecha herdada **não** inspecionados |
| `entity.spells.poison_cloud.PoisonCloud` | `applyEffect` referencia `POISON_CLOUD` e dano direto por `hurt`, **sem chamada a `DamageSources.applyDamage`** | ✅ prova de método compilado; ⚠️ eventos NeoForge gerais, outras inserções e resultado físico não certificados |

**Arrow Volley — revisão:** a ausência de `super.tick` em `ArrowVolleyEntity` está comprovada no JAR do Iron's, **mas não causa, isoladamente, ausência de incremento**: o servidor vanilla oficial 1.21.1 incrementa `tickCount` em `ServerLevel.tickNonPassenger` antes da chamada de `Entity.tick`. A hipótese anterior de *unbounded per-tick spawn* por contador congelado foi **retificada**. A contagem em NeoForge transformado ainda exige GameTest e instrumento de orçamento por tick; ⛔ perk de +flechas continua bloqueado por falta de seam seguro e QA.

**SummonedSkeleton — limite de atribuição:** a prova de que `performRangedAttack` é herdado **não prova** que o `DamageSource` de flecha é `RAISE_DEAD_SPELL` ou não é. O golpe melee `doHurtTarget` já tem evidência distinta de `RAISE_DEAD_SPELL`. Para Mastery/XP de ranged, a atribuição continua ⚠️ condicionada à implementação do jogo e à observação de eventos reais.

**PoisonCloud — limite de observação:** o caminho `PoisonCloud.applyEffect` não usa o helper do provider que publica `SpellDamageEvent`; assim, filtrar somente `SpellDamageSource` no adapter não identifica o dano periódico da nuvem. Não afirmar ausência de todos os eventos NeoForge: `target.hurt` ainda pode publicá-los.

## Próximos testes que não foram executados

1. **GameTest/dedicated-server 1.21.1/NeoForge + JAR exato:** o incremento vanilla está provado; logar `ArrowVolleyEntity.tickCount` e o número de `SmallMagicArrow` criadas por tick, níveis 1 e 6, durante ≥ 100 ticks; avaliar se descarte é alcançado e se há budget fixo.
2. **GameTest de chunk/salvamento:** interromper/recarregar o controlador enquanto emite flechas; comparar `rows`, `arrowsPerRow`, contador e número de projéteis antes/depois.
3. **Vanilla/NeoForge skeleton ranged:** inspecionar bytecode de `Skeleton`/`AbstractSkeleton` e `AbstractArrow` da versão física, registrar `DamageSource.getDirectEntity`, `getEntity`, source class, `SpellDamageEvent`, `LivingIncomingDamageEvent` e `SUMMON_DAMAGE`.
4. **PoisonArrow:** testar hit de projétil versus nuvem e listar eventos realmente recebidos; efeito de i-frames, proteção, PvP e claims.
5. **Paridade de perfil:** calcular SHA do arquivo instalado e compará-lo ao hash acima; sem isso, esta é prova do **artefato publicado**, não do pack físico local.

## Política de promoção

✅ `BINARY-STATIC-PROOF` apenas para estes quatro caminhos; ⚠️ `RUNTIME/PROFILE-QA-PENDING`; ⛔ `PER-PLAYER-PROJECTILE-COUNT/INHERITED-DAMAGE-ATTRIBUTION` bloqueado até GameTest e contrato provider-native. Não transferir ownership de magic runtime ao RPG Skill Tree, não tocar em `ArrowVolleyEntity` por mixin sem autorização e não promover Stage 06.05.

**Clean-room:** `javap` usado somente para prova de interfaces/métodos e fluxo relevante à interoperabilidade; nenhum bytecode, implementação ou asset de terceiro publicado na branch ou no artifact.
