# Sistema Hemático — Reservatório e Vínculos

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

Este documento registra a direção de design solicitada para uma economia mágica hemática própria. Não substitui o runtime canônico atual até uma implementação revisada entrar em `main`.

## Invariante principal

A Magia de Sangue **não usa mana normal**.

Se um spell pertencente à disciplina hemática exigir combustível, o custo deve ser resolvido exclusivamente por fontes hemáticas válidas, como sangue próprio, sangue de alvo autorizado, sangue de uma entidade vinculada ou sangue armazenado em infraestrutura hemática. Ausência de uma fonte válida faz o cast falhar fechado.

## Reservatório de sangue

O sistema deve permitir uma construção física de armazenamento de sangue com capacidade medida em `mB`.

Exemplo conceitual:

- capacidade estrutural: `70.000 mB`;
- sangue armazenado: `50 mB`;
- HUD: `50 / 70.000`;
- preenchimento visual proporcional: aproximadamente `0,071%` da barra.

A capacidade vem do volume/arquitetura válida da construção; o recurso disponível vem do sangue realmente armazenado. A barra **não regenera passivamente**.

Uma construção grande e quase vazia permanece uma reserva grande em potencial, mas oferece pouca energia atual.

## Sangue não é energia vital

O sistema deve distinguir explicitamente:

- `SANGUE` — recurso hemático fisiológico de seres que realmente possuem sangue segundo classificação registrada;
- `ENERGIA_VITAL` — vida/força vital abstrata; não é convertida automaticamente em sangue;
- `ALMA/ESPÍRITO` — recurso espiritual provider-owned; não é sangue;
- `MANA` — recurso arcano comum; não participa do combustível hemático por padrão.

Exemplo obrigatório: **Iron Golem não é fonte de sangue.** Ele pode possuir vida/energia vital para outras mecânicas, mas não satisfaz uma operação que exige `SANGUE`.

## Classificação de fontes

Toda entidade elegível deve passar por uma classificação server-authoritative. O design futuro deve prever pelo menos:

- `HEMATIC_BLOOD` — sangue normal válido;
- `ALTERED_BLOOD` — sangue especial (vampírico, corrupto, mágico etc.) com identidade própria;
- `NO_BLOOD` — construtos, golems, máquinas e outros alvos sem sangue;
- `UNKNOWN` — falha fechado até classificação segura.

Nenhuma decisão deve depender só do nome visível da entidade.

## Vínculos

Um vínculo hemático é uma relação persistente e autorizada:

`CONJURADOR ⇄ VÍNCULO ⇄ FONTE`

A fonte pode ser, conforme regras futuras:

- o próprio conjurador;
- criatura viva compatível;
- familiar/servo com ownership válido;
- jogador com consentimento explícito quando PvP/multiplayer;
- reservatório hemático;
- artefato/estrutura que exponha recurso hemático real.

O vínculo deve registrar identidade estável, ownership/consentimento, tipo de recurso, limites, distância/dimensão quando aplicável e política de quebra.

## Transação de cast

Um cast hemático deve seguir uma única transação canônica:

1. resolver spell e custo;
2. resolver fontes permitidas;
3. cotar disponibilidade real;
4. reservar o recurso sem duplicação;
5. executar validação final de targeting/gates;
6. aplicar/commit do spell;
7. consumir exatamente o valor confirmado;
8. refund/rollback quando o cast não for cometido.

Não pode haver dano à fonte sem cast correspondente nem cast gratuito após falha de liquidação.

## Relação com Blood Price existente

O Black Arcana já possui `Blood Price`, que substitui parcialmente um custo provider-owned por vida real de forma transacional. Esse contrato é evidência reutilizável para atomicidade e rollback, mas **não é o sistema final desta economia hemática**, porque o objetivo desta disciplina é não depender da mana normal.

## Próximas decisões de design

Ainda precisam ser fechados antes da implementação:

- razão `mB` ↔ custo mágico;
- como coletar sangue sem duplicação;
- capacidade por bloco/material da estrutura;
- perdas, se existirem;
- distância máxima de vínculo;
- cross-dimension policy;
- prioridade entre múltiplas fontes;
- consentimento PvP;
- compatibilidade Vampirism/Bloodlines/Iron's Blood;
- integração visual com HUD;
- efeitos de tipos especiais de sangue;
- limites de bosses/summons/farms;
- persistência e invalidação após morte/despawn;
- progressão e unlocks no RPG Skill Tree.
