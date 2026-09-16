# Goety 3.1.4 — Black Arcana integration rules

Status: `PROVIDER-NATIVE FIRST / EXACT 3.1.4 INTEGRATION HOOKS NOT YET VERIFIED / FAIL-CLOSED`

## 1. Resource authority

Goety owns **Soul Energy**.

Black Arcana must not:

- create a mirrored Goety Soul Energy pool;
- derive guessed Soul Energy amounts from generic death events;
- charge/refund Goety Soul Energy outside a verified provider transaction boundary;
- convert Malum spirits, Eidolon souls/Soul Shards, Vampirism blood or Black Arcana resources into Goety Soul Energy by thematic similarity.

If no safe exact 3.1.4 resource boundary exists, direct resource integration is disabled.

## 2. Casting authority

Goety owns Focus + Wand/Staff casting semantics.

A provider-native Focus cast may be observed only through a verified causal boundary. Black Arcana must not process the same action a second time from:

- item-use animation;
- Focus selection/radial UI;
- projectile/entity appearance;
- damage event plus separate guessed cast event;
- specialized Staff behavior;
- servant spawn alone.

One causal provider cast must map to at most one external integration event.

## 3. Focus inventory is not a Black Arcana spell registry

The public 110-Focus inventory is used for semantic coverage/deduplication. It does not authorize:

- importing Goety Focuses into Black Arcana spell definitions;
- inventing registry ids from display names;
- attaching Black Arcana costs/cooldowns to Goety Focuses;
- treating a Goety category as a Black Arcana school by default.

A future cross-cast bridge must preserve Goety's own settlement and identity.

## 4. Servant ownership and lifecycle

Goety is authority for Goety servants/minions.

Black Arcana Binding/Familiar systems must not:

- overwrite Goety owner identity;
- reset provider summon pressure/caps;
- extend lifespan/persistence without an explicit supported contract;
- heal using a second resource settlement path;
- re-award summon creation from both Focus cast and entity spawn;
- count all undead/magical entities as Goety servants.

If a stable provider owner/lifecycle query cannot be proven, the entity is treated as `provider ownership unknown` rather than assigned by inference.

## 5. Summon Down / anti-bypass

Public documentation identifies **Summon Down** as provider pressure on repeated summoning. Any Black Arcana or RPG integration must preserve its provider meaning.

Never build a bridge that allows the same Goety summon to avoid Summon Down by being invoked through a different UI, loadout, perk or Black Arcana wrapper.

## 6. Ritual authority

Goety ritual admission, Soul Energy cost, ingredients, sacrifice/conversion targets and completion remain Goety-owned.

External systems may consume only provider-confirmed facts. Do not infer ritual completion from:

- particles;
- sounds;
- altar proximity;
- pedestal emptiness;
- victim death alone;
- item disappearance;
- client UI state.

Exactly-once progression/rewards require a stable completion identity or equivalent provider evidence.

## 7. Research/progression authority

Goety research gates Goety content. Black Arcana/RPG progression does not automatically unlock it.

A Black Arcana knowledge/mastery gate may require Goety research only if a supported read-only query exists. It must not write Goety research state directly.

If the exact query is unavailable, the dependent gate fails closed rather than assuming research from item possession or semantic mastery.

## 8. Lichdom / transformation authority

Goety Lichdom remains provider-owned transformation/progression.

Future Black Arcana soul/death transformations must not silently:

- reuse Goety state without a contract;
- clear/overwrite Goety transformation state;
- duplicate provider sustain/resource rules;
- treat visual/model appearance as authoritative identity.

Cross-provider identity requires a real server-side boundary.

## 9. Witchcraft / Taglock deduplication

Goety already exposes Taglock and brew/witchcraft surfaces. Before Black Arcana adds sympathetic identity tokens (hair, blood, true-name, personal-object evidence), compare the required semantics against Goety.

Decision rule:

- if Goety already provides the necessary proof/token behavior and a safe integration seam exists, reuse/integrate provider-native first;
- if behavior is only thematically similar but semantically insufficient, Black Arcana may implement an original bounded gap;
- similarity alone never creates a bridge.

## 10. World safety

Goety remains authority for its own ritual/spell world behavior. Black Arcana's `WorldEffectPolicy` governs **Black Arcana-owned** destructive effects and Black Arcana wrappers.

Do not pretend that an external Goety world mutation passed Black Arcana safety merely because Black Arcana observed it afterward.

Conversely, if Black Arcana initiates a cross-provider operation that could mutate the world, admission must remain fail-closed unless the provider seam and Black Arcana world-safety contract can both be preserved without double-processing.

## 11. RPG Skill Tree boundary

RPG Skill Tree may supply progression/mastery/perk gates through real provider contracts. It is not the Goety cast engine or Soul Energy authority.

Mastery/progression credit requires discrete causal authorship and deduplication. Do not award the same Goety action from both:

- Focus activation and resulting damage;
- summon cast and servant spawn;
- servant kill and generic owner kill unless the perk contract explicitly defines one canonical event;
- ritual sacrifice and ritual completion.

## 12. Black Arcana Arcane Danger

Goety damage/resource/progression does not automatically become Black Arcana Arcane Danger.

A future adapter may classify a Goety-origin action only when there is a verified causal boundary and explicit mapping. Never infer Arcane Resistance/Corruption/Strain from:

- Soul Energy cost alone;
- necromancy theme;
- servant usage;
- ritual category name.

Black Arcana Backlash remains Black Arcana-owned and must not be injected into provider-native Goety casts without an explicit approved bridge.

## 13. Addon boundaries

### Goety Iron 3.1

Separate provider/bridge. It may connect Goety and Iron's semantics, but those contracts must be audited under its own exact version. Do not attribute its behavior to base Goety.

### Goety Cataclysm 1.21.1-1.8.2

Separate content addon. Cataclysm-derived Focuses/servants/powers are addon-owned and excluded from the base 110 Focus count.

## 14. Failure policy

Until exact 3.1.4 integration APIs/hooks are verified:

- read-only descriptive catalog: allowed;
- semantic deduplication from public documentation: allowed with confidence label;
- direct source-internal integration: blocked;
- guessed resource mutation: blocked;
- guessed owner/progression mutation: blocked;
- guessed ritual completion: blocked;
- generic fallback that changes provider identity: blocked.

Fail closed when the safe hook does not exist.
