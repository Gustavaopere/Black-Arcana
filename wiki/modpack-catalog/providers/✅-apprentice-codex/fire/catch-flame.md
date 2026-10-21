# Catch Flame

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:catch_flame`
- **Iron's school:** Fire
- **Levels:** 1–8
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 0.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 800`
- `spellPowerPerLevel = 75`
- `baseManaCost = 10`
- `manaCostPerLevel = 3`
- `castTime = 10 ticks`
- fixed range: **3 blocks**
- effect half-size around impact: **0.5 block**

Raw damage:

`spellPower / 100`

then multiplied by `DamageMultiplierKey.CATCH_FLAME`.

Burn duration:

`max((spellLevel - 1) * 20, 10)` ticks.

## Entity-hit behavior

The spell resolves a short-range raycast and builds a small impact AABB. Valid combat targets must intersect the impact volume and have line of sight from the resolved impact origin.

If a target is already burning, Catch Flame selects its dedicated penetrating damage type; otherwise it uses the standard Catch Flame damage type. On successful damage, remaining fire ticks are raised to at least the spell's burn duration.

## Block/world interaction

Catch Flame can ignite a targeted block surface and has a dedicated interaction for the provider's **Essence Smoker**.

Important world-safety facts from exact source:

- block ignition is gated by provider server config;
- Spell Dispenser casting has a separate ignition permission toggle;
- remote-owner and non-player casts are resolved separately;
- real-player interaction permissions are checked before ignition;
- `mayInteract` / `mayUseItemAt` checks are preserved;
- ordinary block ignition is routed through a Flint and Steel `useOn` flow so loader/land-protection events can deny it;
- Essence Smoker ignition executes only after provider hook/protection checks.

This is significant for Black Arcana: the addon owns these local Fire world effects. A bridge must not bypass provider protection checks or route the same ignition through Black Arcana `WorldEffectPolicy` a second time after the provider has already settled it.

## What it does

Provider guide semantics: kindles fire at close range; already-burning targets can be struck through normal invulnerability-frame behavior; it can ignite an Essence Smoker or place fire on a block surface. The implementation explicitly preserves land-protection/interact hooks.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **short-range Fire strike + burn + protected block ignition / Essence Smoker utility** niche. Black Arcana should not recreate the same convenience ignition spell or bypass these provider-owned checks.

## Confidence

`SOURCE-PINNED SPELL + TARGETING + IGNITION PATH / PACK CONFIG VALUES + FULL MODPACK LAND-PROTECTION QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`CatchFlame.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/catchflame/CatchFlame.java); classe `jp.aquafactory.apprenticecodex.spell.catchflame.CatchFlame`.
- **Registro comprovado:** `SpellRegistry.reg("catch_flame", CatchFlame::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.

## Engenharia causal aprofundada — utilidades, persistência e recursos (2026-10-14)

**Registry:** `apprenticecodex:catch_flame`. **Proveniência source:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1); classes e helpers: [CatchFlame.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/catchflame/CatchFlame.java); [CatchFlameImpactEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/catchflame/CatchFlameImpactEntity.java); [CatchFlameLoaderHooks.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/catchflame/CatchFlameLoaderHooks.java).

**Cadeia causal no código-fonte:** CatchFlame.onCast resolve raycast e aplica tryIgniteBlock, affectEntities, partículas e CatchFlameImpactEntity; o impacto visual possui shouldBeSaved=false, expira após 2 ticks e não é segunda explosão de dano. affectEntities deduplica combat targets, valida LOS, escolhe damage type segundo burning e só renova burnDuration se CombatTools.applyDamage teve sucesso. tryIgniteBlock verifica configurações de Spell Dispenser e caster não-jogador, pode checar mayInteract/mayUseItemAt, encaminha item flint-and-steel por useOn e trata EssenceSmoker separadamente.

**QA prioritário pendente:** Claims/protection/mods que interceptam useOn, disparo por dispenser/owner remoto, fire spread, dano PvP/LOS, limpeza de entity VFX não persistente.

**Governança:** o host Iron's controla cast/mana/recast; o addon controla o estado/efeito/custo especializado verificado. Um pulso, dano periódico, bloco, item gerado, job tick, cast visual ou cast derivado não é uma identidade semântica nova nem gatilho de Mastery/XP automático. Black Arcana não reprocessa recursos, eventos, mutação do mundo ou callback dos providers. ⚠️ Source-level não comprova bytecode idêntico/config efetiva/teste físico. ⛔ Nenhum contrato de RPG Skill Tree perks/Mastery homologado: fail-closed.
