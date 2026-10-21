# Auto Turret

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:auto_turret`
- **School:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 40`
- `baseManaCost = 80`
- `manaCostPerLevel = 20`
- `castTime = 40 ticks / 2 s`
- placement targeting range: **8 blocks**

Damage per turret shot:

`4 * spellPower / 100 * AUTO_TURRET damage multiplier`

Initial projectile/ammo count:

`8 + round(8 * spellPower / 100)`

Turret maximum health:

`20 + (spellLevel - 1) * 10`

Owner restock mana cost:

`spell mana cost / 4`

## Server-authoritative placement

The spell captures a client placement preview but admission is re-resolved on the server. It rejects invalid placement and positions already occupied by another Auto Turret in the placement box. The admitted block position is persisted in cast data and restored/revalidated at execution.

## Autonomous entity lifecycle

The provider spawns an owner-bound `AutoTurretEntity` with its anchor, damage, initial ammo, restock cost and health frozen from the cast.

Exact autonomous combat timing includes:

- target search cadence: every **10 ticks** when a new target is needed;
- charge time before a shot: **15 ticks**;
- post-shot cooldown: **8 ticks**;
- first auto-lock shot delay: **10 ticks**;
- lock retention before target reconsideration: **60 ticks**;
- lost-line-of-sight tolerance: **20 ticks**;
- empty-ammo discard delay: **100 ticks**.

The turret searches within its FOLLOW_RANGE (base 24), validates combat targets and line of sight, applies provider-owned hit damage, and spends one internal bullet after firing.

## Restocking and mana authority

Only the owner can restock by interacting with the turret. If ammo is below the initial capacity, the provider directly reads the owner's canonical Iron's `MagicData` mana, requires enough for `restockManaCost`, subtracts that amount once, synchronizes mana, and restores ammo to the initial count.

The turret therefore has **ammunition state but not a second magical mana pool**. Restock cost is paid from Iron's mana.

## Authority / deduplication

The original summon is one cast. Autonomous turret shots are provider-owned downstream activity; they must not become repeated Black Arcana casts or per-shot Mastery farming.

Black Arcana must not duplicate the turret target loop, ammo ledger, restock payment or shot damage. RPG integration requires a deliberately bounded causal contract rather than observing every autonomous hit.

## Confidence

`SOURCE-PINNED PLACEMENT + STATS + AUTONOMOUS TIMING + OWNER RESTOCK / FULL MODPACK TARGETING AND PERSISTENCE QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:auto_turret` → `SpellRegistry.reg("auto_turret", AutoTurret::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.autoturret.AutoTurret`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/autoturret/AutoTurret.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — entidades 0.9.7.1

**Source pin declarado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. **Classes lidas:** [`autoturret/AutoTurret.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/autoturret/AutoTurret.java) · [`autoturret/AutoTurretEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/autoturret/AutoTurretEntity.java) · [`autoturret/AutoTurretPlacementHelper.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/autoturret/AutoTurretPlacementHelper.java). O arquivo físico da modlist é 0.9.7.1; **igualdade de corpo dos métodos no bytecode compilado não foi atestada nesta etapa**. Este conteúdo é engenharia documental factual, não código incorporado.

### Cadeia de execução e recibo provider-owned

- **Entrada, alvo e materialização:** `AutoTurret.checkPreCastConditions` resolve colocação no servidor com `AutoTurretPlacementHelper.resolveServer` e rejeita sobreposição `hasNearbyTurret` consultando `AutoTurretEntity` na `placementBox().inflate(0.1)`. A posição aceita é guardada em `AutoTurretCastData` e revalidada em `onCast` antes de `serverLevel.addFreshEntity`. A entidade recebe owner, ancoragem, dano, munição inicial, custo de restock e vida via setters locais do provider.
- **Tick e combate:** `AutoTurretEntity.tickOnServer` descarta entidade sem owner vivo na mesma dimensão. Com suporte abaixo, mantém posição ancorada; sem suporte, volta a seguir física da entidade. Atualiza alvo periodicamente (a cada 10 ticks no ramo sem alvo/saturação), testa linha de visão, usa `CHARGE_TICK=15` e `COOLDOWN_TICK=8`, além de timers de lock e de descarte. `fire` aplica `CombatTools.applyDamage` com `DamageTypes.AUTO_TURRET`, owner e escola; só redireciona a agressividade de `Mob` quando `damaged==true`.
- **Restock é outro tipo de operação:** `mobInteract` requer `MAIN_HAND` e o UUID do dono, recusa quando já cheio ou sem mana e debita `restockManaCost` de `MagicData` ao reabastecer. Depois sincroniza `SyncManaPacket`, restaura a munição e reinicia o prazo de descarte. Não é uma nova execução do feitiço `auto_turret`.
- **Riscos para perks:** o disparo periódico, reposição, dano e spawn não constituem casts independentes. Testar targeting PvP, owner offline, múltiplas torres, proteção de world placement, restock concorrente e estados do JAR físico. Ação e gasto continuam sob Iron's/Apprentice's.

### Atribuição técnica e condições para perks

- **Identidade semântica:** exatamente uma raiz `apprenticecodex:auto_turret`; eventos de entidades, timers, limpeza, efeitos derivados, recursos e cooldown são de Iron's/Apprentice's, não casts BA adicionais.
- **Observabilidade:** sem boundary/receipt interoperável comprovado, ⛔ Mastery, perks ou efeitos de RPG Skill Tree que suponham cast confirmado, hit, spawn ou settlement. Não inventar API de bridge.
- **QA pendente ⚠️:** configuração efetiva, JAR físico dos métodos, dedicated/full-modpack, Survival, cross-dimension, persistência, claim/PvP e compatibilidade de inventário. Não promover Stage 06.05.
- **Clean-room:** apenas comportamento observado no source é descrito. Black Arcana conserva seu próprio casting, Corruption, Strain e WorldEffectPolicy.

[Matriz de lifecycle](../PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
