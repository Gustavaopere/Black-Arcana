# Otherside Portal Activation

Status: `✅ PHYSICAL ACTION ROOT CATALOGED / COUNTED_EXACT / +1 STRICT / ⚠️ RUNTIME QA OPEN`

- Provider: **Deeper and Darker** (`deeperdarker`)
- Version line: `1.4.1`
- Semantic owner: `deeperdarker:heart_of_the_deep`
- Public/source seam: `WardenHeartItem.useOn(...)` -> `OthersidePortalBlock.spawnPortal(...)`
- Exact source pin: `KyaniteMods/DeeperAndDarker@f7ba235d078411a1165a8cac184adfe0ccc8cebe`
- Public publisher SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`
- Current physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`
- Semantic type: supernatural portal creation / traversal setup
- Current strict state: `COUNTED_EXACT / CURRENT PHYSICAL ROOT + ACQUISITION VERIFIED / +1`

**Current physical-JAR reconciliation (2026-10-08):** the matching `83f7edd0...` JAR directly confirms this action root and its packaged acquisition path, independently of the public-source baseline. Quantitative source-only claims below are **not** automatically projected to the physical JAR. See `../PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`.

## Trigger and admission

The player uses `deeperdarker:heart_of_the_deep` on a block.

Exact source admits the action only when:

- a player exists in the interaction context;
- the player is in either the vanilla **Overworld** or Deeper and Darker's **Otherside** dimension;
- a valid Otherside portal shape can be found at the block adjacent to the clicked face;
- the provider `PortalSpawnEvent` is not cancelled.

Heart of the Deep is registered with:

- stack size: **1**;
- rarity: **RARE**;
- fire resistance: enabled.

## Portal-frame contract

`OthersidePortalShape` validates a reinforced-deepslate frame with:

- interior width: **2–21 blocks**;
- interior height: **2–21 blocks**;
- reinforced deepslate on the frame boundary;
- the broader shape/lifecycle validator treats interior cells as structurally empty when they are air or existing Otherside portal blocks.

For **new player activation**, `OthersidePortalBlock.isPortal(...)` adds a stricter condition: the selected valid X/Z shape must have `numPortalBlocks == 0`. A frame whose interior already contains any Otherside portal block is therefore **not eligible for a new Heart activation**, even though those blocks are accepted by the broader shape-validity/lifecycle checks.

The player activation path does **not** read `othersidePortalWidth` or `othersidePortalHeight`. Those COMMON config keys therefore are not used here as activation dimensions.

## Settlement

If portal creation succeeds:

- the provider fills the validated interior with Otherside portal blocks;
- it plays `SCULK_CATALYST_BLOOM` at volume **6.0** and pitch **0.8**;
- a non-creative player loses the Heart of the Deep;
- a creative player retains it;
- the interaction returns success.

If the portal cannot be spawned, the interaction returns failure and this path does not consume the Heart.

## Public/source acquisition

Exact generated 1.4.1 loot data adds `deeperdarker:heart_of_the_deep` to the vanilla Warden loot-table context through provider loot modifier `deeperdarker:add` with:

- `min = 1`;
- `max = 1`.

This is baseline acquisition evidence only; exact physical reachability is not asserted while the installed JAR remains byte-different.

## Excluded adjacent behavior

`WardenHeartItem.inventoryTick(...)` may play Warden heartbeat sounds when `wardenHeartPulses` is enabled. That is presentation/state behavior, not another semantic action.

Portal collision, cross-dimensional transfer and exit-portal generation after activation are downstream lifecycle of this same root and are not separate spell identities.

## Evidence boundary

The public release and source support the baseline details above. The separately audited exact-current physical JAR confirms the action root and acquisition, but **does not yet establish exact numeric/mechanical parity** for every public-source value. The publisher/source hash mismatch is provenance-only for this catalog identity.

- catalog: **✅ exact-current action materialized**;
- exact-current root and acquisition: **verified by static physical-JAR audit**;
- strict semantic contribution: **+1 `COUNTED_EXACT`**;
- provider runtime QA: **⚠️ pending**.

Sources inside this provider folder: `../PUBLIC-1.4.1-BASELINE-AUDIT.md`, `PUBLIC-BASELINE-ACTIONS.md`.
