# 03.01 — Iron's Spells 'n Spellbooks

## Intent
Use Iron's as the preferred host for conventional active Black Arcana spells when its API is suitable, while keeping Black Arcana execution/safety rules authoritative for Black Arcana-specific mechanics.

## Investigate/freeze
- supported addon registration API for 1.21.1;
- school/spell registration ownership;
- mana read/consume/refund semantics;
- casting items/slots and spell selection interoperability;
- attributes, cooldowns, damage sources and events;
- client presentation extension points.

## Acceptance
One synthetic Black Arcana spell registers through the supported API, consumes the expected resource once, obeys core cooldown/safety validation and works on dedicated server.
