# Alex's Mobs Continued 2.1.13 — BlockTransmutationTable, menu e persistência

**Estado inicial:** 🟡 auditoria estática read-only do publisher 2.1.13 historicamente identificado; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Nenhum código do provider foi copiado.

## Continuidade após PR #1112

As PRs #1109–#1112 documentaram receptor C2S, contexto NeoForge, settlement e reroll diferido, `TransmutationData`, NBT e opções de display. Esta etapa investiga **o bloco dono da mesa e sua relação com o menu/slots/tile**, sem redescobrir as mesmas classes como se fossem novas magias.

Autoridade histórica: `alexsmobs-2.1.13-neoforge+1.21.1.jar` (mod ID `alexsmobs`), SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`, 27.452.738 bytes, CurseForge `1635121/8856498`. **Não está reconfirmado que a modlist atual possui esse mod/versionamento; o estudo não homologa compatibilidade com o pack atual.**

## Fontes e plano reproduzível

- [Auditor read-only](alexsmobs_213_table_block_lifecycle_probe.py) e [11 testes sintéticos](alexsmobs_213_table_block_lifecycle_probe_test.py).
- [GitHub Actions](../../.github/workflows/alexsmobs-213-table-block-lifecycle.yml) baixa JAR por URL fixa, impõe SHA-256/tamanho e Java 21; valida os fingerprints do tile e menu contra [snapshot C2S](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-C2S-2.1.13.json).
- Owners inspecionados: `BlockTransmutationTable`, `MenuTransmutationTable`, `TileEntityTransmutationTable`, `MenuTransmutationTable$1` e `MenuTransmutationTable$2`. O scanner de outras classes usa apenas strings `BlockTransmutationTable/TileEntityTransmutationTable/MenuTransmutationTable` no classfile: **um candidato não prova chamada, hook ou cobertura exaustiva**.
- Relatório JSON registra hash de classfile, roster com descritores, fingerprints de métodos, offsets, branches e windows de operandos relacionados a bloco, menu, cliente/servidor, owner, slots, transmutação e notificações `setChanged`/`sendBlockUpdated`; não publica corpos integrais do código de terceiro.
- Resultados de descoberta não promovem o numerador, Stage ou hooks; após observar o JSON real, fixar digest SHA-256, documentar somente ramos efetivamente comprovados, reexecutar `--lock` no CI final e atualizar a ficha individual.

## Questões que precisam de prova

1. **Abertura do menu:** como `BlockTransmutationTable` resolve jogador, lado lógico, `MenuProvider` e `BlockEntity`, e quais guardas impedem abertura inválida?
2. **Validade de sessão:** há ligação demonstrada com `ContainerLevelAccess`, posição e tipo de bloco? `MenuTransmutationTable.stillValid` deve ser diferenciado de eventual chamada no `transmute`.
3. **Reroll e slots:** `MenuTransmutationTable$1.setChanged` já é conhecido por chamar `slotsChanged` e `SimpleContainer.setChanged`. O callback realmente informa o `BlockEntity` ou só o container de inventário?
4. **Persistência:** existência/ausência de chamadas diretas a `BlockEntity.setChanged` e `Level.sendBlockUpdated` é sinal estático. Não concluir perda de dados sem verificar callbacks indiretos, superclass, save/chunk lifecycle e reload físico.
5. **Abuso/replay:** menu de mesma classe, mas outra mesa, player ausente, chunk descarregado, input retirado, duas mensagens serializadas e alteração de dimensão precisam de QA dedicada.

## Limites/QA e integração

`BlockTransmutationTable` é **consumidor técnico** da raiz `Item Transmutation`, não uma nova magia. Black Arcana não deve duplicar custo, movimento de itens, XP nem reroll do provider. O RPG Skill Tree permanece dono apenas de progressão/perks/gates por contratos reais.

Checks CI de desassembly/compilação/GameTest do **Black Arcana** não equivalem a execução física do Alex's Mobs no modpack. AMC-T01, AMC-T02, AMC-T03, multiplayer, restauração NBT e testes de sessão continuam sem evidência de PASS. Manter `NO_MUTATION` / fail-closed; nenhum aumento de contratos (0/3 no recorte observado), nenhum avanço de Stage.

## Resultado

PENDENTE — acrescentar exclusivamente depois da inspeção do relatório SHA-exato e da revisão dos branches.
