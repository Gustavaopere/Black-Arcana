# Somake 1.0.9 — Funeral Bloom: consumidores estruturais de raio e seleção de alvos

**Estado vigente após PR #843 (20/10/2026):** ✅ raio sincronizado → AABB expandida → consulta de candidatos e **bootstrap #0 do `Predicate` vinculado a `lambda$launchWave$0` por `REF_invokeVirtual`** · ⚠️ resultados dos branches, elegibilidade, alvo final, `maxTargets`, buds/impacto e QA físico não demonstrados · ⛔ perks mutadoras `FAIL_CLOSED`. As seções históricas mantêm seu escopo temporal.

## Proveniência física

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, Somake `somakespells-1.0.9-1.21.1.jar`, CurseForge File **8867079**, mod ID `somakespells`, SHA-1 **`171841ac9f802be9309ecc166c1d972ac6d404c0`**. Ambiente Minecraft 1.21.1 / NeoForge / Java21.
- [Workflow de auditoria de consumidores #39262591589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39262591589): `SUCCESS`, **9 testes** sintéticos/negativos e inspeção de 3 classfiles físicos. Um HEAD subsequente congela o conjunto esperado de callsites e descritores de versão exata; só resultados desse HEAD são elegíveis para merge.
- [Verificador](../../../../docs/qa/somake_109_radius_consumers.py), [testes](../../../../docs/qa/somake_109_radius_consumers_test.py), [workflow](../../../../.github/workflows/somake-109-radius-consumers.yml). A saída contém assinaturas de métodos e referências simbólicas agrupadas por método, nunca JAR, implementação Java, bytecode ou assets do publisher.

## Matriz estrutural dos métodos compilados

| Classe / método | Instruções JVM | Invocações estáticas/virtuais/especiais | `invokedynamic` | Referências relevantes |
|---|---:|---:|---:|---|
| `FuneralBloomSpell.onCast(Level,int,LivingEntity,CastSource,MagicData)` | 81 | 21 | 1 | `getRadius(int,LivingEntity):float`; `getImpactDamage(int,LivingEntity):float`; construtor de `FuneralBloomControllerEntity` |
| `FuneralBloomSpell.getRadius(int,LivingEntity)` | 28 | 4 | 0 | Getter com duas expressões certificadas [na auditoria de caminhos](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md) |
| `FuneralBloomControllerEntity.tick()` | 156 | 29 | 0 | `getRadius():float` e `launchWave(ServerLevel):void` |
| `FuneralBloomControllerEntity.launchWave(ServerLevel)` | 196 | 36 | 2 | `getRadius():float`, `AABB.inflate(double,double,double)`, `ServerLevel.getEntitiesOfClass`, `getOwner()`, criação de `FuneralBloomBudEntity` |
| `FuneralBloomBudEntity.tick()` | 150 | 33 | 0 | lifecycle, dependência do estado da controller (`isRemoved`) e posições da entidade |
| `FuneralBloomBudEntity.impact(ServerLevel)` | 279 | 35 | 0 | `LivingEntity.getBoundingBox`, `AABB.inflate(double,double,double)`, `ServerLevel.getEntitiesOfClass`, `DamageSources.applyDamage`, `SpellHealEvent`, `LivingEntity.heal`, `getOwner`, `isAlliedTo` |

## Descritores relevantes para integração

- `onCast` invoca `getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F`, além de construir a controller com descriptor **`(Level,LivingEntity,float,int,int,int,int,float,int,int)void`** na forma JVM `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V`. **Dois argumentos do construtor são float**, mas a coincidência com o getter não comprova qual posição recebe o resultado; isso exigirá reconstrução de pilha da instrução `invokespecial`.
- `controller.tick` e `controller.launchWave` invocam `getRadius:()F`, que é a superfície de leitura do estado da controller. Ainda não há prova de campo backing específico, valor originalmente copiado nem unidade de medida.
- `controller.launchWave` passa por `getBoundingBox`/`AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;`, depois possui chamada a `ServerLevel.getEntitiesOfClass` e instancia bud com descriptor **`(Level,FuneralBloomControllerEntity,LivingEntity,Vec3,int,float,int,int)void`**. A presença dessas referências no mesmo método **não** garante que `getRadius()` seja a dimensão de `inflate` nem que todo alvo elegível gere bud.
- `bud.impact` possui uma **segunda** chamada independente a `AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;` e a `ServerLevel.getEntitiesOfClass`. Nesse método há referências a `DamageSources.applyDamage`, `SpellHealEvent` e `LivingEntity.heal`. O **método `bud.impact` não possui callsite direto `getRadius`**, então não atribuir automaticamente à área de dano o mesmo raio de `controller.launchWave`.

## Causalidade e status de perks

**Comprovado:** as referências de execução e símbolos acima existem nos seis métodos específicos do JAR 1.0.9; `onCast` conhece o getter do spell e a construção da controller; a controller consulta seu próprio `getRadius` e possui um caminho de seleção; a bud possui seleção/área e efeitos próprios. **Não comprovado:** dataflow de valores através dos argumentos dos construtores, distância da AABB em cada fase, hierarquia de branch/lifetime, alcance em blocos, eficácia de dano/cura/Wither, deduplicação por vítima, owner válido, comportamento em cliente/multiplayer ou presença real da API modificadora.

Dois eixos potenciais permanecem separados no catálogo: **raio de seleção/lançamento de buds** e **área de impacto de cada bud**. Mesmo quando ambos usam `AABB.inflate`, podem ter escalas e regras independentes. Não usar o retorno de `FuneralBloomSpell.getRadius` para implementar uma perk de área sem prova de dependência e hook versionado.

- ⛔ **FAIL_CLOSED** para perks per-player de raio, tamanho de área, targeting, dano, status, duração e quantidade de buds.
- ⚠️ `invokedynamic` ocorre em `onCast` (1) e `launchWave` (2): o probe registra a contagem, **não** imputa automaticamente alvo de lambda, predicado ou callback.
- ⚠️ Stage 06.05 segue 🟡; Stage 09 retém QA provider-loaded, Survival, cliente/multiplayer e modpack físico, conforme D035. Black Arcana mantém autoridade do runtime próprio; Somake executa sua magia; Iron's preserva o host e recursos; RPG Skill Tree apenas progressão por contrato real.

**Métricas:** Somake **83/83** identidades previamente inventariadas; cinco fichas com auditoria de entidades downstream sobre 83 (**6,02%**), sete classfiles downstream distintos no acumulado. **Zero** identidade ou adaptador adicional neste lote. [Ficha individual](registry-1.0.9/funeral-bloom.md) · [raio JVM](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md) · [controller/bud](EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md).

## Prova de operandos da expansão da AABB — 19/10/2026 (PR #840)

**Publisher SHA-exato:** `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. Na [auditoria Java21 #39304248399](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39304248399), **21 testes sintéticos/negativos passaram**; os três argumentos `double` de `FuneralBloomControllerEntity.launchWave(ServerLevel) → AABB.inflate:(DDD)AABB` foram rastreados por uma sequência local JVM estrita, não apenas pelo conjunto de callsites.

| Argumento de `inflate` | Proveniência certificada, versão 1.0.9 |
|---|---|
| Primeiro — **X** | `aload_0 → invokevirtual getRadius:()F → f2d` da controller |
| Segundo — **Y** | literal tipado JVM **`10.5d`** (`double`), sem consumo de `getRadius` nessa posição |
| Terceiro — **Z** | `aload_0 → invokevirtual getRadius:()F → f2d` da controller |

**Expressão certificada dos operandos:** `AABB.inflate((double) controller.getRadius(), 10.5d, (double) controller.getRadius())`. São argumentos de expansão nos três eixos do objeto AABB, não uma prova de raio esférico, de dano ou de aquisição de alvo no mundo. O getter da controller lê `SynchedEntityData.get(DATA_RADIUS)`; a cadeia upstream `FuneralBloomSpell.getRadius → primeiro float do construtor → setRadius(clamp 6–18) → DATA_RADIUS` já foi validada nas PRs #838/#839. O getter upstream do spell possui clamp separado `10–15` para entradas finitas (auditoria tipada independente).

**Por que foi necessária a segunda hipótese:** o [scanner estrutural SHA-exato #39303857720](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39303857720) encontrou três chamadas `getRadius` no método inteiro, mas **somente duas antes** da única chamada `inflate`, com conversões `f2d` e intervalos relativos de instruções 5 e 1. O padrão rejeitado de três getters adjacentes retornou `NOT_PROVED`, corretamente; o modelo local de **dois getters X/Z mais literal `double` em Y** foi então certificado sem reclassificar chamadas posteriores.

**Limites estritos:** a cadeia do **objeto AABB receptor** e o encaminhamento da **AABB resultante** a `ServerLevel.getEntitiesOfClass` não foram aqui reconstruídos; tampouco a escolha do owner/caster, filtros de distância/equipe, cardinalidade, criação efetiva de buds, `FuneralBloomBudEntity.impact` (AABB própria), dano/cura, alcance percebido em blocos, configs, Survival, cliente ou multiplayer. Não interpretar `10.5d` como alcance vertical **efetivo** de uma perk antes do consumidor e da QA. A ausência de hook público de mutação por jogador mantém ⛔ `FAIL_CLOSED`.

**Contagens:** Somake **83/83** IDs exatos; **5/83** fichas com entidade downstream auditada na campanha e **0** adapters mutadores homologados. Não acrescenta novo spell nem permite promoção de Stage. Sem redistribuir JAR, bytecode, código ou assets do provider.

## Nova prova física: AABB expandida → slot JVM 3 → consulta de entidades (20/10/2026; PR #841)

**Contexto exato:** `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`; Somake Spells 1.0.9, mod ID `somakespells`, File 8867079, `somakespells-1.0.9-1.21.1.jar`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. Java 21; método `com.somake.somakespells.entity.FuneralBloomControllerEntity#launchWave(ServerLevel)`, **196 instruções JVM**.

O [workflow #39465768438](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465768438) executou **28 testes** e identificou fisicamente `PROVED_WAVE_INFLATE_RESULT_CONSUMED_BY_ENTITY_QUERY` / `aabb_transport=via_local_3`. Após adicionar gate estrito de versão, o [workflow #39466062186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39466062186) concluiu `SUCCESS` com **29 testes** e `PASS_SHA_EXACT_WAVE_XZ_RADIUS_Y_10_5_AND_QUERY_AABB_LINK`.

**Certificado no corpo compilado:** após `AABB.inflate((double)getRadius(),10.5d,(double)getRadius())`, o objeto AABB produzido é guardado em `astore_3`. Na mesma janela sem escritas intermediárias sobre esse slot, `aload_3` devolve a caixa à pilha; o argumento AABB é consumido pelo descriptor exato `ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;`. O fluxo abrange **nove instruções intermediárias** e **uma consulta**. O argumento `Class` é `LivingEntity`. O `Predicate` é produzido por `invokedynamic` que captura referências tipadas da controller e de `LivingEntity`; sua **lógica de aceitação interna NÃO foi examinada**.

**RED → GREEN:** a fixture de passagem direta falhou corretamente no [RED #39465037334](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465037334), pois o JAR real possui armazenamento intermediário; o [GREEN #39465768438](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465768438) certificou o novo padrão. O gate de regressão físico falhou de propósito em sete desvios no [RED #39465962139](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465962139) e passou no [GREEN #39466062186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39466062186), que exige slot local 3, nove instruções, descriptor exato e fingerprint de 196 instruções.

**Limites:** a relação **expansão → consulta de candidatos** está comprovada, mas não a geometria inicial da caixa receptora, nem o resultado efetivo do `Predicate`, elegibilidade PvP/aliados, distância extra, cardinalidade, escolha final, formação de buds ou AABB independente em `FuneralBloomBudEntity.impact`. Não há API/hook homologado de mutação per-player; **⛔ FAIL_CLOSED**. Esta auditoria acrescenta profundidade a uma magia preexistente, não IDs ou adapters. Não redistribui JAR, bytecode, implementação ou assets do provider.

## Prova de vínculo `Predicate → lambda$launchWave$0` (20/10/2026, PR #842)

A [auditoria Java 21 SHA-exata #39471626461](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39471626461), **SUCCESS / 38 testes**, validou o publisher Somake 1.0.9 File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` e elevou o vínculo entre a consulta de entidades e sua implementação de `Predicate` de mera coocorrência para **`PROVED_QUERY_PREDICATE_BOOTSTRAP_TO_LAUNCHWAVE_LAMBDA0`**. O gate físico `PASS_SHA_EXACT_WAVE_QUERY_PREDICATE_BOOTSTRAP_BOUND` exige `InvokeDynamic #0:test`, `BootstrapMethods[0]` com `LambdaMetafactory.metafactory`, **`REF_invokeVirtual`** da própria `FuneralBloomControllerEntity`, helper booleano e fingerprints locais.

| Método do provider (JAR físico) | Evidência técnica certificada | Restrição |
|---|---|---|
| `lambda$launchWave$0(LivingEntity,LivingEntity):boolean` | **15 instruções, 2 branches condicionais**, chama `isValidTarget:(LivingEntity,LivingEntity)Z`, `LivingEntity.getUUID()`, `Set.contains(Object)` e lê `activeTargetIds:Ljava/util/Set;`. O bootstrap **#0**, consumido como `Predicate` por `getEntitiesOfClass(Class,AABB,Predicate)`, aponta para este helper por `REF_invokeVirtual`. | **Não** se certificou o valor booleano de cada ramo, o tratamento de owner/caster, a expressão lógica composta ou quais alvos passam |
| `lambda$launchWave$1(LivingEntity):double` | **4 instruções, zero branches**, chama `LivingEntity.distanceToSqr(Entity):double`. | A existência do helper **não prova** ainda o uso como comparador/ordenador, seu binding de bootstrap ou distância máxima |

**Cadeia de aquisição até o filtro:** `FuneralBloomSpell.getRadius → first constructor float → setRadius(clamp 6–18) → DATA_RADIUS → controller.getRadius() → AABB.inflate(R,10.5d,R) → local 3 → getEntitiesOfClass(LivingEntity.class,AABB,Predicate)` com `Predicate` vinculado fisicamente ao helper `lambda$launchWave$0`. A AABB base, os resultados booleanos dos dois branches, exclusão por equipe/PvP/claim, iteração da lista, `maxTargets`, criação das buds e a AABB independente de `FuneralBloomBudEntity.impact` **seguem não comprovados**.

**RED–GREEN:** a hipótese de method handle estático foi rejeitada em [RED #39471158372](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39471158372); o [GREEN #39471258573](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39471258573) demonstrou `REF_invokeVirtual`; oito casos negativos do gate físico de impressão digital falharam deliberadamente em [RED #39471476260](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39471476260) e passaram em [GREEN #39471626461](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39471626461). A auditoria limita sua exportação a assinaturas, contagens e símbolos relevantes, sem JAR/bytecode/implementação/asset de terceiro.

**Perks:** nenhum hook de mutação de `Predicate`, `activeTargetIds` ou `maxTargets` é autorizado; **⛔ FAIL_CLOSED**. Nenhuma alteração de runtime/casting/dano ou Stage.

## Regra booleana do `Predicate` — caminhos condicionais exatos (20/10/2026, PR #843)

**Publisher SHA-exato:** Somake 1.0.9, mod ID `somakespells`, File 8867079, `somakespells-1.0.9-1.21.1.jar`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`. O [workflow Java21 #39504441297](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39504441297) concluiu `SUCCESS`, **45 testes**, gate `PASS_SHA_EXACT_WAVE_BOOLEAN_VALID_AND_UUID_NOT_ACTIVE`.

Pelo vínculo de bootstrap #0/ `REF_invokeVirtual` já certificado na PR #842, o `Predicate` da consulta de candidatos é implementado por `FuneralBloomControllerEntity.lambda$launchWave$0(LivingEntity,LivingEntity):boolean`. A auditoria de **15 instruções JVM** reconstruiu seu grafo de controle estrito: chamada `isValidTarget(LivingEntity,LivingEntity):boolean` seguida imediatamente de `ifeq` que leva ao resultado **falso**; em seguida, leitura da field `activeTargetIds:Ljava/util/Set;` sobre a controller, UUID da segunda referência `LivingEntity.getUUID():UUID` e `Set.contains(Object):boolean`, seguido imediatamente de `ifne` que também leva ao resultado **falso**. Somente a condição válida **e UUID ausente do conjunto** percorre o resultado **verdadeiro**. Os dois caminhos reúnem-se em **um `ireturn`**; a outra transferência incondicional ao join foi certificada. A fórmula booleana estática é:

`isValidTarget(capturedLivingEntityA,capturedLivingEntityB) && !activeTargetIds.contains(capturedLivingEntityB.getUUID())`.

Os testes negativos rejeitam inversão dos branches, targets divergentes, símbolo/owner de `Set.contains` e campo `activeTargetIds`, mudança na ordem das três chamadas e alteração da junção. O primeiro modelo de **dois** `ireturn` foi rejeitado no JAR real, antes de se reconstruir o modelo de um único retorno. O gate versionado falhou com **nove** mutações deliberadas em [RED #39504344777](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39504344777) e passou em [GREEN #39504441297](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39504441297).

**Limites técnicos:** as duas referências capturadas são tipadas `LivingEntity`, mas a certificação ainda não resolve seus papéis definitivos de owner/caster/candidato no gameplay nem o corpo independente de `isValidTarget` (filtro PvP, equipe, alive etc.). A referência JVM `maxTargets:I` aparece em `launchWave`, mas **nenhuma prova de fluxo até um limite de quantidade de buds** foi homologada. Não foi auditado o consumo da lista, a criação/cardinalidade final de `FuneralBloomBudEntity`, a AABB independente de `bud.impact`, efeitos de dano/cura ou comportamento cliente/servidor modpack físico. `FAIL_CLOSED` para mutações por perks; nenhum adapter ou runtime alterado. Esta é a mesma identidade `somakespells:funeral_bloom`, sem incremento da contagem global.

## IsValidTarget nativo e leituras de maxTargets — prova estrutural exata (20/10/2026; PR #844)

O [workflow Java 21 #39507349822](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39507349822) concluiu `SUCCESS`, **53 testes**, no JAR publisher `somakespells-1.0.9-1.21.1.jar` (CurseForge File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`). A prova `PASS_SHA_EXACT_NATIVE_SELECTION_SHAPE_AND_MAXTARGETS_COSITES` certifica **somente o fingerprint técnico** de métodos e coocorrências, não o resultado de gameplay.

- **Método nativo `FuneralBloomControllerEntity.isValidTarget(LivingEntity,LivingEntity):boolean`:** presente no corpo compilado com **41 instruções**, **9 invocações**, **6 desvios condicionais** com opcodes `ifeq, ifne, if_acmpne, ifnull, ifeq, ifgt`, **3 `ireturn`**, nenhum acesso a field e zero `invokedynamic`. Referências simbólicas verificadas: `LivingEntity.isAlive()`, `isSpectator()`, `isAlliedTo(Entity)`, `distanceToSqr(double,double,double)`, `LivingEntity.getY()`, `getX()`, `getZ()` e `FuneralBloomControllerEntity.getRadius()`. As combinações e os sentidos dessas verificações, valores/relações numéricas e papéis dos dois `LivingEntity` permanecem **NOT_PROVED**.
- **`FuneralBloomControllerEntity.launchWave(ServerLevel)`:** **196 instruções** e **4 branches condicionais**; **2 leituras** compiladas `getfield maxTargets:I`, **1** chamada ao construtor de `FuneralBloomBudEntity` e a primeira leitura ocorre **49 instruções antes** da chamada. Esse intervalo não autoriza concluir que a criação é limitada por `maxTargets`, nem quantidade efetiva, multiplicadores ou defaults.
- **Cadeia preservada:** `FuneralBloomSpell.getRadius → controller.setRadius → DATA_RADIUS → AABB.inflate(R,10.5d,R) → local JVM 3 → getEntitiesOfClass(LivingEntity.class,AABB,Predicate)`. O `Predicate` validado em PR #843 continua `isValidTarget(A,B) && !activeTargetIds.contains(B.getUUID())`, porém a implementação interna de `isValidTarget` ainda não foi certificada semanticamente.
- **TDD:** casos positivos e negativos do scanner foram observados inicialmente RED no [workflow #39506633942](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39506633942), GREEN físico [#39506740495](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39506740495). A costura `maxTargets` foi testada com negativa antes de GREEN [#39507010262](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39507010262). O gate versionado falhou contra mutações intencionais no [RED #39507257929](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39507257929) e ficou GREEN no [#39507349822](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39507349822). Não há reprodução de body/JAR/bytecode/código externo nos arquivos.
- **Bloqueios mantidos:** certificação por CFG de `isValidTarget` (owner/equipe/PvP, alive, spectator, alcance), cadeia quantitativa de `maxTargets` até um cap, consulta final de alvos, impacto de buds, dano/cura e contrato público de mutação por jogador. ⛔ `FAIL_CLOSED` para perks/atributos/Mastery. Nenhuma nova magia, nenhum adapter ou mudança de runtime. Stage 06.05 🟡, Stage 09 físico PENDING.

## Branches físicos e rejeições iniciais de isValidTarget (20/10/2026, PR #845)

**Identidade física:** `somakespells-1.0.9-1.21.1.jar`, Somake 1.0.9, File 8867079, mod ID `somakespells`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, Java 21, modlist `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.

[Workflow #39511081176](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39511081176): `SUCCESS`, **61 testes**, gate `PASS_SHA_EXACT_NATIVE_ISVALIDTARGET_EARLY_GUARDS_AND_CFG`. O método `FuneralBloomControllerEntity.isValidTarget(LivingEntity,LivingEntity):boolean` preserva **41 instruções JVM, seis branches e três retornos booleanos**. O novo scanner certifica seis destinos de branch (índices estruturais, não bytecode redistribuído): `ifeq` posição 2 → 9 (constante `false`); `ifne` posição 5 → 9 (`false`); `if_acmpne` posição 8 → 11 (continuação); `ifnull` posição 12 → 19 (continuação); `ifeq` posição 16 → 19 (continuação); `ifgt` posição 36 → 39 (constante `false`). Esses destinos estão protegidos por gate físico versionado.

**Primeira porção do CFG com dataflow de operandos verificado:** o método aplica `LivingEntity.isAlive()` sobre a referência do **slot JVM 2** e retorna `false` se o resultado for falso; aplica `LivingEntity.isSpectator()` à **mesma referência** e retorna `false` se for verdadeira; compara por **identidade de objeto** (`if_acmpne`) a referência do **slot 2** com a do **slot 1** e retorna `false` se forem idênticas. Só depois percorre as condições restantes. A hipótese inicial de slot 1 como referência avaliada foi rejeitada e corrigida por prova física.

**TDD / clean-room:** RED inicial do inventário de CFG [#39510087699](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39510087699); GREEN de mapeamento dos seis destinos [#39510203524](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39510203524) (**56 testes**); mismatch físico dos slots diagnosticado em [#39510662483](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39510662483); RED discriminante para slot real em [#39510757065](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39510757065); GREEN da prova dos três guardas [#39510823945](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39510823945) (**60 testes**). O gate estrito rejeitou mutações de fingerprint em [RED #39510995945](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39510995945) e passou em [GREEN #39511081176](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39511081176) (**61 testes**). Nenhum JAR, body, classfile, opcode dump ou assets do provider foi comitado.

**Limites:** não foi certificado o fluxo concreto dos operandos dos três últimos branches (`ifnull`, `ifeq`, `ifgt`), nem as relações exatas de `isAlliedTo` e `distanceToSqr` e o cálculo de alcance, ou qual slot corresponde a owner/caster/candidato no gameplay. `maxTargets` continua apenas com duas leituras coocorrentes, não um cap comprovado; spawn/cardinalidade de buds, AABB e dano/cura de `bud.impact`, QA físico e hooks mutadores seguem condicionados. **⛔ FAIL_CLOSED**. Esta auditoria aprofunda a identidade preexistente `somakespells:funeral_bloom`, não incrementa a contagem de magias.

## Guardas intermediárias nativas — referência nula e aliança (20/10/2026; PR #847)

**Novo probe físico independente:** [workflow #39521070264](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39521070264), Somake 1.0.9 File 8867079 com SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, Java 21 `SUCCESS`. A análise reaplica `certify_exact_native_target_cfg_109` antes de interpretar a janela. O novo `certify_exact_native_middle_109` exige explicitamente os slots 1/2/1, branch de referência nula, chamada tipada `LivingEntity.isAlliedTo(Entity):boolean`, os destinos compartilhados e retorno falso, rejeitando mudanças de slot mesmo quando a estrutura dos opcodes permanece semelhante.

**Fatos derivados do classfile**, sem exportar bytecode nem código de terceiros:

1. A referência consultada por `ifnull` é a do **slot 1**; referência nula pula diretamente a rejeição local.
2. A chamada `isAlliedTo` usa **receptor slot 2** e **argumento slot 1**, retornando booleano.
3. O `ifeq` salta para a continuação quando o booleano é falso. Quando verdadeiro, o retorno do método é diretamente `false`.
4. A continuação comum é a instrução estrutural **19** do método de **41** instruções. A passagem por esse ponto não comprova aceitação; o `ifgt` posterior permanece sem regra numérica certificada.

A causalidade local corresponde a `slot1 != null && slot2.isAlliedTo(slot1) ⇒ rejeição`. **Ainda não está certificado** se slot 1 significa owner/caster ou se slot 2 significa candidato no contexto de jogo; `ifgt` / `distanceToSqr`, `maxTargets`, criação efetiva das buds, PvP/claims e hooks por jogador permanecem `NOT_PROVED`. Contrato de perk: **⛔ FAIL_CLOSED**. Somake 83/83 identidades; 5/83 fichas com downstream desta campanha, inalteradas.

[Scanner middle guards](../../../docs/qa/somake_109_native_filter_middle.py) · [testes](../../../docs/qa/somake_109_native_filter_middle_test.py) · [ficha](registry-1.0.9/funeral-bloom.md).

## Fórmula do último `ifgt` — dataflow JVM de distância e raio ao quadrado (PR #848)

**Fonte:** JAR Somake 1.0.9 File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [workflow físico Java 21 #39523827891](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39523827891), `SUCCESS`, **12 testes sintéticos**. Fingerprint do scanner anterior de 41 instruções/seis branches e do filtro de aliados é reaplicado antes da prova final. O primeiro probe [#39523500039](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39523500039) rejeitou corretamente uma hipótese de uma única leitura do raio; o segundo [#39523682490](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39523682490) comprovou seis chamadas coordenada/distância/raio e identificou as operações `dstore_3/dload_3` inicialmente não interpretadas.

**Cadeia compilada sem exportar body/bytecode:** `slot2.distanceToSqr(slot0.getX(),slot2.getY(),slot0.getZ())` produz um `double` armazenado/recuperado no slot 3. O limiar é `f2d(fmul(slot0.getRadius(),slot0.getRadius()))`. Segue `dcmpg` e `ifgt` com destino ao retorno literal `false`. O verificador constrói a árvore simbólica `cmp(distSq(slot2,x(slot0),y(slot2),z(slot0)),(R*R)) > 0` por operações JVM tipadas. Para entradas finitas, a rejeição corresponde à distância **no plano XZ**, porque a coordenada Y passada é a da própria entidade medida. **A comparação é contra raio ao quadrado em float32**, não uma distância euclidiana vertical em relação à controller.

**Limites:** slots JVM não equivalem, sem outro gate, a identidade real de caster/owner/alvo; `dcmpg` rejeita NaN via ramo `ifgt`; não inferir raio PvP/claims, AABB da bud, cap `maxTargets`, prioridades/sort, consequências em jogo, mutação por perks ou Mastery. Nova prova = profundidade de `somakespells:funeral_bloom`, **+0** feitiços/adapters; Stage 06.05 🟡 / Stage 09 físico pendente. [Script](../../../docs/qa/somake_109_native_distance_branch.py) · [regressões](../../../docs/qa/somake_109_native_distance_branch_test.py) · [ficha](registry-1.0.9/funeral-bloom.md).

## maxTargets — do corte da lista até a tentativa de bud (20/10/2026, PR #849)

**Release SHA-exato:** Somake 1.0.9 File 8867079, `171841ac9f802be9309ecc166c1d972ac6d404c0`. O gate anterior de duas leituras do campo e um construtor era apenas estrutural. O scanner [`somake_109_wave_maxtargets.py`](../../../docs/qa/somake_109_wave_maxtargets.py), [testes](../../../docs/qa/somake_109_wave_maxtargets_test.py) e [workflow](../../../.github/workflows/somake-109-wave-maxtargets.yml) consolidam provas derivadas sem exportar JAR/bytecode/body.

1. **Limitação de lista:** `List.size` da lista JVM local **4** é comparado à primeira leitura do campo `maxTargets:I`; `if_icmple` desvia o truncamento no caso `size<=maxTargets`. Quando maior, `List.subList(0,maxTargets)` consome a segunda leitura do campo, e o resultado substitui a lista local **4**.
2. **Transporte até iteração:** `List.iterator` recebe o slot **4** após o join do branch. O iterador resultante é armazenado no slot **6**; `Iterator.hasNext` governa entrada/saída, com corpo no loop contíguo e back-edge conhecido.
3. **Tentativas normais e deduplicação:** por iteração normal não excepcional do loop, há exatamente um sítio de construtor da bud, uma chamada `ServerLevel.addFreshEntity(Entity):boolean` cujo retorno é descartado, e `Set.add(UUID):boolean` associado ao field `activeTargetIds`, também com retorno descartado. Não confundir **chamada** com **spawn confirmado**, nem presença de inserção em Set com identidade causal certificada do UUID.

**Provas:** [auditoria inicial #39526636618](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39526636618) verificou SHA, 6 testes e inventário semântico; [gate de lista #39527264831](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39527264831) `SUCCESS`; [auditoria iterativa #39527484911](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39527484911) `SUCCESS` com 19 regressões. CI do HEAD definitivo será conferido à parte.

**Boundary:** o tamanho válido/não-negativo de `maxTargets` no cast real, entrada do argumento no construtor, exceções/cancelamentos, persistência de buds, identidade do UUID, PvP/claims, impacto de bud e QA de jogador são `NOT_PROVED`. ⛔ Nenhum adapter/perk de cardinalidade ativado. Mesma identidade `somakespells:funeral_bloom`; +0 magias e +0 adapters. [Ficha](registry-1.0.9/funeral-bloom.md).

## Prova da geometria independente da bud e consumo da AABB (21/10/2026, PR #850)

O [workflow físico Java21 #39529183029](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39529183029) confirmou, no arquivo oficial Somake 1.0.9 File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, a cadeia de `FuneralBloomBudEntity.impact(ServerLevel)` com **279 instruções JVM**. Foram aprovados **14 testes sintéticos** no scanner clean-room.

**Causalidade certificada:** `getImpactPosition():Vec3 → slot 2 → new AABB(slot2,slot2) → inflate(1.75d,1.35d,1.75d) → slot 5 → ServerLevel.getEntitiesOfClass(LivingEntity.class,slot5)`. A consulta usa a sobrecarga **sem Predicate**, de dois argumentos explícitos. A dimensão resultante da caixa de consulta (quando a origem tem ambos os extremos coincidentes) é **3,50 × 2,70 × 3,50**. Esse volume é independente da AABB anterior da controller, que usa `controller.getRadius()` nos eixos X/Z e `10.5d` no eixo Y. A primeira geometria identifica candidatos ao lançamento; esta segunda identifica entidades presentes na região local do impacto.

**Superfície de efeitos identificada, ainda não atribuída causalmente:** `DamageSources.applyDamage` (índice de instrução 118), `addEffect` (132), `push` (138), `SpellHealEvent` (167), `heal` (172). A sequência de índices **não comprova execução**, dano aceito, heal realizado, condições de aliado ou deduplicação. Existem branches no método e critérios internos não certificados.

**Boundary:** ⛔ nenhuma perk de raio/dano/cura/target/hitbox liberada; nenhum contrato de modificação por jogador foi encontrado; arquivo de catálogo e scanner não alteram provider, casting ou runtime Black Arcana. Stage 06.05 🟡 / Stage 09 QA físico pendente. Somake 83/83 identidades, 5/83 fichas downstream nesta campanha, +0 identidades. [Verificador](../../../docs/qa/somake_109_bud_impact_geometry.py) · [ficha](registry-1.0.9/funeral-bloom.md).

## Guardas nativos de dano/Wither/empurrão e cura — PR #851 (20/10/2026)

**JAR SHA-exato:** Somake Spells 1.0.9, CurseForge File **8867079**, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. O [run Java21 #39531339901](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39531339901) passou com **22 testes**, após reaplicar `certify_exact_impact_geometry_109` para a AABB da bud da PR #850.

**Dano e efeitos:** em `FuneralBloomBudEntity.impact(ServerLevel)`, o retorno `boolean` do callsite `DamageSources.applyDamage` (índice 118) é consumido pelo `ifeq` seguinte (119). O ramo falso salta ao índice 145, no retorno ao laço; o verdadeiro executa bloco sem jumps internos no qual há a referência nativa `MobEffects.WITHER` (123), construção de `MobEffectInstance` (131), `LivingEntity.addEffect` (132), descarte do retorno (133) e `Entity.push` (138). O CFG auditado não possui ingressos externos ao intervalo 120–138. Portanto, a chamada de dano com retorno falso **não executa os callsites de Wither/push desse bloco**. Retorno verdadeiro prova o caminho de invocação normal, não efeito aceito, dano ou magnitude.

**Cura condicional distinta:** dois guards independentes na mesma função usam `aload 4 → ifnull` (147) e `iload 6 → ifle` (149). Ambos pulam ao índice 173, evitando a sequência interna de evento/cura. No caminho normal em que slot 4 é não nulo e slot 6 é positivo, o método constrói `SpellHealEvent` (167), chama `post` (168), descarta esse retorno (169) e invoca `LivingEntity.heal(F)` (172) com receptor **slot 4** e argumento **float slot 7**. Não existe branch dentro de 150–172 nem ingresso externo nesse intervalo. Isto não prova que o evento concede/cancela cura, o valor efetivo de HP, ou que o objeto 4 seja o caster real.

**Boundary de engenharia:** não promover caster/owner/vítima, valor final de dano, duração/amplificador de Wither, impulso, healing, procs únicos ou hooks per-player sem dataflow dos campos e teste provider-loaded. A prova é de **fluxo de controle compilado**, não de resultado prático em Survival/PvP. Nenhuma segunda pipeline de dano/recursos, Stage ou adaptador. Status de perks mutadoras: **⛔ FAIL_CLOSED**. [Scanner](../../../docs/qa/somake_109_bud_impact_damage_gates.py) · [Testes](../../../docs/qa/somake_109_bud_impact_damage_gates_test.py) · [Ficha](registry-1.0.9/funeral-bloom.md).

## Dataflow owner/Wither/empurrão/cura na bud (20/10/2026; PR #852)

**Prova de JAR exato:** Somake 1.0.9 File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [GitHub Actions Java 21 #39533416067](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39533416067), `SUCCESS`, **14 testes originais sintéticos** e gate rígido `PASS_SHA_EXACT_OWNER_WITHER_COUNTER_IMPULSE_AND_HEAL`.

1. **Owner condicional:** `FuneralBloomBudEntity.getOwner():Entity` é guardado no slot JVM 3; `instanceof LivingEntity`/cast constroem o slot JVM 4, com fallback `null` para owner de outro tipo. Não certificar que owner seja um jogador ou o conjurador efetivo.
2. **Pré-Wither + dano:** `slot8.hasEffect(WITHER)` retorna booleano salvo no slot 14 **antes** de `DamageSources.applyDamage`. Somente se esse dano retorna `true` ocorre o bloco de efeitos e o caminho posterior `iload14/ifeq`, que incrementa o inteiro slot 6 em uma unidade quando o status era preexistente. Slot 6 inicia em zero no começo de `impact`.
3. **Wither novo:** a bud fornece os fields `witherDuration:I` e `witherAmplifier:I` ao construtor de `MobEffectInstance`, seguido de `false,true,true`. Duração/nível concretos, aceitação de status, mutation seam e condições de reload não foram inferidos.
4. **Push:** `slot8.push(0.0d,0.34d,0.0d)` e `slot8.hurtMarked=true`. Esse é um vetor passado ao método, não deslocamento efetivamente observado.
5. **Cura condicional e clamp:** a expressão JVM `Math.min(3.75f,1.25f*(float)slot6)` via `fmul`, `min(FF)F` e `fstore slot7` é o argumento de `slot4.heal(F)`. Os guards `slot4!=null` e `slot6>0` condicionam a sequência `SpellHealEvent/post` e o heal. O evento não fornece o argumento do `heal`; o fluxo lê o local float 7. Isso não certifica cancelamento efetivo de evento nem HP restaurado.

**Delimitação de perícia:** o recorte auditado contém 279 instruções e os gates pré-existentes de AABB da bud (#850), return de dano/Wither/empurrão e evento de cura (#851). O novo probe deriva apenas símbolos/categorias e dataflow tipo-local de regiões finitas, sem exportar bytecode, código ou JAR do provider. Não promover player/caster, PvP/claims, duplicação entre múltiplas buds, compatibilidade do modpack, hook ou perk. **⛔ FAIL_CLOSED.** Stage 06.05 🟡; Stage 09 físico pendente. [Fonte do gate](../../../docs/qa/somake_109_bud_operand_provenance.py) · [Ficha](registry-1.0.9/funeral-bloom.md).

## Controller → Bud: clamps de Wither e transferência de fields (20/10/2026; PR #853)

**Release:** Somake 1.0.9, File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [prova física #39536052412](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39536052412), `SUCCESS`, **14 regressões originais**. O gate `certify_exact_wither_handoff_109` depende previamente dos gates de operands de `impact` e de clipping/iteração de `launchWave`.

**Dois construtores do JAR:** `(EntityType,Level)` com **17 instruções**, valor inicial `witherDuration=80`, e `(Level,Controller,LivingEntity,Vec3,int,float,int,int)` com **41 instruções**. Este segundo usa `impactDamage=(float slot 6)`, `witherDuration=Math.max(30,(int slot 7))` e `witherAmplifier=Math.max(0,(int slot 8))`. O scanner exige contagens, constantes, tipos, operações de `Math.max(II)I`, ordem das escritas e descriptors; mudanças rejeitam a certificação.

**Cadeia de invocação compilada:** no índice estrutural 93 de `launchWave(ServerLevel)`, `new FuneralBloomBudEntity` recebe o `ServerLevel`, a controller, os objetos locais JVM 7/8, `Mth.ceil(fload local9)` e, por fim, `getfield impactDamage:F`, `getfield witherDuration:I`, `getfield witherAmplifier:I`, em ordem. Esses argumentos alimentam diretamente os slots correspondentes no construtor da bud. Depois, `impact` lê os dois fields Wither para `MobEffectInstance`; essa leitura foi validada na PR #852. Não inferir que os fields ficam imutáveis entre construtor e impacto.

**Limites:** sem prova da **atribuição inicial na controller**, da configuração do cast ou da validade de argumentos sob condições PvP/Survival. `activeTargetIds` pertence ao escopo observável da controller e não certifica dedup entre instâncias ou sucesso de spawn. Sem hooks mutadores por jogador e sem efeitos duplicados inventados. ⛔ `FAIL_CLOSED`. Stage 06.05 🟡, Stage 09 físico PENDING. [Verificador](../../../docs/qa/somake_109_bud_wither_construction.py) · [Ficha](registry-1.0.9/funeral-bloom.md).

## Source-pinning do construtor da controller, NBT e membership de UUID (21/10/2026; PR #854)

**Arquivo oficial:** Somake Spells 1.0.9, File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [auditoria Java21 #39538804021](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39538804021), `SUCCESS`, 12 regressões sintéticas e `certify_exact_controller_lifecycle_109`.

**Construtor básico da `FuneralBloomControllerEntity`:** inicializa `witherDuration=80`, `maxTargets=8` e cria o conjunto `this.activeTargetIds`. **Construtor especializado:** `maxTargets=Math.max(1,slot7)`, `impactDamage=(float)slot8`, `witherDuration=Math.max(30,slot9)`, `witherAmplifier=Math.max(0,slot10)`. No JAR exato, os três campos de efeito são gravados via `addAdditionalSaveData → putFloat/putInt` e restaurados via `readAdditionalSaveData → getFloat/getInt`, com clamps de duração e amplificador reaplicados durante a leitura. A PR #853 já provou os argumentos da controller transferidos ao construtor da bud.

**Filtro e poda intra-controller:** o corpo `lambda$launchWave$0` consulta `isValidTarget(arg1,arg2)`, depois `arg2.getUUID()` e `this.activeTargetIds.contains(UUID)`; uma UUID já presente torna o candidato inelegível nesse predicado. Na mesma instância, `pruneTargets` constrói uma coleção de UUIDs obtidos por `getTargetUuid()` e chama `this.activeTargetIds.retainAll(coleção)`. O caminho normal de `launchWave` também chama `activeTargetIds.add(candidateUUID)` depois de tentar `ServerLevel.addFreshEntity` e descarta os dois retornos, como certificado na PR #849.

**Limitações:** o inventário de campos NBT certificados cobre **impactDamage, witherDuration, witherAmplifier**, não uma serialização comprovada de `activeTargetIds`. Regras de dedup entre controllers, reconstrução após reload, sucesso de spawn, execução da poda e ownership efetivo precisam de testes adicionais. `FAIL_CLOSED` para perks mutadoras, nenhuma nova fonte de dano, mana ou Mastery. Stage 06.05 🟡; Stage 09 QA físico ainda pendente. [Verificador](../../../docs/qa/somake_109_controller_fields.py) · [Ficha](registry-1.0.9/funeral-bloom.md).

## Spell `onCast` → controller: fórmulas nativas SHA-exatas (21/10/2026; PR #855)

**Publisher:** Somake Spells 1.0.9, CurseForge File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. Classe física `com.somake.somakespells.spells.blood.FuneralBloomSpell`. [Auditoria Java21 #39541775847](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39541775847) concluiu com **14 testes** e certificou 81 instruções no método `onCast`, oito getters na sequência que alimenta o construtor de `FuneralBloomControllerEntity` no índice 51, e cast level/caster como slots JVM 2 e 3 nos getters que os consomem.

| Getter | Expressão ou decisão JVM de retorno |
|---|---|
| `getRadius(I,LivingEntity):F` | `Mth.clamp(9.5f+level*0.82f+Math.max(0f,(caster!=null ? getSchoolType().getPowerFor(caster) : 1f)-1f)*0.65f,10f,15f)`, aritmética `float` conforme JVM |
| `getDuration(I):I` | `240+20*(Mth.clamp(level,1,5)-1)` |
| `getWaveInterval(I):I` | `18-Mth.clamp(level,1,5)` |
| `getTelegraphTicks(I):I` | `Math.max(9,13-level/2)` com divisão inteira |
| `getMaxTargets(I):I` | `4+Mth.clamp(level,1,5)` |
| `getImpactDamage(I,LivingEntity):F` | `1.5f+0.75f*getSpellPower(level,caster)` |
| `getWitherDuration(I):I` | `60+12*Mth.clamp(level,1,5)` |
| `getWitherAmplifier(I):I` | `level>=5 ? 1 : 0` |

Os saltos de `getRadius` quando caster é nulo e de `getWitherAmplifier` foram resolvidos pelo CFG compilado. Os getters de raio e telegraph **não** limitam o próprio argumento level a 1–5, diferentemente das expressões que invocam `Mth.clamp`. O `onCast` não contém branch explícito no método auditado; a semântica do `invokedynamic Predicate` do raycast de **32.0d** permanece **não certificada**. Após `groundPosition`, a controller recebe `setPos` e uma tentativa de `addFreshEntity` cujo retorno é descartado.

**Handoff encadeado já comprovado:** `FuneralBloomSpell getters → FuneralBloomControllerEntity constructor (maxTargets>=1, witherDuration>=30, witherAmplifier>=0) → launchWave: FuneralBloomBudEntity constructor (witherDuration>=30, amplifier>=0) → bud.impact: consulta AABB própria e efeitos condicionais`. Esta cadeia une os argumentos até as chamadas provider-native, mas não prova dano efetivo, número de entidades persistidas, evento de cura cancelável, dedup inter-controller, hook mutador ou QA real. Black Arcana preserva seu runtime; RPG Skill Tree fica apenas na progressão contratual; Somake/Iron's mantêm casting e efeitos. **⛔ FAIL_CLOSED**. Stage 06.05 🟡, Stage09 físico PENDING. [Verificador](../../../docs/qa/somake_109_funeral_spell_handoff.py) · [Ficha](registry-1.0.9/funeral-bloom.md).

## Raycast: bootstrap LambdaMetafactory → `false` constante (21/10/2026; PR #856)

**Proveniência:** Somake 1.0.9, CurseForge File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. [GitHub Actions Java21 #39543931954](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39543931954), **SUCCESS, 15 testes**; gate `certify_exact_raycast_lambda_link_109` e marker `PASS_SHA_EXACT_ONCAST_FALSE_PREDICATE_LINKED`.

O `onCast` de `com.somake.somakespells.spells.blood.FuneralBloomSpell` possui fábrica `invokedynamic #0:test:()Predicate` no índice de instrução 13 e passagem para `raycastForEntity` no índice 14. A tabela `BootstrapMethods` **0** contém método de fábrica `LambdaMetafactory.metafactory` e `REF_invokeStatic` para `FuneralBloomSpell.lambda$onCast$0:(Entity)Z`. O método `lambda$onCast$0` deste JAR contém exatamente **duas** instruções — `iconst_0` e `ireturn`. Logo, **o Predicate compilado fornecido ao raycast devolve false em qualquer chamada**, sem dispatch a outro método de validação de entidade. Qualquer mudança na tabela de bootstrap, assinatura, corpo do método ou opcode invalida o gate e permanece fail-closed.

**Escopos não equivalentes:** (a) predicado da localização inicial de `onCast` (sempre false), (b) `launchWave` com `isValidTarget` e `activeTargetIds.contains(UUID)` na controller, (c) AABB e booleano de dano em `bud.impact`. Esta prova **não** verifica como a biblioteca host Iron's processa um predicado rejeitante, se a consulta de blocos prevalece, a posição final, ou se a tentativa de `addFreshEntity` resulta em spawn. Não representa permissão para adaptar `Predicate` ou injetar perks per-player. Black Arcana mantém runtime próprio e RPG Skill Tree exclusivamente progressão sob contrato; Somake/Iron's são authority do casting externo. Stage 06.05 🟡; Stage 09 físico PENDING. [Verificador](../../../../docs/qa/somake_109_funeral_raycast_predicate.py) · [Ficha individual](registry-1.0.9/funeral-bloom.md).
