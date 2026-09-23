# Acolyte 1.0.3 — exact host spell references

## Evidence boundary

Physical identity from the sibling re-audit:

- `acolyte-1.0.3.jar`;
- mod id `acolyte`;
- runtime `1.0.3`.

Exact publisher artifact audited:

- CurseForge project `1534642`;
- file `8098233`;
- SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`;
- SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.

This file records **host references**, not provider-owned spell registrations.

## Explicit Iron's spell IDs in packaged Acolyte resources

The exact release contains these 29 Iron's spell resource locations in provider text/data resources:

| # | Host spell ID | Semantic owner | Acolyte contribution |
|---:|---|---|---:|
| 1 | `irons_spellbooks:acupuncture` | Iron's | +0 |
| 2 | `irons_spellbooks:arrow_volley` | Iron's | +0 |
| 3 | `irons_spellbooks:ball_lightning` | Iron's | +0 |
| 4 | `irons_spellbooks:blood_needles` | Iron's | +0 |
| 5 | `irons_spellbooks:blood_slash` | Iron's | +0 |
| 6 | `irons_spellbooks:chain_lightning` | Iron's | +0 |
| 7 | `irons_spellbooks:fire_arrow` | Iron's | +0 |
| 8 | `irons_spellbooks:firebolt` | Iron's | +0 |
| 9 | `irons_spellbooks:firecracker` | Iron's | +0 |
| 10 | `irons_spellbooks:flaming_barrage` | Iron's | +0 |
| 11 | `irons_spellbooks:flaming_strike` | Iron's | +0 |
| 12 | `irons_spellbooks:fortify` | Iron's | +0 |
| 13 | `irons_spellbooks:frost_step` | Iron's | +0 |
| 14 | `irons_spellbooks:guiding_bolt` | Iron's | +0 |
| 15 | `irons_spellbooks:gust` | Iron's | +0 |
| 16 | `irons_spellbooks:icicle` | Iron's | +0 |
| 17 | `irons_spellbooks:magic_arrow` | Iron's | +0 |
| 18 | `irons_spellbooks:magic_missile` | Iron's | +0 |
| 19 | `irons_spellbooks:poison_arrow` | Iron's | +0 |
| 20 | `irons_spellbooks:poison_breath` | Iron's | +0 |
| 21 | `irons_spellbooks:raise_dead` | Iron's | +0 |
| 22 | `irons_spellbooks:ray_of_siphoning` | Iron's | +0 |
| 23 | `irons_spellbooks:root` | Iron's | +0 |
| 24 | `irons_spellbooks:summon_swords` | Iron's | +0 |
| 25 | `irons_spellbooks:summon_vex` | Iron's | +0 |
| 26 | `irons_spellbooks:teleport` | Iron's | +0 |
| 27 | `irons_spellbooks:throw` | Iron's | +0 |
| 28 | `irons_spellbooks:wisp` | Iron's | +0 |
| 29 | `irons_spellbooks:wither_skull` | Iron's | +0 |

## Additional code-level SpellRegistry references

Two additional host spells are referenced through exact Iron's `SpellRegistry` fields in provider bytecode metadata:

| # | Host registry field | Canonical host identity | Semantic owner | Acolyte contribution |
|---:|---|---|---|---:|
| 30 | `SpellRegistry.BLOOD_STEP_SPELL` | `irons_spellbooks:blood_step` | Iron's | +0 |
| 31 | `SpellRegistry.STOMP_SPELL` | `irons_spellbooks:stomp` | Iron's | +0 |

The canonical Iron's 3.16.3 catalog already contains Blood Step and Stomp; Acolyte only references them.

## Dynamic host selection

The exact release also references:

- `SpellRegistry.getSpell(ResourceLocation)`;
- `SpellFilter.getRandomSpell(RandomSource)`;
- `WizardAttackGoal.setSpells(...)`;
- `WizardAttackGoal.setSingleUseSpell(...)`.

Consequently the 31 explicit identities above are an **explicit-reference inventory**, not proof that no other Iron's spell can ever be selected dynamically under every runtime configuration.

That distinction affects Acolyte loadout reconstruction, but not semantic ownership: any dynamically selected host spell remains an Iron's spell and contributes **+0** under Acolyte.

## Provider-owned spell search result

Exact 1.0.3 structural audit found:

- `AbstractSpell` subclass chain: **0**;
- provider spell resource paths: **0**;
- provider `spell.acolyte.*` localization roots: **0**;
- provider-owned semantic spell registrations: **0 observed**.

## Result

Acolyte's exact release has **31 explicitly named Iron's spell references** plus dynamic host-selection surfaces, but **0 independent Acolyte spell identities**.

Semantic delta: **+0**.
