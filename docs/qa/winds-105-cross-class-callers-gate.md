# Wind's Spellbooks 1.0.5 — arestas entre classes e consumidores dos getters

**Data:** 24/10/2026 · **Estado:** 🟡 auditoria binária em andamento. Nenhuma perk implementada.

## Fonte física e escopo

- Modlist do RPG Skill Tree: Wind's Spellbooks `wind_spellbooks-1.0.5.jar` (posição 571); host Iron's Spells 3.16.3 (posição 342) e IronSable X Wind's 1.0.0 (posição 345). A fonte efetiva é a modlist física do repositório sibling; não extrapolar para outras versões.
- SHA-1 congelado do JAR `8744886899bc245ae147a44baa2b183689cec7da`, verificado antes de inspecionar classes. A fonte de evidência é o **artefato JSON** do GitHub Actions; nunca publicar o JAR nem instruções ou código de terceiros.
- PR #884 provou invocações diretas de nove getters **dentro** das sete classes de spell. A nova campanha visita todos os `.class` sob `net/raptorzizi/wind_spellbooks/` do **mesmo JAR físico**, incluindo classes de efeito, entidade e outras classes internas do provider.
- A enumeração de classes deriva do ZIP oficial com bounds e validação de integridade. O scanner percorre cada classe com `javap -c -p` e seleciona somente `invokevirtual`, `invokespecial`, `invokestatic` e `invokeinterface` com referência JVM verificável e descritor exato para os nove getters já rastreados.

## Perguntas técnicas

1. Há **referências diretas entre classes** aos métodos `TailwindSpell.getPercentAirSpeed`, `getPercentJump` ou `AeropicSpell.getRecastCount`? Registre o nome completo e o método do chamador somente se estiverem explícitos no JAR.
2. As invocações dos getters de Almighty Push, Iron Slash, Tornado e Wind Jump permanecem nas classes declarantes ou existem outras classes do mesmo provider com chamadas diretas?
3. O inventário de nove getters do PR #884 continua reproduzível? Qualquer divergência nas chamadas diretas já homologadas, classe ausente, ZIP truncado ou falha na inspeção encerra com `FAIL_CLOSED`.

## Limites: prova positiva, não exclusão absoluta

- Nenhuma chamada entre classes encontrada significa apenas **zero chamadas JVM diretas correspondentes dentro das classes do namespace examinado nesta versão do JAR**. Não significa ausência de consumidores no Iron's, IronSable, código herdado, Mixin, evento, reflexão, método virtual ou `invokedynamic`.
- A chamada a um getter não prova que seu retorno chegue ao parâmetro aplicado no mundo. Para provar `getter → argumento → setter`, falta a pilha/CFG, os guardas, unidades, host e efeitos de lifecycle. `onCast` e `getUniqueInfo` não conferem direitos para mutar a magia.
- Um percentual getter referido apenas por `getUniqueInfo` não implica que o efeito Tailwind seja somente cosmético. Investigar classes `MobEffect` e código do host antes de decidir.
- Black Arcana mantém autoridade sobre o próprio runtime; Wind's/Iron's mantêm os efeitos e recursos provider-native. RPG Skill Tree fornece progressão por contrato real. Nenhum hook de perks está aprovado; `SEM_HOOK_SEGURO`.

## Critérios de aceite

- Onze testes sintéticos positivos/negativos abrangem descritor exato, owner totalmente qualificado, shorthand de classe própria, chamada incorreta, reflexão não contada, universo incompleto e drift dos nove getters.
- Workflow Wind do GitHub Actions valida o SHA físico e o scanner, grava `cross-class-getter-calls.json` e publica exclusivamente metadados clean-room.
- Somente depois do CI com JAR exato e inspeção do JSON é permitido atualizar as fichas individuais e registrar a contagem de classes e chamadas diretas. Não usar números supostos.
- CI Black Arcana (`verify`, `stage05_qa_companion_smoke`) e Wind precisam de `SUCCESS` no HEAD final; conferir 0 commits behind e diff antes de merge.

Sem novas identidades: **7/7** fichas Wind's; **9/9** getters selecionados; **38/39** campanha binária geral selecionada; mínimo ≥1.856 objetos e progresso global indeterminado. Stage 06.05 🟡 e Stage 09 pendente.
