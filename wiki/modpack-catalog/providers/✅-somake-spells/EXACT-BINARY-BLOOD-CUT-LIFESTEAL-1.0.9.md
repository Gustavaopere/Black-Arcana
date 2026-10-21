# Somake Spells 1.0.9 — Blood Cut: argumento de lifesteal no damage source

**Certificado:** ✅ `SHA_EXACT_NATIVE_SETTER_0.15F`. **Não certificado:** ⚠️ cura aplicada, receita/config do host, teto, modificadores por jogador. **Perks mutadoras:** ⛔ FAIL_CLOSED.

## Artefato e reprodutibilidade

- Magia: `somakespells:blood_cut`.
- Provider: Somake Spells `1.0.9`, mod ID `somakespells`.
- Artefato: `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`, SHA-1 físico/publisher **`171841ac9f802be9309ecc166c1d972ac6d404c0`**.
- [GitHub Actions Java 21 #39594615862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39594615862) **SUCCESS**: **51 testes sintéticos** (7+9+5+10+10+10), incluindo regressões estritas de mutação no float, tipo da assinatura, duplicação de calls e precedência. O JAR foi confrontado a `sha1sum --check`.
- Inspeção clean-room: [verificador exato](../../../../docs/qa/somake_109_blood_cut_lifesteal.py), [testes](../../../../docs/qa/somake_109_blood_cut_lifesteal_test.py) e [workflow](../../../../.github/workflows/somake-109-blood-cut-refs.yml). Sem exportar JAR, método bruto, classfile ou material autoral do provider.

## Sequência causal provada no método

Classe: `com.somake.somakespells.spells.blood.BloodCutSpell`.

Método auditado: `getDamageSource(Entity, Entity):SpellDamageSource`. O método contém **7 instruções JVM**, nenhum desvio condicional reportado e retorno `areturn`. Entre as referências de método verificadas:

| Índice de instrução no método | Prova de bytecode compilado | Implicação |
|---|---|---|
| 3 | Chamada a `AbstractSpell.getDamageSource` | Fonte-base delegada ao host Iron's |
| 4 | Instrução `ldc` carregando **float `0.15f`** | Carrega o valor literal diretamente no topo da pilha JVM |
| 5 | Chamada a `SpellDamageSource.setLifestealPercent(float)` | Consome o `0.15f` colocado imediatamente antes; nenhuma instrução intermediária o altera |
| 6 | `areturn` | Método devolve referência a objeto, sem adicionar processamento posterior nesse método |

A inspeção estrita rejeita se o literal, a posição, o setter tipado, os callsites ou o tamanho do método deixarem de coincidir com essa versão física.

**Prova certificada:** Blood Cut **passa `0.15f` ao setter de percentual de lifesteal do damage source**. Se o host interpretar o valor como fração convencional, o parâmetro nominal equivaleria a 15%; a equivalência numérica é hipótese de interpretação do host, não comprovação de cura real.

## Implicações e limites para perks

Esta evidência permite catalogar o valor fixo de configuração do `SpellDamageSource` na classe da magia. Não demonstra:

- que o dano secundário do `LivingDamageEvent.Post` execute sempre ou chegue ao host;
- como `DamageSources.applyDamage` aplica a origem, qual evento é gerado, qual entidade recebe cura e qual regra o host usa para o setter;
- tratamento de resistências, PvP, invulnerabilidade, cancelamentos, caps ou persistência;
- se há uma API de mutação de `lifesteal` por caster sem substituir a autoridade do provider;
- qualquer custo, cooldown ou Mastery extra.

**Consequência:** ainda é inseguro implementar uma perk que aumente lifesteal por substituição ou reaplicação de dano. Tratar modificadores externos como ⛔ FAIL_CLOSED até contrato real com o Iron's e causalidade comprovada de caster/target/proc.

Complementa o [dossiê de CFG e `getDamageModifier`](EXACT-BINARY-BLOOD-CUT-CFG-MODIFIER-1.0.9.md), o [dossiê de evento](EXACT-BINARY-BLOOD-CUT-EVENT-1.0.9.md) e a [ficha individual](registry-1.0.9/blood-cut.md).

## Progresso

**+0** novas identidades semânticas, **+0** adapters, **+0** hooks de perk. Mantêm-se os recortes anteriores: Somake **83/83 IDs** registrados, **8/83** fichas com auditoria estática aprofundada no recorte documentado, **5/83** na campanha downstream anterior. Catálogo global técnico **—%** (denominador aberto; piso **≥1.856** objetos). Stage 06.05 🟡 e Stage 09 físico pendente.

## Correlação com dano secundário (atualização de 21/10/2026; PR #862)

A [auditoria do callsite #39604864087](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39604864087) revelou **sobrecarga diferente** no handler `onLivingDamage`: este chama `BloodCutSpell.getDamageSource(Entity)` com **um** argumento, enquanto o setter `setLifestealPercent(0.15f)` auditado neste dossiê pertence a `getDamageSource(Entity,Entity)` com **dois** argumentos. Não foi demonstrado encadeamento/dispatch entre os métodos. **Não associar o `0.15f` à fonte efetiva do dano secundário sem prova específica do host.** [Novo dossiê de argumentos](EXACT-BINARY-BLOOD-CUT-APPLY-DAMAGE-1.0.9.md).
