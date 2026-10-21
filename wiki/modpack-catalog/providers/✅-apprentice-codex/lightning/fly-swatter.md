# Fly Swatter

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:fly_swatter`
- **Iron's school:** Lightning
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous lock-on
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 10`
- `manaCostPerLevel = 5`
- `castTime = 300 ticks / 15 s`
- lock-on/search range: **128 blocks**
- fixed explosion radius seeded into launcher: **3 blocks**

Raw missile damage:

`3 + 2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.FLY_SWATTER`.

Maximum locked targets:

`min(8, round(2 * spellPower / 100))`

Lock-on time per target:

`max(10, 40 - round(10 * spellPower / 100))` ticks.

## Lock-on lifecycle

During continuous casting the provider keeps `FlySwatterCastData` containing:

- current candidate entity id;
- current lock-on progress ticks;
- a serialized list of confirmed entity ids.

Holding the same valid entity in the caster raycast advances its lock timer. Looking away or losing the target resets current lock progress. Once the threshold is reached the entity id is appended to the confirmed lock list, up to the calculated maximum.

On cast completion, **only the confirmed list** is copied into the launcher; if it is non-empty the launcher begins firing. The launcher then owns homing/explosion execution.

## What it does

Provider guide semantics: summons a magical launcher, locks onto targets in line of sight, then sends homing attacks toward them.

A lock-on list is one cast outcome, not one independent cast per target/missile. Future progression bridges must not multiply mastery/procs by confirmed target count.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **continuous multi-lock → homing explosive volley** niche. Black Arcana should not add an equivalent target-painted missile launcher under Chaos/Lightning semantics without a materially different contract.

## Confidence

`SOURCE-PINNED SPELL + SERIALIZED LOCK DATA / MISSILE HOMING ENTITY DETAILS + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:fly_swatter` → `SpellRegistry.reg("fly_swatter", FlySwatter::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.flyswatter.FlySwatter`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/flyswatter/FlySwatter.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:fly_swatter`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [FlySwatter.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/flyswatter/FlySwatter.java); [FlySwatterLauncherEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/flyswatter/FlySwatterLauncherEntity.java); [FlySwatterProjectileEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/flyswatter/FlySwatterProjectileEntity.java).

**Cadeia causal verificada no source:** FlySwatter.onCastTickWithWeapon atualiza damage e lock-on por entity ID no AdditionalCastData com relógio de alvo contínuo. onCastCompleteWithWeapon transfere lockOnEntityIdList para a launcher e chama startFiring quando lista não vazia, sem checagem explícita de cancelled nesse método; isto merece QA, não inferência de bug físico. FlySwatterLauncherEntity.tickOnServer emite um projétil por target a cada FIRE_INTERVAL_TICK=5 e descarta quando liberado. FlySwatterProjectileEntity.onHitEntity aplica dano direto e onImpact exclui o directHitTarget do dano de explosão; colisão com bloco aplica área, anti-magic fizzle descarta sem efeito de explosão.

**QA direcionado (pendente):** Lock-on stale IDs, cancelamento no final, área/LOS de splash, custo de múltiplos foguetes, ownership e anti-magic.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
