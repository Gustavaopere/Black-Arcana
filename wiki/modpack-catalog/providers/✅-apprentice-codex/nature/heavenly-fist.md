# Heavenly Fist

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:heavenly_fist`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 80`
- `manaCostPerLevel = 20`
- `castTime = 0`
- target range: **32 blocks**

Damage:

`(4 + 6 * spellPower / 100) * HEAVENLY_FIST damage multiplier`

Impact radius:

`2.5 + 2.0 * spellPower / 100`

Optional pressing capacity before flooring:

`8 * spellPower / 100`, then optionally modified by Craftsman's Delight process-speed logic.

## Target resolution

The server resolves a single locked center along the caster's view line. Resolution precedence is:

1. valid combat entity before the first blocking block;
2. processable dropped item when Create pressing support is active;
3. adjacent center of the hit block face;
4. otherwise the cast is denied.

The client does not author the final AoE center.

## Delayed provider-owned impact

A short-lived `HeavenlyFistFistEntity` is spawned at the locked center. Its exact lifecycle is bounded:

- attack animation begins at tick 4;
- impact settles once at tick **25**;
- entity discards at tick **30**;
- entity is non-persistent, non-pickable and cannot be damaged by normal gameplay.

At the single impact, the provider:

- resolves unique combat targets inside the configured radius;
- applies Heavenly Fist damage without knockback;
- applies `GRAVITY_BOUND` for **200 ticks / 10 s** to successfully damaged living targets;
- optionally processes dropped items through the provider's Create pressing processor;
- optionally runs the provider crystal-harvest processor for a valid real player owner;
- emits bounded visual tremor particles, with a visual block limit of **18**.

## Causality / ownership

The delayed fist entity is downstream execution of one already-admitted cast. Damage targets, pressed item stacks, harvested crystals and visual tremor blocks are not independent magical casts.

Create recipe semantics and Craftsman's Delight modifiers remain provider-owned. Black Arcana must not re-run pressing/compacting, reapply damage, or treat the particle tremor as terrain destruction.

For any future Mastery/progression bridge, the safe causal unit is the original Heavenly Fist cast unless a provider-native discrete processing event is explicitly contracted.

## Confidence

`SOURCE-PINNED TARGETING + COEFFICIENTS + IMPACT ENTITY LIFECYCLE / OPTIONAL CREATE PROCESSING + CRYSTAL HARVEST FULL PACK QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:heavenly_fist` → `SpellRegistry.reg("heavenly_fist", HeavenlyFist::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.heavenlyfist.HeavenlyFist`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/heavenlyfist/HeavenlyFist.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — lote persistente 0.9.7.1

**Evidência source-located:** [`heavenlyfist/HeavenlyFist.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/heavenlyfist/HeavenlyFist.java) · [`heavenlyfist/HeavenlyFistFistEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/heavenlyfist/HeavenlyFistFistEntity.java) · [`heavenlyfist/HeavenlyFistPressingProcessor.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/heavenlyfist/HeavenlyFistPressingProcessor.java) · [`heavenlyfist/HeavenlyFistCrystalHarvestProcessor.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/heavenlyfist/HeavenlyFistCrystalHarvestProcessor.java). Source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, alinhado à release 0.9.7.1. **Não há demonstração de equivalência dos corpos de métodos compilados no JAR da modlist**, nem GameTest provider-native neste dossiê.

### Sequência e ownership

- **Impacto único:** `HeavenlyFistFistEntity.tickServer` marca `impacted=true` e chama `impact` quando chega `IMPACT_TICK`, impedindo repetição por ticks seguintes no objeto; descarta ao alcançar `DISCARD_TICK`. `impact` busca alvos únicos via `CombatTools.resolveUniqueCombatTargets` na `AABB` do centro congelado e raio, aplica `DamageTypes.HEAVENLY_FIST` e, somente quando `applyDamage` retorna verdadeiro, `GRAVITY_BOUND` por `20*10` ticks a living target.
- **Subações de material:** o mesmo impacto chama `HeavenlyFistPressingProcessor.processItems` para itens no chão e `HeavenlyFistCrystalHarvestProcessor.harvest` quando há `ServerPlayer` real disponível. Este resolvedor evita confiar em `FakePlayer` para permissão/equipamento, procurando UUID do player online para harvesting. Create Pressing é integração condicional: o processor tem tratamento separado de recipe e reflection; não assumir Create habilitado.
- **Efeito de tremor:** `spawnTremorBlocks` amostra **no máximo 18** posições distintas dentro de `TREMOR_RADIUS=2.35` para pacotes/partículas; no corpo de `spawnTremorBlock` lido, a operação chama `sendTremorParticle`, não posicionamento persistente de blocos. Não classificar esses visuais como world mutation confirmada.
- **Riscos:** claims para harvest real, outputs e duplicação de drops com Create, crash entre efeitos, limite de itens e target selection exigem QA. Dano, pressing e colheita são consequências da mesma `heavenly_fist`, sem recompensa independente por subação.

### Integração com perks e QA

O evento original `apprenticecodex:heavenly_fist` já está catalogado. Spawn, processamento por tick, efeitos atrasados, partículas, loot, custo e cleanup pertencem ao Iron's/Apprentice's. **⛔** Não há adapter RPG Skill Tree de Mastery/perks com contrato testado; Black Arcana não cria segundo cast, segundo recurso ou efeito substituto do addon. **⚠️** Dados físicos de métodos, configuração, Survival, multiplayer/claims, save/reload e ordem intermod seguem pendentes. Stage 06.05 não é promovido.

[Engenharia source-level da etapa](../PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
