# Pufferfish's Unofficial Additions — 2.2.8

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / XP-SOURCE + REWARD BRIDGE / ZERO_SEMANTIC_SKILL_XP_REWARD_BRIDGE / +0 STRICT / DEPLOYED TREE QA SEPARATE`

## Current physical identity

Sibling physical authority: current `neoforge-rpg-skilltree` dossier for row **#462**.

- JAR: `pufferfish_unofficial_additions-1.21.1-2.2.8.jar`;
- mod id: `pufferfish_unofficial_additions`;
- runtime: `2.2.8`;
- physical SHA-1: `b273ea691e027b33fb9a19fb966c5f072edfa5c0`;
- required host: Pufferfish's Skills 0.19.0;
- optional Iron's Spells integration is physically present in the pack.

This addon extends the Pufferfish Skills data model with extra experience sources, conditions/prototypes and an effect reward. It does not own a second skill-tree engine and does not register Iron's spells.

## Exact artifact closure

NON-MERGE evidence PR **#547** audits the exact current publisher artifact.

- exact-artifact run: `37137288035` — **SUCCESS**;
- evidence artifact: `11277989415`;
- evidence digest: `sha256:277c4c8d88684ab28c67e30b4419bb54a5e875f97f0fde4b95670037e8a5bdcc`;
- CurseForge project/file: `935166 / 7389968`;
- publisher SHA-1: `b273ea691e027b33fb9a19fb966c5f072edfa5c0`;
- publisher SHA-256: `2f7831975da0740fd29f9bee775ac9fe43d3650c9d0720e8c4f108241c4092d8`;
- bytes: `52,976`.

The publisher SHA-1 exactly equals the physical pack SHA-1.

See [`EXACT-2.2.8-ARTIFACT-AUDIT.md`](EXACT-2.2.8-ARTIFACT-AUDIT.md).

## Exact extension surface

The exact JAR contains **46 archive entries / 27 classes / 19 resources / 0 provider data entries / 0 packaged provider JSONs**.

Provider-owned registered extension roots include:

- experience source `pufferfish_unofficial_additions:harvest_crops`;
- experience source `pufferfish_unofficial_additions:fishing`;
- experience source `pufferfish_unofficial_additions:spell_casting` when Iron's is present;
- configurable reward `pufferfish_unofficial_additions:effect`;
- conditions/prototypes for strings, Iron's spell holders and school holders;
- powder-snow behavior keyed by the `walk_on_powder_snow` player tag.

Detailed disposition: [`EXTENSION-SURFACE-2.2.8.md`](EXTENSION-SURFACE-2.2.8.md).

## Iron's Spells integration is a bridge, not spell ownership

The exact classes read Iron's existing `SpellRegistry` and `SchoolRegistry` holders and expose cast context such as spell ID, school, rarity, level, mana cost, cast duration, charge time, cooldown and expected ticks to the **experience calculation**.

No new `AbstractSpell` registration or provider spell registry exists. Mana cost/cooldown are observed inputs; this addon must not be counted as owning or settling those spells a second time.

Therefore `spell_casting` is an XP-source identity, not a magic-action identity.

## Effect reward is configurable progression, not a fixed spell

The exact `effect` reward can be configured to grant, immunize or modify mob effects. Its concrete target effect/amplifier/duration behavior comes from the consuming skill-tree data.

The JAR packages **zero provider tree JSONs**. Consequently the reward factory does not define one fixed player-facing supernatural action by itself.

The powder-snow hook similarly checks the `walk_on_powder_snow` tag; it is a progression consequence/state, not a standalone cast.

## Semantic result

Under the Black Arcana semantic metric, the addon contributes no fixed provider-owned spell/glyph/ritual/rite/equivalent supernatural player-action roster.

Result: **`ZERO_SEMANTIC_SKILL_XP_REWARD_BRIDGE / +0 strict`**.

Concrete skills/rewards configured by external datapacks remain owned by those datapacks/content providers. Existing Iron's spells remain owned by Iron's or their actual addon provider.

## Runtime QA remains separate

Deployed tree/config contents, harvest/fishing XP rates, continuous-spell `expected_ticks`, duplicate listener protection, effect-loading behavior and server authority remain runtime/config QA. They do not reopen this addon's provider-owned semantic denominator.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_SKILL_XP_REWARD_BRIDGE`.**

Strict semantic delta: **+0**.
