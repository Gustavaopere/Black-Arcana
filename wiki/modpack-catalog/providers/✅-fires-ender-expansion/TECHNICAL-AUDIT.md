# Fire's Ender Expansion 2.4.1 — technical audit

## Provenance

Autoridade instalada: `firesenderexpansion-2.4.1.jar` na modlist atual.

Autoridade de source usada para documentação:

`FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`

Esse commit declara Minecraft `1.21.1`, `mod_version=2.4.1` e dependência de Iron's `1.21.1-3.15.6`. O pack roda Iron's `1.21.1-3.16.3`; portanto o catálogo está source-pinned, mas a compatibilidade binária/semântica com o provider-base instalado continua sendo um gate de runtime QA.

## Registry

`SpellRegistries` registra exatamente 11 `AbstractSpell` ativos no pin: Arcane Slice, Aspect of the Shulker, Hollow Crystal, Dimensional Adaptation, Obsidian Rod, Infinite Void, Dragon's Fury, Gate of Ender, Displacement Cage, Binary Stars e Scintillating Stride. Todos usam `SchoolRegistry.ENDER_RESOURCE`.

## Authority e pipelines

- Spell lifecycle, mana/cooldown/cast/recast: Iron's + classes do provider.
- Teleport: `Utils.handleSpellTeleport` / `SpellTeleportEvent` onde o provider os chama.
- Domain: `AbstractDomainEntity` de Ace's Spell Utils + `InfiniteVoid`/`InfiniteVoidEffect` do provider.
- Friendly-fire/eligibility: usar o resultado do provider/Iron's; não introduzir uma segunda filtragem que altere causalidade sem contrato explícito.
- Effects `Anchored`, `Nova Burn`, `Eclipsed`, `Striding`, `Infinite Void`, `Ascended Caster` e `Voidtorn` são provider-native.
- Projectiles/entities (`HollowCrystal`, `ObsidianRod`, `GatePortal`, unstable weapons, Binary Stars) são autoridade de hit/lifecycle do provider.

## Config defaults relevantes

- `allow_sword_hail=false`
- `hollow_crystal_break_projectiles=true`
- `shulker_aspect_internal_cooldown=20` ticks
- `fragments_obtainable=true`
- `crystal_heart_obtainable=true`

## Dimensional Adaptation data

`data/firesenderexpansion/adaptable_dimensions.json` no pin:

- `minecraft:overworld` → Night Vision, 400 ticks base, amplifier 0;
- `minecraft:the_nether` → Fire Resistance, 400 ticks base, amplifier 0;
- `minecraft:the_end` → Slow Falling, 200 ticks base, amplifier 0;
- `irons_spellbooks:pocket_dimension` → Saturation, 2 ticks base, amplifier 0.

A duração final é `baseDuration × (spellPower / 10)`.

## QA findings

### FEE-QA-001 — Binary Stars slam inativo

`BinaryStarEntity` mantém a lógica de teleportar acima do alvo e executar slam/AoE inteiramente comentada. O contract 2.4.1 ativo é homing + hit + debuff; não documentar o slam como funcional até evidência de outro artefato/runtime.

### FEE-QA-002 — Nova Burn amplifier zero

`NovaBurnEffect.onSpellCastEvent` usa:

`damage = 5 × beneficialEffectCount × NOVA_BURN amplifier`.

A Nova Star aplica `new MobEffectInstance(NOVA_BURN_EFFECT, duration)` sem amplifier explícito, portanto amplifier 0. Pelo caminho estático auditado, o dano calculado é 0. Runtime test deve confirmar; não corrigir silenciosamente nesta frente documental.

### FEE-QA-003 — Stride blast eligibility

O loop de explosão de `ScintillatingStrideSpell.onRecastFinished` chama `DamageSources.applyDamage` para todos os `LivingEntity` na área sem filtro provider-side explícito de caster/friendly-fire. O comportamento efetivo deve ser validado no runtime do Iron's 3.16.3.

### FEE-QA-004 — source-base mismatch

O source pin compila contra Iron's 3.15.6; pack atual usa 3.16.3. Validar todos os hooks usados: recasts, `DamageSources`, `Utils.handleSpellTeleport`, `SpellTeleportEvent`, `SpellPreCastEvent`, `TargetEntityCastData`, `AbstractMagicProjectile` e school attributes.

### FEE-QA-005 — Infinite Void return fallback

Se `InfiniteVoidEffect` não encontrar uma origem válida ou registrar a própria void dimension como origem, o fallback move a entidade para Overworld `(0,100,0)`. Testar remoção normal, morte, logout, chunk unload, anti-magic e encerramento de domain clash.

## Fail-closed

Nenhuma integração deve reproduzir, substituir ou normalizar esses mechanics enquanto o runtime não os confirmar. Divergência source/runtime deve ser registrada e devolvida à auditoria; não inventar bônus genérico.

## Status

**CATÁLOGO DOCUMENTAL 11/11 COMPLETO — RUNTIME QA PENDENTE.**