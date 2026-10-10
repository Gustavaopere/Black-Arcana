# Veil Anchor Consecration — ingresso Survival

Implementação: PR #733 (2026-10-10). Estado: **🟡 revisão de engenharia/CI**, não é teste físico nem PASS em Survival. Base antes do PR: Black-Arcana/main@d1d17157abc4be05be6898292526644ad55ca4ad. Snapshot do plano 06.05: Minecraft 1.21.1, NeoForge 21.1.248, Malum 1.8.2.

## Altar original e interação

Construir este altar **horizontal 3×3 no mesmo nível Y**:

    S A S
    A C A
    S A S

- **C**: Crying Obsidian, centro da Âncora do Véu.
- **A**: quatro Amethyst Blocks nos pontos cardeais.
- **S**: quatro Soul Sand nos pontos diagonais.
- **Gesto**: segurar um Echo Shard na mão principal, **agachar + clicar com o botão direito** no centro.

Todos os blocos e o item existem no Minecraft vanilla e podem ser obtidos em Survival. Echo Shard é chave reutilizável, não custo consumido. O custo canônico do Malum permanece **4 espíritos arcane + 2 wicked** e só é comprometido no tick 100; conclusão no tick 400. Não há comando debug, item creative-only, hook Malum inventado nem segundo motor de rituais.

## Caminho de execução e limites

1. O evento NeoForge RightClickBlock é registrado no game bus. O cliente apenas percorre o pipeline de interação; exclusivamente o servidor resolve identidade, mundo, bloco, permissões e resultado.
2. O jogador precisa estar vivo, não espectador, no mesmo mundo, a até 6 blocos do centro, com direito de interagir via gates vanilla de mundo/edição. A compatibilidade com claim mods permanece pendência de testes reais.
3. O padrão só inspeciona nove células previamente conhecidas, todas com chunks já carregados e dentro do world border. Sem varredura global, ticket ou carregamento de chunk.
4. Definição e binding reais precisam estar presentes no runtime. A checagem de componentes confirma recursos **antes de iniciar** mas não reserva nem consome.
5. O servidor gera UUID único de ativação, constrói o contexto a partir do ServerPlayer e da posição real, e chama exclusivamente RitualEngine.start. O motor existente controla exclusividade por âncora, replay, persistência, commit e conclusão.
6. O requisito de Malum revalida geometria e autorização do jogador no commit e no outcome. Altar desmontado ou caster indisponível cancela, sem recompensa; após commit os espíritos não são reembolsados, conforme PR #732.
7. A resposta é enviada como mensagem de action bar. Nenhum payload de custo, resultado ou identidade confiado ao cliente.

A recompensa atual é registrada no RitualCompletionSavedData, sem mutação de terreno. Portanto não há mutação de mundo para submeter ao WorldEffectPolicy nesta feature; quaisquer futuros outcomes destrutivos precisam passar explicitamente pela Stage 04.

## Testes e bloqueios remanescentes

Teste determinístico de wiring no composition root, padrão exato de nove células (incluindo célula ausente/incorreta), ausência de provider/binding, espíritos insuficientes, exclusividade da âncora em multiplayer, interrupção pré-commit e conclusão uma única vez. Testes anteriores cobrem replay, restore, delays e componentes Malum. Exigir ambos os jobs da CI no HEAD final antes de merge.

**Ainda sem prova física:** Malum 1.8.2 da instância, claims, latência cliente/multiplayer, obtenção no pack real, quebra/reconstrução entre fases, Eidolon real e persistência do candidato exato. Conservar no Stage 09 sob D035. Não declarar Stage 06.05 ✅ ou iniciar Stage 07 apenas pela presença de código.

## 2026-10-10 — correção de interrupção em eventos de lifecycle (PR #735)

Uma lacuna foi encontrada após o PR #733: mesmo com os requisitos revalidados aos ticks 100/400, o caster poderia desconectar e reconectar, trocar de dimensão e retornar, ou morrer entre os checkpoints, sem que a sessão fosse interrompida nesse intervalo. O PR #735 adiciona cancelamento **imediato** por UUID do caster em `PlayerLoggedOutEvent`, `PlayerChangedDimensionEvent` e no tick do servidor para jogadores mortos, usando o `RitualEngine.interrupt(...)` existente. O scan é limitado ao registro de sessões ativas; não toca JAR/API do Malum e não inspeciona estruturas globais.

- **Antes de commit:** não há consumo; a âncora é liberada e a sessão desaparece do snapshot.
- **Depois de commit:** o espírito já consumido permanece gasto e nenhum outcome de conclusão é executado, mesmo após retorno rápido do jogador.
- **Outros jogadores:** sessões de outros casters permanecem intactas; o cancelamento do caster remove todas as suas sessões ativas e libera suas âncoras.
- **Persistência:** a camada server manager recaptura o estado quando o evento remove sessões; o próximo save do Minecraft usa a lista de sessões canceladas, evitando snapshot em memória stale. Isso não é garantia física contra queda do processo antes de flush em disco.

Testes determinísticos comprovam esses contratos no core e a presença de listeners no composition root. Ainda faltam testes **com cliente real** de logout/reconnect, morte, troca de dimensão, custos Malum e preservação após restart do mesmo save, na Stage 09. Este PR não promove a Stage 06.05.

## 2026-10-10 — atendimento justo de sessões com orçamento por tick (PR #737)

Auditoria do `RitualEngine.tick` encontrou starvation: `ArcanaServerRuntime` permite até 1.024 sessões ativas e processa no máximo 64 por tick, mas a seleção anterior retornava sempre o prefixo mais antigo do registro. Assim, mesmo uma sessão já pronta para commit/outcome poderia permanecer sem processamento enquanto as primeiras sessões aguardavam prazos futuros. Duas regressões determinísticas falharam no workflow RED `38085725067`, inclusive com `tick(..., 1)` retornando zero commits para uma sessão posterior já pronta.

A correção introduz seleção **round-robin limitada ao lote escolhido** em `RitualSessionRegistry.sessionsForTick(limit)`. Ela move somente as sessões escolhidas para o final da ordem de seleção; `RitualEngine.tick` passa a usar essa rota. `snapshot`, `interruptCaster` e `restore` continuam com seus próprios métodos; a ordem de serialização dos snapshots pode acompanhar a ordem rotativa, sem alterar os elementos, identidades, estados ou os prazos persistidos. Sem nova varredura global, ticket de chunk, novo motor ou modificação de custos/outcomes. O limite de 64 sessões processadas por tick e a capacidade de 1.024 permanecem os mesmos.

Consequência importante: sob saturação, uma sessão pode ser processada **após** seu tick nominal de commit/conclusão devido ao orçamento, mas deve receber serviço de modo justo; não prometer duração exata sob 1.024 sessões concorrentes. Aceitação física com Malum, cliente e modpack continua transferida para Stage 09. O teste de CI não comprova TPS real sob carga.

## 2026-10-10 — captura de SavedData por transição do ritual (PR #738)

Auditoria do ciclo de persistência encontrou um intervalo de estado obsoleto: antes deste PR o `ArcanaServerRuntimeManager` recapturava as sessões a cada **200 ticks**, além de saída, troca de dimensão e morte do caster. Uma ativação, um commit de espíritos, uma conclusão ou um cancelamento poderiam ocorrer antes da próxima captura periódica, permitindo que um world-save visse a lista/fase anterior das sessões do Black Arcana.

Agora o ingresso legítimo `MinecraftVeilAnchorConsecrationRuntime` solicita a captura da nova sessão **somente quando `RitualEngine.start(...)` retorna STARTED**. Após cada tick do runtime, o gerente verifica `lastRitualTickSummary()`: um ou mais commits, outcomes ou cancelamentos levam a **uma captura do `BlackArcanaSavedData` nesse tick**. Ticks sem transição continuam no regime de 200 ticks e eventos de lifecycle já estabelecidos. Não há nova ledger, registro global por tick, segundo motor, autoridade de cliente ou dependência da API do Malum.

A captura atualiza o objeto `SavedData` e marca-o dirty; **não força o Minecraft a gravar/flush no disco**. Não se pode prometer atomicidade entre Malum inventory e Black Arcana SavedData em queda abrupta do processo. Essa janela de crash-consistency e a execução com o modpack físico permanecem **PENDING — Stage 09**. Os testes automatizados cobrem a decisão de captura em commit, conclusão, cancelamento e o wiring da ativação e do tick, sem considerar isto prova física.

## 2026-10-10 — validação cronológica de sessões restauradas (PR #739)

A auditoria determinística de `RitualEngine.restoreOne` identificou que o restore verificava os delays de cada `RitualDefinition`, mas não conferia se a fase persistida já poderia existir no tempo atual do servidor. Um `RitualSessionSnapshot` com `state=COMMITTED` antes do `commitAtTick` seria restaurado diretamente como comprometido; a rota normal de reserva/consumo dos componentes não seria executada antes do outcome. Um snapshot cujo `startedAtTick` fosse posterior ao `nowTick` também podia entrar no registro.

O restore agora rejeita ambos os casos **antes** de memorizar o `RitualActivationId`, sem ocupar âncora, conceder outcome, cobrar espíritos ou poluir a proteção de replay. A restauração legítima de `COMMITTED` exatamente no commit tick continua permitida e mantém a proibição de consumir os mesmos recursos duas vezes.

Evidência TDD: PR #739, workflow RED `38088781581`: os dois cenários inválidos foram aceitos indevidamente antes da correção (esperado `restored=0`, obtido `restored=1`). O teste limítrofe de um estado `COMMITTED` válido também está registrado. A aceitação binária/real de Malum, Eidolon, save/restart do modpack e o caso de crash permanecem **PENDING / DEFERRED TO STAGE 09** conforme D035; não converter CI em prova física nem promover Stage 06.05 por inferência.

## 2026-10-10 — admissão com capacidade de conclusão esgotada (PR #743)

Auditoria do caminho Malum identificou que o requisito do grande ritual verificava conclusão duplicada, mas não capacidade do `RitualCompletionSavedData`. O ledger de conclusões é limitado a `16.384` entradas. A reserva/consumo de `4 arcane + 2 wicked` ocorre no commit do ritual, enquanto o resultado só é gravado na conclusão; a saturação já conhecida poderia causar consumo de espíritos sem novo registro.

O candidato do PR #743 adiciona um preflight somente-leitura de capacidade em `RitualCompletionLedger` e `RitualCompletionSavedData`, consultado no `MalumServerIntegrationBootstrap` durante a admissão e a revalidação existente imediatamente antes da reserva de espíritos. `ALREADY_COMPLETED` mantém precedência sobre `CAPACITY_EXCEEDED`. Testes JUnit exercitam o ledger limitado, o `SavedData` no limite físico de entradas e dois cenários do grande ritual com acesso Malum sintético: cheio no início e saturado entre start e pré-commit.

**Limite do escopo:** o preflight não reserva uma vaga futura e não garante que o ledger permaneça disponível *após* o commit caso outros rituais concluam antes. Concorrência na saturação, persistência simultânea de inventário Malum versus SavedData, falha abrupta e comportamento do JAR físico permanecem sem aceitação; não converter essas observações em PASS, nem promover Stage 06.05/Stage 07 por CI. Se o esgotamento entre commit e outcome for confirmado como cenário aplicável, ele exige correção funcional na Stage 06 antes de fechamento.
