# Wind's Spellbooks 1.0.5 — BootstrapMethods e supplier→registry→holder

**Data:** 24/10/2026 · **Estado:** ✅ associação compilada de duas entradas de registry comprovada; ⚠️ execução runtime e callbacks/hook continuam pendentes.

## Recorte físico e autoridade

- Fonte física: modlist do sibling RPG Skill Tree. JAR `wind_spellbooks-1.0.5.jar`, mod ID `wind_spellbooks`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; host Iron's Spells 3.16.3 e IronSable X Wind's 1.0.0 são providers externos distintos.
- PR #888 documentou `AeropicEffect` e `TailwindEffect` como classes compiladas; `ModMobEffectRegistry` apresenta campos `ACROBATICS` e `TAILWIND`, strings `aeropic` e `tailwind`, dois `invokedynamic`, e factories `lambda$static$0`/`lambda$static$1`. O **binding** ainda não estava demonstrado.
- O novo scanner `docs/qa/winds_105_bootstrap_registry_trace.py` valida primeiro o JAR exato, as cinco classes/ABI e o contrato do PR #888, antes de executar `javap -v -c -p` **somente em `ModMobEffectRegistry`**.

## Contrato de prova

Uma aresta compilada `Supplier → DeferredRegister.register → DeferredHolder` só pode ser declarada quando todos estes itens são simultaneamente confirmados, no mesmo método `<clinit>` e em fluxo contíguo de cinco instruções JVM:

1. Recepção de objeto com o tipo JVM exato `DeferredRegister` via `getstatic`.
2. Chave constante `ldc String aeropic` ou `ldc String tailwind`.
3. `invokedynamic` com descritor de `Supplier` e índice de bootstrap verificável.
4. Chamada com assinatura JVM exata `DeferredRegister.register(String, Supplier): DeferredHolder`.
5. Armazenamento do resultado com `putstatic` no campo `ACROBATICS` ou `TAILWIND` do tipo `DeferredHolder`.

Além da contiguidade, o índice no atributo `BootstrapMethods` precisa apontar para o factory method correto, cujo método já foi inspecionado no JAR e constrói a classe de efeito correspondente. O teste rejeita alterações de tipo, chave, índice, factory, field, opcode, duplicidade ou instruções extras na janela. **Se o bytecode real não atender à gramática restrita, encerrar com `FAIL_CLOSED` e ampliar a prova com análise de pilha rigorosa, nunca completar lacunas por inferência.**

## Limites de interpretação

- Mesmo uma associação compilada comprovada do `Supplier` ao `DeferredHolder` não é validação de execução real do registro, carregamento de cliente, invocação de `MobEffect`, lifecycle ou dos bônus numéricos.
- Não comprova o dispatch virtual de `AbstractSpell.getRecastCount` ao override Aeropic, nem titularidade de hooks de RPG Skill Tree.
- Sem runtime e QA físico, perks mutadoras de recast, movimento, salto e fallDistance seguem **⛔ SEM_HOOK_SEGURO**, sem duplicar efeitos do Iron's/Wind's. Black Arcana mantém autoridade apenas sobre o seu runtime.
- Este recorte não aumenta a população de **7/7 magias Wind's**, **9/9 getters selecionados**, **38/39 identidade binária selecionada** ou global mínimo **≥1.856**. Denominador global permanece —%. Stage 06.05 🟡, Stage 09 físico pendente.

## Validações exigidas

Doze testes sintéticos de prova positiva/fail-closed, execução do JAR SHA-exato em Java 21 e revisão do artifact JSON `bootstrap-registry-trace.json`. Atualizar as duas fichas somente com evidência verificada. Concluir CI especializado e Black Arcana CI (`verify` + `stage05_qa_companion_smoke`) no HEAD final; verificar `main`, diff e branch antes de merge.

### Critério de leitura da tabela de bootstrap

Em classes Java com lambda `Supplier`, o *bootstrap method handle* aponta para `java/lang/invoke/LambdaMetafactory.metafactory`. **O alvo da lambda deve ser resolvido a partir dos argumentos `Method arguments` desse bootstrap**, em um `REF_invokeStatic` único que referencia o método `lambda$static$N` da própria classe `ModMobEffectRegistry`. O parser não usa o método `metafactory` como factory de efeito; qualquer ausência, ambiguidade ou classe incorreta é `FAIL_CLOSED`.

## Resultado binário confirmado e limites — 24/10/2026

Fonte: [Wind CI #40143051496](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40143051496), `SUCCESS`; `bootstrap-registry-trace.json` extraído e inspecionado do artefato `wind-spellbooks-105-methods`, SHA-1 do JAR `8744886899bc245ae147a44baa2b183689cec7da`. A validação confirmou **2/2** arestas estritas:

| Campo `DeferredHolder` | Key literal | Site `invokedynamic` | Alvo `REF_invokeStatic` do `BootstrapMethods` | Construção compilada da factory | Estado |
|---|---|---:|---|---|---|
| `ACROBATICS` | `aeropic` | `#0` | `lambda$static$0` | `new AeropicEffect` | ✅ ligação compilada |
| `TAILWIND` | `tailwind` | `#1` | `lambda$static$1` | `new TailwindEffect` | ✅ ligação compilada |

Cada cadeia compreende o `getstatic` do `DeferredRegister`, `ldc` da key, `invokedynamic Supplier`, a chamada `DeferredRegister.register(String, Supplier)` e o `putstatic` do holder, em sequência válida. O alvo lambda foi extraído de **`Method arguments` de `LambdaMetafactory.metafactory`**, não confundido com o próprio method handle de bootstrap. Os métodos auxiliares `lambda$static$0` e `$1` já tinham construtores de efeito confirmados no inventário anterior, revalidado pelo scanner.

**Mudança de classificação documental:** a associação **compilada** `registry→supplier→factory→holder` que era `NOT_PROVEN` no PR #888 passa para `PROVEN_BOUNDED_JVM_STACK_AND_BOOTSTRAP` nesta versão exata. Isso não significa `runtime_instance_registration` nem `client_gameplay_effect` executados: permanecem `NOT_TESTED`. `safe_mutating_hook` segue `NOT_PROVEN`. Nenhuma prova de despacho virtual Aeropic, progressão, magnitude de salto ou queda.

### Contract de imutabilidade documental

`winds_105_bootstrap_registry_contract.py` compara os dois campos, keys, sites, factory owner/target, JAR SHA-1 e escopo exato do resultado. Dez testes sintéticos de mutação rejeitam mudanças ou promoção indevida de runtime e hooks; o workflow verifica esse contrato **contra o artefato extraído do JAR** antes de publicar JSON. O scanner de BootstrapMethods tem doze testes de pilha/atribuição e fail-closed.
