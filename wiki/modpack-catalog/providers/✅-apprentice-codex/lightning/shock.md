# Shock

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:shock`
- **Iron's school:** Lightning
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Instant
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 500`
- `spellPowerPerLevel = 50`
- `baseManaCost = 15`
- `manaCostPerLevel = 2`
- `castTime = 0`
- combat targeting range: **24 blocks**

Raw damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.SHOCK`.

## Targeting

Server-side targeting uses two provider raycast passes:

1. thin assisted raycast width **1.0** over 24 blocks;
2. if no target, wide assisted raycast width **4.0** over the same combat range.

If neither pass resolves a valid combat target, the spell still creates its visual bolt toward a block/empty position up to **16 blocks**, but applies no entity damage.

The visual Shock Bolt life is randomized from **5–8 ticks**. Damage itself is settled immediately server-side before the visual bolt entity is spawned.

## What it does

Provider guide semantics: fires a compact lightning bolt converted from elemental energy. It is a simple, low-cooldown direct Lightning attack rather than a persistent projectile authority.

## Causality

The bolt entity is presentation after immediate server-side damage settlement. A future integration must not treat later visual-bolt callbacks as a second damaging cast.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **fast low-cooldown assisted-target direct lightning strike** niche. A Black Arcana lightning zap with the same targeting/cooldown identity would be redundant.

## Confidence

`SOURCE-PINNED SPELL + SERVER TARGETING / PACK CONFIG MULTIPLIER + VISUAL CLIENT QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:shock` → `SpellRegistry.reg("shock", Shock::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.shock.Shock`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/shock/Shock.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — fechamento das nove fichas (2026-10-14)

**Source:** [`shock/Shock.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/shock/Shock.java) · [`shock/ShockBoltEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/shock/ShockBoltEntity.java).

- **O dano é imediato, não do raio visual:** `Shock.onCast` resolve alvo por dois passes de `RaycastTools.raycastFromEye`: primeiro largura **1.0** e depois **4.0**, alcance de combate **24 blocos**. Se houver alvo, aplica `CombatTools.applyDamage` **antes** de criar `ShockBoltEntity`; se não houver, clip de até **16 blocos** define somente o ponto visual do disparo vazio.
- **Lifetime da entidade:** `ShockBoltEntity` tem `noPhysics=true`, lifetime aleatório **5–8 ticks**, endpoints/path seed/flag de impacto sincronizados; `tick` só cuida de partículas no cliente e descarte por idade. A entidade salva coordenadas finais, seed e lifetime, mas não reaplica dano.
- **QA:** wall-hit, alvo multipart, raycast estreito/amplo, condições PvP/claims e VFX após recast. Não contar o bolt cosmético como nova ação de combate.

🟡 Dossiê causal source-level; ⚠️ equivalência bytecode/JAR/config, PvP/claims e QA Survival/dedicated pendentes; ⛔ sem adapter Mastery/perks real. Black Arcana não apropria casts, mana ou efeitos do provider.
