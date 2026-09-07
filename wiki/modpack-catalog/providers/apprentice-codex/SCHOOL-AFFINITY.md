# Apprentice's Codex — School Affinity

Source checkpoint: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` / installed provider `0.9.7.1`.

## Authority

School Affinity is an Apprentice's Codex runtime layered on Iron's canonical school-power attributes. It is not RPG Skill Tree Mastery and it does not create a new spell school.

Iron's owns the underlying school registry and school spell-power attributes. Apprentice's Codex owns affinity slot assignment, potion/effect registration, catalyst binding and the resulting temporary modifiers.

## Exact slot model

The exact source reserves **25 slots**:

- **9 fixed builtin slots** for Iron's Fire, Ice, Lightning, Holy, Ender, Blood, Evocation, Nature and Eldritch schools;
- **16 extra slots** for eligible additional schools.

Builtin schools retain stable positions. Extra schools are selected deterministically from eligible loaded schools, with provider priority/deny policy and a hard 16-school extra cap. If more eligible extra schools exist than slots, the provider leaves some unsupported rather than silently inventing additional storage.

Each slot pre-registers:

- one dynamic affinity mob effect;
- one base potion;
- one long potion;
- one strong potion.

Unassigned extra slots remain registered but have no active school binding.

## Exact effect

`SchoolAffinityEffect` resolves the assigned Iron's school and its spell-power attribute. It applies a stable modifier ID per affinity slot using:

`ADD_MULTIPLIED_TOTAL = 0.10 * (amplifier + 1)`

Therefore:

- amplifier 0 = **+10%** to the assigned school's spell power;
- amplifier 1 = **+20%**.

The effect itself has no periodic tick behavior. The modifier is added/removed with the mob-effect lifecycle.

## Exact potion variants

| Variant | Duration | Amplifier | Spell-power bonus |
|---|---:|---:|---:|
| Base | 3 min | 0 | +10% |
| Long | 8 min | 0 | +10% |
| Strong | 90 s | 1 | +20% |

Potion/effect names and colors are resolved dynamically from the assigned school. Catalyst mappings are resolved by the provider and can be synchronized from server to client.

## Integration rules

Black Arcana must not:

- turn School Affinity into Arcane Resistance, Corruption Resistance, Strain mitigation or Black Arcana Mastery;
- duplicate the school-power modifier after the provider has applied it;
- assume all third-party Iron's schools receive affinity support when more than 16 eligible extra schools are present;
- assign an unsupported extra school by theme/name alone.

RPG Skill Tree may only interact with this state if a future real adapter deliberately exposes the provider's resolved school/effect state. Generic school-power bonuses should continue to use the actual provider/attribute contract rather than copying the affinity system.

## Confidence

`SOURCE-PINNED SYSTEM / EXACT SLOT COUNT+BUILTIN ORDER+EXTRA CAP+MODIFIER OPERATION+POTION DURATIONS / PACK-SPECIFIC EXTRA-SCHOOL ASSIGNMENT REQUIRES RUNTIME QA`