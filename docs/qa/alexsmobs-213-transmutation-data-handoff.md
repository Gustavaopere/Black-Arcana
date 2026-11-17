# Alex's Mobs Continued 2.1.13 — TransmutationData, NBT e sincronização das opções

**Estado:** 🟡 auditoria estática read-only do publisher histórico; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

## Continuidade e escopo

Após as PRs #1109 (receptor), #1110 (contexto NeoForge) e #1111 (settlement, reroll diferido e persistência parcial), esta tranche investiga **o objeto de dados e seus consumidores**, não repete a inspeção do pacote C2S nem implementa hook mutador.

A versão física confirmada anteriormente foi `alexsmobs-2.1.13-neoforge+1.21.1.jar`, SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8` e 27.452.738 bytes. **Não há prova nova de que a modlist atual ainda inclui esse provider:** a árvore atual do sibling não mostrou uma entrada nominal de Alex's Mobs. Análises abaixo são condicionadas ao JAR historicamente identificado; não interpretar como compatibilidade certificada com um pack diferente.

## Método reprodutível

O [auditor](alexsmobs_213_transmutation_data_probe.py), os [testes sintéticos](alexsmobs_213_transmutation_data_probe_test.py) e o [workflow SHA-exato](../../.github/workflows/alexsmobs-213-transmutation-data.yml) leem somente o JAR publisher.

Escopo principal: `TransmutationData` (métodos `onTransmuteItem`, `fromNBT`, `saveAsNBT`, `getTotalWeight`, `getRandomItem`); `AMCompat` (wrappers NBT aplicáveis); `TileEntityTransmutationTable` (`loadAdditional`, `saveAdditional`, `postTransmute`, `randomizeResults`, `tick`); `MenuTransmutationTable` (construtor/slots/removed); `MessageUpdateTransmutablesToDisplay` (codec e processamento) e classes auxiliares presentes no JAR.

O scanner faz descoberta global por referências binárias a `TransmutationData` e `MessageUpdateTransmutablesToDisplay`, mas essas ocorrências são somente **candidatos**, não prova de call graph completo. O resultado JSON contém classfile SHA-256, assinaturas, fingerprints de métodos, branches, callsites, literais limitados e sinais diretos de `setChanged`/`sendBlockUpdated`, sem publicar o corpo completo de qualquer implementação de terceiros.

O workflow verifica os hashes físicos, o selo anterior de classes nativas e os índices de certificação. A primeira execução gera discovery read-only; depois da análise do resultado é possível fixar um manifesto SHA-256 do relatório completo e reexecutar os testes.

## Perguntas de investigação

1. Como `TransmutationData` registra input/output e calcula peso acumulado, e quais fatores efetivamente mudam as probabilidades? Verificar os operandos, sem assumir que pesos declarativos bastam para calcular chances efetivas.
2. Quais tags NBT persistem os dados por jogador e as alternativas de output? Diferenciar `TransmutationData` do campo transitório `rerollPlayerUUID` já identificado na PR #1111.
3. A geração das três alternativas é sincronizada em direção servidor→cliente? Quais classes e side-gates atuam no receptor de `MessageUpdateTransmutablesToDisplay`?
4. Há chamadas diretas a `setChanged` ou `sendBlockUpdated` nos caminhos de reroll e settlement? **Ausência de chamada direta não prova falha de persistência**, que pode ser delegada ao container/slot ou ciclo de vida.
5. Quais consumidores precisam ser considerados para perks de custo, seleção, quantidade, reroll e Mastery sem criar um segundo pipeline transacional?

## Limitações e estados

Esta auditoria não faz download da modlist física local do usuário, não testa o jogo em multiplayer, não certifica replay, não mede chances efetivas em runtime e não habilita perks. Candidatos a extensões permanecem conceituais até comprovar seam real. `NO_MUTATION` e fail-closed permanecem incondicionais.

Não promover o numerador de Alex's Mobs (0/3 no recorte observado), o universo total do provider, o índice global ou Stage 06 com base apenas no scanner. Os testes AMC-T01..T03 e as validações de login/reload/datapack/servidor continuam `NOT_TESTED`.

## Resultado

Pendente da primeira inspeção de resultados e da fixação de evidências do JAR SHA-exato.
