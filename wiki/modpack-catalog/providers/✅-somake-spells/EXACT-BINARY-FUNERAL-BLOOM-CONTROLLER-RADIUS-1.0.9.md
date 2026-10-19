# Somake Spells 1.0.9 — Funeral Bloom: ponte de argumento float da controller

**Estado:** 🟡 auditoria exata em andamento. Esta prova é restrita ao armazenamento do parâmetro `float` no construtor e ao retorno direto de `getRadius():float`, se ambos estiverem integralmente comprovados. Não concluir passagem de `Spell.getRadius` ou valor dos operandos de `AABB.inflate`.

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
