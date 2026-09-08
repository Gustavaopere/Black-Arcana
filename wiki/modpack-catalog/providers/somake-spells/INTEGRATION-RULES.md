# Somake Spells — regras de integração para Black Arcana

## Authority split

Somake is the provider/owner of its own spell content, Aqua/Symmetry content, Elemental Charges, book/grimoire/Upgrade Forge progression, equipment evolution and Soul Fire/Infernal Fire ritual progression.

Iron's Spells 'n Spellbooks remains the casting/school substrate where Somake registers Iron's-native content.

Black Arcana remains authority for its own casting pipeline, forbidden spell domains, hazards, rituals, WorldEffectPolicy, Corruption, Strain, Arcane Danger, persistence and replay/cost safety.

RPG Skill Tree remains a sibling progression/mastery/perk provider only. It must not own Somake or Black Arcana magic runtime state.

## Provider-native first

For any future Somake bridge:

1. confirm `somakespells` exact installed version;
2. identify the real registry/content ID involved;
3. identify a stable provider/Iron's boundary;
4. consume provider-owned state rather than mirroring it;
5. preserve causal ownership and costs;
6. avoid duplicate listeners/effects/rewards;
7. fail closed when an exact hook is unavailable.

A name in a changelog is not an API contract.

## Elemental Charges

Do not create a Black Arcana `SomakeCharge`, duplicate stack counter or inferred data attachment.

The installed fix explicitly repairs Symmetry/Spirit Charge buffs, proving that Somake owns charge-state semantics in the current line. Exact generation, cap, expiry, buff and synchronization mechanics remain unknown.

Any perk that wishes to react to Somake charges must wait for a real read-only provider boundary. It must not infer charge state from particles, item names, damage type or spell name.

## Aqua School and T.O Magic coexistence

Current physical stack includes both Somake 1.0.8-fix and the deprecated T.O Magic 1.21.1 alpha (`traveloptics` 4.4.0.1).

Rules:

- do not assume that Somake Aqua has already migrated to T.O Magic;
- do not assume that T.O's deprecated alpha is harmless or inactive;
- do not register a third Aqua school in Black Arcana;
- do not bridge by display-name matching;
- if duplicate schools/IDs are observed, stop and document exact runtime evidence before writing compatibility code.

A future adapter needs explicit registry identity and runtime tests with both artifacts loaded.

## Ritual progression

Somake's Altar-of-Ignis/pedestal path for Soul Fire and Infernal Fire is provider-owned.

Black Arcana must not:

- complete Somake ritual objectives in parallel;
- grant Somake necklaces/staff upgrades from a second listener;
- consume/duplicate Somake ingredients speculatively;
- convert the provider's ritual into a Black Arcana ritual merely because it is occult/infernal.

Black Arcana may create distinct forbidden rituals only when their mechanics, costs, authority and reward state are materially different.

## Connection / transfer spells

Public 1.0.7 semantics include:

- Guardian Connetion — target damage prevention with redirected hits to caster;
- Blessed Connetion — shared healing;
- Cursed Connection — shared damage;
- Chain Connection — movement-distance tether, moved to Aqua in 1.0.8.

These mechanics are high risk for double-processing. Black Arcana must not add generic global damage/heal redirection hooks intended to "support" them without exact provider identity checks and replay/dedup guards.

Backlash must not trigger normal offensive proc chains through redirected Somake damage.

## Bloodmark

Bloodmark's public release semantics use repeated casts to define a persistent damage zone.

Do not:

- maintain a parallel point list;
- add a second zone tick pipeline;
- independently persist or reconstruct the zone;
- treat it as a Black Arcana Forbidden Domain.

Black Arcana domains remain their own bounded server-authoritative state machine.

## Water Control / Aqua

Water Control is publicly described as a channeled, aim-following water mass.

Do not infer:

- block placement/destruction;
- fluid source manipulation;
- entity type;
- per-tick scan/raycast implementation;
- WorldEffectPolicy interaction.

If runtime evidence later shows real world mutation, any Black Arcana-triggered destructive/environmental effect still passes through Black Arcana's WorldEffectPolicy; provider-native Somake behavior remains owned by Somake.

## Firestorm Vortex / control effects

Do not add a duplicate pull/burn listener to Somake's vortex. If Black Arcana later has a forbidden vortex, it needs distinct causal semantics, budgets/caps and bounded effect processing.

## Damage immunity / negation

Guardian Connetion and The Rose's Secret occupy damage prevention/negation space.

Any Black Arcana immunity/ward candidate must be deduplicated semantically and must not stack by accidental duplicate cancellation listeners. Exact priority/order with Iron's/NeoForge events is runtime-QA pending.

## Optional integrations

Current pack has Born in Chaos, Geomancy Plus, Tunes 'n Tomes and Mowzie's Mobs. Magic From the East and Better Combat are not present.

Do not hard-depend on an optional provider merely because it is present in this pack snapshot. Somake's own optional gating remains provider authority.

For Magic From the East absence, the 1.0.8 publisher says most relevant Symmetry content becomes ice-based. Treat that as publisher-described expected behavior, not as proof of exact current spell IDs/damage types until runtime inspection.

For Born in Chaos presence, the publisher says ritual progression can extend to Infernal Fire. Runtime QA must still confirm current config/recipe reachability.

## Performance / safety

No Somake integration may introduce:

- global per-tick registry/entity scans;
- duplicate damage/heal pipelines;
- unbounded area scans;
- duplicate resource ledgers;
- client-authoritative spell state;
- inferred replay/cooldown state.

Adapters should be event/identity-driven, bounded and server authoritative where Black Arcana owns the action.

## Fail-closed trigger conditions

Disable/withhold a Somake-specific integration when:

- mod id/version differs from audited expectations and contract compatibility is unknown;
- target registry ID cannot be proven;
- T.O/Somake Aqua collision cannot be resolved safely;
- required provider API is absent;
- only display names/particles/tooltips are available as identifiers;
- double-processing cannot be ruled out.

Fail-closed means the optional integration does nothing; it does not emulate Somake behavior.