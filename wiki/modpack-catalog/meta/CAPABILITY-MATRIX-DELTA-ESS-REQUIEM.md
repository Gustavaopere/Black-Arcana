# Capability Matrix Delta — Ender's Spells and Stuff: Requiem 0.1.7

Status: `✅ SOURCE-PINNED SPELL/ACTION PROVIDER / 53 STRICT SEMANTIC ACTIONS`

| Capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| Blood spells | player casts, summons, domain and weapon-exclusive/evolved actions | preserve Iron's host mana/cooldown and Requiem-owned effect/summon settlement |
| Strain | max-HP trade for Blood spell power | do not duplicate max-HP modifier lifecycle |
| Spellblade school | provider-owned school with provider focus/tag/gear | do not mint a second Spellblade authority |
| weapon-exclusive spells | source-held spells on provider weapons | preserve item ownership during cast and exactly-once resource/cooldown settlement |
| Ebony Cataphract actions | tackle/heal/slam direct player actions while effect is active | counted as discrete provider actions; do not collapse into the parent buff |
| summon ecosystem | Death Knight, Homunculus, Vessel, Skulls, Soulmaster etc. | owner attribution and summon lifecycle remain provider-owned |
| Battle Standard AI spells | summon-internal `gild_summon` sub-action | registry-visible but excluded from strict player-action metric |
| DTE integration | two counted addon spells on Dream Ripper plus one Nightmare AI spell | physical DTE presence activates the registry branch; do not duplicate DTE ownership |
| Apothic/Ace integration | attributes/helpers consumed by Requiem | external libraries remain authorities for their own contracts |

## Semantic boundary

Exact source registrations: **58**.

Strict semantic actions: **53**.

Excluded implementation/residual roots: **5**.

The provider is cataloged independently even though its CurseForge category path in the sibling is only `Addons`; category taxonomy does not determine semantic ownership.

## Runtime boundary

Catalog closure is not an assembled-pack compatibility PASS.

Keep fail-closed:

- deployed host config;
- source/JAR byte equivalence;
- max-HP and effect cleanup;
- weapon swap during casts;
- summon death/reentrancy;
- multiplayer attribution;
- DTE optional integration after reload;
- external attribute stacking.
