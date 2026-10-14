# Werewolves 2.0.3.3 — exact compiled action registry gate

**Audit 2026-10-14. Status: ✅ exact SHA-matched publisher/modlist registry proof 9/9 observed in Java21 CI; ⚠️ assembled runtime/Survival remain untested.**

## Authorities and invariant

- Current assembled-modlist authority: `Gustavaopere/neoforge-rpg-skilltree/main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`, position **#570**, `Werewolves-1.21-2.0.3.3.jar`, mod ID `werewolves`, installed SHA-1 **`12a400d50c6e2afdcd96caf73cb80d37877147c8`**. Do not silently switch to the newer public 2.0.3.4 version.
- Publisher CurseForge [file 7814024](https://www.curseforge.com/minecraft/mc-mods/werewolves-become-a-beast/files/7814024) for the exact installed 2.0.3.3 NeoForge 1.21.1 release; the first CI attempt returned HTTP 403 from the CurseForge CDN before any hash comparison. Official [Modrinth version zkd687ts](https://modrinth.com/mod/werewolves/version/zkd687ts) of the same 2.0.3.3 release is now the candidate download. **Neither filename nor release page proves equality; SHA-1 matching the sibling physical entry remains mandatory.**
- Source authority `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`. `src/main/java/de/teamlapen/werewolves/core/ModActions.java` declares exactly **9** `VampirismRegistries.Keys.ACTION` `DeferredRegister<IAction<?>>` callsites: `human_form`, `beast_form`, `survival_form`, `howling`, `rage`, `sense`, `fear`, `leap`, `hide_name`.
- Existing [Werewolves semantic coverage row](../../wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md) counts **8** provider-native semantic actions: three player forms, Howling, Rage, Sense, Fear and **Leap**. `leap` is hidden from the normal selector but the source-located survival-tree skill and dedicated-server input path support its catalog inclusion; that input has not been run in gameplay. **`hide_name` is registered but excluded from the strict semantic count because it controls client-facing name display.** Forms, passive skills, bite and infection have separate provider-native classifications; nine registered action fields do not imply nine semantic objects.
- Black Arcana `main@98b9a0fe53f0b51c7d371d33355c8c55291e8ddc` after #810: frozen cohort **27/39** binary exact, **12/39** pending; no new semantic roots, minima **1857 global / 1855 scoped**.

## Compiled acceptance gate

Workflow `.github/workflows/werewolves-2033-binary-audit.yml` must:

1. Download exact release 2.0.3.3 via official Modrinth version zkd687ts (CurseForge file 7814024 initially returned HTTP 403), compare SHA-1 to installed physical #570 and verify NeoForge `modId = werewolves`. A filename or a source release tag is insufficient.
2. Execute independent Java 21 `javap -c -p` inspection of `de.teamlapen.werewolves.core.ModActions` in that exact JAR, checking nine unambiguous `ACTIONS → ldc ID → invokedynamic supplier → DeferredRegister.register(String,Supplier) → putstatic FIELD` pairs and exactly nine matching declared `DeferredHolder` fields.
3. Reject missing/extra/duplicate or field-remapped actions and invalid/altered JARs. The output report is limited to the SHA digests, counts, deviations, and non-gameplay disclaimer. Synthetic Java unit tests prove only the parser behavior; passing fixtures cannot substitute for JAR inspection.

**Proof boundary:** successful static JAR registry inspection promotes compiled action-registration identity only, not action visibility, survival-tree unlock implementation, Vampirism granted skills/cooldowns, Werewolf form/bite lifecycle, full-moon enforcement, sickness/effects, faction state or actual client/server rendering. The eight source-counted actions **include Leap and exclude the UI-only Hide Name action**. The nine compiled registrations are not nine new spells.

## Open release gates

⚠️ Actual Werewolves/Vampirism 1.10.13/Vampiric Ageing 1.4.21/Epic Fight 21.17.3.1 co-loaded QA has not been observed. Howling AABB, Sense radius/cooldown, Leap reachability, bite cooldown, day/full-moon transitions, form render, authority on PvP/claims and save/restart remain live physical checks. `Stage 06.05` remains 🟡; no existing `RPG Skill Tree` adapter/Mastery/perks authorization. Black Arcana does not duplicate Vampirism's faction state or action engine.

**Observed publisher-JAR evidence:** [run #38600511526](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38600511526) confirms **9/9** unique compiled action registrations, no differences, official Modrinth version zkd687ts JAR **2,297,879 bytes**, SHA-1 `12a400d50c6e2afdcd96caf73cb80d37877147c8`, SHA-256 `ecbca2cd344e24ad48157834a8f321d1a7d2221c727fe8e61e4436d1219c6cfb`. The separate publisher CurseForge download attempt failed HTTP 403, not a hash mismatch. Independent source catalog keeps **8** strict semantic actions including Leap, excluding Hide Name. No new roots. This constitutes candidate registry evidence for the **28th/39** provider, but record formal promotion only with final-HEAD audit and both canonical CI jobs SUCCESS. No physical gameplay proof or Stage promotion.
