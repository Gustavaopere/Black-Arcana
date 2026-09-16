# Goety Iron 3.1 — regras de integração

## Authorities envolvidas

### Goety

Permanece autoridade de:

- Soul Energy;
- Focus/Staff framework;
- servants e ownership/lifecycle;
- ritual framework;
- Void Vault e demais estados Goety.

### Iron's Spells 'n Spellbooks

Permanece autoridade de:

- spell identities e schools;
- mana/cast/cooldown/spell attributes do ecossistema Iron's;
- spellcaster semantics nativas que o addon reutiliza.

### Goety Iron

É autoridade da bridge que:

- cria/adapta servants derivados de criaturas do Iron's;
- conecta summon/ritual paths;
- permite aprendizado/empowerment adicional conforme suas regras;
- configura spell attributes dos servants;
- aplica replacements e compatibilities que a release efetivamente implementa.

### Black Arcana

Não assume nenhuma dessas authorities. Seu papel futuro é apenas consumir causalidade comprovada quando houver boundary seguro.

## Regras obrigatórias

1. Não criar segundo servant ledger.
2. Não criar uma segunda mana ou Soul Energy para servants Goety Iron.
3. Não rerodar um spell do Iron's dentro do pipeline de Black Arcana.
4. Não cobrar nem reembolsar custo de provider pela segunda vez.
5. Não converter todo servant magic damage em cast Black Arcana.
6. Não inferir caster ownership a partir da proximidade do jogador.
7. Não conceder Mastery por tick, entidade viva, equipamento ou servant simplesmente carregado.
8. Não usar Polar Bear/Vex replacement como evidência de um hook público até a implementação exata ser comprovada.
9. Não interceptar Tincture/Void Vault para criar uma segunda persistência ou reset concorrente.
10. Não aplicar efeitos ofensivos duplicados ao Improved Ominous Fire Orb.

## Progressão e causalidade

Caso o RPG Skill Tree consuma futuramente eventos desta bridge, a progressão deve exigir evento discreto e autoria causal, por exemplo um cast/kill/milestone cuja origem possa ser comprovada pelo provider.

`servant exists` ou `servant dealt damage` sem provenance estável não basta para settlement de Mastery. Se múltiplos hooks observarem a mesma ação, todos devem convergir para uma única replay identity/mutation canônica.

## Arcane Danger

Goety Iron não herda Danger Profiles genericamente de Goety ou Iron's. Qualquer spell/ability relevante precisa de mapeamento explícito e bounded.

- Arcane Resistance não substitui spell resistance nativa do provider.
- Corruption Resistance não é resistência Goety/Soul Energy.
- Strain/Backlash são canais Black Arcana e só podem ser adicionados quando o cast causal estiver provado.
- Backlash não gera proc chains ofensivas normais.

## Estado técnico atual

`PUBLIC SURFACE USABLE FOR DEDUP/AUTHORITY DESIGN; PROVIDER-SPECIFIC ADAPTER FAIL-CLOSED`.

O File ID 8662179 e o changelog 3.1 são exatos, mas source/API internals da release não foram localizados. Implementação de adapter aguarda boundary verificável ou teste dirigido sobre API pública comprovada.
