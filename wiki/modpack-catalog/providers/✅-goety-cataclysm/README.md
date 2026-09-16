# Goety Cataclysm 1.21.1-1.8.2 — exact-artifact semantic closure

## Estado canônico do catálogo

- JAR físico: `goety_cataclysm-1.21.1-1.8.2.jar`
- Mod ID: `goety_cataclysm`
- versão: `1.21.1-1.8.2`
- Minecraft: `1.21.1`
- loader: NeoForge
- CurseForge project/file: `1224214 / 8518940`
- SHA-1 físico e auditado: `4e3052a082200371b36e1a88fdce05e294d82757`
- licença: `All Rights Reserved`
- classificação: `BRIDGE_COMPAT + SPELL/RITUAL CONTENT`
- estado semântico: `COUNTED_EXACT`
- contribuição semântica: **52**
- componente técnico: **#60** após Phase 2BL

A Phase 2BL substitui o antigo limite publisher-only por evidência do JAR exato hash-matched. O source público antigo da linha 1.20 não é tratado como authority de implementação da build física 1.21.1. O JAR não é redistribuído.

## Inventário semântico exato

O provider registra exatamente **28 Focuses próprios**:

`ABYSSAL_BEAM_FOCUS`, `ABYSSAL_MINE_FOCUS`, `ABYSSAL_ORB_FOCUS`, `AMETHYST_CLUSTER_FOCUS`, `ASHEN_BREATH_FOCUS`, `BATTLEFIELD_FOCUS`, `CURSED_CAIRN_FOCUS`, `CURSED_GRAVE_FOCUS`, `CURSED_TOMB_FOCUS`, `DEATH_LASER_FOCUS`, `DESERT_CRUSH_FOCUS`, `DESERT_RAID_FOCUS`, `EARTH_SHAKE_FOCUS`, `EXTINCT_FLAME_FOCUS`, `FLARE_BOMB_FOCUS`, `KAKOURGOS_FOCUS`, `KYRIA_FOCUS`, `LIGHTNING_SPEAR_FOCUS`, `POLEMISTIS_FOCUS`, `SANDSTORM_FOCUS`, `STORM_SERPENT_FOCUS`, `SUNKEN_CURRENT_FOCUS`, `SUNKEN_SWELL_FOCUS`, `SUNKEN_TRIBUNE_FOCUS`, `THUNDER_RAGE_FOCUS`, `VOID_RUNE_FOCUS`, `VOID_VORTEX_FOCUS`, `WATER_SPEAR_FOCUS`.

Todos os 28 possuem caminho de aquisição no artefato: **24 via `goety:ritual` e 4 via crafting normal**. As recipes de aquisição não são recontadas como ações independentes.

O JAR contém **48 recipes `goety:ritual`**; retiradas as 24 recipes de aquisição de Focus, restam **24 rituais não-Focus**. O passe direcionado fecha 24 outcomes distintos, sem conditions de mod: 10 conversões, 13 summon/thrall actions e 1 fabricator action. Esses outcomes são addon-owned e não duplicam os 238 rituais distintos já contados no Goety base.

Portanto: **28 Focus + 24 rituais não-Focus = 52 objetos mágicos semânticos `COUNTED_EXACT`.**

## Gate de registration/config

O passe estrutural do initializer prova:

- Focus holders: `28`;
- branches no static initializer do registry: `0`;
- chamadas `DeferredRegister.register` observadas no initializer: `38`;
- referências a `GCSpellConfig` no initializer: `0`;
- campos config enable/disable-like: `0`.

Logo os 28 Focuses não dependem de um gate provider-specific de registration/config. Balance, custos, servant stats e combat behavior continuam runtime/balance QA separado.

## Authority e deduplicação

- Goety continua authority de Soul Energy, Focus casting e servant lifecycle base.
- L_Ender's Cataclysm continua authority dos mobs, bosses e conteúdo-base que fornece.
- Goety Cataclysm é authority somente dos Focuses, rituais, servants e adaptações que registra.
- Black Arcana não cria segundo Soul ledger, segundo servant state, segundo ritual settlement nem segundo cast pipeline.

## Evidência

- NON-MERGE PR #206, HEAD `cd91bc9719f63ba0565981349f06a103fd6a9782`;
- structural run `34704449593`, artifact `10301367858`, digest `sha256:1dc688c4068dc4e89e6f04142cb1cd99eeff995ba1f53b8ce4e1429cc8af53d8`;
- targeted semantic run `34704823100`, artifact `10301168646`, digest `sha256:8cc6324727a854700e149df3d05ef376c5a078e9ec6c1cea79f702ec9bbde980`;
- registration/config run `34705567753`, artifact `10301603762`, digest `sha256:79054acb2c82ec3472403e9b926c9f1a6bafd1da47a873ef0a3dc3b794875850`.

Runtime servant lifecycle/combat, numerical balance, cross-addon compatibility e qualquer adapter Black Arcana permanecem fail-closed até QA/contrato provider-native específico.
