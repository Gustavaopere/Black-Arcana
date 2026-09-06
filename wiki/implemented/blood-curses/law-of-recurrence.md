# Law of Recurrence

## Estado

`IMPLEMENTADO / AUTOMAÇÃO VERDE / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Blood & Curses
- **Função:** adaptação defensiva com tradeoff

## Descrição

Mantém uma adaptação temporária e bounded a famílias semânticas estáveis de dano. Repetir a mesma família aumenta resistência até um teto abaixo de imunidade; trocar de família aplica vulnerabilidade bounded.

## Mecânica

- classificador usa famílias semânticas estáveis;
- resistência acumulada possui teto inferior a imunidade;
- mudança de família produz vulnerabilidade como tradeoff;
- sessão expira e é podada pelo tick do servidor.

## Números

- **Resistência por stack/rank:** `TBD — Stage 08 / configuração final`.
- **Teto:** confirmado conceitualmente como abaixo de imunidade; valor exato deve ser lido do runtime antes de publicar como número final.
- **Duração:** `TBD — reconciliar runtime`.

## Cooldown / cast time

`TBD — host/progressão final`.

## Obtenção/aprendizado

`TBD — Stage 08 / progressão`.

## Segurança

- sem imunidade total por repetição;
- state bounded e com expiry;
- classificação estável evita adaptação por nomes/IDs frágeis;
- troca de família impede defesa universal sem custo.
