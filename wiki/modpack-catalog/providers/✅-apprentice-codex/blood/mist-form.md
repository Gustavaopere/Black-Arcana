# Mist Form

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mist_form`
- **Iron's school:** Blood
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 15`
- `baseManaCost = 150`
- `manaCostPerLevel = 30`
- `castTime = 30 ticks`
- nearby-awareness suppression radius: `32 blocks`

## Duration

Exact spell source computes the applied Mist Form duration as:

`round(10 * 20 * spellPower / 100)` ticks

or equivalently ten seconds scaled by effective spell power.

## What it does

The provider guide describes a temporary mist-like state that:

- slightly improves mobility;
- allows passage through some blocks;
- briefly distracts/suppresses nearby enemy awareness when activated;
- can destabilize/cancel when the user attacks;
- makes the user **extremely vulnerable to fire and Holy spells**.

The spell source applies the provider's `MIST_FORM` effect server-side and explicitly suppresses nearby awareness in a 32-block radius at cast completion.

## Safety / overlap

This is a transformation/phasing/evasion spell with a strong weakness tradeoff. It overlaps Black Arcana observation/displacement and Blood-state design at the semantic level but remains an Iron's Blood spell owned by Apprentice's Codex.

Black Arcana must not:

- mirror the effect into a second transformation state;
- independently suppress the same mobs' awareness;
- grant phasing merely because this provider effect is active without an explicit bridge;
- award continuous mastery for every Mist Form tick.

## Acquisition

Uses the Iron's spell registry/scroll model. Exact 0.9.7.1 loot and recipe acquisition remains pending provider data audit.

## Confidence

`SOURCE-PINNED SPELL CONFIG + SERVER APPLICATION PATH + PROVIDER GUIDE / EFFECT INTERNAL DETAILS AND PACK RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`MistForm.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/mistform/MistForm.java); classe `jp.aquafactory.apprenticecodex.spell.mistform.MistForm`.
- **Registro comprovado:** `SpellRegistry.reg("mist_form", MistForm::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.

## Engenharia de perks — cadeia causal exata

- **`MistForm.onCast`** aplica `EffectRegistry.MIST_FORM` apenas no servidor, amplificador zero, duração `Math.round(200*getSpellPower(level,caster)/100)` ticks. `SummonedFirearmTools.suppressNearbyAwareness` é chamado com raio fixo `32.0D` após ativar o efeito.
- **Perks:** duração (associada ao spell power) e awareness radius (constante da classe) têm contratos distintos. Invulnerabilidade, phasing, interrupção ao atacar e vulnerabilidade a Fire/Holy dependem do MobEffect/handlers do provider; não modificar por equivalência temática nem repetir suppression a cada tick de Mastery.

**Confiança:** source auditado do commit fixado 0.9.7.1; hooks externos de mutação e teste em Survival permanecem pendentes.
