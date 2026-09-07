# Paladin Spells — technical audit 1.1.1

## Exact source pin

- installed: `paladin_spells-1.21.1-1.1.1.jar`;
- branch: `Kaufko/Paladin-Spells` → `1.21`;
- audited head: `31f64ccdb39d062b21cc25d434cb62d6463b486e`;
- head message: `Fixed server crash due to using client only class`;
- upstream `gradle.properties`: `minecraft_version=1.21.1`, `mod_version=1.21.1-1.1.1`.

## Registry

`PaladinSpellRegistry` registers exactly five spells into Iron's `SPELL_REGISTRY_KEY`:

- `paladin_spells:taunt`;
- `paladin_spells:bulwark`;
- `paladin_spells:sworn_protector`;
- `paladin_spells:bedrock_skin`;
- `paladin_spells:ram`.

All five use `SchoolRegistry.HOLY_RESOURCE` and minimum rarity Rare.

## Current-release correction

The upstream README still labels Sworn Protector WIP, but the 1.1.1 changelog explicitly says WIP was removed from two spells because they are released. For current-state cataloging the release changelog outranks stale README wording.

## Iron's inherited formula

Installed Iron's 3.16.3 `AbstractSpell` confirms:

`mana = (baseManaCost + manaCostPerLevel*(level-1)) * configManaMultiplier`

`spellPower = (baseSpellPower + spellPowerPerLevel*(level-1)) * genericSpellPower * HolyPower * configPowerMultiplier`

Individual pages therefore show neutral/base ranges plus formulas that consume final `getSpellPower` where applicable.

## QA findings

### Bulwark

- spell power baseline: 15→60;
- duration formula: `min(5 + 0.15*spellPower, 35)`;
- amplifier: `round(spellPower*10)`;
- `BulwarkEffect` declares `Attributes.ARMOR`, `ADD_MULTIPLIED_TOTAL`, amount `0.0`.

No separate Bulwark event handler was found. Live validation is mandatory before using Bulwark as an armor-authority dependency.

### Sworn Protector

The server event is structurally robust in several ways: it only handles player victims, ignores redirect damage recursively, chooses the closest eligible protector, checks stored per-protector range, avoids redirect when the protector is the attacker, subtracts the redirected portion exactly once and hurts the protector with a dedicated `REDIRECT` damage type.

However, the current spell's `onCast` applies effect and persistent redirect/range data only when `level.isClientSide`. The event explicitly returns client-side. Static source therefore shows a server-authority mismatch requiring live validation/fix upstream before Black Arcana relies on it.

### Bedrock Skin

- server cast writes `bedrock_skin_reduction` persistent float;
- repository search finds that key only in spell/effect declarations, not a damage handler;
- effect independently declares +10 Armor ADD_VALUE and the spell uses amplifier `level-1`;
- `BedrockSkinEntity` roots horizontal movement by mounting the caster onto an invulnerable anchor that only moves vertically and discards after duration/dismount.

The immobilization contract is source-confirmed; percentage mitigation settlement is not.

### Ram

- server cast generates dash `ImpulseCastData` and directly sets movement;
- swept AABB is movement vector expansion +1.5;
- every alive LivingEntity except the caster is hurt with `mobAttack` and knocked back;
- no friendly-fire/party gate appears here;
- `vec.add(0,0.25,0)` is called without reassigning the immutable Vec3 return when grounded; static source suggests the intended extra vertical vector component may be lost, although the caster is separately moved upward by 1.5 blocks.

### Taunt

- scans nearby `Mob` instances;
- only `Enemy` mobs receive the effect;
- stores caster UUID in mob persistent data;
- `TauntEffect` runs every tick, resolves the UUID server-side, sets mob target/aggressive and sets last-hurt-by-player when the taunter is a player.

This is the provider-native authority for forced aggro; bridges should not issue parallel `setTarget` loops.

## Acquisition and assets

Provider-specific acquisition data was not confirmed. Exact scroll generation/Inscription/loot behavior remains `NÃO VERIFICADO`.

Presentation is provider-native. Black Arcana may improve visuals only through non-authoritative presentation layers that do not duplicate effects, target selection or damage settlement.
