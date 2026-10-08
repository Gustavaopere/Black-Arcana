# Mowzie's Mobs 1.8.2 — fichas canônicas de poderes do jogador

Este índice materializa em fichas individuais as **11 identidades semânticas player-facing** reconciliadas no artefato físico/publisher exato `mowziesmobs-1.21.1-1.8.2.jar`.

A identidade `tunneling` permanece **⚠️ condicionada** porque sua ativação depende do valor efetivamente implantado de `enableTunneling`. As outras dez identidades permanecem strict.

## Heliomancy — 4

- [Sunstrike](actions/sunstrike.md)
- [Solar Beam](actions/solar-beam.md)
- [Solar Flare](actions/solar-flare.md)
- [Supernova](actions/supernova.md)

## Weapon / Ice — 3

- [Wrought Axe Swing](actions/wrought-axe-swing.md)
- [Wrought Axe Slam](actions/wrought-axe-slam.md)
- [Ice Breath](actions/ice-breath.md)

## Geomancy — 4

- [Boulder Lift](actions/boulder-lift.md)
- [Pillar Rise](actions/pillar-rise.md)
- [Rock Sling](actions/rock-sling.md)
- [Tunneling](actions/tunneling.md) — conditional

## Contagem e exclusões

- strict: **10**;
- conditional: **1** (`tunneling`);
- strict contribution: **+10**;
- `hit_boulder` é subação técnica do Boulder Lift e adiciona +0;
- `backstab` é proc/slot técnico de ataque e adiciona +0;
- `fireball`, `ground_slam`, `boulder_roll` e `fissure` são declarados mas não pertencem ao `PLAYER_ABILITIES` atual e adicionam +0;
- entidades, projéteis, efeitos, animações e settlement downstream não criam identidades adicionais.

## Gate implantado

A única pendência de catálogo é o valor efetivo do provider para Tunneling, coletado da instância/mundo atual e associado ao SHA-1 físico esperado.

- efetivo `true` => Tunneling pode ser promovido; strict do provider passa a 11;
- efetivo `false` => Tunneling fecha como deployed-disabled; strict permanece 10;
- missing/ambiguous/conflicting => provider permanece ⚠️.

Checkpoint de materialização: [INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

Fontes canônicas: [PLAYER-MAGIC-INVENTORY.md](PLAYER-MAGIC-INVENTORY.md), [EXACT-1.8.2-ARTIFACT-AUDIT.md](EXACT-1.8.2-ARTIFACT-AUDIT.md) e [DEPLOYED-CONFIG-CHECKLIST.md](DEPLOYED-CONFIG-CHECKLIST.md).
