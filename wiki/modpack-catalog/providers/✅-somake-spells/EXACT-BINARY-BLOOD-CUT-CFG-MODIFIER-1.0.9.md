# Somake Spells 1.0.9 — Blood Cut: fluxo normal do dano e fórmula do modificador

**Estado:** ✅ `EXACT_SHA_NORMAL_CFG` e `EXACT_SHA_FLOAT_RETURN_DATAFLOW` no classfile; ⚠️ conexão completa de argumentos em `onLivingDamage`, gameplay, host e QA; ⛔ nenhuma API mutadora de perk aprovada.

## Evidência física e reprodutibilidade

- Provider: Somake Spells, mod ID `somakespells`, release `1.0.9`, `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`.
- SHA-1 exato instalado/publicador: `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [GitHub Actions Java 21 #39552478074](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39552478074): **SUCCESS**, JAR validado por `sha1sum`; **38 testes sintéticos** no conjunto (7+9+5+10+7).
- Scripts clean-room: [CFG](../../../../docs/qa/somake_109_blood_cut_cfg.py), [testes CFG](../../../../docs/qa/somake_109_blood_cut_cfg_test.py), [dataflow float](../../../../docs/qa/somake_109_blood_cut_modifier_flow.py), [testes do dataflow](../../../../docs/qa/somake_109_blood_cut_modifier_flow_test.py).
- Classe compilada: `com.somake.somakespells.effect.blood.BloodCutEffect`. Nenhuma fonte upstream, bytecode bruto, JAR ou asset proprietário é exportado.

## Controle de fluxo normal — `onLivingDamage(LivingDamageEvent.Post)`

O grafo normal foi reconstruído usando destinos JVM verificados, sem usar valores de runtime para avaliar branches:

| Medida | Resultado compilado |
|---|---:|
| Instruções | 103 |
| Desvios `ifeq`, `ifeq`, `ifnull`, `ifne`, `goto` | 5 |
| Pontos terminais (return/throw, escopo dos opcode observados) | 2 |
| Chamadas sintáticas a `getNewDamage` | 1 |
| Chamadas sintáticas a `DamageSources.applyDamage` | 1 |
| Caminhos normais distintos chegando à chamada de `applyDamage` | 2 |
| Caminhos normais distintos que a evitam | 3 |

Duas transferências condicionais saltam diretamente para a saída sem passar pelo dano secundário; outra condição possui saída sem dano em uma de suas alternativas. As demais opções convergem para a chamada de dano. **Este é um número de caminhos no grafo compilado, não uma probabilidade nem uma contagem de eventos disparados em jogo.** Não foram reconstruídos os predicados de cada condição nem a relação exata entre evento inicial e um eventual segundo evento do mesmo handler.

## Retorno numérico integral — `getDamageModifier(int, LivingEntity):float`

A interpretação de pilha JVM, incluindo o armazenamento local `fstore`/`fload`, derivou as **duas rotas** do `ifnonnull` até `freturn`:

```text
a = argumento int de getDamageModifier
e = argumento LivingEntity de getDamageModifier

factor = (e != null) ? BloodCutSpell.getEntityPowerMultiplier(e) : 1.0f
return (float)(a + 1) * factor * 0.1f
```

A expressão legível preserva a sequência compilada: **`iadd` → `i2f` → `fmul` (por factor) → `fmul` (por 0.1f) → `freturn`**. Há avaliação `float` em cada multiplicação; não substituí-la por aritmética `double` ou uma reorganização algébrica na implementação. O getter contém **19 instruções e dois desvios** (`ifnonnull`, `goto`) e não apresentou um clamp adicional nesse caminho de retorno.

**Limites:**

- O argumento inteiro `a` não foi causalmente vinculado nesta auditoria ao `MobEffectInstance.getAmplifier()`, embora o método de evento referencie ambos. Esse vínculo exige análise da ordem dos operandos no callsite.
- O retorno é um **modificador**; não é o dano causado, nem revela sozinho a multiplicação por `getNewDamage`, limites de invulnerabilidade, lifesteal, resistência, evento recursivo, arredondamento final ou tratamento de dano por outros mods.
- A função `BloodCutSpell.getEntityPowerMultiplier(e)` é externa a este getter; sua fórmula e limites não foram abertos aqui.
- O valor da configuração efetiva, a elegibilidade, os efeitos de um alvo e a identidade de cast/owner ainda dependem do host e de testes de servidor/cliente.

## Integração e estado

Uma perk de RPG Skill Tree que multiplicasse o retorno nativo sem hook real poderia duplicar o processamento do `LivingDamageEvent.Post`; portanto, nenhuma bridge foi implementada: **⛔ FAIL_CLOSED**. Iron's mantém custos, cooldown e pipeline de cast; Somake mantém a lógica do efeito; Black Arcana mantém apenas o próprio runtime mágico.

**Próximos gates:** provar na pilha JVM que o amplificador lido e a entidade da fonte alimentam `getDamageModifier`; caracterizar os predicados de saída do handler, filtros de fonte, prevenção de proc-chain, lifesteal, dano subsequente e compatibilidade em multiplayer. Então comparar com a configuração host da versão física e executar QA no modpack.

**Impacto no catálogo:** +0 identidades, +0 adapters; Somake 83/83 IDs registrados, 8/83 no recorte de auditoria de métodos, sem promover o numerador downstream aprofundado de 5/83. Global —% (piso semântico >=1.856, denominador ainda aberto). Stage 06.05 🟡, Stage 09 físico pendente.
