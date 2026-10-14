# Dual Acrobat

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:dual_acrobat`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 75`
- `spellPowerPerLevel = 65`
- `baseManaCost = 5`
- `manaCostPerLevel = 5`
- `castTime = 60 ticks / 3 s`
- range: **16 blocks**

Raw shot damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.DUAL_ACROBAT`.

## Cast lifecycle

The spell summons a dual-SMG entity for the duration of continuous casting. While channeling it refreshes the weapon's damage from current spell power every cast tick so provider item effects such as Focus Staffbow adjustments remain reflected.

Cast completion or cancellation releases the summoned weapon. The weapon entity owns actual firing cadence and hit settlement.

The spell is marked as affected by the provider's Magi Agent Suit contract; that provider equipment may change interruptibility and is not RPG Skill Tree authority.

## What it does

Provider guide semantics: summons two magical SMGs and sprays fire forward after a brief charge. The shots cause no knockback and can ignore target invulnerability frames.

A three-second barrage is one continuous provider cast. Per-shot callbacks must not be promoted into independent Black Arcana/RPG casts or proc chains.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **short continuous dual-SMG Lightning barrage / no-knockback i-frame bypass** niche.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / SMG FIRING ENTITY + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:dual_acrobat` → `SpellRegistry.reg("dual_acrobat", DualAcrobat::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.dualacrobat.DualAcrobat`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/dualacrobat/DualAcrobat.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:dual_acrobat`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [DualAcrobat.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/dualacrobat/DualAcrobat.java); [DualAcrobatSmgEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/dualacrobat/DualAcrobatSmgEntity.java); [DualAcrobatCounterSpellEvent.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/dualacrobat/DualAcrobatCounterSpellEvent.java).

**Cadeia causal verificada no source:** DualAcrobat.onCastNoWeapon cria SMG; onCastTickWithWeapon recalcula dano; onCastCompleteWithWeapon libera a arma. DualAcrobatSmgEntity.tickOnServer mantém formação, inicia shooting após startup, alterna lado a cada FIRE_INTERVAL_TICKS=2, realiza raycast e dano pelo CombatTools; releaseWeapon descarta. DualAcrobatCounterSpellEvent.onCounterSpell, prioridade LOWEST, descarta a arma do cast ou as armas do mesmo owner num fallback limitado a 16 blocos somente se o evento não foi cancelado.

**QA direcionado (pendente):** Contramágica coexistindo com cancelamentos anteriores, múltiplas entidades por owner, startup e shots ao relogar, ownership e performance.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
