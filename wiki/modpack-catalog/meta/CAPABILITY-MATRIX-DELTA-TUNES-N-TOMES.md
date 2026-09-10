# Capability Matrix Delta — Tunes n' Tomes 1.1.0-HOTFIX

## Scope

This file is a narrow Phase 2 deduplication overlay for `wiki/modpack-catalog/CAPABILITY-MATRIX.md`. It records capabilities proven by the current Tunes n' Tomes publisher surface without rewriting the monolithic historical matrix in place.

Physical/provider anchor:

- installed JAR: `tunes_n_tomes-1.1.0-HOTFIX.jar`;
- mod id: `tunes_n_tomes`;
- runtime version: `1.1.0-HOTFIX`;
- physical SHA-1: `6cac45631ea63577f8eeeab454e1df0ce8f78386`;
- exact CurseForge file: `1509193 / 8370271`;
- Minecraft / loader: NeoForge 1.21.1;
- casting substrate: Iron's Spells 'n Spellbooks;
- physical pack Iron's version: `3.16.3`;
- semantic roster: **16 current publisher-enumerated Melodic spells**, `COUNTED_RELEASE_BOUNDED` in `SEMANTIC-MAGIC-COVERAGE.md`.

The HOTFIX publisher note targets Iron's 3.16.2. Compatibility with the installed 3.16.3 remains a runtime regression gate; this delta records semantic coverage, not runtime validation.

## Capability rows affected

| Canonical capability family | Tunes n' Tomes evidence | Deduplication consequence | State |
|---|---|---|---|
| Healing / regeneration / life transfer | **Celestial Chant** is publisher-described as healing and protecting the caster/allies; **Hymn of Hope** grants ally support that varies with missing health | generic musical healing/protection/support is already provider-occupied; Black Arcana needs a distinct forbidden-magic contract rather than a renamed heal/support cast | `PROVEN PUBLISHER SEMANTICS / VALUES QA PENDING` |
| Teleport / portals / displacement | **Dal Segno** teleports to the closest Segno; **Swift Melody** places a Segno at the aimed location and can teleport the caster back through its provider behavior | marker-based return/teleport semantics are provider-occupied; do not clone Segno state or rewrite provider teleport settlement | `PROVEN PUBLISHER SEMANTICS / STATE+RUNTIME QA PENDING` |
| Telekinesis / forced movement / gravity | **Fortissimo** applies strong knockback together with deafening | musical forced displacement is provider-occupied; exact force/range is not inferred | `PROVEN PUBLISHER SEMANTICS / VALUES QA PENDING` |
| Summons / familiars / servants | **Rhapsody** is publisher-described as summoning small birds that support allies/caster | summon-like support is provider-occupied, but no persistent familiar ownership, taming, lifetime or storage semantics are inferred from the public description | `PROVEN HIGH-LEVEL SEMANTICS / LIFECYCLE OPEN` |
| Shields / wards / barriers | **Celestial Chant** provides protection and Hymn of Hope includes a low-health protective state | defensive/protective magic is provider-occupied; no barrier entity, ward geometry or Black Arcana field contract is inferred | `PROVEN PROTECTION SEMANTICS / BARRIER FORM UNVERIFIED` |
| Time / haste / slow / recurrence | **Resonance/Segno** can make provider markers cast the eligible sound/melodic spell again after the original cast; extra markers may take longer to resonate | this is recurrence/recast coverage, not proof of time manipulation. Repeated provider casts must preserve parent/child causal identity and must not be double-settled by Black Arcana | `PROVEN RECURRENCE SEMANTICS / TIMING+CAPS QA PENDING` |
| Conditional / contingency / event-triggered casting | Resonance is triggered by eligible melodic casting and **Encore** forces a targeted player to recast the last spell used | forced/triggered recast is provider-occupied. Black Arcana/RPG consumers must not infer free payment, bypass cooldowns, or create recursive proc chains without a verified provider contract | `PROVEN PUBLISHER SEMANTICS / VALIDATION+RECURSION QA PENDING` |

## Causal and authority boundary

Iron's remains authority for its generic casting substrate, spell registration framework, mana and normal provider cast settlement. Tunes n' Tomes owns its Melodic content, Segno/Resonance state and provider-specific repeated/forced-cast behavior.

Black Arcana must not:

- turn one player intent plus Resonance descendants into unrelated authoritative player casts;
- charge or refund a second resource for provider-owned settlement;
- duplicate provider cooldown, damage, healing, status or teleport results;
- infer server success from client particles/audio;
- award progression once for the parent cast and again for each consequence unless the integration contract explicitly identifies legitimate child casts;
- use Encore/Resonance as a route around Black Arcana replay protection, Backlash recursion rules or server-side targeting policy.

RPG Skill Tree may observe provider-confirmed outcomes for progression only through a real boundary. It does not become authority for Tunes or Black Arcana casting.

## What this delta does not prove

This semantic delta does not establish:

- registry IDs/classes or a stable external API;
- exact mana, cooldown, duration, damage, range, knockback or buff values;
- exact Segno persistence, ownership, cleanup or maximum marker count;
- whether each Resonance descendant consumes mana/cooldown independently or through another provider rule;
- Encore validation, PvP permission behavior or recursion guards;
- exact runtime compatibility with Iron's 3.16.3;
- any Black Arcana adapter.

All of those remain fail-closed until exact current runtime/API evidence exists.

## Phase 3 effect

Every affected capability row remains **BLOCKED** for Phase 3 gap claims. This delta adds provider evidence; it does not create a new Black Arcana feature or authorize implementation.

## Sources

- provider checkpoint: `../providers/tunes-n-tomes/README.md`
- semantic ledger: `SEMANTIC-MAGIC-COVERAGE.md`
- canonical matrix: `../CAPABILITY-MATRIX.md`
- current publisher project: `https://www.curseforge.com/minecraft/mc-mods/tunes-n-tomes-a-bards-journey`
- exact HOTFIX file: `https://www.curseforge.com/minecraft/mc-mods/tunes-n-tomes-a-bards-journey/files/8370271`
