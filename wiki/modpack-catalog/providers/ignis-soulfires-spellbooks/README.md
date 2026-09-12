# Ignis Soulfires: Spellbooks — exact provider closure

Status: `INSTALLED 1.1.0 / EXACT CURSEFORGE FILE / HASH-MATCHED / ARR / BRIDGE_COMPAT + GEAR_LOOT_SUPPORT / ZERO_BRIDGE_INFRA / SEMANTIC +0`

- **JAR do pack:** `ignissoulfires_spellbooks-1.1.0.jar`
- **Mod ID:** `ignissoulfires_spellbooks`
- **Runtime:** `1.1.0`
- **Physical/audit SHA-1:** `dcde77db35b6de3562b4e6de0025746eaf68f119`
- **CurseForge exato:** project `1572171`, file `8620663`
- **Licença do artefato:** `ARR`
- **Evidência exata:** NON-MERGE PR #203, HEAD `ed807b77345cde1803767d804e26ea972c41d964`, run `34688273425`, text-only artifact `10296406134`

See [`EXACT-1.1.0-ARTIFACT-AUDIT.md`](EXACT-1.1.0-ARTIFACT-AUDIT.md).

## Classification and authority

Ignis Soulfires: Spellbooks is an exact **`BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`** provider between Cataclysm: Ignis Soulfires and Cataclysm: Spellbooks/Iron's.

Authority remains provider-native:

- Cataclysm: Ignis Soulfires owns Souled Ignitium and its base material/equipment semantics;
- Cataclysm: Spellbooks / Iron's own their spellcasting substrate and magic registries;
- this addon owns the compatibility armor/material registrations it actually contributes;
- Black Arcana owns none of those external state machines and does not duplicate armor modifiers, spell modifiers, material state, flight state, mana or cast settlement.

## Exact artifact inventory

The hash-matched 1.1.0 JAR contains **11 provider classes total**. Its own registration surfaces are:

- one `DeferredRegister<ArmorMaterial>`;
- one `DeferredRegister.Items`;
- exactly five provider item holders: Souled Ignitium Wizard helmet, chestplate, elytra chestplate, leggings and boots.

The remaining provider classes are bootstrap/client setup, armor render/animation, armor item classes, creative-tab event and layout plugin support.

Packaged provider data contains item tags and equipment upgrade/fusion/smithing recipe resources.

## Semantic closure

Clean-room constant-pool and signature inspection across every provider class finds:

- `AbstractSpell`: **0** class hits;
- `registerSpell`: **0** class hits;
- `SpellRegistry`: **0** class hits;
- `Ritual`: **0** class hits;
- `Rite`: **0** class hits;
- `Ability`: **0** class hits.

There is no provider-owned spell/ritual/equivalent-action registry in the exact artifact. The only `DeferredRegister` hits are the armor material and item registries.

Under the canonical semantic definition, items, gear, passive equipment behavior, recipes and downstream consequences do not count as semantic magic objects. Therefore Ignis Soulfires: Spellbooks 1.1.0 contributes **0** independent semantic magic objects and is classified **`ZERO_BRIDGE_INFRA`** for semantic accounting.

The strict semantic minimum remains **1250**. This zero is established from the exact artifact; it is no longer inferred from publisher armor-only prose.

## Runtime / integration boundary

This catalog closure does not approve a Black Arcana adapter. Numerical armor/spell modifiers, equip/relog idempotence, elytra behavior, ABI compatibility and full-pack runtime QA remain separate fail-closed questions.

Any future integration must use a real provider-native contract and preserve exactly-once ownership. Similar naming or material identity does not create a bridge.

## Clean-room boundary

The exact artifact and current publisher surfaces are All Rights Reserved. Inspection retained only factual cryptographic identity, metadata/resource paths, class/member/type signatures and narrow registry type/count facts.

No implementation bodies, recipe ingredient payloads, localization prose, textures, models, animations, sounds or other provider assets are copied/adapted into Black Arcana. The upstream JAR is not redistributed.
