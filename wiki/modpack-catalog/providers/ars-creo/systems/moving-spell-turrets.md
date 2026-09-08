# Moving Spell Turrets

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Ars Creo registers Create behavior on existing Ars Nouveau Basic, Timer and Enchanted Spell Turrets.

- Basic: server-side interaction with the moving actor invokes the shared cast path.
- Timer: positive stored `time` triggers when server game time is divisible by that interval.
- Enchanted: invokes the shared cast path when the moving actor visits a new block position.

The shared cast path decodes Ars spell data, uses Ars resolver/context, charges Source on the contraption first and falls back to nearby Ars Source. Projectile velocity incorporates contraption rotation/motion; Touch uses the provider's moving position/facing logic.

The wrapped caster reports Ars `CasterType.OTHER`; there is no source-supported player Mastery attribution contract here.

Rotating Turret appears in Display Source registration but not in the exact movement-behavior registration list, so moving-cast support for it is not claimed.

Black Arcana must observe this as one provider causal action and never double-settle it.