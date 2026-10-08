# Stage 06.05 — decisão de produto para ativação de Veil Anchor Consecration

Status: **⛔ SEM INGRESSO CANÔNICO DE JOGADOR NO RUNTIME ATUAL**. Documento de arquitetura/critério de implementação, **não uma implementação**. Baseline analisada: Black Arcana `main@9141a8ed1c345db4e995e5f2aa849df2c24769b9`.

## Evidência já estabelecida

- [Plano 06.05](../../plans/06-rituals/05-final-validation-handoff.md) e [evidência do ritual](rituals-final-validation-evidence.md) identificam ausência de caller de produção para `RitualEngine.start(...)` e ausência de rede, bloco/item, UI/evento ou comando de ativação canônico.
- `BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION` já é uma definição server-owned com **100 ticks até commit** e **400 ticks até conclusão**.
- A integração Malum atual fornece **4 espíritos arcane + 2 wicked**; consumo/reserva/outcome continuam sob `RitualEngine` e `RitualCompletionSavedData`.
- O servidor mantém gate de jogador online, dimensão/âncora válida e chunk carregado. Nada disso produz sozinho a ação explícita de jogador.

## Decisão de UX/produto ainda necessária

A implementação deve fornecer uma **interação legítima em jogo com uma âncora de ritual identificável**, distinta de um atalho administrativo/QA. A forma exata da peça de mundo, sua obtenção, posição de multibloco, gesto de ativação, cancelamento e feedback visual ainda **não está aprovada nem demonstrada** pelo código atual. Não inventar um evento/hook da API de Malum ou Eidolon.

Um desenho candidato para revisão é uma ação server-authoritative sobre uma âncora Black Arcana, sem construir um segundo motor de rituais. Isso é proposta de interface, não afirmação de feature existente.

## Checklist de aceitação para desbloquear 06.05

1. Definir e implementar uma interação de jogador real e alcançável no pack, preferencialmente vinculada a um bloco/ritual Black Arcana registrado e com aquisição legítima documentada; não aceitar exclusivamente comando debug/creative-only.
2. No servidor, resolver jogador, mundo, chunk, âncora, definição já registrada e componente Malum **antes** de iniciar. Não aceitar `RitualContext`, `RitualActivationId`, custos ou outcome serializados como autoridade do cliente.
3. Criar identidade de ativação replay-protected **no servidor**, atravessar exclusivamente `RitualEngine.start(...)` e manter `RitualEngine.tick(...)` como pipeline único de commit/conclusão.
4. Rejeitar sem consumo quando falta provider, autorização/WorldEffectPolicy, espírito, chunk, player online, capacidade ou ownership; sem fallback de ritual gratuito.
5. Disponibilizar feedback visual apenas como apresentação/predição client-side da decisão do servidor.
6. Incluir testes determinísticos para pré-commit, pós-commit, replay, segunda pessoa/mesma âncora, custos, reinício/lifecycle, provider ausente e side-only, antes de chamar engenharia `✅`.
7. Transferir testes de Survival, servidor real, multiplayer e Eidolon/Malum físicos para Stage 09 conforme D035; não converter CI em aceitação física.

## Proibição de promoção prematura

Sem a forma de interação player-facing verificada, o item permanece **⛔ bloqueado**. Este arquivo não autoriza acionar o ritual em produção por comando de teste, nem proclama Stage 06.05 finalizada. Interfaces/assinaturas e implementações devem ser verificadas na branch concreta antes de serem utilizadas.
