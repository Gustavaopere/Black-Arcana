# Ars Morph 2.0.0 — engenharia individual para perks

**✅ 1/1 glyph registrado no source alinhado à release e com ficha standalone nesta branch**; source `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`; installed JAR `ars_morph-1.21.1-2.0.0.jar`, SHA-1 `68ff47cc58c0ffe9570bb907f65c2910311ed45f`. Runtime exato com Identity2 2.2.4 ⚠️ pendente.

| Objeto | Semântica exata no source 2.0.0 | Limites para perk |
|---|---|---|
| [Morph](glyphs/morph.md) | `ars_morph:glyph_morph`, `EffectMorph`, Tier II, 200 mana, sem augments; server-real-player; offhand MobJar > struck type > Spawn Egg; Identity2 `morph`/ `clearMorph` | HP estritamente menor que `max_hp_morph` default 100; player target pode ser recipient; ⛔ adapter RPG e permissões não comprovados |

**Riscos verificáveis:** o ramo `clearMorph` de player envia partículas sem consultar um resultado; no ramo `IdentityProgression.morph` as partículas dependem de retorno true. O método não implementa timer de morph (código de duração comentado). FamiliarEntity é recusado. Morfologia, aquisição de formas e persistência pertencem ao Identity2, não Ars Morph/Black Arcana.

**Status separados:** ✅ classe source e ID declarados / ⚠️ execução e semântica exata do bytecode instalado não verificadas / ⛔ hook de progressão/gates não implementado. +0 novos objetos no ledger global.

[README](README.md) · [ficha de registro anterior](GLYPH-MORPH.md) · [padrão](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
