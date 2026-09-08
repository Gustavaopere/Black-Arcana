# Potion Jar ↔ Create potion-fluid bridge

State: `SOURCE-PINNED 5.4.0 / ROUNDING QA PENDING`

Ars Creo registers NeoForge `Capabilities.FluidHandler.BLOCK` on the Ars Nouveau Potion Jar BlockEntityType, backed by `PotionTank`.

Exact conversion constants:

- Ars potion units -> mB: `2.5`;
- mB -> Ars potion units: `0.4`.

Capacity is `int(maxFill * 2.5)`. Fill/drain use ceiling when converting mB back into jar units. Only Create's Potion source fluid with `POTION_CONTENTS` accepted by the Ars jar is valid.

This is a capability adapter, not a second potion inventory. The Ars Potion Jar remains authority for potion type/count; Create/NeoForge fluid transport owns transfer requests.

Rounding at small transfer sizes and interaction with other fluid handlers require runtime QA.