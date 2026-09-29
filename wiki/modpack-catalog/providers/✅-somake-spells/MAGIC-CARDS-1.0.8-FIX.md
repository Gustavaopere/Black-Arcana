# Somake Spells 1.0.8-fix — fichas históricas de registry

Este índice preserva em fichas individuais as **67 identidades de spell** fechadas pela auditoria clean-room do artefato físico histórico `somakespells-1.0.8-1.21.1-fix.jar` (SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`). A linha física atual é 1.0.9; estas fichas não são um registry 1.0.9. Use `CURRENT-1.0.9-REVALIDATION-CHECKLIST.md` para a autoridade corrente.

No checkpoint físico de 1.0.8-fix, todas as 67 identidades estavam registradas sob o conjunto de dependências opcionais daquele snapshot, mas permaneciam `EXACT_REGISTRY / REACHABILITY_CONDITIONAL`: a aquisição survival objeto-a-objeto e o valor COMMON implantado de `enableSpellLockSystem` não estão provados. O provider continua **⚠️ parcial/condicionado**.

A organização abaixo é por **gate de registro**, não por escola. Escola, efeitos e números não são inferidos do nome do registry.

## Registros sem gate opcional — 61

- [`combustion`](registry/combustion.md)
- [`ritual_flame`](registry/ritual-flame.md)
- [`damned_demomans`](registry/damned-demomans.md)
- [`eruption`](registry/eruption.md)
- [`fire_blast`](registry/fire-blast.md)
- [`firestorm_vortex`](registry/firestorm-vortex.md)
- [`pumpkin_bomb`](registry/pumpkin-bomb.md)
- [`ignis_shield`](registry/ignis-shield.md)
- [`incinerator_slash`](registry/incinerator-slash.md)
- [`abyssal_burn`](registry/abyssal-burn.md)
- [`fire_orbs`](registry/fire-orbs.md)
- [`abyssal_orbs`](registry/abyssal-orbs.md)
- [`apocalyptic_burst`](registry/apocalyptic-burst.md)
- [`earthbound`](registry/earthbound.md)
- [`submerge`](registry/submerge.md)
- [`tidal_grasp`](registry/tidal-grasp.md)
- [`tsunami`](registry/tsunami.md)
- [`tidal_dash`](registry/tidal-dash.md)
- [`thunder_cloud`](registry/thunder-cloud.md)
- [`water_control`](registry/water-control.md)
- [`water_spear`](registry/water-spear.md)
- [`hydro_slash`](registry/hydro-slash.md)
- [`sea_serpent`](registry/sea-serpent.md)
- [`sea_serpent_jet`](registry/sea-serpent-jet.md)
- [`storm_aura`](registry/storm-aura.md)
- [`water_ball`](registry/water-ball.md)
- [`summon_zombie`](registry/summon-zombie.md)
- [`lightning_spear`](registry/lightning-spear.md)
- [`ender_corruption`](registry/ender-corruption.md)
- [`phantom_barrage`](registry/phantom-barrage.md)
- [`overgrowth`](registry/overgrowth.md)
- [`permafrost`](registry/permafrost.md)
- [`blessing`](registry/blessing.md)
- [`custodia_caeli`](registry/custodia-caeli.md)
- [`blood_rush`](registry/blood-rush.md)
- [`blood_cut`](registry/blood-cut.md)
- [`bloody_legacy`](registry/bloody-legacy.md)
- [`bloodmark`](registry/bloodmark.md)
- [`fragmented_requiem`](registry/fragmented-requiem.md)
- [`rose_secret`](registry/rose-secret.md)
- [`eldritch_gambit`](registry/eldritch-gambit.md)
- [`chain_connection`](registry/chain-connection.md)
- [`evocation_fortitude`](registry/evocation-fortitude.md)
- [`reverberation`](registry/reverberation.md)
- [`slumber_melody`](registry/slumber-melody.md)
- [`resonant_pulse`](registry/resonant-pulse.md)
- [`ram_tchum`](registry/ram-tchum.md)
- [`jingle_bell`](registry/jingle-bell.md)
- [`lightning_ball`](registry/lightning-ball.md)
- [`lightning_dance`](registry/lightning-dance.md)
- [`lightning_field`](registry/lightning-field.md)
- [`lightning_strike`](registry/lightning-strike.md)
- [`lightning_cut`](registry/lightning-cut.md)
- [`lightning_spark`](registry/lightning-spark.md)
- [`lightning_swarm`](registry/lightning-swarm.md)
- [`lightning_lash`](registry/lightning-lash.md)
- [`halberd_strike`](registry/halberd-strike.md)
- [`render_rush`](registry/render-rush.md)
- [`axe_cleave`](registry/axe-cleave.md)
- [`desert_wrath`](registry/desert-wrath.md)
- [`soul_grab`](registry/soul-grab.md)

## Gate Mowzie's Mobs — 3

O artefato exato testa `mowziesmobs`; o checkpoint físico usado pela auditoria continha Mowzie's Mobs `1.8.2`.

- [`blessed_connection`](registry/blessed-connection.md)
- [`guardian_connection`](registry/guardian-connection.md)
- [`cursed_connection`](registry/cursed-connection.md)

## Gate Magic From the East — 3

O artefato exato testa `iss_magicfromtheeast`; o checkpoint físico usado pela auditoria continha Magic From the East `1.1.5`.

- [`mirror_strike`](registry/mirror-strike.md)
- [`spirit_empowerment`](registry/spirit-empowerment.md)
- [`symmetry_empowerment`](registry/symmetry-empowerment.md)

## Contagem e estado

- 67/67 identidades de registry materializadas em fichas individuais;
- 61 registros incondicionais no initializer auditado;
- 3 registros com gate `mowziesmobs`, satisfeitos naquele checkpoint;
- 3 registros com gate `iss_magicfromtheeast`, satisfeitos naquele checkpoint;
- 67/67 continuam `REACHABILITY_CONDITIONAL`;
- nenhuma escola, fórmula, custo, cooldown, nível, rarity, targeting ou aquisição foi inventada;
- contribuição estrita permanece `+0` enquanto reachability/config implantada não forem fechadas.

## Autoridade

`EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md` e `SPELL-CATALOG-1.0.8-FIX.md` permanecem as fontes técnicas primárias **do checkpoint histórico 1.0.8-fix**. Estas fichas são uma projeção editorial objeto-a-objeto. Iron's mantém autoridade do host casting/resource settlement; Somake mantém autoridade sobre suas spells e progressão; Black Arcana não duplica esses runtimes.
