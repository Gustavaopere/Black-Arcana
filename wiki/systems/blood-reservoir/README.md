# Blood — Reservatório, custo hemático e vínculos

## Estado

`CONCEITO / PESQUISA — REFORMA DA ESCOLA BLOOD EXISTENTE; NÃO IMPLEMENTADO`

Este documento descreve a reforma planejada da **escola Blood já existente no Iron's Spells 'n Spellbooks**. Não cria uma nova escola, não cria uma segunda mana e não altera o runtime atual até uma implementação revisada entrar em `main`.

## Invariante principal planejado

Depois da implementação, spells Blood integrados **não usarão mana normal**.

Se um spell Blood exigir combustível, o custo será resolvido exclusivamente por fontes hemáticas válidas:

- sangue do próprio caster;
- sangue de alvo autorizado quando a semântica do spell permitir;
- sangue de entidade vinculada;
- sangue armazenado em infraestrutura hemática;
- combinação explícita dessas fontes.

Mana normal disponível não satisfaz um custo Blood. Ausência de fonte hemática válida faz o cast falhar fechado.

## Estado provider-native atual

Hoje o Iron's cobra mana normal nos spells Blood. A Wiki preserva esses valores como **baseline factual do provider**.

Durante a futura implementação, cada spell receberá adapter explícito com dois campos separados:

- `provider_native_mana_cost` — custo original, preservado para auditoria/config;
- `black_arcana_blood_cost` — custo efetivo novo em HP/mB/fontes vinculadas.

O primeiro deixa de ser debitado quando o override hemático estiver ativo e validado.

## Reservatório de sangue

O sistema deve permitir uma construção física com capacidade medida em `mB`.

Exemplo:

- capacidade estrutural: `70.000 mB`;
- sangue armazenado: `50 mB`;
- HUD: `50 / 70.000 mB`;
- preenchimento visual: aproximadamente `0,071%`.

A capacidade vem do volume/arquitetura válida da construção; o recurso disponível vem do sangue realmente armazenado. A barra **não regenera passivamente**.

Uma construção grande e quase vazia oferece grande capacidade potencial, mas quase nenhum combustível atual.

## Sangue não é energia vital

O sistema distingue explicitamente:

- `SANGUE` — recurso hemático fisiológico;
- `ENERGIA_VITAL` — vida/força vital abstrata;
- `ALMA/ESPÍRITO` — recurso espiritual provider-owned;
- `MANA` — recurso arcano comum.

Esses recursos não se convertem automaticamente.

Exemplo obrigatório: **Iron Golem não é fonte de sangue.** Ele pode possuir HP/energia vital para outras mecânicas, mas satisfaz `NO_BLOOD` para operações hemáticas.

## Classificação de fontes

Toda entidade elegível passa por classificação server-authoritative:

- `HEMATIC_BLOOD` — sangue normal válido;
- `ALTERED_BLOOD` — sangue especial, como vampírico/corrupto/mágico, quando houver provider/registro;
- `NO_BLOOD` — construtos, golems, máquinas e outros alvos sem sangue;
- `UNKNOWN` — falha fechado até classificação segura.

Nenhuma decisão depende somente do nome visível da entidade.

## Vínculos

Um vínculo hemático é uma relação persistente/autorizada:

`CONJURADOR <-> BLOOD LINK <-> FONTE`

A fonte pode ser:

- o próprio conjurador;
- criatura hemática compatível;
- familiar/servo com ownership válido e sangue real;
- jogador com consentimento/política PvP adequada;
- reservatório hemático;
- artefato/estrutura que exponha sangue real por contrato.

O vínculo registra identidade estável, ownership/consentimento, tipo de recurso, limites, distância/dimensão e política de quebra.

## Transação de cast

Um cast Blood reformado deve seguir uma única transação:

1. resolver spell e adapter Blood;
2. calcular custo hemático;
3. resolver fontes permitidas;
4. cotar disponibilidade real;
5. reservar HP/mB sem duplicação;
6. executar targeting/gates finais;
7. commit do cast;
8. consumir exatamente o valor confirmado;
9. refund/rollback se o cast não for cometido.

Não pode haver dano/consumo sem cast correspondente, cast gratuito após falha, nem double-spend entre corpo, vínculo e tanque.

## Relação com Blood Price existente

`Blood Price` já demonstra atomicidade e rollback ao trocar parcialmente custo provider-owned por vida. Na nova arquitetura ele deve ser **reavaliado/migrado**: Blood school não deve depender de substituição parcial de mana, porque o objetivo final é `0 mana normal` para spells Blood integrados.

Blood Price pode permanecer como mecânica separada para outros contextos se houver identidade legítima, mas não será usado como desculpa para manter mana como combustível da Blood school.

## Compatibilidade obrigatória antes do override global

Não aplicar cegamente a regra apenas por `school == Blood`. Auditar individualmente:

- 10 Blood spells do Iron's base;
- addons que adicionem spells à Blood school;
- Vampire Spells Addon/Vampirism/Bloodlines;
- Hazen/Somake/Travel Optics e demais providers com conteúdo hemático;
- summons, self-cost, channeled spells e spells com custos especiais.

Cada adapter incompatível deve falhar fechado até existir integração segura.

## Próximas decisões de design

- razão HP ↔ mB ↔ custo do spell;
- coleta de sangue;
- capacidade por bloco/material;
- perdas/eficiência;
- distância e cross-dimension de vínculo;
- prioridade entre múltiplas fontes;
- consentimento PvP;
- tipos especiais de sangue;
- limites de bosses/summons/farms;
- persistência após morte/despawn;
- HUD/resource bar;
- progressão/unlocks no RPG Skill Tree.
