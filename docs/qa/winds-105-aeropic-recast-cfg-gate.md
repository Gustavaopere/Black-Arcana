# Aeropic 1.0.5 — grafo JVM de fluxo de controle de recast

**Estado:** auditoria independente de topologia, com resultado físico do JAR ainda pendente. A main anterior é 32a6efd3c1a65cac66971d978ebd37204ff48212 (#894 integrado).

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
