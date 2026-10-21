# Illuminate Stellar

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:illuminate_stellar`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 80`
- `manaCostPerLevel = 80`
- `castTime = 0`
- `setAllowCrafting(false)`
- `allowLooting() = false`

Raw damage per spawned star:

`2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.ILLUMINATE_STELLAR`.

## Exact star fan

A cast spawns **3–4** Illuminate Stellar star entities.

- total even-distribution yaw spread: **120°**;
- each star gets an additional random yaw offset up to ±10°;
- pitch randomization up to ±10°;
- fallback assisted target search: **64 blocks**, raycast width **2**;
- spawn positions are collision-checked progressively closer to the caster before falling back to the base position.

Each child star receives the provider damage value, drift direction and optional fallback target. The star entity owns subsequent targeting/travel/hit behavior.

## What it does

Provider guide semantics: a latent spell unique to the Illuminate Stellar Staff. Waving the staff spreads twinkling stars that fly toward entities with malevolent intent.

## Acquisition / item binding

The spell is explicitly non-craftable and non-lootable. The provider guide identifies it as a latent staff capability; exact staff exposure/equipment rules remain provider-owned.

## Causality/deduplication

Three or four spawned stars remain child effects of **one** provider cast. Mastery, hazards and offensive proc integrations must not count each star as a new cast.

## Confidence

`SOURCE-PINNED SPELL + SPAWN FAN / STAR ENTITY HOMING-HIT DETAILS + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:illuminate_stellar` → `SpellRegistry.reg("illuminate_stellar", IlluminateStellar::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.illuminatestellar.IlluminateStellar`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/illuminatestellar/IlluminateStellar.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — fechamento das nove fichas (2026-10-14)

**Source:** [`illuminatestellar/IlluminateStellar.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/illuminatestellar/IlluminateStellar.java) · [`illuminatestellar/IlluminateStellarStarEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/illuminatestellar/IlluminateStellarStarEntity.java).

- **Um cast, múltiplos projéteis:** `IlluminateStellar.spawnStars` cria **3–4 estrelas** com dispersão em leque de 120°, ruído angular de ±10° e fallback de alvo via raycast até 64 blocos. As posições de spawn são verificadas com `noCollision` em distâncias decrescentes; caso todas falhem, retorna a posição base, sem prova de segurança geométrica absoluta.
- **Fases da estrela:** `IlluminateStellarStarEntity.tickServer`: `DRIFT` **20–25 ticks**, `WAIT` **10–15 ticks**, `LAUNCH` até **60 ticks**, velocidade `1.48`; nova busca em região até 32 blocos no lançamento. `onHitEntity` aplica dano provider-owned e descarta; `onAntiMagic` termina com efeito visual, não uma segunda causa de dano.
- **Persistência condicionada:** NBT salva `TargetEntityId`/`FallbackTargetEntityId` como IDs de entidade de runtime, não UUID. Validar semântica de retomada após save/restart, recast/cancelamento, alvo inválido e stress 3–4 projéteis por cast; nenhum efeito derivado gera novo cast.

🟡 Dossiê causal source-level; ⚠️ equivalência bytecode/JAR/config, PvP/claims e QA Survival/dedicated pendentes; ⛔ sem adapter Mastery/perks real. Black Arcana não apropria casts, mana ou efeitos do provider.
