# Not Enough Glyphs 4.6.1 — Delegation, Repacking and Disabled Content

## Why this file exists

NEG deliberately preserves historical addon namespaces while providing fallback implementations. Registry namespace, implementation owner and current active provider are therefore separate questions.

## Current pack

### Too Many Glyphs

`toomanyglyphs` is absent. NEG therefore implements/registers 14 fallback primitives under `toomanyglyphs:*`.

### Ars Omega

`arsomega` is absent. NEG implements/registers 8 fallbacks under `arsomega:*`.

### Ars Trinkets

`ars_trinkets` is absent. NEG implements/registers `ars_trinkets:filter_self` and `ars_trinkets:filter_not_self`.

### Ars Scalaes

NEG registers `ars_scalaes:resize` unconditionally in current source. Ars Scalaes itself is absent from the physical pack.

### Ars Elemental

`ars_elemental` is installed. NEG does **not** register its local Arc/Homing fallbacks. Instead it adds the real Ars Elemental Arc Projectile, Homing Projectile, Propagate Arc and Propagate Homing objects to its internal listing and registers four Binder Elemental Focus perks.

Those four glyphs remain Ars Elemental runtime authority.

### Ars Controle

`ars_controle` is installed. NEG does not register `FilterRandom`. Runtime authority is Ars Controle.

## Momentum

`not_enough_glyphs:momentum` is passed through NEG's spell registration helper but its class explicitly returns `isEnabled() = false`. No generated glyph recipe exists in the exact source tree. Treat it as **source-disabled current content**, not an active default capability.

## Migration/perk aliases

NEG's `registerPerk` registers each perk under its current registry name and adds an old Ars Nouveau namespace alias for world migration. These aliases are migration compatibility, not duplicate perk authorities.

## Black Arcana dedup rule

Do not count each historical namespace and NEG implementation as separate semantic gaps. The active provider/implementation must be resolved from the installed-mod condition first. If a previously absent original addon is installed later, this matrix must be re-audited before implementation decisions.
