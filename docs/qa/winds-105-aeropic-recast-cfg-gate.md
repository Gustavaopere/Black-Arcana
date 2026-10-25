# Aeropic 1.0.5 — grafo JVM de fluxo de controle de recast

**Estado:** topologia CFG normal auditada no JAR oficial 1.0.5; prova de receiver/dataflow em applyEffectTick ainda pendente. A main anterior é 32a6efd3c1a65cac66971d978ebd37204ff48212 (#894 integrado).

## Necessidade

O scanner do PR #894 atribuiu corretamente o receiver compilado em onEffectAdded usando locais JVM explícitos, mas applyEffectTick ficou NOT_PROVEN porque o trecho contém controle de fluxo. Não se deve tratar todo o método como um único bloco nem inferir transferência causal a partir de referências próximas.

## Contrato do novo scanner

A ferramenta winds_105_aeropic_recast_cfg.py usa apenas o JAR Wind's Spellbooks 1.0.5 SHA-1 8744886899bc245ae147a44baa2b183689cec7da e inspeciona AeropicEffect.applyEffectTick e onEffectAdded. A partir de offsets da saída javap, reconstrói arestas normais de if/goto e termina em return/athrow, conta nós alcançáveis, pontos de junção, referências ao campo ACROBATICS_SPELL que pertencem a algum caminho normal de entrada até a invocação exata, e referências que **dominam** a invocação quando a topologia é completamente modelada.

- Dominância é apenas uma propriedade de ordem em caminhos normais; **não estabelece que Supplier.get forneça o receiver**, nem que qualquer valor passe à pilha, a PlayerRecasts ou ao NBT.
- Qualquer switch, jsr/ret, salto inválido, final sem retorno ou tabela de handlers de exceção bloqueia conclusões positivas de dominância (FAIL_CLOSED_INCOMPLETE_CFG); cobertura parcial pode continuar quantificada.
- Nenhum offset, disassembly, bytecode, classe copiada ou conteúdo do JAR é publicado: apenas campos simbólicos, contagens e avisos de não prova.
- Não executa jogo, Java do provider, hooks, integração de perks ou runtime de Black Arcana.

## Gates de aceitação

1. Executar testes sintéticos que incluam bypass do supplier, branch e join, loop, método com exception table, switch e desvio inválido.
2. Examinar a saída JSON do JAR do publicador e documentar os valores observados na ficha Aeropic.
3. Fixar resultado em contrato de regressão independente, verificando SHA, campos não comprovados e não alteração de contador mágico.
4. Conferir CI especializado + Black Arcana verify e QA companion no HEAD final, branch 0 behind main e diff sem mudança em Java/runtime.
5. Não avançar Stage 06.05 nem Stage 09; permanência do estado SEM_HOOK_SEGURO até prova provider-native.

**Contagem preservada:** Wind's 7/7 spells, nove getters selecionados; campanha binária 38/39, ≥1.856 objetos mágicos globais como limite inferior, denominador global desconhecido.

## Evidência física do JAR — 25/10/2026

[CI SHA-exato #40159609661](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40159609661): SUCCESS, 15 testes sintéticos aprovados, hash oficial conferido, saída JSON inspecionada no log do job. Análise dos dois métodos sem exception table/switch não modelado, somente arestas normais. O CI de contrato adicionado posteriormente congela estes dados e ainda precisa passar no HEAD final.

| Campo | applyEffectTick | onEffectAdded |
|---|---:|---:|
| Instruções JVM | 288 | 43 |
| Branches if/goto | 20 | 2 |
| Instruções alcançáveis pela entrada normal | 288 | 43 |
| Instruções em caminhos normais até a chamada getRecastCount | 222 | 34 |
| Junções de caminhos normais até o recast | 5 | 0 |
| Leituras do campo ACROBATICS_SPELL | 3 | 1 |
| Leituras em ao menos um caminho de entrada ao recast | 3 | 1 |
| Leituras que dominam a chamada de recast | 1 | 1 |
| Callsite alcançável no CFG normal | sim | sim |
| Grau | BOUNDED_NORMAL_CFG_TOPOLOGY_ONLY | BOUNDED_NORMAL_CFG_TOPOLOGY_ONLY |

Uma leitura do Supplier **domina** o callsite de recast no fluxo normal de applyEffectTick. É uma relação de *ordem e alcançabilidade de instruções*, não uma prova de que o retorno de Supplier.get ocupa a posição de receptor na operand stack. Há três leituras possíveis, cinco junções e 20 branches; o algoritmo de pilha de bloco único do #893/#894 permanece insuficiente para fechar o dataflow de applyEffectTick.

O resultado anterior de **onEffectAdded** no PR #894 (COMPILED_SUPPLIER_GET_CAST_RECEIVER) é evidência independente e não foi recalculado nem revogado por esta auditoria de topologia. O novo scanner registra compiled_receiver_source=NOT_PROVEN_BY_CFG_TOPOLOGY, runtime_receiver_class=NOT_PROVEN, return_value_to_PlayerRecasts=NOT_PROVEN, dynamic_override_executed=NOT_PROVEN e safe_mutating_hook=NOT_PROVEN.

**Próximo gate:** interpretação de operand stack entre os nós e junções demonstrados, com semântica de locals/StackMap e confluência conservadora, e verificação separada da instância concreta devolvida pelo Supplier. Nenhum hook de perk é autorizado; lifecycle de PlayerRecasts segue provider-native. Contadores e Stages não mudam.
