# Black Arcana — Wiki de Feitiços

Esta pasta é a fonte canônica de documentação dos feitiços do Black Arcana.

## Regras de estado

Cada página individual deve marcar o feitiço como um destes estados:

- `IMPLEMENTADO / CANÔNICO` — presente em `main` com runtime canônico.
- `IMPLEMENTADO / VALIDAÇÃO FINAL DEFERIDA` — runtime presente, mas aceitação final em modpack/cliente ainda pendente.
- `PLANEJADO` — design previsto, ainda sem runtime canônico.
- `CONCEITO / PESQUISA` — proposta em estudo; não deve ser tratada como funcionalidade disponível.
- `BLOQUEADO / FAIL-CLOSED` — depende de provider/API/authority ainda não confirmados.

## Estrutura

- `implemented/` — feitiços e mecânicas já implementados/canônicos.
- `planned/` — feitiços já planejados nos stages do Black Arcana.
- `schools/chaos/` — futura disciplina de Magia do Caos, hospedada prioritariamente no ecossistema Iron's Spells.
- `schools/order/` — futura disciplina de Magia da Ordem, hospedada prioritariamente no ecossistema Iron's Spells.
- `schools/blood-binding/` — futura expansão de Magia de Sangue/Vínculos, sem uso da mana normal.
- `systems/blood-reservoir/` — especificação da economia de sangue armazenado em mB e vínculos de fontes.
- `sources/` — metodologia e referências externas usadas para inspiração/adaptação.

## Campos obrigatórios por feitiço

Cada arquivo individual deve documentar, quando aplicável:

1. Identidade e fantasia.
2. Estado de implementação.
3. Escola/domínio/provider.
4. Tier/raridade/progressão.
5. Método de obtenção/aprendizado.
6. Requisitos e gates.
7. Recurso consumido e custo exato/escala.
8. Cooldown.
9. Cast time/channel time.
10. Alcance, área e seleção de alvos.
11. Dano, cura, transferência ou efeito quantitativo.
12. Escalonamento.
13. Efeitos secundários.
14. Regras PvP/bosses/summons.
15. Fallback/fail-closed.
16. Segurança/anti-abuso/deduplicação.
17. VFX, animação, áudio e HUD.
18. Integrações com outros mods.
19. Receitas, rituais, estruturas ou itens associados.
20. Testes e evidência de validação.
21. Referências de design e proveniência.

Nenhum número de dano, cooldown, custo ou progressão deve ser inventado em páginas de estado `IMPLEMENTADO`. Valores ainda não fechados devem permanecer explicitamente como `TBD — Stage 08 / balanceamento`.
