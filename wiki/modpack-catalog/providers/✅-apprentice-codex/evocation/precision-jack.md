# Precision Jack

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:precision_jack`
- **School:** Evocation
- **Levels:** 1–4
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 1 s
- **Interruptible:** no
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 60`
- `manaCostPerLevel = 30`
- `castTime = 40 ticks / 2 s`
- fixed base damage: `6 * PRECISION_JACK damage multiplier`

Looting bonus:

`min(5, max(1, round(spellPower / 100)))`

Duplicate-loot-roll chance:

`min(30, max(0, round(spellPower / 10)))%`

## Attack-time snapshot

The provider writes damage, looting bonus and duplicate-drop chance into the summoned knife when it is created, and refreshes all three at the initial weapon cast. These values therefore belong to the attack context and are not recomputed by an external loot observer.

A successful completion triggers the provider knife slice; cancellation releases the weapon.

## Provider-owned drop settlement

`PrecisionJackLootingEvent` only acts when all causal checks match:

- the damage source is the provider `PRECISION_JACK` damage type;
- the victim is not a player;
- the direct damage entity is the provider `PrecisionJackKnifeEntity`.

If the duplicate chance triggers, the provider performs **one additional loot-table roll** using the target/entity damage context and player luck when kill credit is a player. Separately, the looting bonus can grow each resulting non-empty drop by a random `0..lootingBonus` amount.

Both caps are enforced again inside the event path: looting at 5 and duplicate chance at 30%.

## Authority / anti-double-processing

Precision Jack's loot mutation is provider-owned. Black Arcana or RPG integrations must not add a second looting pass, second loot-table roll or duplicate-drop chance from the same kill.

One successful Precision Jack kill remains one causal spell outcome even if several item entities result from the provider's loot settlement.

## Confidence

`SOURCE-PINNED SPELL + ATTACK SNAPSHOT + LIVING-DROPS SETTLEMENT / FULL MODPACK LOOT-TABLE COMPAT QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:precision_jack` → `SpellRegistry.reg("precision_jack", PrecisionJack::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.precisionjack.PrecisionJack`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/precisionjack/PrecisionJack.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:precision_jack`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [PrecisionJack.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/precisionjack/PrecisionJack.java); [PrecisionJackKnifeEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/precisionjack/PrecisionJackKnifeEntity.java); [PrecisionJackLootingEvent.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/precisionjack/PrecisionJackLootingEvent.java).

**Cadeia causal verificada no source:** PrecisionJack.onCastNoWeapon cria lâmina; updateAttackValues fixa damage/looting/duplicate chance e onCastTickWithWeapon prepara; onCastCompleteWithWeapon só chama slice no sucesso. PrecisionJackKnifeEntity.tickOnServer controla owner e timeouts, e slice usa hitsAabb para aplicar damage_type PRECISION_JACK. PrecisionJackLootingEvent.onLivingDrops restringe bonus a esse DamageType e à knife como direct entity; pode acrescentar uma execução extra da loot table, com chance limitada a 30%, e ampliar stacks originais com lootingBonus limitado a 5. Nenhuma dessas operações transforma cada drop em outro cast.

**QA direcionado (pendente):** Loot de mob modded, eventos concorrentes de drop, resgate de owner/weapon, morte de player explicitamente excluída, dupe/limite de itens e cadeia de XP.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
