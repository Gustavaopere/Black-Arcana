# 05A.10 — RPG Skill Tree Integration

## Objective
Allow the RPG Skill Tree to contribute Arcane Resistance, Corruption Resistance and future hazard modifiers through the public Black Arcana API.

## Rules
- Black Arcana does not read RPG internal attachments/services directly for hazard resistance.
- The RPG adapter registers provider contributions through Black Arcana-owned interfaces.
- Contributions are snapshotted at the hazard activation boundary and cannot change an already committed cast.
- Mastery/attribute gates remain separate from resistance; meeting a cast requirement does not imply backlash immunity.
- Missing/incompatible RPG integration contributes zero and does not disable Black Arcana.
- No recursive mastery gain from backlash damage.

## Acceptance
Integration tests prove provider presence/absence, snapshot immutability, bounded contributions, no mastery feedback loop and fail-closed behavior for incompatible API signatures.
