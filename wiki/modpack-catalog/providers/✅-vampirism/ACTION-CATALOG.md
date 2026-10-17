# Vampirism 1.10.13 — Action Catalog

Status: `COUNTED_EXACT STATIC JAR 1.10.13 / VAMPIRE 14/14 + HUNTER 3/3 + LORD 2/2 / RUNTIME QA PENDENTE`

Canonical source: `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`

## Fichas causais individuais para perks — 17/10/2026

**19/19 = 100%** das identidades provider-native com fichas técnicas individuais `SOURCE_CAUSALITY` vinculadas às classes e métodos do source **TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7**. **19/19 = 100%** das identidades compiladas já eram `COUNTED_EXACT STATIC REGISTRY` no JAR físico da versão 1.10.13; a rodada ampliou fichas de **3→19, +16 dossiês, +0 novas ações**. A engenharia documentada **não** prova equivalência completa JAR→código, instanciamento de abilities, sucesso de cast, mutabilidade per-caster nem integração de perks.

| Grupo | Identidade | Ficha individual | Propriedades de interesse para perks |
|---|---|---|---|
| Vampire | `bat` | [Bat](actions/bat.md) | hitbox 0,6×0,6, flight/movement, 3 modifiers, exhaustion, lifecycle |
| Vampire | `dark_blood_projectile` | [Dark Blood Projectile](actions/dark-blood-projectile.md) | projectile, hitbox, AOE, DamageType, cooldown e impacto |
| Vampire | `disguise_vampire` | [Disguise Vampire](actions/disguise-vampire.md) | self, specialAttributes, duração e detecção |
| Vampire | `freeze` | [Freeze](actions/freeze.md) | AABB de efeito, canFreeze, buff/tempo e resultado real |
| Vampire | `half_invulnerable` | [Half Invulnerable](actions/half-invulnerable.md) | threshold, delayed blood cost e damage settlement |
| Vampire | `regen` | [Regeneration](actions/regen.md) | Regeneration reapply, timing de heal e refinement |
| Vampire | `sunscreen` | [Sunscreen](actions/sunscreen.md) | duration multiplier, efeito protetor e cooldown |
| Vampire | `summon_bat` | [Summon Bat](actions/summon-bat.md) | fan-out 16→8, summon, cooldown e ownership |
| Vampire | `teleport` | [Teleport](actions/teleport.md) | raycast 50, DimensionTransition, target/position e cooldown |
| Vampire | `vampire_invisibility` | [Invisibility](actions/vampire-invisibility.md) | estado invisível, lifecycle e efeitos visuais |
| Vampire | `vampire_rage` | [Rage](actions/vampire-rage.md) | buffs e duração proporcional ao nível |
| Vampire | `hissing` | [Hissing](actions/hissing.md) | AABB, Mob target e AI goal reset |
| Vampire | `infect` | [Infect](actions/infect.md) | targeted entity, biteability, visibilidade e conversão |
| Vampire | `jump_boost` | [Jump Boost](actions/jump-boost.md) | specialAttributes movement e timers |
| Hunter | `awareness_hunter` | [Awareness](actions/awareness-hunter.md) | raio 25, cliente-only, closest Vampire e intensidade |
| Hunter | `disguise_hunter` | [Hunter Disguise](actions/disguise-hunter.md) | fade 20, detecção, exclusão de Awareness |
| Hunter | `potion_resistance_hunter` | [Potion Resistance](actions/potion-resistance-hunter.md) | tag filter e remoção em ticks t%3!=0 |
| Lord | `lord_speed` | [Lord Speed](actions/lord-speed.md) | AABB ±10, efeito 600 ticks, cálculo de cooldown |
| Lord | `lord_attack_speed` | [Lord Attack Speed](actions/lord-attack-speed.md) | buff de ataque, AABB ±10 e cooldown efetivo |

**Cross-provider:** o `ActionEvent.ActionActivatedEvent` público oferece veto e setters de **cooldown/duração**, não de radius/dano/target/projectile size; o event acontece **antes** de `onActivated`. A disponibilidade de uma classe ou campo para leitura não autoriza mutação de resultado por perk. Mastery só em causalidade de sucesso validada, deduplicando childs (bats/projéteis/efeitos) e mantendo recursos/atributos originais.

**Atenção Lord:** `SpeedLordAction.getCooldown` e `AttackSpeedLordAction.getCooldown` somam `super.getCooldown` (**getEffectDuration=600 ticks** com duração default 30s) com a config `laLord*Cooldown=120` **sem multiplicar esse valor por 20**, apesar do comentário de config "In seconds". Resultado aritmético do source para defaults: **720 ticks = 36 segundos** (20 TPS), e não os 150s antes atribuídos. Requer QA com config carregada no servidor e `ActionHandler` efetivo; não tratar como regressão física comprovada.

**Barras independentes:** GLOBAL **—%** (piso documental 1.856 / 1.854 estrito, denominador ainda desconhecido), VAMPIRISM **19/19 = 100%** para identidades e para fichas causais desta série. Os adapters Mastery/perks seguem **⛔ sem homologação** e os testes cliente/servidor/multiplayer/Survival **⚠️ PENDING**. **+0 raízes e nenhum Stage promovido.**

## Current binary provenance

The exact publisher [Java21 run #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643) matched the installed SHA-1 and verified all **19 distinct compiled action registrations**, their literal IDs, DeferredHolder fields, supplier constructors and IEventBus forwarding. [Evidence dossier](EXACT-BINARY-PLAYER-ACTIONS-1.10.13.md). Every timer and effect below remains a source-level behavioral description, not a completed physical Survival or provider runtime test.

## Action authority

Player actions are not Iron's-style spells. `ActionHandler` is the provider authority for:

- registration/unlock;
- permission gate;
- `canUse(...)`;
- activation context;
- cooldown/duration;
- active/cooldown timers;
- persistence and synchronization;
- deactivation/update lifecycle.

Canonical activation order on server:

1. active/cooldown check;
2. spectator check;
3. unlocked check;
4. permission check;
5. `action.canUse(player)`;
6. `ActionActivatedEvent` — cancellable and allowed to mutate cooldown/duration;
7. `action.onActivated(player, context)`;
8. only if activation succeeds: stat + active/cooldown timer settlement.

For lasting actions, `ActionUpdateEvent` is emitted during updates and `ActionDeactivatedEvent` on deactivation. Manual early deactivation can reduce cooldown according to remaining duration; timeout uses the expected full cooldown.

All cooldown/duration values below are **defaults for 1.10.13**. Server config and events may change them.

## Vampire actions — 14/14

| # | Registry id | Type | Default timer | Verified runtime semantics |
|---:|---|---|---|---|
| 1 | `vampirism:bat` | lasting | cooldown 0s (+1 operational tick); duration effectively indefinite | changes player to provider Bat state/size, grants creative-flight attribute, removes armor/toughness contribution through action modifier, sets flight speed; blocked by sun damage, garlic, water, Rage, umbrella, vehicle and dimension blacklist; adds provider exhaustion while active |
| 2 | `vampirism:dark_blood_projectile` | instant | cooldown 4s | fires provider dark-blood projectile; direct damage default 6, indirect component 50%; refinements can modify damage/speed/penetration/multishot/AOE |
| 3 | `vampirism:disguise_vampire` | lasting | cooldown 60s; duration 60s | toggles provider disguise state; identity/detection semantics are provider-owned |
| 4 | `vampirism:freeze` | instant | cooldown 60s | scans non-friendly LivingEntities around player in approximately 10×5×10 inflated range, applies provider Freeze to eligible targets; default freeze duration 3s; refinement can extend duration |
| 5 | `vampirism:half_invulnerable` | lasting | cooldown 60s; duration 30s | enables provider half-invulnerable state + Slowness; **does not pay on activation**; qualifying large hits can be blocked by paying blood later in the damage path |
| 6 | `vampirism:regen` | lasting | cooldown 60s; duration 20s | periodically applies vanilla Regeneration; refinement increases amplifier |
| 7 | `vampirism:sunscreen` | lasting | cooldown 500s; duration 40s | periodically maintains provider `SUNSCREEN`; refinement multiplies duration |
| 8 | `vampirism:summon_bat` | instant | cooldown 300s; count 16 | summons `BlindingBatEntity`; refinement changes targeting, halves count and reduces cooldown to 0.7×; normally usable while Bat is active, or independently when the refinement is equipped |
| 9 | `vampirism:teleport` | instant | cooldown 10s; max distance 50 | provider ray/path teleport; 1.10.13 uses `DimensionTransition`, dismounts passenger and resets fall/impulse state; blocked while Bat is active; refinement modifies range/cooldown |
| 10 | `vampirism:vampire_invisibility` | lasting | cooldown 25s; duration 25s | sets entity invisible and provider special-attribute invisibility state; reasserts state while active |
| 11 | `vampirism:vampire_rage` | lasting | cooldown 20s; duration `13 + 5×vampireLevel` seconds | blocked while Bat active; maintains Speed III, Strength I and Haste I |
| 12 | `vampirism:hissing` | instant | cooldown 60s | scream; mobs within radius 10 whose target is the player stop running target goals and clear target |
| 13 | `vampirism:infect` | instant | cooldown 10 ticks | attempts provider infection through `IBiteableEntity.tryInfect`; unavailable in Peaceful; uses visibility/biteability gates; successful use increments provider infected-creatures stat |
| 14 | `vampirism:jump_boost` | lasting | cooldown 0s (+1 operational tick); duration effectively indefinite | sets provider jump-boost special attribute to `vsJumpBoost + 1`; default `vsJumpBoost=1`; provider owns movement behavior |

## Blood settlement nuance

### Bat

Bat calls `IVampirePlayer.addExhaustion(default 0.005)` while active. It does **not** call direct `useBlood` in the action class. Blood may subsequently be reduced by `BloodStats` when exhaustion crosses the provider threshold.

Integration consequence: a system observing Bat activation must not immediately charge blood.

### Half Invulnerable

Default threshold is `0.4 × maxHealth`. When a qualifying hit is intercepted, the player damage path attempts `useBlood(4, false)` by default. On successful payment the hit is ignored; if payment fails the action is deactivated.

Integration consequence: the economic transaction is caused by the **blocked hit**, not by the original action activation. Debiting blood at activation would be wrong and can double-charge.

### Other audited Vampire actions

No direct blood debit was found in the 1.10.13 action implementation for Bat, Dark Blood Projectile, Freeze, Regeneration, Sunscreen, Summon Bats, Teleport, Invisibility, Rage, Hissing, Infect or Jump Boost. The absence of a direct debit is recorded as source behavior; Black Arcana must not infer a thematic blood cost.

## Hunter actions — 3/3

| # | Registry id | Type | Default timer | Verified runtime semantics |
|---:|---|---|---|---|
| 1 | `vampirism:awareness_hunter` | lasting | cooldown 1 tick; duration effectively indefinite | scans client-side for nearest actual Vampire-faction LivingEntity within default radius 25 and stores proximity intensity; cannot run together with Hunter Disguise |
| 2 | `vampirism:disguise_hunter` | lasting | cooldown 0; duration indefinite | activates provider Hunter disguise state/fade; cannot run together with Awareness; detection behavior is provider-owned |
| 3 | `vampirism:potion_resistance_hunter` | lasting | cooldown 1200 ticks; duration 400 ticks | removes only effects tagged `vampirism:hunter_potion_resistance`; source condition executes removal on update ticks where `tickCount % 3 != 0` |

The unusual Potion Resistance modulo condition is documented exactly as source behavior. It is not silently “corrected” to every third tick.

## Shared Lord actions — 2/2

Registered ids:

- `vampirism:lord_speed`
- `vampirism:lord_attack_speed`

Both extend `LordRangeEffectAction` and are faction-neutral action definitions usable through the Lord skill system.

Activation behavior:

1. read caster Lord level;
2. find LivingEntities of the caster's faction in an AABB inflated by 10 blocks;
3. skip player targets whose Lord level is greater than or equal to the caster's;
4. apply provider Lord effect to remaining allies;
5. fail activation if no eligible same-faction entity is found.

Defaults:

| Action | Effect | Effect duration | Additional cooldown | Effective default cooldown |
|---|---|---:|---:|---:|
| Lord Speed | `LORD_SPEED` | 600 ticks (30s) | 120 **ticks somados**, embora config comente "seconds" | **720 ticks (36s)** no source |
| Lord Attack Speed | `LORD_ATTACK_SPEED` | 600 ticks (30s) | 120 **ticks somados**, embora config comente "seconds" | **720 ticks (36s)** no source |

Both subclasses force amplifier 0. The base class normally derives amplifier from Lord level, but these two installed actions override that behavior.

## Canonical events for integration

### `ActionEvent.ActionActivatedEvent`

Use for:

- validating/augmenting a provider-approved attempt before effect execution;
- explicit cooldown/duration modifiers;
- canceling activation under a designed cross-mod gate.

Do not treat event emission alone as proof that the action effect succeeded, because it fires before `onActivated(...)`. For completion credit that requires actual success, correlate with provider state/stat/result.

### `ActionEvent.ActionUpdateEvent`

Can:

- request deactivation;
- skip provider `onUpdate` for that tick.

This is a high-authority hook. Black Arcana must not use it casually to suppress provider behavior.

### `ActionEvent.ActionDeactivatedEvent`

Provides remaining duration and mutable cooldown. It is the canonical lifecycle hook for a lasting action ending.

## Deduplication rules

- One provider action toggle receives one causal identity.
- Effects, spawned bats, teleport movement, potion effects and state changes downstream from that action are consequences, not additional casts.
- Quest/perk logic should prefer the action event and correlate downstream effects rather than awarding separately for both.
- Do not reapply action potion effects or movement state from a generic `LivingEntity` effect observer.
- Do not overwrite action timers directly unless a documented integration intentionally modifies cooldown/duration through the provider event/API.

## Runtime QA queue

- ActionActivated event -> failed `onActivated` correlation.
- manual deactivation cooldown reduction.
- timeout cooldown behavior.
- ActionWheel persistence fixed in 1.10.13.
- Bat ↔ Epic Fight/movement/stamina/flight compatibility.
- Teleport ↔ portals/dimensions/movement mods.
- Half Invulnerable exact damage cancellation and blood debit timing.
- Hunter Potion Resistance modulo behavior in dedicated server.
- Lord range action eligibility and same/higher Lord exclusion.
