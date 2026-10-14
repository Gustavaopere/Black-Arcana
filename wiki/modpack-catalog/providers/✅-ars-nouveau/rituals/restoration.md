# Restoration

Status: `SOURCE-PINNED 5.13.1 / HEALING-CURE RITUAL`

- Registry id: `ars_nouveau:ritual_restoration`
- Class: `RitualHealing`
- Source cost declaration: `200`
- Processing cadence: every `100` game ticks
- Radius: `5` blocks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every 100 ticks, Restoration scans LivingEntities in radius 5 and selects the first nearby player, if any, for Zombie Villager cure attribution.

For each entity:

- `ZombieVillager`: starts conversion immediately (`conversion time = 0`) using the nearby player's UUID when available;
- inverted heal/harm entities: receive `10.0` damage from an Ars fake-player attack source;
- other damaged living entities: heal `10.0` health.

If at least one eligible operation occurs, the ritual marks the work cycle as needing Source.

The provider description notes that cured villagers can grant discounts when a player was nearby; the exact discount semantics remain vanilla/provider conversion behavior rather than a separate Black Arcana reward.

## Authority / Black Arcana boundary

Healing, undead harm, villager conversion attribution and Source settlement remain Ars Nouveau/vanilla authority. Black Arcana must not replay healing/damage or create a second cure/reputation credit.

## QA

Source behavior is pinned to 5.13.1. Effective Source debit timing and interactions with altered villager curing/undead tags in the full pack remain runtime QA.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualHealing.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualHealing.java), versão Ars Nouveau 5.13.1.
- **Frequência/targets:** `RitualHealing.tick()` a cada `100` game ticks usa AABB `inflate(5)` e `LivingEntity`, procurando primeiro `Player` na lista para possível UUID de atribuição de cura.
- **Três destinos:** `ZombieVillager.startConverting(optionalPlayerUUID,0)` diretamente; para `isInvertedHealAndHarm`, `hurt(...playerAttack(ANFakePlayer),10.0f)`; para outros danificados, `heal(10.0f)`. Marca `didWorkOnce` e `setNeedsSource(true)` quando algo foi processado. O dano a entidades inverted é playerAttack fake, **não** magic damage de Ars glyph Heal.
- **Custos/perks:** `getSourceCost()=200` no source; débito efetivo pelo contexto Ritual requer validação. Cure credit/reputation, XP e life-steal não devem ser atribuídos como ataque/cast independente por sinais indiretos.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.
