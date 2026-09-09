# Monsters & Spellbooks — schools and authority

## Registered provider-owned schools in the inspected source head

`ModSpellSchools` registers two `SchoolType` objects under the `monstersspellbooks` namespace.

### Necro

Source identity: `monstersspellbooks:necro`.

The source assigns Necro its own focus tag, display identity, provider-owned magic-power attribute, provider-owned magic-resistance attribute, cast sound and provider-owned damage type.

Necro is therefore a genuine provider school surface. Its progression/equipment/stat semantics belong to Monsters & Spellbooks/Iron's, not to Black Arcana Corruption, Arcane Danger or the sibling RPG Skill Tree unless a real adapter explicitly maps them.

The current `ModSpellRegistry` source organization contains 25 spell registrations in the `necro` family.

### Aero

Source identity: `monstersspellbooks:aero`.

The inspected source still registers the Aero SchoolType, but it reuses Iron's Evocation power/resistance, Gust cast sound and Evocation magic damage type rather than owning a parallel Aero attribute/damage stack.

The exact 0.0.16.2 release says Aero was **soft deleted** and directs users to Snackpirate's Aeromancy. The current `ModSpellRegistry` contains no Aero spell registrations.

For Phase 2 deduplication:

- Aero SchoolType existence is recorded as a retained/compatibility surface;
- Aero contributes **0** entries to the 98 active source-registration inventory;
- Black Arcana must not infer an active Aero spell family merely because the school object remains registered;
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

Only `necro` and retained `aero` are proven here as provider-owned `SchoolType` registrations. The other family labels are source organization and may use Iron's schools or other provider logic inside the individual classes.

Do not convert the 11 source-family labels into 11 new schools in the capability matrix without class-level evidence.

## Black Arcana boundary

- Monsters & Spellbooks/Iron's owns its school stat calculations and spell damage types.
- Black Arcana does not mirror Necro power/resistance into its own persistent attribute ledger.
- RPG Skill Tree Mastery does not become Necro progression merely because both systems expose progression concepts.
- If a future adapter reads a provider school, it must be read-only or transactional according to a verified provider hook and must fail closed when the exact contract is unavailable.
