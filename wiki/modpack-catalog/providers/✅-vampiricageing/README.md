# Vampiric Ageing 1.21-1.4.21

Canonical source-level provider audit for the installed Black Arcana build.

## Installed authority

- JAR: `vampiricageing-1.21-1.4.21.jar`
- mod id: `vampiricageing`
- installed optional provider: `Werewolves-1.21-2.0.3.3.jar`
- installed base provider: `Vampirism-1.21-1.10.13.jar`
- exact upstream source: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`
- upstream `gradle.properties` at that commit: `mod_version=1.21-1.4.21`

This audit is **source-pinned**, not runtime-confirmed. Static source contracts are authoritative for this catalog; addon interoperability with the exact Black Arcana Vampirism/Werewolves builds remains a runtime-QA item.

## Provider model

Vampiric Ageing does not implement a standalone spell engine. It extends the TeamLapen faction/action/skill systems and owns an ageing attachment layered over those providers.

Installed-build surface:

- **3 Age Types**: `VAMPIRE`, `HUNTER`, `WEREWOLF` (`WEREWOLF` only when Werewolves is loaded; it is loaded in Black Arcana);
- **8 Age Methods** registered with the installed optional provider: `BITING`, `TIME`, `V_HUNTING`, `HUNTING`, `DRAINING`, `DEVOUR`, `W_HUNTING`, `W_MIXED`;
- **9 Actions** registered in `VampirismRegistries.Keys.ACTION` with Werewolves installed;
- **10 Skills** registered in `VampirismRegistries.Keys.SKILL` with Werewolves installed;
- persistent/synchronized `AgeingManager` state;
- Hunter Tainted Blood substate and cumulative-age mechanic;
- age-scaled attributes, damage hooks, food/trade/sun/blood interactions and Werewolves integration.

## Canonical documents

- [`MAGIAS.md`](MAGIAS.md) — canonical supernatural-power index; explicitly distinguishes Actions/Skills from spells.
- [`ACTION-CATALOG.md`](ACTION-CATALOG.md) — all 9 registered Actions, gates, defaults and settlement authority.
- [`SKILL-CATALOG.md`](SKILL-CATALOG.md) — all 10 Skills and provider unlock gates.
- [`PROGRESSION-AND-AGE-METHODS.md`](PROGRESSION-AND-AGE-METHODS.md) — age ranks, methods, thresholds and causal progression rules.
- [`STATE-AUTHORITY.md`](STATE-AUTHORITY.md) — `AgeingManager`, Hunter Tainted state, serialization and ownership rules.
- [`INTEGRATION-RULES.md`](INTEGRATION-RULES.md) — Black Arcana bridge/gate/dedup/fail-closed rules.
- [`TECHNICAL-AUDIT.md`](TECHNICAL-AUDIT.md) — source-level mismatches and mandatory runtime-QA targets.

## Authority boundary

Black Arcana must not recreate age rank, rank progress, ageing method, Tainted Age, permanent transformation, Action active state, provider Skill enablement or settlement outcomes in a parallel scoreboard/tag/custom-NBT model.

Use provider-native state as the source of truth. Any integration dependent on one of the static mismatches listed in `TECHNICAL-AUDIT.md` remains fail-closed until runtime QA proves the installed combination.
