# Malum 1.8.2 — Spirit Rites

## Estado

`SPIRIT RITE SYSTEM PROVEN / DEFERRED-REGISTRY MIGRATION PROVEN / RITE LOCUS+ANCHOR+UNWAVER ARCHITECTURE PROVEN / COMPLETE 1.8.2 RITE REGISTRY+RECIPES UNVERIFIED`

Cada Spirit Rite ativo confirmado na versão instalada recebe seu próprio `.md` somente quando houver evidência suficiente da build 1.8.2. A branch pública posterior não é usada para promover nomes ou efeitos automaticamente para o pack.

## Arquitetura confirmada para a geração 1.8

O changelog publisher-authored da linha 1.8, ancorado ao commit exato de versão identificado no catálogo pai, confirma que:

- Spirit Rites migraram para um **Deferred Registry**;
- providers/addons de rites precisaram adaptar compatibilidade a essa mudança;
- muitos rites foram retrabalhados;
- world-affecting rites passaram a usar **Rite Locus**;
- **Rite Anchors** podem definir um vetor de deslocamento/travel para o Rite Locus;
- tipos de spirit diferentes podem fortalecer/alterar o locus conforme a regra do rite;
- **Rite Unwaver** remove/mata um Rite Locus ativo quando o encontra.

Isso prova a arquitetura da geração instalada, mas não fecha a lista nominal de rites do JAR 1.8.2.

## Consequências de authority

Um Rite Locus é um efeito persistente provider-owned. Para Black Arcana:

- um tick de locus não é um novo cast;
- permanência em área não gera Mastery por tick;
- mutação de mundo já executada por Malum não deve ser reaplicada por Black Arcana;
- se Black Arcana iniciar uma operação cross-provider, a admissão pelo `WorldEffectPolicy` do lado Black Arcana não substitui a própria authority do rite Malum;
- lifecycle/remoção deve permanecer Malum-owned, inclusive quando Rite Unwaver participa do encerramento.

## Healing Rite — delta 1.8.2

O changelog exato 1.8.2 documenta que o **healing rite** passou a disparar somente quando a cura produziria efeito. Isso é evidência comportamental publisher-authored da build instalada, mas não fornece registry ID, fórmula, raio, custo ou cadence.

## Addon boundary — Gaze

O changelog 1.8 cita explicitamente que addons de rite como **Gaze** precisaram ser atualizados para o novo registry model. Portanto qualquer Rite registrado por Gaze permanece `gaze`-owned e não entra na contagem base de Malum.

## Campos ainda abertos

- lista completa de Spirit Rites 1.8.2;
- registry IDs;
- recipes/inputs;
- spirit requirements;
- ranges/areas;
- durations/cadence;
- Rite Locus budgets e persistence;
- activation/termination contracts;
- safe public API/event hooks.

Até esses gates serem resolvidos, fichas individuais permanecem `UNVERIFIED / FAIL-CLOSED`.