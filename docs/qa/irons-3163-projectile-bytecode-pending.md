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

## Provas compiladas e interpretação

| Classe do JAR | Sinal observado em `javap -p -c` | Estado |
|---|---|---|
| `entity.spells.ArrowVolleyEntity` | `tick()` lê `tickCount`, **não chama `super.tick()` e não escreve diretamente `tickCount`** | ✅ provado estaticamente neste binário; ⛔ `tickCount` efetivo e limite de criação de flechas em gameplay não resolvidos |
| `entity.spells.small_magic_arrow.SmallMagicArrow` | `shoot(Vec3)` usa `setDeltaMovement` sem `getSpeed()`; `onHitEntity` referencia `ARROW_VOLLEY_SPELL` | ✅ provado para o caminho compilado; ⚠️ danos e hits aceitos não medidos |
| `entity.mobs.SummonedSkeleton` | Herda diretamente de `net.minecraft.world.entity.monster.Skeleton`; **não declara `performRangedAttack`** | ✅ prova da ausência de override local; ⚠️ classe vanilla/NeoForge e `DamageSource` de flecha herdada **não** inspecionados |
| `entity.spells.poison_cloud.PoisonCloud` | `applyEffect` referencia `POISON_CLOUD` e dano direto por `hurt`, **sem chamada a `DamageSources.applyDamage`** | ✅ prova de método compilado; ⚠️ eventos NeoForge gerais, outras inserções e resultado físico não certificados |

**Arrow Volley — risco especialmente importante:** no código-fonte `ArrowVolleyEntity.tick` condiciona disparos a `tickCount % 5 == 0`, mas o bytecode não mostra incremento local nem invocação a `super.tick`. A documentação NeoForge de entidades recomenda chamar `super.tick` e explica a passagem a `baseTick`, mas isto **não substitui** bytecode de `Entity`/GameTest para demonstrar precisamente o comportamento real. O risco de *unbounded per-tick spawn* continua **HIPÓTESE**, não defeito reproduzido; **⛔ +flechas ou multiplicadores automáticos de Arrow Volley bloqueados** até medir contador, cardinalidade por tick, descarte e persistência.

**SummonedSkeleton — limite de atribuição:** a prova de que `performRangedAttack` é herdado **não prova** que o `DamageSource` de flecha é `RAISE_DEAD_SPELL` ou não é. O golpe melee `doHurtTarget` já tem evidência distinta de `RAISE_DEAD_SPELL`. Para Mastery/XP de ranged, a atribuição continua ⚠️ condicionada à implementação do jogo e à observação de eventos reais.

**PoisonCloud — limite de observação:** o caminho `PoisonCloud.applyEffect` não usa o helper do provider que publica `SpellDamageEvent`; assim, filtrar somente `SpellDamageSource` no adapter não identifica o dano periódico da nuvem. Não afirmar ausência de todos os eventos NeoForge: `target.hurt` ainda pode publicá-los.

## Próximos testes que não foram executados

1. **GameTest/dedicated-server 1.21.1/NeoForge + JAR exato:** logar `ArrowVolleyEntity.tickCount` e o número de `SmallMagicArrow` criadas por tick, níveis 1 e 6, durante ≥ 100 ticks; avaliar se descarte é alcançado e se há budget fixo.
2. **GameTest de chunk/salvamento:** interromper/recarregar o controlador enquanto emite flechas; comparar `rows`, `arrowsPerRow`, contador e número de projéteis antes/depois.
3. **Vanilla/NeoForge skeleton ranged:** inspecionar bytecode de `Skeleton`/`AbstractSkeleton` e `AbstractArrow` da versão física, registrar `DamageSource.getDirectEntity`, `getEntity`, source class, `SpellDamageEvent`, `LivingIncomingDamageEvent` e `SUMMON_DAMAGE`.
4. **PoisonArrow:** testar hit de projétil versus nuvem e listar eventos realmente recebidos; efeito de i-frames, proteção, PvP e claims.
5. **Paridade de perfil:** calcular SHA do arquivo instalado e compará-lo ao hash acima; sem isso, esta é prova do **artefato publicado**, não do pack físico local.

## Política de promoção

✅ `BINARY-STATIC-PROOF` apenas para estes quatro caminhos; ⚠️ `RUNTIME/PROFILE-QA-PENDING`; ⛔ `PER-PLAYER-PROJECTILE-COUNT/INHERITED-DAMAGE-ATTRIBUTION` bloqueado até GameTest e contrato provider-native. Não transferir ownership de magic runtime ao RPG Skill Tree, não tocar em `ArrowVolleyEntity` por mixin sem autorização e não promover Stage 06.05.

**Clean-room:** `javap` usado somente para prova de interfaces/métodos e fluxo relevante à interoperabilidade; nenhum bytecode, implementação ou asset de terceiro publicado na branch ou no artifact.
