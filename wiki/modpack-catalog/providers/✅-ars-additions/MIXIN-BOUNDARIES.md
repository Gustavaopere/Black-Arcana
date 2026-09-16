# Ars Additions 21.3.0 — Mixin / base-provider modification boundaries

Status: `SOURCE-PINNED 11 MIXINS AUDITED AT REGISTRATION SURFACE / MATERIAL GAMEPLAY MODIFIERS CATALOGED`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

The addon declares 10 common mixins plus one client-only GUI accessor. These matter because some Ars Additions behavior is implemented by changing Ars Nouveau/vanilla execution rather than through addon registries alone.

## Gameplay-relevant common mixins

### `CasterTomeRegistryMixin`

Adds Imbued Spell Parchments generated from Ars Caster Tome recipe data to Ars basic dungeon loot. This extends loot; it does not replace Ars caster-tome authority.

### `EffectBlinkMixin`

Cancels the Ars Nouveau Blink entity-warp invocation when the spell shooter has an Explorer's Warp Scroll in off-hand. This is an explicit base-spell behavior modification. Black Arcana must not assume core Ars Blink semantics are unchanged in the full pack when this addon is present.

### `charms.PiglinAiMixin` / `charms.PiglinBruteAiMixin`

Integrate the Gilded Friendship charm with Piglin anger/neutrality behavior. Charm semantics are cataloged under `charms/gilded-friendship.md`.

### Spellweave mixins

- `spellweave.EnchantmentMixin` — excludes existing Ars perk armor and provider-incompatible items from Spellweave support.
- `spellweave.AlterationTableMixin` — converts Spellweave level into addon-owned override + Ars `ARMOR_PERKS` tier state.
- `spellweave.PerkRegistryMixin` — supplies the override PerkSlot provider layout for those stacks.

See `systems/spellweave.md`.

### Wixie mixins

- `wixie.WixieCharmMixin` — turns an Ars Enchanting Apparatus into the addon Enchanting Wixie block.
- `wixie.WixieCauldronMixin` — adds persistent output-storage connection and `IWandable` behavior to Ars Wixie Cauldrons.
- `wixie.CraftingManagerMixin` — redirects successful Wixie outputs into that storage when possible.
- `wixie.WixieCauldronAccessor` — accessor supporting the provider integration surface.

See `systems/enchanting-wixie.md`.

## Client-only accessor

`GuiAccessor` is client presentation plumbing used by Memory Crystal overlay behavior. It does not establish server gameplay authority.

## Integration rule

A Black Arcana compatibility decision must evaluate the **effective provider stack**, including these mixins. Cataloging only registered addon objects would miss actual modifications to Ars Nouveau Blink, perks, Wixie automation and dungeon loot. Conversely, mixin presence is not permission to hook or copy implementation; future integration still requires a verified exact-version seam and clean-room boundaries.
