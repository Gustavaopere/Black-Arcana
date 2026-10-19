# Somake Spells 1.0.9 — Funeral Bloom: fórmulas e operandos numéricos do JAR exato

**Estado:** ✅ `EXACT_SHA1_NUMERIC_LITERAL_AND_BOUNDED_INT_DATAFLOW` para cinco getters; ⚠️ valores de outros métodos e aplicação em gameplay; ⛔ nenhum hook per-player/perk homologado.

## Provenance física e gates

- `somakespells-1.0.9-1.21.1.jar`, mod ID `somakespells`, CurseForge File `8867079`, SHA-1 publisher/modlist `171841ac9f802be9309ecc166c1d972ac6d404c0`; sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.
- [Java 21 / GitHub Actions #39201041605](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39201041605): **SUCCESS**, 15 testes (fixtures sintéticas, negativas e javac/javap 21), 4 classfiles e 17 métodos SHA-exatos.
- [Verificador](../../../../docs/qa/somake_109_numeric_fingerprint.py), [testes](../../../../docs/qa/somake_109_numeric_fingerprint_test.py), [workflow](../../../../.github/workflows/somake-109-numeric-fingerprints.yml). Emite somente os nomes/descritores de métodos selecionados, multiconjunto tipado de literais, histogramas de instruções, callsites limitados e fórmulas algébricas *apenas quando todo o fluxo linear do getter int é suportado*. Não exporta implementação, sequência de bytecode, pool de constantes, código fonte ou JAR.

## Fórmulas demonstradas de cinco getters

Defina **L = clamp(level, 1, 5)** para os quatro getters que usam `Mth.clamp`. O quinto, `getTelegraphTicks`, usa diretamente o parâmetro inteiro `level` e divisão inteira Java truncada em direção a zero (`jvm_idiv`). Os cinco métodos têm descritor `(I)I`, fluxo linear sem branch e operações reconhecidas até `ireturn` terminal. Estas são expressões de retorno **para os argumentos recebidos**, não garantias de invocação em jogo.

| Método | Expressão integral reconstruída de fluxo linear | level=1 | level=2 | level=3 | level=4 | level=5 |
|---|---|---:|---:|---:|---:|---:|
| `getMaxTargets(int)` | `4 + clamp(level,1,5)` | 5 | 6 | 7 | 8 | 9 |
| `getDuration(int)` | `240 + (clamp(level,1,5)-1)*20` | 240 | 260 | 280 | 300 | 320 |
| `getWaveInterval(int)` | `18 - clamp(level,1,5)` | 17 | 16 | 15 | 14 | 13 |
| `getWitherDuration(int)` | `60 + clamp(level,1,5)*12` | 72 | 84 | 96 | 108 | 120 |
| `getTelegraphTicks(int)` | `max(9, 13 - jvm_idiv(level,2))` | 13 | 12 | 12 | 11 | 11 |

**Limite semântico:** o verificador prova retornos numéricos do método compilado, com semântica Java de operações inteiras, incluindo divisão truncada para `getTelegraphTicks`. O `max(9,...)` desse getter não deve ser confundido com um teto de 9: é o piso da expressão matemática. O nome `level` é rótulo do parâmetro, não comprovação de origem em atributos/Mastery do RPG Skill Tree. `getDuration`, `getWaveInterval` e `getWitherDuration` retornam `int`; a conversão para ticks, aplicação efetiva, recasts, valores de config e consumidores downstream exigem investigação específica. Não confundir o `clamp(level,1,5)` com retorno final de duração de 1 a 5.

## Clamps de três argumentos com dois operandos literais consecutivos

O segundo verificador só certifica posições de operandos quando as **duas instruções imediatamente anteriores à chamada estática** de `Mth.clamp(FFF)F` ou `Mth.clamp(III)I` produzem diretamente os dois números; qualquer operação/conversão entre elas e o callsite bloqueia a certificação. Isso é evidência de argumentos passados à função, **não** de fórmula global nem de mutabilidade.

| Classe · método | Assinatura do clamp | Segundo argumento literal | Terceiro argumento literal |
|---|---|---:|---:|
| `FuneralBloomSpell.getRadius(int,LivingEntity)` | `Mth.clamp(FFF)F` | 10.0 | 15.0 |
| `FuneralBloomSpell.getMaxTargets(int)` | `Mth.clamp(III)I` | 1 | 5 |
| `FuneralBloomSpell.getDuration(int)` | `Mth.clamp(III)I` | 1 | 5 |
| `FuneralBloomSpell.getWaveInterval(int)` | `Mth.clamp(III)I` | 1 | 5 |
| `FuneralBloomSpell.getWitherDuration(int)` | `Mth.clamp(III)I` | 1 | 5 |
| `FuneralBloomImpactEntity.setScale(float)` | `Mth.clamp(FFF)F` | 0.65 | 1.6 |
| `FuneralBloomImpactEntity.getOpenProgress(float)` | `Mth.clamp(FFF)F` × 2 | 0.0 | 1.0 |

Em `getRadius` há **duas instruções de branch**, uma chamada `SchoolType.getPowerFor` e literais adicionais `0.65`, `0.82`, `9.5`, `1.0` além de `10.0`/`15.0`. **Não reconstruímos fórmula integral nem comprovamos se o resultado do clamp é sempre o valor final de alcance.** Em `setScale`, o par 0.65/1.6 passa diretamente ao clamp no classfile, mas não equivale a hitbox ou raio do dano.

## Literais adicionais sem fórmula certificada

| Método | Literais observados no próprio método | O que permanece pendente |
|---|---|---|
| `FuneralBloomSpell.getImpactDamage(int,LivingEntity)` | float `0.75`, `1.5`; 1 `fadd`, 1 `fmul`, `getSpellPower` referenciado | ✅ Fórmula JVM float do **retorno** comprovada na [auditoria seguinte](EXACT-BINARY-FUNERAL-BLOOM-FLOAT-DATAFLOW-1.0.9.md): `1.5f + (getSpellPower(level,caster)*0.75f)`; ⚠️ dano final/eventos/SpellPower reais ainda desconhecidos |
| `FuneralBloomSpell.getWitherAmplifier(int)` | int `0`, `1`, `5` e 2 branches | Tabela de ramificações, configuração de amplificador, caps finais |
| `FuneralBloomControllerEntity.tick` | float `0.01`, `0.025`, `0.035`, `0.07`, `0.16`, `0.38`, `0.52`, `0.82`, `0.85`, `1.55`, outros números, 12 branches | Cadência de ondas, custos por tick, eventos de entidades e unidade dos parâmetros sem dataflow completo |
| `FuneralBloomControllerEntity.launchWave` | double `0.34`, `0.35`, `0.55`, `0.62`, `2.0`, `2.8` e constantes adicionais; 6 branches | Geometria, variação aleatória, posição dos buds, quantidade e limites de world-safety |
| `FuneralBloomBudEntity.impact` | float `0.46`, `0.78`, `1.25`, `1.28`, `1.32`, `1.55`, `1.85`, `2.45`, `3.75`; double e int adicionais; 31 branches | Valores efetivos de dano/cura/Wither, raio de AABB, knockback, owner, branch de cada vítima e deduplicação |
| `FuneralBloomImpactEntity.getOpenProgress(float)` | float `0`, `1`, `4.0`, `5.0`, `7.0`; 2 chamadas clamp com argumentos literais 0..1 | Função integral visual, progresso e duração efetivos |
| `FuneralBloomImpactEntity.tick` | int `12`, 2 branches | Não declarar lifetime exato de 12 ticks sem provar o caminho de comparação/descarte |

Todos os números acima são **literais tipados do classfile**, não unidades de mundo, tempo ou balanceamento inferidas. O relatório JSON do workflow conserva o conjunto completo de valores por método; esta tabela traz apenas os sinais de maior interesse para perks.

## Contratos de engenharia e próximos gates

- ✅ `getMaxTargets`, `getDuration`, `getWaveInterval`, `getWitherDuration` e `getTelegraphTicks` possuem expressões JVM lineares demonstradas, independentes de hipóteses sobre jogabilidade.
- ⚠️ Para `getRadius`, permanecem 2 branches e callback de escola sem fluxo integral. Para `getImpactDamage`, o retorno float já foi certificado estaticamente na [auditoria seguinte](EXACT-BINARY-FUNERAL-BLOOM-FLOAT-DATAFLOW-1.0.9.md); a implementação efetiva de `getSpellPower`, consumo e dano sofrido por alvos ainda precisam de prova. Para `getTelegraphTicks`, o retorno matemático está provado, mas aplicação temporal em jogo ainda não.
- ⚠️ Para controller/bud/impact, ainda não é seguro inferir hitbox, cooldown, intervalo real de ataque, dano aplicado ou cura observada a partir de literais numéricos.
- ⛔ **FAIL_CLOSED:** um literal, uma fórmula de getter ou um setter interno como `setScale` não cria API pública de perk por jogador. Não sobrescrever casts, custos, cooldown ou dano nativo do Somake/Iron's nem duplicar Mastery por bud.
- ⚠️ Multiplayer, provider-loaded, real client, Survival, reload/NBT e modpack seguem sob D035; Stage 06.05 🟡 e Stage 09 condicionado.

**Catálogo:** `somakespells:funeral_bloom` continua uma única identidade entre 83; a campanha cobre 4 classfiles usados neste probe numérico, sem acrescentar nenhuma magia. Fontes relacionadas: [ficha individual](registry-1.0.9/funeral-bloom.md), [controller/bud](EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md), [impact](EXACT-BINARY-FUNERAL-BLOOM-IMPACT-1.0.9.md).

## Extensão: retorno float de impacto (19/10/2026)

O [workflow #39243467444](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39243467444) realizou interpretação abstrata JVM estritamente linear de `getImpactDamage(int,LivingEntity)`: **`1.5f + (getSpellPower(level_input,caster)*0.75f)`**, com 0 branches e tipos checados. `getRadius` continua com **2 branches**, clamp 10.0f/15.0f e `NOT_PROVED` para fórmula integral. A prova não resolve eventos, HP efetivamente removido, escolaridade, targets, hook per-player ou a execução de consumidor. [Dossiê específico](EXACT-BINARY-FUNERAL-BLOOM-FLOAT-DATAFLOW-1.0.9.md).
