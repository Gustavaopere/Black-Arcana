# Stage 05 Block J — provider-real execution profile

Status: **SUPPORTING QA PROFILE / PHYSICAL EXECUTION PENDING**

This document is a mandatory companion to Block J in `docs/qa/casting-ux-real-client-runbook.md`. It narrows the provider-real preparation path for the Iron's-hosted Black Arcana probe. It does not replace the manual matrix, does not create real-client evidence, and does not authorize changing any Block J row to `PASS` without direct physical observation.

## Scope and authority boundary

The test spell is `black_arcana:irons_integration_probe`. Iron's supplies the provider-native host surface and mana storage/synchronization. Black Arcana remains authoritative for cast admission, transactional cost, cooldown and authoritative cast result. Epic Fight / EFIS may affect combat or animation presentation but must not become Black Arcana cast-legality authority.

The Black Arcana probe cost is 20 Iron's mana and its Black Arcana cooldown is 40 ticks. Those values are expectations to be verified physically, not inferred as PASS from unit tests.

## Candidate prerequisite

Use the exact Black Arcana JAR from the candidate SHA under test. The candidate must include the synthetic presentation-overlay support that keeps provider-conditional spell metadata visible through declarative spell-data reloads while rejecting ID collisions fail-closed.

Before physical testing with Iron's present, open the normal Black Arcana loadout editor and confirm `black_arcana:irons_integration_probe` is available from the server-synchronized presentation catalog. The probe intentionally uses provider-conditional synthetic metadata rather than a static datapack entry, so it must not be exposed merely because Black Arcana is installed while Iron's is absent or incompatible.

The probe currently references an optional dedicated icon path. If that resource is unavailable, the Stage 05 client icon resolver is designed to use the Black Arcana placeholder. A placeholder icon is not by itself a reachability failure; the synchronized spell identity must still be present and selectable.

If Iron's is available but the probe is absent from the legitimate Black Arcana editor catalog, record the Block J attempt as `FAIL`; do not inject a client-only loadout entry or use a debug bypass.

## Physical snapshot gate

Before the run, record the exact physical Minecraft/NeoForge instance, Black Arcana candidate SHA/JAR, and installed JAR filenames and versions for the provider/coexistence set. The planning baseline is:

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Spell Actionbar `1.1.4`;
- Epic Fight `21.17.3.1`;
- EFIS Compat `3.1.0`;
- Controlling `19.0.5`.

These are baseline values only. Treat them as the tested versions only when the physical instance actually matches them. Record file digests when the campaign evidence process supports them.

## Iron's-hosted probe preparation

1. Use a player in **Survival**. The player may have operator permission for setup commands, but do not perform the debit observation in Creative. Black Arcana's current payment policy bypasses the probe payment for Creative context, which would make the mana-debit observation invalid.
2. Through the normal Black Arcana loadout editor, add `black_arcana:irons_integration_probe` to **slot 0**, apply the draft, and confirm the server-accepted loadout after reopening the editor. Reconnect once when practical and confirm slot 0 remains server-owned and synchronized before the provider invocation.
3. With command permission level 2 available for setup, create a legitimate Iron's sword host using the provider command, for example:

   `/createImbuedSword minecraft:iron_sword black_arcana:irons_integration_probe 1`

   Iron's `1.21.1-3.16.3` registers `createImbuedSword`, requires permission level 2, accepts a `SwordItem`, resolves the supplied spell through its spell registry and installs the resulting spell container on the sword. This setup is provider-native; it is not a Black Arcana debug ingress.
4. Equip the created sword and select its hosted spell through the ordinary Iron's spell-selection path.
5. Invoke it using Iron's normal **Cast Selected Spell** input. Do **not** use a scroll for the cooldown-authority observation. The normal selected-spell path sends Iron's cast packet and initiates the selected spell using the host item's cast source; the sword profile exercises a non-scroll provider cast source.
6. Perform one clean invocation first. Repeat only when needed to distinguish settlement behavior or to verify cooldown expiry. Do not infer authority from animation count alone.

## Required provider-real observations

Capture enough client/server evidence to support every applicable statement below on the same physical candidate:

- one provider host action produces at most one Black Arcana root cast/result;
- the synchronized Iron's mana value decreases by exactly the one Black Arcana probe cost, **20 mana**, and no second provider-native debit is applied;
- the client-visible Iron's mana state converges to the server-authoritative post-debit value;
- Black Arcana applies the probe cooldown once, with the expected **40-tick** duration, and no second provider-native cooldown is stacked on the hosted transaction;
- no duplicate Black Arcana effect/result/settlement appears from the one host action;
- loadout slot 0 remains the server-owned identity admitted by the Black Arcana ingress rather than a forged client selection.

Record mana before and after, the relevant cast/result observation, and the cooldown observation in one continuous capture when practical. If the available production observation surface cannot positively distinguish one-root/one-result behavior, mark that subcase `BLOCKED`; do not substitute animation count for authoritative evidence.

## Epic Fight / EFIS coexistence

With Epic Fight / EFIS present, establish a Black Arcana cast whose ordinary server-owned gates are satisfied. Repeat the same operation while changing only the relevant combat/animation mode where the installed version permits it. Cosmetic or animation differences are allowed; the provider/combat client state must not independently allow or deny a Black Arcana cast whose server-owned inputs are otherwise equivalent.

## Optional-provider failure profile

Where a safe reproducible profile exists, run Black Arcana with Iron's absent or demonstrably incompatible and verify fail-closed behavior for the dependent integration: no crash, no free/duplicate fallback and no unrelated Black Arcana casting failure. Exercise the core Black Arcana keyboard/mouse paths required by the runbook in that profile.

Do not require the Iron's-only probe to remain available when Iron's is absent. Provider-conditional presentation must disappear with the provider/runtime integration rather than becoming static gameplay content.

If provider absence/incompatibility cannot be exercised safely on the physical campaign without changing production semantics, record the corresponding row `BLOCKED` with the concrete reason.

## Automated evidence boundary

The following are supporting evidence only:

- `SpellDataCatalogTest` verifies synthetic metadata survives declarative replacement and that declarative data cannot shadow an installed synthetic ID;
- `IronsSyntheticContentTest` verifies the hosted probe remains presentable across metadata replacement, consumes the Black Arcana cost once, uses the Black Arcana cooldown, and fails before partial hosted runtime installation when presentation metadata collides;
- NeoForge build, Foundation GameTest, dedicated-server smoke and Stage 05 companion smoke validate automated integration/build boundaries.

A fully green CI run still leaves Block J provider-real execution **PENDING** until the observations above are performed in the actual physical modpack instance and recorded in `docs/qa/casting-ux-real-client-evidence.md` under the manual matrix vocabulary.
