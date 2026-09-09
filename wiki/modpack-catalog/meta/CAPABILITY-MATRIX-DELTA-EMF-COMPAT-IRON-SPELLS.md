# Capability Matrix Delta — EMF Compat: Iron's Spells 2.0.0

Scope: physical `emf_compat_iron_spells` 2.0.0 + exact official source revision `79d730a9d02275b7d721967c75f5f22dc815d9dc`.

| Capability / surface | Exact provider evidence | Authority | Black Arcana disposition |
|---|---|---|---|
| Standalone spells | 0 in exact subproject | none | do not inflate spell catalog |
| Schools / mana / cooldowns | no provider registration/ownership | Iron's | no duplicate resource/cooldown/school path |
| Cast state | reads `ClientMagicData`; local immediate, remote synced | Iron's | presentation input only; never BA cast authority |
| Third-person arm pose | `PlayerModelMixin` captures left/right arms at `setupAnim` RETURN, priority 2500 | EMF Compat presentation | do not double-capture/restore provider pose |
| First-person arm pose | `PlayerRendererMixin` restores saved arm/sleeve rotations before rendering | EMF Compat presentation | no gameplay significance |
| EMF animation pause | mixin unpauses EMF during Iron's cast except explicit entity pause | EMF + compat | no BA timing/proc semantics inferred |
| First-person vanilla model | registered EMF condition while local first-person cast + Iron's arm/item display | EMF Compat | presentation only |
| Pose merge priority | source `iron_spells`, priority 10 | EMF Compat Core | not combat/cast priority |
| Master switch | `ironspells.enabled`, default true | provider client config | honor provider config; do not override |
| Body-follow mode | `ironspells.bodyFollowArms`, default true | provider client config | visual mode only |
| Network payloads | none in exact addon surface | none | no network bridge to BA |
| Server events/world effects | none in exact addon surface | none | no WorldEffectPolicy interaction |
| Corruption / Strain / Arcane Danger | none | Black Arcana | no conversion or coupling |
| RPG progression | none | RPG Skill Tree only through its own contracts | no progression identity created by visual compat |

## Deduplication result

The physical modpack already contains a provider-native solution for the specific cross-mod presentation problem “Iron's casting arms are overwritten/frozen by EMF animations.” Black Arcana should not implement an Iron's-specific duplicate solution.

If BA needs equivalent EMF support for BA-native casting later, that is a separate BA client presentation adapter driven by BA-owned server-authoritative cast state. It must not reuse the Iron's compat mixins as BA runtime authority.

## Gap-analysis result

This component contributes **zero spell gaps** and occupies one cross-domain provider component through presentation compatibility. Closing it improves catalog completeness without creating new player abilities.
