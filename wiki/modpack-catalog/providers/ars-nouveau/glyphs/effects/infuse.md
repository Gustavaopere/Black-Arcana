# Ars Nouveau — Infuse

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_infuse`
- Display name: Infuse
- Default tier: 2
- Default mana cost: 30
- Compatible augments: AOE, Extend Time
- Default AOE limit: 1
- Default Extend Time limit: 1
- School: no explicit school override in the inspected class; do not infer one

## Provider-native behavior

Infuse obtains potion contents from Ars' potion-provider/inventory surfaces. Priority is: an `IPotionProvider` item or flask (one use consumed), then a normal PotionItem (one item consumed and bottle returned), then a nearby Potion Jar with more than 100 units (100 removed). Direct entity resolution applies the potion contents; AOE spawns a splash potion and Extend Time spawns a lingering potion.

## Authority / deduplication

Ars Nouveau owns potion/flask/jar consumption and application for this spell. Black Arcana must not consume a second potion resource, duplicate the thrown potion, or infer an Ars spell school not declared by the exact source class.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectInfuse`).
