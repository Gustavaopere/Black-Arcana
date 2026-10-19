# Somake Spells 1.0.9 — Funeral Bloom: ponte de argumento float da controller

**Estado:** ⚠️ JAR exato auditado: o getter `getRadius():float` **não** corresponde à sequência direta `aload_0 → getfield → freturn`; portanto, o elo construtor → getter permanece **`NOT_PROVED`**. O próximo incremento coleta apenas um resumo estrutural do getter, ainda dependente do CI do HEAD final. ⛔ Nenhuma perk mutadora homologada.

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
