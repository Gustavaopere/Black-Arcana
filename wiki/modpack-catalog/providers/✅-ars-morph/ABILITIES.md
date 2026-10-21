# Ars Morph 2.0.0 — Identity2 ability adapters

## Regra do host: cooldown + use_duration — 17/10/2026

Inspeção de `xGabou/Identity2` em commits anteriores e posteriores à publicação 2.2.4 confirma que `ModPackets` define contador primário `max(0,cooldown+useduration)`, `EntityMixin.baseTick` reduz em **1 por tick**, e o servidor fixa o valor **antes** de executar o callback. Exemplo: Wixie JSON `200/20` corresponde a **220 ticks** de contador primário no source, não 200; Wilden Stalker `800/100` corresponde a **900 ticks**. Veja [dossiê cross-version](IDENTITY2-ABILITY-COOLDOWN-SOURCE-BRACKET-2.2.4.md) e [matriz com sete totais](ABILITY-PERK-CAUSAL-MATRIX-2.0.0.md).

Isso resolve a **unidade operacional do source** (ticks), não certifica o binário instalado da versão 2.2.4, nem substitui duração dos efeitos de cada spell Ars. O callback Wixie pode lançar exceção depois de o cooldown ser fixado; não há refund explícito no handler observado. **⛔ Nenhum adapter de modificação per-player**.

## Ampliação individual 17/10/2026 — sete habilidades

Sete fichas `abilities/{weald-walker,wilden-hunter,wilden-stalker,starbuncle,whirlisprig,wixie,firenando}.md` foram criadas com observações por classe e links ao Java 2.0.0 e **11 atribuições JSON**. [Matriz causal das habilidades](ABILITY-PERK-CAUSAL-MATRIX-2.0.0.md). Os 7 adaptadores Java e 11 assignments **não representam onze spells novas**; ações derivadas de Ars continuam provider-native. `cooldown` e `use_duration` são valores JSON sem unidade física confirmada.

O ramo agachado de Wixie pode indexar posições 10/11 da tabela benéfica que tem dez entradas; wrapper captura Throwable, portanto somente QA no pack pode determinar impacto. Whirlisprig faz mutação world Grow e passivo Jump Boost, Firenando é condicional, Weald Walker reutiliza o mesmo `predef` para cinco variantes. **Source-only, sem API de perks ou Mastery homologada**.

Status: `7 JAVA ADAPTERS + 11 DATA ASSIGNMENTS CATALOGED / RUNTIME QA OPEN`

## Authority

Ars Morph implements Identity2 `BuiltinIdentityAbility` adapters through `MorphBoundAbility<T>`. The base adapter:

- accepts only a `Player` host;
- asks `IdentityApi.getCurrentMorph(player)` for the current form;
- requires the current form to match the expected Ars entity class;
- delegates active/passive behavior to the typed subclass;
- catches/logs thrown errors rather than making Black Arcana a fallback authority.

Identity2 owns ability dispatch and the data-driven cooldown/use-duration contract. Ars/Ars Elemental own the spell/entity behavior reused by the adapter.

## Java ability adapters — 7

### Weald Walker

Registration id: `ars_nouveau:weald_walker`.

The adapter builds an `EntitySpellResolver` from the current Weald Walker's stored `spell` and `color`, with the player as caster. After a non-canceled Ars post event it fires an `EntityProjectileSpell` at speed 1.0 / inaccuracy 0.8.

Committed assignments using this predef:

| Identity data path | Cooldown | Use duration |
|---|---:|---:|
| Blazing Weald Walker | 100 | 20 |
| Cascading Weald Walker | 100 | 20 |
| Flourishing Weald Walker | 100 | 20 |
| Vexing Weald Walker | 100 | 20 |
| optional Flashing Weald Walker (Ars Elemental) | 100 | 20 |

### Wilden Hunter

Registration uses Ars `WILDEN_HUNTER` EntityType.

Active behavior:

- howl sound;
- Ars spell `Summon Wolves + Extend Time`;
- uses player as the Ars caster;
- resolves on the player when the Ars event is not canceled;
- then removes Ars `Summoning Sickness` from the player.

Identity assignment: cooldown 800, use duration 20.

The removal of Summoning Sickness is part of the provider ability path and must not be duplicated as a separate RPG perk consequence.

### Wilden Stalker

Registration uses Ars `WILDEN_STALKER` EntityType.

Active behavior:

- bat takeoff sound;
- Ars self spell with `Launch ×2`, `Glide`, `Duration Down`;
- executes only after a non-canceled resolver event.

Identity assignment: cooldown 800, use duration 100.

A separate provider morph-tick handler mirrors a server player's derived flying state into the current `WildenStalker` representation and calls `IdentityApi.syncBoolean(serverPlayer, "isFlying", flying)`.

### Starbuncle

Registration uses Ars Starbuncle EntityType.

Active behavior adds vanilla `MOVEMENT_SPEED` for 3000 ticks at amplifier 1, hidden particles/icon flags.

Identity assignment: cooldown 100, use duration 20.

### Whirlisprig

Registration uses Ars Whirlisprig EntityType.

Active behavior resolves Ars `Grow + AOE ×3` on the block below the player, using green spell color. Passive behavior on server adds vanilla Jump Boost for 40 ticks at amplifier 2.

Identity assignment: cooldown 400, use duration 20.

The form is also added to Identity2 `slow_falling` by data.

### Wixie

Registration uses Ars Wixie EntityType.

Active behavior throws a splash potion with one random custom effect instance, 200 ticks, amplifier 1:

- crouching selects the good-effect table;
- not crouching selects the bad-effect table.

Good table contains 10 effects; bad table contains 12 effects.

`SOURCE-RISK`: the exact source always generates the random index using `badEffectTable.size()` even after choosing the good table. In the crouching branch, indices 10 or 11 would be out of bounds for the 10-entry selected list. Phase 2X records this as a concrete source defect hypothesis requiring installed reproduction; it does not claim a pack crash without runtime evidence.

Identity assignment: cooldown 200, use duration 20.

### Firenando — optional Ars Elemental

Registered only when Ars Elemental is loaded.

The adapter uses the current Firenando's stored spell and variant-sensitive particle color, builds an Ars Elemental homing projectile, then adds an ignore predicate that excludes every target that is not an `Enemy`.

Identity assignment: cooldown 120, use duration 40.

## Causal deduplication

An Identity2 ability activation may internally create an Ars resolver/projectile/effect. These descendants remain part of the provider ability transaction.

Black Arcana and RPG Skill Tree must not:

- count the Identity ability and its internal Ars resolver as two player casts;
- charge a second Ars/BA resource for the internal provider execution;
- replay projectile/effect output;
- reapply Summoning Sickness removal;
- duplicate cooldown ownership;
- treat passive callbacks as independent player actions;
- replace Identity2 dispatch with a parallel keybind/ability registry merely to expose the same behavior.

## Runtime QA

Validate each assignment under Identity2 2.2.4, including cooldown, use duration, cancellation, server/client execution, death/respawn, logout/reconnect and dimension transfer. Reproduce/refute the Wixie crouching index-risk explicitly.
