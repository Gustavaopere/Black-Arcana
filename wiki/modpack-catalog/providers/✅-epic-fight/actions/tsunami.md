# Tsunami

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:tsunami`
- Owner/reachability: `minecraft:trident` with vanilla **Riptide**
- Semantic type: deliberate supernatural tide/mobility attack
- State: `COUNTED_EXACT`

## Gate posterior — handler instalado, ainda sem hit real (18/10/2026)

✅ [Preflight NeoForge Java21 #39098101364](../EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md) observou no `LivingEntity` carregado exatamente um handler Epic Fight de absorção de armadura. **Não houve ataque Tsunami, ativação da variante água/chuva ou passagem de `EpicFightDamageSource` por esse método em runtime.** ⚠️ alcance/dano/AA e cliente pendentes; ⛔ adapter.

## Semântica delimitada de armadura e stun (18/10/2026)

✅ [Consumidores binários Java21 #39096586191](../EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md): `ARMOR_NEGATION_MODIFIER.adder(100)` alimenta o acumulador de negação de `EpicFightDamageSource`. O ramo compilado de `MixinLivingEntity` aplica `min(A×0.01,1)` e calcula no `CombatRules` apenas o dano restante, **se** a fonte satisfizer as guardas. `KNOCKDOWN` permanece `STUN_TYPE` de fase, não dano mágico automaticamente. Distância do avanço, área, alvos, efeito de água/chuva e dano líquido em jogo continuam **NÃO VERIFICADO**; sem adapter.

## Vínculo do registro comprovado — 18/10/2026

✅ [JAR publisher Java21 #39095049311](../EXACT-TRIDENT-REGISTRY-BOOTSTRAP-LINKAGE-21.17.3.1.md): `String tsunami → InvokeDynamic #68 → DeferredRegister.register → TSUNAMI`; `BootstrapMethods` associa ao método `EpicFightSkills.lambda$static$42` (`ConditionalWeaponInnateSkill`). **ID → builder** comprovado para as propriedades abaixo, sem provar alcance/dash ou hit em runtime.

## Prova posterior de propriedades compiladas (18/10/2026)

✅ [JAR 21.17.3.1, Java21 #39094435160](../EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md): `EpicFightSkills.lambda$static$42` para `ConditionalWeaponInnateSkill` passa `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE=KNOCKDOWN`, tag `WEAPON_INNATE`, e vincula `setAnimations`. Prova da **entrada de fase**, não do impacto no HP, área, dash ou acerto. O registro exato normal/reforçado em água/chuva segue em auditoria separada. ⛔ Perks e mudança de targeting sem hook real.

## Technical parameters for perks — exact JAR vs adjacent source

✅ **Exact publisher JAR 21.17.3.1:** packaged `data/epicfight/skill_parameters/tsunami.json` declares **`consumption=50.0`**, unit/charge settlement unverified. The [bounded Java21 proof #39093719405](../EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md) confirms `isInWaterOrRain` with two compiled results in `EpicFightSkills` and both animations `TSUNAMI` / `TSUNAMI_REINFORCED`. `ConditionalWeaponInnateSkill` selects an animation and invokes `playAnimationSynchronized`. This establishes an environmental selection seam, not measured dash distance/damage.

✅ **Valores de builder confirmados no binário exato 21.17.3.1; source 21.17.3 é referência independente:** `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE KNOCKDOWN`, and tag `WEAPON_INNATE` in its configured attack phase. [Source L352–360](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L352-L360). The constant 100 is not proof of a 100% HP-damage bonus or full armor bypass.

**Perk axes:** target, range, dash length, AOE radius, hitbox, projectile velocity/scale, real damage type, cast duration, cooldown and settled cost remain **NÃO VERIFICADO**. A perk may not permanently apply the rain variant or duplicate water particles as casts; both animations belong to one Tsunami root. ⛔ External retarget/range manipulation without safe provider hook.

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Tsunami when the trident has Riptide.

Because Riptide is the first selector branch, this path takes precedence over the Channeling and Loyalty branches in the same exact selector.

## Exact provider behavior

The exact artifact packages dedicated Tsunami animation resources and provider Tsunami particle paths. Exact control flow also chooses a strengthened action variant when the server player is in water or rain.

Water/rain state modifies this same Tsunami identity. It does not create a second semantic root.

## Deduplication boundary

Dash/movement, particles, animation, hits, damage and the strengthened environmental variant are parameters or consequences of the one provider-owned action.

## Authority boundary

Epic Fight remains authority for movement, resource state, animation, target/hit processing and all settlement. Black Arcana catalogs the action but must not duplicate it.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.
