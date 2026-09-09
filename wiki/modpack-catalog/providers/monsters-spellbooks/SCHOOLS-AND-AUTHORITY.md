# Monsters & Spellbooks — schools and authority

## School registrations observed in the inspected source head

`ModSpellSchools` at public source head `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2` contains two `SchoolType` registrations under the `monstersspellbooks` namespace.

The public source metadata is not an exact 0.0.16.3 build pin. Consequently, these are source-head observations; exact installed-binary existence must be evaluated separately.

### Necro

Source identity: `monstersspellbooks:necro`.

The source assigns Necro its own focus tag, display identity, provider-owned magic-power attribute, provider-owned magic-resistance attribute, cast sound and provider-owned damage type.

This establishes a genuine **source-observed** provider school surface. The exact 0.0.16.3 release notes do not announce Necro removal and instead contain Necro visual/jewelry fixes, but exact installed class/registry parity remains outside the evidence available in this phase.

Its progression/equipment/stat semantics, when present in the installed provider, belong to Monsters & Spellbooks/Iron's, not to Black Arcana Corruption, Arcane Danger or the sibling RPG Skill Tree unless a real adapter explicitly maps them.

The current `ModSpellRegistry` source organization contains 25 spell registrations in the `necro` family.

### Aero

Source identity: `monstersspellbooks:aero`.

The inspected source head still contains an Aero SchoolType registration that reuses Iron's Evocation power/resistance, Gust cast sound and Evocation magic damage type rather than owning a parallel Aero attribute/damage stack.

However:

- exact 0.0.16.2 release notes say Aero was **soft deleted** and direct users to Snackpirate's Aeromancy;
- exact 0.0.16.3 release notes say remaining Aero content was deleted because it could disturb tags;
- the current source `ModSpellRegistry` contains **zero Aero spell registrations**;
- the inspected source tree still declares stale `mod_version=0.0.14` metadata and is not an exact 0.0.16.3 binary pin.

Therefore **the existence of `monstersspellbooks:aero` in the installed 0.0.16.3 JAR is `NÃO VERIFICADO`**. It must not be treated as a retained runtime school without exact-JAR evidence.

For Phase 2 deduplication:

- Aero contributes **0** entries to the 98 source-registration spell inventory;
- the Aero SchoolType is recorded only as a source-head observation plus release-line removal signal;
- Black Arcana must not infer an active Aero spell family or installed Aero SchoolType from the stale source tree;
- no automatic bridge to another Aeromancy provider is created from theme/name similarity.

## Source families are not automatically SchoolTypes

`ModSpellRegistry` is organized into these source families:

- blood;
- ender;
- evocation;
- fire;
- holy;
- hydro;
- ice;
- lightning;
- nature;
- necro;
- technomancy.

Only `necro` and `aero` are observed as `SchoolType` registrations in the inspected source head. This does **not** prove both survive in the installed 0.0.16.3 binary, and specifically Aero is fail-closed because the exact release line removes Aero content. The other family labels are source organization and may use Iron's schools or other provider logic inside the individual classes.

Do not convert the 11 source-family labels into 11 new schools in the capability matrix without class-level and version-appropriate evidence.

## Black Arcana boundary

- Monsters & Spellbooks/Iron's owns provider school stat calculations and spell damage types where those surfaces exist at runtime.
- Black Arcana does not mirror source-observed Necro power/resistance into its own persistent attribute ledger.
- RPG Skill Tree Mastery does not become Necro progression merely because both systems expose progression concepts.
- If a future adapter reads a provider school, it must first verify the exact installed contract, then remain read-only or transactional according to that provider hook and fail closed when the contract is unavailable.
