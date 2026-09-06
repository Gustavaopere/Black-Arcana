# Rift Blades

## Estado

`IMPLEMENTADO / CANÔNICO — REAL-MODPACK HOST ACCEPTANCE DEFERRED`

## Identidade

- **Domínio:** Projection & Arsenal
- **Authority:** Black Arcana
- **Função:** volley/projéteis efêmeros com marked strike e gap-close opcional

## Descrição

Cria handles de lâminas projetadas com lifetime/range explícitos. O dano de marked strike passa pela admissão canônica de interação com entidades. O gap-close é independente: destino bloqueado pode negar somente o deslocamento sem desfazer dano real já autorizado.

## Obtenção/aprendizado

`TBD — Stage 08 / provider/RPG`

## Custo e casting

- **Custo:** `TBD`
- **Cooldown:** `TBD`
- **Cast time:** `TBD`

## Targeting

Range normal e volley normal: `TBD — Stage 08`.

## Hard ceilings confirmados

- máximo técnico de projéteis por volley: `64`;
- raw attack damage de profile: `<= 100.0`;
- handles contam no budget de projeções e liberam budget em expiry/collision/range/logout/shutdown.

## Gap-close

- opcional e independente do settlement de dano;
- não force-load;
- revalida world border, collision/headroom, fluids, protection, teleport support e vehicle state;
- destino inseguro falha fechado.

## Segurança

- dano reautorizado antes de settlement;
- nenhuma blade vira item persistente;
- lifetime/range/owner explícitos;
- cleanup em server shutdown/logout;
- destino de gap-close não é confiado ao cliente.

## VFX

Rift/arsenal visual deve indicar spawn, trajetória e marked strike. Gap-close precisa de telegraph suficiente para não parecer teleport arbitrário.

## Testes/evidência

Stage 07.03 teve RED específico e GREEN com sete GameTests de Rift Blades; integração final passou pipeline completo antes e depois do merge PR #50.
