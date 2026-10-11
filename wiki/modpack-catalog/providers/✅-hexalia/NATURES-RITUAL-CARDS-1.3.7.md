# Hexalia 1.3.7 — 23 fichas individuais de Nature's Ritual

Estado: **✅ 23/23 receitas `COUNTED_SOURCE_PINNED` individualizadas** · **⚠️ config instalada/QA Survival pendentes**.

## Evidência e boundary

- Artefato físico `hexalia-neoforge-1.3.7.jar`, SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`; release source pin `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283` (correlacionado por versão, sem igualdade de bytes comprovada).
- Cada uma das 23 identidades está registrada como **`hexalia:natures_ritual` recipe ID** na [matriz source-pinned](rituals/NATURES-RITUAL-CATALOG.md); não são Iron's ou Ars spell IDs.
- A mudança do 1.3.7 conserva 19 receitas player-facing da 1.3.6, adiciona quatro novas e remove somente a receita antiga de debug não contabilizada. **+0 identidades semânticas novas nesta individualização**; as 23 já estão no ledger do provider.
- Admission: `hexalia:hex_focus`, braziers SALTED em raio horizontal 8, determinismo por distância/bloco, duração 40 ticks por offering e crops maduras condicionais `naturesRitualCropRequirement=0..32`.
- `summon_cacofey` e `summon_silk_moth` usam `requires_soul=true`, `AWAITING_SOUL` e **50 ticks** de manifestação após morte elegível com Athame; não são summons instantâneos. Provider-owned lifecycle não pode ser repetido pelo Black Arcana.
- Os **seis** Celestial Infusions distintos estão [indexados separadamente](CELESTIAL-INFUSION-CARDS-1.3.7.md); 23 + 6 = **29** ações mágicas atuais do Hexalia, já contadas. Fases e outputs não somam identidades adicionais.

| # | Recipe ID | Resultado | Processamento | Soul? | Ficha |
|---:|---|---|---|---|---|
| 1 | `hexalia:fire_node_from_ritual_table` | `hexalia:fire_node` | 2 / 80 ticks | no | [Abrir](rituals/cards/fire_node_from_ritual_table.md) |
| 2 | `hexalia:air_node_from_ritual_table` | `hexalia:air_node` | 2 / 80 ticks | no | [Abrir](rituals/cards/air_node_from_ritual_table.md) |
| 3 | `hexalia:water_node_from_ritual_table` | `hexalia:water_node` | 2 / 80 ticks | no | [Abrir](rituals/cards/water_node_from_ritual_table.md) |
| 4 | `hexalia:earth_node_from_ritual_table` | `hexalia:earth_node` | 2 / 80 ticks | no | [Abrir](rituals/cards/earth_node_from_ritual_table.md) |
| 5 | `hexalia:astrylis_from_ritual_table` | `hexalia:astrylis` | 6 / 240 ticks | no | [Abrir](rituals/cards/astrylis_from_ritual_table.md) |
| 6 | `hexalia:kelpweave_blade_from_ritual_table` | `hexalia:kelpweave_blade` | 6 / 240 ticks | no | [Abrir](rituals/cards/kelpweave_blade_from_ritual_table.md) |
| 7 | `hexalia:rootshaper_from_ritual_table` | `hexalia:rootshaper` | 6 / 240 ticks | no | [Abrir](rituals/cards/rootshaper_from_ritual_table.md) |
| 8 | `hexalia:sage_pendant_from_ritual_table` | `hexalia:sage_pendant` | 5 / 200 ticks | no | [Abrir](rituals/cards/sage_pendant_from_ritual_table.md) |
| 9 | `hexalia:bloomwrap_hat_from_ritual_table` | `hexalia:bloomwrap_hat` | 4 / 160 ticks | no | [Abrir](rituals/cards/bloomwrap_hat_from_ritual_table.md) |
| 10 | `hexalia:bloomwrap_robes_from_ritual_table` | `hexalia:bloomwrap_robes` | 4 / 160 ticks | no | [Abrir](rituals/cards/bloomwrap_robes_from_ritual_table.md) |
| 11 | `hexalia:bloomwrap_leggings_from_ritual_table` | `hexalia:bloomwrap_leggings` | 4 / 160 ticks | no | [Abrir](rituals/cards/bloomwrap_leggings_from_ritual_table.md) |
| 12 | `hexalia:bloomwrap_boots_from_ritual_table` | `hexalia:bloomwrap_boots` | 4 / 160 ticks | no | [Abrir](rituals/cards/bloomwrap_boots_from_ritual_table.md) |
| 13 | `hexalia:grimshade_from_ritual_table` | `hexalia:grimshade` | 4 / 160 ticks | no | [Abrir](rituals/cards/grimshade_from_ritual_table.md) |
| 14 | `hexalia:rabbage_seeds_from_ritual_table` | `hexalia:rabbage_seeds` | 4 / 160 ticks | no | [Abrir](rituals/cards/rabbage_seeds_from_ritual_table.md) |
| 15 | `hexalia:nautilite_from_ritual_table` | `hexalia:nautilite` | 4 / 160 ticks | no | [Abrir](rituals/cards/nautilite_from_ritual_table.md) |
| 16 | `hexalia:windsong_from_ritual_table` | `hexalia:windsong` | 4 / 160 ticks | no | [Abrir](rituals/cards/windsong_from_ritual_table.md) |
| 17 | `hexalia:lourdes_from_ritual_table` | `hexalia:lourdes` | 4 / 160 ticks | no | [Abrir](rituals/cards/lourdes_from_ritual_table.md) |
| 18 | `hexalia:aegiflora_from_ritual_table` | `hexalia:aegiflora` | 4 / 160 ticks | no | [Abrir](rituals/cards/aegiflora_from_ritual_table.md) |
| 19 | `hexalia:morphora_from_ritual_table` | `hexalia:morphora` | 6 / 240 ticks | no | [Abrir](rituals/cards/morphora_from_ritual_table.md) |
| 20 | `hexalia:cinderhew_from_ritual_table` | `hexalia:cinderhew` | 6 / 240 ticks | no | [Abrir](rituals/cards/cinderhew_from_ritual_table.md) |
| 21 | `hexalia:heartseed_from_ritual_table` | `hexalia:heartseed` | 6 / 240 ticks | no | [Abrir](rituals/cards/heartseed_from_ritual_table.md) |
| 22 | `hexalia:summon_silk_moth` | entity `hexalia:silk_moth` ×1 | 6 / 240 ticks + 50-tick manifestation after soul | yes | [Abrir](rituals/cards/summon_silk_moth.md) |
| 23 | `hexalia:summon_cacofey` | entity `hexalia:cacofey` ×1 | 8 / 320 ticks + 50-tick manifestation after soul | yes | [Abrir](rituals/cards/summon_cacofey.md) |

**⚠️ Limites:** source release-correlated não comprova byte-parity de JAR, nem configs implantadas, Survival, output verificado por gameplay ou API pública de integração. Black Arcana não cria segundo ritual/custo/world mutation. Stage 06.05 mantém status 🟡.
