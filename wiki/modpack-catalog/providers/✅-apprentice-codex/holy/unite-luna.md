# Unite Luna

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:unite_luna`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 160`
- `manaCostPerLevel = 160`
- `castTime = 0`
- `setAllowCrafting(false)`
- `allowLooting() = false`

Raw moon-projectile damage:

`20 * spellPower / 100`

then multiplied by `DamageMultiplierKey.UNITE_LUNA`.

## Spawn lifecycle

A successful server-side cast normalizes the caster look direction, creates one `UniteLunaMoonEntity`, seeds its damage, picks a collision-safe spawn position near the caster eye/weapon area and launches it along that direction.

Spawn placement attempts several offsets before falling back to the base position; it therefore does not blindly instantiate the moon inside nearby solid geometry.

## What it does

Provider guide semantics: a latent spell unique to the Unite Luna Staff. Waving it creates a crescent moon that obliterates hostile/disturbing entities. The guide states that attempts to negate the moon's magic are converted into greater power.

The exact anti-negation/counterspell amplification behavior belongs to `UniteLunaMoonEntity`; this catalog does not infer the formula from guide text without the entity audit.

## Acquisition / item binding

Explicitly non-craftable and non-lootable. Provider guide identifies it as a latent staff capability.

## Deduplication

Occupies the **high-damage Holy crescent projectile with provider anti-negation behavior** niche. Black Arcana anti-magic systems must not both negate and independently amplify the same provider projectile.

## Confidence

`SOURCE-PINNED SPELL + PROJECTILE SPAWN / MOON ANTI-MAGIC AMPLIFICATION FORMULA + PACK CONFIG QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:unite_luna` → `SpellRegistry.reg("unite_luna", UniteLuna::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.uniteluna.UniteLuna`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/uniteluna/UniteLuna.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — fechamento das nove fichas (2026-10-14)

**Source:** [`uniteluna/UniteLuna.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/uniteluna/UniteLuna.java) · [`uniteluna/UniteLunaMoonEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/uniteluna/UniteLunaMoonEntity.java).

- **Trajetória:** `UniteLuna.spawnMoon` cria uma lua na direção do olhar após tentativas de spawn sem colisão e fallback para posição base. `UniteLunaMoonEntity.tickServer` segue `DECELERATE` por **15 ticks** e passa a `PHASE_HOMING`, porém `tickHoming` comenta e implementa **aceleração reta** sem selecionar alvo (até **120 ticks**), seguido de dissipação quando não impacta.
- **Antimagia não é neutralização:** `onAntiMagic` chama `explodeByAntiMagic` se ainda não explodiu. O código define `COUNTERSPELL_DAMAGE_MULTIPLIER=3.0` e visual ampliado (`COUNTERSPELL_BURST_CUBE_SIZE=2 × 11`), enquanto impacto normal `explode` usa multiplicador `1.0`. Isso é um risco source-level explícito para integração com Counterspell/PvP; dano real exige QA físico.
- **Persistência:** NBT guarda `Phase`, `BurstKind`, `BurstCubeSize` e direção do movimento. Não tratar duas fases ou Counterspell como dois casts nem assumir que a política BA neutraliza automaticamente essa entidade provider-owned.

🟡 Dossiê causal source-level; ⚠️ equivalência bytecode/JAR/config, PvP/claims e QA Survival/dedicated pendentes; ⛔ sem adapter Mastery/perks real. Black Arcana não apropria casts, mana ou efeitos do provider.
