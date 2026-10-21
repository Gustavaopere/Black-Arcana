# Fujin

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:fujin`
- **Iron's school:** Evocation
- **Levels:** 1–10
- **Minimum rarity:** Uncommon
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 75`
- `baseManaCost = 5`
- `manaCostPerLevel = 1`
- `castTime = 100 ticks`
- projectile damage: `(1 + spellPower / 200) * providerDamageMultiplier`
- projectile range: **10 blocks**

## Provider lifecycle

The spell summons a `FujinKatanaEntity`, injects the computed projectile damage and 10-block range, and releases that weapon when the continuous cast completes.

The katana entity — not the top-level spell tick callback — owns projectile cadence. At the exact source pin the executable constants are:

- first slash at weapon tick **10**;
- subsequent slashes every **5 ticks**;
- slash animation speed `3.0`;
- one `FujinSlashProjectileEntity` spawned per slash.

Each projectile receives the damage frozen into the katana, the **10-block** maximum travel distance and the provider combat-owner UUID.

This executable entity cadence is authoritative for the audited snapshot. A comment in the top-level spell mentions a "10 tick interval", but the actual `FujinKatanaEntity.SLASH_INTERVAL_TICKS` value is **5**; the catalog therefore records the executable behavior rather than promoting the stale comment.

The source deliberately leaves firing cadence to the katana entity so ordinary cast-speed modification does not alter the internal 5-tick slash interval.

## Causality and progression

Repeated katana projectiles during the channel remain children of one continuous provider cast. Do not award spell-cast progression per projectile or infer cast-speed-scaled projectile frequency when the provider deliberately isolates that cadence.

Black Arcana must not duplicate the katana timer, projectile spawn, combat-owner attribution or projectile damage settlement.

## Deduplication

Occupies the **continuous summoned katana that emits short-range projectiles on a fixed provider-owned cadence** niche.

## Confidence

`SOURCE-PINNED SPELL + KATANA ENTITY / EXACT CONFIG+DAMAGE+10-BLOCK RANGE+FIRST-SLASH TICK 10+5-TICK INTERVAL+OWNER HANDOFF / PROJECTILE COLLISION DETAIL RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:fujin` → `SpellRegistry.reg("fujin", Fujin::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.fujin.Fujin`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/fujin/Fujin.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:fujin`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [Fujin.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/fujin/Fujin.java); [FujinKatanaEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/fujin/FujinKatanaEntity.java); [FujinSlashProjectileEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/fujin/FujinSlashProjectileEntity.java).

**Cadeia causal verificada no source:** Fujin.onCastNoWeapon conjura katana; onCastTickWithWeapon não dispara, porque o tick da katana controla a cadência independente da cast speed. FujinKatanaEntity.tickOnServer dispara slash em FIRST_SLASH_TICK e depois a cada SLASH_INTERVAL_TICKS, propagando combatOwnerUuid. FujinSlashProjectileEntity.tick verifica colisão de bloco por segmento, resolve alvos multipart, conserva victimUuids para não repetir dano por entidade e filtra oclusão antes de CombatTools.applyDamage; descarta ao colidir/atingir limite de distância.

**QA direcionado (pendente):** Colisões próximas de paredes/claims, UUID de vítima no save/restart, owner ausente, quantidade de slashes em channel longo e dedup.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
