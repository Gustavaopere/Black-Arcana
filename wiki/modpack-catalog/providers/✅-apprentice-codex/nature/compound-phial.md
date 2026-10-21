# Compound Phial

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:compound_phial`
- **School:** Nature
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Long
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 15`
- `baseManaCost = 10`
- `manaCostPerLevel = 4`
- `castTime = 10 ticks`
- projectile speed: **1.0**

Raw damage:

`4 + 2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.COMPOUND_PHIAL`.

Splash radius:

`1.75 + max(0, spellLevel - 1) / 9`

Thus the spell grows gradually from 1.75 blocks at level 1 to 2.75 blocks at level 10 before any entity-specific collision details.

## What it does

A successful cast creates one `CompoundPhialProjectileEntity`, launches it from the caster and seeds damage, splash radius and a randomized potion color.

Provider guide semantics: instantly compounds a potion-like projectile and hurls it; its attack bypasses armor according to provider-facing text and can also catch the caster in the splash.

The projectile entity owns final collision/damage causality. One splash may hit multiple entities but remains one provider cast.

## Deduplication

Occupies the **fast Nature thrown-phial / scalable splash damage** niche. Black Arcana alchemical magic should not duplicate this as another instant thrown flask without materially different forbidden-resource/risk semantics.

## Confidence

`SOURCE-PINNED SPELL / PROJECTILE DAMAGE-TYPE + FULL SPLASH SETTLEMENT + PACK CONFIG QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:compound_phial` → `SpellRegistry.reg("compound_phial", CompoundPhial::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.compoundphial.CompoundPhial`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/compoundphial/CompoundPhial.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — utilidades, persistência e recursos (2026-10-14)

**Registry:** `apprenticecodex:compound_phial`. **Proveniência source:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1); classes e helpers: [CompoundPhial.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/compoundphial/CompoundPhial.java); [CompoundPhialProjectileEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/compoundphial/CompoundPhialProjectileEntity.java).

**Cadeia causal no código-fonte:** CompoundPhial.onCast cria projétil com damage, splashRadius, potion color e lança via shootFromRotation. CompoundPhialProjectileEntity.onHitBlock/onHitEntity chama onImpact e descarta; onImpact resolve multipart para cada target e usa HashSet de entidades resolvidas para liquidar CombatTools.applyDamage uma vez por entidade, com falloff mínimo e CombatTargetPolicy.ALLOW_SELF_PROTECT_ALLIES. Partículas/evento de cor e splash são efeitos derivados, não novos casts.

**QA prioritário pendente:** Alcance/oclusão, impacto em vários hitboxes de entidade, splashes repetidos em eventos, política friendlies/PvP e anti-magic.

**Governança:** o host Iron's controla cast/mana/recast; o addon controla o estado/efeito/custo especializado verificado. Um pulso, dano periódico, bloco, item gerado, job tick, cast visual ou cast derivado não é uma identidade semântica nova nem gatilho de Mastery/XP automático. Black Arcana não reprocessa recursos, eventos, mutação do mundo ou callback dos providers. ⚠️ Source-level não comprova bytecode idêntico/config efetiva/teste físico. ⛔ Nenhum contrato de RPG Skill Tree perks/Mastery homologado: fail-closed.
