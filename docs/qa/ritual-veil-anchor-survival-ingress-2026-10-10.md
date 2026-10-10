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
