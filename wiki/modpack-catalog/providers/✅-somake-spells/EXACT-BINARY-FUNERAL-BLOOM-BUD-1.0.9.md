# Somake Spells 1.0.9 — FuneralBloomBudEntity: efeito downstream SHA-exato

**Estado:** ✅ `EXACT_SHA1_FUNERAL_BLOOM_BUD_JVM_REFERENCES` / ⚠️ causalidade de runtime, valores e integração ainda condicionados / ⛔ sem mutador de perks homologado.

## Artefato e trilha de QA

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, entrada #513, `somakespells-1.0.9-1.21.1.jar`, CurseForge File 8867079, mod ID `somakespells`, SHA-1 físico/publisher `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [Workflow Java 21 #39197671447](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39197671447) **SUCCESS**, 10 testes sintéticos Java21, 26 métodos nomeados analisados, FQCN exato `com.somake.somakespells.entity.FuneralBloomBudEntity`, hash e metadata exigidos antes da inspeção.
- A primeira execução [#39197533908](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39197533908) passou, mas auditoria posterior identificou que o parser incluía o corpo de inicialização estática no último método nomeado. O script foi corrigido e passou novamente com dois testes adicionais: exclusão do inicializador estático e rejeição de múltiplos inicializadores. **A evidência usada aqui é apenas o resultado corrigido #39197671447.**
- [Scanner](../../../../docs/qa/somake_109_funeral_bud_probe.py), [testes](../../../../docs/qa/somake_109_funeral_bud_probe_test.py), [workflow](../../../../.github/workflows/somake-109-funeral-bud.yml). O JAR/código de terceiros não integra o repositório; somente símbolos, descritores e branches são registrados.

## Métodos e relações observadas no classfile

| Superfície | Assinaturas/callsites exatos | Consequência para engenharia |
|---|---|---|
| Identidade e alvo | `getControllerId/setControllerId(UUID)`, `getTargetUuid/setTargetUuid(UUID)`, `findController(ServerLevel)` | O bud possui referências sincronizadas de controlador e alvo; não comprova se o owner continuará válido em todos os eventos |
| Posicionamento | `getImpactPosition/setImpactPosition(Vec3)`, `updatePrediction(ServerLevel)`, `ServerLevel.getEntity(UUID)`, `LivingEntity.isAlive`, `FuneralBloomControllerEntity.groundPosition` | Há uma rota de predição do alvo e posicionamento de impacto; range/LOS/prediction lead numéricos não aferidos |
| Fases e duração | `getTelegraphTicks/setTelegraphTicks(int)`, `getFallTicks/setFallTicks(int)`, `beginRetreat`, `getTelegraphProgress`, `getFallProgress`, `getRetreatProgress` | Timers e estado `DATA_RETREATING` são campos separados, com `Math.max` e `Mth.clamp` em helpers; nenhuma fórmula/cap completo homologado |
| Ciclo de vida | `tick()` (11 instruções de branch no método capturado) referencia `Projectile.tick`, controlador, `beginRetreat`, `discard` e `impact` | Não concluir que cada tick causa hit, que o bud desaparece sempre ou que o disparo não é reentrante sem dataflow e servidor |
| Impacto | `impact(ServerLevel)` (31 instruções de branch) consulta `getImpactPosition`, `getOwner`, cria AABB, seleciona entidades com `getEntitiesOfClass`, consulta `isAlive`, `isAlliedTo`, `LivingEntity.hasEffect(WITHER)` e bounding boxes | Tipos/limites de alvo, critérios condicionais e tamanho da AABB dependem de análise de fluxo; não confundir shortlist com alvos atingidos |
| Dano | `impact` referencia `FuneralBloomSpell.getDamageSource`, `impactDamage` e `DamageSources.applyDamage(Entity,float,DamageSource)` | Candidato ao pipeline do Iron's, mas sem prova de dispatch de `SpellDamageEvent` ou hook de perk per-player |
| Wither | `impact` referencia `MobEffects.WITHER`, campos `witherDuration/witherAmplifier`, `MobEffectInstance` e `LivingEntity.addEffect` | Status separado de dano; valor, empilhamento e condições de aplicação pendentes |
| Cura | `impact` referencia `SpellHealEvent(LivingEntity,LivingEntity,float,SchoolType)`, `NeoForge.EVENT_BUS.post` e `LivingEntity.heal(float)` | **Callsite de evento encontrado**; evento pode ser condicionado, sem confirmação de leitura de eventual valor alterado/cancelamento ou quantidade real curada |
| Knockback e entidade secundária | `LivingEntity.push(DDD)`, `hurtMarked`, `FuneralBloomImpactEntity.<init>(Level,Vec3,float)` e `ServerLevel.addFreshEntity` | A entidade de impacto foi inspecionada em [auditoria própria](EXACT-BINARY-FUNERAL-BLOOM-IMPACT-1.0.9.md): expõe Scale sincronizado, abertura e descarte, sem callsites diretos de dano/cura nos oito métodos inspecionados; não inferir comportamento exclusivamente visual |
| Persistência | `readAdditionalSaveData(CompoundTag)`, `addAdditionalSaveData(CompoundTag)` referenciam controlador/alvo UUID, impact position, telegraph/fall, retreat, impactDamage e Wither metadata | Superfície NBT identificada, sem teste de round-trip, tolerância a NBT malformado, restart ou correlação de Mastery |

## Limites e consequências para perks

Uma magia **não deve** recompensar Mastery uma vez pelo casting, outra por cada bud e ainda outra por cada dano sem contrato explícito de correlação e contagem. Uma futura perk de dano e uma perk de cura precisam respeitar os pipelines independentes indicados em `impact()` e a autoridade original do Somake e do host Iron's. A presença de `SpellHealEvent` é prova de referência Java no JAR compilado, **não** prova de que qualquer handler, cancelamento ou mutação será aplicado em todas as condições.

Não derivar numerais, raio, quantidade de buds, duração, fórmula de escala, cooldown, proteção de mundo, cálculo de empuxo, multiplicidade ou compatibilidade de callback sem prova adicional. O valor numérico de um getter, a disponibilidade real do config, o processamento de branches e a validade do owner continuam desconhecidos neste gate. `FAIL_CLOSED` para adapters de mutação. Nenhum estado Stage 06.05/Stage 09 foi promovido.

**Seguinte cadeia causal a auditar:** `FuneralBloomSpell.onCast → FuneralBloomControllerEntity.launchWave → FuneralBloomBudEntity.tick/impact → FuneralBloomImpactEntity` (entidade de impacto agora inspecionada quanto a símbolos estáticos, ainda sem dataflow e gameplay). A seta representa **relações de referências e dependências catalogadas**, não execução garantida ou ordem causal provada em cada cast.

Fontes: [dossiê das cinco entidades](EXACT-BINARY-ENTITY-CALLSITES-1.0.9.md), [sete classes de casting](EXACT-BINARY-CAST-CALLSITES-1.0.9.md), [ficha da magia](registry-1.0.9/funeral-bloom.md).


## Continuação da entidade de impacto — 19/10/2026

A [auditoria exata da `FuneralBloomImpactEntity`](EXACT-BINARY-FUNERAL-BLOOM-IMPACT-1.0.9.md), [workflow #39198753251](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39198753251), encontrou **8 métodos** (incluindo `setScale(float)`, `getOpenProgress(float)`, `tick()`, leitura e gravação NBT). Não detectou referência direta de dano/cura/status nos oito métodos capturados, mas isso não exclui efeitos herdados ou outras dependências. A presença de `Mth.clamp` é prova de referência ao helper, não do intervalo numérico. Nenhum hook per-player ou QA de runtime foi homologado.
