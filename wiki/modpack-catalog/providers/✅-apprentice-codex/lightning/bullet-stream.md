# Bullet Stream

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:bullet_stream`
- **Iron's school:** Lightning
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 20`
- `spellPowerPerLevel = 100`
- `baseManaCost = 3`
- `manaCostPerLevel = 2`
- `castTime = 600 ticks / 30 s`
- fixed effective cast time: equipment cast-time modifiers do **not** alter the duration
- range: **32 blocks**
- spin-up: **40 ticks / 2 s**

Raw per-tick shot damage:

`0.5 + spellPower / 100`

then multiplied by `DamageMultiplierKey.BULLET_STREAM`.

## Exact minigun lifecycle

The summoned minigun:

- follows the caster and continuously aims at line of sight;
- begins firing once the 40-tick spin-up completes;
- calls its firing path **every server tick** after spin-up while the channel continues;
- applies damage with no knockback through the provider combat helper;
- refreshes current damage from the owner's current spell power rather than relying only on summon-time damage;
- plays its continuous firing sound every 10 firing ticks;
- after release, remains for a 10-tick spin-down lifecycle before discard.

Provider guide semantics state that its shots can ignore target invulnerability frames and that cancelling during spin-up still triggers normal cooldown. The spell intentionally keeps its 30-second maximum channel independent of equipment cast-time modifiers.

## Causality

A single Bullet Stream channel can generate hundreds of provider-owned hit callbacks. They are **not** hundreds of spell casts. Any mastery/perk/Black Arcana bridge must key off a suitable original cast identity and prevent per-tick offensive proc multiplication.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **spin-up → long sustained magical minigun barrage / i-frame bypass** niche. This is a particularly strong no-duplicate case for future Chaos/Lightning rapid-fire magic.

## Confidence

`SOURCE-PINNED SPELL + MINIGUN ENTITY / PROVIDER GUIDE I-FRAME SEMANTICS + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:bullet_stream` → `SpellRegistry.reg("bullet_stream", BulletStream::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.bulletstream.BulletStream`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/bulletstream/BulletStream.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — lote persistente 0.9.7.1

**Evidência source-located:** [`bulletstream/BulletStream.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/bulletstream/BulletStream.java) · [`bulletstream/BulletStreamMinigunEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/bulletstream/BulletStreamMinigunEntity.java). Source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, alinhado à release 0.9.7.1. **Não há demonstração de equivalência dos corpos de métodos compilados no JAR da modlist**, nem GameTest provider-native neste dossiê.

### Sequência e ownership

- **Canal contínuo e weapon:** `BulletStream.onCastNoWeapon` cria `BulletStreamMinigunEntity` associada ao caster; `onCastTickWithWeapon` e `onCastCompleteWithWeapon` fazem parte do ciclo de channeling do provider, não de uma nova root por tick. Dano, range e spin-up vêm de fórmulas e configuração da spell.
- **Tick server:** `BulletStreamMinigunEntity.tickOnServer` descarta arma sem owner `LivingEntity`. Quando ativa, acompanha o owner, faz raycast de mira a **64 blocos** para orientar a arma e só começa o ramo `fire` após `currentTick>=spinUpDelayTick`. A arma emite som periódico com `FIRING_SOUND_INTERVAL_TICKS=10`.
- **Disparo lógico:** `fire` executa **outro raycast** com `range`, largura `0.5` e predicado de alvo válido; se atingir entidade aplica `CombatTools.applyDamage` com `DamageTypes.BULLET_STREAM` e `NO_KNOCKBACK`. Envia `GunSpellTracerPacket` e partículas, que são apresentação e não projéteis físicos adicionais do método examinado.
- **Cancelamento:** `releaseWeapon` marca `isReleased`, muda estado de animação e usa `RELEASE_DURATION_TICKS=10` antes de descartar em `tickOnServer`. A tentativa de dano de cada tick não garante dano líquido efetivo nem recibo cross-provider.
- **QA:** cadence sob lag/TPS, channel cancellation, owner offline, PvP, proteção de mira, mana base do Iron's e multiplicadores externos; não debitar segunda mana, XP ou Mastery por tracer/tick.

### Integração com perks e QA

O evento original `apprenticecodex:bullet_stream` já está catalogado. Spawn, processamento por tick, efeitos atrasados, partículas, loot, custo e cleanup pertencem ao Iron's/Apprentice's. **⛔** Não há adapter RPG Skill Tree de Mastery/perks com contrato testado; Black Arcana não cria segundo cast, segundo recurso ou efeito substituto do addon. **⚠️** Dados físicos de métodos, configuração, Survival, multiplayer/claims, save/reload e ordem intermod seguem pendentes. Stage 06.05 não é promovido.

[Engenharia source-level da etapa](../PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
