# Epic Fight 21.17.3.1 — propriedades de AttackPhase no classfile exato

**Prova posterior dos consumidores:** ✅ [Java21 #39096586191](EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md) confirmou no JAR físico publicado a ordem dos acumuladores de `ValueModifier`, os callsites de `AttackAnimation`, `EpicFightDamageSource` e o método de absorção do mixin `MixinLivingEntity`. A presente ficha permanece prova dos **argumentos do builder**, enquanto o novo dossiê cobre referências do **consumidor**; nenhum dos dois executa um hit no jogador.


**Atualização posterior: ✅ [linkagem do registry em bytecode Java21 #39095049311](EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md)**, com `<clinit>` + `BootstrapMethods` ligando os IDs das três skills às lambdas `$40/$42/$43`, `PASS_BOUNDED_TRIDENT_REGISTRY_BOOTSTRAP_LINKAGE`, 10/10 autotestes. A ressalva de linkage não demonstrado abaixo corresponde ao gate original isolado e foi suprida por esta prova nova; sem promover gameplay ou hook.

**Checkpoint:** 18/10/2026. ✅ `EXACT_PUBLISHER_COMPILED_SUPPLIER_PROPERTY_CALLSITES` para os três métodos estáticos selecionados em `EpicFightSkills`. A prova certifica sequências *de construção de propriedades*, não resultados de dano/armor bypass, aplicação de um golpe, seleção efetiva de animations, consumo de recurso, compatibilidade de addons nem API para perks.

## Autoridade e execução

- Fonte física histórica do RPG Skill Tree: linha #260, JAR `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`, mod ID `epicfight`; publisher CurseForge projeto 405076 / arquivo 8175609.
- [GitHub Actions #39094435160](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39094435160), `exact_skill_parameters` **SUCCESS**: o workflow exige SHA-1 **`fb199b7bbea2fc402da28ab586e73f47e32f8fc0`** e SHA-256 **`8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`** antes do `javap`. O JAR possui 8.578.288 bytes no registro já certificado.
- Etapa nova: **11/11** autotestes e `PASS_BOUNDED_TRIDENT_ATTACK_PHASE_PROPERTIES`, `deviations=[]`; mesmo run também reportou **21/21** testes do comparador de JSON/símbolos, **10/10** testes de ordem de método e **9/9** do gate de ações sobrenaturais. O artefato JSON **#12124346492** contém provas read-only, sem redistribuir o JAR.
- [Verificador novo](../../../../docs/qa/epicfight_211731_trident_attack_phase.py) e [workflow Java 21](../../../../.github/workflows/epicfight-211731-perk-binary.yml). Os testes negativos rejeitam alterações de coeficiente, property key, `ValueModifier` factory, tipo de stun, tag, número de grupos, identidade de lambda, ramo condicional, ausência de build ou vínculo de animação.

## Resultados compilados (construção de objetos, sem gameplay)

| Habilidade já catalogada | Method supplier em `EpicFightSkills` | Sequência exata delimitada |
|---|---|---|
| `epicfight:wrathful_lighting` | `lambda$static$40` → retorno `WrathfulLightingSkill` | Grupo 1 `MAX_STRIKES_MODIFIER ← ValueModifier.setter(1.0f)`. Grupo 2 `DAMAGE_MODIFIER ← ValueModifier.setter(8.0f)`, `MAX_STRIKES_MODIFIER ← ValueModifier.setter(3.0f)`, `ARMOR_NEGATION_MODIFIER ← ValueModifier.adder(100.0f)`, `STUN_TYPE=KNOCKDOWN`, `SOURCE_TAG` contém `WEAPON_INNATE` |
| `epicfight:tsunami` | `lambda$static$42` → retorno `ConditionalWeaponInnateSkill` | Um grupo `ARMOR_NEGATION_MODIFIER ← ValueModifier.adder(100.0f)`, `SOURCE_TAG` contém `WEAPON_INNATE`, `STUN_TYPE=KNOCKDOWN`; existe vínculo do builder com `setAnimations` |
| `epicfight:everlasting_allegiance` | `lambda$static$43` → retorno `EverlastingAllegiance` | Um grupo `ARMOR_NEGATION_MODIFIER ← ValueModifier.adder(30.0f)`, `DAMAGE_MODIFIER ← ValueModifier.multiplier(1.4f)`, `SOURCE_TAG` contém `WEAPON_INNATE`, `STUN_TYPE=HOLD` |

**Como a prova opera:** identifica exatamente um método compilado por nome de lambda e tipo retornado; percorre seus opcodes em ordem, rejeita fluxos de branch inesperados, valida o número de grupos `newProperty`, compara todas as chaves `AttackPhaseProperty` na ordem encontrada e exige adjacência `getstatic property → carga float → invokestatic ValueModifier.{setter|adder|multiplier} → invokevirtual Builder.addProperty`. Valida a ligação imediata dos enums de stun, presença da tag antes do `addProperty`, `Builder.build` e `setAnimations` quando aplicável. Isto demonstra o argumento **do builder**; não é análise formal genérica de todos os fluxos Java nem confirmação de valor final depois da animação.

## Limites e implicações para perks

- **Dano:** `setter(8.0)` ou `multiplier(1.4)` são `ValueModifier` de propriedade de fase, não uma medida de dano a HP. Para uma perk de tipo de dano ou bônus percentual líquido, identificar a aplicação real no `AttackAnimation`, os cálculos do `EpicFightDamageSource`, combinação de outros modifiers, i-frames e flags de PvP/claims em dedicated server.
- **Armadura:** `adder(100)` é entrada para `ARMOR_NEGATION_MODIFIER`, não confirmação de exatamente 100% de penetração, nem autorização para aplicar dano paralelo por Black Arcana.
- **Alvo, AOE, range, hitbox, velocidade/tamanho de projétil, duração e cooldown:** **NÃO VERIFICADO**. Nenhum desses campos está garantido pelo verificador.
- **Recurso:** os três JSONs físicos já comprovados têm `consumption=50/50/40`; nenhuma unidade ou débito real é inferida.
- **Controle causal:** animações, múltiplas phases, hits, raio e recall pertencem a uma única ativação provider-owned, e não geram automaticamente casts adicionais ou progressão no sibling.
- **Identidade:** o método supplier é identificado por classe de retorno e nome sintético observado no binário; o probe atual não faz reconstrução completa de bootstrap/`invokedynamic` ligando cada lambda ao field registry no `<clinit>`. A identidade do registro de 43 skills, o seletor do tridente e os três JSONs foram demonstrados em provas independentes. Não afirmar que o linkage bootstrap foi validado por este gate.
- **Runtime:** nenhum `ServerPlayerPatch.initialized=true` de jogador conectado, equip/unequip, efeitos de chuva/raio/recall, danos, transação de `WEAPON_CHARGE`, Mastery ou adapter foi validado por esta inspeção.

## Contrato de autoridade

Epic Fight possui skill, seleção do moveset, `AttackPhase`, `ValueModifier`, animação, dano/hit, gauge e entidade de tridente. RPG Skill Tree fornece progressão/perks/Mastery **apenas por boundary real**, e Black Arcana controla seu próprio casting, custos, hazards e `WorldEffectPolicy`. Não reproduzir efeitos nem criar uma segunda etapa de consumo de recurso.

**Inventário inalterado:** 43/43 identidades core, 3/3 sobrenaturais do tridente (`COUNTED_EXACT`) e 40 não mágicas relevantes para perks; +0 magias, +0 adapters. Global mínimo 1.857 objetos semânticos / 1.855 estritos, denominador final aberto; Stage 06.05 🟡 e Stage 09 físico pendente, PR #825 draft.

Referências anteriores: [trident selector, JSON e ingressos](EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md), [fichas individuais](actions/SUPERNATURAL-ACTION-CARDS.md), [fonte pública adjacente 21.17.3](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L337-L371).
