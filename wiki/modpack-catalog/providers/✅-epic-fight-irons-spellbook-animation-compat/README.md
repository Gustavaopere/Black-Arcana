# Epic Fight & Iron's Spellbook Animation Compat — 3.1.0

Status: `✅ CATALOGED / CURRENT PHYSICAL 3.1.0 / EXACT VERSION-DECLARED OFFICIAL SOURCE BRANCH / ZERO_SEMANTIC_CAST_ANIMATION_BRIDGE / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling authority records:

- JAR: `efiscompat-3.1.0.jar`;
- mod id: `efiscompat`;
- runtime: `3.1.0`;
- physical SHA-1: `4250e1c65732d70d1091cc50b84a91b6ed5b2b3f`;
- Minecraft / loader: 1.21.1 / NeoForge;
- current hosts: Epic Fight 21.17.3.1 + Iron's Spells 3.16.3.

## Exact version-declared source

Official repository: `domanhthang2110/efiscompat`.

The `1.21.1` branch resolves to `b4b58aff86e707420fac8a7c29fe647d7f5aaac4`. Its `gradle.properties` declares:

- `minecraft_version=1.21.1`;
- `mod_id=efiscompat`;
- `mod_version=3.1.0`;
- description: compatibility fix for Iron's Spellbooks animation while using Epic Fight.

This is a version-declared source pin, not a physical-JAR byte-equivalence claim.

## Exact source surface

The source tree contains **332** paths and **28 Java files**. It includes many `data/efiscompat/spell_animations/**` JSONs, including Iron's and Traveloptics spell IDs.

Those resources are animation mappings for **existing provider spell identities**.

Bounded source search establishes:

- `registerSpell`: **0**;
- `DeferredRegister`: **0**;
- spell registration surface: **0**.

The source does reference Iron's `SpellRegistry` and `AbstractSpell`, but only to:

- resolve an existing casting spell;
- select/render animation;
- synchronize/cancel animation/cast state;
- apply compatibility behavior.

It does not register a second copy of those spells.

## Provider role

Provider-owned behavior includes:

- multiple casting animations;
- staff-specific animation variants;
- held-item visibility configuration;
- cast cancellation on Epic Fight skills such as guard/roll;
- datapack-driven spell→animation mappings.

Iron's remains authority for spell identity, cast validity, mana, cooldown and spell effect. Epic Fight remains authority for its animation/combat skill state.

## Semantic disposition

Canonical disposition:

`ZERO_SEMANTIC_CAST_ANIMATION_BRIDGE`

- provider-owned semantic magic identities: **0**;
- strict semantic delta: **+0**.

A JSON mapping for `traveloptics:blackout`, `irons_spellbooks:fireball` or any other existing spell does not create a new spell identity.

## Authority boundary

EFIS owns animation/cancel interoperability. It must not become cast-success, mana/cooldown or spell-effect authority.

## Runtime QA remains separate

Still separate:

- exactly-once cast cancellation;
- first/third-person presentation;
- staff variant selection;
- datapack reload;
- current Epic Fight/Iron's API compatibility;
- coexistence with other animation layers.

## Result

**✅ Cataloged — zero-semantic cast-animation compatibility bridge.**
