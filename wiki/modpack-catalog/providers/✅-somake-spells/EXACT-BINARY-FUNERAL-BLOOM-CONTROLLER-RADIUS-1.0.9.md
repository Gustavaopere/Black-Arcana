# Somake Spells 1.0.9 — Funeral Bloom: ponte de argumento float da controller

**Estado vigente (PR #839):** ✅ cadeia estática `onCast.getRadius` → primeiro float do construtor → setter clamp 6–18 → `DATA_RADIUS` → getter da controller comprovada; ⚠️ operandos de AABB, alvos e gameplay não demonstrados; ⛔ nenhuma perk mutadora homologada. Os resultados históricos abaixo preservam seu escopo temporal.

## Artefato e método

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, `somakespells-1.0.9-1.21.1.jar`, CurseForge File 8867079; mod ID `somakespells`; SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. Java21 e NeoForge para Minecraft 1.21.1.
- Scanner clean-room [constructor/getter](../../../../docs/qa/somake_109_controller_radius_bridge.py), [fixtures](../../../../docs/qa/somake_109_controller_radius_bridge_test.py) e [workflow SHA-exato](../../../../.github/workflows/somake-109-controller-radius-bridge.yml). Nunca exporta JAR, classfile, sequência de bytecode, implementação de terceiros ou assets.

## Contratos a validar

- `FuneralBloomControllerEntity.<init>(Level,LivingEntity,float,int,int,int,int,float,int,int):void`. A assinatura compilada contém dois argumentos `float`: posições ordinais 3 e 8, slots de variável local JVM 3 e 8 (construtor de instância). São duas entradas diferentes; não associá-las a raio ou dano por nome antes da prova.
- `getRadius():float` somente é declarado retorno direto de campo quando seu **corpo inteiro** é exatamente `aload_0 → getfield` do campo `float` → `freturn`.
- Um parâmetro do construtor só é vinculado ao campo se existir **uma única** atribuição direta adjacente `aload_0 → fload(slot) → putfield` para o mesmo campo. Qualquer operação intermediária, atribuição duplicada ou ausência dessa sequência produz `NOT_PROVED`, sem estimar origem.

## Limites e próximo passo

Mesmo se o elo interno for certificado, o scanner **não analisa** os argumentos de `invokespecial` no método `FuneralBloomSpell.onCast`, nem as expressões passadas aos três parâmetros `double` de `AABB.inflate` em `controller.launchWave` ou `bud.impact`. O vínculo entre esses métodos segue ⚠️ condicionado. Uma atribuição local também não é um setter público de perk.

**Autoridade:** Black Arcana controla apenas seu runtime; Somake executa a magia; Iron's conserva recursos e casting provider-native; RPG Skill Tree fornece progressão por contratos reais. Zero adapters novos; ⛔ `FAIL_CLOSED` para mudança per-player de área, targeting e impacto. Stage 06.05 🟡 e Stage 09 condicionado conforme D035. Contagem Somake 83/83 identidades sem alteração.

## Resultado físico da primeira auditoria (19/10/2026)

O [workflow #39286470816](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39286470816) concluiu com **`SUCCESS`**, após **13 testes** sintéticos/compilados em Java 21, incluindo gate do SHA-1 exato do Somake 1.0.9. A saída literal de status foi **`PASS_EXACT_SHA_OBSERVATIONAL_ONLY_BRIDGE_NOT_PROVED`**.

- `getRadius():float`: **`NOT_PROVED`**, razão `getter_is_not_exact_three_opcode_direct_field_read`.
- `constructor_to_getter`: **`NOT_PROVED`**, razão `no_certified_getter_field`.
- Os argumentos `float` do construtor permanecem distintos nos slots JVM **3** e **8**, sem atribuição comprovada de qualquer deles ao getter.
- Essa é uma **rejeição do padrão específico de leitura direta**, não demonstra que o getter jamais utilize qualquer campo do construtor. Não atribuir semântica ao slot pelo nome do parâmetro ou proximidade de callsites.

**Próximo recorte:** o verificador agora produz apenas número de instruções, campos `float` diretamente referenciados, chamadas simbólicas, quantidade de operações aritméticas/conversões e branches do getter, para orientar uma auditoria de fluxo completo posterior. Esse resumo estrutural ainda **não** constitui uma fórmula ou vínculo causal. Aguardam-se testes do HEAD que contém esse complemento.

## Extensão física: dados sincronizados e descoberta dos métodos de escrita

Uma segunda execução no JAR SHA-exato, [workflow #39288405552](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39288405552), `SUCCESS`, 16 testes Java21, demonstrou integralmente o caminho de sete instruções do getter `FuneralBloomControllerEntity.getRadius():float`: leitura do campo herdado `entityData`, consulta a **`SynchedEntityData.get(DATA_RADIUS)`**, conversão segura de `java.lang.Float` com `Float.floatValue()` e retorno float. O `EntityDataAccessor` estático `DATA_RADIUS` é da própria controller. Não há aritmética ou desvios nesse getter. **Status `PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER`.**

A varredura ampliada de **30 métodos** no [workflow #39289130886](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39289130886), `SUCCESS`, localizou:

| Método JVM | Referências encontradas | Natureza da prova |
|---|---|---|
| `defineSynchedData(SynchedEntityData.Builder)` | `DATA_RADIUS` e `Float.valueOf` | Inicialização relevante à configuração do accessor, mas valor/default efetivo não inferido |
| `getRadius():float` | `DATA_RADIUS`, `SynchedEntityData.get`, `Float.floatValue` | ✅ fluxo completo do getter certificado |
| `setRadius(float):void` | `DATA_RADIUS`, `Float.valueOf`, `SynchedEntityData.set`, `fload` slot 1 | ⚠️ referências co-presentes; não há prova completa da pilha do setter |
| `setDuration(int)` e `setWaveInterval(int)` | chamadas próprias a `SynchedEntityData.set` | Referências a outros dados sincronizados; não são writes de raio por evidência atual |

A tentativa subsequente de exigir um setter **exatamente** de sete instruções retornou **`NOT_PROVED / setter_not_exact_seven_opcode_float_write`**; o construtor, por sua vez, não contém acesso direto ao accessor no padrão `getstatic DATA_RADIUS` reconhecido. Esses resultados excluem apenas os dois padrões auditados, e não a possibilidade de uma chamada intermediária como `setRadius`.

**Pendências objetivas:** interpretar o fluxo inteiro de `setRadius(float)` e rastrear a eventual chamada do construtor com o slot `float` correto; examinar o argumento efetivamente enviado por `FuneralBloomSpell.onCast`; distinguir uso do getter da controller nos operandos de `AABB.inflate` da wave e no impacto independente da bud. Não atribuir raio, hitbox ou tamanho de alvo por semelhança de nome.

**Boundary:** ⛔ `FAIL_CLOSED` para mutação de parâmetros native-Somake e para atribuir contratos de perks do RPG Skill Tree. As conclusões acima são binárias e estáticas, não QA provider-loaded/Survival/multiplayer nem prova de alteração do runtime Black Arcana.

## Prova posterior: setter sincronizado com clamp e vínculo local do construtor — 19/10/2026 (PR #838)

A pendência de **dataflow local construtor → setter → `DATA_RADIUS` → getter** registrada acima foi encerrada por um verificador de **corpo integral, dez opcodes** após a auditoria estrutural de `setRadius(float)`. Evidência física no JAR oficial 1.0.9 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`: [GitHub Actions #39292948277](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39292948277), `SUCCESS`, 31 testes Java21 no HEAD `db24ea457eaa24c977d990ddf199ff4bc968c60c`. Testes de regressão específicos adicionais na PR #838 devem ser aferidos no HEAD subsequente, não inferidos deste run.

| Elo / parâmetro | Resultado estritamente certificado |
|---|---|
| Construtor `(Level,LivingEntity,float,int,int,int,int,float,int,int)` | ✅ chamada direta `this.setRadius(float)` com o primeiro float, **slot JVM 3 / argumento ordinal 3**. Segundo float permanece no **slot 8**, sem ser associado a raio neste elo |
| `setRadius(float)` → clamp | ✅ corpo integral com 10 instruções, `fload_1`, limites float **6.0f e 18.0f**, `Mth.clamp:(FFF)F` |
| Clamp → sincronização | ✅ `Float.valueOf:(F)Ljava/lang/Float;` seguido de `SynchedEntityData.set(DATA_RADIUS,...)`, com accessor do mesmo owner |
| `getRadius():float` | ✅ leitura completa de `SynchedEntityData.get(DATA_RADIUS)` e `Float.floatValue()` (já comprovada na PR #837) |
| `FuneralBloomSpell.onCast` → valor de cada float no construtor | ⚠️ **não examinado neste gate**: chamada presente, sem atribuição certificada das expressões/argumentos |
| `controller.launchWave` / `bud.impact` → argumentos de `AABB.inflate` | ⚠️ **não demonstrado** que ambas as áreas usem esse raio, nem a unidade ou efeito por alvo |
| Hook per-player/perk | ⛔ **FAIL_CLOSED**: método interno de entidade não equivale a API oficial mutadora |

A expressão **certificada apenas no escopo interno do setter** é `DATA_RADIUS := Float.valueOf(Mth.clamp(setRadius_argument_float, 6.0f, 18.0f))`. A trilha do primeiro float do construtor até a leitura posterior da controller está certificada, mas isso **não** identifica a expressão que a spell usou para construí-la. Tampouco autoriza prometer que 18 seja o raio máximo de efeito no mundo: seleção e impacto secundário têm consumidores próprios.

O antigo `NOT_PROVED / setter_not_exact_seven_opcode_float_write` permanece válido apenas para o **padrão de sete opcodes sem clamp**, que a implementação real não segue. Não usá-lo para negar a prova posterior de dez opcodes. O `NOT_PROVED` da escrita **direta pelo construtor em `SynchedEntityData.set`** também continua correto, porque a escrita agora é comprovadamente **indireta pelo setter**.

**Contagens e autoridade invariantes:** 83/83 identidades Somake; 5/83 fichas com entidade downstream na campanha; +0 novas identidades e +0 adapters homologados. Somake controla magia/efeito, Iron's hospeda casting/custos e RPG Skill Tree controla perks/Mastery via contratos reais; Black Arcana não duplica esses runtimes. Stage 06.05 🟡, Stage 09 de QA físico pendente.

## Continuação: origem do primeiro float no `onCast` — 19/10/2026 (PR #839)

**Nova prova física exata:** [Java 21 #39296264174](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39296264174), `SUCCESS`, **45 testes** em `Somake Spells 1.0.9`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` igual à modlist sibling. Um scanner de descritores e pilha JVM analisou a **janela local de 31 instruções** entre a alocação de `FuneralBloomControllerEntity` e a única invocação exata do seu construtor. Rejeita branches, `invokedynamic`, opcodes/tipos não modelados, deslocamento de origem, receptores divergentes e alterações de assinatura.

- ✅ `FuneralBloomSpell.getRadius(int,LivingEntity):float` fornece **diretamente o primeiro argumento `float` do construtor**. Resultado do scanner: `PROVED_ONCAST_GET_RADIUS_TO_FIRST_CTOR_FLOAT` / `exact_getRadius_call_stack_argument`, argumento ordinal **3**.
- ✅ Provas independentes anteriores: argumento do construtor (slot local JVM **3**) → `setRadius(float)` → `Mth.clamp(float,6.0f,18.0f)` → `SynchedEntityData.set(DATA_RADIUS)` → `getRadius():float`. A expressão de retorno de `FuneralBloomSpell.getRadius` é documentada separadamente com seu próprio clamp **10.0f–15.0f** em [dossiê tipado](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md).
- ✅ O **segundo argumento `float`** do construtor recebe um retorno classificado como `other_method` na janela; **não se certificou** qual método ou semântica para essa posição.
- ⚠️ As fontes dos argumentos `int` e `LivingEntity` da chamada `getRadius` ainda não foram certificadas até os parâmetros/estado reais de `onCast`; tampouco foram provadas unidades e efeitos em jogo.
- ⚠️ O getter da controller é referenciado por `launchWave` e o método também possui `AABB.inflate`, mas os três operandos `double` não foram associados por dataflow à leitura do accessor. O volume independente de `FuneralBloomBudEntity.impact` segue em aberto.
- ⛔ **Sem hook/API pública mutadora por jogador**; a existência de `setRadius(float)` interno e a fórmula de raio não autorizam alterar, recriar, cancelar ou duplicar um cast Somake, custos Iron's nem perks/Mastery RPG. Estado `FAIL_CLOSED`.

Esta adição **supera apenas a pendência histórica de proveniência do primeiro float do callsite**, mantendo as incertezas sobre AABBs, target selection, configuração efetiva, classloading, Survival, PvP, multiplayer, cliente e integração. É uma prova estática, não QA físico. Identidades Somake **83/83**, fichas com downstream nesta campanha **5/83**, adapters homologados **0**; Stage 06.05 🟡, Stage 09 PENDING.

## Consumidor direto: `launchWave.AABB.inflate` — 19/10/2026, PR #840

Uma auditoria posterior do exato JAR Somake 1.0.9, [Java21 #39304248399](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39304248399), **SUCCESS / 21 testes**, fecha a proveniência **local dos três argumentos `double`** de `AABB.inflate` em `FuneralBloomControllerEntity.launchWave(ServerLevel)`: **X = `(double)getRadius()`; Y = `10.5d`; Z = `(double)getRadius()`**. O método tem 196 instruções, com três chamadas totais a `getRadius`, mas somente duas anteriores à expansão; a terceira não foi atribuída a essa chamada `inflate`.

**Cadeia agora certificada até os operandos dessa expansão:** `FuneralBloomSpell.getRadius(int,LivingEntity)` → argumento `float` ordinal 3 da controller → `setRadius(float)` clamp `6–18` → `DATA_RADIUS` → `controller.getRadius()` → argumentos X/Z da AABB. A expressão upstream do getter do spell, clamp `10–15` para entradas finitas, permanece prova separada.

**Não encerrado:** origem/identidade efetiva de todos os argumentos do getter de spell, objeto AABB receptor, propagação do **retorno** de `inflate` à lista de entidades, filtros e quantidade de alvos, dano/cura, `FuneralBloomBudEntity.impact` e hook público de mutação de área por jogador. Essa certificação **não autoriza** declarar que `R` seja raio de dano no mundo ou altura real de uma perk; permanece ⛔ `FAIL_CLOSED`. [Dossiê do consumidor](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md).

## Extensão do consumidor até `getEntitiesOfClass` — 20/10/2026, PR #841

A [auditoria SHA-exata Java21 #39466062186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39466062186) concluiu com `SUCCESS` / **29 testes**. A caixa que `launchWave` constrói por `inflate((double)getRadius(),10.5d,(double)getRadius())` é armazenada e recuperada do **slot JVM 3** e fornecida diretamente como argumento `AABB` à consulta `ServerLevel.getEntitiesOfClass(Class,AABB,Predicate)` de `LivingEntity`. A janela contém nove instruções intermediárias; o `Predicate` vem de `invokedynamic` capturando controller e `LivingEntity`, sem prova da lógica de teste.

Esta atualização **substitui apenas a pendência anterior de transporte do retorno da expansão para a consulta**, não certifica a geometria da AABB base, execução dos filtros, aceitação/quantidade de alvos, propagação até buds, dano/cura, `bud.impact` ou hook mutador. O setter `setRadius` é interno ao provider, não API per-player. `FAIL_CLOSED` mantido. [Dossiê de consumidores](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md).
