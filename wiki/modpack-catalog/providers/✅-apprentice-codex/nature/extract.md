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

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:extract` → `SpellRegistry.reg("extract", Extract::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.extract.Extract`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/extract/Extract.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
