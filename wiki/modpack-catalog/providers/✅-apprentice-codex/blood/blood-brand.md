# Blood Brand

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:blood_brand`
- **Iron's school:** Blood
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 4 s
- **Resource:** Iron's mana
- **Introduced/explicitly called out:** public 0.9.7.1 changelog
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 75`
- `baseManaCost = 35`
- `manaCostPerLevel = 10`
- `castTime = 0`
- burst radius: `5 blocks`

## Initial hit

Exact raw projectile damage:

`1 + spellPower / 100`

then multiplied by server config `DamageMultiplierKey.BLOOD_BRAND`.

The source comment explicitly characterizes the initial damage as intentionally low because the debuff/brand is the main mechanic.

## Death burst

Exact raw burst damage seeded by the spell:

`8 * spellPower / 100`

then multiplied by the same Blood Brand server damage multiplier.

The provider guide states:

- the projectile brands a damaged mob;
- when the branded mob dies, blood magic bursts against nearby mobs;
- healing equals **50% of health actually lost to the burst**;
- a killing blow from Higanbana causes a stronger burst;
- walls block the blood magic;
- the burst fails if the brand loses connection to its caster.

The precise stronger-Higanbana multiplier and brand lifecycle are owned by the provider's downstream entity/effect implementation and remain separate detailed QA items unless needed for a future bridge.

## Causality

Blood Brand is a particularly important deduplication case because one cast produces a delayed death-triggered effect. Correct causal identity is:

`Blood Brand cast -> branded victim -> qualifying death -> provider burst/heal`

Black Arcana must not treat the downstream burst as a second independent cast or generate normal offensive proc chains twice from the initial kunai plus death burst unless an explicit future integration contract defines that behavior.

## Acquisition

Uses Iron's spell registry/scroll infrastructure. Exact 0.9.7.1 acquisition distribution remains pending data audit.

## Confidence

`SOURCE-PINNED SPELL CONFIG + DAMAGE FORMULAS + SERVER PROJECTILE SPAWN + PROVIDER GUIDE / DOWNSTREAM BRAND ENTITY LIFECYCLE AND PACK CONFIG QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`BloodBrand.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/bloodbrand/BloodBrand.java); classe `jp.aquafactory.apprenticecodex.spell.bloodbrand.BloodBrand`.
- **Registro comprovado:** `SpellRegistry.reg("blood_brand", BloodBrand::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.

## Engenharia de perks — cadeia causal exata

- **`BloodBrand.onCast`** cria `BloodBrandKunai` somente em `ServerLevel`; entrega `setDamage`, `setBurstDamage`, `setBurstRange(5)` e `setProjectileVelocity` antes do spawn.
- **Dano de contato:** `(1 + getSpellPower/100)*DamageMultiplierKey.BLOOD_BRAND`; **dano bruto de explosão:** `(8*getSpellPower/100)*DamageMultiplierKey.BLOOD_BRAND`, onde a chave é resolvida por `ApprenticeCodexServerConfig.damageMultiplier`.
- **Alvo/direção:** `resolveLaunchGeometry` utiliza `RemoteOwnerCastContext` para `ServerPlayer` quando existe; caso contrário olhar e olhos do caster. A origem de cast remoto tem owner explícito.
- **Perks:** raio cinco é repassado à entidade, mas não é comprovado setter externo por evento. A morte de vítima marcada e burst/heal continuam no ciclo de `BloodBrandKunai`/status; implementar proc exige correlacionar cast e morte exatamente uma vez.

**Confiança:** source auditado do commit fixado 0.9.7.1; hooks externos de mutação e teste em Survival permanecem pendentes.
