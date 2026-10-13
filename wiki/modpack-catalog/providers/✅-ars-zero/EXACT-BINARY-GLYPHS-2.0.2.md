# Ars Zero 2.0.2 — 22 registros binários / 18 glyphs próprios

**Prova `COUNTED_EXACT` de registry estático:** 22 inscrições `GlyphRegistry.registerSpell` diretas, 18 identidades próprias únicas e 4 variantes copied/optional. O inventário de release anterior documentava 12 das 18 raízes; foram encontrados **6 IDs adicionais**. Delta semântico estrito **+6**, mínimos atualizados **1857 global / 1855 escopo** (anteriores 1851 / 1849). Campanha física: **14/39 comprovados, 25/39 pendentes**.

## Evidência binária independente

- Artefato oficial [CurseForge file 8703997](https://www.curseforge.com/minecraft/mc-mods/ars-zero/files/8703997): `ars_zero-1.21.1-2.0.2.jar` NeoForge/Minecraft 1.21.1, **6774561 bytes**, SHA-1 `ac9b6e6f7a2bd403ee7cdc16023509fde7c4e1d0`, igual ao fingerprint físico do sibling.
- [Auditoria Java 21 #38343776242](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38343776242) **SUCCESS**, [discovery #38343636260](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38343636260) e [discovery inicial #38343528559](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38343528559). O runner conferiu o SHA, ZIP, 22 classes concretas, mod ID, 22 sufixos, identidade completa por `ArsZero.prefix`, sequência exata de 22 campos e ausência de branch no registrador.
- Cadeia comprovada: `ArsZero` chama `ModGlyphs.registerGlyphs()`, que chama `com.hollingsworth.arsnouveau.api.registry.GlyphRegistry.registerSpell` **22 vezes**.
- Os quatro augments de compatibilidade copied do Adams Ars Plus são descritos como **disabled by default** pelos próprios textos do bytecode; a **configuração efetivamente carregada** no pack não foi testada.

## Inventário 22/22

| # | ResourceLocation | Classe no JAR | Contagem |
|---:|---|---|---|
| 1 | `ars_zero:temporal_context_form` | `com.github.ars_zero.common.glyph.TemporalContextForm` | base |
| 2 | `ars_zero:near_form` | `com.github.ars_zero.common.glyph.NearForm` | base |
| 3 | `ars_zero:conjure_voxel_effect` | `com.github.ars_zero.common.glyph.ConjureVoxelEffect` | base |
| 4 | `ars_zero:conjure_arcane_shield_effect` | `com.github.ars_zero.common.glyph.ConjureArcaneShieldEffect` | base |
| 5 | `ars_zero:select_effect` | `com.github.ars_zero.common.glyph.SelectEffect` | base |
| 6 | `ars_zero:anchor_effect` | `com.github.ars_zero.common.glyph.AnchorEffect` | base |
| 7 | `ars_zero:sustain_effect` | `com.github.ars_zero.common.glyph.SustainEffect` | NEW |
| 8 | `ars_zero:push_effect` | `com.github.ars_zero.common.glyph.PushEffect` | base |
| 9 | `ars_zero:effect_beam` | `com.github.ars_zero.common.glyph.EffectBeam` | base |
| 10 | `ars_zero:zero_gravity_effect` | `com.github.ars_zero.common.glyph.ZeroGravityEffect` | base |
| 11 | `ars_zero:effect_convergence` | `com.github.ars_zero.common.glyph.convergence.EffectConvergence` | base |
| 12 | `ars_zero:effect_geometrize` | `com.github.ars_zero.common.glyph.geometrize.EffectGeometrize` | base |
| 13 | `ars_zero:discard_effect` | `com.github.ars_zero.common.glyph.DiscardEffect` | NEW |
| 14 | `ars_zero:augment_hollow` | `com.github.ars_zero.common.glyph.augment.AugmentHollow` | NEW |
| 15 | `ars_zero:augment_sphere` | `com.github.ars_zero.common.glyph.augment.AugmentSphere` | NEW |
| 16 | `ars_zero:augment_cube` | `com.github.ars_zero.common.glyph.augment.AugmentCube` | NEW |
| 17 | `ars_zero:augment_flatten` | `com.github.ars_zero.common.glyph.augment.AugmentFlatten` | NEW |
| 18 | `ars_zero:effect_conjure_blight` | `com.github.ars_zero.common.glyph.EffectConjureBlight` | base |
| 19 | `ars_zero:augment_aoe_two` | `com.github.ars_zero.common.glyph.augment.AugmentAOETwo` | COPIED |
| 20 | `ars_zero:augment_aoe_three` | `com.github.ars_zero.common.glyph.augment.AugmentAOEThree` | COPIED |
| 21 | `ars_zero:augment_amplify_two` | `com.github.ars_zero.common.glyph.augment.AugmentAmplifyTwo` | COPIED |
| 22 | `ars_zero:augment_amplify_three` | `com.github.ars_zero.common.glyph.augment.AugmentAmplifyThree` | COPIED |

**As seis novas raízes** são [Sustain](glyphs/sustain.md) (`sustain_effect`), [Discard](glyphs/discard.md) (`discard_effect`), [Hollow](glyphs/hollow.md) (`augment_hollow`), [Sphere](glyphs/sphere.md) (`augment_sphere`), [Cube](glyphs/cube.md) (`augment_cube`) e [Flatten](glyphs/flatten.md) (`augment_flatten`). É uma correção do catálogo semântico **12 → 18**, não uma adição de 22 objetos novos.

As quatro compat copied são `augment_aoe_two`, `augment_aoe_three`, `augment_amplify_two` e `augment_amplify_three`: são registradas estaticamente, mas seu papel de compatibilidade e a habilitação condicional impedem contá-las como novas capacidades próprias. Entidades, staffs, equipamentos, efeitos auxiliares e classes presentes porém não inscritas no método também não entram nessa contagem.

## Limites e arquitetura

**⚠️ PENDING:** gameplay real, config efetiva, Source/mana settlement, fusão de cast, Beam por hit, Convergence, conversão de geometria, segurança de Blight/claims, aquisição de glyphs em Survival, cliente, multiplayer e alterações de dimensão. Stage 06.05 não é promovida. A prova diz respeito a registry/ID/bytecode, não a funcionamento runtime.

Ars Nouveau/Ars Zero retêm mana, Source e spell execution do provider. Black Arcana mantém casting, hazards, Arcane Danger e `WorldEffectPolicy` próprios, sem duplicar casts, cobranças ou efeitos. RPG Skill Tree permanece sibling de progressão/Mastery/perks/gates somente por contrato real.

**Clean-room:** extração factual de identificadores e pontos de registro para interoperabilidade, sem importar código, assets ou bytecode do provider.
