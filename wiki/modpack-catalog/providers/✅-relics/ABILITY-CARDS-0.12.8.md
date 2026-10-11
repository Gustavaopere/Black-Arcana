# Relics 0.12.8 — 41 fichas owner-scoped de poderes

Estado: **✅ 39/39 habilidades base + 2/2 sinergias `COUNTED_EXACT` individualizadas** · **⚠️ QA de configuração/equipamento/Survival e contratos de runtime pendentes**.

## Prova técnica e contabilização

- Mod ID `relics`, JAR físico `relics-1.21.1-0.12.8.jar`, SHA-1 físico = publisher `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`, CurseForge 445274/8158315. [Inventário exato](EXACT-0.12.8-ABILITY-INVENTORY.md).
- O artefato auditado contém 20 relíquias base, mas os **itens não são 20 ações semânticas novas**. O modelo provider-native possui **39 raízes de habilidade** mais **duas sinergias `SynergyTemplate` owner-scoped**.
- A chave de identidade é **`<relic>|<ability>`** ou **`<relic>|<synergy>`**. `hunting_belt|slots` e `kinetic_belt|slots` não colidem; tampouco `glitchy_mantle|electricity` e `kinetic_belt|electricity`.
- Há evidência estrutural e de hashes diferentes para as duas sinergias `electricity` (owner class, token sets e texto localizado distinto), sem reutilizar as strings originais de tooltip.
- Todas as 41 identidades **já pertencem à métrica global `COUNTED_EXACT`**: materialização **+0 novas identidades**. Mínimo do projeto permanece **1.851 global / 1.849 escopo**, com denominador final aberto.
- Cuidado: os IDs exatos são **raízes internas de identidade de ability/synergy extraídas do artefato**, não uma prova de `ResourceLocation` de spell, hook, método, custo, fórmula, efeito ou configuração do modpack.
- Relics é autoridade de abilities, synergies, XP/level, cooldown, targeting e progressão; Curios é dono de slots. Black Arcana não duplica execução ou liquidação nem transfere isso ao RPG Skill Tree.

## Habilidades base — 39/39

| # | Relíquia proprietária | ID factual | Chave composta | Ficha |
|---:|---|---|---|---|
| 1 | `chef_hat` | `satiety` | `chef_hat|satiety` | [Abrir](abilities/chef_hat/satiety.md) |
| 2 | `chorus_staff` | `blink` | `chorus_staff|blink` | [Abrir](abilities/chorus_staff/blink.md) |
| 3 | `clot_of_time` | `rewind` | `clot_of_time|rewind` | [Abrir](abilities/clot_of_time/rewind.md) |
| 4 | `cut_glass_boot` | `glass` | `cut_glass_boot|glass` | [Abrir](abilities/cut_glass_boot/glass.md) |
| 5 | `experience_disperser` | `dispersion` | `experience_disperser|dispersion` | [Abrir](abilities/experience_disperser/dispersion.md) |
| 6 | `ghostly_mantle` | `fog` | `ghostly_mantle|fog` | [Abrir](abilities/ghostly_mantle/fog.md) |
| 7 | `ghostly_mantle` | `gaze` | `ghostly_mantle|gaze` | [Abrir](abilities/ghostly_mantle/gaze.md) |
| 8 | `ghostly_mantle` | `spectral_escape` | `ghostly_mantle|spectral_escape` | [Abrir](abilities/ghostly_mantle/spectral_escape.md) |
| 9 | `glitchy_mantle` | `distortion` | `glitchy_mantle|distortion` | [Abrir](abilities/glitchy_mantle/distortion.md) |
| 10 | `glitchy_mantle` | `glitch` | `glitchy_mantle|glitch` | [Abrir](abilities/glitchy_mantle/glitch.md) |
| 11 | `glitchy_mantle` | `illusion` | `glitchy_mantle|illusion` | [Abrir](abilities/glitchy_mantle/illusion.md) |
| 12 | `hunting_belt` | `pack` | `hunting_belt|pack` | [Abrir](abilities/hunting_belt/pack.md) |
| 13 | `hunting_belt` | `slots` | `hunting_belt|slots` | [Abrir](abilities/hunting_belt/slots.md) |
| 14 | `jellyfish_necklace` | `regeneration` | `jellyfish_necklace|regeneration` | [Abrir](abilities/jellyfish_necklace/regeneration.md) |
| 15 | `jellyfish_necklace` | `shock` | `jellyfish_necklace|shock` | [Abrir](abilities/jellyfish_necklace/shock.md) |
| 16 | `kinetic_belt` | `gliding` | `kinetic_belt|gliding` | [Abrir](abilities/kinetic_belt/gliding.md) |
| 17 | `kinetic_belt` | `slots` | `kinetic_belt|slots` | [Abrir](abilities/kinetic_belt/slots.md) |
| 18 | `leafy_mantle` | `camouflage` | `leafy_mantle|camouflage` | [Abrir](abilities/leafy_mantle/camouflage.md) |
| 19 | `leafy_mantle` | `revival` | `leafy_mantle|revival` | [Abrir](abilities/leafy_mantle/revival.md) |
| 20 | `midnight_mantle` | `constellation` | `midnight_mantle|constellation` | [Abrir](abilities/midnight_mantle/constellation.md) |
| 21 | `midnight_mantle` | `invisibility` | `midnight_mantle|invisibility` | [Abrir](abilities/midnight_mantle/invisibility.md) |
| 22 | `midnight_mantle` | `phase` | `midnight_mantle|phase` | [Abrir](abilities/midnight_mantle/phase.md) |
| 23 | `midnight_mantle` | `starfall` | `midnight_mantle|starfall` | [Abrir](abilities/midnight_mantle/starfall.md) |
| 24 | `piglin_mask` | `barter` | `piglin_mask|barter` | [Abrir](abilities/piglin_mask/barter.md) |
| 25 | `piglin_mask` | `looting` | `piglin_mask|looting` | [Abrir](abilities/piglin_mask/looting.md) |
| 26 | `piglin_mask` | `neutrality` | `piglin_mask|neutrality` | [Abrir](abilities/piglin_mask/neutrality.md) |
| 27 | `reflective_necklace` | `reflection` | `reflective_necklace|reflection` | [Abrir](abilities/reflective_necklace/reflection.md) |
| 28 | `rider_flute` | `stable` | `rider_flute|stable` | [Abrir](abilities/rider_flute/stable.md) |
| 29 | `ring_of_the_seven_deadly_sins` | `envy` | `ring_of_the_seven_deadly_sins|envy` | [Abrir](abilities/ring_of_the_seven_deadly_sins/envy.md) |
| 30 | `ring_of_the_seven_deadly_sins` | `gluttony` | `ring_of_the_seven_deadly_sins|gluttony` | [Abrir](abilities/ring_of_the_seven_deadly_sins/gluttony.md) |
| 31 | `ring_of_the_seven_deadly_sins` | `greed` | `ring_of_the_seven_deadly_sins|greed` | [Abrir](abilities/ring_of_the_seven_deadly_sins/greed.md) |
| 32 | `ring_of_the_seven_deadly_sins` | `lust` | `ring_of_the_seven_deadly_sins|lust` | [Abrir](abilities/ring_of_the_seven_deadly_sins/lust.md) |
| 33 | `ring_of_the_seven_deadly_sins` | `pride` | `ring_of_the_seven_deadly_sins|pride` | [Abrir](abilities/ring_of_the_seven_deadly_sins/pride.md) |
| 34 | `ring_of_the_seven_deadly_sins` | `sloth` | `ring_of_the_seven_deadly_sins|sloth` | [Abrir](abilities/ring_of_the_seven_deadly_sins/sloth.md) |
| 35 | `ring_of_the_seven_deadly_sins` | `wrath` | `ring_of_the_seven_deadly_sins|wrath` | [Abrir](abilities/ring_of_the_seven_deadly_sins/wrath.md) |
| 36 | `roller_skate` | `skating` | `roller_skate|skating` | [Abrir](abilities/roller_skate/skating.md) |
| 37 | `shield_of_retaliation` | `retaliation` | `shield_of_retaliation|retaliation` | [Abrir](abilities/shield_of_retaliation/retaliation.md) |
| 38 | `sphere_of_self_sacrifice` | `sacrifice` | `sphere_of_self_sacrifice|sacrifice` | [Abrir](abilities/sphere_of_self_sacrifice/sacrifice.md) |
| 39 | `springy_boot` | `bounce` | `springy_boot|bounce` | [Abrir](abilities/springy_boot/bounce.md) |

## Sinergias distintas — 2/2

| # | Relíquia proprietária | ID factual | Chave composta | Ficha |
|---:|---|---|---|---|
| 1 | `glitchy_mantle` | `electricity` | `glitchy_mantle|electricity` | [Abrir](synergies/glitchy_mantle/electricity.md) |
| 2 | `kinetic_belt` | `electricity` | `kinetic_belt|electricity` | [Abrir](synergies/kinetic_belt/electricity.md) |

## Condicionantes

**⚠️ QA físico pendente:** equip/unequip Curios, rank e XP, modo e state persistence, cooldown/buffer, targeting FTB Teams, convivência com Reliquified, Sophisticated Backpacks, mortes, reinício, mudança de dimensão e testes do modpack completo. Nenhum dos 41 foi certificado por ativação real nesta materialização. **⛔** Sem hooks/API contratados, o adapter Black Arcana permanece fail-closed.

**Clean-room:** fichas contêm exclusivamente identidade/proveniência factual e limitações; não transportam código, descrição de habilidade, tooltip, assets, textos criativos nem modelo do provider.
