# Ars Creo 5.4.0 — config, dependencies and compatibility

Status: `SOURCE-PINNED DEFAULTS / EFFECTIVE PACK CONFIG+RUNTIME QA PENDING`

## Physical provider set

- Ars Creo `5.4.0`
- Ars Nouveau `5.13.1`
- Create `6.0.10`
- NeoForge `21.1.248`

## Declared source requirements

Exact 5.4.0 `neoforge.mods.toml` declares:

- NeoForge `[21,)`;
- Minecraft `[1.20.6,1.21.2)`;
- Ars Nouveau `[5.0.0,)` mandatory;
- Create `[6.0.9,)` mandatory;
- side BOTH.

The physical pack satisfies these ranges. This is metadata compatibility, not proof of full runtime compatibility with the exact installed versions.

## Common config defaults

`CreoConfig` defines:

- `wheelBaseSpeed = 16`, min 0;
- `wheelMaxSpeed = 24`, min 0;
- `wheelStressCapacity = 16`, min 0.0.

No other provider config values were found in the exact config class.

## Create/Ars seams

Ars Creo uses public/internal runtime classes from both providers, including Create movement/interaction registries and Ars spell/source/portal/ritual classes. Public Java visibility is not treated as a stable Black Arcana API contract.

## Runtime QA priorities

1. Verify Ars Creo 5.4.0 with physical Ars Nouveau 5.13.1 and Create 6.0.10.
2. Verify effective server config values rather than source defaults.
3. Verify moving turrets under Create/Aeronautics/Sable sublevel contexts separately.
4. Verify portal destination behavior and claim/world-safety interactions.
5. Verify which Ars rituals work with the stand-in brazier implementation.
6. Verify Potion Jar fluid rounding/automation under the full fluid stack.
7. Verify SourceManager provider registration/removal through assembly/disassembly/unload.

No unsupported seam receives a fallback Black Arcana adapter.