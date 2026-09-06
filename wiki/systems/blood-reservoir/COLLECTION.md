# Coleta de Sangue

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

A coleta precisa produzir `mB` apenas a partir de eventos hemáticos confirmados. Possíveis produtores futuros:

- drenagem ativa de alvo elegível;
- extração ritual autorizada;
- sacrifício/abate causal válido;
- transferência manual para o reservatório;
- adapters provider-native quando um mod já possuir sangue real consumível.

## Regras

- damage dealt não equivale automaticamente a mB coletado;
- um mesmo evento causal tem uma única identidade de crédito;
- alvos `NO_BLOOD` geram 0 mB;
- alvos `UNKNOWN` falham fechado;
- sangue coletado nunca excede o que o producer autorizado declarou disponível;
- summons/farms podem exigir anti-farm multiplier/cap;
- player targets seguem PvP/consentimento;
- boss blood, se permitido, deve ter cap explícito;
- não converter Soul Energy, spirit, mana ou energia vital em sangue por fallback.

## Relação com Sanguine Harvest

Sanguine Harvest é um candidato de producer no futuro, mas o runtime atual liquida sustain por dano confirmado; ele **ainda não autoriza** registrar mB automaticamente.
