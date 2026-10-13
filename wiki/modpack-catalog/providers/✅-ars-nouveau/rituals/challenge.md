# Challenge

Status: `SOURCE-PINNED 5.13.1 / RAID RITUAL`

- Registry id: `ars_nouveau:ritual_challenge`
- Class: `RitualPillagerRaid`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Once per 20 server ticks the ritual increments progress. At progress `18`, it looks for `ServerPlayer` entities within an AABB inflated by `5.0` blocks around the ritual and asks the vanilla raid manager to create or extend a raid using the first returned player and the ritual position.

The ritual finishes only when a non-null `Raid` is returned.

### Optional Emerald modifier

Outside Hard difficulty, the ritual accepts exactly one emerald-tag item while its consumed-item list is empty. If that Emerald was consumed and a raid is successfully created, the provider sets `raid.numGroups = 7`.

On Hard difficulty the ritual refuses this optional modifier.

The provider description frames the ritual as summoning an illager raid when used inside a village; the actual village/raid validity remains enforced by the vanilla raid creation path.

## Authority / Black Arcana boundary

Raid creation, player association, raid group count and optional item consumption remain provider/vanilla authority. Black Arcana must not create a second raid, consume another Emerald or re-credit raid waves as separate ritual completions.

## QA

Source behavior is pinned to 5.13.1. Effective interaction with other raid modifiers and full-pack village mechanics remains runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`RitualPillagerRaid.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualPillagerRaid.java), `com.hollingsworth.arsnouveau.common.ritual.RitualPillagerRaid`, Ars 5.13.1.
- **Progresso:** a cada `20` ticks server avança `progress`, e quando `>=18` procura `ServerPlayer` em `AABB(brazier).inflate(5.0)`; usa o **primeiro** player retornado para `world.getRaids().createOrExtendRaid(player,brazierPos)`. Ritual só finaliza com `Raid` não nulo; sem player ou sem raid válida pode persistir.
- **Modificador:** `canConsumeItem` permite item de `Tags.Items.GEMS_EMERALD` se dificuldade **não** HARD e `consumedItems` estiver vazio. Quando raid foi criada, `didConsumeItem(Items.EMERALD)` (tipo **exato**) altera `raid.numGroups=7`. A diferença entre aceitação por tag e teste de `Items.EMERALD` merece verificação com gems equivalentes; não presumir que qualquer emerald-tag tenha o mesmo resultado.
- **Perks:** raid e waves pertencem ao manager vanilla/Ars. Não creditar Mastery por cada onda como conclusão independente, nem mutar `raid.numGroups`/consumo sem API de integração e validação de conflito com addons.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.
