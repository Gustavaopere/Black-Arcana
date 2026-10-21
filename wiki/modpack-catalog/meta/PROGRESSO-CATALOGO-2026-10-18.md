# Black Arcana — acompanhamento do catálogo de magias




## Somake Blood Cut — Iron's 3.16.3 virtual lifesteal (PR #863, 21/10/2026)

[Java 21 #39613550972](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39613550972) SUCCESS, **97 testes sintéticos**, SHA-1 Somake `171841ac9f802be9309ecc166c1d972ac6d404c0` e SHA-256 Iron's API `69e81104a9fd31a402d9c89ab09c2a6b2fd6d2ab98db5a37bb159517363ee9ad` conferidos. O host `AbstractSpell.getDamageSource(e)` envia `(e,e)` à sobrecarga virtual de dois argumentos; a implementação `BloodCutSpell.getDamageSource(e,e)` executa `super` e `SpellDamageSource.setLifestealPercent(0.15f)`. O caminho compilado do hit secundário está, portanto, ligado ao setter nominal; **cure/heal efetivo, capped settlement, caster/perk hook e QA provider-loaded seguem pendentes**. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-BLOOD-CUT-IRONS-VIRTUAL-LIFESTEAL-1.0.9.md).

**Barras de cobertura preservadas:** global **—%** (denominador ainda aberto, piso semântico ≥1.856); Somake **83/83 IDs = 100%** de registry, **8/83 = 9,64%** do recorte estático de métodos, **5/83 = 6,02%** no recorte downstream aprofundado anterior. +0 identidades, +0 adapters, +0 hooks mutadores. Stage 06.05 🟡; Stage 09 físico PENDING.

## Somake — Blood Cut 1.0.9: argumentos do dano secundário (PR #862, 21/10/2026)

[GitHub Actions #39604864087](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39604864087) **SUCCESS**, SHA-1 exato `171841ac9f802be9309ecc166c1d972ac6d404c0`, **86 testes sintéticos**: `DamageSources.applyDamage` recebe `event.getEntity()` (target), `local_3` (float calculado) e `BloodCutSpell.getDamageSource(local_1)` (fonte), descartando o resultado booleano. O setter de lifesteal `0.15f` pertence à **sobrecarga de dois argumentos**, ao passo que o handler invoca a **sobrecarga de um argumento**: vínculo não demonstrado. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-BLOOD-CUT-APPLY-DAMAGE-1.0.9.md).

**Barras estáveis:** global **—%** (piso semântico ≥1.856; universo aberto), Somake registry **83/83 = 100%**, método estático **8/83 = 9,64%**, recorte downstream aprofundado anterior **5/83 = 6,02%**; campanhas independentes de providers exatos **35/39 = 89,74%** no checkpoint próprio. **+0 magias, +0 adapters, +0 hooks de perk**; Stage 06.05 🟡, Stage 09 físico PENDING.

## Somake Blood Cut — vínculo causal nativo do evento de dano (21/10/2026; PR #861)

[Java 21 #39599959888](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39599959888): SHA-1 físico/publisher `171841ac9f802be9309ecc166c1d972ac6d404c0`, **73 testes sintéticos**. O handler `onLivingDamage(LivingDamageEvent.Post)` obteve `LivingEntity` da entidade da fonte de dano, consultou nela `BLOOD_CUT`, leu amplificador e aplicou a fórmula intermediária `getNewDamage × getDamageModifier(amplifier, sourceEntity)` em float. Há `return` nativo se `event.getSource() instanceof SpellDamageSource`, mas isso **não** elimina todas as rotas de proc recursivo. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-BLOOD-CUT-CAUSAL-EVENT-1.0.9.md). Dano final, receiver do applyDamage, lifesteal realmente curado e QA no modpack PENDING.

**Barras conservadoras:** global **—%** (piso semântico ≥1.856, denominador aberto); Somake registry **83/83 = 100%**, recorte método estático **8/83 = 9,64%**, recorte downstream aprofundado anterior **5/83 = 6,02%**; campanha de providers exatos **35/39 = 89,74%** no checkpoint próprio. **+0 magias, +0 adapters, +0 hooks por jogador**; Stage 06.05 🟡 / Stage 09 físico pendente.

## Somake 1.0.9 — Blood Cut: parâmetro literal de lifesteal (21/10/2026, PR #860)

[GitHub Actions #39594615862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39594615862) **SUCCESS**, **51 testes sintéticos** e SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`: comprovado `BloodCutSpell.getDamageSource` → fonte-base Iron's → `ldc 0.15f` → `SpellDamageSource.setLifestealPercent(float)` → `areturn`. O float **é argumento compilado do setter**; não é evidência de healing efetivo em jogo. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-BLOOD-CUT-LIFESTEAL-1.0.9.md).

**Barras sem promoção:** global **—%** (piso **≥1.856**, universo de conteúdo ainda aberto), Somake registry **83/83 = 100%**, recorte método estático **8/83 = 9,64%**; downstream aprofundado anterior **5/83 = 6,02%**; providers físicos exatos **35/39 = 89,74%** no checkpoint separado. **+0** identidades, **+0** adapters, **+0** hooks mutadores. Stage 06.05 🟡; Stage 09 físico pendente.

## Somake Blood Cut — grafo normal e retorno float exatos (21/10/2026, PR #859)

Evidência física [GitHub Actions #39553030589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39553030589): SHA-1 Somake 1.0.9 `171841ac9f802be9309ecc166c1d972ac6d404c0`, **41 testes sintéticos**, grafo normal de **2 caminhos sintáticos que alcançam applyDamage / 3 que não alcançam** no handler de 103 instruções e cinco desvios; `getDamageModifier(int a,LivingEntity e)` retorna `((float)(a+1) * (e != null ? getEntityPowerMultiplier(e) : 1.0f)) * 0.1f`. São dados de classfile, não dano final ou contagem de eventos de gameplay. [Dossiê técnico](../providers/✅-somake-spells/EXACT-BINARY-BLOOD-CUT-CFG-MODIFIER-1.0.9.md). Ainda pendentes: vínculo dos argumentos do evento, todos os predicados, recursão, host config e QA físico. Nenhuma perk mutadora homologada.

**Barra global de completude técnica:** —% (piso semântico registrado **≥1.856**, denominador final aberto). **Barra Somake**: **83/83 IDs = 100%** de registry, **8/83 = 9,64%** de fichas no recorte estático de métodos, **5/83 = 6,02%** no recorte aprofundado anterior (sem nova raiz nem promoção automática). Campanha independente de providers exatos: **35/39 = 89,74%** no checkpoint. **+0 magias e +0 adapters**. Stage 06.05 🟡, Stage 09 QA físico pendente.

## Somake Blood Cut — anotação de evento e risco de segundo dano (21/10/2026; PR #858)

[Java21 #39549751471](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39549751471) **SUCCESS** no Somake 1.0.9 físico/publisher SHA-1 171841ac9f802be9309ecc166c1d972ac6d404c0, **20 testes sintéticos**: classe BloodCutEffect com EventBusSubscriber e método onLivingDamage com SubscribeEvent em RuntimeVisibleAnnotations; **103 instruções/5 desvios** no handler Post e **19 instruções/2 desvios** no modificador. Há referências a getNewDamage e DamageSources.applyDamage no mesmo método, sem prova de predicados, despacho runtime, taxa de dano/recursão nem hooks mutadores. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-BLOOD-CUT-EVENT-1.0.9.md) e [ficha individual](../providers/✅-somake-spells/registry-1.0.9/blood-cut.md).

**Barras conservadoras:** global **—%** (piso **≥1.856** raízes semânticas; denominador aberto); Somake **83/83 = 100% IDs**, recorte de método estático **8/83 = 9,64%**, downstream aprofundado **5/83 = 6,02%**; campanha fixa dos providers exatos **35/39 = 89,74%** no último checkpoint correspondente. **+0 magias, +0 adapters, nenhum hook externo de perk aprovado**; Stage 06.05 🟡 / Stage 09 físico PENDING.

## Somake Blood Cut — evidência de dano secundário e scaling incompleto (21/10/2026; PR #857)

[Java21 #39546058075](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39546058075) passou **16 testes sintéticos** com o JAR Somake 1.0.9 SHA-1 exato `171841ac9f802be9309ecc166c1d972ac6d404c0`. Foram provadas as FQCN `BloodCutSpell` (7 métodos) e `BloodCutEffect` (2 métodos), `CastType.INSTANT`, `onCast` → `ModMobEffects.BLOOD_CUT` / `LivingEntity.addEffect`, `getDamageSource` → `setLifestealPercent`, e `onLivingDamage(LivingDamageEvent.Post)` → referências a `getNewDamage`, `getDamageModifier` e `DamageSources.applyDamage`. O handler possui **cinco branches** e o getter de modificador possui **dois**, não reconciliados causalmente; wiring do evento, dano real, caps, alvo, tempo e qualquer hook de perk permanecem ⚠️/⛔. [Ficha](../providers/✅-somake-spells/registry-1.0.9/blood-cut.md) e [dossiê](../providers/✅-somake-spells/registry-1.0.9/blood-cut-technical-gate.md).

**Barras:** universo global **—%** (piso conservador **≥1.856**, denominador aberto); Somake **83/83 IDs registrados = 100%**; agora **8/83 = 9,64%** com inspeção de método estático no recorte (7 anteriores + Blood Cut), enquanto o recorte aprofundado downstream anterior mantém **5/83 = 6,02%** sem promoção por esta prova parcial. Campanha de providers físicos exatos **35/39 = 89,74%** em checkpoint próprio. **+0 magias, +0 adapters**, mutações externas ⛔. Stage 06.05 🟡 e Stage 09 QA físico pendente.

## Somake 1.0.9 — `onCast` raycast Predicate e linkage JVM exato (21/10/2026, PR #856)

**Barras inalteradas:** global **—%** (piso conservador **≥1.856** objetos semânticos, universo universal aberto), **Somake IDs 83/83 = 100%**, recorte de auditorias downstream **5/83 = 6,02%**, campanha física registrada de providers **35/39 = 89,74%** no respectivo checkpoint. +0 magias, +0 adapters; sem hooks de perks mutadoras homologados.

O [workflow Java 21 #39543931954](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39543931954) confrontou Somake File 8867079 ao SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` e passou **15 testes**. O novo gate prova que `FuneralBloomSpell.onCast` constrói `Predicate` por `invokedynamic` índice 13, cujo `BootstrapMethods[0]` via `LambdaMetafactory` referencia `lambda$onCast$0(Entity):Z`; esta lambda é **`iconst_0; ireturn`**, portanto sempre `false`. A invocação de `raycastForEntity` ocorre em seguida. Isso não demonstra o algoritmo de raycast do host, fallback de blocos, resultado de posição, criação efetiva da controller, targeting da wave ou gameplay. As condições de `activeTargetIds` permanecem por controller, sem dedup entre instâncias. Perks mutadoras **⛔ FAIL_CLOSED**; Stage 06.05 🟡 e Stage 09 QA físico PENDING. [Ficha](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake — `FuneralBloomSpell.onCast` e oito getters nativos (21/10/2026; PR #855)

**Barra global:** **—%** (denominador universal ainda aberto; piso documentado **≥1.856** objetos semânticos). **Barra Somake:** **83/83 = 100%** para identidades registradas; **5/83 = 6,02%** para aprofundamento downstream por ficha; campanha fixa anterior de providers com release exato **35/39 = 89,74%** no checkpoint próprio. Esta auditoria adiciona **+0 magias, +0 adapters**, hooks mutadores homologados **0**, taxa de perks sem denominador.

O [workflow Java21 #39541775847](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39541775847) verificou o JAR oficial Somake 1.0.9 File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, com **14 testes**, e ligou `FuneralBloomSpell.onCast(Level,int,LivingEntity,CastSource,MagicData)` à construção nativa de `FuneralBloomControllerEntity` por oito getters: raio, duração, intervalo de waves, telegraph, maxTargets, dano de impacto, Wither duração e Wither amplificador. Certificadas as expressões JVM, incluindo `getImpactDamage=1.5f+0.75f*getSpellPower(level,caster)`, `getWitherDuration=60+12*clamp(level,1,5)`, `getWitherAmplifier=(level>=5?1:0)`, raio nominal clampado 10–15 e raycast com distância literal 32. Não confundir raycast/radius/controller com hitbox de impacto da bud ou resultados reais. O constructor/controller/NBT e wave/bud possuem gates prévios das PRs #849–#854.

**Fronteira:** nenhuma API mutadora por jogador comprovada. Preservar o provider como autoridade de dano, status, cura e casting; ⛔ `FAIL_CLOSED` para perks externas; Stage 06.05 🟡 e Stage 09 QA físico PENDING. [Ficha](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake — campos da controller e deduplicação de UUID por instância (21/10/2026; PR #854)

**Barra global:** —% porque o denominador universal permanece aberto; piso conservador **≥1.856** objetos semânticos. **Barra Somake:** **83/83 IDs = 100%**; aprofundamento downstream em **5/83 fichas = 6,02%**; subcampanha fixa de providers com JAR exato **35/39 = 89,74%** no checkpoint documentado. +0 magias, +0 adapters e nenhum hook mutador homologado.

A [prova física Java 21 #39538804021](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39538804021), com SHA oficial Somake 1.0.9 `171841ac9f802be9309ecc166c1d972ac6d404c0`, passou **12 testes** e certificou os defaults `witherDuration=80`, `maxTargets=8`, os clamps especializados `maxTargets>=1`, `witherDuration>=30`, `witherAmplifier>=0`, a atribuição `impactDamage:float` e os callsites de armazenamento/restauração NBT dos três campos de efeito. `activeTargetIds` pertence à instância da controller: `lambda$launchWave$0` usa `contains(candidateUUID)` para exclusão e `pruneTargets` usa `retainAll`. **Não** inferir dedup entre controllers, persistência de UUIDs, sucesso real de spawn, valores de cast ou API por jogador. Stage 06.05 🟡, Stage 09 físico PENDING; perks modificadoras **⛔ FAIL_CLOSED**. [Ficha](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake — constructor handoff de Wither e dano na bud (20/10/2026; PR #853)

**Barras inalteradas:** global **—%**, universo total aberto, piso conservador **≥1.856** objetos semânticos; Somake Spells 1.0.9 **83/83 IDs = 100%**, downstream por ficha **5/83 = 6,02%**, subcampanha fixa de JARs de providers exatos **35/39 = 89,74%** no checkpoint publicado. Hooks de perks mutadoras homologados: **0**, sem denominador.

[Prova Java21 #39536052412](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39536052412), `SUCCESS` com **14 testes** e JAR publisher File `8867079` SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`: `FuneralBloomControllerEntity.launchWave` encaminha `impactDamage:F`, `witherDuration:I` e `witherAmplifier:I` da controller ao construtor especializado de `FuneralBloomBudEntity`. O construtor da bud armazena `impactDamage`, limita `witherDuration = Math.max(30,argumento)` e `witherAmplifier = Math.max(0,argumento)`; construtor básico tem default de duração 80. Nova prova estática **não** comprova origem desses fields na controller, imutabilidade em lifecycle, dedup entre buds/controllers, sucesso de efeitos em gameplay ou API per-player. **+0 IDs, +0 adapters**, Stage 06.05 🟡 / Stage 09 real PENDING; perks mutadoras ⛔ `FAIL_CLOSED`. [Ficha](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake 1.0.9 — parâmetros nativos de Wither, push e cura da bud (20/10/2026, PR #852)

**Cobertura global:** `—%` — denominador aberto; piso conservador **≥1.856** objetos semânticos catalogáveis, não equivalentes a todas as habilidades implementadas. **Identidades Somake:** `83/83 = 100%` dos IDs físicos registrados; **auditoria downstream:** `5/83 = 6,02%` fichas neste recorte. **Subcampanha de providers com release exato:** `35/39 = 89,74%` no checkpoint fechado. **Hooks mutadores aprovados:** zero, sem denominador conhecido.

A [auditoria física Java 21 #39533416067](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39533416067) confrontou Somake 1.0.9 File 8867079 ao SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` e passou **14 testes sintéticos**. O novo gate exige a prova exata de `bud.getOwner()` tipado como `LivingEntity` ou nulo (slot4), `slot8.hasEffect(WITHER)` **anterior** ao dano, contador slot6 que cresce apenas quando `applyDamage` retorna verdadeiro e Wither já existia, fields `witherDuration`/`witherAmplifier`, vetor `push(0,0.34,0)` e fórmula de argumento de cura `min_f32(3.75f,1.25f*(float)slot6)`. Nada disso equivale a prova de dano/HP efetivos, jogador owner, aceitação dos status ou API de perks. +0 magias, +0 adapters; **⛔ FAIL_CLOSED** para modificação externa. Stage 06.05 🟡, Stage 09 QA real ainda PENDING. [Ficha detalhada](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake 1.0.9 — filtros efetivos do bloco de dano e cura da bud (20/10/2026, PR #851)

**Barras sem aumento artificial de identidade:** universo global **—%** (piso conservador **≥1.856** objetos semânticos; denominador final aberto), Somake **83/83 IDs = 100%**, recorte de fichas downstream **5/83 = 6,02%**, subcampanha fixa de providers exatos **35/39 = 89,74%** no último checkpoint. A prova acrescenta profundidade técnica a `somakespells:funeral_bloom`, **+0** novos feitiços e **+0** adapters. Hooks de perks mutadoras homologados: **0**, percentual indefinido sem denominador.

A auditoria física Java 21 [#39531339901](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39531339901), com JAR publisher Somake 1.0.9 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, passou **22 regressões sintéticas**. No método nativo `FuneralBloomBudEntity.impact` foi provado que `DamageSources.applyDamage:Z` governa os callsites seguintes de `MobEffects.WITHER`, `addEffect` e `push`; resultado falso salta todo esse bloco. A cura é uma segunda sequência delimitada: slot JVM 4 não nulo **e** inteiro slot JVM 6 positivo, seguidos por `SpellHealEvent → eventBus.post → heal(slot4,float slot7)`. Os retornos de `addEffect` e `post` são descartados. **Gameplay, resultados efetivos, identidade de ator, valor numérico, sucessos de spawn/hit, repetição de proc e hooks continuam não homologados.** Stage 06.05 🟡; Stage 09 QA físico PENDING; perks externas de dano/cura/targeting **⛔ FAIL_CLOSED**. [Ficha detalhada](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake 1.0.9 — AABB independente de Funeral Bloom Bud (21/10/2026, PR #850)

**Barra geral:** `—%`, denominador universal aberto, piso histórico conservador **≥1.856** objetos semânticos. **Barra Somake — identidades:** `83/83 = 100%`; fichas com auditoria downstream na campanha: `5/83 = 6,02%`; hooks mutadores homologados: **0** (taxa sem denominador). Subcampanha física fixa de providers: `35/39 = 89,74%` no último checkpoint com denominador fechado, não uma taxa de cobertura de todos os mods.

A [auditoria Java21 #39529183029](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39529183029) confirmou SHA do Somake 1.0.9 (File 8867079), **14 testes** e o uso de `getImpactPosition` como centro de `AABB(Vec3,Vec3).inflate(1.75d,1.35d,1.75d)`, com armazenamento no slot 5 e consulta posterior `ServerLevel.getEntitiesOfClass(LivingEntity.class,AABB)`. Região de **3,50 × 2,70 × 3,50 blocos** para origem coincidente. Não usar essa geometria como prova de dano/cura/Wither ou mutabilidade por jogador. Efeitos no corpo foram localizados, mas sem guardas efetivamente resolvidos. Nenhum novo ID/adaptador, Stage 06.05 permanece 🟡, Stage 09 físico PENDING e todos os mutadores externos mantêm ⛔ `FAIL_CLOSED`. [Ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake — `maxTargets` ligado ao corte de lista e iteração normal de buds (20/10/2026; PR #849)

**Barras inalteradas:** geral —% (piso global conservador **≥1.856** objetos semânticos, denominador total ainda aberto), Somake 1.0.9 **83/83 IDs = 100%**, aprofundamento downstream nesta campanha **5/83 = 6,02%**, `0` hooks mutadores aprovados (taxa indefinida sem universo de perks). Subcampanha fixa de registro exato em providers: **35/39 = 89,74%** no checkpoint documentado, sem equivalência à completude universal.

[GitHub Actions #39527264831](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39527264831) certificou que `launchWave` aplica `List.subList(0,maxTargets)` ao slot local JVM 4 quando a lista de candidatos excede o campo `maxTargets`, e obtém o iterador desse mesmo slot após o branch. [#39527484911](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39527484911) verificou no JAR SHA-exato a estrutura do loop: uma tentativa de `addFreshEntity` e uma `activeTargetIds.add(UUID)` por iteração normal, descartando ambos os retornos booleanos. **Não** é prova de spawn bem-sucedido, cap de entidades persistidas, identidade do UUID, configuração do field, QA real ou API de perks. Nenhuma nova magia, adapter ou Stage; ⛔ `FAIL_CLOSED` para modificadores externos. Stage 06.05 🟡, Stage 09 físico PENDING. [Ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Somake 1.0.9 — prova de distância XZ e limiar R² no filtro (PR #848)

**Barra geral:** `—%`, universo final ainda sem denominador, mínimo conservador **≥1.856** objetos semânticos, histórico 1.857 em reconciliação. **Barra Somake — identidades:** `83/83 = 100%`. **Downstream por ficha:** `5/83 = 6,02%` no recorte da campanha. **Hooks mutadores homologados:** `0`; percentual das demandas permanece `—%`, pois denominador não foi fechado. **Providers binários exatos da subcampanha fixa:** `35/39 = 89,74%`, sem promoção adicional.

[Workflow Java 21 #39523827891](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39523827891) `SUCCESS`, **12 testes** e SHA do publisher igual: o método `FuneralBloomControllerEntity.isValidTarget(LivingEntity,LivingEntity)` agora tem prova física do seu branch numérico final. `slot2.distanceToSqr(controller.getX(),slot2.getY(),controller.getZ())` é guardado no slot local double 3; o limiar usa duas leituras `controller.getRadius()`, `fmul` float32, `f2d`, `dcmpg` e `ifgt` para rejeição `false`. Para valores finitos, rejeita distâncias quadráticas XZ superiores ao raio ao quadrado. A aceitação final, os papéis de caster/owner/candidato, o impacto separado da bud, o efetivo `maxTargets`, o contrato de perk e QA provider-loaded não são automaticamente promovidos. **⛔ FAIL_CLOSED** para modificadores de targeting/range até boundary segura; Stage 06.05 🟡, Stage 09 PENDING. [Ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Continuação Somake: dois branches intermediários provados (20/10/2026; PR #847)

**Barras de cobertura inalteradas:** universo global **—%** (denominador final aberto, piso conservador **≥1.856** ações/objetos semânticos); Somake 1.0.9 **83/83 (100%)** identidades físicas; auditoria downstream **5/83 (6,02%)** fichas nesta campanha; **0** hooks de mutação por jogador homologados (percentual sem denominador). Subcampanha binária do recorte fixo: **35/39 (89,74%)** no último checkpoint integrado, sem equiparar esse número à completude de todos os mods.

[GitHub Actions Java 21 #39521070264](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39521070264) retornou `SUCCESS` após confronto com Somake 1.0.9 File 8867079 SHA-1 exato; `isValidTarget` agora tem prova causal explícita de **rejeição por aliança**: a referência `slot 1` não pode ser nula para ativar o teste; `slot 2.isAlliedTo(slot 1)` verdadeiro resulta em `false`; valor falso de `isAlliedTo` apenas prossegue. Esta análise amplia o gate anterior de três guardas iniciais sem criar nova identidade, modificar runtime ou promover Stage. **Pendente:** expressão e semântica do `ifgt` final, papéis de caster/owner/alvo, cardinalidade de buds, área de `bud.impact`, configuração e testes provider-loaded/multiplayer/Survival; todos os mutadores seguem ⛔ `FAIL_CLOSED`. `Stage 06.05` 🟡; `Stage 09` QA físico pendente. [Ficha detalhada](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).


## Checkpoint operacional reconciliado — 20/10/2026 (documentação; sem nova prova binária)

**Authority revisada:** `Black-Arcana/main@2e23b94638b4eed9a6d7b83cd1a6b7a82ad6e91b` após merge [#845](https://github.com/Gustavaopere/Black-Arcana/pull/845); modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`; Enshrouded `main@a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`. Este checkpoint apenas reconcilia informações **já documentadas**; hashes de JAR e validações de gameplay não foram reexecutados.

**Barra 1 — universo global de todas as magias, rituais, técnicas e ações sobrenaturais:**

```text
TODOS OS MODS  [????????????????????]  —%  denominador total não identificado
Piso atual do ledger: >=1.856 objetos semânticos (>=1.854 no escopo estrito).
Histórico 1.857/1.855 mantido em revisão após exclusão de registro não publicado.
```

**Subcampanha fechada (não substitui a barra global):** `[██████████████████░░] 35/39 = 89,74%` providers com registro **binário exato** no recorte fixo de 39, conforme checkpoint Hazen de 15/10 no [tracker de pendências](PENDENCIAS-MAGICAS-ATUAIS.md). A diferença 4/39 não define quais quatro magias faltam, tampouco a quantidade de fichas técnicas. PRs #811, #812, #817 e #820 continuam **abertas**, e não se confundem com `main` nem recebem merge por essa métrica.

**Barra 2 — Somake Spells 1.0.9, provider sendo aprofundado:**

```text
IDENTIDADES     [████████████████████]  83/83   = 100% catalogadas na registry
DOWNSTREAM      [█░░░░░░░░░░░░░░░░░░░]   5/83   =   6,02% neste recorte
PERKS MUTADORAS [????????????????????]  —% (0 hooks aprovados; demanda sem denominador)
```

O aprofundamento adicional de `somakespells:funeral_bloom` em [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md) não aumenta a contagem de identidades nem o número 5 de fichas downstream já visitadas. Após [#845](https://github.com/Gustavaopere/Black-Arcana/pull/845), **três condições de rejeição de `isValidTarget` são comprovadas**, porém três branches posteriores, papéis de A/B, `maxTargets` efetivo, efeitos da bud e hooks continuam `NOT_PROVED`; `FAIL_CLOSED`.

**Painel de providers e escopo correto da contagem:**

| Provider | Identidades/objetos conhecidos | Aprofundamento técnico e estado de integração |
|---|---|---|
| Somake Spells 1.0.9 | ✅ 83/83 IDs de spell | ⚠️ 5/83 fichas com auditoria downstream; ⛔ 0 hooks mutadores homologados |
| Iron's Spells 'n Spellbooks 3.16.3 | ✅ 110/110 **IDs ativos** no catálogo | 🟡 **110/110 dossiês causais source-pinned** apenas na [PR #825 draft](https://github.com/Gustavaopere/Black-Arcana/pull/825); 110 fichas-base mapeadas na [PR #795 draft](https://github.com/Gustavaopere/Black-Arcana/pull/795); ⚠️ sem equivalência JAR instalado/QA universal; ⛔ adapters não dedutíveis da cobertura documental |
| Epic Fight 21.17.3.1 | ✅ 43/43 IDs core classificados; 42/42 JSONs físicos e 28 dossiês reportados na branch #825 | ⚠️ técnicas, ataque/fase/dano e carregamento têm provas por eixo, mas nenhum número de perks homologadas inferido; PR #825 permanece **draft** |
| Universo de outras famílias | ⚠️ recorte parcial com mínimos semânticos documentados | 🟡 identificar todos os providers pela modlist; ⛔ nenhuma conclusão global de completude até fechar o denominador |

O **ledger da PR #825** corrige a fila ativa do Iron's: `soulfire_ray` e `thunder_step` têm implementações de fonte mas **registro comentado**, portanto **fora** das 110 magias ativas; `cloud_of_regeneration` está **deprecated**, preservada como LEGACY, fora do denominador. Checkpoints intermediários 101/110 e 102/110 daquela mesma branch são históricos e não devem sobrescrever o novo 110/110 causal.

**Guardas para o próximo trabalho:** separar identidade registrada, parâmetros estáticos, dataflow downstream, hook per-player e comportamento efetivo no mundo; inserir classes/métodos/source pins por ficha; não transformar evento observacional em setter. Custos e casting permanecem em Iron's/Somake, dano/mundo mágico próprio em Black Arcana, e Mastery/perks no RPG Skill Tree por contrato real. Stage 06.05 🟡 em auditoria; Stage 09 físico PENDING. Este checkpoint de documentação não modifica runtime, testes binários ou Stage.


**Checkpoint documental com base em `Black-Arcana/main@511ec03f0da62ebfc1722825def50354594976c3` e modlist física indexada no `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.** Este arquivo distingue a cobertura dos objetos mágicos, a dos registros binários, o aprofundamento por campo e a habilitação real de perks.

## Barra 1 — universo de magias/rituais/ações sobrenaturais de todos os mods

**Total desconhecido — percentual global indeterminado.** O catálogo registra pelo menos **1.857 objetos semânticos na baseline de 13/10** (**1.855** no escopo mencionado naquele checkpoint), mas o universo final de objetos de todos os mods continua **sem denominador verificável**. Isto é um **piso**, não uma fração; não representar como `1857 / 1857 = 100%`. A PR draft #825 tem uma baseline operacional diferente, **mínimo 1.856 / 1.854**; reconciliar denominador e cortes antes de substituir uma baseline por outra.

Campanha de evidência física do recorte histórico **39 providers** na `main`: **25/39 = 64,1%** com prova binária exata no último checkpoint consolidado de 13/10; é uma **submétrica delimitada**, não a conclusão do catálogo global, não é cobertura de perks nem QA em cliente. PRs draft posteriores podem ter avançado a campanha mas não contam como `main`.

## Barra 2 — Somake Spells 1.0.9, provider trabalhado nesta tranche

**83/83 (100%)** — fichas de identidade de spells do release verificadas no registry exato e já presentes em `registry-1.0.9/`. **7/83 (8,43%)** — fichas que receberam **nesta tranche** um novo dossiê de gate de aquisição/perk por terem `allowCrafting()` próprio (3 retornos `false` constantes, 4 não constantes). **7/7 (100%)** — classes com overrides `allowCrafting()` cobertas por esse recorte de documentação. Isto não representa percentual de todas as fichas com hooks/perks implementáveis: a auditoria de causalidade dos efeitos e mecanismos para os outros 76 não foi aferida aqui.

`Somake 1.0.9` = ✅ catalogado estruturalmente, ⚠️ condicionado em configuração/reachability, ⛔ sem hook mutador homologado para a mudança destas skills. Nenhuma nova identidade estrita; nenhuma migração de runtime; Stage 06.05 continua 🟡 e Stage 09 depende da campanha física sob D035.

### Critérios de avanço, por mod

Para cada provider o acompanhamento deve sempre expor: `registrados confirmados / identificados`, `fichas com campos técnicos comprovados / objetos elegíveis`, `hooks mutadores validados / demandas de mutação` (quando houver denominador) e `QA físico`. Se qualquer denominador estiver aberto, usar **—%** e declarar explicitamente o escopo, sem completar com estimativas.

Fonte da tranche: [Somake — matriz de sete gates](../providers/✅-somake-spells/PERK-REACHABILITY-GATES-1.0.9.md). Fonte global: [catálogo canônico](CATALOGO-GLOBAL-MAGIAS.md), [pendências](PENDENCIAS-MAGICAS-ATUAIS.md) e [regras técnicas](PERK-READY-TECHNICAL-STANDARD.md).

## Continuação Somake — prova de métodos de crafting no JAR (18/10/2026)

[CI SHA-exata #39186593493](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39186593493): **7/7 métodos de `allowCrafting()` com classe/descritor comprovados, 7/7 testes sintéticos**, incluindo quatro dependentes de três campos `Config.DISABLE_*` identificados no bytecode e três constantes `false`. Evidência estritamente estática/clean-room; [matriz compilada](../providers/✅-somake-spells/EXACT-BINARY-CRAFTING-METHOD-SEAMS-1.0.9.md). Barras inalteradas em seu escopo: global —% (denominador aberto), Somake identidades 83/83 (100%), aprofundamento **7/83 = 8,43% no recorte de métodos de aquisição**. Nenhuma QA física Survival, API de perk ou implementação nova inferida.

## Somake 1.0.9 — segundo eixo: descobertas compiladas de execução

[Java21 #39192999780](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39192999780) **SUCCESS**, SHA-1 físico/publisher verificado. O novo probe compilado cobriu as **7/7 classes desta campanha**, encontrou 116 declarações de métodos (101 com nomes de interesse para inspeção), incluindo onCast, onServerCastTick, pre-cast, getters de dano/cura/raio/duração e referências a entidades downstream. A [matriz causal estática](../providers/✅-somake-spells/EXACT-BINARY-CAST-CALLSITES-1.0.9.md) e as sete fichas foram atualizadas. O primeiro run #39192927218 falhou pelo teto de 250 caracteres para uma referência JVM, corrigido para 2048 com teste negativo; a execução seguinte passou.

**Barras invariantes:** global **—%** (universo ainda sem denominador); Somake **83/83 = 100% identidades**. A campanha limitada de **métodos de cast/efeito cobre 7/83 = 8,43%** das fichas atuais, sem equivaler a profundidade causal de runtime, fórmula completa ou perks homologadas. Identidades novas +0; adapters +0; Stage 06.05 🟡; validações físicas/Survival ainda pendentes.

## Somake 1.0.9 — terceira camada: auditoria de entidades

**Fonte:** [GitHub Actions #39195233005](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195233005), Java 21, JAR Somake 1.0.9 com SHA-1 exata `171841ac9f802be9309ecc166c1d972ac6d404c0`, `SUCCESS`, **8 testes sintéticos**. O gate de cast dependente [#39195233020](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195233020) também passou. Inspeção estática, não QA de jogador/mundo.

- **Barra geral:** —% (denominador final do universo de todos os providers e ações semânticas ainda aberto). O checkpoint histórico de 1.857 objetos globais é piso, sem promoção desta campanha.
- **Somake — identidade de registry:** 83/83 = **100%**, mantido; novas identidades: **0**.
- **Somake — métodos de spell/casting:** 7/83 = **8,43%** das fichas receberam exploração de assinaturas/referências no lote anterior; não representa fórmula completa.
- **Somake — entidades downstream:** 5/83 = **6,02%** das fichas agora possuem nova referência binária de entidade específica auditada; **5/5 = 100% deste recorte fechado** (21 + 28 + 23 + 18 + 15 = 105 declarações e 15 + 22 + 17 + 15 + 9 = 78 métodos de interesse). A existência dessas cinco entidades não implica que as 78 rotinas tenham execução efetiva comprovada.
- **Hooks mutadores por jogador validados neste lote:** 0 (não inferir percentual sem denominador de demandas de perks). **Survival/provider-loaded/real-client**: ⚠️ pendentes; **perks de mutação**: ⛔ FAIL_CLOSED.

O scanner evidencia `LivingEntity.hurt` direto no Fragmented Sword Rain versus `DamageSources.applyDamage` no Vortex/Bell, além de filtragem de aliados/alvos e efeitos Wither/Blessing. Estes são símbolos compilados, não provas de que `SpellDamageEvent` seja consumido em todos os caminhos, de hitbox/raio numericamentes modificáveis ou de equivalência com o pack real. [Matriz exata](../providers/✅-somake-spells/EXACT-BINARY-ENTITY-CALLSITES-1.0.9.md).

**Próximo gate:** `FuneralBloomBudEntity` e `pulseDamage`/`tick` com dataflow, caps e coexistência de eventos; preservar autoridade do Somake, Iron's e RPG Skill Tree sem dupla cobrança/dano/Mastery. Stage 06.05 continua 🟡; Stage 09 preserva todos os gates físicos.

## Somake 1.0.9 — quarta camada: bud e impacto secundário (19/10/2026)

**Evidência auditada:** [Java21 #39197671447](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39197671447) `SUCCESS`, **10 testes sintéticos**, classfile `FuneralBloomBudEntity` SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, **26 métodos JVM** inspeccionados com o inicializador estático isolado. A primeira execução #39197533908 não é usada para a atribuição final de símbolos por possível contaminação da última rotina pelo `<clinit>`.

- **Barra global de todo o conteúdo mágico:** **—%**, denominador não determinado; piso histórico de pelo menos 1.857 objetos semânticos não recebe nova raiz por esta entidade.
- **Barra Somake — identidades da registry:** **83/83 = 100%** inventariadas no release, independente de reachability/castability.
- **Somake — fichas com auditoria de entidades downstream:** **5/83 = 6,02%** das identidades tiveram no mínimo uma entidade analisada no lote anterior; a Funeral Bloom é **a mesma identidade** enriquecida novamente, portanto o percentual não sobe.
- **Subescopo de classfiles downstream inspecionados:** seis classes distintas: `FragmentedSwordRainEntity`, `FuneralBloomControllerEntity`, `WitheredRoseVortexEntity`, `CustodiaCaeliSigilEntity`, `BellEntity` e agora `FuneralBloomBudEntity`. Uma sétima classe conhecida, `FuneralBloomImpactEntity`, foi referenciada pelo bud e **não** está inspecionada. Esse conjunto é apenas a cadeia descoberta até agora; não apresenta percentual global de todas as entidades do mod.
- **0** novos spells, **0** adapters mutadores homologados. Dano/Wither/cura/impulso/NBT foram identificados como símbolos do bud, não há fórmula numérica ou execução física comprovada.

**Autoridades e gates:** Somake mantém runtime do provider; Iron's mantém host/recursos/dano host; RPG Skill Tree atributos/perks/Mastery por boundary efetivo; Black Arcana rege seu próprio runtime. Stage 06.05 🟡, Stage 09 físico PENDING sob D035. [Dossiê do bud](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md).

## Somake 1.0.9 — quinta camada: entidade Funeral Bloom Impact (19/10/2026)

- [Java21 #39198753251](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39198753251) `SUCCESS`, publisher File 8867079/ SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, **sete testes sintéticos**, classe `FuneralBloomImpactEntity` com **8 métodos nomeados** (Scale sincronizado, `setScale` com `Mth.clamp`, abertura com `tickCount/smoothstep`, `tick/discard`, NBT de Scale).
- **Global —%**: número total de magias/rituais/ações e universo de mods ainda não denominados; não promover completude do catálogo.
- **Somake — registry 83/83 = 100% identidades**; **5/83 = 6,02%** das fichas com pelo menos uma auditoria de entidade downstream, sem alteração. A Funeral Bloom continua sendo a mesma magia.
- **7 classfiles downstream distintos inspecionados** neste recorte acumulado: cinco do primeiro lote, `FuneralBloomBudEntity` e agora `FuneralBloomImpactEntity`. Não é prova de que todas as entidades mágicas do Somake foram encontradas.
- **0 novas identidades; 0 adapters mutadores certificados**. Nenhum callsite direto de dano, cura ou status apareceu nos oito métodos da entidade de impacto, o que não exclui execução herdada/delegada. A natureza exclusivamente visual permanece hipótese.

**Gates:** custos e cooldown permanecem owner Iron's; Black Arcana conserva apenas seu runtime; RPG Skill Tree fornece perks/Mastery por contrato real. Stage 06.05 🟡, Stage 09 físico pendente sob D035. Próxima prioridade é análise de constantes, dataflow de `FuneralBloomBudEntity.impact`/controller e perfil real provider-loaded. [Dossiê exato](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-IMPACT-1.0.9.md).

## Somake 1.0.9 — sexta camada: prova aritmética JVM da Funeral Bloom (19/10/2026)

- **Fonte física exata:** CurseForge File 8867079, `somakespells-1.0.9-1.21.1.jar`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; sibling modlist `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.
- **Auditoria numérica Java21 [#39201393631](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39201393631):** `SUCCESS` em 15 testes sintéticos/integrados, 4 classfiles e 17 métodos. As cinco provas de getter `int` são derivadas por avaliador JVM estritamente linear, com fluxos ramificados/não suportados rejeitados. O HEAD final será atualizado com snapshots de fórmulas para fail-closed.
- **Fórmulas comprovadas** para `L=clamp(level,1,5)`: `getMaxTargets=4+L`, `getDuration=240+20*(L-1)`, `getWaveInterval=18-L`, `getWitherDuration=60+12*L`. `getTelegraphTicks=max(9,13-jvm_idiv(level,2))` usa `level` sem clamp e semântica de divisão inteira Java.
- **Limites de clamp diretamente demonstrados** em callsites: `FuneralBloomSpell.getRadius` passa 10.0/15.0 como segundo/terceiro argumentos, `FuneralBloomImpactEntity.setScale` passa 0.65/1.6, `getOpenProgress` passa 0/1 em duas chamadas. Isto **não** é prova da dimensão final ou da possibilidade de perk alterar o método.
- **Barra global:** —% (denominador completo de mods/magias/ações mágicas ainda sem prova); piso histórico 1.857 objetos não alterado.
- **Barra Somake — registry:** **83/83 = 100%** identidades; **5/83 = 6,02%** fichas com auditoria de uma ou mais entidades downstream; 7 classfiles distintos permanecem no acumulado. O novo probe examina 4 classes **já conhecidas**, sem aumentar as contagens.
- **0** novas magias, **0** adapters de mutação homologados, **0** validações Survival/cliente provadas neste incremento.

**Critérios pendentes:** aplicar as expressões aos consumidores da versão exata, identificar unidade de duração/raio/ticks, dados de SpellPower/escola/branch, proteger contra duplicação de dano/cura/Mastery, e executar QA provider-loaded/multiplayer/Survival do modpack. Stage 06.05 segue 🟡; Stage 09 condicionado conforme D035. [Dossiê numérico](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-NUMERIC-1.0.9.md).

## Somake 1.0.9 — sétima camada: dataflow float de dano da Funeral Bloom (19/10/2026)

- Artefato: `somakespells-1.0.9-1.21.1.jar`, publisher CurseForge File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` (modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`).
- [Auditoria Java21 #39243467444](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39243467444): `SUCCESS`, **10 testes** de interpretação abstrata tipada (inclui Java compilado), prova integral do **retorno float** de `FuneralBloomSpell.getImpactDamage(int,LivingEntity)` como `1.5f + (getSpellPower(level_input,caster)*0.75f)` (0 branches, 1 chamada externa tipada); `getRadius` retorna `NOT_PROVED / branch_or_throw` por ter 2 branches, embora clamp 10.0f/15.0f esteja identificado.
- A PR também inclui regressões de snapshot negativas para impedir que uma mudança no JAR seja interpretada como prova do mesmo retorno; o gate final do HEAD será verificado separadamente.
- **Barra global:** —% (universo de spells/rituais/poderes e providers não fechado; piso histórico >=1857 ações/objetos não é denominador).
- **Barra Somake — identidades:** 83/83 = **100%** catalogadas. **5/83 = 6,02%** fichas com auditoria de pelo menos uma entidade downstream, sem incremento; sete classes downstream acumuladas (não novas magias). A análise presente adiciona profundidade a `somakespells:funeral_bloom`, não cobertura de novos IDs.
- **Perks de alteração de dano/área aprovadas:** **0**; `FAIL_CLOSED` até API/evento/callback per-player versionado e prova de causalidade downstream. Sem alterações em Black Arcana runtime, host Iron's, RPG Skill Tree, Mastery, custo ou cooldown.

**Pendências:** CFG completo de `getRadius`/`SchoolType.getPowerFor`, origem e configuração de `getSpellPower` no host 3.16.3, consumo do `impactDamage` pelo bud, dano efetivo/Wither/cura/knockback, bounds, FPS/carga, cliente/multiplayer/Survival e modpack físico (D035). Stage 06.05 permanece 🟡; Stage 09 condicionado. [Dossiê float](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-FLOAT-DATAFLOW-1.0.9.md).

## Somake 1.0.9 — oitava camada: CFG do raio e assinatura do host Iron's (19/10/2026)

- [Java21 #39246133056](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39246133056) `SUCCESS` — nove testes sintéticos e dois JARs de release específica. Somake File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; API Iron's 3.16.3 SHA-256 `69e81104a9fd31a402d9c89ab09c2a6b2fd6d2ab98db5a37bb159517363ee9ad`. CI final de PR será registrado separadamente.
- ✅ `getImpactDamage` do Somake chama `getSpellPower(int,Entity):float`; assinatura encontrada no `AbstractSpell` da API oficial. ⚠️ Corpo do método API referencia `SpellConfigManager.getSpellConfigValue`, `SchoolType.getPowerFor` e `LivingEntity.getAttributeValue`, sem prova de fórmula/config/atributo real do RPG Skill Tree.
- ✅ CFG estrutural de `getRadius`: 28 instruções alcançáveis, `ifnonnull` + `goto`, uma junção/retorno e clamp 10.0f/15.0f. ⚠️ Condição concreta e fórmula integral do raio permanecem sem prova.
- **Barra global:** —% (denominador não estabelecido; piso histórico de >=1.857 objetos semânticos, sem aumento). **Barra Somake:** 83/83 identidades = 100% inventariadas; 5/83 (6,02%) fichas com auditoria downstream, sete classfiles distintos anteriormente examinados. Esta rodada aprofunda a mesma magia, não acrescenta IDs ou classfiles de efeito.
- **Hooks per-player validados nesta rodada:** 0; ⛔ `FAIL_CLOSED`. Black Arcana mantém apenas seu runtime; Somake efeitos provider-native; Iron's host; RPG Skill Tree somente progressão com contrato real. Stage 06.05 🟡 e Stage 09 condicionado sob D035.

[Relatório técnico de CFG/host](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-IRONS-1.0.9.md).

## Somake 1.0.9 — nona camada: duas fórmulas de ramo do raio (19/10/2026)

- [Java21 #39259507432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39259507432) `SUCCESS`, dez testes sintéticos/negativos e fixture Java21, JAR Somake File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`: o interpretador JVM tipado validou os 28 opcodes do `getRadius` nos dois caminhos de `ifnonnull(caster)`, guard `caster == null` ou `caster != null`.
- ✅ Retorno de raio: `clamp_f32((9.5 + i2f(level)*0.82) + max_f32(0, P-1)*0.65, 10,15)` para caster não nulo, com `P=d2f(SchoolType.getPowerFor(caster))`; mesmo cálculo com `P=1` para caster nulo. São representações matemáticas das operações float32 do JAR; sem prova de raio/hitbox/alcance aplicados em jogo.
- ✅ Agora há **sete getters com expressões JVM de retorno examinadas nesta cadeia específica da Funeral Bloom**: cinco inteiros, `getImpactDamage` float e `getRadius` float por dois caminhos. Não contar os dois ramos como duas magias ou duas identidades independentes.
- **Barra global:** —%, denominador final não comprovado; piso histórico de pelo menos 1.857 objetos semânticos sem variação neste incremento.
- **Barra Somake (identidades):** **83/83 = 100%** dos IDs da registry; **5/83 = 6,02%** fichas com entidades downstream auditadas (cohort anterior), sete classfiles distintos de entidades já examinados; não houve nova magia nem nova classe nesta PR.
- **Integração:** 0 adapters mutadores per-player homologados. ⛔ `FAIL_CLOSED` para perks de área/dano/tempo/targets até provar consumidores/eventos/atributos/config e QA provider-loaded; Stage 06.05 🟡; Stage 09 condicionado sob D035.

[Dossiê tipado de ramo e raio](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md).

## Somake 1.0.9 — décima camada: consumidores de área da Funeral Bloom (19/10/2026)

- [Java21 #39262591589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39262591589), **SUCCESS / 9 testes**: inspeção SHA-exata de `FuneralBloomSpell`, `FuneralBloomControllerEntity`, `FuneralBloomBudEntity` em seis métodos. Somake File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- `Spell.onCast`: 81 instruções, chamada `getRadius(int,LivingEntity)` e construção da controller com dois argumentos float. `Controller.tick`: 156 instruções, chama `getRadius()` e `launchWave`. `Controller.launchWave`: 196 instruções, `getRadius()`, `AABB.inflate`, `ServerLevel.getEntitiesOfClass` e construção de buds. `Bud.impact`: 279 instruções, outra `AABB.inflate`, query de entidades, `DamageSources.applyDamage`, `SpellHealEvent`/`heal`, sem chamada direta `getRadius`.
- ⚠️ **Não concluir** que o getter determina ambas as AABB: callsites por método não demonstram dataflow do float nos construtores, operandos `inflate`, ramificações nem efeito recebido por entidade. `invokedynamic` permanece sem destino de callback reconstruído.
- **Barra global:** —% (denominador de todos mods/actions ainda aberto); piso histórico >=1857 objetos semânticos sem aumento.
- **Barra Somake:** **83/83 = 100%** identidades registry, **5/83 = 6,02%** fichas com entidades downstream auditadas na campanha, sete classfiles de entidades distintos já conhecidos. Novo lote de callsites em três classes **existentes**, sem nova magia ou entidade adicional.
- **Perks mutadoras homologadas:** 0. ⛔ `FAIL_CLOSED`; Stage 06.05 🟡 e Stage 09 condicionado (D035). RPG Skill Tree fornece progressão sem controlar casting/efeitos do Black Arcana ou dos providers.

[Dossiê de consumidores do raio](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md).

## Somake 1.0.9 — décima primeira camada: tentativa de vínculo construtor → raio (19/10/2026)

- [Auditoria exata #39286470816](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39286470816): `SUCCESS` com 13 testes Java21 e SHA-1 físico Somake 1.0.9 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- **Resultado da prova:** `FuneralBloomControllerEntity.getRadius()` não é o getter direto de três opcodes esperado pelo scanner (`NOT_PROVED`). Por consequência, ainda não foi demonstrado qual dos dois floats do construtor (slots JVM 3 e 8) origina o getter. Esta é uma rejeição **restrita ao padrão direto**, não uma incompatibilidade do mod.
- **Revisão subsequente na PR #837:** agrega metadados estruturais (contagens, campos `float` e referências) para determinar a próxima auditoria; a execução no HEAD final ainda precisa ser comprovada.
- **Barra global:** —% (denominador total indisponível; piso histórico >=1.857 objetos semânticos sem alteração). **Somake:** 83/83 identidades = 100%; 5/83 fichas com entidades downstream = 6,02%; as sete classes downstream conhecidas e o conjunto de magias permanecem inalterados.
- **Integração:** zero novas interfaces mutadoras; ⛔ `FAIL_CLOSED`; Stage 06.05 🟡 e Stage 09 condicionado sob D035. Sem promover status com base em testes sintéticos ou na presença de callsites.

[Dossiê de auditoria do construtor/raio](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md).

## Somake 1.0.9 — décima segunda camada: `DATA_RADIUS` sincronizado (19/10/2026)

- **JAR exato** File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. [Java21 #39288405552](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39288405552), `SUCCESS` 16 testes, prova do caminho `FuneralBloomControllerEntity.getRadius():float → SynchedEntityData.get(DATA_RADIUS) → Float.floatValue()`. O getter possui sete instruções, 0 branches, 0 operações aritméticas e um único retorno.
- [Varredura de 30 métodos #39289130886](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39289130886), `SUCCESS`: `defineSynchedData`, `getRadius`, `setRadius(float)` referenciam o accessor; `setRadius` também possui referências a `Float.valueOf` e `SynchedEntityData.set`. A escrita direta no construtor e a interpretação completa do setter continuam `NOT_PROVED`.
- **Contagens inalteradas:** global —% (denominador desconhecido; piso histórico >=1.857 objetos); Somake **83/83 (100%)** identidades, **5/83 (6,02%)** fichas com entidades downstream auditadas e sete classfiles downstream no conjunto anterior. Novo trabalho aprofunda a mesma entidade e não adiciona ID de magia.
- **Bloqueios:** `0` adapters de alteração do raio homologados; ⛔ `FAIL_CLOSED` para perks sem contrato; Stage 06.05 🟡 e Stage 09 condicionado conforme D035. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md).

## Continuação da campanha — Somake Funeral Bloom: construtor → raio interno (19/10/2026, PR #838)

**Barra geral — magias, rituais e ações sobrenaturais de todos os mods:** **—%** porque o denominador global segue aberto. Pisos históricos divergem entre **1.856** (reconciliação Requiem) e **1.857** objetos; usar conservadoramente `>=1.856`, sem somar entidades, helpers ou as mesmas magias repetidas. Nenhuma nova raiz foi identificada neste lote.

**Barra Somake 1.0.9 — identidades de spells:** **83/83 = 100%** da registry física, não 100% dos dados causais nem de perks. **Profundidade de efeitos downstream no recorte acumulado:** **5/83 = 6,02%** fichas de origem com entidade auditada, sete classfiles downstream distintos observados; esta prova aprofunda a Funeral Bloom já contada, sem aumentar 5/83. **Perks de mutação homologadas: 0**; percentual de cobertura de mutações permanece —% por falta de denominador de demandas/hook testado.

**Nova evidência de artefato exato:** [workflow SHA-exato #39292948277](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39292948277), `SUCCESS`, Java 21, 31 testes até HEAD `db24ea457eaa24c977d990ddf199ff4bc968c60c`. JAR Somake File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.

- ✅ `FuneralBloomControllerEntity.<init>(Level,LivingEntity,float,int,int,int,int,float,int,int)`: primeiro `float` no slot JVM **3** passado diretamente à chamada interna `setRadius(float)`; segundo `float` slot **8** não é associado ao raio pela presente prova.
- ✅ `setRadius(float)`: caminho linear integral de **10 opcodes** com `Mth.clamp:(FFF)F` e limites **6.0f / 18.0f**, `Float.valueOf` e `SynchedEntityData.set(DATA_RADIUS,...)`.
- ✅ `getRadius():float`: `SynchedEntityData.get(DATA_RADIUS)`, `Float.floatValue()` (prova de leitura antecedente preservada).
- ⚠️ Não aferidos o stack dos argumentos de `FuneralBloomSpell.onCast`, uso do valor nos operandos `AABB.inflate` de controller/bud, configuração e targeting/raio de impacto reais.
- ⛔ Sem hook oficial de mutação per-player, adapter do RPG Skill Tree ou QA real do modpack: **FAIL_CLOSED**. Stage 06.05 🟡, Stage 09 físico PENDING sob D035.

As três relações locais acima **superam o resultado negativo anterior referente ao setter de sete opcodes**, sem invalidar o registro histórico de sua rejeição. Testes negativos adicionais da PR #838 e o CI do HEAD final exigem observação separada, antes de merge. [Dossiê](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md) e [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).

## Continuação Somake — proveniência do raio a partir de `onCast` (19/10/2026, PR #839)

- **Barra geral de todas as magias/rituais/ações sobrenaturais:** **—%**, universo/denominador definitivo ainda aberto. Adotar piso histórico conservador `>=1.856` enquanto os checkpoints `1.856 / 1.857` não forem integralmente reconciliados. A análise de callsite **não acrescenta uma identidade**.
- **Barra Somake 1.0.9 (identidades registradas):** **83/83 = 100%**. **Subbarra de fichas com auditoria downstream nesta campanha:** **5/83 = 6,02%**. Esta prova é da mesma Funeral Bloom, já contada; não aumenta a segunda barra. Mutadores per-player homologados: **0** (sem denominador total de demandas verificadas, percentual —%).
- [Java21 SHA-exata #39296264174](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39296264174): `SUCCESS`, **45 testes**. Scanner de pilha JVM com janela estrita de **31 instruções** comprovou que o retorno de `FuneralBloomSpell.getRadius(int,LivingEntity):float` é diretamente o **primeiro argumento float (ordinal 3)** da `FuneralBloomControllerEntity`. Somado às provas anteriores (#838), encerra a causalidade estática **callsite getter → construtor float slot 3 → setter clamp 6–18 → SynchedEntityData.DATA_RADIUS → getter da controller**. A prova independente do `getRadius` do spell documenta clamp `10–15` no retorno para entradas finitas.
- **Pendências mantidas:** `onCast` origem efetiva dos parâmetros do getter e do segundo float, operandos de `AABB.inflate` em `launchWave` e `bud.impact`, efeitos/dano/cura por alvo, configs efetivas/Survival, cliente, multiplayer/claims e contrato público de mudança por perk. ⛔ `FAIL_CLOSED`; Stage 06.05 🟡, Stage 09 físico PENDING; nenhuma promoção de Stage.

Provas por método em [dossiê de radius controller](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md) e [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md). Esta evidência é estática/clean-room, sem exportar código ou bytecode de terceiros.

## Continuação Somake — `launchWave` e três operandos de `AABB.inflate` (19/10/2026, PR #840)

**Barra geral (todas as magias/rituais/ações sobrenaturais dos mods): —%**, por denominador global ainda aberto; piso histórico conservador `>=1.856` objetos semânticos até reconciliar checkpoints `1.856/1.857`. **Sem novas identidades** neste lote.

**Barra Somake 1.0.9 (identidades de registry): 83/83 = 100%.** **Subbarra de fichas com entidades downstream auditadas nesta campanha: 5/83 = 6,02%.** Aprofundamento da mesma `somakespells:funeral_bloom` já catalogada; sete classfiles downstream acumulados não crescem. Mutadores per-player aprovados **0**, e o percentual de cobertura de perks segue —% por denominador de demandas ainda não auditado.

- [Java21 #39303857720](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39303857720), `SUCCESS`, SHA exata: prova estrutural de 196 instruções, três chamadas a `getRadius` no método, mas só duas anteriores ao único `AABB.inflate(DDD)`. A hipótese dos três getters consecutivos foi **rejeitada** corretamente no gate causal.
- [Java21 SHA-exata #39304248399](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39304248399), `SUCCESS`, **21 testes**: sequência JVM tipada sem ingressos de desvios prova que **X/Z recebem `f2d(controller.getRadius())`** e **Y recebe literal `double 10.5d`** em `FuneralBloomControllerEntity.launchWave(ServerLevel).AABB.inflate(DDD)`. Publisher File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; mesma modlist física sibling.
- **Cadeia local certificada:** spell getter (clamp retorno 10–15 para entrada finita) → argumento 3 do construtor → setter da controller (clamp 6–18) → `DATA_RADIUS` → getter da controller → X/Z da expansão AABB; Y = 10.5d, separado do raio.
- **Pendências:** origem da AABB receptora, uso da AABB retornada na query e filtros/alvos, existência real e cardinalidade de buds, `FuneralBloomBudEntity.impact` e suas dimensões, dano/cura/Wither, QA em Survival/provider-loaded, cliente/multiplayer, API externa segura de modificação per-player. ⛔ `FAIL_CLOSED`; Stage 06.05 🟡 e Stage 09 físico PENDING. A prova de operandos não é contrato de perk ou validação de raio/hitbox no mundo.

[Detalhes de consumidores](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md), [cadeia da controller](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md) e [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).

## Continuação Somake — `launchWave` passa AABB expandida à query (20/10/2026; PR #841)

**Barra global:** —% (denominador dos mods/objetos semânticos ainda aberto; piso histórico conservador `>=1.856`, com discrepância de checkpoints 1.856/1.857 ainda não reconciliada). **Barra Somake:** **83/83 = 100%** identidades da registry SHA-exata. **Subbarra downstream:** **5/83 = 6,02%** fichas com entidades auditadas na campanha; a mesma Funeral Bloom recebe prova aprofundada. **Perks mutadoras homologadas:** **0**, percentagem de cobertura indeterminada por denominador/hook não provado. Nenhuma identidade ou adapter adicionada.

- [Java21 SHA-exata #39466062186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39466062186): `SUCCESS` / **29 testes**, gate `PASS_SHA_EXACT_WAVE_XZ_RADIUS_Y_10_5_AND_QUERY_AABB_LINK`, publisher Somake 1.0.9/File 8867079/SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. Modlist sibling: `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.
- **Nova cadeia SHA-exata local:** spell `getRadius` → primeiro float da controller → `setRadius`/clamp 6–18 → `DATA_RADIUS` → `controller.getRadius()` → `AABB.inflate(R,10.5d,R)` → armazenamento `astore_3` → recuperação `aload_3` → argumento AABB de `ServerLevel.getEntitiesOfClass(LivingEntity.class,AABB,Predicate)`. O `Predicate` é simbolicamente verificado como construído por `invokedynamic`, mas sua lógica **não** foi auditada.
- **Continuam ⚠️:** AABB inicial, critérios reais de `Predicate`, transformação de resultados em buds, deduplicação/maxTargets, geometrias de `FuneralBloomBudEntity.impact`, dano/cura/Wither, gameplay client/provider-loaded/Survival/multiplayer, contratos API de perk. **⛔ FAIL_CLOSED** quanto a mutações; Stage 06.05 🟡, Stage 09 manual físico PENDING sob D035. Esta prova estática não promove Stage.

[Auditoria da seleção](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md) · [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).

## Continuação Somake — implementação do Predicate localizada por BootstrapMethods (20/10/2026; PR #842)

- **Barra global:** **—%**, denominador da modlist/catálogo total ainda não reconciliado. Piso conservador `>=1.856` objetos semânticos, com divergência `1.856/1.857` de checkpoints históricos em aberto. **Nenhuma identidade nova.**
- **Barra Somake 1.0.9:** **83/83 = 100%** para IDs registrados no JAR SHA-exato; **subbarra downstream nesta campanha 5/83 = 6,02%** (a mesma Funeral Bloom foi aprofundada). Perks mutadoras homologadas **0** e sem denominador de demandas; —%.
- [Java21 SHA-exata #39471626461](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39471626461): `SUCCESS / 38 testes`, Somake 1.0.9 File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, gate `PASS_SHA_EXACT_WAVE_QUERY_PREDICATE_BOOTSTRAP_BOUND`. O `Predicate` fornecido a `ServerLevel.getEntitiesOfClass(Class,AABB,Predicate)` em `FuneralBloomControllerEntity.launchWave` tem `InvokeDynamic #0:test` → `LambdaMetafactory` → **`REF_invokeVirtual lambda$launchWave$0(LivingEntity,LivingEntity):boolean`**. O helper tem **15 instruções / 2 branches**, chama `isValidTarget`, `getUUID`, `Set.contains` e consulta `activeTargetIds`. Um segundo helper com retorno `double` refere `distanceToSqr` (4 instruções), sem ligação de bootstrap/sort/raio comprovada.
- **Limites:** sentidos booleanos dos desvios, semântica completa de elegibilidade, priorização por distância, `maxTargets`, cardinalidade/geração de buds, AABB do `FuneralBloomBudEntity.impact`, dano/cura, Survival/provider-loaded, cliente/multiplayer/PvP/claims e API mutadora por jogador **não provados**. ⛔ `FAIL_CLOSED`; Stage 06.05 🟡, Stage 09 validação física PENDING. Zero runtime/adapter modificado.

[Prova de targeting](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md) · [ficha da magia](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).

## Continuação Somake — `Predicate` seleciona válido e UUID inédito (20/10/2026; PR #843)

- **Progresso global:** **—%**, denominador total ainda não reconciliado. Piso semântico conservador `>=1.856` e discrepância histórica `1.856/1.857` mantida. **Não há novo ID de feitiço.**
- **Somake 1.0.9:** **83/83 = 100%** registros exatos catalogados; subbarra de fichas downstream nesta campanha **5/83 = 6,02%**. Mutadores por perks homologados **0** e sem denominador de demandas definitivo; percentual —%.
- **Prova causal nova:** [Java 21 SHA-exata #39504441297](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39504441297) `SUCCESS / 45 testes`; File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; gate `PASS_SHA_EXACT_WAVE_BOOLEAN_VALID_AND_UUID_NOT_ACTIVE`. O `Predicate` de `launchWave → getEntitiesOfClass(Class,AABB,Predicate)`, já associado por bootstrap a `lambda$launchWave$0`, prova dois desvios sobre `isValidTarget(A,B)` e `activeTargetIds.contains(B.getUUID())`, retornando verdadeiro somente com alvo válido e UUID não ativo. Fingerprint de **15 instruções / 2 branches / 1 ireturn**. Referência `maxTargets:I` é observada no corpo de `launchWave`, mas limite de buds não foi estabelecido por dataflow.
- **Pendências e segurança:** implementação de `isValidTarget` e identidade A/B, critérios PvP/equipe, resultado da consulta, ordenação por distância, `maxTargets` como gate quantitativo, criação de buds e área independente `FuneralBloomBudEntity.impact`, dano/cura, QA real cliente/provider-loaded/Survival/multiplayer, hook de mutação por player. **⛔ FAIL_CLOSED**, Stage 06.05 🟡 e Stage 09 físico PENDING conforme D035. Esta prova é estática e não promove Stage.

[Detalhes da seleção](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md) · [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).

## Continuação Somake — isValidTarget e maxTargets (20/10/2026; PR #844)

**Catálogo global de ações sobrenaturais:** **—%**, denominador final ainda desconhecido; conservar piso histórico >=1.856 objetos e discrepância 1.856/1.857 sob reconciliação. **Somake 1.0.9 identidades:** **83/83 = 100%**, registry físico SHA-exato. **Subbarra de fichas com auditoria downstream na campanha:** **5/83 = 6,02%**. Nenhum novo spell/método semântico independente foi adicionado; nenhuma perk mutadora homologada (**0**), percentual de demandas indeterminado.

- [Java 21 Somake SHA-exata #39507349822](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39507349822), **SUCCESS / 53 testes**, File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. `isValidTarget(LivingEntity,LivingEntity):boolean` possui 41 instruções, 9 invocações, 6 branches, 3 retornos; referencia `isAlive`, `isSpectator`, `isAlliedTo`, `distanceToSqr`, `getX/Y/Z` e `getRadius`. A semântica dos ramos permanece **NOT_PROVED**.
- `launchWave` contém 2 leituras `maxTargets:I` e 1 chamada ao construtor da bud, com 49 instruções da primeira leitura até a chamada. **A causalidade do cap quantitativo ainda não foi provada**; a mera coocorrência não homologa cardinalidade de buds.
- **Pendências mantidas:** owner/caster/candidato efetivos, corpo/branches de `isValidTarget`, defaults/caps de `maxTargets`, iteração/sort/seleção, spawn/impacto das buds, alcance real, dano/cura, física provider-loaded/cliente/Survival/multiplayer, hook mutador e autorização PvP/claims. ⛔ `FAIL_CLOSED`, Stage 06.05 🟡 e Stage 09 físico PENDING conforme D035. Nenhuma promoção, adapter ou runtime alterado.

[Dossiê dos consumidores](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md) · [ficha individual](../providers/✅-somake-spells/registry-1.0.9/funeral-bloom.md).

## Continuação Somake — três guardas de isValidTarget certificados (20/10/2026, PR #845)

**Global:** —%, piso conservador histórico `>=1.856` objetos semânticos, denominador final ainda aberto e divergência 1.856/1.857 ainda não reconciliada. **Somake 1.0.9:** 83/83 IDs físicos catalogados (100% de identidades); **5/83 = 6,02%** fichas com downstream na campanha. Nenhum novo ID, adapter ou hook mutador.

- [Auditoria SHA-exata Java21 #39511081176](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39511081176): `SUCCESS / 61 testes`, File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, gate `PASS_SHA_EXACT_NATIVE_ISVALIDTARGET_EARLY_GUARDS_AND_CFG`. A identificação dos **seis destinos** de desvio de `isValidTarget(LivingEntity,LivingEntity):boolean` foi fixada, incluindo **três rejeições causais comprovadas**: slot JVM 2 deve `isAlive()`, não deve `isSpectator()` e não pode ser a mesma referência de slot JVM 1. O método possui 41 instruções e três `ireturn`.
- ⚠️ **Pendente:** provar o significado e a fórmula dos três branches posteriores, owner/caster/candidato, `isAlliedTo`, `distanceToSqr`/alcance, `maxTargets` até cardinalidade de buds, construção/spawn real, `FuneralBloomBudEntity.impact` independente, dano/cura, modpack físico e API pública para modificadores.
- ⛔ `FAIL_CLOSED` para perks mutadoras; Stage 06.05 🟡 e Stage 09 físico PENDING. Esta prova estática **não** valida a experiência de jogo nem avança Stage. [Dossiê técnico](../providers/✅-somake-spells/EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md).
