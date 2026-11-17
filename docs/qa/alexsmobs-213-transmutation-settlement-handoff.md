# Alex's Mobs Continued 2.1.13 — Item Transmutation: settlement, replay e ciclo de vida

**Estado inicial:** 🟡 auditoria estritamente estática do JAR publisher já identificado; \`static_perk_contract=NOT_CERTIFIED\`, \`mutating_hook=NOT_VERIFIED\`, \`physical_qa=NOT_TESTED\`, \`NO_MUTATION\`. Nenhuma mudança de runtime, XP, itens, pools ou Mastery.

## Autoridade e objetivo da tranche

A PR #1109 rastreou \`MessageTransmuteFromMenu\`, \`Handler\` e o caminho até \`MenuTransmutationTable.transmute\`. A PR #1110 comprovou a implementação \`AMNeoNetwork$1\`, a ligação ao \`IPayloadContext\` e o registro do envelope por \`playBidirectional\`. Esta tranche **não repete** esse trabalho: investiga a sequência de settlement, os callbacks de menu e a persistência de estado, distinguindo guardas estáticos de garantias de replay, concorrência e sessão.

Artefato publisher histórico cruzado com modlist física em auditorias anteriores: \`alexsmobs-2.1.13-neoforge+1.21.1.jar\`, mod id \`alexsmobs\`, SHA-1 \`50ddafdf3d12b33331e4eecb4ab514ae451baadd\`, SHA-256 \`eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8\`, 27.452.738 bytes; CurseForge project/file \`1635121/8856498\`. **A revalidação da modlist física contemporânea ainda é pendência**, pois a árvore atual do sibling não exibiu entrada nominal de Alex's Mobs.

## Programa de inspeção SHA-exata

- [Auditor de settlement](alexsmobs_213_transmutation_settlement_probe.py) e [13 testes sintéticos fail-closed](alexsmobs_213_transmutation_settlement_probe_test.py).
- [Workflow](../../.github/workflows/alexsmobs-213-transmutation-settlement.yml) baixa o mesmo artefato e exige SHA-256/tamanho antes de executar \`javap\` do Java 21.
- O auditor confere também o hash de classfile e o fingerprint de métodos relevantes com o manifesto previamente selado [EXACT-TRANSMUTATION-C2S-2.1.13.json](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-C2S-2.1.13.json).
- Escopo: \`MessageTransmuteFromMenu\` (codec/identidade); \`MenuTransmutationTable\` (construtores, \`stillValid\`, \`slotsChanged\`, \`clickMenuButton\`, \`transmute\`, \`removed\`); \`TileEntityTransmutationTable\` (\`getPossibility\`, \`rollPossiblity\`, \`randomizeResults\`, \`postTransmute\`, \`tick\`, \`loadAdditional\`, \`saveAdditional\`, \`setRerollPlayerUUID\`).
- Somente offsets JVM, operadores selecionados, ramos, hash e contexto muito curto: sem publicar disassembly completo, código proprietário ou JAR.
- A primeira execução fornece apenas **evidência candidata**; selar o resultado real SHA-exato depois da inspeção, rodar os testes novamente e só então registrar conclusões delimitadas na ficha individual.

## Hipóteses a verificar (não resultados)

A auditoria C2S anterior identificou quatro calls de settlement em \`transmute\`: \`ItemStack.setCount @122\`, \`Slot.set @131\`, \`Player.giveExperienceLevels @138\` e \`TileEntityTransmutationTable.postTransmute @149\`. Esta auditoria reprova mudança desses offsets e verifica que cada ação aparece exatamente uma vez. **Ordem no bytecode não implica atomicidade transacional, execução única, rollback ou idempotência.**

Analisar a presença/ausência de chamada **explícita** a \`stillValid\` no método \`transmute\`, sem extrapolar para ausência de invalidação pelo controlador de menus Minecraft/NeoForge. Rastrear \`removed\` e a identidade da table; revisar o registro pós-settlement, NBT, UUID de reroll e reload. A mensagem transporta \`playerId\` e \`choice\`, sem nonce próprio identificado na PR #1109, mas isso isoladamente não prova replay explorável.

Para avaliar replay/concorrência, o teste físico deve perguntar: após um packet válido, uma segunda cópia serializada pode atingir \`transmute\` com input e XP alterados? O mesmo slot é consumido novamente? As opções reroladas interferem? O menu e a mesa continuam os mesmos? Quais efeitos são persistidos após save/restart? São hipóteses de teste, não afirmações de vulnerabilidade.

## Invariantes de interoperabilidade

A transação de itens, XP, reroll e progressão é do provider. Não chamar \`Slot.set\`, \`giveExperienceLevels\` nem \`postTransmute\` outra vez dentro do Black Arcana. Não tratar múltiplas escolhas como spells distintos. O RPG Skill Tree permanece autor de atributos/perks/Mastery somente através de boundaries reais. Sem hook comprovado, \`NO_MUTATION\` e fail-closed.

**Aceitação física pendente:** AMC-T01, AMC-T02, AMC-T03, servidor dedicado + cliente, packet inválido, janela de input, replay, concorrência, desconexão/mudança de dimensão, menu stale e restauro NBT. CI do auditor estático não substitui nenhum deles. Stage 06 permanece como estava.

## Resultado

PENDENTE — preencher exclusivamente após execução no publisher SHA-exato, inspeção do relatório e verificação de testes.
