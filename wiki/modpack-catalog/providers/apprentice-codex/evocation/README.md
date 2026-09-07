# Apprentice's Codex — Evocation school

Exact source checkpoint: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

Installed provider: `apprentice_codex-0.9.7.1+mc1.21.1.jar` / `apprenticecodex` / `0.9.7.1`.

The exact 0.9.7.1 registry contains **17/17** Apprentice's Codex spells in Iron's canonical **Evocation** school:

1. [Archer Multiple](archer-multiple.md)
2. [Feather Rush](feather-rush.md)
3. [Slash Blade](slash-blade.md)
4. [Precision Jack](precision-jack.md)
5. [Auto Turret](auto-turret.md)
6. [Companion Trunk](companion-trunk.md)
7. [Search Beacon](search-beacon.md)
8. [Tamer's Pocket](tamers-pocket.md)
9. [Silent Assassin](silent-assassin.md)
10. [Tiro Volley](tiro-volley.md)
11. [Bound Sword](bound-sword.md)
12. [Bound Bow](bound-bow.md)
13. [Lethal Assault](lethal-assault.md)
14. [Edge Dancer](edge-dancer.md)
15. [Linear Build](linear-build.md)
16. [Fujin](fujin.md)
17. [Call Broom](call-broom.md)

## Semantic coverage

This school is unusually broad. It includes owner-bound autonomous weapons, firearm-style summons, persistent/temporary equipment, pet storage, personal storage, structure searching, building automation, loot-modifying attacks and mount deployment.

High-overlap Black Arcana families:

- **Familiars/Binding:** Archer Multiple, Auto Turret, Companion Trunk, Tamer's Pocket and Call Broom occupy owner-bound summon/storage/control niches.
- **Divination:** Search Beacon provides provider-native structure search.
- **Item-bound casting:** Bound Sword, Bound Bow, Edge Dancer and Call Broom deliberately disable ordinary crafting/loot where source says so.
- **World interaction:** Linear Build is a provider-native construction transaction with explicit inventory/resource sourcing and server validation.
- **Combat saturation:** Feather Rush, Slash Blade, Silent Assassin, Tiro Volley, Lethal Assault and Fujin occupy multiple projectile/blade/firearm patterns.

Iron's remains authority for mana/cast/cooldown lifecycle. Apprentice's Codex owns the concrete entities, recasts, custom equipment and state. Black Arcana/RPG must observe causally safe provider events rather than replaying any of these effects.