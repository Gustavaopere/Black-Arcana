# Malum 1.8.2 — Spirit Rites

## Estado

`SPIRIT RITE SYSTEM PROVEN / 26 BASE RITE IDENTITIES RELEASE-BOUNDED / DEFERRED-REGISTRY MIGRATION PROVEN / RITE LOCUS+ANCHOR+UNWAVER ARCHITECTURE PROVEN / RECIPES+RUNTIME/API QA PENDING`

A lista base de `SpiritRiteType` da linha instalada 1.8.2 está fechada por evidência release-bounded. Isso não equivale a prova byte-a-byte de que um commit específico gerou o JAR físico e não promove mecânicas internas, recipes ou APIs não documentadas para contrato do Black Arcana.

## Evidência de intervalo completo 1.8.2

A linha oficial `SammySemicolon/Malum-Mod` para Minecraft 1.21.1 é delimitada por:

- `f56691e56e591a6d8d1859ff119e749375e14d61`, primeiro checkpoint observado com `mod_version=1.8.2`; o pai ainda declara `1.8.1`;
- `03b743a37f3eeb0cc7f4364f0730e1f135f78408`, último checkpoint observado antes de o filho avançar para `1.8.3`.

O blob de `MalumSpiritRiteTypes.java` é `2b9e4e5445733dee4ed205e4331d55c93ac86028` nos dois extremos. Além disso, a consulta ao histórico Git do próprio caminho durante toda a janela 1.8.2 retorna **nenhum commit intermediário**. Portanto não existe, nesse caminho, alteração temporária seguida de reversão entre os checkpoints usados para o fechamento semântico.

Como evidência auxiliar de deduplicação dos dois rites especiais, `MalumSpiritRiteEffectTypes.java` possui blob SHA `e5fd8854c12783e4503475ccaf461c3a19c2a0b0` nos mesmos dois extremos, e o histórico Git desse caminho retorna **nenhum commit** em toda a janela 1.8.2. O arquivo registra efeitos separados `undirected_rite_effect` e `unchained_rite_effect`. Esse registry de efeitos não adiciona objetos ao ledger semântico; ele apenas sustenta que os dois `SpiritRiteType` especiais registrados no inventário primário não são um único alias/proxy compartilhado.

## Inventário base release-bounded — 26 rites

Os 26 registros ativos base-Malum são:

- especiais Arcane: `malum:undirected_rite`, `malum:unchained_rite`;
- Sacred: `malum:rite_of_healing`, `malum:rite_of_nourishment`, `malum:rite_of_nurturing`, `malum:rite_of_lust`;
- Wicked: `malum:rite_of_harming`, `malum:rite_of_empowerment`, `malum:rite_of_culling`, `malum:rite_of_rending`;
- Aerial: `malum:rite_of_the_howling_gale`, `malum:rite_of_the_sky_tether`, `malum:rite_of_gravity`, `malum:rite_of_ascension`;
- Aqueous: `malum:rite_of_the_flowing_grasp`, `malum:rite_of_the_good_tides`, `malum:rite_of_soaking`, `malum:rite_of_sapping`;
- Earthen: `malum:rite_of_the_stone_ward`, `malum:rite_of_the_oaken_might`, `malum:rite_of_creation`, `malum:rite_of_destruction`;
- Infernal: `malum:rite_of_the_burning_fervor`, `malum:rite_of_the_fiery_embrace`, `malum:rite_of_smelting`, `malum:rite_of_quickening`.

O registry de efeitos release-bounded acima possui efeitos distintos para `undirected_rite` e `unchained_rite`; eles são mantidos como identidades de rite e não tratados como aliases/proxies. Estes **26 rites** são os únicos objetos desta página adicionados ao ledger semântico atual.

## Arquitetura confirmada para a geração 1.8

O changelog publisher-authored da linha 1.8 confirma que:

- Spirit Rites migraram para um **Deferred Registry**;
- providers/addons de rites precisaram adaptar compatibilidade a essa mudança;
- muitos rites foram retrabalhados;
- world-affecting rites passaram a usar **Rite Locus**;
- **Rite Anchors** podem definir um vetor de deslocamento/travel para o Rite Locus;
- tipos de spirit diferentes podem fortalecer/alterar o locus conforme a regra do rite;
- **Rite Unwaver** remove/mata um Rite Locus ativo quando o encontra.

Isso confirma a arquitetura pública da geração instalada, mas não transforma a implementação interna do provider em API do Black Arcana.

## Consequências de authority

Um Rite Locus é um efeito persistente provider-owned. Para Black Arcana:

- um tick de locus não é um novo cast;
- permanência em área não gera Mastery por tick;
- mutação de mundo já executada por Malum não deve ser reaplicada por Black Arcana;
- se Black Arcana iniciar uma operação cross-provider, a admissão pelo `WorldEffectPolicy` do lado Black Arcana não substitui a própria authority do rite Malum;
- lifecycle/remoção deve permanecer Malum-owned, inclusive quando Rite Unwaver participa do encerramento.

## Healing Rite — delta 1.8.2

O changelog 1.8.2 documenta que o **healing rite** passou a disparar somente quando a cura produziria efeito. Isso é evidência comportamental publisher-authored da linha instalada, mas não fornece fórmula, raio, custo ou cadence.

## Addon boundary — Gaze

O changelog 1.8 cita explicitamente que addons de rite como **Gaze** precisaram ser atualizados para o novo registry model. Portanto qualquer Rite registrado por Gaze permanece `gaze`-owned e **não** entra na contagem base de 26 Malum rites.

## Campos ainda abertos

O inventário nominal/registry ID dos 26 rites base está fechado para a contagem release-bounded. Continuam pendentes, quando necessários para integração ou QA:

- recipes/inputs;
- spirit requirements e quantidades;
- ranges/areas;
- durations/cadence;
- Rite Locus budgets e persistence;
- activation/termination contracts;
- safe public API/event hooks;
- equivalência byte-a-byte entre source e JAR físico.

Fichas individuais só podem promover detalhes mecânicos além da identidade nominal quando houver evidência adequada para a linha 1.8.2. Até lá, esses campos permanecem `UNVERIFIED / FAIL-CLOSED`.