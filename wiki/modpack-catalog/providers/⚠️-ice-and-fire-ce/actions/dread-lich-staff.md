# Dread Lich Staff Projectile

- Provider: **Ice And Fire Community Edition** (`iceandfire`)
- Version: `2.1.2`
- Provider item: `iceandfire:lich_staff`
- Classificação: **projectile magic-staff action**
- State: `COUNTED_EXACT`

## Identidade semântica

Uma única ação de staff/projétil provider-owned. O projétil e seus efeitos downstream pertencem à mesma raiz causal.

## Reachability

A rota de aquisição está fechada por auditoria runtime específica do pack: o artefato 2.1.2 equipa Dread Liches com o staff em `MAINHAND`, e a runtime NeoForge 21.1.250 atual fecha o caminho herdado de equipment drop.

Essa conclusão não é uma inferência genérica de vanilla; ela depende do audit registrado em `DREAD-LICH-STAFF-EXACT-RUNTIME-REACHABILITY.md`.

## Evidence boundary

A identidade e a rota de aquisição estão fechadas. Chance observada na runtime auditada não é reinterpretada como garantia de drop por encontro, e mecânicas do projétil permanecem provider-owned.

Source: `../ACTIVE-MAGIC-INVENTORY.md`.
