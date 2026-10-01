# Cataclysm: Ignis Soulfires 1.8.0 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / CLEAN-ROOM STRUCTURAL AUDIT / 8 ACTION ROOTS`

## Evidence packet

- temporary NON-MERGE PR: **#491**;
- audit HEAD: `24e0b5b63e816d96314acc610b7abdb39dec0792`;
- run: `36832733575` — SUCCESS;
- artifact: `11148470931`;
- artifact digest: `sha256:c7c8f7116590df736eaecb02521658b47d8f27ada402facdfde2215a4401f60a`.

| Field | Value |
|---|---|
| physical SHA-1 | `a6f1c8cfe673aaff17f081ee9546e3600b4c72f1` |
| audited publisher SHA-1 | `a6f1c8cfe673aaff17f081ee9546e3600b4c72f1` |
| audited publisher SHA-256 | `a2368227b6cab37988334b4b6b8b6936fdf939aaa3518494a3921b45a426989d` |
| audited bytes | `489267` |
| equality | **EXACT** |

Archive counts: **454 entries / 181 classes / 273 resources / 378 provider-associated paths**.

The temporary audit emitted path/resource/localization inventories and bounded `javap -p -c -constants` evidence for relevant item/config/registry classes. The durable catalog does not store the upstream JAR or implementation bodies.

## Action-root proof

### Bulwark of the Soul Flame

Exact class: `com.ziver.ignissoulfires.content.item.weapons.BulwarkOfTheSoulFlame`.

**Bulwark Deployment:** `use(...)` reaches `deployBulwark(...)` only on the server-side Bulwark control path. The method raycasts with the player's real block interaction range, constructs `BulwarkOfTheSoulFlameWall`, collision-checks it and spawns the wall server-side. This is a discrete player action.

**Bulwark Charge:** shift-use enters the use lifecycle; `releaseUsing(...)` creates Cataclysm `ChargeAttachment` state and settles the provider `chargeCooldown`. This is a second action branch, not the barrier deployment.

Attack ignition and block-knockback traits are passive/downstream and add zero identities.

### Souled Gauntlet of Bulwark

Exact class: `com.ziver.ignissoulfires.content.item.weapons.SouledGauntletOfBulwark`.

**Soul-Fire Chain:** shift-held execution scans forward along the look vector and uses distinct `chainCooldown`, `chainRange`, `chainPullSpeed`, `chainHitDamage` and `chainHitKnockback` seams. The target is pulled and the terminal hit/effects are resolved as one causal action.

**Gauntlet Charge:** the non-shift charged release uses Cataclysm `ChargeAttachment` and the distinct provider `chargeCooldown`. This is separate from the chain branch.

### The Immolator of Souls

Exact class: `com.ziver.ignissoulfires.content.item.weapons.TheSouledImmolator`.

**Soul-Fire Stun Area:** shift release after the charge threshold resolves the area branch using provider area cooldown/radius/stun-damage seams.

**Flame Strike:** non-shift release invokes `spawnFlameStrike(...)` and settles the distinct `strikeCooldown` path.

Particles, screen shake, sound, Stun and Blazing Brand are consequences/presentation and add zero identities.

### The Incinerator of Souls

Exact class: `com.ziver.ignissoulfires.content.item.weapons.TheSouledIncinerator`.

**Incinerator Dash:** shift release after the exact 60-tick threshold uses `dashCooldown`, `dashDamage`, `dashKnockback` and Cataclysm `ChargeAttachment`.

**Incinerator Slam:** non-shift release after the same threshold invokes `useIncineratorSlam(...)`, which resolves a forward `spawnStrike(...)` sequence and uses the distinct `slamCooldown`.

The individual strike spawns are substeps of one slam action.

## Acquisition proof

The exact artifact contains:

- `data/ignissoulfires/recipe/shape/bulwark_of_the_soul_flame.json` → `ignissoulfires:bulwark_of_the_soul_flame`;
- `data/ignissoulfires/recipe/smithing/bulwark_of_the_soul_flame.json` → the same owner;
- `data/ignissoulfires/recipe/weapon_infusion/souled_gauntlet_of_bulwark.json` → `ignissoulfires:souled_gauntlet_of_bulwark`;
- `data/ignissoulfires/recipe/weapon_infusion/the_souled_immolator.json` → `ignissoulfires:the_souled_immolator`;
- `data/ignissoulfires/recipe/smithing/the_souled_incinerator.json` → `ignissoulfires:the_souled_incinerator`.

Bounded recipe extraction verifies the actual result IDs and Cataclysm/provider ingredient references; the routes are not inferred from filenames alone.

## Exclusion audit

Metric-excluded but catalog-relevant surfaces include thrown Ignitium/Souled tools, tool return, distance breaking/actions, 3×3 Souled tool behavior, prospecting, Tree Cap, mode cycling, Souled Blazing Grips procs, armor/horse-armor passive effects, materials/attributes/recipes themselves and client presentation.

These are not additional standalone spell/ritual/equivalent action roots under the canonical ledger.

## Semantic result

- exact discrete supernatural player action roots: **8**;
- strict state: **8 × `COUNTED_EXACT`**;
- conditional roots among these eight: **0 identified**;
- excluded supporting/passive/tool surfaces: **+0**.

Strict semantic delta: **+8**.

## Clean-room boundary

The durable catalog records factual observations: identifiers, control branches, class/method/config names, resource presence, recipe outputs/provenance and action relationships. It does not copy upstream bytecode/source bodies, creative assets or localization prose.