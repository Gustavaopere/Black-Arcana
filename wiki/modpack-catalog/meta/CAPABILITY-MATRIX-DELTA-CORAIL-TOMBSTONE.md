# Capability Matrix Delta — Corail Tombstone 9.5.6

Status: `⚠️ PARTIAL / 10 COUNTED_RELEASE_BOUNDED PRAYER-RITE ACTIONS / 12 EXACT DEDUPED CONFIG-CONDITIONAL CASTABLE ACTION FAMILIES / DEPLOYED BOOLEANS MISSING`

| Tombstone capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| Grave Prayer | Ankh prayer near prayable grave; exact `onGrave` action | preserve provider cooldown/Knowledge settlement; counted once |
| enhanced prayer family | Dissonance, Empathy, Harmonization, Protection, Undead | five provider action identities; do not duplicate branches such as exorcism/zombify |
| Ritual Flute | four exact note/action paths: Heal Dead Coral, Coral Chant, Remanence, Silent Bond | preserve learned/progression state and provider melody execution; counted once per action |
| Grave Souls | provider resource used for magic enchanting/progression | do not duplicate Soul consumption |
| 11 scroll buffs | physical scrolls backed by provider MobEffects | effect/status physicalization; +0 semantic actions |
| readable Forgotten Knowledge | lore/progression documents | +0 by themselves; unlock/resulting actions counted under their action owner |
| Tablet of Assistance | player-to-player assistance/join teleport-request action | one conditional action family; `allowTabletOfAssistance` |
| Tablet of Cupidity | randomized location-search/relocation action | one conditional action family; `allowTabletOfCupidity` |
| Tablet of Guard | Spectral Wolf summon | one conditional action family; `allowTabletOfGuard` |
| Tablet of Home | respawn/home teleport | one conditional action family; `allowTabletOfHome` |
| Tablet of Recall | teleport to bound location/tomb place | one conditional action family; `allowTabletOfRecall` |
| Gemstone of Familiar | revive saved familiar | one conditional action family; `allowGemstoneOfFamiliar` |
| Gemstone of Guardian | summon Grave Guardian | one conditional action family; `allowGemstoneOfGuardian` |
| Gemstone of Merchant | improve/level villager/provider merchant trade state | one conditional action family; `allowGemstoneOfMerchant` |
| Grave Key | teleport to recorded grave/tomb location | one conditional action family; `allowGraveKey` |
| Lost Tablet | destination discovery/travel family with exact `EXPLORATION/VILLAGE/TREASURE` modes | one conditional action family, not three identities; `allowLostTablet` |
| Magic Scroll | generic stored MobEffect cast on target/nearby entities | one conditional wrapper action; effect variants remain non-additive; `allowMagicScroll` |
| Scroll of Knowledge | XP/knowledge storage-recovery/reward action | one conditional action family; internal readable-scroll rewards remain non-additive; `allowScrollOfKnowledge` |
| Gemstone of Prayer | prayer invocation/support surface | deduplicate against the counted prayer family |
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

The provider remains ⚠️ because the 12 castable action families are semantically resolved but their deployed `allow_*` booleans are not present in repository evidence.

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
