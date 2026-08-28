# 03.05 — RPG Skill Tree

## Intent
Connect Black Arcana to the user's canonical RPG attributes/mastery/perk system rather than inventing a competing level system.

## Contract targets
- query canonical attributes;
- query mastery/knowledge gates;
- emit mastery-use events only after meaningful successful casts;
- expose Black Arcana tags/categories for perks;
- prevent recursive XP/event feedback.

## Acceptance
A fake/real adapter can gate a spell by attribute+mastery, award bounded mastery for a successful cast and award nothing for denied/spam casts.
