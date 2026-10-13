# Ars Elemental 0.7.10.1 — 39 glyphs de produção + 8 rituais: prova binária exata

**Status:** ✅ `COUNTED_EXACT` para **47/47 identidades de registry estático** (39 spell parts + 8 rituals), **+0 objetos semânticos** além dos 47 já contabilizados. Campanha física **15/39 exatos / 24/39 pendentes**. Mínimos globais **1857** e escopo usuário **1855**, inalterados. `MethodCarianPhalanx` está condicionado a **`!FMLLoader.isProduction()`** e **NÃO** é a 40ª spell part de produção.

## Proveniência e reprodução

- Publisher: [CurseForge file 8399862](https://www.curseforge.com/minecraft/mc-mods/ars-elemental/files/8399862), `ars_elemental-1.21.1-0.7.10.1.jar`, **2260550 bytes**, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3` idêntico à modlist física `neoforge-rpg-skilltree`, 1.21.1 NeoForge, mod ID `ars_elemental`.
- [Auditoria estática Java 21 conclusiva #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682), após [discovery #38402990653](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38402990653) e [verificação de JAR #38402811220](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38402811220). Todos **SUCCESS**.
- `ArsElemental → ArsNouveauRegistry.init → registerGlyphs/registerRituals`. O método de glifos possui **40** chamadas ao wrapper `register(AbstractSpellPart)`, 39 diretas no caminho de produção e a 40ª sob `!isProduction()`. O wrapper chama uma vez a API Ars `GlyphRegistry.registerSpell`. Nenhum outro branch no método. O ritual registrar chama `RitualRegistry.registerRitual` indiretamente em **8** entradas incondicionais. A ordem de campos/classes é conferida pelo `javap` no artefato SHA-verificado.
- `ArsElemental.prefix` usa namespace literal `ars_elemental` e `ResourceLocation.fromNamespaceAndPath`; classes abstratas compiladas demonstram a composição `glyph_` e `_filter`; as 39 classes e sufixos são verificadas individualmente. Os 8 rituais expõem sufixos literais e invocam `ArsElemental.prefix`. A versão original source pin continua **não certificada como build byte-a-byte equivalente**, embora o JAR físico/publicador coincida.
- Testes automatizados de integridade, método e identidade: `EXACT_STATIC_REGISTRY_AUDIT=PASS`, `PRODUCTION_GLYPHS=39`, `DEV_ONLY_NONPRODUCTION_GLYPH=1`, `PHYSICAL_RITUALS=8`, `EXACT_MAGIC_REGISTRY_OBJECTS=47`, `NEW_SEMANTIC_ROOTS=0`.

## Glifos de produção 39/39 — identidade exata

| # | ResourceLocation | Classe/campo de registro | Família |
|---:|---|---|---|
| 1 | `ars_elemental:glyph_watery_grave` | `EffectWaterGrave.INSTANCE` | Effect |
| 2 | `ars_elemental:glyph_bubble_shield` | `EffectBubbleShield.INSTANCE` | Effect |
| 3 | `ars_elemental:glyph_conjure_terrain` | `EffectConjureTerrain.INSTANCE` | Effect |
| 4 | `ars_elemental:glyph_charm` | `EffectCharm.INSTANCE` | Effect |
| 5 | `ars_elemental:glyph_phantom_grasp` | `EffectPhantom.INSTANCE` | Effect |
| 6 | `ars_elemental:glyph_life_link` | `EffectLifeLink.INSTANCE` | Effect |
| 7 | `ars_elemental:glyph_poison_spores` | `EffectSpores.INSTANCE` | Effect |
| 8 | `ars_elemental:glyph_envenom` | `EffectEnvenom.INSTANCE` | Effect |
| 9 | `ars_elemental:glyph_spike` | `EffectSpike.INSTANCE` | Effect |
| 10 | `ars_elemental:glyph_discharge` | `EffectDischarge.INSTANCE` | Effect |
| 11 | `ars_elemental:glyph_spark` | `EffectSpark.INSTANCE` | Effect |
| 12 | `ars_elemental:glyph_conflagrate` | `EffectConflagrate.INSTANCE` | Effect |
| 13 | `ars_elemental:glyph_cauterize` | `EffectCauterize.INSTANCE` | Effect |
| 14 | `ars_elemental:glyph_rage` | `EffectRage.INSTANCE` | Effect |
| 15 | `ars_elemental:glyph_water_jet` | `EffectWaterJet.INSTANCE` | Effect |
| 16 | `ars_elemental:glyph_geyser` | `EffectGeyser.INSTANCE` | Effect |
| 17 | `ars_elemental:glyph_mist` | `EffectMist.INSTANCE` | Effect |
| 18 | `ars_elemental:glyph_slip_feet` | `EffectSlipper.INSTANCE` | Effect |
| 19 | `ars_elemental:glyph_cavitate` | `EffectCavitate.INSTANCE` | Effect |
| 20 | `ars_elemental:glyph_oxidize` | `EffectOxidize.INSTANCE` | Effect |
| 21 | `ars_elemental:glyph_summon_bee` | `EffectSummonBee.INSTANCE` | Effect |
| 22 | `ars_elemental:glyph_summon_slime` | `EffectSummonSlime.INSTANCE` | Effect |
| 23 | `ars_elemental:glyph_homing_projectile` | `MethodHomingProjectile.INSTANCE` | Cast method |
| 24 | `ars_elemental:glyph_arc_projectile` | `MethodArcProjectile.INSTANCE` | Cast method |
| 25 | `ars_elemental:glyph_propagator_homing` | `PropagatorHoming.INSTANCE` | Propagator |
| 26 | `ars_elemental:glyph_propagator_arc` | `PropagatorArc.INSTANCE` | Propagator |
| 27 | `ars_elemental:glyph_aquatic_filter` | `AquaticFilter.INSTANCE` | Filter |
| 28 | `ars_elemental:glyph_not_aquatic_filter` | `AquaticFilter.NOT_INSTANCE` | Filter |
| 29 | `ars_elemental:glyph_fiery_filter` | `FieryFilter.INSTANCE` | Filter |
| 30 | `ars_elemental:glyph_not_fiery_filter` | `FieryFilter.NOT_INSTANCE` | Filter |
| 31 | `ars_elemental:glyph_aerial_filter` | `AerialFilter.INSTANCE` | Filter |
| 32 | `ars_elemental:glyph_not_aerial_filter` | `AerialFilter.NOT_INSTANCE` | Filter |
| 33 | `ars_elemental:glyph_insect_filter` | `InsectFilter.INSTANCE` | Filter |
| 34 | `ars_elemental:glyph_not_insect_filter` | `InsectFilter.NOT_INSTANCE` | Filter |
| 35 | `ars_elemental:glyph_undead_filter` | `UndeadFilter.INSTANCE` | Filter |
| 36 | `ars_elemental:glyph_not_undead_filter` | `UndeadFilter.NOT_INSTANCE` | Filter |
| 37 | `ars_elemental:glyph_summon_filter` | `SummonFilter.INSTANCE` | Filter |
| 38 | `ars_elemental:glyph_not_summon_filter` | `SummonFilter.NOT_INSTANCE` | Filter |
| 39 | `ars_elemental:glyph_nullify_defense` | `EffectNullify.INSTANCE` | Effect |

### Glifo compilado, mas fora da produção

`MethodCarianPhalanx.INSTANCE` existe no artefato e corresponde a `ars_elemental:glyph_carian_phalanx`, mas o único caminho de registro depende de `!FMLLoader.isProduction()`. **Excluído do catálogo de 39 glifos de produção e da contagem estrita.** A presença da classe, da EntityType ou de partículas não prova acesso pelo jogador.

## Rituais 8/8 — identidade exata

| # | ResourceLocation | Classe no binário |
|---:|---|---|
| 1 | `ars_elemental:ritual_squirrels` | `alexthw.ars_elemental.common.rituals.SquirrelRitual` |
| 2 | `ars_elemental:ritual_tesla_coil` | `alexthw.ars_elemental.common.rituals.TeslaRitual` |
| 3 | `ars_elemental:ritual_detection` | `alexthw.ars_elemental.common.rituals.DetectionRitual` |
| 4 | `ars_elemental:ritual_repulsion` | `alexthw.ars_elemental.common.rituals.RepulsionRitual` |
| 5 | `ars_elemental:ritual_attraction` | `alexthw.ars_elemental.common.rituals.AttractionRitual` |
| 6 | `ars_elemental:ritual_pollination` | `alexthw.ars_elemental.common.rituals.PollinationRitual` |
| 7 | `ars_elemental:ritual_archwood_forest` | `alexthw.ars_elemental.common.rituals.forest.ArchwoodForestRitual` |
| 8 | `ars_elemental:ritual_archwood_forestation` | `alexthw.ars_elemental.common.rituals.forest.ArchwoodForestationRitual` |

## Diferenciações necessárias

- `Nullify Defense`: `ars_elemental:glyph_nullify_defense` está **registrado no caminho de produção**. A receita de aprendizado é **default-disabled no source**, e a configuração efetiva do pack não foi extraída/testada; registro não é garantia de aquisição.
- `Sliding` é o display de `ars_elemental:glyph_slip_feet`, `Create Geyser` é `glyph_geyser`, `Mist Cloud` é `glyph_mist`; nunca derivar IDs do nome editorial.
- Filtros usam IDs de registro distintos para cada modo normal/invertido: 12 no total.
- Rituais Archwood mantêm efeitos de biome/feature provider-native; a semântica e custo herdados registrados em [RITUALS.md](RITUALS.md) são source-pinned, não prova de settlement e persistência em execução.
- A soma 39+8 é a mesma contribuição semântica histórica do provider, **+0**. Familiars, perks, armor, child projectiles, Source machines, status e equipment não são glifos/rituais adicionais.

## Contratos e pendências

**✅ Provado:** SHA e tamanho do JAR oficial equivalem à modlist; classes, IDs, cardinalidade, bootstrap e gates de registro estático.

**⚠️ PENDENTE:** custo mana/Source observado, configs de glyph/ritual efetivamente aplicadas, receitas e aquisição Survival, compatibilidade com Ars Nouveau 5.13.1 no pack real, multiplayer e client/dedicated acceptance, limite de projectile propagation, efeitos worldgen, claims, familiars e Source relays. Testes determinísticos do Black Arcana não se confundem com gameplay real do Ars Elemental. Stage 06.05 continua 🟡.

**Autoridade/clean-room:** Ars Nouveau/Elemental mantêm casting, mana, Source, glyph/ritual execution e world effects externos. Black Arcana mantém seu casting, rituais, hazards, Corruption/Strain e `WorldEffectPolicy` sem double-cast ou double-debit. RPG Skill Tree fornece apenas progressão/perks/Mastery/gates sob contrato real. Nenhum código/asset/bytecode de terceiros foi copiado.
