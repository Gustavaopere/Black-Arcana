# Ars Controle 1.6.15 — config, dependencies and compatibility

Status: `SOURCE-PINNED DEFAULTS / EFFECTIVE PACK CONFIG+RUNTIME QA PENDING`

Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`.

## Declared dependency baseline

Exact source metadata/build properties declare:

- Minecraft `1.21.1`;
- NeoForge source build `21.1.217`, metadata range `[21,)`;
- Ars Nouveau build baseline `5.10.6.1245`, metadata requirement `>=5.10.6`;
- Curios build baseline `9.0.12`, metadata requirement `>=1.21-9.0.0`;
- CC:Tweaked build baseline `1.112.0` for optional peripheral code.

Current physical pack:

- NeoForge `21.1.248`;
- Ars Nouveau `5.13.1`;
- Curios `9.5.1+1.21.1`;
- no top-level ComputerCraft/CC:Tweaked JAR found.

The installed versions satisfy the broad metadata ranges visible in source, but range eligibility is not proof of ABI/event/mixin compatibility. Runtime QA remains required.

## Server config defaults

### Warping Spell Prism

| Key | Default | Meaning in source |
|---|---:|---|
| `warping_spell_prism.max_cost` | `-1` | negative means no configured Source cap in helper calculation |
| `warping_spell_prism.cost_min_distance` | `1024` | distance threshold used by Source helper |
| `warping_spell_prism.cost_per_block` | `0.03125` | Source multiplier after threshold formula |
| `warping_spell_prism.dimension_cost` | `2000` | additional/base cross-dimension Source helper cost |
| `warping_spell_prism.load_time` | `600` | destination region-ticket lifetime parameter in ticks when >0 |
| `warping_spell_prism.allow_linking_other_players` | `false` | non-creative linking to other players denied by default |

### Warp Scroll Holder

| Key | Default |
|---|---:|
| `scroll_holder.cost` | `1000` Source |

The source comment defines 1 Source Jar as 10000 Source.

### Scryer's Linkage

| Key | Default | Audit state |
|---|---:|---|
| `scryers_linkage.load_time` | `600` | declared, but audited 1.6.15 linkage block/tile/capability paths do not demonstrate the corresponding chunk-ticket behavior; `RUNTIME QA REQUIRED` |

## Startup config

`Scryer's Linkage` has `blacklisted_capabilities`, represented as class paths loaded at startup.

Defaults:

- Ars Nouveau `LecternInvWrapper` canonical class;
- `appeng.api.networking.IInWorldGridNodeHost`.

Missing default classes are tolerated. User-added missing classes produce a warning. The resolved class list is used both to skip capability types and to reject returned capability implementation classes.

## Client config

`ACClientConfig` exists in source but declares no values. The exact mod constructor registers startup and server configs; it does not register this empty client config surface. No client gameplay authority is inferred from it.

## ComputerCraft / CC:Tweaked

`ArsControle.onRegisterCapabilities` checks `ModList.get().isLoaded("computercraft")` before registering CC peripherals.

When active:

- Warping Spell Prism peripheral can configure block targets, inspect current target and query calculated Source requirement;
- Scroll Holder peripheral can inspect valid Warp Scroll target data.

The current pack has no top-level ComputerCraft/CC:Tweaked JAR, so this compatibility is `OPTIONAL / ABSENT` at the physical-modlist checkpoint.

## Curios

Curios is declared mandatory by the exact mod metadata, not an optional integration gate. Its presence/version is therefore part of provider boot compatibility. Phase 2R does not infer any Black Arcana Curios contract from that dependency alone.

## Notion compatibility correction

The older Notion dossier listed optional Ars Additions, Alex's Caves and StarbuncleMania extensions and a broader 31-component logic surface. The exact 1.6.15 registry/build/runtime paths audited for Phase 2R do not promote those as registered glyph/system surfaces. They remain historical/editorial claims unless separately proven against this exact artifact/source.

## Fail-closed policy

Any future Black Arcana adapter must verify its exact seam against the installed Ars Nouveau 5.13.1 / Ars Controle 1.6.15 combination. Metadata compatibility ranges, class names, persisted NBT/components or source visibility are not sufficient by themselves.
