# Ars Nouveau 5.13.1 — Effects

Status: `67/67 SOURCE-PINNED / INDIVIDUAL PAGES COMPLETE`

Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

The production 5.13.1 `APIRegistry` registers **67 core Effects**. Every Effect has an individual page in this directory.

## Inventory

1. Break
2. Harm
3. Ignite
4. Conjure Mageblock / Phantom Block
5. Heal
6. Grow
7. Knockback (`glyph_gust`)
8. Conjure Magelight
9. Dispel
10. Launch
11. Pull
12. Blink
13. Explosion
14. Lightning
15. Slowfall
16. Fangs
17. Summon Vex
18. Access Ender Inventory
19. Harvest
20. Fell
21. Item Pickup
22. Interact
23. Place Block
24. Snare
25. Smelt
26. Leap
27. Delay
28. Redstone Signal
29. Intangible
30. Invisibility
31. Wither
32. Exchange
33. Craft
34. Flare
35. Cold Snap
36. Conjure Water
37. Gravity
38. Cut
39. Crush
40. Summon Wolves
41. Summon Steed
42. Summon Decoy
43. Hex
44. Glide
45. Rune
46. Freeze
47. Name
48. Summon Undead
49. Firework
50. Toss
51. Bounce
52. Wind Shear
53. Evaporate
54. Linger
55. Sense Magic
56. Infuse
57. Rotate
58. Wall
59. Animate Block
60. Burst
61. Orbit
62. Reset
63. Wololo
64. Rewind
65. Bubble
66. Wind Burst
67. Prestidigitation

## Catalog rules

- Source-pinned defaults are not claimed as final effective modpack config until runtime/config QA.
- Provider-owned costs, spell contexts, child resolvers, summons, delayed events, world effects, inventory extraction and settlement remain Ars Nouveau authority.
- Black Arcana does not create a second mana charge, cooldown, damage settlement, summon ledger or child-cast pipeline for Ars spells.
- Independent Black Arcana destructive effects still route through `WorldEffectPolicy`; provider-owned world mutation is observed, not replayed.
- Visual effects never become gameplay authority.

## Remaining Ars Nouveau provider work

Closing 67/67 Effects does not close the provider. Phase 2M still needs granular coverage for 24 rituals, 6 familiars, 20 perks and provider-wide systems/infrastructure/acquisition/runtime boundaries before Ars Nouveau can be considered source-catalog complete.