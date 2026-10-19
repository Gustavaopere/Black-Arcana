# Somake Spells 1.0.9 — Funeral Bloom: dois caminhos tipados de `getRadius`

**Estado:** ✅ `EXACT_SHA1_TWO_PATH_JVM_RADIUS_RETURN` — fórmula de retorno JVM e origem do guard demonstradas; ⚠️ consumidores, geometria efetiva, atributos e gameplay não comprovados; ⛔ perks mutadoras `FAIL_CLOSED`.

## Proveniência e verificações

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`: Somake `somakespells-1.0.9-1.21.1.jar`, Minecraft 1.21.1/NeoForge/Java21; mod ID `somakespells`, CurseForge File 8867079, SHA-1 físico `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [Java21 #39259507432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39259507432): `SUCCESS`, 10 testes (positivos, negativos e fixture compilada Java21), 28 instruções do classfile real integralmente processadas pelo interpretador de caminhos, duas saídas tipadas `freturn`, um `ifnonnull` e um `goto`.
- [Parser de caminhos](../../../../docs/qa/somake_109_radius_typed_paths.py), [testes de regressão](../../../../docs/qa/somake_109_radius_typed_paths_test.py), [workflow SHA-gated](../../../../.github/workflows/somake-109-radius-typed-paths.yml). Snapshot negativo do HEAD subsequente exige que ambas as expressões e callsites permaneçam idênticos — revalidar no CI final.
- A [PR #834](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-IRONS-1.0.9.md) comprovou o CFG estrutural e a assinatura host `getSpellPower(int,Entity):float`; esta campanha acrescenta **prova tipada do valor retornado em cada caminho**, sem duplicar nenhuma identidade de spell.

## Condição exata do branch

Na entrada de `FuneralBloomSpell.getRadius(int,LivingEntity):float`, o valor cujo estado não nulo é testado pelo `ifnonnull` corresponde ao argumento local `caster` (`LivingEntity`). O parser acompanha a pilha, os slots e os dois sucessores, e rejeita qualquer outro sujeito, opcode não suportado, tipo incompatível ou caminho incompleto. O `caster == null` pula a chamada `SchoolType.getPowerFor`, enquanto `caster != null` referencia `getSchoolType()` e `SchoolType.getPowerFor(LivingEntity):double`.

## Fórmulas de retorno, preservando operações JVM

**Caster não nulo:**

```text
R = Mth.clamp_f32(
      (9.5f + (i2f(level) * 0.82f))
       + (Math.max_f32(0f, (d2f(schoolPower(caster)) - 1f)) * 0.65f),
      10.0f, 15.0f)
```

**Caster nulo:**

```text
R = Mth.clamp_f32(
      (9.5f + (i2f(level) * 0.82f))
       + (Math.max_f32(0f, (1f - 1f)) * 0.65f),
      10.0f, 15.0f)
```

Estas são representações legíveis das **expressões simbólicas de retorno do bytecode**. A operação de poder da escola retorna `double` e sua contribuição é convertida via `d2f`; `level` é convertido de inteiro via `i2f`. Os operadores e chamadas `Math.max(float,float)`/`Mth.clamp(float,float,float)` obedecem à semântica float32 da JVM; não redistribuir somas/multiplicações como equivalências de ponto flutuante arbitrárias. A apresentação algébrica simplificada para argumentos finitos é `clamp(9.5 + 0.82 L + 0.65 max(0,float(P)-1),10,15)` no ramo não nulo; no ramo nulo o adicional escolar vale zero.

| Dimensão de engenharia | Evidência | Estado |
|---|---|---|
| Nível | `i2f(level)` multiplicado por literal float `0.82` | ✅ coeficiente de retorno, não origem de Mastery comprovada |
| Poder escolar | ramo caster válido chama `getSchoolType`/`SchoolType.getPowerFor`, converte `double → float`, subtrai `1`, aplica `Math.max(0,...)` e multiplica por `0.65` | ✅ expressão simbólica, ⚠️ SpellPower/config/caps ativos desconhecidos |
| Casters ausentes | bônus escolar assume `1f` antes de subtrair `1f`, produzindo zero | ✅ caminho do retorno, ⚠️ se o provider de fato chama com caster nulo em jogo, não verificado |
| Clamp de retorno | argumentos finais float `10.0`/`15.0`, em ambos os caminhos | ✅ limite de retorno para entradas finitas, ⚠️ NaN e comportamento do helper em casos excepcionais não certificados |
| Unidades/área | getter nomeado `getRadius` | ⚠️ não demonstra blocos, AABB, raio de dano, quantidade de buds ou alcance de targeting |
| Mutação por jogador | nenhuma API/hook de perk testado | ⛔ `FAIL_CLOSED` |

## Clean-room, boundaries e pendências

Somente dados derivados de análise abstrata e assinaturas JVM entram no repositório. Sem código Java do provider, disassembly, sequência de bytecode, classfile, JAR ou assets. Esta prova estática não é evidência de Minecraft client/server carregado nem de efeito real atingindo entidades.

Próximas investigações: **consumidores** de `getRadius` na cadeia `FuneralBloomSpell → Controller → Bud`; origem efetiva de `SchoolType.getPowerFor` na versão do Iron's 3.16.3; config/atributos do jogador; colisão, AABB, world-safety, Mastery/dano/cura por evento. O Black Arcana mantém autoridade sobre seu runtime; o Somake sobre a magia provider-native; o Iron's sobre host/recursos; RPG Skill Tree participa apenas por contrato real.

**Catálogo:** permanece 83/83 identidades Somake no registry e 5/83 fichas com auditoria de entidades downstream. Este recorte não cria identidade de magia, classe nova, adapter, Stage completo ou QA físico. Stage 06.05 continua 🟡, Stage 09 condicionado sob D035.
