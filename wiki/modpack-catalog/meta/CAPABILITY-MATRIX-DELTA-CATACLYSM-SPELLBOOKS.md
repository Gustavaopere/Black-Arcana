# Capability Coverage Matrix — Cataclysm: Spellbooks 1.1.13 delta

Date: `2026-09-07`

This delta records only capabilities that are justified by the current publisher surface or by the explicitly non-current 1.1.11-labelled source baseline. It does **not** claim an exact 1.1.13 per-spell inventory.

Current installed identity: `cataclysm_spellbooks-1.1.13-1.21.jar` / `cataclysm_spellbooks` / `1.1.13-1.21`.

| Capability family | Evidence | Coverage consequence | Black Arcana posture |
| --- | --- | --- | --- |
| Iron's-native addon spellcasting | provider is explicitly an Iron's + Cataclysm addon; old source registers `AbstractSpell` instances into Iron's spell registry | Cataclysm: Spellbooks owns its spell content while Iron's owns shared casting/mana/school plumbing it delegates to | observe/integrate only through real boundaries; never double-charge mana, cooldown or settlement |
| Abyssal magic | current publisher identifies Abyssal as a provider school; old source baseline has seven concrete Abyssal registrations | underwater/abyssal beams, rifts, mines, buffs, melee/shockwave and grab/control territory is already materially occupied | reject cosmetic reskins; new Black Arcana abyssal-like ideas require a real semantic gap |
| Technomancy | current publisher identifies Technomancy; old source registers the school but no concrete Technomancy spells | the old source cannot enumerate current Technomancy, so Order/mechanical-control overlap is unresolved rather than absent | fail-closed for Order candidates until current Technomancy spell identities are available |
| Sand/desert sub-school | old source registers `cataclysm_spellbooks:sand` as provider school using Iron's Nature attributes/resistance/damage; six concrete Nature/Sand-section spells exist in baseline | provider already occupies sandstorms, desert projectiles/structures, amethyst and desert-boss progression semantics | preserve provider ownership; do not create a duplicate school merely to restyle desert magic |
| Fire / Ignis-derived magic | old source baseline contains nine concrete Fire/Ignis registrations | Incineration, Infernal Strike, Hellish Blade, bone projectiles/barrage, Ashen Breath and Tectonic Tremble already block several obvious Infernal candidates | Infernal remains gated against exact current provider content plus other Fire/Soul Fire providers |
| Void / gravity / displacement | old source baseline contains Void Rune, Void Bulwark, Gravity Storm and Gravitational Pull | provider already occupies several void/gravity control primitives | Space/Displacement additions must preserve the approved Black Arcana domain contract and avoid duplicate primitives |
| Cataclysm-derived summons | old baseline contains Koboldiator/Koboleton/Thrall/Amethyst Crab and other summon-oriented registrations | provider owns these summoned combat entities; a summon is not automatically a Black Arcana familiar | deduplicate by persistence/control/utility/acquisition role; do not re-own provider summons |
| Battlefield control | baseline includes gravity control, Hellish Blade locking, Malevolent Battlefield, rifts/mines/grabs and sandstorm-area effects | substantial control/AoE territory exists before considering the unknown 1.1.13 additions | Chaos/Order/Forbidden candidates require mechanical comparison, not VFX comparison |
| Destructive world effects | old source comments/implementations include terrain-affecting concepts such as Desert Winds; exact current behavior is not promoted | provider-owned terrain effects remain provider-owned | independent Black Arcana destruction still routes through `WorldEffectPolicy`; never replay provider destruction |
| Provider progression/acquisition | old source exposes Cataclysm-material-gated families such as Ignis/Burning Ashes; exact current acquisition remains pending | provider-native progression exists and must be respected if still current | do not replace with a second Black Arcana resource merely for thematic uniformity |
| New 1.1.13 boss/content | exact 1.1.13 changelog says a new boss was added | current provider surface is larger than the old source baseline | identity/mechanics remain `UNVERIFIED`; no overlap claim beyond publisher-visible existence |

## Confidence boundary

High confidence current facts:

- installed 1.1.13 identity;
- File ID `8792628`, Beta NeoForge 1.21.1;
- current publisher claim of 65 spells;
- current publisher presence of Abyssal and Technomancy;
- coarse 1.1.13 changelog.

High confidence **historical/source-baseline** facts:

- public source commit `82a0af71f051058fe515c8b1cb9168e7f972f41c` declares 1.1.11;
- 34 concrete spell registrations in that snapshot;
- provider-owned Abyssal, Technomancy and Sand schools in that snapshot.

Not established for current 1.1.13:

- exact 65 spell ids and values;
- exact current school distribution;
- current acquisition details;
- current entity/item/effect registries;
- new boss mechanics;
- supported integration/API seams.

No Phase 3 capability may treat those unknowns as empty space.