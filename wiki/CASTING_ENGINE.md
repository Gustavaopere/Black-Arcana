# Pipeline de conjuração

`ArcanaCastEngine` define a ordem canônica de validação e execução. Essa ordem é relevante para gameplay e para integrações porque um cast pode ser recusado antes de qualquer custo ser consumido.

## Ordem atual

1. **Identity / request validation** — valida identidade e forma básica da requisição.
2. **Replay guard** — reivindica o cast e rejeita reenvios/replays.
3. **Progression gate** — verifica se o jogador possui acesso lógico ao conteúdo.
4. **Cooldown check** — rejeita casts ainda em cooldown/sem charge disponível.
5. **Target resolution** — resolve o alvo no servidor.
6. **Cost check** — confirma que os recursos necessários estão disponíveis.
7. **World policy** — decide se o efeito é permitido naquele contexto de mundo/alvo.
8. **Cost reservation** — os recursos são reservados, mas ainda não finalizados.
9. **Effect application** — o efeito tenta executar.
10. **Commit** — somente após sucesso do efeito a reserva é confirmada.
11. **Cooldown start** — cooldown começa depois do commit.
12. **Success observer** — observadores opcionais recebem o sucesso.

## Falha e refund

O custo é transacional. Depois da reserva, o engine mantém uma flag de commit. Se o efeito falhar ou uma exceção interromper o caminho antes do commit, o `finally` executa `reservation.refund()`.

Isso evita a situação em que um cast falha tecnicamente depois de retirar mana/espíritos e deixa o jogador pagando por um efeito que nunca aconteceu.

## Observadores de sucesso são isolados

Depois que efeito e recurso já foram confirmados, falha de um `CastSuccessObserver` é ignorada pelo engine. O cast permanece válido e não é duplicado/refundado só porque telemetria, integração secundária ou outro observer falhou.

## Status de recusa

O resultado diferencia pelo menos:

- `DENIED_IDENTITY`;
- `DENIED_REPLAY`;
- `DENIED_PROGRESSION`;
- `DENIED_COOLDOWN`;
- `DENIED_TARGET`;
- `DENIED_COST`;
- `DENIED_WORLD_POLICY`;
- `EFFECT_FAILED`;
- sucesso.

Isso permite ao HUD receber feedback autoritativo sem tentar deduzir localmente por que o servidor recusou o cast.

## Ingress e canais

O core também contém `ArcanaCastIngressService`, `ArcanaChannelManager` e `ArcanaChannelCastCoordinator`. Casts iniciados por UX ou host integration convergem para esse ingresso canônico em vez de possuírem caminhos de autoridade paralelos.

O channel manager mantém estado de casts canalizados separado do clique inicial, enquanto o coordinator decide o avanço/finalização pelo runtime do servidor.
