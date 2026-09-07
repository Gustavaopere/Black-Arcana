# Extract

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:extract`
- **School:** Nature
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 0.5 s
- **Crafting:** disabled
- **Looting:** disabled
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 30`
- `manaCostPerLevel = 90`
- `castTime = 10 ticks / 0.5 s`

Potion amplification is derived from spell power:

- power `<= 100` → amplification bonus `0`;
- otherwise: `floor((spellPower - 100) / 100)`.

## Admission and flask authority

Extract is not a generic potion-creation spell. It requires an **Apprentice's Codex Alchemist's Flask** held in either hand with at least one extractable stored dose.

Before casting, the provider:

1. searches main hand and off hand for `AlchemistsFlask`;
2. requires `AbstractPotionFlaskItem.canExtractOneDose(...)`;
3. snapshots the selected hand and the exact stored item into cast data;
4. rejects casts with no flask or no extractable dose.

At execution, it re-resolves that flask and only accepts the original stored item when `ItemStack.isSameItemSameComponents(...)` still matches. If the held state changed incompatibly, the cast does not invent a replacement potion.

## Effect settlement

On the server, the provider creates the extracted potion through its own flask API, spawns an `ExtractPotionProjectileEntity`, and consumes the resolved flask dose **only if the projectile was successfully added to the level**.

This ordering is an important transactional property: failed projectile creation does not spend a dose as though the effect had succeeded.

If the stored vanilla potion type is mismatched for its normal use, provider logic can force the extracted thrown form and explicitly warns the player before completion.

## Authority / deduplication

The Alchemist's Flask owns stored-dose identity and dose consumption. Iron's owns the spell cast/mana lifecycle. Apprentice's Codex owns conversion into the thrown potion projectile.

Black Arcana must not:

- maintain a second flask-dose ledger;
- consume the dose again after observing the cast;
- duplicate the potion projectile/effects;
- expose Extract as a generic free potion source detached from the provider flask.

For progression, one Extract cast is one causal action. Potion splash targets are downstream results, not separate casts.

## Confidence

`SOURCE-PINNED FLASK ADMISSION + CAST SNAPSHOT + PROJECTILE/DOSE SETTLEMENT / FULL MODPACK POTION-COMPAT RUNTIME QA PENDING`