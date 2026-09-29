# Ice And Fire Community Edition 2.1.2 — fichas canônicas de ações

Este índice materializa em fichas individuais as **9 famílias de ação mágica** fechadas pela auditoria do artefato físico/publisher exato `iceandfire-2.1.2.jar`.

O provider permanece **⚠️ parcial/condicionado** porque Ghost Sword / Phantasmal Blade ainda depende do valor implantado de `tools.phantasmalBladeAbility`. As outras oito famílias já são `COUNTED_EXACT`.

## Ações strict — 8

- [Cockatrice Scepter Beam](actions/cockatrice-scepter-beam.md)
- [Deathworm Gauntlet Lunge / Strike](actions/deathworm-gauntlet.md)
- [Gorgon Head Petrification](actions/gorgon-head.md)
- [Dread Lich Staff Projectile](actions/dread-lich-staff.md)
- [Pixie Wand Charge](actions/pixie-wand.md)
- [Siren Flute Charm](actions/siren-flute.md)
- [Summoning Crystal Teleport](actions/summoning-crystal.md)
- [Stymphalian Feather Volley](actions/stymphalian-feather-volley.md)

## Ação condicional — 1

- [Ghost Sword / Phantasmal Blade](actions/ghost-sword.md)

## Contagem e deduplicação

- total exato de famílias ativas: **9**;
- strict: **8**;
- condicional: **1**;
- strict contribution do provider: **+8**;
- Deathworm Gauntlet e Summoning Crystal possuem variantes físicas, mas cada conjunto é uma única família causal;
- Dread Queen Staff, Cyclops Eye, Dragon Flute, Dragon Horn, Tide Trident e post-hit `BuiltinAbilities` permanecem excluídos conforme o inventário canônico;
- efeitos, projéteis, partículas, cooldown, durabilidade, tame state e demais consequências downstream não criam identidades adicionais.

## Reachability

As oito famílias strict já têm aquisição/reachability fechada por evidência exata. Para sete delas, drift do artefato físico reabre a rota. Para **Dread Lich Staff**, a prova também depende da runtime NeoForge `21.1.250`; drift do provider **ou do loader/runtime** reabre especificamente essa aquisição e exige nova auditoria antes de preservar `COUNTED_EXACT`.

Ghost Sword possui recipe/advancement exatos, mas sua ação só pode entrar no strict após evidência implantada de:

`config/iceandfire/iaf-common.json -> tools.phantasmalBladeAbility=true`

associada ao SHA-1 físico esperado.

Fontes canônicas: [ACTIVE-MAGIC-INVENTORY.md](ACTIVE-MAGIC-INVENTORY.md) e [DEPLOYED-CONFIG-AND-REACHABILITY-CHECKLIST.md](DEPLOYED-CONFIG-AND-REACHABILITY-CHECKLIST.md).