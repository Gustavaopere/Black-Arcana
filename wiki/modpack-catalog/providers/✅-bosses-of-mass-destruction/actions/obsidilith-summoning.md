# Obsidilith Summoning

- Provider: **Bosses of Mass Destruction** (`bosses_of_mass_destruction`)
- Version: `1.3.3`
- Exact physical/publisher SHA-1: `446ff63afb858ad49149d24b72541739de83d38d`
- Trigger item: vanilla Eye of Ender
- Provider target: Obsidian Altar / `obsidilith_end_frame`
- Semantic type: deliberate boss-summoning ritual/action
- State: `COUNTED_EXACT`

## Identity and trigger

The exact installed artifact provides an Ender Eye interaction path through the provider's Obsidilith summon block/mixin surface. Using an Eye of Ender on the provider summon frame is the deliberate player action root.

The vanilla Eye remains the input object; BOMD owns the target frame, summon scheduling and resulting boss lifecycle.

## Server settlement

Exact-artifact inspection closes the following provider settlement:

- Eye of Ender is consumed server-side;
- the provider schedules the summon event;
- the summon frame is removed/replaced through provider logic;
- an Obsidilith entity is created and added by the provider.

Scheduler phases, particles, sounds, runes and downstream boss AI are consequences of this same root, not separate semantic identities.

## Reachability

The exact artifact packages Obsidilith arena/worldgen resources. No exact 1.3.3 provider config field was found that disables this summon action.

This is sufficient for the catalog's exact-current action/reachability classification.

## Evidence boundary

The exact physical JAR equals the audited publisher artifact. This card records the action identity, trigger, provider-owned settlement and reachability proven by the exact-artifact audit; it does not infer unstated timing, arena-generation probability or combat behavior.

Source: `../EXACT-1.3.3-ARTIFACT-AUDIT.md`.
