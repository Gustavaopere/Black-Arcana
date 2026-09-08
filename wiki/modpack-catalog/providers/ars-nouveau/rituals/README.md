# Ars Nouveau — Rituals

State: `24/24 SOURCE-PINNED / INDIVIDUAL PAGES COMPLETE / RUNTIME QA PENDING`

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

Rituais do Ars Nouveau ficam separados dos glyphs porque possuem preparação, reagentes, Source/world interaction e autoridade próprias. A registry de produção 5.13.1 contém 24 entradas e todas possuem página individual nesta pasta.

## 24 rituais

1. [Burrowing](burrowing.md) — `ars_nouveau:ritual_burrowing`
2. [Moonfall](moonfall.md) — `ars_nouveau:ritual_moonfall`
3. [Cloudshaping](cloudshaping.md) — `ars_nouveau:ritual_cloudshaping`
4. [Sunrise](sunrise.md) — `ars_nouveau:ritual_sunrise`
5. [Disintegration](disintegration.md) — `ars_nouveau:ritual_disintegration`
6. [Challenge](challenge.md) — `ars_nouveau:ritual_challenge`
7. [Overgrowth](overgrowth.md) — `ars_nouveau:ritual_overgrowth`
8. [Fertility](fertility.md) — `ars_nouveau:ritual_fertility`
9. [Restoration](restoration.md) — `ars_nouveau:ritual_restoration`
10. [Warping](warping.md) — `ars_nouveau:ritual_warping`
11. [Scrying](scrying.md) — `ars_nouveau:ritual_scrying`
12. [Flight](flight.md) — `ars_nouveau:ritual_flight`
13. [Gravity](gravity.md) — `ars_nouveau:ritual_gravity`
14. [Summon Wilden](summon-wilden.md) — `ars_nouveau:ritual_wilden_summon`
15. [Summon Animals](summon-animals.md) — `ars_nouveau:ritual_animal_summon`
16. [Binding](binding.md) — `ars_nouveau:ritual_binding`
17. [Awakening](awakening.md) — `ars_nouveau:ritual_awakening`
18. [Harvest](harvest.md) — `ars_nouveau:ritual_harvest`
19. [Containment](containment.md) — `ars_nouveau:ritual_containment`
20. [Conjure Island: Plains](conjure-island-plains.md) — `ars_nouveau:ritual_conjure_island_plains`
21. [Forestation](forestation.md) — `ars_nouveau:ritual_forestation`
22. [Flowering](flowering.md) — `ars_nouveau:ritual_flowering`
23. [Conjure Island: Desert](conjure-island-desert.md) — `ars_nouveau:ritual_conjure_island_desert`
24. [Sanctuary](sanctuary.md) — `ars_nouveau:ritual_sanctuary`

## Regras de integração

- Ars Nouveau é authority do Ritual Brazier, Source, reagentes, registry, lifecycle e efeitos provider-native desses rituais.
- Efeitos destrutivos ou de biome/world conversion observados no Ars não transferem autoridade para Black Arcana nem enfraquecem `WorldEffectPolicy`.
- Alterações globais de tempo/clima, teleporte, spawn denial, familiar binding e automation continuam provider-owned e não devem ser double-processed.
- Diferenças entre descrição provider-native e path executável ficam explicitamente marcadas como `RUNTIME QA`, nunca corrigidas por inferência.
