# Blood — reforma hemática sobre a escola existente do Iron's

## Decisão canônica

**Não existe uma nova escola `Blood Binding`.**

A escola **Blood** já existe no Iron's Spells 'n Spellbooks e continuará sendo a escola hemática do pack. O Black Arcana atuará como camada de integração/reforma de recurso e vínculo.

## Mudança principal planejada

Após implementação da reforma hemática, **spells Blood não usarão mana normal**.

O custo será resolvido exclusivamente por fontes hemáticas válidas, por exemplo:

1. sangue do próprio caster;
2. sangue de criatura-alvo quando o spell explicitamente drena/consome;
3. sangue de uma fonte vinculada elegível;
4. sangue armazenado em reservatório em mB;
5. combinações aprovadas dessas fontes.

Mana normal cheia não deve permitir cast Blood sem sangue disponível.

## Estado atual x estado planejado

A Wiki de cada spell Blood deve preservar ambos:

- **provider atual:** custo nativo em mana do Iron's, cooldown, dano, etc.;
- **override Black Arcana planejado:** `0 mana normal` e custo hemático ainda calibrado em HP/mB/vínculos.

Isso evita apagar como o provider funciona hoje enquanto documenta o contrato futuro.

## Sangue não é vida genérica

`BLOOD != VITAL_ENERGY != SOUL != SPIRIT != MANA`

Ter HP não prova possuir sangue.

Exemplo obrigatório:

- Iron Golem: pode possuir vida/energia vital para outras mecânicas, mas **NO_BLOOD** para custos hemáticos.

## Vínculo hemático

`CASTER <-> BLOOD LINK <-> SOURCE`

Um vínculo autoriza acesso a sangue real já existente; ele não cria sangue nem converte automaticamente outros recursos.

A fonte pode ser:

- o próprio corpo;
- criatura hemática elegível;
- jogador com consentimento/PvP policy adequada;
- familiar/servo se ownership e blood eligibility forem comprovados;
- reservatório hemático;
- estrutura/artefato que exponha sangue real por contrato.

Quebra de vínculo deve considerar morte/despawn, distância, dimensão, consentimento, ownership, claims/protection e indisponibilidade do provider.

## Reservatório

A infraestrutura canônica permanece em `wiki/systems/blood-reservoir/`.

Princípios:

- conteúdo em mB é separado da capacidade;
- `50 / 70000 mB` significa tanque grande quase vazio;
- não há regeneração passiva de sangue;
- reserva de custo usa `reserve -> validate -> commit/refund`;
- não pode haver double-spend entre caster, vínculo e tanque.

## Spells Blood existentes

O Iron's base atualmente possui 10 spells Blood e todos serão catalogados individualmente em `wiki/modpack-catalog/providers/irons-spells/blood/`:

- Acupuncture;
- Blood Needles;
- Blood Slash;
- Blood Step;
- Devour;
- Heartstop;
- Raise Dead;
- Ray Of Siphoning;
- Sacrifice;
- Wither Skull.

Addons que registrem outros spells Blood também entram em suas próprias pastas/provider e participarão da mesma auditoria antes de qualquer override global.

## Cuidado de compatibilidade

A mudança de recurso não deve ser feita cegamente por `school == Blood` sem auditar addons. Cada spell precisa declarar se o custo pode ser convertido para sangue sem quebrar provider, progressão ou semântica. O objetivo é chegar à regra 'Blood não usa mana normal', mas com adapters explícitos e fail-closed quando um addon não puder ser integrado com segurança.
