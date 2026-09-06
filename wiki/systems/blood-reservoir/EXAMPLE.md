# Exemplo de uso

Reservatório: `50 / 70.000 mB`.

Spell A custa `40 mB` (valor meramente ilustrativo; não é balanceamento canônico).

- quote encontra 50 mB disponíveis;
- reserva 40 mB;
- HUD pode mostrar 10 mB livres + 40 mB reservados;
- cast confirmado → stored cai para 10 mB;
- cast negado antes do commit → reserva é liberada e stored continua 50 mB.

O exemplo existe apenas para explicar transação/UX; os custos reais serão definidos por spell em Stage 08.
