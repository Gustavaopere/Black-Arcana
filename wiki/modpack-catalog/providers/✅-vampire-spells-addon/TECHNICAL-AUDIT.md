# Vampire Spells Addon 0.0.9 — Technical Audit

Status: `EXACT RELEASE 0.0.9 / SOURCE-PINNED / PROVIDER-NATIVE BRIDGE / RUNTIME QA PENDING ON IRON'S 3.16.3`

## 1. Provenance

Authority used for this audit:

- repository: `xsharov/VampireSpellsAddon`;
- official release/tag: `1.21.1-0.0.9`;
- release target commit: `2d36e94e67611a316b7311b11e4574b499025580`;
- published NeoForge asset: `vampire_spells_addon-neoforge-1.21.1-0.0.9.jar`;
- SHA-256: `8997f71035f29e4d2fe9e37dd76ca5f4b574906d1aed0914df6c119111570fed`.

The source release declares Minecraft 1.21.1 / NeoForge and Java 21. Its supported ranges are NeoForge `>=21.1.200,<21.2`, Vampirism `>=1.10.7,<1.11` and Iron's Spells `>=1.21.1-3.14.3,<1.21.1-4`.

Pack state at this checkpoint:

- NeoForge `21.1.248`;
- Vampirism `1.10.13`;
- Iron's Spells `1.21.1-3.16.3`.

All are within declared metadata ranges. However, the addon's own source compatibility audit explicitly inspected Iron's `3.16.2`; therefore 3.16.3-specific mixin/reflection compatibility remains a runtime QA requirement.

## 2. Architecture

The addon intentionally does not compile directly against parent-mod classes in its shared integration layer. Parent APIs are resolved at runtime through reflection, while platform adapters register loader events. Two narrow mixin surfaces participate in the behavior:

1. the Iron's affordability/cast path used for resource replacement;
2. the client Ray of Siphoning rendering path used for beam-direction reversal.

This architecture means metadata compatibility alone is insufficient evidence after parent updates. A descriptor/local-ordinal change can break the bridge even while version constraints still allow loading.

## 3. Provider authority

| Domain | Authority | Addon role |
|---|---|---|
| spell identity/registry | Iron's Spells | read only / classify |
| school identity | Iron's Spells | read Blood/Holy school |
| mana price | Iron's Spells | mutate only the current cast transaction where defined |
| cast eligibility/lifecycle | Iron's Spells | intercept/cancel narrowly |
| spell cooldown | Iron's Spells | modify provider event value |
| vampire identity | Vampirism | query provider API |
| player blood | Vampirism `BloodStats`/API | atomic consume/restore through provider surface |
| native Vampirism Actions | Vampirism `IActionHandler` | no ownership |
| cross-provider Blood/Holy policy | Vampire Spells Addon | authoritative bridge semantics |

No second mana, blood, cast, action or cooldown system is introduced.

## 4. Event/order contract

The addon's compatibility audit records the relevant Iron's order as:

```text
spell.checkPreCastConditions
-> SpellPreCastEvent
-> channel/cast start
-> SpellOnCastEvent
-> addon unpaid-blood abort hook
-> Iron's mana debit
-> spell implementation
-> SpellCooldownAddedEvent.Pre
```

For damage:

```text
SpellDamageEvent
-> school resistance/friendly-fire checks
-> LivingEntity.hurt
-> LivingDamageEvent.Pre
-> absorption + health change
-> LivingDamageEvent.Post
```

For healing:

```text
SpellHealEvent
-> LivingEntity.heal
-> LivingHealEvent
```

The ordering is semantically important. Resource substitution is resolved before the original mana debit/effect, while Ray/Devour restoration and Holy reflection use delivered health damage after downstream processing.

## 5. Blood resource substitution

### Eligibility

A cast is a resource-replacement candidate only when all are true:

- server-side player;
- player is a Vampirism Vampire;
- non-creative;
- spell is not `irons_spellbooks:ray_of_siphoning`;
- school is Iron's Blood;
- cast source consumes mana;
- current cast is not a recast.

### Selection rule

With default config, blood is used only if current mana cannot cover the **full** mana cost. If `alwaysUseBloodForVampireBloodSpells=true`, eligible casts use blood regardless of available mana.

### Cost formula

Source method:

```text
bloodCost = ceil(manaCost × interpolatedRatio)
```

Default configuration uses equal endpoints:

- floor mana: `20`;
- ceiling mana: `140`;
- min ratio: `0.05`;
- max ratio: `0.05`.

Therefore default behavior simplifies to:

```text
bloodCost = ceil(manaCost × 0.05)
```

This is a config default, not a permanent gameplay constant.

### Atomicity

On an eligible blood-paid cast:

1. the current Iron's event mana cost is set to zero;
2. the addon attempts the full provider blood debit;
3. if full blood payment fails, the cast is denied;
4. no partial blood debit is accepted;
5. no second mana debit should occur for the same bridge settlement.

Black Arcana must never independently debit/refund the same resource transaction.

## 6. Devour special pricing

For Vampire caster only:

- default `devourManaMultiplier = 2.0`;
- adjusted mana price is written into the current cast;
- that final adjusted price becomes the basis of any blood fallback.

This means the order is:

```text
base/final Iron's mana cost
-> Vampire Devour multiplier
-> resource-selection decision
-> possible blood cost calculation
```

Do not calculate fallback blood from the unadjusted Devour price.

## 7. Blood cooldown overlay

Every Blood School spell cast by a Vampire is eligible for cooldown scaling.

Default:

```text
vampireBloodSpellCooldownMultiplier = 2 / 3
```

Source calculation rounds the scaled tick count and keeps a minimum of 1 tick for positive cooldowns.

The addon uses the Iron's cooldown event rather than maintaining a duplicate timer.

## 8. Ray of Siphoning restoration

Ray is intentionally excluded from blood-for-mana replacement.

After delivered health damage is observed:

```text
requestedBlood = round(actualHealthDamage × rayBloodRestoreMultiplier)
```

Defaults:

- multiplier `1.0`;
- saturation `0.5`.

The bridge caps the request to free blood capacity before provider restoration. It also guards overkill by correlating delivered damage rather than the initial raw spell amount.

## 9. Devour restoration

After delivered health damage:

```text
requestedBlood = round(actualHealthDamage × devourBloodRestoreMultiplier)
```

Defaults:

- multiplier `2.0`;
- saturation `0.6`.

As with Ray, actual restoration goes through the Vampirism provider and is bounded by free capacity.

## 10. Holy damage overlay

### NPC Vampire target

If a non-player target is recognized through the Vampirism Vampire entity contract and the spell damage source is Holy, the addon doubles the Iron's spell damage event amount.

### Vampire player caster

If a Vampire player casts Holy damage and the target receives positive delivered health damage, the addon applies an equal amount of magic damage back to the caster.

The reflection is based on delivered health damage, not the early spell event amount.

## 11. Holy healing overlay

For Holy healing:

- Vampire target receives damage equal to the heal amount;
- the corresponding heal is queued for bounded correlation and suppressed at `LivingHealEvent`;
- if caster and target differ and the caster is a Vampire player, the caster also receives the heal amount as damage;
- correlation state expires/is cleared across lifecycle boundaries to prevent unrelated later heals from being suppressed.

This is not generic anti-heal logic and must not be reproduced by a second Black Arcana `LivingHealEvent` handler.

## 12. Holy utility allowlist

The exact 0.0.9 source allowlist is:

- `irons_spellbooks:angel_wing`
- `irons_spellbooks:fortify`
- `irons_spellbooks:wisp`
- `irons_spellbooks:haste`
- `irons_spellbooks:cleanse`
- `irons_spellbooks:sunbeam`

For a Vampire player:

1. pre-cast is canceled;
2. Iron's additional cast data is reset;
3. `5` magic self-damage is applied.

The allowlist is exact. A future Holy spell is not automatically a utility-cancel target merely because it belongs to the Holy school.

## 13. Deduplication rules

### Blood restoration

Do not reward or restore again from both:

- Iron's `SpellDamageEvent`;
- NeoForge damage Pre;
- NeoForge damage Post;
- resulting Vampirism blood increase.

The addon already establishes one correlated delivered-damage settlement.

### Resource payment

Do not count or charge separately:

- affordability bypass;
- `SpellOnCastEvent`;
- mana zeroing;
- Vampirism blood debit.

These are phases of one cast transaction.

### Holy healing

Do not treat both `SpellHealEvent` and the correlated suppressed `LivingHealEvent` as two separate gameplay actions.

## 14. Native Vampirism Actions boundary

The bridge touches Iron's spell casts. It does **not** convert native Vampirism Actions into spells.

Therefore no addon evidence exists to apply its mana/blood/cooldown/Holy rules to:

- Bat;
- Teleport;
- Freeze;
- Rage;
- Half Invulnerable;
- Summon Bats;
- Hunter/Lord actions;
- any other `IActionHandler` action.

That boundary remains provider-native first.

## 15. Fail-closed matrix

| Failure | Required behavior |
|---|---|
| addon absent | omit addon-specific bridge behavior |
| Iron's absent | no spell bridge |
| Vampirism absent | no Vampire-specific bridge |
| parent API reflection contract missing | disable affected bridge path and emit diagnostic |
| Iron's mixin target changed | affected resource replacement/client overlay not trusted until revalidated |
| Vampire context cannot resolve | reject Vampire-specific mutation |
| full blood debit fails | no spell settlement through blood fallback |
| duplicate cast/settlement evidence | no second external reward/debit |
| only client Ray visual evidence exists | no server gameplay mutation |
| installed Iron's 3.16.3 behavior not runtime-validated | Black Arcana adapter-specific dependency remains fail-closed |

## 16. Runtime QA matrix for the installed pack

Required against NeoForge `21.1.248`, Vampirism `1.10.13`, Iron's `3.16.3`, Vampire Spells Addon `0.0.9`:

### Load/contracts

- dedicated-server class loading;
- reflection contract marker;
- server mixin application;
- client Ray mixin application.

### Blood School

- all 10 active base Blood spells;
- sufficient mana;
- insufficient mana + sufficient blood;
- insufficient mana + insufficient blood;
- forced blood-only config;
- creative source;
- non-mana source;
- recast;
- interrupted/channeled/repeated casts;
- cooldown scaling.

### Ray/Devour

- armor;
- absorption;
- lethal overkill;
- full/nearly full blood bar;
- correct saturation/resource delta;
- no duplicate settlement.

### Holy

- ordinary living target;
- Vampirism NPC Vampire;
- Vampire player caster;
- self heal;
- targeted heal;
- area heal;
- six utility cancels;
- Cleanse targeting-data cleanup;
- pending correlation across logout/death/dimension transition.

## 17. Audit conclusion

The 0.0.9 release semantics are sufficiently source-pinned to close the **documentation/catalog** of the bridge. The installed parent versions are inside declared compatibility ranges, but Iron's 3.16.3-specific runtime/mixin validation has not been demonstrated here. Consequently:

`CATÁLOGO/CONTRATO SOURCE-PINNED = FECHADO`

`RUNTIME QA NO PACK ATUAL = PENDENTE`
