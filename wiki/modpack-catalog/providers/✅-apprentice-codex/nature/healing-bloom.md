# Healing Bloom

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:healing_bloom`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 300 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 100`
- `manaCostPerLevel = 20`
- `castTime = 50 ticks`
- placement/targeting range: **8 blocks**

Bloom max health:

`round(20 * spellPower / 100)`

Effect range:

`min(16, round(4 * spellPower / 100))` blocks.

Fruit maturation interval:

`max(600, round(1200 * (4 - spellPower / 100)))` ticks.

This preserves the exact source arithmetic: the floor is 600 ticks / 30 s.

## One-bloom-per-caster lifecycle

Server placement is resolved through `HealingBloomPlacementHelper` and rejected if invalid.

For ServerPlayers, `HealingBloomManager` enforces one managed bloom:

- if one already exists, ordinary casting is rejected;
- sneaking marks the cast as an explicit **force replace** operation;
- the force-replace flag and validated position are stored in cast data;
- successful spawn registers the new bloom through the provider manager, which owns replacement/lifecycle cleanup.

## Spawned bloom state

The entity is seeded with:

- owner;
- anchor block position;
- effect range;
- calculated maximum health;
- calculated Comfort Berry growth interval.

Provider guide semantics: the bloom softly lights its surroundings, heals nearby entities and produces Comfort Berries over time.

## Authority

The provider manager owns the single-instance invariant and replacement. Black Arcana must not create a parallel bloom registry or issue duplicate cleanup when the same provider entity is replaced/destroyed.

## Deduplication

Occupies the **one-per-caster placed healing/light/fruit-producing plant** niche.

## Confidence

`SOURCE-PINNED SPELL + PLACEMENT/MANAGER ENTRYPOINTS / BLOOM ENTITY HEAL-FRUIT CADENCE + PERSISTENCE RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:healing_bloom` → `SpellRegistry.reg("healing_bloom", HealingBloom::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.healingbloom.HealingBloom`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/healingbloom/HealingBloom.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — lote persistente 0.9.7.1

**Evidência source-located:** [`healingbloom/HealingBloom.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/healingbloom/HealingBloom.java) · [`healingbloom/HealingBloomEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/healingbloom/HealingBloomEntity.java) · [`healingbloom/HealingBloomManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/healingbloom/HealingBloomManager.java) · [`healingbloom/HealingBloomLightBlockEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/healingbloom/HealingBloomLightBlockEntity.java). Source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, alinhado à release 0.9.7.1. **Não há demonstração de equivalência dos corpos de métodos compilados no JAR da modlist**, nem GameTest provider-native neste dossiê.

### Sequência e ownership

- **Identidade e reconciliador:** `HealingBloomManager.getManagedBloomUuid` tenta resolver UUID do bloom dono no servidor, adota entidade viva carregada quando necessário e limpa referência antiga quando não consegue distinguir bloom descarregado de removido. `registerBloom` substitui entidade anterior e remove duplicados vivos do mesmo owner; `shouldKeepLoadedBloom` rejeita duplicados quando outra UUID já está gerenciada.
- **Fases de efeito:** `HealingBloomEntity.tickOnServer` ancora a entidade e desliga se unmanaged ou perdeu suporte. Tem `ACTIVATION_DELAY_TICK=40`, `HEAL_INTERVAL_TICK=80` para própria vida, `REGEN_APPLY_INTERVAL_TICK=200` com efeito `REGENERATION` por 300 ticks em vivos não-undead, `UNDEAD_DAMAGE_INTERVAL_TICK=50` com dano provider e `PULSE_INTERVAL_TICK=100` para apresentação. A duração/frutos dependem do lifecycle e stat, não de hits repetidos contabilizáveis.
- **World-affecting light:** `tryPlaceLight` procura `BlockRegistry.HEALING_BLOOM_LIGHT` e só coloca o bloco de luz se o espaço for `canBeReplaced()`. `removeLightBlock` remove apenas a identidade de luz própria quando presente. Não inferir que essas checagens equivalham a claim protection ou WorldEffectPolicy do Black Arcana.
- **Riscos:** blooms em chunks descarregados, restauração de estado UUID, drops de frutos/morte e proteção de bloco de luz exigem QA. Aura, undead damage, frutos e visual são efeitos de **uma única** spell gerida pelo addon; sem segundo scheduler, Mastery ou loot BA.

### Integração com perks e QA

O evento original `apprenticecodex:healing_bloom` já está catalogado. Spawn, processamento por tick, efeitos atrasados, partículas, loot, custo e cleanup pertencem ao Iron's/Apprentice's. **⛔** Não há adapter RPG Skill Tree de Mastery/perks com contrato testado; Black Arcana não cria segundo cast, segundo recurso ou efeito substituto do addon. **⚠️** Dados físicos de métodos, configuração, Survival, multiplayer/claims, save/reload e ordem intermod seguem pendentes. Stage 06.05 não é promovido.

[Engenharia source-level da etapa](../PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
