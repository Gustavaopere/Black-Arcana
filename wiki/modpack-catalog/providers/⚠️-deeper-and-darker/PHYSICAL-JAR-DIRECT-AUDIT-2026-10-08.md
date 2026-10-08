# Deeper and Darker 1.4.1 — direct current-physical JAR intake (2026-10-08)

Status: `EXACT PHYSICAL JAR INSPECTED / EXACT-CURRENT 3 SUPERNATURAL ROOTS / 2 COUNTED_EXACT + 1 CONFIG-CONDITIONAL / +2 STRICT / DEPLOYED COMMON TOML UNKNOWN`

## Exact uploaded physical authority

User-supplied modpack bytes were inspected read-only. The JAR was never executed.

- JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- bundled mod id/version: `deeperdarker` / `1.4.1`;
- current sibling physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` — exact match;
- SHA-256: `b05a882f49f8e65263a45fa1653c1b85491e90ee451c34b0dc8790f84e84ec7f`;
- byte length **3,906,044**; **2,900** archive entries; **207** classes.

The 3,906,044-byte size coincides with the historically recorded local NeoVitae `v2` compatibility JAR, but this is **not** a byte-identity/provenance claim.

The deployed `deeperdarker.mixins.json` lists six common mixins. The archive contains both `PlayerMixin.class` and `ServerPlayerMixin.class` yet neither appears in the active `mixins` array. This is an exact-current *configuration-list* fact, not proof that the original NeoVitae conflict is solved in the fully assembled runtime.

## Exact current semantic roots

Direct inspection of physical item activation methods, provider packet handling and packaged acquisition resources corroborates the baseline **3** distinct supernatural player-action roots:

1. **Otherside Portal Activation** — `WardenHeartItem.useOn` handles Heart of the Deep on the provider portal-frame surface. The physical `warden_heart_from_warden` modifier grants `deeperdarker:heart_of_the_deep` through the Warden loot table and is listed in the active global-modifier index. **`COUNTED_EXACT`**.
2. **Sonorous Staff Sonic Boom** — physical `SonorousStaffItem.releaseUsing` provides the deliberate charged sonic action and its cooldown; `data/deeperdarker/recipe/sonorous_staff.json` gives the provider item recipe. **`COUNTED_EXACT`**.
3. **Soul Elytra Boost** — exact physical `SoulElytraBoostPacket` checks flight, equipped `SOUL_ELYTRA`, current cooldown and the COMMON `soulElytraCooldown` value before spawning a provider-owned firework boost. The physical Soul Elytra recipe exists. **`CONDITIONAL`** because the deployed `config/deeperdarker-common.toml` value is unavailable.

All **9** top-level concrete classes in `content/items/` were reviewed for interaction/tick signatures. Their activation surface agrees with the earlier public-release 1.4.1 item index. Teleportation after opening a portal, equipment passives, Sculk Transmitter utility, enchantment modifiers and item visual ticks remain excluded.

## Accounting

- physical current semantic denominator: **3 roots**;
- **2** exact-current countable actions (portal and staff);
- **1** conditional root (Soul Elytra Boost);
- provider strict addition: **+2**;
- previous global strict minimum: **1849** -> **1851**.

The deployed `soulElytraCooldown` is not embedded in the JAR and was not uploaded. Source default `600` is **not** a deployed observation; `-1` remains a possible disablement. Therefore Soul Elytra contributes **+0** until its actual current-instance COMMON value is supplied. The directory remains **⚠️** pending this deployed activation gate and runtime acceptance; the semantic object inventory is no longer blocked by missing physical bytes.

## Method/clean-room

Read-only SHA-1/SHA-256, ZIP JSON/metadata inspection, Java 21 `javap -p -c` inspection of action/packet/config methods, exhaustive top-level item-method-signature audit and bounded recipe/loot index checks. Local structural assertions passed. No code, disassembly, model, texture or sound is transferred into Black Arcana. No actual NeoForge/modpack server launch was performed.
