# Sky Edge

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:sky_edge`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 500`
- `spellPowerPerLevel = 0`
- `baseManaCost = 80`
- `manaCostPerLevel = 15`
- `castTime = 30 ticks`
- targeting/raycast range: **64 blocks**
- inaccuracy scalar: **0.75**

Raw per-projectile damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.SKY_EDGE`.

Projectile count begins at `spellLevel + 3`, with source-pinned bonuses:

- level 4+ and spell power >= 700: +1 projectile;
- level 5 and spell power >= 900: another +1.

Each projectile receives a random standby delay of roughly **10–15 ticks** and a speed between **2.4–2.5**. Spawn points are selected around the caster with collision checks and a fallback toward eye position.

## What it does

Provider guide semantics: summons multiple weapon-like projectiles, winds them up, then fires toward the caster's line of sight. The attacks cause no knockback and can ignore the target's normal invulnerability frames according to the provider guide.

The spell is one cast with multiple child projectiles. Integration/mastery logic must deduplicate those child hits rather than counting them as independent spell casts.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **delayed Lightning multi-projectile volley / i-frame-bypassing barrage** niche. Black Arcana should not recreate an equivalent orbiting/wind-up projectile volley merely with different VFX.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / PROJECTILE DAMAGE-TYPE RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:sky_edge` → `SpellRegistry.reg("sky_edge", SkyEdge::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.skyedge.SkyEdge`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/skyedge/SkyEdge.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — fechamento das nove fichas (2026-10-14)

**Source:** [`skyedge/SkyEdge.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/skyedge/SkyEdge.java) · [`skyedge/SkyEdgeProjectileEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/skyedge/SkyEdgeProjectileEntity.java).

- **Fan e standby:** `SkyEdge.onCast` invoca `spellLevel + 3` projéteis, podendo ganhar +1 em nível 4 com spell power ≥700 e outro +1 em nível 5 com power ≥900. Cada lançamento escolhe posição por tentativas de `noCollision` e fallback no olho; direção deriva de raycast até 64 blocos + dispersão, velocidade de **2.4–2.5**, espera randômica **10–15 ticks**.
- **Entidade/impacto:** `SkyEdgeProjectileEntity.tick` expira acima de **100 ticks** e só movimenta/colide após standby; respeita cancelamento de impacto por `EventHooks.onProjectileImpact` inclusive com `ProjectileCollisionTools.continueAfterCancelledImpact` para certos hits de bloco físicos. `onHitEntity` aplica dano sem knockback e descarta; `onAntiMagic` descarta. NBT salva dano e standby.
- **QA:** PvP/claims, posições de fallback, impacto cancelado, multi-alvo e contagem de projéteis por spell power; não multiplicar crédito de progressão por flecha.

🟡 Dossiê causal source-level; ⚠️ equivalência bytecode/JAR/config, PvP/claims e QA Survival/dedicated pendentes; ⛔ sem adapter Mastery/perks real. Black Arcana não apropria casts, mana ou efeitos do provider.
