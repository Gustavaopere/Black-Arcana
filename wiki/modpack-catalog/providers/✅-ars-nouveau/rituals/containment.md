# Containment

Status: `SOURCE-PINNED 5.13.1 / MOB-JAR CAPTURE RITUAL`

- Registry id: `ars_nouveau:ritual_containment`
- Class: `RitualMobCapture`
- Source cost declaration: `500`
- Work cadence: every `60` game ticks
- Jar search cube: `±3` blocks around the ritual
- Entity search: AABB inflated `5` blocks around each eligible empty Mob Jar
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

On each server work cycle, Containment scans nearby placed `MobJar` blocks. Only empty `MobJarTile` instances are eligible. For each, it searches entities around that jar using the provider `canJar` predicate.

Before serialization, the provider detaches passengers, drops valid leashes, removes active Raiders from raids and releases Villager POI memories. If `MobJarTile.setEntityData(e)` succeeds, the original entity is removed with `UNLOADED_TO_CHUNK`, a visual flying-item effect is spawned toward the jar and provider advancements may trigger for special captures.

Default capture admission:

- explicit provider jar whitelist always allowed;
- provider jar blacklist denied;
- multipart `PartEntity` denied;
- blacklisted ItemEntity stacks denied;
- otherwise living non-player, non-dead entities are allowed.

If at least one capture succeeds in the work cycle, the ritual calls `setNeedsSource(true)` once after scanning the jars.

## Description ↔ executable-radius mismatch

The provider description says mobs and jars must be within 3 blocks of the brazier. The pinned executable path enforces the 3-block cube for **jars**, but searches entities within an AABB inflated by **5 blocks around each jar**. This difference is preserved as runtime/UX QA rather than normalized by assumption.

## Authority / Black Arcana boundary

Entity serialization, removal, Mob Jar data, special jar behavior and Source settlement remain Ars Nouveau authority. Black Arcana must not create a parallel capture ledger or duplicate entity data.

## QA

Source entry path is pinned to 5.13.1. Effective Source batching, multipart/modded entity support and special Mob Jar behaviors remain runtime/provider QA.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`RitualMobCapture.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualMobCapture.java), `com.hollingsworth.arsnouveau.common.ritual.RitualMobCapture`, Ars 5.13.1.
- **Geometria/cadência:** a cada `60` ticks no servidor percorre posições `brazier±3` por eixo, isto é um cubo de `7×7×7` **candidatos a jarro** antes de filtro `MobJar`. Para cada `MobJarTile` vazio procura entidades em `AABB(jarPos).inflate(5)`, volume independente de 3 blocos do brazier. Divergência da descrição do provider deve permanecer explícita.
- **Elegibilidade:** `canJar` aceita whitelist `JAR_WHITELIST` antes da blacklist; em seguida bloqueia `JAR_BLACKLIST`, `PartEntity`, `ItemEntity` com tag de item `JAR_ITEM_CAPTURE_BLACKLIST`; fallback admite `LivingEntity` não-player e não morta. A ordem whitelist→blacklist é significativa e não deve ser invertida por um gate customizado.
- **Settlement:** desmonta passageiros/leash/raid/POI de Villagers antes de `tile.setEntityData(e)`; apenas após sucesso retira entidade com `RemovalReason.UNLOADED_TO_CHUNK` e cria efeitos visuais. Se ao menos uma captura teve sucesso marca `setNeedsSource(true)` ao final; `getSourceCost=500` não prova debit 500 por mob. Mesmo `MobJarTile` processa no máximo uma entidade por ciclo devido ao `break` interno.
- **Perks:** captura, descarte, persistência do jarro, Source e conquistas especiais pertencem ao Ars; não duplicar entity serialization nem award XP por VFX.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.
