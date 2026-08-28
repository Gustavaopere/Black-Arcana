# Segurança de mundo e entidades

Stage 04 já está implementado e funciona como uma camada de admissão para efeitos perigosos. A ideia central é que uma spell não deve modificar mundo/entidades diretamente só porque passou pelo gate de progressão.

## Segurança de chunks e destinos

O core contém:

- `LoadedChunkGuard`;
- `ProtectedDestinationGuard`;
- `ProtectionQuery`;
- `ProtectionAdapterRegistry`.

Essas seams permitem recusar efeitos em destino inválido/protegido e evitam transformar um cast em chunk-loader implícito.

## Política configurável de efeitos

`ConfigurableWorldEffectPolicy` e `WorldEffectProfileRegistry` classificam/admitam efeitos de mundo por perfil. O resultado do policy é consultado no pipeline **antes** de reservar o custo.

Isso significa que uma magia negada por proteção do mundo não deveria consumir o recurso e só depois descobrir que não podia executar.

## Orçamento

`WorldEffectBudgetLedger` existe para limitar trabalho/mutações dentro de budgets explícitos. `BoundedWorkScheduler` oferece o mesmo princípio para efeitos agendados: trabalho futuro é bounded e contabilizável.

## Mutações temporárias

Há infraestrutura própria para alterações reversíveis:

- `TemporaryWorldMutation`;
- `TemporaryMutationKey`;
- `TemporaryMutationTracker`;
- `TemporaryBlockMutationGateway`;
- `TemporaryRestorationService`;
- `TemporaryBlockBackend`.

Isso separa “colocar um bloco temporariamente” de “esquecer de restaurar o mundo”. O tracker é parte do estado necessário para restauração controlada.

## Entidades

A camada inclui:

- `EntityInteractionAdmissionService`;
- `DefaultEntityInteractionPolicy`;
- `EntityProtectionFacts`;
- `EntityEffectLimits`;
- tipos/autorização de interação.

Portanto, target resolution e permission to affect target são decisões distintas.

## Regra de interpretação

Essas classes são infraestrutura real e congelada do Stage 04. Elas não implicam que já exista uma spell canônica para cada classe de mutação suportada. O catálogo futuro deve declarar como cada spell usa esses limites.
