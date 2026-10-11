# Hexalia 1.3.7 — seis fichas de Celestial Infusion

Estado: **✅ 6/6 receitas `COUNTED_SOURCE_PINNED` individualizadas**, **⚠️ QA físico, config e runtime provider-native não medidos**.

## Evidência e deduplicação

- JAR `hexalia-neoforge-1.3.7.jar`, SHA-1 físico `ca90edf1664cf6d44fe7e5318c71069050499c7e`; source release pin `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`.
- Source 1.3.7 e o checkpoint 1.3.6 preservam seis blobs de receita e classes-base iguais, sem inferir byte equality com o JAR físico.
- Contrato: Ritual Brazier, `hexalia:hex_focus`, céu aberto, três blooms em raio horizontal 3 no mesmo Y, **sem salt gating**, channel **120 ticks**, input/pending output/sol/blooms válidos a cada tick, um output e degradação de três flores.
- As quatro infusões Moonweave produzem armor set que afeta duração dos oito brews padrão (**1,5x**) sob autoridade Hexalia. Esses efeitos downstream não criam novos feitiços.
- Seis infusões + [23 Nature's Rituals](NATURES-RITUAL-CARDS-1.3.7.md) = **29** magic actions já contadas. **+0 novas identidades semânticas** nesta materialização.

| # | Recipe ID | Input | Output | Ficha |
|---:|---|---|---|---|
| 1 | `hexalia:galeberries_from_celestial_infusion` | `minecraft:glow_berries` | `hexalia:galeberries` | [Abrir](infusions/cards/galeberries_from_celestial_infusion.md) |
| 2 | `hexalia:celestial_crystal_from_celestial_infusion` | `minecraft:amethyst_shard` | `hexalia:celestial_crystal` | [Abrir](infusions/cards/celestial_crystal_from_celestial_infusion.md) |
| 3 | `hexalia:moonweave_hood_from_celestial_infusion` | `hexalia:silkweave_hood` | `hexalia:moonweave_hood` | [Abrir](infusions/cards/moonweave_hood_from_celestial_infusion.md) |
| 4 | `hexalia:moonweave_mantle_from_celestial_infusion` | `hexalia:silkweave_mantle` | `hexalia:moonweave_mantle` | [Abrir](infusions/cards/moonweave_mantle_from_celestial_infusion.md) |
| 5 | `hexalia:moonweave_bindings_from_celestial_infusion` | `hexalia:silkweave_bindings` | `hexalia:moonweave_bindings` | [Abrir](infusions/cards/moonweave_bindings_from_celestial_infusion.md) |
| 6 | `hexalia:moonweave_footwraps_from_celestial_infusion` | `hexalia:silkweave_footwraps` | `hexalia:moonweave_footwraps` | [Abrir](infusions/cards/moonweave_footwraps_from_celestial_infusion.md) |

**⚠️** Não comprovados no modpack físico: config, sky/environment snapshots, cancelamento em desconexão, ownership de blooms, output, claims e APIs. Sem contrato real, integração fail-closed. Stage 06.05 não muda.
