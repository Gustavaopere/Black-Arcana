# Not Enough Glyphs 4.6.2 — Deployed SERVER Config Checklist

Status: `39 SOURCE-ENABLED REGISTRATIONS / DEPLOYED ENABLED STATE UNVERIFIED`

## Purpose

This checklist turns the remaining Not Enough Glyphs catalog blocker into a finite evidence request.

Exact current 4.6.2 source-semver pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77` preserves the same `ArsNouveauRegistry.java` Git blob as 4.6.1, so the current-pack matrix remains 40 NEG registration primitives. `not_enough_glyphs:momentum` also retains the same source blob and explicit disabled override, leaving **39 source-enabled candidates** before Ars/NeoForge SERVER config.

Exact Ars Nouveau 5.13.1 config construction, already audited in this provider dossier, maps a registered spell-part identity `<namespace>:<path>` to SERVER config file `<namespace>/<path>.toml`, where `[general].enabled` controls the base spell-part enabled state. Source default `true` is **not** accepted as deployed pack state because SERVER config may be world-overridden.

Therefore every row below remains `NÃO VERIFICADO` until the effective deployed config is captured from an authoritative server/world configuration set.

## NEG-native — 14 source-enabled

| Registry identity | Expected SERVER config path | Effective `[general].enabled` |
|---|---|---|
| `not_enough_glyphs:plow` | `not_enough_glyphs/plow.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:trail` | `not_enough_glyphs/trail.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:ride` | `not_enough_glyphs/ride.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:feed` | `not_enough_glyphs/feed.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:filter_light` | `not_enough_glyphs/filter_light.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:filter_dark` | `not_enough_glyphs/filter_dark.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:contingency_fall` | `not_enough_glyphs/contingency_fall.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:contingency_heal` | `not_enough_glyphs/contingency_heal.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:contingency_health` | `not_enough_glyphs/contingency_health.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:contingency_death` | `not_enough_glyphs/contingency_death.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:contingency_fire` | `not_enough_glyphs/contingency_fire.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:contingency_blink` | `not_enough_glyphs/contingency_blink.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:contingency_time` | `not_enough_glyphs/contingency_time.toml` | `NÃO VERIFICADO` |
| `not_enough_glyphs:propagate_plane` | `not_enough_glyphs/propagate_plane.toml` | `NÃO VERIFICADO` |

## Too Many Glyphs fallback namespace — 14 source-enabled

These registrations are implemented by NEG in the current pack because `toomanyglyphs` is absent, while preserving the historical `toomanyglyphs` namespace.

| Registry identity | Expected SERVER config path | Effective `[general].enabled` |
|---|---|---|
| `toomanyglyphs:ray` | `toomanyglyphs/ray.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:reverse_direction` | `toomanyglyphs/reverse_direction.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:chaining` | `toomanyglyphs/chaining.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_block` | `toomanyglyphs/filter_block.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_entity` | `toomanyglyphs/filter_entity.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_living` | `toomanyglyphs/filter_living.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_living_not_monster` | `toomanyglyphs/filter_living_not_monster.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_living_not_player` | `toomanyglyphs/filter_living_not_player.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_monster` | `toomanyglyphs/filter_monster.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_player` | `toomanyglyphs/filter_player.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_item` | `toomanyglyphs/filter_item.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_animal` | `toomanyglyphs/filter_animal.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_is_baby` | `toomanyglyphs/filter_is_baby.toml` | `NÃO VERIFICADO` |
| `toomanyglyphs:filter_is_mature` | `toomanyglyphs/filter_is_mature.toml` | `NÃO VERIFICADO` |

## Ars Trinkets fallback namespace — 2 source-enabled

`ars_trinkets` is absent in the current physical pack, so NEG provides these fallbacks under the historical namespace.

| Registry identity | Expected SERVER config path | Effective `[general].enabled` |
|---|---|---|
| `ars_trinkets:filter_self` | `ars_trinkets/filter_self.toml` | `NÃO VERIFICADO` |
| `ars_trinkets:filter_not_self` | `ars_trinkets/filter_not_self.toml` | `NÃO VERIFICADO` |

## Ars Omega fallback namespace — 8 source-enabled

`arsomega` is absent in the current physical pack, so NEG provides these fallbacks under the historical namespace.

| Registry identity | Expected SERVER config path | Effective `[general].enabled` |
|---|---|---|
| `arsomega:flatten` | `arsomega/flatten.toml` | `NÃO VERIFICADO` |
| `arsomega:propagate_underfoot` | `arsomega/propagate_underfoot.toml` | `NÃO VERIFICADO` |
| `arsomega:propagate_projectile` | `arsomega/propagate_projectile.toml` | `NÃO VERIFICADO` |
| `arsomega:propagate_self` | `arsomega/propagate_self.toml` | `NÃO VERIFICADO` |
| `arsomega:missile` | `arsomega/missile.toml` | `NÃO VERIFICADO` |
| `arsomega:overhead` | `arsomega/overhead.toml` | `NÃO VERIFICADO` |
| `arsomega:propagate_missile` | `arsomega/propagate_missile.toml` | `NÃO VERIFICADO` |
| `arsomega:propagate_overhead` | `arsomega/propagate_overhead.toml` | `NÃO VERIFICADO` |

## Ars Scalaes fallback namespace — 1 source-enabled

NEG registers Resize unconditionally under the historical `ars_scalaes` namespace in the audited 4.6.2 source.

| Registry identity | Expected SERVER config path | Effective `[general].enabled` |
|---|---|---|
| `ars_scalaes:resize` | `ars_scalaes/resize.toml` | `NÃO VERIFICADO` |

## Source-disabled registration

`not_enough_glyphs:momentum` is registered but its provider implementation explicitly reports disabled in the audited source. It is therefore **not** one of the 39 candidates awaiting deployed config proof.

Expected base config path, if emitted by the Ars spell-part config construction, is `not_enough_glyphs/momentum.toml`; observing an enabled config value would not override the provider's explicit source-level disable for catalog classification.

## Acceptance rule

A candidate may move from `CONFIG_CONDITIONAL` only when authoritative deployed evidence establishes its effective SERVER config state. Acceptable evidence must be tied to the actual pack/world/server configuration, not copied from source defaults or a fresh generated config.

For each observed file, record at minimum:

- exact relative path;
- effective `[general].enabled` value;
- source of the deployed configuration (server/world instance or authoritative exported config set);
- pack/world checkpoint or fingerprint sufficient to distinguish it from defaults;
- any absent file whose effective value is resolved by authoritative runtime/config behavior rather than assumption.

Until then:

- 39 candidates remain `CONFIG_CONDITIONAL`;
- Momentum remains `SOURCE_DISABLED`;
- Not Enough Glyphs remains `⚠️ Parcial / condicionado`;
- no semantic-count increase is claimed from this checklist alone.
