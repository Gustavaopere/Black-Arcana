# Wind's Spellbooks 1.0.5 — efeitos, movimentos e registries

**Estado 🟡: aguardando prova no JAR exato pelo CI deste PR.** Isto não é um novo mod, spell, adapter nem autorização de perk mutadora.

## Contexto físico e recorte

- Versão instalada da modlist sibling: `wind_spellbooks-1.0.5.jar`, mod ID `wind_spellbooks`, SHA-1 congelado `8744886899bc245ae147a44baa2b183689cec7da` (posição 571). Iron's Spellbooks host `irons_spellbooks-1.21.1-3.16.3.jar` e IronSable X Wind's `ironsable-wind-1.0.0.jar` são dependências/sibling providers distintos; não são automaticamente incluídos na inspeção.
- A auditoria anterior verificou 64 classes do JAR oficial, nove getters escalares selecionados e 16 `invoke*` diretos aos getters (zero a partir de outra classe no mesmo JAR). A ausência de chamada direta não explica o comportamento dos efeitos.
- O novo scanner `docs/qa/winds_105_effect_boundaries.py` percorre todas as `.class` do namespace físico Wind's, aproveitando a verificação ZIP/SHA exata já homologada.

## Perguntas semânticas e limites

1. Quais classes no JAR têm nomes associados a `Tailwind`, `Acrobatics` ou `Effect`? **Nome é apenas indicador de candidato**: não prova registration, listener, efeito ativo, hook nem atributo efetivo.
2. Quais métodos possuem referências diretas aos campos `TAILWIND` ou `ACROBATICS` do registry observado? Qual o método de origem e se ele é `onCast`, `tick`, `applyEffectTick` ou um helper?
3. Em candidatos de efeito, quais assinaturas e símbolos JVM sugerem possíveis operações de velocidade, salto, queda, atributo, impulso, dano, tick e remoção? Relatar métodos, campos, chamadas e famílias de operadores, sem copiar implementação nem atribuir argumentos.

## Prova admissível

- `onCast` de `TailwindSpell` lê o campo `TAILWIND` e o de `AeropicSpell` lê `ACROBATICS`: isso é **prova de referência JVM ao registry**, não de qual instância `MobEffect`/classe é retornada ou de como seu modificador funciona.
- `javap -c -p` é usado apenas para obter metadados simbólicos de método/campo/opcode, publicando **somente JSON de inventário**. Sem source/copiar asset/disassembly ou JAR proprietário.
- O scanner usa `CANDIDATE_AND_OR_REGISTRY_REFERENCE_ONLY`; `runtime_effect_settlement` é sempre `NOT_PROVEN` sem host/provider execution. Nenhum ponteiro de API de perks decorre de nomes.
- Falha de SHA, classe/roster, referência onCast esperada, duplicidade, erro do scanner ou método fora do limite de output deve falhar fechado.

## Gates de integração

- Rodar os testes sintéticos de proveniência, a varredura no JAR exato e inspecionar o artefato JSON. Só depois registrar fatos nas fichas `tailwind.md` e `aeropic.md`, distinguindo `name-candidate`, `direct-field-ref` e o que permanece `NOT_PROVEN`.
- `Black Arcana CI` (`verify` e `stage05_qa_companion_smoke`) e `Wind's exact-JAR` no HEAD final devem ser `SUCCESS`; reconciliar o PR com a `main` atual antes do merge.
- Nenhum Stage promovido: `06.05` 🟡 para aceitação física, `09` pendente; runtime Black Arcana próprio, RPG Skill Tree apenas provider progressão/gates; nenhum hook mutador da Wind implementado.
- Denominadores independentes e preservados: catálogo Wind's **7/7 magias**; getters previamente selecionados **9/9**; campanha binária **38/39**; global **—%**, ≥1.856 objetos.
