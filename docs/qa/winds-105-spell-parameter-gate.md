# Wind's Spellbooks 1.0.5 — método exato para aprofundar as 7 fichas

**Estado inicial:** 🟡 parser de método/operando proposto. **Não** declarar parâmetros causais extraídos nem gameplay validado antes do CI.

## Evidência já integrada e preservada

- Modlist sibling (NeoForge 1.21.1): `wind_spellbooks-1.0.5.jar`, mod ID `wind_spellbooks`, SHA-1 físico histórico `8744886899bc245ae147a44baa2b183689cec7da`.
- [CurseForge release 8485822](https://www.curseforge.com/minecraft/mc-mods/winds-spellbooks-irons-spells-n-spellbooks-addon/files/8485822), 459532 bytes; [auditoria anterior #38312284152](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38312284152) prova 7/7 campos/IDs estáticos sem provar métodos internos.
- Sete identidades: `wind_jump`, `tornado`, `iron_slash`, `aeropic`, `almighty_push`, `wind_blade`, `tailwind`. `ACROBATICS_SPELL` corresponde a `aeropic`, sem oitava magia.

## Recorte adicional e limites

- Nova inspeção usa `javap -c -p` (JDK 21) exclusivamente sobre os sete nomes de classe registrados, valida SHA-1 exato antes de qualquer inspeção e recusa JAR faltante, alterado ou com entradas duplicadas.
- Saída: nome/sig de método, consumidores simbólicos `invoke*`, literais candidatos organizados por método. Não preserva código-fonte, corpos de métodos, disassembly integral ou JAR no repositório.
- **Não converter literal em fórmula sem reconstruir fluxo**. Um `2.0f` dentro de `onCast` não prova dano, range, radius, duration, tamanho de projétil ou hook mutável por perk. Uma chamada a `setDeltaMovement` não comprova qual entidade ou vetor sem estudo de operandos.
- CI sintético cobre formato básico e fail-closed; auditoria publisher é separada, e um `PASS` só prova superfícies simbólicas e integridade física, não casting carregado/Survival.
- Após evidência real, atualizar cada uma das sete fichas em `wiki/modpack-catalog/providers/✅-winds-spellbooks/wind/` com campos efetivamente ligados a fonte/target/geometria/dano/duração/custos e marcar cada campo `NÃO VERIFICADO` quando faltar nexo causal.
- Não criar hooks de perks, duplicar efeitos provider-native, nem contabilizar novos feitiços. Iron's é authority de mana/cooldown/casting; Wind's Spellbooks é authority das sete implementações. RPG Skill Tree: progressão somente por contrato real. Black Arcana conserva runtime próprio.
- `Stage 06.05` 🟡, `Stage 09` físico ⚠️ PENDING. Barra global —% e 7/7 identidades existentes inalteradas.

## Infraestrutura reutilizável futura

- [minecraft-mod-factory](https://github.com/Gustavaopere/minecraft-mod-factory) permanece candidata para padronizar validadores/esquemas de evidência. É infraestrutura compartilhada, **não** runtime de casting, provider instalado, nova dependência ou fonte de verdade das spells específicas. Sem migração/cópia nesta tranche.

## Ampliação do inventário de dependências — 24/10/2026

O scanner acrescenta, **em cada método já inventariado**, `read_fields` (`getfield`/`getstatic`), `written_fields` (`putfield`/`putstatic`), `numeric_opcodes` (aritmética/conversões explícitas) e `branch_opcodes` (`if*`/`switch`). Cada conjunto contém apenas símbolos ou nomes de instruções; **não** reconstrói fluxo de pilha, argumentos, beneficiário, escala, guardas ou fórmula.

Exemplo de inferência **proibida**: observar `getfield radius:F` e `fadd` no mesmo método e declarar uma fórmula para o raio. A causalidade desses operandos permanece `NÃO VERIFICADA`. Não há novo hook homologado, nova identidade mágica, alteração do runtime ou mudança na barra 7/7; integrações seguem `SEM_HOOK_SEGURO` até QA e contrato provider-native.

Os testes sintéticos verificam a separação por método, acesso de leitura/escrita e comentários ausentes; o workflow existente testa separadamente o JAR oficial exato (SHA-1 congelado) e publica apenas o JSON clean-room. **Somente a execução final do CI pode promover esta inspeção para evidência binária executada.**

## Próxima prova: análise da pilha para getters escalares — 24/10/2026

**Estado: ✅ expressão de quatro getters exatos confirmada pelo CI #40124346655, sem validação de gameplay ou hook mutador.** Quatro métodos selecionados, sem alterar o inventário 7/7:

- Aeropic `getRecastCount(int, LivingEntity)` — recasts.
- Almighty Push `getDuration(int)` — retorno inteiro com nome de duração.
- Tornado `getDuration(int)` — retorno inteiro com nome de duração.
- Wind Jump `getFloatDuration(int, LivingEntity)` — retorno inteiro com nome de duração.

O arquivo `docs/qa/winds_105_getter_formulas.py` revalida o JAR no SHA-1 físico fixado pelo scanner anterior e lê somente símbolos da classe correspondente. Interpreta, de forma conservadora, carregamentos locais, constantes numéricas, casts, aritmética escalar, `java/lang/Math.max(II)I` e retorno do método. Os demais opcodes, efeitos colaterais, branches e chamadas desconhecidas retornam `UNRESOLVED`. A saída é **AST aritmética**, não decompilação/cópia da implementação.

Uma expressão exata de getter não comprova escala efetiva no jogo: ainda faltam unidade dos parâmetros, condições de invocação, amplificadores, configuração, bounds upstream/downstream, target, network e lifecycle. Em particular, `getRecastCount` não comprova a janela/recast consumido; `getDuration` não comprova ticks sem verificação do consumidor. Nenhum contrato mutador para perks está autorizado. O efeito provider-native permanece único, sob autoridade Iron's/Wind's e com Black Arcana responsável pelo próprio runtime.

**Gates:** testes sintéticos de fail-closed, scanner no JAR físico, inspeção da saída JSON sem inferir resultados para getters `UNRESOLVED`, CI geral no HEAD final, revisão de branch/main e PR. Stages 06.05 e 09 inalterados; mínimo global ≥1.856, campanha binária 38/39, barra global —%, sete fichas Wind's já identificadas 7/7.

### Resultado do JAR oficial, sem interpolação

Execução [Wind CI #40124346655](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40124346655) em `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`, publicou `scalar-getters.json`. A inspeção desse JSON confirmou **4/4 métodos selecionados com `EXACT_STRAIGHT_LINE_EXPRESSION`**, nenhum `UNRESOLVED` neste recorte.

| Spell | Getter | AST aritmética da JVM (nível = 1º parâmetro `int`) |
|---|---|---|
| Aeropic | `getRecastCount` | `Math.max(0, level - 1)` |
| Almighty Push | `getDuration` | `25 + (level * 3)` |
| Tornado | `getDuration` | `15 * (5 + (level * 2))` |
| Wind Jump | `getFloatDuration` | `100 * level` |

**4/4 não representa 4 magias completas nem 4 hooks homologados.** Getter escalar não prova unidade, limites válidos, config, janela de recast, aplicação a entidade, `onCast`, nem persistência. A barra Wind's de fichas simbólicas 7/7 permanece separada; o denominador global continua —%. O exercício é exclusivamente clean-room de interoperabilidade.

### Prevenção de regressão da evidência

`docs/qa/winds_105_formula_contract.py` contém uma referência independente para **as quatro ASTs exatas** comprovadas no JAR SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. No CI, o gate compara o JSON produzido pelo scanner contra essa referência: SHA, mod ID, versão, roster, `EXACT_STRAIGHT_LINE_EXPRESSION` e todos os operandos/operadores devem corresponder. Um getter `UNRESOLVED`, constante alterada, árvore reordenada ou quarto getter ausente torna o check `FAIL_CLOSED`, em vez de permanecer verde silenciosamente.

Sete testes sintéticos independentes cobrem aceitação e rejeição desses casos. O gate valida **conservação de evidência documental**, não que a implementação do provider seja alterável ou que fórmulas devam ser replicadas em Black Arcana. Nenhuma API mutadora é ativada.
