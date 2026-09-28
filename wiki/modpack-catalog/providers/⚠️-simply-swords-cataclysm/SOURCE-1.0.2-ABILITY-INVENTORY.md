# Simply Swords: Cataclysm 1.0.2 — exact-version source inventory

Checkpoint: 2026-09-27

## Evidence class

`SOURCE_PINNED_INVENTORY / ACTIVE_CONFIG_OPEN`

## Physical line

- JAR: `simplycataclysm-1.0.2+1.21.1+neoforge.jar`;
- runtime: `1.0.2+1.21.1+neoforge`;
- mod id: `simplycataclysm`;
- SHA-1: `a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469`;
- sibling row: #501 at `neoforge-rpg-skilltree@107ce395d9b37f908ad0ba39ef6ea6a01e5f27b2`.

## Publisher release correlation

Official CurseForge project `1382969` publishes File `7391959`:

- filename `simplycataclysm-1.0.2+1.21.1+neoforge.jar`;
- NeoForge / Minecraft 1.21.1;
- release date 2025-12-29;
- release changelog: NeoForge fix making Ignitium, Cursium and Witherite properly unbreakable.

Official source branch `1.21.1-neo` points to commit
`a81158e53b2d215ff534fa59732edd08cfd1d4f4`, also dated 2025-12-29.

That commit:

- changes `mod_version` from 1.0.1 to exactly `1.0.2+1.21.1+neoforge`;
- changes only `gradle.properties` and the three Ignitium/Cursium/Witherite item classes;
- adds the Unbreakable component to those three item classes;
- leaves the four ability implementations intact.

This is release-correlated exact-version source evidence, not a physical byte-equality claim.

## Source-tree completeness

The source tree at `a81158e...` is complete and contains 13 Java files:

- config/main registration;
- effects;
- melee callback/event handler;
- five material item classes;
- item registry;
- sounds.

No separate spell/ability package or additional behavior class exists in that exact tree.

The localized trait roots are:

- `accursed_rage`;
- `blazing_brand`;
- `mecha_pulse`;
- `mecha_smite`;
- `fireproof_unbreakable`.

The final entry is a material/item property label and is excluded from semantic-action counting.

## Four semantic roots

1. **Blazing Brand** — implemented by Ignitium weapon behavior.
2. **Accursed Rage** — implemented by Cursium weapon behavior.
3. **Mecha Pulse** — implemented by Witherite weapon behavior.
4. **Mecha Smite** — implemented by Witherite weapon behavior.

Ancient Metal and Black Steel item classes have no comparable special-trait path.

MobEffect registrations are supporting state:

- `accursed_rage`;
- `blazing_brand`;
- `pulse_charge`;
- `pulse_cooldown`.

They do not increase the semantic count.

## Config-gate audit

`SimplyCataclysm` registers `SCConfig.SPEC` as `ModConfig.Type.STARTUP`.

Exact source exposes ranges including zero for the proc gates. In particular, source comments explicitly identify zero as disable-state for Accursed Rage and Blazing Brand.

Therefore exact inventory cardinality is closed at four, but the active current-pack subset cannot be strict-counted from source defaults.

## Clean-room boundary

Upstream license: All Rights Reserved.

Only factual source structure, identifiers, release/version correlation, config schema and causal ownership are recorded. No implementation body or asset is reused in Black Arcana.

## Result

- complete exact-version semantic inventory: **4**;
- evidence: **source-pinned / release-correlated**;
- deployed active subset: **open**;
- strict contribution: **+0**;
- provider remains: **⚠️**.
