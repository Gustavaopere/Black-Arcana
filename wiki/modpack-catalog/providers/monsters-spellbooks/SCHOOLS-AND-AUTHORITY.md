# Schools and authority

Status: `SOURCE BASELINE / CURRENT BINARY PARITY UNVERIFIED`

## Provider schools visible at the public source pin

At official source head `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`, `ModSpellSchools` registers two provider school ids:

### `monstersspellbooks:necro`

Source-baseline ownership includes provider-defined school identity and associated spell-power/focus/resistance/cast/damage surfaces. The source spell registry also contains a large Necro family (25 handles at this pin).

Deduplication boundary:

- Necro is **not** automatically Black Arcana Souls & Death;
- Necro is not Goety Soul Energy;
- Necro is not Malum spirit storage/rites;
- Necro does not become Black Arcana Corruption or Strain;
- Necro progression/power is not RPG Skill Tree Mastery unless a real sibling/provider contract explicitly maps it.

### `monstersspellbooks:aero`

The same source pin still registers Aero and maps it onto Iron's Evocation-oriented focus/power/resistance/cast/damage surfaces. However:

- the source spell registry has zero Aero spell registrations at this pin;
- the exact 0.0.16.3 release notes say some remaining Aero content/files were removed to avoid tag interference;
- the exact installed JAR was not extracted.

Therefore exact current Aero school registration, player availability and runtime authority are `UNVERIFIED`. No Black Arcana adapter may bind to it from this evidence alone.

## Host authority

Iron's owns its native casting/mana/spell framework. Monsters & Spellbooks extends that host with provider content. Black Arcana must preserve one causal provider cast rather than wrapping it in a second Black Arcana cast settlement.

For provider spells, Black Arcana integration must not independently:

- subtract host mana;
- recreate host cooldown/cast timing;
- duplicate provider damage/effect application;
- spawn a second provider-equivalent summon/projectile;
- award a second provider progression event;
- infer school identity from string fragments when provider metadata is unavailable.

## Black Arcana-owned channels remain separate

Black Arcana retains authority over:

- Corruption;
- Strain;
- Arcane Danger;
- Backlash restrictions;
- Black Arcana spell-domain runtime;
- Black Arcana-owned destructive world mutation through `WorldEffectPolicy`.

A provider spell may overlap semantically with one of those concepts, but overlap is evidence for deduplication, not authority transfer.