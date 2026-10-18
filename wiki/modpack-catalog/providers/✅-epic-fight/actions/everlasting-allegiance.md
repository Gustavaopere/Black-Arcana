# Everlasting Allegiance

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:everlasting_allegiance`
- Owner/reachability: `minecraft:trident` with vanilla **Loyalty**
- Semantic type: deliberate supernatural damaging trident recall
- State: `COUNTED_EXACT`

## Prova posterior de propriedades compiladas (18/10/2026)

✅ [JAR 21.17.3.1, Java21 #39094435160](../EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md): `EpicFightSkills.lambda$static$43` (`EverlastingAllegiance`) liga `ARMOR_NEGATION_MODIFIER adder(30)` e `DAMAGE_MODIFIER multiplier(1.4)` aos `Builder.addProperty`, além de `STUN_TYPE=HOLD` e `WEAPON_INNATE`. Há também `EXTRA_DAMAGE`, mas a composição inteira da expressão permanece fora deste gate. **Não significa 1,4× HP damage medido ou penetração efetiva de 30%.** ⛔ Sem alterações externas de recall/damage ou Mastery.

## Technical parameters for perks — exact JAR vs adjacent source

✅ **Exact publisher JAR 21.17.3.1:** `data/epicfight/skill_parameters/everlasting_allegiance.json` declares **`consumption=40.0`** (unit and actual debit not proven). [Java21 #39093719405](../EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md) verifies the compiled `checkExecuteCondition` reference to `THROWN_TRIDENT_ENTITY_ID` and a signed boundary, plus ordered references in `executeOnServer` to `recalledBySkill`, `playAnimationSynchronized`, `cancelOnServer`. This does **not** establish real trident return or damage/hit count.

✅ **Entradas numéricas e enums de fase agora compiladas no publisher 21.17.3.1, corroboradas pelo source adjacente 21.17.3:** `ARMOR_NEGATION_MODIFIER adder(30)`, `DAMAGE_MODIFIER multiplier(1.4)`, `STUN_TYPE HOLD`, `WEAPON_INNATE` tag and Sweeping Edge extra-damage object. [Source L363–371](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L363-L371). The 1.4 multiplier is an attack-phase input, **not** a measured final HP-damage multiplier.

**Perk axes:** target cap, hitbox/recall trajectory, projectile speed/scale, radius, range, return duration, real damage type, cooldown and cost actually settled are **NÃO VERIFICADO**. A future RPG Mastery bridge must associate all recall hits with the same provider-owned action without replaying recall or duplicating damage. ⛔ No adapter yet.

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Everlasting Allegiance when Loyalty is present and neither the earlier Riptide nor Channeling selector branch is selected.

This closes owner/reachability through the exact vanilla-trident + enchantment surface.

## Exact provider settlement

The exact skill obtains the provider patch for the tracked thrown trident and invokes `recalledBySkill()`.

Exact thrown-trident behavior then performs Epic Fight's provider-owned return path and entity-hit settlement.

This differs semantically from vanilla Loyalty's automatic passive return because Epic Fight exposes an explicit player skill action and its own damaging recall lifecycle.

## Deduplication boundary

Repeated hits or movement during the returning trident lifecycle are settlement of the same recall root, not separate spell identities.

## Authority boundary

Epic Fight owns thrown-trident tracking, skill activation, return path, hit processing and resource settlement. Black Arcana must not trigger a second recall or duplicate damage.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.
