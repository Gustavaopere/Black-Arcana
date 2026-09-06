# Sanguine Harvest

## Estado

`IMPLEMENTADO / AUTOMAÇÃO VERDE / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Blood & Curses
- **Função:** drenagem em área / sustain hemático

## Descrição

Executa um único pulso bounded de drenagem sobre uma lista bounded de candidatos. O sustain é liquidado a partir do dano realmente entregue, não do dano solicitado.

## Targeting

- range e line-of-sight são validados;
- jogadores e bosses são excluídos segundo o contrato atual documentado;
- target admission é canônica;
- candidatos são bounded e deduplicados.

## Dano e sustain

- **Dano base/final:** `TBD — reconciliar configuração/runtime e Stage 08`.
- **Sustain:** derivado do dano confirmado e sujeito a anti-farm weighting.
- **Sem crédito por dano não entregue:** bloqueio/mitigação reduz o settlement correspondente.

## Cooldown / cast time

`TBD — Stage 08 / host final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Segurança

- sem loops de cura positiva infinita;
- anti-farm weighting;
- exclusões de alvo;
- settlement por dano confirmado;
- sem processamento recursivo de derived damage.

## Relação com reservatório futuro

A drenagem pode vir a ser uma producer legítima de sangue em mB apenas se um contrato causal explícito converter quantidade hemática extraída em recurso armazenável. Até isso existir, esta Wiki não declara produção de mB.
