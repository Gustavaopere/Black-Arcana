# Alex's Mobs Continued 2.1.13 — Item Transmutation: settlement, replay e ciclo de vida

**Estado inicial:** 🟡 auditoria estritamente estática do JAR publisher já identificado; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Nenhuma mudança de runtime, XP, itens, pools ou Mastery.

## Autoridade e objetivo da tranche

A PR #1109 rastreou `MessageTransmuteFromMenu`, `Handler` e o caminho até `MenuTransmutationTable.transmute`. A PR #1110 comprovou a implementação `AMNeoNetwork$1`, a ligação ao `IPayloadContext` e o registro do envelope por `playBidirectional`. Esta tranche **não repete** esse trabalho: investiga a sequência de settlement, os callbacks de menu e a persistência de estado, distinguindo guardas estáticos de garantias de replay, concorrência e sessão.

Artefato publisher histórico cruzado com modlist física em auditorias anteriores: `alexsmobs-2.1.13-neoforge+1.21.1.jar`, mod id `alexsmobs`, SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`, 27.452.738 bytes; CurseForge project/file `1635121/8856498`. **A revalidação da modlist física contemporânea ainda é pendência**, pois a árvore atual do sibling não exibiu entrada nominal de Alex's Mobs.

## Programa de inspeção SHA-exata

- [Auditor de settlement](alexsmobs_213_transmutation_settlement_probe.py) e [17 testes sintéticos fail-closed](alexsmobs_213_transmutation_settlement_probe_test.py).
- [Workflow](../../.github/workflows/alexsmobs-213-transmutation-settlement.yml) baixa o mesmo artefato e exige SHA-256/tamanho antes de executar `javap` do Java 21.
- O auditor confere também o hash de classfile e o fingerprint de métodos relevantes com o manifesto previamente selado [EXACT-TRANSMUTATION-C2S-2.1.13.json](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-C2S-2.1.13.json).
- Escopo: `MessageTransmuteFromMenu` (codec/identidade); `MenuTransmutationTable` (construtores, `stillValid`, `slotsChanged`, `clickMenuButton`, `transmute`, `removed`); `TileEntityTransmutationTable` (`getPossibility`, `rollPossiblity`, `randomizeResults`, `postTransmute`, `tick`, `loadAdditional`, `saveAdditional`, `setRerollPlayerUUID`).
- Somente offsets JVM, operadores selecionados, ramos, hash e contexto muito curto: sem publicar disassembly completo, código proprietário ou JAR.
- A primeira execução fornece apenas **evidência candidata**; selar o resultado real SHA-exato depois da inspeção, rodar os testes novamente e só então registrar conclusões delimitadas na ficha individual.

## Hipóteses a verificar (não resultados)

A auditoria C2S anterior identificou quatro calls de settlement em `transmute`: `ItemStack.setCount @122`, `Slot.set @131`, `Player.giveExperienceLevels @138` e `TileEntityTransmutationTable.postTransmute @149`. Esta auditoria reprova mudança desses offsets e verifica que cada ação aparece exatamente uma vez. **Ordem no bytecode não implica atomicidade transacional, execução única, rollback ou idempotência.**

Analisar a presença/ausência de chamada **explícita** a `stillValid` no método `transmute`, sem extrapolar para ausência de invalidação pelo controlador de menus Minecraft/NeoForge. Rastrear `removed` e a identidade da table; revisar o registro pós-settlement, NBT, UUID de reroll e reload. A mensagem transporta `playerId` e `choice`, sem nonce próprio identificado na PR #1109, mas isso isoladamente não prova replay explorável.

Para avaliar replay/concorrência, o teste físico deve perguntar: após um packet válido, uma segunda cópia serializada pode atingir `transmute` com input e XP alterados? O mesmo slot é consumido novamente? As opções reroladas interferem? O menu e a mesa continuam os mesmos? Quais efeitos são persistidos após save/restart? São hipóteses de teste, não afirmações de vulnerabilidade.

## Invariantes de interoperabilidade

A transação de itens, XP, reroll e progressão é do provider. Não chamar `Slot.set`, `giveExperienceLevels` nem `postTransmute` outra vez dentro do Black Arcana. Não tratar múltiplas escolhas como spells distintos. O RPG Skill Tree permanece autor de atributos/perks/Mastery somente através de boundaries reais. Sem hook comprovado, `NO_MUTATION` e fail-closed.

**Aceitação física pendente:** AMC-T01, AMC-T02, AMC-T03, servidor dedicado + cliente, packet inválido, janela de input, replay, concorrência, desconexão/mudança de dimensão, menu stale e restauro NBT. CI do auditor estático não substitui nenhum deles. Stage 06 permanece como estava.


## Resultado estático SHA-exato — descoberta CI #44174127031

**Evidência obtida:** execução do JAR publisher anteriormente identificado, SHA-1/SHA-256/tamanho verificados, manifesto anterior validado por classfile SHA-256 e fingerprints dos métodos nativos relevantes, **3 classes e 21 métodos selecionados**. O relatório integral produzido pelo auditor tem **128.611 bytes** e SHA-256 `ce2690b5568168b7d446e2dd9184ab8f17dbafa4784cd43bba353070f6975a62`. O digest e o resumo fail-closed estão fixados no [manifesto de settlement](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-SETTLEMENT-2.1.13.json). O CI reexecuta o mesmo auditor com `--snapshot` e reprova divergência.

### 1. Sequência de execução de `MenuTransmutationTable.transmute(Player,int)`

| Operação nativa | Offset JVM | Disposição estática |
|---|---:|---|
| Consulta do slot de entrada | `Slot.getItem @4` | dados efetivos do slot nativo |
| Custo configurado | `AMConfig.transmutingExperienceCost @8` | valor de configuração; não presumir valor efetivo do pack |
| Seleção de alternativa | `TileEntityTransmutationTable.getPossibility @18` | getter normaliza `choice` em `0..2` |
| Pré-condições / saída | branches em `@47, @54, @61, @71, @78, @87, @97` | incluem lado servidor, tabela, razão de tamanhos, possibilidades, entrada e XP ou creative `instabuild` |
| Quantidade selecionada | `ItemStack.setCount @122` | modifica a cópia da saída nativa |
| Substituição da entrada | `Slot.set @131` | escreve no slot nativo |
| Débito de níveis | `Player.giveExperienceLevels @138` | efeito posterior à escrita do slot |
| Pós-processamento | `TileEntityTransmutationTable.postTransmute @149` | atualiza estado do provider e **agenda** reroll posterior |

O auditor exige exatamente uma referência de cada efeito final, ordem crescente **`122 → 131 → 138 → 149`** e guardas SHA-exatos. Essa ordem **não demonstra** rollback se qualquer chamada falhar, atomicidade sob concorrência, persistência completa do movimento de item nem idempotência diante de mensagens duplicadas.

O menu possui override próprio de `stillValid(Player)`, com `ContainerLevelAccess` e `AMBlockRegistry.TRANSMUTATION_TABLE`; entretanto, o corpo integral de `transmute` **não faz chamada direta a `stillValid` ou `removed`**. A eventual invalidação do menu no pipeline Minecraft/NeoForge permanece uma questão externa ao método, portanto isso não é prova de um bypass alcançável.

### 2. `postTransmute` não executa reroll imediatamente

Pivôs SHA-exatos de `TileEntityTransmutationTable.postTransmute`:

- `@50 TransmutationData.onTransmuteItem`: registra transformação na estrutura de dados do provider;
- `@79 putfield totalTransmuteCount`: incrementa contador de transmutação usando `ItemStack.getCount @75`;
- `@93 sipush 1000` e `@99 TRANSMUTE_1000_ITEMS`: ramificação para advancement em jogador do servidor quando o contador atinge o limite;
- `@114 setRerollPlayerUUID`: guarda o UUID para processamento **posterior**, sem chamar diretamente `randomizeResults` neste método.

No `TileEntityTransmutationTable.tick`, a condição `rerollPlayerUUID == null` desvia de `@14` para `@87`, encerrando o tick. Com UUID pendente:

1. `Level.getPlayerByUUID @25` busca o jogador;
2. `ifnull @30 → @82` desvia **para depois de** `randomizeResults @79` quando o jogador não foi encontrado;
3. `putfield rerollPlayerUUID @84` limpa o UUID mesmo nessa ramificação sem reroll.

Portanto, **o fluxo de bytecode observado descarta o reroll pendente quando o jogador não é localizado naquele tick**. `randomizeResults`, quando chamado, solicita três `rollPossiblity` nos offsets `@3, @9, @15`. Não inferir que todos os resultados efetivos mudarão: pools, config, loot e RNG podem condicioná-los.

### 3. Salvamento e restauração

`TileEntityTransmutationTable.saveAdditional` e `loadAdditional` referenciam `totalTransmuteCount`, `PlayerTransmutationData`, UUIDs de jogadores, `TransmutationData` e os `ItemStack` das três possibilidades. **Ambos não referenciam diretamente o campo `rerollPlayerUUID`.**

Isso estabelece uma distinção entre: (a) dados persistidos de transmutação e opções; (b) **UUID transitório em memória** usado para agendar reroll no próximo tick. O comportamento físico entre settlement, unload e save/restart, incluindo eventual restauração indireta por outra rotina, continua `NOT_TESTED`/`NOT_VERIFIED`; não converter o padrão estático em alegação de perda de itens.

### 4. Limites de segurança e condições para perks

- **Protocolo:** `MessageTransmuteFromMenu` transporta `playerId` e `choice`; o contexto NeoForge foi auditado na PR #1110, mas não há evidência de nonce/idempotência do evento. Guardas de tipo do menu e comparação do ID **não equivalem** a vinculação da mesa/posição/sessão.
- **Repetição:** um segundo pacote pode ser processado com estado alterado; a execução e seus efeitos só podem ser qualificados em cliente/servidor real. Não afirmar duplicação sem reproduzir.
- **Sem seam:** não existe hook mutador homologado pré-XP/pré-output, e nada permite o Black Arcana gerar output, repetir custo ou forçar `randomizeResults` para satisfazer perks.
- **Rigor de contagem:** 3 raízes semânticas identificadas, 0/3 contratos estáticos certificados; nenhum novo spell, índice, Mastery, runtime ou Stage promovido.
- **Próximo QA:** AMC-T01..T03; teste de jogador ausente no tick, reload entre `postTransmute`/`tick`, menu stale, seleção inválida, replay serial, concorrência em servidor dedicado, bloqueios de config/datapack e proteção de recursos.

**Status final desta tranche:** `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION` / fail-closed. Contrato estático individual segue **⚠️ parcial**, apesar do fortalecimento da evidência causal.
