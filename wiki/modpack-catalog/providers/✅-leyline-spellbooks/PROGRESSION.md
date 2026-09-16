# Leyline Spellbooks — progressão pública confirmada

## Elementos citados oficialmente

A descrição pública associa a progressão do addon a:

- descoberta de fenômenos/pilares ligados às leylines;
- carregamento de pilares e abertura de Leyline Rifts;
- encontros em ondas;
- loot temático e experiência;
- chance de obter **Ley Crystal**;
- crafting/uso de **Leyline Codex** e **Ley Staff** como ferramentas de attunement.

## Evidência exata 1.0.3

O JAR físico agora fecha os IDs e recursos de progressão principais:

- `leylines:ley_crystal`;
- `leylines:leyline_codex`;
- `leylines:ley_staff`;
- recipes provider-owned do Codex e Staff usando Ley Crystal;
- advancements para obter crystal/codex/staff, carregar pilar e concluir rift;
- o Codex como container de spells no substrato do Iron's;
- reward path do encounter referenciando o Leyline Codex;
- injeção dedicada de scroll `leylines:charge_leyline` em loot tables do Iron's.

Continuam não provados por este fechamento: probabilidades finais no pack montado, tuning/economia, detalhes internos de persistence/network do rift/pilar e um seam API estável para integração Black Arcana.

## Regra para Black Arcana

Não construir uma segunda progressão de Leylines com números presumidos. Se perks ou sistemas próprios precisarem reconhecer attunement/progresso, devem ler estado/item/advancement provider-native comprovado depois da extração. Até lá, gates dependentes de detalhes internos permanecem fail-closed.
