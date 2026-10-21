# Epic Fight 21.17.3.1 — consumidores compilados de AttackPhase e negação de armadura

**Preparação posterior de prova física:** ✅ [Java21/NeoForge #39098965924](NATIVE-PLAYER-DAMAGE-TELEMETRY-QA-21.17.3.1.md) compilou e armou em servidor sem cliente um companion passivo que aceita apenas `EpicFightDamageSource` originado por `ServerPlayer` conectado nos eventos `LivingIncomingDamageEvent` e `LivingDamageEvent.Post`. A execução certifica **prontidão de observação, não um ataque real**; `ARMOR`, `ABSORPTION` e `health_damage` permanecem sem samples e o handler não foi invocado experimentalmente.


**Prova runtime posterior, restrita:** ✅ [servidor dedicado #39098101364](EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md) detectou um handler `epicfight$getDamageAfterArmorAbsorb` com assinatura esperada **na classe `LivingEntity` transformada** (NeoForge 21.1.250, Epic Fight 21.17.3.1). A ressalva de injeção não observada abaixo é histórica ao workflow estático #39096586191: a **presença instalada** agora foi comprovada em servidor, mas **invocação efetiva no método-alvo, dano, amortecimento de armadura e cliente seguem não medidos**.


**18/10/2026 · ✅ `PUBLISHER_COMPILED_CONSUMER_METHOD_OPCODE_REFERENCES` delimitado · ⚠️ execução de combate/instalação do mixin não testadas · ⛔ bridges de perks/Mastery não autorizadas.** Este documento estende a cadeia [ID → supplier → builder](EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md), sem somar magias.

## Artefato, testes e reprodutibilidade

- Provider `epicfight`, publicação CurseForge 405076 / arquivo 8175609, JAR 21.17.3.1 de 8.578.288 bytes. O runner exige **SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`** e **SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`** antes do `javap`; não houve nova leitura do disco do usuário.
- [GitHub Actions Java21 #39096586191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39096586191) — job `exact_skill_parameters` **SUCCESS**, `PASS_BOUNDED_EPICFIGHT_ATTACK_PHASE_CONSUMERS`, `deviations=[]`, mais **8/8** novos autotestes fail-closed. Executados também os gates de JSON/registry, seleção sobrenatural, propriedades builder e bootstrap, todos com sucesso.
- Artefato JSON de evidências **#12124059084**; [verificador read-only](../../../../docs/qa/epicfight_211731_attack_phase_consumers.py) e [workflow](../../../../.github/workflows/epicfight-211731-perk-binary.yml). Sem redistribuição de JAR/código upstream; o script apenas examina métodos e opcodes públicos do JAR publicado.
- A validação recusa substituição de método, alteração de propriedade, mudança de sequência de operações e ausência de ramo de retorno. **Não** é interpretador JVM genérico, GameTest nem prova de injeção Mixin efetiva.

## Cadeia demonstrada por referências compiladas

| Ponto | Evidência em classfile | Consequência restrita |
|---|---|---|
| `ValueModifier$Adder.attach` | lê campo `ResultCalculator.add`, `fadd`, grava `add` | contribuições aditivas se acumulam |
| `ValueModifier$Multiplier.attach` | lê `ResultCalculator.multiply`, `fmul`, grava `multiply` | fatores se multiplicam |
| `ValueModifier$Setter.attach` | `Float.isNaN` e `Math.min`, duas vias `putfield ResultCalculator.set` | setters não são simplesmente somados: há regra de mínimo quando ambos são definidos |
| `ResultCalculator.getResult(float)` | `Float.isNaN`, seleção de `set`, `fadd` com `add`, `fmul` com `multiply` antes do `freturn` | computa com ordem set → adicionar → multiplicar |
| `AttackAnimation.getMaxStrikes` | `AttackPhaseProperty.MAX_STRIKES_MODIFIER` → `Phase.getProperty` → `Optional.map`, fallback a `LivingEntityPatch.getMaxStrikes` | modificador de máximo de strikes é uma **propriedade de fase**, não uma contagem certificada de hits reais |
| `AttackAnimation.getEpicFightDamageSource(DamageSource,...,Phase)` | busca, nessa ordem, `DAMAGE_MODIFIER`, `ARMOR_NEGATION_MODIFIER`, `STUN_TYPE` e `SOURCE_TAG`, usando `Optional.ifPresent` | há passagem condicional das propriedades; esta auditoria não prova, isoladamente, a tabela de method handles dos `Optional.ifPresent` |
| `EpicFightDamageSource.attachDamageModifier/attachArmorNegationModifier` | cada método envia o argumento ao `ResultCalculator.attach` do acumulador específico | dano e negação possuem acumuladores distintos |
| `EpicFightDamageSource.calculateDamageAgainst` | `modifiedDamageCalculator.getResult` precede processamento adicional de `extraDamages` | `DAMAGE_MODIFIER` não é o resultado HP final, nem inclui automaticamente os bônus extras |
| `EpicFightDamageSource.calculateArmorNegation` | `modifiedArmorNegationCalculator.getResult(baseArmorNegation)` | o 100/30 compilado dos builders é **entrada** para esse resultado, sujeita à base e a outros modifiers |
| `MixinLivingEntity.epicfight$getDamageAfterArmorAbsorb` | exige `EpicFightDamageSource`, consulta `DamageTypeTags.BYPASSES_ARMOR`, chama `calculateArmorNegation`, carrega `0.01f`, `fmul`, `Math.min`, chama `CombatRules.getDamageAfterAbsorb`, soma `fadd` e define `CallbackInfoReturnable` | percurso de mitigação **no método compilado**, sem prova de mixin aplicado em servidor/jogador |

## Expressões documentadas sem fabricar dano final

O source upstream pinado `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` fornece a interpretação semântica para a sequência compilada do `ResultCalculator`:

```text
base = valor inicialmente fornecido pelo host
set = valor do Setter (ou indefinido/NaN)
add = soma dos Adder
multiply = produto dos Multiplier
result = ((set se definido, senão base) + add) * multiply
```

**No método compilado de absorção de armadura**, para uma fonte `EpicFightDamageSource` **sem** `DamageTypeTags.BYPASSES_ARMOR`, o algoritmo equivale a:

```text
armorNegation = EpicFightDamageSource.calculateArmorNegation()
bypassPart = incomingDamage * min(armorNegation * 0.01, 1.0)
remaining = incomingDamage - bypassPart
remainingAfterArmor = CombatRules.getDamageAfterAbsorb(remaining, source, armor, armorToughness)
returnedDamageAtThisStage = bypassPart + remainingAfterArmor
```

A função `min` limita a fração pelo topo a 1 neste ramo; este verificador **não** demonstra um clamp inferior a zero e não extrapola para outros DamageSources. Não inferir um valor final de HP ou que todo impacto de `ARMOR_NEGATION_MODIFIER.adder(100)` seja sempre idêntico: base, outros modifiers, tags, regras de armadura, absorção, efeitos e eventos podem afetar a transação.

Referências upstream source-adjacent (21.17.3; fórmula também corroborada parcialmente no JAR físico 21.17.3.1): [`ValueModifier.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/api/utils/math/ValueModifier.java#L29-L131), [`AttackAnimation.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/api/animation/types/AttackAnimation.java#L283-L330), [`EpicFightDamageSource.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/world/damagesource/EpicFightDamageSource.java#L130-L147), [`MixinLivingEntity.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/mixin/common/MixinLivingEntity.java#L102-L113).

## Aplicação em fichas de skills e integração

| ID | Entrada de builder **exata** | Interpretação permitida | Gate não resolvido |
|---|---|---|---|
| `epicfight:wrathful_lighting` | `DAMAGE_MODIFIER.setter(8)`; `ARMOR_NEGATION_MODIFIER.adder(100)`; `MAX_STRIKES_MODIFIER.setter(1/3)` por grupo | fonte provider-native terá cálculo de dano e mitigação pelos consumidores compilados | não há dano HP ou hit cap medido, nem execução real de duas fases |
| `epicfight:tsunami` | `ARMOR_NEGATION_MODIFIER.adder(100)`, stun `KNOCKDOWN` | parâmetro entra no acumulador de negação e no ramo de absorção se a fonte satisfizer os guards | distância, AOE, alvo, animação real e valor de dano desconhecidos |
| `epicfight:everlasting_allegiance` | `DAMAGE_MODIFIER.multiplier(1.4)`, `ARMOR_NEGATION_MODIFIER.adder(30)`, stun `HOLD` | parâmetros de fase destinados ao cálculo provider-owned | dano final/retorno de tridente/quantidade de hits e custo não mensurados |

**Causalidade:** o Epic Fight mantém authority sobre `AttackPhase`, animações, `EpicFightDamageSource`, stamina/weapon charge, knockdown/hold e damage settlement. Não recriar hits, lightning ou damage source no Black Arcana e não conceder RPG Skill Tree Mastery por cada chamada do calculador. Modificar tipo de dano, targeting, alcance, collider, AOE, tamanho de projétil, duração ou cooldown continua **⛔** até um hook/provider boundary seguro e QA real.

**Gates físicos:** `ServerPlayerPatch.initialized=true` após conexão natural/respawn, `AttributeInstance` real, pipeline de hit/attack, `MixinLivingEntity` injetado, compatibilidade do modpack completo, observação de dano/custo e rollback/equip/unequip. Nenhum foi convertido em PASS por este job estático.

**Contagem:** Epic Fight ✅ 43/43 IDs core documentados, 3/3 raízes sobrenaturais já contadas, 40 habilidades não mágicas pertinentes a perks. **+0** magias e adapters. Global mínimo **1.857 semânticos / 1.855 estritos**, denominador integral desconhecido (**—%**). Stage 06.05 🟡; Stage 09 físico PENDING; PR #825 draft, sem merge.
