# Regras de Vínculo Hemático

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

## Princípio

Um vínculo não transforma qualquer ser vivo em fonte de sangue. O vínculo apenas autoriza acesso a um recurso que a fonte realmente possui.

## Elegibilidade mínima

Uma fonte hemática válida precisa satisfazer, no momento da criação e no momento do consumo:

1. identidade estável reconhecida pelo servidor;
2. classificação hemática válida (`HEMATIC_BLOOD` ou subtype explicitamente aceito);
3. quantidade de sangue disponível > 0 quando o cast exigir consumo;
4. ownership/consentimento válido quando aplicável;
5. entidade/estrutura carregada e acessível segundo a política do spell;
6. ausência de proteção/claim/gate que proíba a operação;
7. ausência de estado `UNKNOWN`.

## Fontes possíveis

### Próprio corpo

Permitido por padrão apenas acima de um piso seguro definido por balanceamento. Nunca pode produzir sangue do nada.

### Entidade viva vinculada

Só é válida se possuir sangue real segundo o classificador. Constructs, golems e máquinas não passam automaticamente.

### Familiar/servo

Exige ownership autoritativo do provider e classificação hemática válida. Ser summon não significa ter sangue.

### Outro jogador

Requer política PvP explícita e consentimento quando não houver contexto hostil autorizado. Nunca inferir consentimento por proximidade.

### Reservatório estrutural

Usa sangue efetivamente armazenado em mB. A estrutura pode ser fonte de grande capacidade sem regeneração passiva.

## Quebra do vínculo

O vínculo deve falhar ou ser suspenso em condições como:

- morte/despawn/removal da fonte;
- troca de dimensão quando cross-dimension não for permitido;
- distância acima do limite;
- perda de ownership/consentimento;
- mudança da classificação hemática;
- indisponibilidade do provider;
- corrupção de estado/persistência;
- proteção/claim que passe a negar acesso.

## Múltiplos vínculos

A ordem de consumo deve ser server-owned e configurável/explicitamente definida no design final. Nunca depender da ordem de renderização da UI.

Estratégias candidatas:

- prioridade manual do jogador;
- reservatório primeiro;
- próprio sangue por último;
- menor impacto vital primeiro;
- distribuição proporcional.

A estratégia definitiva permanece `TBD` até balanceamento.

## Anti-abuso

- uma unidade de sangue não pode ser reservada por dois casts simultâneos;
- rollback devolve no máximo o que foi realmente reservado;
- morte/remoção entre quote e commit deve invalidar/recalcular a transação;
- summons/farms recursivos não criam sangue sem um producer causal válido;
- nenhuma conversão automática de `ENERGIA_VITAL`, `MANA`, `SOUL_ENERGY` ou `SPIRIT` para sangue.
