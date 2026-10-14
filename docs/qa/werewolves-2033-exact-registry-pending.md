# Werewolves 2.0.3.3 — exact compiled action registry gate

**Audit started 2026-10-14. Status: 🟡 binary audit drafted; ⚠️ physical success unproven until Java 21 workflow finishes.**

## Authorities and invariant

- Current assembled-modlist authority: `Gustavaopere/neoforge-rpg-skilltree/main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`, position **#570**, `Werewolves-1.21-2.0.3.3.jar`, mod ID `werewolves`, installed SHA-1 **`12a400d50c6e2afdcd96caf73cb80d37877147c8`**. Do not silently switch to the newer public 2.0.3.4 version.
- Publisher CurseForge [file 7814024](https://www.curseforge.com/minecraft/mc-mods/werewolves-become-a-beast/files/7814024) for the exact installed 2.0.3.3 NeoForge 1.21.1 release.
- Source authority `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`. `src/main/java/de/teamlapen/werewolves/core/ModActions.java` declares exactly **9** `VampirismRegistries.Keys.ACTION` `DeferredRegister<IAction<?>>` callsites: `human_form`, `beast_form`, `survival_form`, `howling`, `rage`, `sense`, `fear`, `leap`, `hide_name`.
- Existing [Werewolves provider catalogue](../../wiki/modpack-catalog/providers/✅-werewolves/README.md) counts **8** normally player-reachable semantic supernatural action identities; `leap` is registered but hidden from the normal selector and lacks a confirmed normal-provider route. The source also separately documents forms, skills, bite and infection. Do not count all registrations as freely usable normal powers or double-count provider forms/skills.
- Black Arcana `main@98b9a0fe53f0b51c7d371d33355c8c55291e8ddc` after #810: frozen cohort **27/39** binary exact, **12/39** pending; no new semantic roots, minima **1857 global / 1855 scoped**.

## Compiled acceptance gate

Workflow `.github/workflows/werewolves-2033-binary-audit.yml` must:

1. Download exactly publisher file 7814024, compare SHA-1 to installed physical #570 and verify NeoForge `modId = werewolves`. A filename or a source release tag is insufficient.
2. Execute independent Java 21 `javap -c -p` inspection of `de.teamlapen.werewolves.core.ModActions` in that exact JAR, checking nine unambiguous `ACTIONS → ldc ID → invokedynamic supplier → DeferredRegister.register(String,Supplier) → putstatic FIELD` pairs and exactly nine matching declared `DeferredHolder` fields.
3. Reject missing/extra/duplicate or field-remapped actions and invalid/altered JARs. The output report is limited to the SHA digests, counts, deviations, and non-gameplay disclaimer. Synthetic Java unit tests prove only the parser behavior; passing fixtures cannot substitute for JAR inspection.

**Proof boundary:** even successful static JAR registry inspection only promotes compiled action-registration identity, not action visibility, normal-player reachability, Vampirism granted skills/cooldowns, Werewolf form/bite lifecycle, full-moon enforcement, sickness/effects, Faction data, survival acquisition or actual client/server rendering. The 8 already source-counted semantic actions remain 8; nine registrations are not nine new spells.

## Open release gates

⚠️ Actual Werewolves/Vampirism 1.10.13/Vampiric Ageing 1.4.21/Epic Fight 21.17.3.1 co-loaded QA has not been observed. Howling AABB, Sense radius/cooldown, Leap reachability, bite cooldown, day/full-moon transitions, form render, authority on PvP/claims and save/restart remain live physical checks. `Stage 06.05` remains 🟡; no existing `RPG Skill Tree` adapter/Mastery/perks authorization. Black Arcana does not duplicate Vampirism's faction state or action engine.

**Recording rule:** Do not mark `COUNTED_EXACT` or 28/39 until the exact JAR workflow itself shows PASS for the required physical SHA and compiled registrations, and no final-head CI regressions remain.
