# Ars Nouveau — Wall

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_wall`
- Display name: Wall
- School: Manipulation
- Default tier: 3
- Default mana cost: 500
- Compatible augments: Sensitive, AOE, Accelerate, Decelerate, Extend Time, Reduce Time (`glyph_duration_down`), Dampen
- Default Sensitive limit: 1
- Per-spell occurrence limit: exactly 1
- Default invalid combination: Linger

## Provider-native behavior

Wall converts the remaining spell into an `EntityWallSpell`: it creates a child context, cancels the original continuation, installs a new resolver, orients the wall from caster facing and stores area, speed, duration, targeting and gravity behavior. Sensitive targets blocks instead of entities; Dampen suppresses gravity. Wall is registered in `EffectReset.RESET_LIMITS`.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dragon_breath` + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Wall is a provider-owned persistent spell-execution surface, not merely a barrier graphic. Black Arcana must not create a second settlement/casting path around Ars Wall execution.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWall`).

## Dossiê de engenharia para perks — classe de efeito

- **Source pin:** [`EffectWall.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWall.java), Ars Nouveau 5.13.1.
- **Transferência de execução:** `onResolve` só age com partes de feitiço restantes; cria `SpellContext.makeChildContext`, cancela continuação do original com `setCanceled(true)`, instancia `EntityWallSpell` e injeta `resolver.getNewResolver(newContext)`.
- **Parâmetros enviados:** `setAoe((float)getAoeMultiplier())`, `setSensitive(isSensitive())`, `setAccelerates((int)getAccMultiplier())`, `extendedTime=getDurationMultiplier()`, `setShouldFall(!hasBuff(Dampen))`. Direção da wall deriva de `getFacingDirection()`, giro clockwise para face não-vertical. Spawn é provider-owned.
- **Limites:** occurrence limit `PER_SPELL_LIMIT=1`, `Sensitive=1` no default e invalid combo `EffectLinger`; `EffectReset.RESET_LIMITS` registra identidade para reset. **Perks:** número de aplicações/per-tick e raio real dependem de `EntityWallSpell`; não equiparar AOE do cast à hitbox nem criar outro cast por hit da parede.
- **Status:** ✅ source exato lido; ⚠️ entidade auxiliar, caps runtime e Survival requerem testes; API por efeito não foi validada contra RPG/Black Arcana. Sem autorização para segunda liquidação de dano/recurso/target.
