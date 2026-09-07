# Eidolon: Repraised 0.5.0.2 — Progression and Resource Authority

Status: `PARTIALLY VERIFIED / SURVIVAL CHAIN NOT YET CLOSED`

## Provider-owned progression axes

The installed version exposes multiple independent progression/resource axes that must not be collapsed into a single generic magic level:

- mana;
- Light deity reputation/devotion;
- Dark deity reputation/devotion;
- research/knowledge;
- soul capability;
- altar power/capacity state;
- prayer cooldown state;
- Sign/chant knowledge and recipe availability.

## Prayer progression

Prayer requires a nearby ready Effigy. On successful prayer the provider:

1. marks the prayer time in the reputation capability;
2. adds deity reputation based on base reputation plus altar power scaling;
3. recalculates/increases max mana using current reputation and altar capacity;
4. increases current mana using reputation and altar power.

Default `PrayerSpell` parameters:

- base reputation: 1;
- power multiplier: 0.25;
- cooldown: 21000 ticks.

All are provider/server-config surfaces.

## Research gates already proven

- Fire Chant -> `Researches.FIRE_SPELL`;
- Frost Touch -> `Researches.FROST_SPELL`;
- Lay on Hands can grant `DeityLocks.HEAL_VILLAGER` when healing another damaged entity;
- Smite can grant `DeityLocks.SMITE_UNDEAD` on successful undead damage.

The complete `Researches` tree and survival acquisition sequence remain to be normalized.

## Reputation gates already proven

- Darklight Chant: Dark reputation ≥3;
- Light Chant: Light reputation ≥3;
- Dark Touch: Dark reputation ≥10;
- Holy Touch: Light reputation ≥10;
- prayers: provider-native cooldown/deity state + effigy readiness.

## Black Arcana rule

Perks may react to provider-confirmed progression state, but must not manufacture equivalent Eidolon progress. No generic perk should silently:

- add Light/Dark reputation;
- mark Eidolon research complete;
- refresh prayer cooldown;
- increase Eidolon max mana;
- create soul state;
- bypass effigy/altar requirements.

Any explicit future integration that changes one of those axes requires a dedicated provider contract and runtime test.