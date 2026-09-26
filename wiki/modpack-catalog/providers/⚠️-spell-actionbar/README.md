# Spell Actionbar — 1.1.4

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 1.1.4 / IRON'S LOADOUT+HUD+QUICK-CAST SURFACE / 0 INDEPENDENT SPELL IDENTITIES / EXACT IMPLEMENTATION SURFACE NOT FULLY RECONSTRUCTED / +0 STRICT`

## Current physical identity

The current physical Project Library modlist captured on 2026-09-16 records:

- JAR: `spell_actionbar-1.1.4.jar`;
- mod id: `spell_actionbar`;
- runtime: `1.1.4`;
- physical SHA-1: `9ce785ff029f3719d1d2f626a0a2f53919b1fb45`;
- Minecraft / loader: 1.21.1 / NeoForge.

A legacy sibling dossier, `PROJECT-INSTRUCTIONS/modlist/spell-actionbar.md`, documents the same 1.1.4 line and its Iron's/Curios/Specs integration. The newer physical modlist is authority for continued installation.

## Provider role

Spell Actionbar is a UI/loadout/input layer for Iron's Spells. Published and sibling-audited behavior includes:

- spell/actionbar equip UI;
- quick-cast slots;
- Iron's spellbook/scroll integration;
- HUD for spell icons, cooldowns, mana/affordability and keybind labels;
- slot capacity influenced by the equipped Iron's spellbook;
- integration surfaces consumed by Specs/Spell Codex.

Iron's Spells remains authority for spell definitions, mana, cooldowns and spell effects. The action bar does not own a second spell registry.

## Semantic disposition

Independent provider-owned spell identities established: **0**.

The same Iron's spell shown or cast from an actionbar slot remains the same provider spell identity. UI slots, keybinds and HUD rows are not semantic magic objects.

Strict semantic delta: **+0**.

## Why the provider remains ⚠️

Physical installation and high-level role are closed, but this Black Arcana audit has not independently reconstructed the complete exact 1.1.4 implementation/API surface from the installed binary or an exact source pin.

Therefore packet/input behavior, exact persistence format and all API signatures remain fail-closed beyond the sibling/publisher evidence.

Current catalog state: **⚠️ partial / conditioned / +0 strict**.

## Authority and safety boundary

- Black Arcana must not treat actionbar selection or animation as cast success.
- Black Arcana must not create a second Iron's quick-cast settlement path.
- Mana/cooldown/effect settlement remains Iron's-owned.
- Slot shrink/return behavior must not be duplicated by another listener.
- Specs/Spell Codex may consume Actionbar gating/UI contracts, but Actionbar itself does not own discovery progression.
- RPG Skill Tree may impose its own external progression gates through verified contracts, without rewriting Actionbar or Iron's provider state.

## Runtime QA remains separate

Relevant assembled checks include:

- slot capacity with and without spellbook;
- scroll return/drop on capacity shrink without duplication;
- quick-cast exactly once;
- cooldown/mana HUD mirrors server state;
- relog/reconnect loadout reconstruction;
- keybind conflicts and Epic Fight animation coexistence;
- Specs/Spell Codex gate agreement client/server.

## Result

**⚠️ Partial / conditioned.**

Semantic inventory: **0 independent spells**. Spell Actionbar is cataloged as a UI/loadout/quick-cast interoperability component over Iron's Spells.
