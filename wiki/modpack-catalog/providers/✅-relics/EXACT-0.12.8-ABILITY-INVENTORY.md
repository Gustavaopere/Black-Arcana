# Relics 0.12.8 — exact artifact ability and synergy inventory

Status: `COUNTED_EXACT / 20 RELICS / 39 BASE ABILITIES / 2 DISTINCT SYNERGIES / 41 TOTAL PROVIDER POWERS`

## Provenance

Physical artifact:

- `relics-1.21.1-0.12.8.jar`;
- SHA-1 `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`.

Audited publisher artifact:

- CurseForge project/file `445274 / 8158315`;
- bytes `5,007,593`;
- SHA-1 `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`;
- SHA-256 `db6f436053fe717413389e55390a5f98103ccd91cca5fe469e090bdfaef70717`.

Physical/publisher SHA-1 equality: **true**.

NON-MERGE evidence:

- exact inventory commit `2af1ea964a3367d860099e0b32422a663674fe19`;
- exact synergy-dedup evidence commit `3fa149bdf55c01ac7c3d7ffcbad4935e49545d97`;
- green CI run `36082547793`.

## Structural inventory

- 702 classes;
- 789 provider resources;
- 0 embedded jars;
- 20 base relic item classes;
- dependency mod IDs: `curios,minecraft,neoforge,octolib,relics`.

## 39 exact base ability roots

| # | Owner | Ability id |
|---:|---|---|
| 1 | chef_hat | satiety |
| 2 | chorus_staff | blink |
| 3 | clot_of_time | rewind |
| 4 | cut_glass_boot | glass |
| 5 | experience_disperser | dispersion |
| 6 | ghostly_mantle | fog |
| 7 | ghostly_mantle | gaze |
| 8 | ghostly_mantle | spectral_escape |
| 9 | glitchy_mantle | distortion |
| 10 | glitchy_mantle | glitch |
| 11 | glitchy_mantle | illusion |
| 12 | hunting_belt | pack |
| 13 | hunting_belt | slots |
| 14 | jellyfish_necklace | regeneration |
| 15 | jellyfish_necklace | shock |
| 16 | kinetic_belt | gliding |
| 17 | kinetic_belt | slots |
| 18 | leafy_mantle | camouflage |
| 19 | leafy_mantle | revival |
| 20 | midnight_mantle | constellation |
| 21 | midnight_mantle | invisibility |
| 22 | midnight_mantle | phase |
| 23 | midnight_mantle | starfall |
| 24 | piglin_mask | barter |
| 25 | piglin_mask | looting |
| 26 | piglin_mask | neutrality |
| 27 | reflective_necklace | reflection |
| 28 | rider_flute | stable |
| 29 | ring_of_the_seven_deadly_sins | envy |
| 30 | ring_of_the_seven_deadly_sins | gluttony |
| 31 | ring_of_the_seven_deadly_sins | greed |
| 32 | ring_of_the_seven_deadly_sins | lust |
| 33 | ring_of_the_seven_deadly_sins | pride |
| 34 | ring_of_the_seven_deadly_sins | sloth |
| 35 | ring_of_the_seven_deadly_sins | wrath |
| 36 | roller_skate | skating |
| 37 | shield_of_retaliation | retaliation |
| 38 | sphere_of_self_sacrifice | sacrifice |
| 39 | springy_boot | bounce |

The identity key is owner-scoped: `<relic>|<ability>`.

Modes, rank modifiers and UI variants do not increase this count.

## 2 exact synergy roots

| # | Owner | Synergy id |
|---:|---|---|
| 1 | glitchy_mantle | electricity |
| 2 | kinetic_belt | electricity |

These are distinct owner-scoped `SynergyTemplate` surfaces. They are not deduplicated solely on the shared local id `electricity`.

Exact audit evidence records:

- distinct owner classes;
- distinct synergy-relevant structural token sets;
- unequal exact hashes for title, disabled-description and enabled-description values.

No upstream prose is retained; only identity/hash/structural facts needed for catalog deduplication are preserved.

## Semantic rule

Relics exposes a provider-native discrete power model with first-class ability and synergy state, targeting, modes, ranks and progression.

For the semantic-magic ledger:

- 39 base abilities count once each;
- 2 distinct synergies count once each;
- rank modifiers/modes do not mint new semantic identities;
- the 20 relic items themselves are equipment identities, not additional magic actions.

Total:

**41 `COUNTED_EXACT` semantic powers.**

## Clean-room boundary

The audit retains only cryptographic digests, archive counts/paths, exact identity roots, class/type relationships, scoped token presence and hash comparisons required for interoperability/catalog classification.

No implementation body, assets, localization prose, models, sounds or proprietary source reconstruction are copied into Black Arcana.
