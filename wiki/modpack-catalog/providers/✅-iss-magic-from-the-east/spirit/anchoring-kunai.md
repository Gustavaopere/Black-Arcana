# Anchoring Kunai

- **ID:** `iss_magicfromtheeast:anchoring_kunai`
- **School:** Spirit
- **Levels:** 1–8
- **Min rarity:** Uncommon
- **Cast:** Instant
- **Mana neutral:** 20–90
- **Direct damage neutral:** 3–10
- **Cooldown:** 90 s
- **Recast count:** 3, recast window 100 ticks / 5 s
- **Anchored Soul duration on target:** `5×level + 10` s = 15–50 s
- **Tooltip linked damage:** `(level+1)×5%` = 10–45%
- **Static event-path linked damage after teleport:** approximately 1–4.5%; see QA

## Contract

Each cast throws an `AnchoringKunaiProjectile` at speed 1.2. It pierces shields, deals direct Spirit damage on an entity hit and applies `ANCHORED_SOUL` with the spell level as amplifier for 15–50 s.

If that affected entity teleports, `AnchoredSoulEffect` creates an `ExtractedSoul` at the **pre-teleport position**, sets its HP equal to the target's current HP, gives it a 10 s lifetime and removes the Anchored Soul effect. Unlike Spirit Challenging, this ExtractedSoul does **not** call `enableRadius()`, so the 12-block break-link punishment is not part of this path.

Damage to the created soul is then proxied to its owner through the shared `SoulChallengingEvents` mechanism.

## QA — percent mismatch

The spell tooltip advertises 10–45%. The teleport handler computes `(effect amplifier + 1) × 0.5` and passes that value to `ExtractedSoul.setBonusPercent`, which divides by 100. With amplifier = spellLevel, the stored coefficient is therefore about **0.01–0.045 = 1–4.5%**, one tenth of the tooltip claim. This is recorded as a static-source bug/divergence; no silent normalization is allowed.

## Dedup / authority

Identity = shield-piercing teleport trap that leaves behind a damage-proxy soul at the origin. Event authority is `EntityTeleportEvent` + `ExtractedSoul`; do not implement a second teleport observer.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`AnchoringKunaiSpell.java` + `AnchoringKunaiProjectile.java` + `AnchoredSoulEffect.java` + `ExtractedSoul.java` + `SoulChallengingEvents.java`, source 1.1.5.
