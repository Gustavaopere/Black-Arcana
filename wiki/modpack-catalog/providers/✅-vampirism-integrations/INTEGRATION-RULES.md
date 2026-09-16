# Vampirism Integrations 1.10.2 — Black Arcana Integration Rules

Status: `PROVIDER-NATIVE FIRST / NO DUPLICATE SETTLEMENT`

## Rule 1 — compatibility is not a new provider resource

Vampirism Integrations connects existing authorities. It must not be modeled as owning generic:

- blood;
- temperature;
- faction;
- villager conversion;
- recipe state;
- HUD information.

The corresponding upstream provider remains authoritative.

## Rule 2 — Cold Sweat owns temperature

For the current pack, Vampirism Integrations contributes a Vampire-specific modifier to Cold Sweat's `freezing_point` and `burning_point` attributes.

Black Arcana must not respond by adding another generic “Vampire cold resistance/heat weakness” value unless a separate design explicitly composes with the **final Cold Sweat result**.

Never:

- mirror the threshold into a Black Arcana temperature variable;
- apply the same 30 °C adjustment again;
- treat the 0.7 burning-point factor as a second damage multiplier;
- infer immunity to cold or automatic fire/sun damage from these threshold modifiers.

## Rule 3 — one lifecycle modifier

The Cold Sweat bridge uses modifier id `vampirism:vampire_modifier` and explicitly prevents duplicate addition.

Black Arcana must preserve this idempotency. If observing a faction transition, it should not remove/re-add or reproduce the modifier independently.

## Rule 4 — Jade is read-only presentation

The installed Jade integration exposes provider state to the player. It is not a causal gameplay event.

Do not:

- award perks/quests because Jade rendered a component;
- scrape Jade NBT/network payloads as the canonical source when Vampirism APIs/state exist;
- duplicate the same overlay under Black Arcana unless there is a separate UI requirement.

Use Jade only as a presentation surface or debugging aid.

## Rule 5 — conditional blood conversions remain Vampirism-owned

If an external blood provider is added later and one of this addon's conditional data maps activates, the conversion rate defined in Vampirism's data map is canonical for that bridge.

Black Arcana must not define a second competing rate for the same input without an explicit new conversion contract and deduplication key.

Current dormant examples include BOP blood, EvilCraft blood, Blood Magic Life Essence and Tinkers blood.

## Rule 6 — current modlist determines active capability

A compatibility counts as active only when its activation path and target provider are present.

Source files, Gradle dependencies, deployment metadata or old classes do not by themselves establish current gameplay.

This rule specifically prevents false claims for:

- MineColonies;
- Survive;
- Blood Magic;
- TConstruct;
- legacy animal integrations;
- other optional targets absent from the current 612-entry snapshot.

## Rule 7 — Jade uses an independent discovery path

The absence of `JadeModCompat` from the central loader does not mean the plugin is disabled. The installed 1.10.2 JAR contains `JadePlugin` with `@WailaPlugin`.

Any future audit must therefore check **both**:

1. central `ModCompatLoader` registrations;
2. framework-native plugin discovery such as Jade annotations/data files.

## Rule 8 — failure must remain fail-closed

The central loader can unload a compat after setup failure. The Cold Sweat handler can also log once and suppress later errors.

Therefore a system that depends on a bridge must verify provider state rather than assuming that “mod installed” means “compat succeeded”.

If a required provider attribute/API is absent:

- do not fabricate a fallback bonus;
- do not silently switch to vanilla temperature;
- disable the dependent integration behavior and record the missing hook.

## Rule 9 — no MineColonies semantics without implementation evidence

MineColonies is installed and appears in build/deploy metadata, but the current source audit did not find a MineColonies runtime module/loader registration.

Do not claim colonist biting, faction recognition, conversion or blood values from Vampirism Integrations 1.10.2 unless runtime/JAR evidence proves that path.

## Rule 10 — future modlist changes trigger re-evaluation

Adding any supported target can activate dormant code/data maps without changing the Vampirism Integrations JAR.

Therefore after a modlist change involving BOP, WAILA, EvilCraft, CraftTweaker, Tough As Nails, MCA, CTOV, Guard Villagers, Blood Magic, TConstruct or Capybara providers:

1. re-run provider presence reconciliation;
2. inspect the exact activation path;
3. update capability matrix/Notion;
4. test runtime settlement before declaring it active.

## Current disposition for Black Arcana

### Cold Sweat bridge

Classification: `BRIDGE / PROVIDER-NATIVE PROGRESSION-NEUTRAL`.

Use final Cold Sweat temperature state; do not duplicate modifiers.

### Jade bridge

Classification: `INFORMATION/UI ONLY`.

No perk capability is created merely by exposing existing state.

### Dormant data-map conversions

Classification: `CONDITIONAL BRIDGE / INACTIVE CURRENT SNAPSHOT`.

Do not include in current gameplay coverage except as future re-audit triggers.

### MineColonies support claim

Classification: `BUILD/DEPLOY REFERENCE FOUND / RUNTIME IMPLEMENTATION UNPROVEN`.

Fail closed.