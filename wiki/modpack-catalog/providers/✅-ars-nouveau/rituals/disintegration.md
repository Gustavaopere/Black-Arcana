# Disintegration

Status: `SOURCE-PINNED 5.13.1 / HOSTILE-ENTITY PROCESSING RITUAL`

- Registry id: `ars_nouveau:ritual_disintegration`
- Class: `RitualDisintegration`
- Source cost declaration: `300`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every `60` game ticks on the server, Disintegration scans LivingEntities inside an AABB inflated by `5.0` blocks around the ritual. Eligible targets are monsters or entities in Ars Nouveau's disintegration whitelist, excluding players and the provider blacklist.

Eligible targets are discarded rather than killed through a normal damage path. Removed mobs do not drop normal items. When an entity reports XP reward, the ritual doubles that XP value and converts it into Ars Nouveau experience gems (`GREATER_EXPERIENCE_GEM` and `EXPERIENCE_GEM`).

## Source-consumption mismatch

The provider description says Source is consumed each time a monster is destroyed. In the pinned executable path, however, `setNeedsSource(true)` is reached only when at least one removed entity also produced an XP value greater than zero (`didWorkOnce`). The code does not increment that flag once per removed mob.

This is recorded as `SOURCE DESCRIPTION ↔ EXECUTABLE PATH MISMATCH / RUNTIME QA REQUIRED`; Black Arcana must not choose a preferred interpretation.

## Authority / Black Arcana boundary

Removal, XP conversion, Source accounting and experience-gem spawning remain Ars Nouveau authority. Black Arcana must not replay removal/rewards or grant normal death-proc chains for a provider action that explicitly discards entities.

Any observation for Arcane Danger/mastery must preserve one ritual causal identity rather than one action per converted entity.

## QA

Source is pinned to 5.13.1; the exact effective Source settlement and interaction with death/drop event consumers require runtime validation.