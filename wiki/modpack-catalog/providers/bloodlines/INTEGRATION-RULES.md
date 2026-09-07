# Bloodlines 3.0.9 — Black Arcana integration rules

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.

Base-provider authority: Vampirism `1.10.13`, audited separately.

This contract applies to every Black Arcana perk, progression bridge, quest, UI surface, spell interaction, combat effect or resource adapter that touches Bloodlines.

# 1. Provider-native first

Bloodlines owns its own domain. Black Arcana must extend that domain without replacing it.

Provider-owned state:

- current Bloodline id;
- Bloodline rank;
- Bloodline perk-point wallet;
- Bloodline custom state;
- Gravebound Souls;
- Gravebound Phylactery ownership/storage;
- Bloodline skill eligibility/accounting;
- Bloodlines action behavior;
- Bloodline-specific join/leave lifecycle.

Vampirism remains provider authority for:

- Vampire/Hunter base faction;
- normal faction level/Lord state;
- normal skill handler and skill-tree topology;
- action handler/timers;
- Vampire blood/saturation/exhaustion;
- base refinements/actions/events.

Black Arcana must not create an authoritative duplicate for either layer.

# 2. Identity gates

Any Bloodline-specific integration must check the canonical provider state.

Minimum gate:

1. required mod/provider is loaded;
2. exact Bloodline identity matches the intended Bloodline;
3. base Vampirism faction is compatible;
4. required Bloodline rank is satisfied;
5. required provider skill/action state is satisfied when applicable.

Never identify a Bloodline from:

- translated/display name;
- armor/item appearance;
- generic Vampire/Hunter status alone;
- presence of a thematically similar effect;
- cached Black Arcana copy.

Use provider registry/state identity.

# 3. Joining and leaving

Black Arcana may observe or intentionally invoke a provider-supported lifecycle only when the design explicitly requires it.

It must not emulate a join by setting a registry id, scoreboard, tag or capability mirror.

Canonical joins have additional settlement:

- skill-tree locks;
- rank/default skills;
- attributes;
- custom state;
- advancement hooks;
- sync;
- Phylactery ownership for Gravebound.

Canonical leaving has additional cleanup:

- Bloodline skill disable;
- points reset;
- custom state cleanup;
- Phylactery/possession cleanup;
- rank reset;
- attributes;
- sync.

Purity Injection + Vampirism Med Chair is the provider-native removal route in 3.0.9. If Black Arcana provides an alternate lore/UI entry point, it must still converge on equivalent provider lifecycle rather than bypassing it.

# 4. Bloodline rank progression

Ranks 2–4 are provider task/reward progressions.

Black Arcana must not:

- create Bloodline XP as an alternative rank authority;
- skip directly to a later rank by setting the integer;
- reward the same task completion twice;
- assume a task appearing in a list means its reward settled.

A bridge that intentionally grants rank must use a provider-supported transition whose precondition proves the prior rank and whose postcondition performs provider lifecycle/sync.

# 5. Bloodline perk points

Bloodline perk points are not generic Black Arcana skill points and not ordinary Vampirism skill points.

Do not convert between them by name or UI similarity.

The 3.0.9 source contains a dual-gate ambiguity between:

- Bloodlines remaining perk points;
- Vampirism ordinary `getSkillPointCost()` checks.

Until installed runtime QA resolves this:

- do not auto-pay normal Vampirism skill points for a Bloodline skill;
- do not auto-refund them;
- do not grant hidden compensating Bloodline points;
- do not bypass `canSkillBeEnabled`;
- do not implement Black Arcana respec/payment integration for Bloodline skills.

Fail closed and expose the unresolved provider state diagnostically.

# 6. Skill-tree topology

Bloodline skill registry presence does not prove reachability.

A Black Arcana perk that depends on a Bloodlines skill must verify:

- skill is registered;
- correct Bloodline tree is active/unlocked;
- parent path exists;
- Bloodline rank gate is satisfied;
- sibling choice is compatible;
- provider skill is actually enabled.

Do not silently enable a downstream skill to satisfy a Black Arcana perk.

Special blocker: Gravebound Sorcerous Strike is registered but absent from the configured Gravebound tree/default lists in the audited 3.0.9 source. Treat it as unavailable for survival-dependent Black Arcana design until runtime or provider datapack evidence proves a legitimate acquisition path.

# 7. Actions and timers

`IActionHandler` is authoritative for Bloodlines actions because all 29 are registered in Vampirism's action registry.

Black Arcana may observe:

- action activation/deactivation events;
- actual handler active/cooldown state;
- provider-specific completion events/state changes.

Black Arcana must not:

- create a second timer for the same action;
- assume the config's nominal duration equals actual duration after provider timer extensions;
- assume a button press proves action success;
- reset provider cooldowns unless an explicit approved integration is designed;
- charge a second resource cost.

Completion-sensitive rewards require a causal signal that proves provider settlement.

Example: Devour Soul activation is **not** proof that a target was devoured because the audited action can return success on an invalid LivingEntity target.

# 8. Mixed timer units

Bloodlines configs/actions mix seconds and raw ticks.

Examples:

- most action configs return `seconds * 20`;
- Crimson Leap cooldown/duration are raw ticks;
- End Mist Form cooldown is raw 20 ticks.

Never infer units from naming convention. Read the exact provider getter or use actual handler timer state.

# 9. Vampirism blood settlement

Bloodlines does not own a separate Vampire blood bar.

Provider pipeline may involve:

- `BloodDrinkEvent.PlayerDrinkBloodEvent` amount/saturation mutation;
- `VampirePlayer.drinkBlood(...)`;
- `useBlood(...)`;
- ExtendedCreature blood;
- Vampirism saturation/exhaustion.

Black Arcana may display/read or explicitly bridge the real Vampirism blood system according to the Vampirism integration contract.

It must not:

- grant a second blood reward after a Bloodlines blood hook already modified the same transaction;
- charge a Bloodknight action twice;
- copy blood amount into a parallel authoritative meter;
- treat Bloodline rank as blood capacity;
- collapse blood, Bloodline perk points and Gravebound Souls into one generic currency.

# 10. Bloodknight exactly-once rules

Bloodknight actions and feeding hooks are especially settlement-sensitive.

For every integration:

- initial action blood debit belongs to Bloodlines/Vampirism;
- periodic upkeep debit belongs to Bloodlines/Vampirism;
- Sapping Strike target debit and attacker credit must occur once;
- Vampire Blood Bottle conversions/rewards must not be duplicated;
- Feeding Frenzy/Blood Frenzy should be observed after provider application, not independently recreated.

Source discrepancy: upkeep descriptions for Sanguine Infusion/Blood Hunt/Daywalker imply one blood per interval, while implementation debits two. Source implementation is the static authority for 3.0.9 pending runtime confirmation.

# 11. Gravebound Souls

`Gravebound.State` is the sole authority for player Souls.

Do not map Souls automatically to:

- Goety Soul Energy;
- Malum spirits;
- XP;
- mana;
- Black Arcana generic Soul resource;
- any item called a soul.

Any bridge between soul systems requires an explicit design with:

- source resource identity;
- target resource identity;
- conversion rate;
- reserve/commit/refund rules;
- duplication prevention;
- causal provenance;
- caps;
- failure behavior.

No bridge exists merely because two systems use the word “soul”.

# 12. Gravebound Soul consumption

Soul-consuming actions require `currentSouls - cost > 0` in the audited shared gate. This preserves at least one Soul.

Mist Form deactivation also uses a strict `souls > requiredSouls` branch for successful payment/resurrection.

Black Arcana must preserve this exact provider behavior unless a deliberate provider patch/redesign is approved. Do not “helpfully” convert the comparison to `>=` in an integration layer.

# 13. Devour causal ownership

Valid Soul acquisition belongs to `BloodlineGravebound.devour(...)` and provider state transfer.

A Black Arcana listener may award secondary progression only after it can prove a canonical devour settled.

Deduplicate at least by the provider event/target transaction identity so that these routes cannot double-credit:

- direct Devour Soul;
- Lingering Devour;
- Soul Claiming;
- Passive Soul Claiming;
- other future provider calls to `devour(...)`.

Do not reward from generic `LivingDeathEvent` alone; unrelated deaths and already-settled provider paths share that event surface.

# 14. Phylactery authority

Phylactery state spans:

- owner UUID;
- block entity storage;
- BlockPos;
- dimension;
- player-bound state;
- storage tier based on total Souls devoured.

Black Arcana must not shadow only the BlockPos or only an owner tag and treat the binding as valid.

Provider resolution/validation must succeed.

Phylactery Soul Transfer is conservation-sensitive: transfer to player, clamp, and return overflow. A Black Arcana UI/bridge must not interpret transfer quantum as newly generated Souls.

# 15. Mist Form / resurrection

Mist Form is a provider-owned lethal-hit substitution, not generic invulnerability.

Black Arcana must preserve:

1. lethal-hit causal source;
2. vulnerable/bypass damage rules;
3. action active/cooldown gate;
4. required Soul threshold;
5. provider state/action activation;
6. health=1 interception;
7. timed Mist Form lifecycle;
8. Soul settlement or death;
9. logout anti-abuse behavior.

A Black Arcana resurrection perk must not race with or independently cancel the same lethal hit without an explicit precedence/deduplication contract.

If multiple death-prevention providers exist in the pack, their ordering must be runtime-tested and documented.

# 16. Possession

Possession is network- and entity-authority-sensitive.

Default provider whitelist contains 14 vanilla entity types only. Black Arcana must not expand eligibility by class/category matching.

Supporting a modded entity requires explicit compatibility review of:

- movement model;
- attack implementation;
- special interaction behavior;
- server authority;
- camera state;
- despawn/death/logout cleanup;
- serialization/network id assumptions.

If unsupported, fail closed rather than falling back to a generic “control mob” mechanic.

# 17. Teleport/movement actions

Movement-heavy actions can conflict with Epic Fight, stamina systems, flight mods, portals and movement providers.

High-risk Bloodlines surfaces:

- Noble Flank;
- Zealot Shadowwalk;
- Zealot Wall Climb;
- Ectotherm Dolphin Leap;
- Bloodknight Crimson Leap;
- Gravebound Mist Form flight;
- Gravebound Phylactery Teleport;
- Ghost Walk;
- Possession/Swap.

Rules:

- provider destination/safety gates remain canonical;
- server-side final positions must not be overwritten by a parallel Black Arcana movement prediction;
- client packets must be validated in dedicated server;
- failed provider movement must not trigger a success reward;
- no cross-dimension fallback for Phylactery Teleport, which is same-dimension in 3.0.9.

# 18. Environmental/light/biome gates

Zealot and Ectotherm rely on actual provider light/biome/water checks.

Black Arcana must not replace them with approximate categories where the provider result is available.

Examples:

- Shadowwalk origin + destination darkness;
- Dark Cloak current light;
- Shadow Armour/light behavior;
- Ectotherm hot/cold biome tags;
- Dolphin Leap/Ink Splash water requirement.

Modded biome/tag interoperability should be validated through the actual NeoForge/provider tags loaded in the pack.

# 19. Static discrepancies are QA gates, not integration patches

Known 3.0.9 findings:

- dual Bloodline/Vampirism skill-point gate;
- wallet charges one per enabled skill regardless of some base skill costs;
- `MaxPerkUnlocker` codec field-name inversion;
- no source cap on non-Gravebound repeating perk tasks;
- Ectotherm cross-reference to Zealot Poisoned Strike;
- unused Shadowwalk-own-distance config in audited action;
- Bloodknight upkeep comment vs implementation mismatch;
- Sorcerous Strike Wither config mismatch;
- Sorcerous Strike survival reachability gap;
- Devour action success without guaranteed devour;
- strict Mist Form reserve-one comparison;
- client-side Wall Climb movement;
- source Heinous Elixir default 15 s vs public README prose mismatch.

Black Arcana must not silently correct any of these. Either:

1. preserve provider behavior and document it;
2. patch Bloodlines intentionally as a separate compatibility change with tests;
3. fail closed if the behavior blocks a safe integration.

# 20. Server authority and anti-abuse

All reward-affecting Black Arcana integrations must settle server-side.

Client/UI may request or display; it must not be authority for:

- rank;
- points;
- blood;
- Souls;
- devour completion;
- Phylactery transfer;
- resurrection success;
- possession target eligibility;
- cooldown completion.

Anti-abuse requirements:

- exactly-once settlement key for repeated events/packets;
- no duplicate rewards across direct + passive Soul Claiming routes;
- no reward from canceled/failed action;
- no logout bypass around Mist Form;
- no resource refund unless a debit was committed by the integration itself;
- no client packet granting progression without server verification.

# 21. Fallback policy

Fallback means **disable the integration**, not “approximate the effect”.

If Bloodlines/Vampirism contract is unavailable or version-incompatible:

- hide/disable dependent Black Arcana perk/action/bridge;
- preserve provider data untouched;
- provide diagnostic logging/telemetry;
- avoid generic stat substitutions.

A fallback may use a different provider only when the design explicitly defines that provider as an equivalent authority and deduplication between them is proven.

# 22. Addon layering

Vampire Spells Addon 0.0.9 is installed in the same pack but is a separate provider audit.

Do not attribute its spells/hooks/overrides to Bloodlines before that audit proves the relationship.

Integration priority after both are audited:

1. Vampirism base authority;
2. Bloodlines extension where the player Bloodline modifies that base behavior;
3. Vampire Spells Addon extension only on the exact surfaces it actually owns;
4. Black Arcana observation/bridge after provider settlement.

Any competing override must be resolved per concrete hook/event/mixin rather than by mod load order assumption.

# 23. Minimum runtime validation before enabling a Bloodlines bridge

A bridge may leave design/documentation state only after the relevant subset of these tests passes in the installed pack:

- exact mod versions loaded;
- base faction/Bloodline/rank gates;
- BloodlineManager persistence/sync;
- skill dual-gate behavior;
- provider action actual timer/cost;
- resource debit/credit conservation;
- causal success event/state;
- duplicate-event protection;
- dedicated-server behavior;
- death/logout behavior when relevant;
- movement/teleport safety when relevant;
- Phylactery ownership/state when relevant;
- interoperability with Vampirism 1.10.13;
- interoperability with Vampire Spells Addon after separate audit.

Until then, integrations remain `DESIGN/SOURCE-VALIDATED / RUNTIME FAIL-CLOSED`.