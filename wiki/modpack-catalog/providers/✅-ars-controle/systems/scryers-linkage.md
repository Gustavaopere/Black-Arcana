# Scryer's Linkage

State: `SOURCE-PINNED 1.6.15 / REMOTE CAPABILITY BRIDGE / LOAD-TIME EFFECT UNVERIFIED / RUNTIME QA PENDING`

Registry id: `ars_controle:scryers_linkage`
Block entity: `ars_controle:scryers_linkage` -> `ScryersLinkageTile`
Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

## Acquisition

Enchanting Apparatus:

- reagent: `ars_nouveau:scryers_crystal`;
- 4 × tag `c:ender_pearls`;
- 4 × `minecraft:popped_chorus_fruit`;
- recipe `sourceCost`: `0`.

## Remote target identity

The target is attachment `ars_controle:block_target` encoded as `GlobalPos`.

When a new target is set, provider capability caches are invalidated. A block in the provider tag `ars_controle:scryers_linkage_blacklist` is rejected. Invalid/missing dimensions resolve to no target information.

The link stores a reference, not a copy of the target inventory/state.

## Capability delegation

At capability-registration time Ars Controle iterates NeoForge `BlockCapability.getAll()` and registers matching capability providers on the Linkage block entity, except blacklisted classes.

A requested capability is delegated through `BlockCapabilityCache` to the remote target's actual block capability. The provider rejects a delegated capability when either:

- the capability type class matches a startup-blacklisted class; or
- the returned capability implementation class matches a startup-blacklisted class.

Default class blacklist:

- Ars Nouveau `LecternInvWrapper`;
- `appeng.api.networking.IInWorldGridNodeHost` when that class is available.

A detected `StackOverflowError` while querying a capability is treated as a probable recursive link; Ars Controle logs the condition, removes the Linkage target and returns no capability.

This is broader than a fixed item/fluid/energy list: it is generic block-capability delegation subject to provider blacklists.

## Redstone and comparator behavior

The block delegates ordinary redstone signal, direct signal, analog output and redstone-connectability to the target block state. Ars Controle also injects contextual comparator handling so the Linkage can expose target analog behavior with the relevant side/context.

Its ticker tracks the identity hash of the target block entity. When the remote block entity identity changes, local capabilities are invalidated. While linked, the ticker also updates neighboring redstone/comparator outputs.

## `load_time` config caution

The server config declares `scryers_linkage.load_time = 600` with text saying how long the target will be loaded after request.

The exact 1.6.15 `ScryersLinkageBlock`, `ScryersLinkageTile` and capability-registration paths audited here do not contain the Warping Prism-style region-ticket operation or a direct reference to that config field. The catalog therefore does **not** claim that Linkage actually force-loads its target for 600 ticks.

Effective chunk-load behavior remains `RUNTIME QA REQUIRED`.

## Protection/authority caution

Interaction with the Linkage itself posts an Ars/NeoForge `BlockEvent.BreakEvent` at the Linkage position. This does not establish that a remote target is authorized for arbitrary Black Arcana mutation.

A capability obtained through the Linkage remains owned by the underlying remote provider. Item/fluid/energy/etc. settlement must happen once through that capability; Black Arcana must not mirror transfers or infer ownership from the Linkage reference.

## Boundary

- Ars Controle owns link state, delegation and local redstone projection.
- The remote provider owns the underlying capability/resource state.
- Black Arcana must not treat `GlobalPos` persistence as target authorization.
- No force-load permission is inherited.
- Remote transfers/queries must never become duplicate Black Arcana resource or Mastery events.

## QA pending

1. Establish actual chunk-load behavior and whether `scryers_linkage.load_time` is operative in the installed JAR.
2. Validate item/fluid/energy and modded capabilities against unloaded/reloaded targets.
3. Validate recursion handling with Linkage-to-Linkage chains.
4. Measure per-tick neighbor-update cost under many active links.
5. Validate AE2/Ars blacklist behavior against the installed provider versions.
