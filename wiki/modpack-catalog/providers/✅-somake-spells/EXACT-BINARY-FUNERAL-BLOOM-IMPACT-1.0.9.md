# Somake Spells 1.0.9 — FuneralBloomImpactEntity: métodos compilados

**Estado:** ✅ `EXACT_SHA1_FUNERAL_IMPACT_ENTITY_JVM_SYMBOLS` · ⚠️ comportamento em jogo e constantes numéricas pendentes · ⛔ nenhum contrato mutador de perks homologado.

## Prova física e testes

- Mod ID `somakespells`, versão **1.0.9**, modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`; JAR `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [GitHub Actions #39198753251](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39198753251) `SUCCESS`: sete testes sintéticos, verificação do publisher JAR por hash/metadata, classe concreta `com.somake.somakespells.entity.FuneralBloomImpactEntity` presente e **8 métodos nomeados** verificados por descritores e símbolos `javap`.
- [Probe](../../../../docs/qa/somake_109_funeral_impact_probe.py) · [testes](../../../../docs/qa/somake_109_funeral_impact_probe_test.py) · [workflow](../../../../.github/workflows/somake-109-funeral-impact.yml). Saída limita-se a símbolos JVM e contagens, sem código compilado ou assets de terceiros.

## Matriz dos oito métodos no classfile exato

| Método e descriptor | Fato verificável nas referências JVM |
|---|---|
| `defineSynchedData(SynchedEntityData.Builder):void` | Declara `DATA_SCALE` como dado sincronizado |
| `getScale():float` | Lê `DATA_SCALE` de `SynchedEntityData` |
| `setScale(float):void` | Referencia `Mth.clamp(float,float,float)` e `SynchedEntityData.set` |
| `getOpenProgress(float):float` | Referencia `tickCount`, `Mth.clamp`, `smoothstep(float)` |
| `smoothstep(float):float` | Método presente; não há referências simbólicas externas capturadas |
| `tick():void` | Duas instruções de branch; referencia `Entity.tick`, `Level.isClientSide`, `tickCount` e `discard()` |
| `readAdditionalSaveData(CompoundTag):void` | Lê `float` via `CompoundTag.getFloat` e chama `setScale` |
| `addAdditionalSaveData(CompoundTag):void` | Lê `getScale` e grava `float` via `CompoundTag.putFloat` |

## Matriz para perks

| Dimensão | Evidência | Condição de integração |
|---|---|---|
| Tamanho / visual do impacto | `DATA_SCALE` sincronizado, `setScale` chama clamp | ⚠️ Valores mínimo/máximo, unidade, geometria renderizada e influência sobre hitbox/dano **não verificados**. Não expor setter como hook per-player |
| Abertura e tempo | `getOpenProgress` usa `tickCount`, clamp e smoothstep; `tick` referencia `discard` | ⚠️ Duração em ticks e condições de descarte sem dataflow completo |
| Persistência | Pares `readAdditionalSaveData`/`addAdditionalSaveData` referenciam `Scale` | ⚠️ Round-trip, restart e estado cliente/servidor não testados |
| Dano / cura / status | No conjunto de **oito métodos nomeados analisados**, nenhum símbolo direto de `DamageSources.applyDamage`, `LivingEntity.hurt`, `SpellHealEvent`, `heal` ou `addEffect` foi observado | ⚠️ Não é prova negativa de execução herdada/delegada; sem fórmula ou evento disponível |
| Geometria de alvo | Nenhum callsite explícito de aquisição por AABB/raycast identificado nesses oito métodos | ⚠️ Não concluir que o efeito não interage com outros mecanismos |
| Mutação por perk | Um setter `setScale(float)` compilado não representa contrato API seguro | ⛔ `FAIL_CLOSED` até adapter real de versão exata e observação por jogador |

**Interpretação restrita:** os nomes e membros são consistentes com uma entidade de apresentação transitória do impacto; esta é uma **inferência estrutural**, não prova de comportamento exclusivamente visual. O dano, Wither, cura e knockback identificados na [FuneralBloomBudEntity](EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md) continuam os callsites de efeito mecânico já localizados. A auditoria não reconstrói todas as branches do pipeline, não prova valores ou ausência de métodos herdados.

## Ownership e continuação

O Black Arcana mantém somente a autoridade sobre seu runtime próprio. Somake é owner da entidade; Iron's dos seus contratos de casting/recursos e helpers quando utilizados; RPG Skill Tree expõe progressão/perks apenas através de contratos reais. Não duplicar danos, curas, custos, cooldown ou créditos de Mastery com base no spawn de uma entidade de apresentação.

**Próximo gate:** auditoria de valores numéricos e dataflow dos `getRadius/getImpactDamage/getHealing`, clamps e dos caminhos de `tick/impact`, com a mesma identidade física; depois QA provider-loaded, cliente, multiplayer, Survival e modpack sob D035. Nenhuma nova magia ou Stage promovida.
