# Spell Codex / Specs: Iron's Spells 'n Spellbooks Addon — 1.6.5

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 1.6.5 / IRON'S DISCOVERY+UNLOCK+CAST-GATE LAYER / 0 INDEPENDENT SPELL IDENTITIES / DEPLOYED CONFIG+REACHABILITY OPEN / +0 STRICT`

## Current physical identity

The current physical Project Library modlist captured on 2026-09-16 records:

- JAR: `specs_irons_spellbooks-1.6.5.jar`;
- mod id: `specs_irons_spellbooks`;
- runtime display: `Specs: Iron's Spells 'n Spellbooks Addon`;
- runtime: `1.6.5`;
- mixin config: `specs_irons_spellbooks.mixins.json`;
- physical SHA-1: `05349ae05cf7119bf46f45621ee578b3651563e6`;
- Minecraft / loader: 1.21.1 / NeoForge.

The sibling legacy dossier `PROJECT-INSTRUCTIONS/modlist/spell-codex-irons-spells-n-spellbooks-addon.md` documents this same line editorially as Spell Codex and records Spell Actionbar 1.1.4 as a functional dependency.

## Provider role

Specs/Spell Codex adds discovery, tier unlock, costs, respec, scroll/page economy and cast gating around existing Iron's spells. It is a progression/access layer, not a standalone spell-content addon.

Sibling-audited surfaces include:

- discovery of existing Iron's/addon spells;
- sequential tier unlock using XP + ink;
- school/spell cost and blacklist JSONs;
- page/scroll/spellbook learning routes;
- integration with Spell Actionbar loadout/casting;
- 1.6.5 `allowImbuedWeaponCasting` exception path for imbued weapon casts.

Iron's Spells remains authority for the actual spell registry, mana, cooldowns and spell effects.

## Semantic disposition

Independent provider-owned spell identities established: **0**.

The Codex references, discovers, unlocks or gates provider spells; it does not make a gated spell into a second semantic identity.

Strict semantic delta: **+0**.

## Why the provider remains ⚠️

Although the physical version and provider role are known, the deployed current pack values for Specs JSON/config are not available as authoritative evidence here.

Those values can materially affect:

- spell/school blacklists;
- per-spell and per-school unlock costs;
- imbued-weapon casting bypass;
- actual discovery/unlock reachability;
- composition with other progression gates.

Therefore Specs remains **⚠️ partial / conditioned** as a runtime/progression component even though its independent spell contribution is +0.

## Authority boundary with Black Arcana and RPG Skill Tree

- Specs owns its provider-native discovery/unlock state for Iron's spells.
- Iron's owns spell runtime, mana, cooldowns and effects.
- Black Arcana must not duplicate either provider's state or turn a Specs unlock event into authority over Black Arcana casting.
- RPG Skill Tree may supply Black Arcana/pack progression, Mastery, perks and external gates through real contracts, but must not silently overwrite Specs' native Iron's unlock ledger.
- If both Specs and RPG Skill Tree gate the same Iron's spell, the composition must be explicit and fail-closed rather than accidentally double-charging or bypassing one gate.

## Runtime QA remains separate

Relevant assembled checks include:

- discovery via pages/scrolls/spellbooks;
- XP + ink exactly-once unlock settlement;
- respec persistence;
- blacklists and synchronized config;
- Actionbar loadout integration;
- addon-school handling;
- imbued-weapon exception behavior;
- relog/restart persistence;
- no unintended double-gating with sibling progression.

## Result

**⚠️ Partial / conditioned.**

Semantic inventory: **0 independent spells**. Specs/Spell Codex is cataloged as a discovery/progression/cast-gate layer over existing Iron's spell identities.
