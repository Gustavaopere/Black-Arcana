# Create Display Sources for Ars infrastructure

State: `SOURCE-PINNED 5.4.0 / PRESENTATION-ONLY`

Ars Creo registers two Create Display Sources:

- `ars_creo:turret`: reads an Ars BasicSpellTurretTile and exposes stored spell name/display string; registered for Basic, Timer, Rotating and Enchanted turret blocks/BEs.
- `ars_creo:source_jar`: reads an Ars SourceJarTile and exposes current Source count.

These values feed Create Display Link/targets. They are observational UI/presentation data and are not a security, cast, resource or Arcane Danger authority surface.

Black Arcana must never use a display value as proof that a spell fired, Source was settled or a player owns the underlying system.