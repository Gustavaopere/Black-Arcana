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

## Fichas individuais de Focus — 2026-10-11

**✅ 28/28 Focuses com páginas próprias:** [FOCUS-CARDS-1.21.1-1.8.2.md](FOCUS-CARDS-1.21.1-1.8.2.md) e `focuses/`. Os nomes de holders já provados pelo JAR exato tornam possível a individualização sem fabricar `ResourceLocation` nem mecânicas. Os **28/28** caminhos de aquisição estão agora individualizados: 24 vias `goety:ritual` já provadas e [4 recipes `minecraft:crafting_shaped` comprovadas com path e output no JAR exato](FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md), reauditoria [#38191990175](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38191990175).

**✅ 24/24 rituais não-Focus individualizados** em [RITUAL-CARDS-1.21.1-1.8.2.md](RITUAL-CARDS-1.21.1-1.8.2.md), a partir de [48 paths/outcomes `goety:ritual` exatos](RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md) reextraídos no [workflow #38190078609](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38190078609) com SHA-1 físico confirmado. São 10 conversões, 13 summons/thralls e 1 fabricator; os outros 24 rituais são receitas de Focus deduplicadas. **+0 identidades** (52 `COUNTED_EXACT` mantidos). Os 24 Focuses com ritual têm path confirmado e os quatro restantes têm agora [paths `minecraft:crafting_shaped` comprovados](FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md), sem inventar ingredientes ou aquisição efetiva em Survival. QA/Survival permanece ⚠️ e API fail-closed.

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

- **4/4 Focuses comuns** com paths e outputs exatos em [FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md](FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md), auditados após hash-match no workflow [#38191990175](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38191990175), branch NON-MERGE `eae06402af7abbe6195e05a41f72cfd27bbf453d`. 28/28 caminhos de aquisição agora nominais, **+0 identidades**.

- Reextração exata text-only, [workflow #38190078609](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38190078609), branch de auditoria NON-MERGE `449444fc897659bb3ab2506ff61c5b1920aa4148`. [Matriz 48/48](RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md) e [24 fichas](RITUAL-CARDS-1.21.1-1.8.2.md); sem JAR/recipes integrais em branch de catálogo.

- NON-MERGE PR #206, HEAD `cd91bc9719f63ba0565981349f06a103fd6a9782`;
- structural run `34704449593`, artifact `10301367858`, digest `sha256:1dc688c4068dc4e89e6f04142cb1cd99eeff995ba1f53b8ce4e1429cc8af53d8`;
- targeted semantic run `34704823100`, artifact `10301168646`, digest `sha256:8cc6324727a854700e149df3d05ef376c5a078e9ec6c1cea79f702ec9bbde980`;
- registration/config run `34705567753`, artifact `10301603762`, digest `sha256:79054acb2c82ec3472403e9b926c9f1a6bafd1da47a873ef0a3dc3b794875850`.

Runtime servant lifecycle/combat, numerical balance, cross-addon compatibility e qualquer adapter Black Arcana permanecem fail-closed até QA/contrato provider-native específico.
