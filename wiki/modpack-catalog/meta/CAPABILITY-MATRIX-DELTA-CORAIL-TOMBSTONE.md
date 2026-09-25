# Capability Matrix Delta — Corail Tombstone 9.5.6

Status: `⚠️ PARTIAL / 10 COUNTED_RELEASE_BOUNDED PRAYER-RITE ACTIONS / CONFIG-CONDITIONAL CASTABLE MAGIC REMAINS`

| Tombstone capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| Grave Prayer | Ankh prayer near prayable grave; exact `onGrave` action | preserve provider cooldown/Knowledge settlement; counted once |
| enhanced prayer family | Dissonance, Empathy, Harmonization, Protection, Undead | five provider action identities; do not duplicate branches such as exorcism/zombify |
| Ritual Flute | four exact note/action paths: Heal Dead Coral, Coral Chant, Remanence, Silent Bond | preserve learned/progression state and provider melody execution; counted once per action |
| Grave Souls | provider resource used for magic enchanting/progression | do not duplicate Soul consumption |
| 11 scroll buffs | physical scrolls backed by provider MobEffects | effect/status physicalization; +0 semantic actions |
| readable Forgotten Knowledge | lore/progression documents | +0 by themselves; unlock/resulting actions counted under their action owner |
| five magic tablets | provider `ItemCastableMagic` actions | current semantic eligibility conditional on deployed `allowTablet*` config |
| Familiar/Guardian/Merchant gemstones | provider castable magic actions | current semantic eligibility conditional on deployed `allowGemstone*` config |
| Gemstone of Prayer | prayer invocation/support surface | deduplicate against the counted prayer family |
| Grave Key / Lost Tablet / Magic Scroll / Scroll of Knowledge | active magic-item surfaces | keep provider authority; semantic promotion waits for config + dedup closure |
| Knowledge of Death | provider progression/perk runtime | do not transfer authority to Black Arcana/RPG Skill Tree |
| 13 enchantments | equipment-driven magical modifiers | gear content; +0 |
| 24 effects | provider supernatural status states | status content; +0 |
| grave/death recovery | authoritative provider inventory/death lifecycle | Black Arcana must not double-process death/recovery |
| XP restoration | Tombstone death/recovery economy | never duplicate XP settlement |
| Create Aeronautics respawn compatibility | provider vehicle-respawn boundary | external runtime QA, not semantic spell overlap |

## Semantic boundary

Exact release-bounded counted actions:

- Grave Prayer: 1;
- enhanced prayers: 5;
- Ritual Flute actions: 4.

Strict semantic delta:

**+10 `COUNTED_RELEASE_BOUNDED`**.

The provider remains ⚠️ because config-sensitive castable items are not yet fully eligible/deduplicated.

## Runtime boundary

Catalog count is independent from runtime PASS.

Remain fail-closed for:

- deployed `AllowedMagicItems`;
- Soul/resource exactly-once settlement;
- prayer/rite persistence;
- grave/death lifecycle coexistence;
- multiplayer/protection;
- vehicle respawn;
- restart/reload/migration.
