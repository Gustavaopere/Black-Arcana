# Ephemeral Tempering

## Estado

`IMPLEMENTADO / CANÔNICO — REAL-MODPACK HOST ACCEPTANCE DEFERRED`

## Identidade

- **Domínio:** Projection & Arsenal
- **Authority:** Black Arcana
- **Função:** aprimoramento temporário de projeções

## Descrição

Aplica estado de tempering temporário e bounded a uma projeção elegível. O efeito não modifica permanentemente equipamento real, não duplica item e não transforma projection state em enchant/NBT persistente.

## Obtenção e aprendizado

`TBD — Stage 08 / RPG/provider`

## Custo e casting

- **Custo:** `TBD — Stage 08/provider`
- **Cooldown:** `TBD — Stage 08/provider`
- **Cast time:** `TBD — Stage 08/provider`

## Mecânica

O tempering existe somente dentro do lifecycle autorizado da projeção/sessão. Finalização, invalidação ou cleanup remove o estado efêmero.

## Hard ceilings relevantes

Subordinado aos budgets de Projection & Arsenal, incluindo `MAX_ACTIVE_ECHOES = 48` e `MAX_RAW_ATTACK_DAMAGE = 100.0` como teto técnico do domínio, nunca como bônus normal.

## Segurança

- nenhuma mutação persistente de gear;
- nenhuma escrita arbitrária de NBT;
- estado bounded e associado ao owner/projection handle;
- cleanup obrigatório.

## VFX

O tempering deve alterar emissivo/material/runa da projeção sem fazê-la parecer um item físico permanente. `TBD — visual profile`.

## Testes/evidência

Stage 07.03 possui evidência automatizada canônica; valores ordinários de balanceamento permanecem Stage 08.
