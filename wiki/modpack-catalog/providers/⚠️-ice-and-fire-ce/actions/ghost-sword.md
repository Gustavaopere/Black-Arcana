# Ghost Sword / Phantasmal Blade

- Provider: **Ice And Fire Community Edition** (`iceandfire`)
- Version: `2.1.2`
- Provider item: `iceandfire:ghost_sword`
- Classificação: **swing-triggered phantasmal projectile action**
- State: `EXACT IDENTITY / DEPLOYED CONFIG CONDITIONAL`

## Identidade semântica

Uma única família supernatural associada ao swing da Ghost Sword / Phantasmal Blade. O projétil é consequência da mesma ação e não uma segunda identidade.

## Reachability

Recipe + advancement do item estão fechados no artefato atual. A ação, porém, lê o gate provider-native:

`config/iceandfire/iaf-common.json -> tools.phantasmalBladeAbility`

O source default não substitui o valor implantado.

- valor efetivo `true` + ausência de outro gate runtime => candidata à promoção individual ao strict;
- `false`, valor ausente/ambíguo ou evidência não vinculada ao SHA-1 atual => fail-closed.

## Evidence boundary

A identidade e aquisição do item estão fechadas; a ativação current-pack permanece condicionada. Fórmulas, dano, velocidade, cooldown e demais detalhes do projétil não são inferidos.

Source: `../DEPLOYED-CONFIG-AND-REACHABILITY-CHECKLIST.md`.
