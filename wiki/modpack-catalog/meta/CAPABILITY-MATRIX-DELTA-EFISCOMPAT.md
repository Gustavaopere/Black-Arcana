# Capability Matrix Delta — `efiscompat` 3.1.0

Scope: physical `efiscompat` 3.1.0 + exact official 1.21.1 source revision `domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4`.

| Capability / surface | Exact provider evidence | Authority | Black Arcana disposition |
|---|---|---|---|
| Standalone spells | 0 provider spell registrations in exact source surface | none | do not inflate spell catalog |
| Iron's spell lookup | existing Iron's `SpellRegistry` queried by spell ID/name | Iron's | read identity only; no BA ownership |
| Mana / spell effect / targeting | no provider-owned system | Iron's for Iron's casts | no duplicate resource/effect/targeting path |
| Pre-cast gate | `SpellPreCastEvent` canceled if Epic Fight stunned or recent-action delay rule fails | Iron's event + `efiscompat` reconciliation policy | do not import as BA global cast rule |
| Skill interruption | `SkillContainer.requestCasting` cancels active Iron's cast then allows skill | `efiscompat` + Iron's cancel utility | provider-native first; do not double-cancel |
| Guard interruption | executable guard can cancel active Iron's cast | `efiscompat` policy over Epic Fight/Iron's | do not shadow |
| Dodge interruption | executable dodge can cancel active cast when config enabled | `efiscompat` policy | do not shadow |
| Cancellation cooldown flag | provider chooses boolean passed to Iron's cancellation utility; continuous casts force true in guard/dodge paths | Iron's cooldown semantics, compat policy | no second cooldown ledger |
| `ComboBasicAttack` compat | server attack blocked while Iron's casting | targeted compat mixin | target owner/presence in physical pack unverified; fail-closed |
| Cast completion/cancel cleanup | Iron's lifecycle seams clear Epic Fight animation layers | `efiscompat` presentation reconciliation | no gameplay reprocessing |
| Epic Fight animation registry | 35 provider animation accessors | `efiscompat` presentation | 0 spell identities; do not copy assets |
| Animation JSON reload | `SpellAnimationLoader` under `spell_animations` | `efiscompat` presentation data | not a spell registry |
| Animation mapping schema | 9 chant/cast/continuous + staff-left/right roles | `efiscompat` presentation | not a BA domain/cast schema |
| Default animation fallback | missing mapping/fields fall back to `default` | `efiscompat` presentation | no gameplay semantics inferred |
| Staff detection | Iron's `StaffItem` or provider-configured item ID | Iron's item class + compat config | not BA equipment taxonomy |
| Required mixins | 12 total: 6 client + 6 common | provider implementation | runtime target parity remains QA |
| Common config | 6 keys | provider | honor provider behavior; no BA config duplication |
| Network authority | no provider-owned spell protocol observed; animation uses Epic Fight synchronization | Epic Fight / Iron's host runtimes | no BA network bridge inferred |
| Corruption / Strain / Arcane Danger | none | Black Arcana | no conversion/coupling |
| RPG progression | none | RPG Skill Tree only via its own contracts | no progression identity created |
| World effects | none | host spell/provider + BA own policy for BA effects | no `WorldEffectPolicy` bypass |

## Deduplication result

The physical modpack already contains a dedicated provider-native solution for the Iron's↔Epic Fight casting interaction represented here. Black Arcana must not install a second observer that independently cancels Iron's casts on the same Epic Fight guard/dodge/skill actions or adds a parallel animation adapter for Iron's.

## Future BA/Epic Fight gap

This component does **not** prove that Black Arcana-native casts are integrated with Epic Fight. That is a distinct future gap, not permission to route BA spells through Iron's merely to inherit `efiscompat` behavior.

A future BA adapter must:

- be driven by BA canonical server-authoritative cast state;
- use a verified physical Epic Fight contract;
- preserve BA transactional cost/replay semantics;
- define deterministic cancellation ordering;
- avoid double-processing Iron's/provider events;
- remain behind an optional fail-safe integration boundary.

## Gap-analysis result

`efiscompat` contributes **zero spell gaps** and one closed cross-domain provider component. Its relevant value to Black Arcana is authority/deduplication knowledge: Iron's↔Epic Fight reconciliation already exists and must remain provider-owned.