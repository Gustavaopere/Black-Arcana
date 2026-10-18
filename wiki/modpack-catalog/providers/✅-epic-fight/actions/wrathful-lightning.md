# Wrathful Lightning

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:wrathful_lighting`
- Owner/reachability: `minecraft:trident` with vanilla **Channeling**
- Semantic type: deliberate supernatural lightning invocation
- State: `COUNTED_EXACT`

## Semântica delimitada dos modifiers após o builder (18/10/2026)

✅ [Consumidores binários Java21 #39096586191](../EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md): o `DAMAGE_MODIFIER.setter(8)` entra na semântica de `ValueModifier.ResultCalculator` (define a referência do valor a ser combinado; não fixa 8 HP na vítima). Os `MAX_STRIKES_MODIFIER.setter(1)` / `setter(3)` são usados por `AttackAnimation.getMaxStrikes`, não provam 1/3 acertos reais em toda situação. `ARMOR_NEGATION_MODIFIER.adder(100)` abastece `EpicFightDamageSource.calculateArmorNegation`; o mixin compilado usa `min(A×0.01,1)` antes de `CombatRules` quando a fonte é elegível. **⚠️** Mixin aplicado, ataques multi-phase e dano real não homologados; ⛔ sem perk de dano/alcance externo.

## Vínculo do registro comprovado — 18/10/2026

✅ [JAR publisher Java21 #39095049311](../EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md) demonstrou a sequência `String wrathful_lighting → InvokeDynamic #67 → DeferredRegister.register → WRATHFUL_LIGHTING`; o bootstrap aponta para `EpicFightSkills.lambda$static$40` (`WrathfulLightingSkill`), método que recebe os coeficientes abaixo. A relação **ID → builder** está comprovada no binário exato. ⚠️ Dano final/cast real pendentes.

## Prova posterior de propriedades compiladas (18/10/2026)

✅ [JAR 21.17.3.1, Java21 #39094435160](../EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md): no supplier `lambda$static$40` (`WrathfulLightingSkill`), o bytecode confirma, na ordem, `MAX_STRIKES_MODIFIER setter(1)` (primeiro grupo), `DAMAGE_MODIFIER setter(8.0)`, `MAX_STRIKES_MODIFIER setter(3)`, `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE=KNOCKDOWN` e `SOURCE_TAG=WEAPON_INNATE` no segundo grupo. São **entradas de AttackPhase**, não dano final nem limite de alvos medido. `EXTRA_DAMAGE` possui chave/builder presentes, mas a composição completa não foi dataflow-validada. Assim, os valores numéricos acima não dependem mais *somente* do source adjacente. ⛔ Hook/perk externo permanece bloqueado.

## Technical parameters for perks — exact JAR vs adjacent source

✅ **Exact publisher JAR 21.17.3.1:** packaged `data/epicfight/skill_parameters/wrathful_lighting.json` declares **`consumption=50.0`**, with resource unit/real debit unverified. [Java21 #39093719405](../EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md) additionally proves that `WrathfulLightingSkill.registerPropertiesToAnimation` has **two** compiled `addProperties` callsites within the method. This confirms the registration seam, not final damage or the number of real hits.

✅ **Valores agora confirmados também no classfile 21.17.3.1 (source 21.17.3 preservado como referência histórica):** first phase-property group contains `MAX_STRIKES_MODIFIER setter(1)`; second `DAMAGE_MODIFIER setter(8.0)`, `MAX_STRIKES_MODIFIER setter(3)`, `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE KNOCKDOWN` and `SOURCE_TAG WEAPON_INNATE`. These are exact-publisher compiled builder inputs, **not** guaranteed damage, armor bypass or runtime effects in 21.17.3.1. [Source L337–349](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L337-L349).

**Perk axes:** target type, range, radius/AOE, projectile dimensions/speed, damage type, cast ticks, duration, cooldown and realized cost are **NÃO VERIFICADO** by this class/JSON. ⛔ Do not inject additional thunder/damage or assign RPG Mastery from uncorrelated thunder callbacks. Epic Fight owns innate attack phases, animation, hits and charges; Black Arcana retains its own runtime.

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Wrathful Lightning when the trident has Channeling, after the Riptide branch and before Loyalty.

This selector closes current catalog reachability without inventing an Epic Fight-owned item: the owner surface remains the vanilla trident, while the enchantment selects the provider-owned innate.

The registry id intentionally uses `lighting`; the player-facing identity is **Wrathful Lightning**.

## Exact provider settlement

The exact skill/animation seam attaches Epic Fight's server-side `SUMMON_THUNDER` event to this skill action.

That establishes one provider-owned supernatural lightning root. The spawned lightning/event processing, particles, animation, damage and downstream hit consequences are settlement details of the same action rather than additional magic identities.

## Fallback boundary

If Riptide is present, the exact trident selector resolves Tsunami instead. Wrathful Lightning is therefore not simultaneously selected by the same innate-selector pass.

## Authority boundary

Epic Fight remains authority for battle mode, skill activation, animation, innate gauge/resource state, event execution and damage settlement. Black Arcana must not replay thunder or charge a second resource/cooldown cost.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.
