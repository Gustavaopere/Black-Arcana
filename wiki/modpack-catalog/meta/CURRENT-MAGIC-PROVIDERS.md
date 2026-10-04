# Inventário atual de providers mágicos

## Estado

`AUDITORIA EM ANDAMENTO — categoria física Magic atual reconciliada 97/97 / cross-domain provider queue ainda PENDING REBASE`

O bloco de 595 entradas / NeoForge `21.1.248` abaixo é um **checkpoint histórico de 2026-09-11**. A autoridade corrente para presença/versão combina a modlist física do Project Library com os dossiês físicos sibling mais novos quando estes a supersedem; a taxonomia status-prefixed do sibling não é usada para negar um JAR diretamente observado. O denominador global de providers continua `PENDING REBASE`: a categoria física `Magic` está mapeada, mas o universo cross-domain/root-level é maior que essa pasta.

O antigo denominador interno de **100 componentes mágicos/cross-domain** permanece apenas como checkpoint histórico: ele foi construído antes da rodada física sibling de 22/09 revelar componentes mágicos adicionais, incluindo Hazen N Stuff. Os fechamentos até Mobstein continuam válidos como **68 componentes canônicos daquele conjunto**, mas `68/100` não deve mais ser publicado como fração técnica corrente. Hazen N Stuff fecha o próximo componente conhecido; o novo denominador global fica `PENDING REBASE` até reconciliação integral da modlist física atual.

A árvore canônica atual possui **151 diretórios top-level de provider = 148 ✅ + 3 ⚠️**. Os três diretórios ainda abertos em nível de catálogo são `⚠️-irons-spellbooks-kubejs`, `⚠️-traveloptics` e `⚠️-deeper-and-darker`. Após o fechamento de StarbuncleMania em 30/09, o rebase cross-domain de 01/10 adiciona `✅-ignis-soulfires`, `✅-artifacts`, `✅-cataclysm`, `✅-betterend`, `✅-weapons-of-miracles`, `✅-born-in-chaos`, `✅-bosses-rise` e `✅-portable-hole`: Ignis fecha 8 ações sobrenaturais discretas `COUNTED_EXACT`; Artifacts 13.2.5 fecha 49 item entries como **+0 independente** sob deduplicação com Reliquified Artifacts; L_Ender's Cataclysm 3.33 fecha **24 ações sobrenaturais de item/equipamento + 3 rituais deliberados = +27 `COUNTED_EXACT`**; BetterEnd: New Dawn 21.0.34 fecha **48 Infusion Rituals + 1 Eternal Portal Ritual = +49 `COUNTED_EXACT`**; Weapons of Miracles 2.0.178 fecha **64/64 skill IDs** e promove **12 ações sobrenaturais `COUNTED_EXACT` + 1 `CONDITIONAL`**; Born in Chaos 1.7.6 fecha **17 ações sobrenaturais `COUNTED_EXACT`**; Bosses'Rise 2.1.2 fecha **8 ações sobrenaturais `COUNTED_EXACT`**; Portable Hole 21.1.0 fecha **1 ação mágica de travessia `COUNTED_EXACT`**; Legendary Monsters 2.2.2 fecha **22 ações sobrenaturais de jogador `COUNTED_EXACT`**; Alex's Caves Continued 1.0.10 fecha **8 ações sobrenaturais/mágicas de jogador `COUNTED_EXACT`**; Alex's Mobs Continued 2.1.13 fecha **1 ação de Transmutation Table `COUNTED_EXACT` + 2 raízes sobrenaturais `CONDITIONAL`** (Void Worm Summoning e Dimensional Carver); Ice And Fire: Dread Land 0.1.2 fecha **1 Dread Portal Activation `COUNTED_EXACT`**; Bosses of Mass Destruction 1.3.3 fecha **5 raízes sobrenaturais: 3 `COUNTED_EXACT` + 2 `CONDITIONAL`**; Deeper and Darker 1.4.1 entra como **⚠️ baseline público de 3 raízes / +0 strict**, porque GitHub/Modrinth/CurseForge oficiais compartilham bytes `b6094add...` que divergem do SHA-1 físico `83f7edd0...`; Protection Pixel 2.2.1 entra como **✅ `ZERO_SEMANTIC_TECH_GEAR` / +0 strict**, com SHA físico idêntico ao publisher e sem registry/resource mágico provider-owned; BetterNether: New Dawn 21.0.26 entra como **✅ `ZERO_SEMANTIC_WORLDGEN_BREWING_EQUIPMENT` / +0 strict**, com altares/portais reconciliados como worldgen/infra e nenhuma action registry mágica provider-owned. Grappling Hook Mod: Skybound 1.1 entra como **✅ `ZERO_SEMANTIC_TRAVERSAL_PHYSICS` / +0 strict**, com Ender Staff/forcefield/rocket/motor/magnet/hook reconciliados como travessia/física/equipamento; o Ender path é launch vetorial, não teleport spell. Dimensional Sable 1.0.5 entra como **✅ `ZERO_SEMANTIC_DIMENSION_TRANSFER_INFRA` / +0 strict**, com `/sable dimension_set` e `SubLevelWarper` reconciliados como ferramenta/API server-side de transferência estrutural entre dimensões, sem roster mágico player-owned. Create Teleporters Remastered 2.0.2b entra como **✅ `ZERO_SEMANTIC_TECH_TELEPORT_INFRA` / +0 strict**: Pocket Dimension Remote, TP Links, Custom/Quantum Portal e Entity/Item/Block Teleporters são transporte tecnológico Create, com zero registry/resource provider-owned de spell/ritual/glyph/ability/mana/arcane. Create: Chromatic Return 1.0.4 entra como **✅ `ZERO_SEMANTIC_ENCHANT_GEAR_INFRA` / +0 strict**: três Infused Books aplicam encantamentos provider-owned via off-hand+crouch, enquanto charms/Creative Flight são passivos/equipment; nenhuma spell/ritual/glyph/ability provider-owned é registrada. Create: Deep Dark 3.0.2 entra como **✅ `ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING` / +0 strict**: a varredura exata das 37 classes encontra zero player-action overrides; Echo armor é buff passivo por tick, Echo Sword é proc on-hit e Molten Echo é efeito ambiental. Create: Mechanical Spawner 1.3.2-6.0.10 entra como **✅ `ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA` / +0 strict**: 28 receitas de spawner são settlement de máquina Create movida por rotação/fluido; zero registry/path mágico e zero player-action override provider-owned. Create: Fantasizing Again 1.2.0-b3 entra como **✅ `ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_INFRA` / +0 strict**: Warden capture é conversão de progressão para Sculk Engine; Block Placer e Tree Cutter são ferramentas em lote; engines, Transporter, storage e Chromatic processing permanecem automação/processing Create sem roster mágico provider-owned. Create: More Features 0.1.3 entra como **✅ `ZERO_SEMANTIC_CREATE_AUTOMATION_VILLAGER_INFRA` / +0 strict**: professions, mechanisms, farms, boxes e devices permanecem economia/automação Create; os cinco overrides `useWithoutItem` auditados são menus/configuração, sem spell/ritual/ability roster. Create: Mobile Packages 0.7.7 entra como **✅ `ZERO_SEMANTIC_CREATE_LOGISTICS_INFRA` / +0 strict**: Bee Port, Robo Bee, Stock Ticker, Mobile Packager, requests e network membership são logística/pacotes; o único `mana` hit é `RoboManager`, sem mana/spell/ritual roster. Create: More Automation 0.5.2 entra como **✅ `ZERO_SEMANTIC_CREATE_RECIPE_AUTOMATION` / +0 strict**: o artefato exato tem 6 classes, 19 provider-data paths, zero paths mágicos e zero player-action overrides; seus 14 JSONs válidos são apenas recipes Create/vanilla de processing. Create: Ender Transmission 2.1.1 entra como **✅ `ZERO_SEMANTIC_REMOTE_TRANSFER_CHUNK_INFRA` / +0 strict**: Energy/Fluid/Item Transmitters são capability/network endpoints configurados por canal/senha, e o Chunk Loader é infraestrutura cinética de forced chunks; nenhum roster spell/ritual/ability provider-owned existe. Create Mechanical Companion 1.9 entra como **✅ `ZERO_SEMANTIC_MECHANICAL_COMPANION_INFRA` / +0 strict**: Mechanical Wolf Link é lifecycle Curios do companion; Quantum Drive, Tesla Tail, Booster Rocket, Mob Radar e Mounted Crossbow são módulos tecnológicos/AI, sem roster spell/ritual/ability provider-owned. Create: Enchantable Machinery 3.6.0 entra como **✅ `ZERO_SEMANTIC_MACHINE_ENCHANTMENT_APPLICATION` / +0 strict**: onze máquinas Create recebem variantes enchantable que persistem/leem encantamentos vanilla/modded existentes; não há enchantment registry próprio nem roster spell/ritual/glyph/ability. Creating Space 1.7.22 entra como **✅ `ZERO_SEMANTIC_SPACE_ROCKET_DIMENSION_TRANSPORT` / +0 strict**: seis dimensões/rotas espaciais, foguetes Create e `CustomTeleporter` implementam transporte aeroespacial player+veículo entre mundo/orbita/planeta; não há roster spell/ritual/glyph/ability provider-owned. Create: Dreams n' Desires 2.3a-BETA entra como **✅ `ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_CONTENT` / +0 strict**: Spud Sentry, Stirling/Smart Hopper, milkshakes, Gatling Breaker, handheld tools, Burst Package e dispenser mixin são automação/logística/alimento/ferramentas; nenhum roster mágico provider-owned existe. Ice And Fire: Dragon Care 1.3.1 entra como **✅ `ZERO_SEMANTIC_HUSBANDRY_SUPPORT` / +0 strict**: source oficial da linha 1.3.1 expõe husbandry/items/effects/tracking/loot/data/config; bond rewards são buffs passivos e syringe/shears/brush-QTE/Dragon Phone/Ash Sensor/tablets não formam roster mágico independente. Esse número já elimina a duplicata histórica `vampiric-ageing`/`vampiricageing` do mesmo mod id `vampiricageing`. É uma métrica estrutural do catálogo, não uma fração de cobertura: não substitui o denominador técnico cross-domain `PENDING REBASE` e não deve ser usado para calcular porcentagem semântica.

A métrica principal para o usuário é a cobertura de objetos mágicos semânticos — spells, glyphs/spell-parts, rituais/rites e equivalentes discretos. Seu denominador global ainda está em reconstrução; portanto nenhuma porcentagem final é declarada aqui. O mínimo estrito de **1496** foi posteriormente ampliado por Hexalia 1.3.7 (**+4**), Reliquified Ars Nouveau 0.8.1 (**+19**), Reliquified Artifacts 1.0.8 (**+52**), Reliquified Iron's Spells 'n Spellbooks 0.2.7 (**+25**), More Relics (**+61**), Ozymandias Sundries (**+2**), Mowzie's Mobs (**+10 strict**), Ice And Fire CE (**+8 strict**), Reliquified L_Ender's Cataclysm 0.1.1 (**+7 `COUNTED_EXACT`**), Waystones 21.1.45 (**+3 `COUNTED_SOURCE_PINNED`**) , StarbuncleMania 1.5.8 (**+2 `COUNTED_EXACT`**) e Cataclysm: Ignis Soulfires 1.8.0 (**+8 `COUNTED_EXACT`**), seguido por L_Ender's Cataclysm 3.33 (**+27 `COUNTED_EXACT`**) e BetterEnd: New Dawn 21.0.34 (**+49 `COUNTED_EXACT`**), seguido por Weapons of Miracles 2.0.178 (**+12 `COUNTED_EXACT` + 1 `CONDITIONAL`**) e Born in Chaos 1.7.6 (**+17 `COUNTED_EXACT`**), seguido por Bosses'Rise 2.1.2 (**+8 `COUNTED_EXACT`**) e Portable Hole 21.1.0 (**+1 `COUNTED_EXACT`**), seguido por Legendary Monsters 2.2.2 (**+22 `COUNTED_EXACT`**) e Alex's Caves Continued 1.0.10 (**+8 `COUNTED_EXACT`**), seguido por Alex's Mobs Continued 2.1.13 (**+1 `COUNTED_EXACT` + 2 `CONDITIONAL`**) e Ice And Fire: Dread Land 0.1.2 (**+1 `COUNTED_EXACT`**), seguido por Bosses of Mass Destruction 1.3.3 (**+3 `COUNTED_EXACT` + 2 `CONDITIONAL`**), seguido pela normalização semântica de Ars Morph 2.0.0 (**+8 `COUNTED_SOURCE_PINNED`**) e Woodwalkers SpellBooks 0.3.1-BETA (**+1 `COUNTED_SOURCE_PINNED`**), levando o mínimo estrito corrente a **1855**. Vampiric Ageing 1.4.21 mantém 9 ações provider-owned `CONDITIONAL` fora do strict até captura do config implantado. Ars 'n' Spells 3.3.4, Traveloptics, KubeJS bridges e os novos layers de UI/compat foram reclassificados sem outro delta estrito nesta rodada. Condições implantadas de Tombstone, Gaze rites, Not Enough Glyphs, Somake e outros providers continuam fail-closed onde configuração/reachability atual não está fechada, sem reabrir a completude de catálogo de pastas já ✅.

Phase 2BS adiciona T.O Magic n' Extras / `traveloptics` 4.4.0.1-1.21.1 ao conjunto **⚠️ parcial/condicionado**: o publisher file exato `6342780` fecha 33 identidades de spell registradas e exclui 32 roots de localization residuais, mas `traveloptics:blackout` permanece sem rota survival objeto-a-objeto fechada e o JAR exato apresenta risco estrutural em `TOLootModifiers` (`KeyLootModifier.CODEC` referenciado duas vezes; `UniversalLootModifier.CODEC` zero). Portanto Phase 2BS contribui **+0 strict**, não cria componente #67 naquele checkpoint e mantém **1344 / 66 de 100** historicamente. Phase 2BT posteriormente fecha o componente #67 com Vampire Spells Addon sem alterar o total semântico.

Capítulos e tabelas históricas abaixo continuam úteis para rastrear deltas, mas não prevalecem sobre o snapshot físico atual.

## Reconciliação física Magic — checkpoint 27/09 pré-normalização de prefixos

A autoridade física corrente é `neoforge-rpg-skilltree@1bb7c7d6e2e6878248b0c178bdae55e84697acd2`. Aplicando o critério ao **campo de categoria** da modlist, existem **84 linhas cuja categoria contém `Magic`**. O nome do mod não é usado como atalho de classificação.

Na reconciliação física de 27/09, antes da normalização posterior dos prefixos por completude de catálogo:

- **72 ✅ catalogados** com diretório Black Arcana correspondente;
- **12 ⚠️ parciais/condicionados** com diretório Black Arcana correspondente;
- **0 ❌** linhas físicas `Magic` sem classificação;
- **0 🟡** de implementação ativa;
- **0 ⛔** por ausência total de evidência.

Assim, naquele checkpoint, **84/84** linhas da categoria física `Magic` estavam mapeadas em Black Arcana (**72 ✅ + 12 ⚠️** pela classificação então vigente). Esse split é histórico e não deve ser reutilizado como contagem de prefixos atual; na correção de 30/09 a árvore canônica daquele checkpoint era **116 = 114 ✅ + 2 ⚠️**. O subtotal físico/categorial não é o denominador semântico global.

O delta contra o snapshot anterior de 67 linhas é **+17**. Onze dessas linhas já possuíam provider canônico e não geram nova contagem. Seis foram inicialmente materializadas como ⚠️: Reliquified L_Ender's Cataclysm, ShadowsZ, Simply Swords: Cataclysm, Simply More, Simply Swords e Waystones. Reliquified L_Ender's Cataclysm 0.1.1 agora está ✅ `COUNTED_EXACT 7`, e Waystones 21.1.45 está ✅ `COUNTED_SOURCE_PINNED 3`. Os outros quatro mantinham gates de strict/runtime abertos naquele checkpoint. A normalização de 29/09 promoveu seus diretórios a `✅-` quando o denominador e a materialização de catálogo ficaram fechados; esses gates de runtime/reachability continuam fail-closed sem reabrir a completude estrutural. ShadowsZ 1.1.9 já tem denominador exato de **10** ações semânticas, mas segue `+0 strict` até capturar `shadowszRestrictPowers` efetivo e `fusionEnabled`. Simply More Alpha 5 tem denominador corrente exato de **24** ações (10 API ativa + 13 legacy de uso direto + 1 Mimicry compartilhada), mas segue `+0 strict` até fechar Awakening/aquisição/Mimicry/config implantados. O delta estrito daquela reconciliation é **+10** e o mínimo global naquele checkpoint passa a **1687**. Ver [PHYSICAL-MAGIC-RECONCILIATION-2026-09-27.md](./PHYSICAL-MAGIC-RECONCILIATION-2026-09-27.md).

**Cross-domain note:** o subtotal físico `Magic` continua sem representar o universo global. Gaze é `✅` em completude de catálogo com um spell contado + 26 rites config-condicionais; Ender's Spells and Stuff: Requiem é ✅ com 53 ações strict; Reliquified Ars Nouveau, Reliquified Artifacts e Reliquified Iron's são ✅ com 19, 52 e 25 ability roots source-pinned; Reliquified L_Ender's Cataclysm 0.1.1 é ✅ com 7 ability roots exact-current; Iron's Spellbooks KubeJS permanece `⚠️` por inventário mutável de scripts; More Relics é ✅ com 61 ability roots exatas; Ozymandias Sundries é ✅ com 2 spells exatos; Mowzie's Mobs é `✅` em completude de catálogo com 10 poderes strict + 1 Tunneling config-condicional; Artifacts 13.2.5 é ✅ exact-current com 49 itens e +0 identidades independentes no stack atual, porque suas 48 owners/relic surfaces nomeadas são deduplicadas com Reliquified Artifacts; L_Ender's Cataclysm 3.33 é ✅ exact-current com **27** ações/rituais semânticos; BetterEnd: New Dawn 21.0.34 é ✅ exact-current com **49** rituais (48 Infusion + 1 Eternal Portal); Weapons of Miracles 2.0.178 é ✅ exact-current com **64 skill IDs totalmente dispositionados**, dos quais 12 ações sobrenaturais são strict e `flash_mutilation` permanece conditional; Born in Chaos 1.7.6 é ✅ exact-current com **17 ações sobrenaturais strict**; Bosses'Rise 2.1.2 é ✅ exact-current com **8 ações sobrenaturais strict**; Portable Hole 21.1.0 é ✅ exact-current com **1 ação mágica de travessia strict**; Legendary Monsters 2.2.2 é ✅ exact-current com **22 ações sobrenaturais strict**; Alex's Caves Continued 1.0.10 é ✅ exact-current com **8 ações sobrenaturais/mágicas strict**; Alex's Mobs Continued 2.1.13 é ✅ exact-current com **3 raízes sobrenaturais catalogadas: 1 strict + 2 conditional**; Ice And Fire: Dread Land 0.1.2 é ✅ exact-current com **1 ação sobrenatural de ativação dimensional strict**; Bosses of Mass Destruction 1.3.3 é ✅ exact-current com **5 raízes sobrenaturais catalogadas: 3 strict + 2 conditional**; Deeper and Darker 1.4.1 é ⚠️ com **3 raízes sobrenaturais no baseline público e +0 strict** por divergência física/publisher; Protection Pixel 2.2.1 é ✅ exact-current como **zero-semantic technological gear provider**; BetterNether: New Dawn 21.0.26 é ✅ exact-current como **zero-semantic worldgen/brewing/equipment provider**; Traveloptics permanece `⚠️` +0 strict pendente de fechamento exact-current. Spell Actionbar, Specs, Recolor e Immersive Portal estão ✅ catalogados com +0 identidades independentes; QA técnico/runtime permanece separado.
**Traveloptics current-physical override:** the current sibling dossier at `neoforge-rpg-skilltree@d1659e7abadcf03c386d17b1886a473dc6541195` confirms physical row #550 as `traveloptics-4.4.0.1-1.21.1.jar` / SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, corroborating the earlier Project Library fingerprint. The installed digest differs from the audited publisher alpha and known patch artifact, so Traveloptics remains a current **⚠️ `OTHER_VERIFIED` / +0 strict** provider blocker until its installed-byte registry and reachability are closed.

## Reconciliação física Magic — correção corrente 30/09

O sibling `neoforge-rpg-skilltree@d1659e7abadcf03c386d17b1886a473dc6541195`, auditado pela **pasta de categoria** e não por palavras no nome do mod, contém **97 dossiês físicos em categorias que incluem `Magic`**.

- antes do novo fechamento: **96/97** já possuíam provider correspondente;
- único ausente: StarbuncleMania 1.5.8;
- PR de evidência NON-MERGE #476: File `8778598` = SHA-1 físico `6af8bc4f9dc24c9ff4d49367ca37fd914822ceb6`, exatamente 2 glyphs Ars;
- PR durável #477: `✅-starbunclemania` materializado com 2/2 cards;
- estado após aquele fechamento: **97/97 mapeados**, árvore **116 = 114 ✅ + 2 ⚠️**, mínimo estrito **1689**.

O checkpoint 84/84 de 27/09 acima continua histórico e não é reescrito.

Fechamentos recentes relevantes:

- ✅ Acolyte 1.0.3 — usa spells do host Iron's; **+0** provider-owned spell identities.
- ✅ Companions! 1.3.4 — **9** Magic Books provider-owned, `COUNTED_SOURCE_PINNED`.
- ✅ Crystal Chronicles 0.1.3-alpha — **1** spell provider-owned (`prismatic_portal`), `COUNTED_SOURCE_PINNED`.
- ✅ Dungeon's Delight 1.5.1 — effects/enchantments/food support; **+0**.
- ✅ Fantasy Armor 1.2.4 — passive gear/MobEffect surface; **+0**.
- ✅ Enchantment Descriptions 21.1.11 — client tooltip presentation; **+0**.
- ✅ A Good Place 1.2.5 — client placement-animation presentation; **+0**.
- ✅ Create: Apokinetics 1.0.6 — exact physical/publisher hash match plus exact-binary bounded audit closes the machine-augmentation surface as **+0** spells/glyphs/rituals.
- ✅ Cataclysm: Spellbooks 1.1.14 — **59/59** current registrations retained; installed SHA-1 equals audited publisher File 8847070; no delta versus the previously counted 59.
- ✅ Ender's Spells and Stuff: Requiem 0.1.7 — **58** source-pinned current registered roots under the present DTE-enabled provider set; **53 `COUNTED_SOURCE_PINNED`** player-facing semantic actions after excluding 5 implementation/residual roots.
- ✅ Corail Tombstone 9.5.6 — Project Library physical SHA-1 equals audited File `8842741`; **10 `COUNTED_EXACT` actions** strict-counted (6 prayer + 4 Ritual Flute); 12 config-sensitive castable magic-item actions remain conditional.
- ✅ Relics 0.12.8 — exact physical/publisher artifact equality; **39 base abilities + 2 distinct synergies = 41 `COUNTED_EXACT` provider powers**; runtime/config QA remains fail-closed.
- ✅ Somake 1.0.9 — physical SHA-1 equals exact publisher File `8867079`; exact physical registry is **83 IDs**, gate topology is **67 unconditional + 16 optional**, current mod composition admits **83/83**, and all 83 current identities now have individual cards. Remaining blockers are effective deployed Iron's/provider config and survival reachability.
- ✅ Ars 'n' Spells 3.3.4 — **5** ritual identities retained; `COUNTED_RELEASE_BOUNDED`; current version delta **+0**.
- ✅ Hexalia 1.3.7 — **29 `COUNTED_SOURCE_PINNED`** semantic actions (23 Nature's Ritual + 6 Celestial Infusion), **+4** versus the prior line.
- ✅ Reliquified Ars Nouveau 0.8.1 — **19 `COUNTED_SOURCE_PINNED`** owner-scoped ability roots.
- ✅ Reliquified Artifacts 1.0.8 — **52 `COUNTED_SOURCE_PINNED`** owner-scoped ability roots.
- ✅ Reliquified Iron's Spells 'n Spellbooks 0.2.7 — **25 `COUNTED_SOURCE_PINNED`** provider-owned relic ability roots.
- ✅ Reliquified L_Ender's Cataclysm 0.1.1 — exact publisher/physical SHA-1 equality; **5 relic owners / 7 owner-scoped ability roots = +7 `COUNTED_EXACT`**; exact-current loot routes for all five owners closed by audit run `36416011761`; assembled/runtime QA remains separate.
- ✅ More Relics 1.7.7-forRelics-0.12.8-1.0 — exact physical/publisher File `8859015` equality; **29 owners / 61 owner-scoped ability roots = +61 `COUNTED_EXACT`**; exact builder/localization root sets agree, runtime/config/evolution QA remains separate.
- ✅ Ozymandias Sundries physical 0.0.5 / embedded 0.0.1 — exact File `6978561` hash match; **2 unconditional registered spells = +2 `COUNTED_EXACT`** (`levitate`, `lightning_warp`); unregistered class/localization residue excluded; runtime/config QA separate.
- ✅ Mowzie's Mobs 1.8.2 — exact File `7760267` hash match; **13 active player-ability slots**, reconciled to **10 strict `COUNTED_EXACT` powers + 1 `CONDITIONAL` Tunneling power**; `hit_boulder`/`backstab` technical-subaction slots and four inactive ids excluded.
- ✅ Ice And Fire Community Edition 2.1.2 — exact File `8757837`; **8 action families strict `COUNTED_EXACT` + 1 `CONDITIONAL`** after exact current-JAR reachability run `36323035696` plus current-pack NeoForge 21.1.250 runtime audit `36327488231`; only Ghost Sword deployed `phantasmalBladeAbility` remains open.
- ✅ Photon 2.2.6.a — exact physical/publisher File `8824095` equality; VFX/editor infrastructure only under the semantic metric; **+0 `ZERO_SEMANTIC_VFX_INFRA`**.
- ✅ RunicLib 5.0.7 — exact physical/publisher File `8188562` equality; reusable effect/attribute/damage/trade/services library surface only; **+0 `ZERO_SEMANTIC_LIBRARY_INFRA`**.
- ✅ Mowzie's Cataclysm 1.2.2 — exact File `8196282` equality; quatro Eyes de localização + recipes/tags, **+0 `ZERO_SEMANTIC_LOCATOR_BRIDGE`**.
- ✅ Pickable Orbs 1.21.1-1.0.0 — exact File `8660158` equality; oito definições de pickup e `OrbEntity`, **+0 `ZERO_SEMANTIC_PICKUP_EFFECT_INFRA`**.
- ✅ IronSable X Wind's Spellbooks 1.0.0 — exact File `8598265` equality; bridge física sobre Tornado/Almighty Push/Wind Blade/Aeropic já pertencentes a Wind's Spellbooks, **+0 `ZERO_SEMANTIC_EXISTING_SPELL_PHYSICS_BRIDGE`**.
- ✅ Iron's Gems 'n Jewelry 1.21.1-2.0.2 — exact File `8365016` equality; oito codecs `IAction` são payloads de proc/bônus de joia, não casts independentes, **+0 `ZERO_SEMANTIC_EQUIPMENT_PROC_FRAMEWORK`**.
- ✅ Integrated Villages 1.3.3+1.21.1-neoforge — exact File `8161672` equality; worldgen/structures/loot/data integration, **+0 `ZERO_SEMANTIC_WORLDGEN_INTEGRATION`**.
- ✅ StarbuncleMania 1.5.8 — physical SHA-1 equals exact File `8778598`; **2 unconditional Ars `AbstractEffect` glyphs = +2 `COUNTED_EXACT`**, with exact `ars_nouveau:glyph` recipes; runtime/config QA remains separate.
- ✅ Cataclysm: Ignis Soulfires 1.8.0 — physical SHA-1 exactly equals the audited official 1.8.0 artifact; four action-hosting items expose **8 discrete supernatural player actions = +8 `COUNTED_EXACT`**. Tool modes, armor/horse-armor passives and on-hit procs are cataloged but metric-excluded; runtime QA remains separate.
- ✅ Artifacts 13.2.5 — physical SHA-1 exactly equals CurseForge File `8791899`; exact `ModItems` closes **49 top-level item entries** and the item-ability component layer. Base items/components contribute **+0 independent semantic identities**; current named owner-scoped supernatural roots remain counted under Reliquified Artifacts 1.0.8, avoiding double counting.
- ✅ L_Ender's Cataclysm 3.33 — exact physical/publisher File `8706841` equality; exhaustive 67-item-class activation audit closes **24 discrete supernatural item/equipment actions + 3 deliberate boss-summoning rituals = +27 `COUNTED_EXACT`**. Ordinary weapon modes, pets/locators, passive gear, recipe machinery, proximity auto-spawn and generic boss-respawn infrastructure remain metric-excluded.
- ✅ BetterEnd: New Dawn 21.0.34 — exact physical/publisher File `8610367` equality; exact ritual audit closes **48 `betterend:infusion` recipe identities + 1 Eternal Portal Ritual = +49 `COUNTED_EXACT`**. Ordinary processing recipes, passive effects, portal aftermath and worldgen remain metric-excluded.
- ✅ Weapons of Miracles 2.0.178 — exact physical/publisher File `8829395` equality; exact `WOMSkills` closes 64 skill IDs. Semantic classification yields **12 `COUNTED_EXACT` supernatural actions + 1 `CONDITIONAL` Flash Mutilation**, while 51 martial/passive/mover/technological/support skills are metric-excluded.
- ✅ Born in Chaos 1.7.6 — exact physical/publisher File `8268280` equality; bounded item/procedure/acquisition audit closes **17 deliberate supernatural player actions = +17 `COUNTED_EXACT`**. Passive/on-hit/reactive equipment, ordinary consumables, primary projectile weapon modes, loot/debug surfaces and mob-native magic are metric-excluded.
- ✅ Bosses'Rise 2.1.2 — exact physical/publisher File `8123167` equality; bounded item/action/acquisition audit closes **8 deliberate supernatural player actions = +8 `COUNTED_EXACT`** across Skor Gauntlet, Sirok Gauntlet, Undying Tentacle, Helvar's Sword and Pirate Saber. Reactive/on-hit effects, primary collision/firing modes, roll, passive gear, boss-native attacks and decor/debug surfaces are metric-excluded.
- ✅ Portable Hole 21.1.0 — exact physical/publisher File `5733788` equality; exact `useOn` + temporary-hole restoration lifecycle closes **1 magical traversal action = +1 `COUNTED_EXACT`**. Stronghold Corridor loot closes acquisition; tunnel depth/blocks/restoration/feedback are parameters or consequences.
- ✅ Legendary Monsters 2.2.2 — exact physical/publisher File `8715533` equality; exhaustive interaction/acquisition audit plus exact Teleport Machine bytecode closes **22 deliberate supernatural player actions = +22 `COUNTED_EXACT`**. Primary firing/throwing, Withered Scythe charge, locators, passive/reactive gear, pet-management follow-ups and mob-native powers are metric-excluded.
- ✅ Alex's Caves Continued 1.0.10 — exact physical/publisher File `8856293` equality; exhaustive 42-item interaction audit plus exact Conversion Crucible/Beholder block seams closes **8 supernatural/magical player actions = +8 `COUNTED_EXACT`**. Primary weapon modes, technology, consumables, vehicles, setup items and mob-native rituals are metric-excluded.
- ✅ Alex's Mobs Continued 2.1.13 — exact physical/publisher File `8856498` equality; exhaustive 26-item + 11-block interaction audit closes **1 Item Transmutation `COUNTED_EXACT` + 2 `CONDITIONAL` supernatural roots** (Void Worm Summoning, Dimensional Carver). Capsid processing, weapons, locators, utilities, vehicles, consumables, pet/colony setup and environmental interactions are metric-excluded.
- ✅ Ice And Fire: Dread Land 0.1.2 — exact physical/publisher File `8708824` equality; exhaustive activation/progression audit closes **1 Dreadland Key → Dread Portal Activation `COUNTED_EXACT`**. Realm keys are progression-only and portal lifecycle/travel is downstream infrastructure.
- ✅ Bosses of Mass Destruction 1.3.3 — exact physical/publisher File `8448640` equality; exhaustive activation/summon/data audit closes **5 supernatural roots = 3 `COUNTED_EXACT` + 2 `CONDITIONAL`**. Lich Summoning and Charged Ender Pearl remain conditional on deployed Lich summon/reachability state.
- ⚠️ Deeper and Darker 1.4.1 — physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` differs from the byte-identical official GitHub/Modrinth/CurseForge 1.4.1 artifact (`b6094adde68bd4b909bc75c64901e1f3fb99ad8f`). Public baseline closes **3 supernatural roots** (Otherside Portal Activation, Sonorous Staff Sonic Boom, Soul Elytra Boost), but exact-current physical denominator remains open; **+0 strict**.
- ✅ Protection Pixel 2.2.1 — exact physical/publisher File `7549821` equality; complete provider audit finds technological Cannon/Hook/Thruster/Wing/armor/device mechanics but no provider-owned spell/ritual/glyph/mana/arcane surface; **`ZERO_SEMANTIC_TECH_GEAR` / +0 strict**.
- ✅ BetterNether: New Dawn 21.0.26 — exact physical/publisher File `8615740` equality; complete class/resource audit reconciles altar/portal/pedestal hits as worldgen/portal infrastructure and brewing/equipment as processing/gear; **`ZERO_SEMANTIC_WORLDGEN_BREWING_EQUIPMENT` / +0 strict**.
- ✅ Grappling Hook Mod: Skybound 1.1 — exact physical/publisher File `8176552` equality; exact action/data audit closes Ender Staff, forcefield, rocket, motor, magnet, dual-hook, rope/hook and Long Fall Boots as traversal/physics/equipment; **`ZERO_SEMANTIC_TRAVERSAL_PHYSICS` / +0 strict**.
- ✅ Dimensional Sable 1.0.5 — exact physical/Modrinth `l9l5j4Zh` equality; exact 38-entry/21-class artifact exposes `/sable dimension_set` plus sublevel transfer internals and zero provider data JSON/spell/ritual/glyph/player-ability roster; **`ZERO_SEMANTIC_DIMENSION_TRANSFER_INFRA` / +0 strict**.
- ✅ Create: Deep Dark 3.0.2 — exact physical/publisher File `7624342` equality; exhaustive 37-class action scan closes zero player-invoked semantic magic roots. Echo armor tick buffs, Echo Sword damage-event debuffs and Molten Echo collision effects are passive/reactive/environmental; **`ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING` / +0 strict**.
- ✅ Create: Mechanical Spawner 1.3.2-6.0.10 — exact physical/publisher File `8418593` equality; 52-class + 97-recipe audit closes 28 spawner recipes as kinetic/data-driven mob-generation infrastructure, with zero provider player-action magic roots; **`ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA` / +0 strict**.
- ✅ Create: Fantasizing Again 1.2.0-b3 — exact physical/publisher File `8585611` equality; 175-class / 105-provider-data audit closes Warden conversion, Block Placer, Tree Cutter, engines, Transporter, storage and Chromatic processing as Create automation/tools infrastructure with zero provider-owned spell/ritual/glyph/summon roster; **`ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_INFRA` / +0 strict**.
- ✅ Create: More Features 0.1.3 — exact physical/publisher File `8325313` equality; 145-class / 108-provider-data audit closes professions, mechanisms, storage boxes/devices and recipes as Create/villager automation with zero provider-owned spell/ritual/glyph/ability/summon/portal roster; **`ZERO_SEMANTIC_CREATE_AUTOMATION_VILLAGER_INFRA` / +0 strict**.
- ✅ Create: Mobile Packages 0.7.7 — exact physical/publisher File `8502329` equality; 130-class / 13-provider-data audit closes Bee Port, Robo Bee, Portable Stock Ticker, Mobile Packager and network/package delivery as Create logistics infrastructure with zero provider-owned spell/ritual/glyph/ability/teleport/portal roster; **`ZERO_SEMANTIC_CREATE_LOGISTICS_INFRA` / +0 strict**.
- ✅ Ice And Fire: Dragon Care 1.3.1 — current physical identity + official version-declared 1.21.1 source; husbandry/care/items/effects/tracking/loot/data/config support with passive bond buffs and no provider-owned spell/glyph/ritual/rite/action roster; **`ZERO_SEMANTIC_HUSBANDRY_SUPPORT` / +0 strict**; binary/runtime QA separate.
- ✅ Pufferfish's Skills 0.19.0 — exact physical/publisher File `8792775` equality; base JAR has zero `data/puffish_skills/**` entries and zero packaged skill-tree JSONs, while built-in rewards are generic progression primitives; **`ZERO_SEMANTIC_SKILL_TREE_FRAMEWORK` / +0 strict**; deployed datapack/addon content remains separately owned and runtime-QA-gated.
- ✅ Pufferfish's Attributes 0.8.3 — exact physical/publisher File `8610466` equality; 42 exact attribute IDs form a dynamic stat layer with no provider-owned spell/ritual/action roster; **`ZERO_SEMANTIC_ATTRIBUTE_FRAMEWORK` / +0 strict**; consumer stacking/runtime QA remains separate.
- ✅ Pufferfish's Unofficial Additions 2.2.8 — exact physical/publisher File `7389968` equality; three XP sources + one configurable effect reward + Iron's spell/school observers, with no provider spell registry or packaged tree JSON; **`ZERO_SEMANTIC_SKILL_XP_REWARD_BRIDGE` / +0 strict**.
- ✅ Create: More Automation 0.5.2 — exact physical/publisher Modrinth `en1TN4J7` equality; 73-entry / 6-class / 19-data-path audit has zero spell/magic/ritual/ability/mana/arcane/glyph/summon/soul/teleport/portal/enchant/curse paths and zero player-action overrides; 14 valid JSONs are Create/vanilla processing recipes; **`ZERO_SEMANTIC_CREATE_RECIPE_AUTOMATION` / +0 strict**.
- ✅ Create: Ender Transmission 2.1.1-1.21.1 — exact physical/publisher Modrinth `eI9pk5JC` equality; 107-entry / 32-class / 14-data-path audit closes transmitter UI/config, item/fluid/energy capability networks and kinetic chunk forcing with zero provider-owned magic roster; **`ZERO_SEMANTIC_REMOTE_TRANSFER_CHUNK_INFRA` / +0 strict**.
- ✅ Create Mechanical Companion 1.9 — exact physical/publisher Modrinth `6ZRWru4y` equality; 198-entry / 54-class / 41-data-path audit closes Curios Mechanical Wolf lifecycle plus Quantum Drive/Tesla Tail/Booster/Radar/Crossbow module surfaces with zero provider-owned magic roster; **`ZERO_SEMANTIC_MECHANICAL_COMPANION_INFRA` / +0 strict**.
- ✅ Create: Enchantable Machinery 3.6.0 — exact physical/publisher Modrinth `Cw5k6c0a` equality; 282-entry / 142-class / 17-data-path audit closes 11 enchantable Create machine mappings, zero provider-owned enchantment definitions and zero provider-owned spell/ritual/glyph/ability roster; **`ZERO_SEMANTIC_MACHINE_ENCHANTMENT_APPLICATION` / +0 strict**.
- ✅ Creating Space 1.7.22 — exact physical/publisher CurseForge File `8882869` equality; 1,986-entry / 354-class / 690-data-path audit closes rocket/planet/dimension transport surfaces, six dimensions and six rocket-accessible-dimension definitions with zero provider-owned spell/ritual/glyph/ability roster; **`ZERO_SEMANTIC_SPACE_ROCKET_DIMENSION_TRANSPORT` / +0 strict**.
- ✅ Create: Dreams n' Desires 2.3a-BETA — exact physical/publisher Modrinth `bqMxf6Ua` equality; 1,363-entry / 227-class / 457-data-path audit closes eight player-interaction classes as automation/logistics/tools/food and zero provider-owned spell/ritual/glyph/ability roster; **`ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_CONTENT` / +0 strict**.
- ✅ Ars Morph 2.0.0 — release-aligned exact-version source closes **1 Morph glyph + 7 Identity2 ability adapter roots = +8 `COUNTED_SOURCE_PINNED`**; internal Ars resolver/effect descendants are deduplicated and installed-host runtime QA remains separate.
- ✅ Woodwalkers SpellBooks 0.3.1-BETA — exact-version source closes exactly **1 active Iron's spell registration = +1 `COUNTED_SOURCE_PINNED`**, `woodwalkers_spellbooks:shapeshifting`; Woodwalkers remains morph-state authority.
- ✅ Vampiric Ageing 1.4.21 — exact source/action catalog closes **9 provider-owned supernatural actions**, all retained as `CONDITIONAL / +0 strict` because deployed provider configuration is not captured; source defaults are not substituted.
- ⚠️ Traveloptics 4.4.0.1-1.21.1 — current physical provider; installed artifact is `OTHER_VERIFIED`; publisher-baseline 33 spells are not promoted as exact-current; **+0 strict**.
- ⚠️ Iron's Spellbooks KubeJS 4.0.3 — **+0 fixed built-in identities**; current pack script-defined spell/school inventory remains open.
- ✅ KubeJS Ars Nouveau 1.3.2 — provider-owned semantic denominator closed at **0 spell IDs + 0 glyph IDs**; uncaptured current scripts remain a recipe/reachability/economy gate, not an open provider-owned semantic denominator.
- ✅ Immersive Portal Iron's bridge, Iron's Recolor, Spell Actionbar and Specs — semantic catalogs closed at **+0 independent identities**; runtime/interop QA remains separate and fail-closed.

O mínimo semântico estrito corrente é **1855**. O denominador semântico final e o denominador técnico cross-domain continuam abertos; não publicar percentual global.

## Provider freshness override — Ars Controle 1.6.16

O sibling revalidado em `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` confirma a posição física **#41** como `ars_controle-1.21.1-1.6.16.jar`, mod id `ars_controle`, runtime `1.21.1-1.6.16` e SHA-1 físico `795567371450debec83fe634fd0114c295f7da5a`.

O source oficial exato `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0` declara `mod_version=1.6.16` e Ars Nouveau `5.13.1.1403`. A comparação contra o checkpoint canônico anterior `ecbb83ba512bc9ca7a025556fb9c62dbd32b6430` (1.6.15) contém seis commits; o único Java de gameplay alterado é `WarpingSpellPrismBlock.java`. O arquivo autoritativo de registro `ACRegistry.java` permanece exatamente no mesmo Git blob `b38959053740605768a8945ed40c012c6bef5953` nos dois checkpoints.

Consequência naquele checkpoint: **✅ Ars Controle 1.6.16 — 9/9 spell parts source-pinned permanecem catalogados; +0 delta semântico; o mínimo estrito então continuava em 1382**. As correções do Warping Spell Prism, mixins, Source settlement, cross-dimension, persistência e comportamento assembled-pack continuam runtime QA fail-closed.

## Provider freshness override — Hazen N Stuff 1.4.0.14

O sibling revalidado em `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` confirma `hazennstuff-1.4.0.14.jar`, mod id `hazennstuff`, runtime `1.4.0.14` e SHA-1 físico `3be20bacb44c1923348ab6f61b685eec6aacfdcd`.

O source oficial release-correlated `Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce` declara 1.4.0.14 e fecha **38 active spell registrations**. O `en_us` do mesmo pin contém 41 root spell keys; `brimstone_hellblast` e `supernova` ficam excluídos por não possuírem active registry entry, e `reign_of_tyros` fica excluído porque sua linha `registerSpell(...)` está comentada no pin exato apesar da classe/localization existente. O registry source-pinned não contém branch de registration por config/mod-presence em torno das 38 identidades ativas. Os três `canBeCraftedBy` especiais — Golden Shower, Night's Edge Strike e Scorching Slash — possuem acquisition path provider-owned no mesmo release; custom focus routes Cosmic/Radiance/Shadow/Hydro também foram reconciliadas com HazentouveLib 1.0.9/Ace's Spell Utils.

Consequência naquele checkpoint: **✅ Hazen N Stuff — 38/38 source-pinned spell registrations catalogadas; +38 semantic objects; runtime QA fail-closed**. O mínimo semântico reconstruível então passou para **1382**. Como Hazen não estava no denominador técnico histórico de 100 componentes, o denominador técnico global fica explicitamente `PENDING REBASE`.

## Provider freshness override — Create: Wizardry 1.21.1-0.5.1-pre1

O sibling atual em `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` reconcilia Create: Wizardry na posição física **#166** como `create_wizardry-1.21.1-0.5.1-pre1.jar`, mod id `create_wizardry`, runtime `1.21.1-0.5.1-pre1`.

O source oficial version-correlated `TTZPlayz/Create-Wizardry@9c4e53aad0ee9477187487443b597b77ef06f323` declara a mesma versão. A auditoria estrutural encontra 75 Java files, 328 resources e **zero** superfície provider-owned de spell registry/resource: sem `registerSpell`, `SpellRegistry`, `DeferredRegister<AbstractSpell>`, `Registries.SPELL`, `SPELLS.register` ou namespace `spell.create_wizardry`. Blaze Caster e Mana Siphon consomem `SpellData`/`AbstractSpell` do Iron's e alteram/automatizam o pipeline host; isso não transfere ownership dos spells. A blacklist explícita do Blaze Caster contém 31 host spell path names e também não cria identidades novas.

Consequência naquele checkpoint: **✅ Create: Wizardry — componente mágico/cross-domain catalogado como `ZERO_SEMANTIC_HOST_SPELL_AUTOMATION`; +0 semantic objects; runtime QA fail-closed**. O mínimo estrito então permanecia em **1382**. Como o denominador técnico global está em rebase, nenhum novo percentual/fração técnica é publicado.

## Provider freshness override — Iron's Apothic 2.2.2

O sibling certificado em `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` preserva a linha física **#339** como `irons_apothic-2.2.2.jar`, mod id `irons_apothic`, runtime `2.2.2`. O dossiê físico atual não preserva digest independente do JAR, portanto igualdade binária não é inferida.

O source oficial exato `muon-rw/Apotheosis-Irons-Spells@c5d501219cc9bbbfb8c69acc08bebac76983d1c1` declara `mod_version=2.2.2`. Nesse pin, o provider registra **7 codecs próprios de affix** no registry de Apotheosis, possui **140 definições JSON de affix**, das quais **48** ficam explicitamente em superfícies `spell`/`imbued`, e **24 definições de gem**. `SpellTriggerAffix` resolve spells pelo `SpellRegistry` de Iron's e `SpellCastUtil` executa o `AbstractSpell` externo pelo pipeline de casting do host; não há registry próprio de spell do provider no source exato.

Consequência naquele checkpoint: **✅ Iron's Apothic 2.2.2 — bridge mágico/source-pinned catalogado, 48 spell-oriented affix definitions tratadas como triggers/suporte sobre spells externos, 0 provider-owned spell registrations, +0 semantic objects**. O mínimo estrito então permanecia em **1382**. O denominador técnico global continua `PENDING REBASE`; não é publicado novo percentual. Compatibilidade assembled-pack com Iron's 3.16.3, Apotheosis 8.8.0, optional schools, cooldown/target settlement e recursão cross-mod permanecem runtime QA fail-closed.

## Provider freshness override — Somake 1.0.9

Current sibling authority rechecked at `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` retains the certified physical dossier `PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + Armor, Tools, and Weapons + Magic/✅-somake v1.0.9.md` for `somakespells-1.0.9-1.21.1.jar` / mod id `somakespells` / runtime `1.0.9`.

The current Black Arcana evidence is materially beyond the earlier resource-only checkpoint:

- physical Project Library SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- exact publisher CurseForge File `8867079` SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- physical ↔ publisher artifact equality: **closed**;
- exact physical/release registry: **83 unique spell IDs**;
- exact registration topology: **67 unconditional + 16 unique optional-provider-gated**;
- exact optional gates: 3 Mowzie's-only, 2 ISS-only, 9 Legendary-Monsters-only and 2 nested ISS+Legendary;
- all three required registration-gate providers are physically present in the current pack, so Somake's own registration predicates admit **83/83** declared spell IDs;
- exact provider code default for `enableSpellLockSystem`: **false**;
- all **83 current identities** are materialized individually through `MAGIC-CARDS-1.0.9.md` and `registry-1.0.9/`.

This closes physical identity, exact registry identity, object-level optional-registration predicates and current registration composition. The runtime probe is no longer needed merely to discover which Somake IDs register in this pack.

Somake nevertheless remains **⚠️ partial / conditioned / +0 strict**. The unresolved catalog gates are narrower:

- effective deployed Iron's per-spell/global/datapack `enabled`;
- effective deployed Iron's `allow_crafting`, especially around the seven provider `allowCrafting()` overrides;
- effective deployed Somake `enableSpellLockSystem` COMMON value;
- object-level or bounded-set survival acquisition/reachability, including Aqua/focus paths;
- assembled-pack progression/runtime settlement remains separate QA.

No source default is promoted into a deployed-state fact. The historical 1.0.8-fix 67-ID audit remains historical only and must not be reused as current authority.

Consequence: Somake remains **⚠️ partial/conditioned / +0 strict**, but **registry discovery and current composition are no longer blockers**.

## Provider freshness override — Not Enough Glyphs 4.6.2

A modlist sibling atual, verificada em `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7`, identifica `not_enough_glyphs-1.21.1-4.6.2.jar` / mod id `not_enough_glyphs` / runtime `4.6.2` como a linha física instalada. Isso supersede apenas a antiga afirmação física 4.6.1; o snapshot global de 595 entradas acima continua sendo checkpoint histórico e não é silenciosamente renomeado.

A release oficial atual é CurseForge project/file `1023517 / 8880291`. O audit exato retido fecha SHA-1 de release `32eea2c478a346ee7499f6a0db156241116f73e9`, SHA-256 `efd90f8ed292fd1b6b08fc33330f4344b70ed1661ffbe3684a64b1b485856c12` e Sauce JarJar `0.0.50.97`. O hash independente do JAR físico instalado ainda não está preservado, então igualdade byte-for-byte com a release não é inventada.

O source oficial `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` declara `mod_version=4.6.2`. Comparado ao pin histórico 4.6.1, `ArsNouveauRegistry.java` permanece blob `28c2007999ec6e534b8c5cd2c90b012c81072cff` e `EffectMomentum.java` permanece blob `7dd4f7ebe06cbadd282fddb1a6ca603013d2af2a`, ainda com `isEnabled() = false`. O conjunto físico atual mantém Ars Elemental e Ars Controle presentes, enquanto Too Many Glyphs, Ars Omega e Ars Trinkets permanecem ausentes da modlist. Portanto a matriz corrente continua **40 registrations / 39 source-enabled / Momentum source-disabled**.

Not Enough Glyphs continua **⚠️ parcial/condicionado / +0 strict / sem ponto de componente**. O blocker não é mais versão/registry; é exclusivamente a ausência dos valores efetivos de SERVER config `[general].enabled` para os 39 candidatos. No checkpoint histórico em que esta seção foi fechada, os totais eram **1344** objetos semânticos mínimos e **68/100** componentes técnicos; os totais correntes acima prevalecem.

## Freshness histórica 2026-09-07

O checkpoint de 2026-09-07 registrou updates como:

- Apotheosis `8.7.0 → 8.8.0`;
- Ars 'n' Spells `3.2.4 → 3.3.0` naquele snapshot; o runtime físico atual está em `3.3.4`;
- GTBC's SpellLib `2.1.0 → 2.2.0` (`2.2.0-1.21.1` no runtime);
- Vampirism `1.10.12 → 1.10.13`.

Esse bloco é histórico. Versões correntes devem sempre ser relidas da modlist física antes de qualquer nova auditoria.

A presença/update de um JAR não revalida automaticamente hook, API ou compatibilidade já assumidos por auditorias anteriores.

## Delta histórico do snapshot 2026-09-06

O snapshot anterior continha 607 entradas top-level. O guia mágico anterior catalogava 94 JARs/providers relevantes; esses números são históricos e não substituem a reconciliação física atual.

| Provider | Guia anterior | Snapshot 2026-09-06 |
|---|---:|---:|
| Ace's Spell Utils | 1.2.7.1 | 1.2.7.2 |
| Apothic Enchanting | 1.6.1 | 1.6.2 |
| Ars 'n' Spells | 3.2.2 | 3.2.4 |
| Cataclysm: Spellbooks | 1.1.12 | 1.1.13 |
| Discerning The Eldritch | 1.4.3 | 1.4.4 |
| Iron's Spells: Recolor | 1.2.5 | 1.3.2 |
| Monsters & Spellbooks | 0.0.16.2 / metadata histórico 0.0.14 | 0.0.16.3 |
| Starbunclemania | 1.5.7 | 1.5.8 |

## Classificação obrigatória

Cada JAR mágico deve ser classificado antes da extração spell-by-spell:

1. `SPELL_PROVIDER` — possui spells/glyphs/poderes jogáveis que precisam de catálogo individual.
2. `RITUAL_RESOURCE_PROVIDER` — fornece ritos, recursos, fluidos, espíritos, toxinas, plantas, altares ou progressão mágica reutilizável.
3. `BRIDGE_COMPAT` — integra providers; não deve ser contado como escola paralela salvo se realmente adicionar spell próprio.
4. `LIBRARY_INFRA` — biblioteca/API/VFX/UI; documentar capabilities, não inventar spells.
5. `GEAR_LOOT_SUPPORT` — gear, loot ou atributos mágicos sem catálogo próprio de spells.
6. `MIXED` — contém mais de uma das categorias; decompor por feature.

## Providers prioritários para deduplicação

### Iron's Spells e grandes addons

- Iron's Spells 'n Spellbooks;
- Cataclysm: Spellbooks;
- Monsters & Spellbooks;
- T.O Magic n' Extras — **histórico Phase 2BS; ausente da modlist física atual**;
- Hazen N Stuff;
- Create: Wizardry;
- ISS: Magic From The East;
- Asterism Arcanum;
- Leyline Spellbooks;
- Paladin Spells;
- Somake;
- Discerning The Eldritch;
- Dreamless Spells;
- Fire's Ender Expansion;
- GTBC's Geomancy Plus;
- Farmer's Spell 'n Spellbooks;
- SnackPirate's Aeromancy Additions;
- Apprentice's Codex;
- demais addons Iron's presentes na modlist.

### Ars Nouveau

Ars Nouveau e seus addons devem ser catalogados em nível de glyph/form/augment e também em combinações canônicas somente quando o pack tratar a combinação como poder nomeado. Não criar uma página para cada permutação possível.

### Sistemas externos de magia/ritual/recurso

- Goety;
- Malum;
- Eidolon: Repraised;
- Hexalia;
- Toxony;
- Vampirism/Bloodlines e bridges mágicas;
- demais providers ocultistas/alquímicos presentes.

### Familiars e infraestrutura relacionada

A modlist física atual inclui, entre outros, `familiarslib-1.21.1-1.7.1.jar` e `alshanex_familiars-1.21.1_v4.0.3.jar`. São componentes distintos e não compartilham automaticamente ownership semântico:

- FamiliarsLib foi fechado na Phase 2AX como `LIBRARY_INFRA`/framework de familiar, com **0** novas magias semânticas independentes;
- Alshanex's Familiars é consumidor/conteúdo concreto; Phase 2BD fecha a linha 4.0.3 em **7 spells próprios + 11 rituais próprios = 18 objetos semânticos**, usando o JAR exato hash-matched; runtime QA e seam de ownership continuam separados;
- documentação histórica que associa Sound School a Alshanex não deve prevalecer sobre a release 4.0, que moveu esse conteúdo para Tunes n' Tomes;
- familiar ownership para Borrowed Sight continua exigindo seam provider-native verificável e revalidação server-side.

## Mobstein 5.4.4 — canonical zero-semantic component #68

A PR #318 fechou o catálogo Mobstein contra o JAR físico `mobstein-5.4.4-neoforge-1.21.1.jar`, SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29`, usando a evidência resource-only clean-room do audit temporário #316 sem decompilação de bytecode. A disposição semântica é `ZERO_SEMANTIC_ACTIONS`: syringes documentadas permanecem interações de item e os keybinds action-like auditados são controles de entidade/montaria, não identidades mágicas independentes.

A PR #318 foi squash-mergeada como `main@73cd692ac0f6aa96ee1a6c422f09d0fcc648c8f4`. O exact merge SHA passou Black Arcana CI **#3217** / run `35293505012` completo, incluindo o job `stage05_qa_companion_smoke`. Com merge durável e gate pós-merge satisfeitos, esta reconciliação promove `mobstein` a componente **#68 / 68/100** sem alterar o mínimo semântico de **1344**.

Isso não é runtime/API PASS. Hooks suportados, persistência, integração Sable e qualquer adapter Black Arcana↔Mobstein permanecem fail-closed; Mobstein mantém autoridade sobre sua própria mecânica.

## Phase 2BT — Vampire Spells Addon 0.0.9 — canonical zero-semantic component #67

A PR #239 fechou `vampire_spells_addon-neoforge-1.21.1-0.0.9.jar` contra a release oficial `1.21.1-0.0.9` e o source target exato `xsharov/VampireSpellsAddon@2d36e94e67611a316b7311b11e4574b499025580`. O audit prova que os identificadores mágicos usados pelo addon pertencem ao namespace `irons_spellbooks`, que o entrypoint instala listeners/bridges sobre Iron's e Vampirism e que não existe registrar provider-owned de spell, school, ritual ou ação mágica equivalente.

O estado semântico é `ZERO_BRIDGE_INFRA`: **+0** objetos. A release/source audit foi mergeada na PR #239 como `main@1c5091807a8773d378c34ffac2e737b5f08b545c`; o exact merge SHA passou Black Arcana CI run `34795795283` completo. Com a evidência durável e o post-merge gate já satisfeitos, esta reconciliação compartilhada promove `vampire_spells_addon` a componente **#67 / 67/100** sem alterar o mínimo semântico de **1344**.

Isso não é runtime PASS. Igualdade byte-for-byte do JAR físico, resolução reflexiva assembled-pack, ordem de mixins/events, serverconfig efetivo, settlement de blood/mana/damage/cooldown e coexistência com outros bridges permanecem fail-closed. Iron's/Vampirism continuam authorities dos spells/recursos modificados; Black Arcana não cria identidade ou settlement duplicado.

## Phase 2BS — T.O Magic n' Extras / Traveloptics 4.4.0.1-1.21.1 — historical publisher checkpoint with current-physical override

O exact publisher release file `6342780` fecha **33** registrations `traveloptics:<id>` no `TOSpells`, com 33 field→classe→ID mappings e zero branches no initializer. Outros **32** root localization spell IDs existem no alpha, mas não estão registrados e são excluídos. `AbstractUniqueSpell.allowCrafting=false`; nove dos dez Unique registrados possuem rotas de loot estruturadas, enquanto `traveloptics:blackout` não possui referência estruturada nem referência provider-owned fora do registry encontrada pelo audit.

O audit de risco também prova que `TOLootModifiers` contém os nomes `key_loot` e `universal_loot`, mas referencia `KeyLootModifier.CODEC` duas vezes e `UniversalLootModifier.CODEC` zero vezes. Um patch de terceiro descreve esse mesmo wiring como defeito de startup, porém Black Arcana não declara crash reproduzido. Durable PR #228 mergeou o publisher-artifact checkpoint em `main@0bd1c04460e63a03b6b484b785247e75f6e44178`; post-merge CI #2682 / run `34741699505` passou e publicou artifact `10311724779` (`sha256:05e28f0dc516e3b51bbd9016a37816cd1854e45caeaa71745189b20297ae3813`). Estado naquele checkpoint: **⚠️ parcial/condicionado / +0 strict / componente aberto**. Evidência física posterior volta a confirmar o provider instalado, porém com SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, diferente do publisher alpha auditado e do patch conhecido; por isso a fila atual mantém Traveloptics como **⚠️ current physical / `OTHER_VERIFIED` / +0 strict**, sem projetar os 33 IDs do publisher como registry exato do JAR instalado.

## Checkpoint GTBC's Geomancy Plus — Phase 2BR canonical

O provider físico `gtbcs_geomancy_plus` está na linha `1.1.0-1.21.1`. O exato publisher release file `7041615` foi inspecionado clean-room: `GGSpells` fecha **12** registrations sem branch/config/mod-gate no registry — **10 Geo + 2 Holy** — e `EarthshatterSpell` permanece excluído por não estar registrado. Como o repositório não preserva um hash independente do JAR físico local, o estado semântico correto é `COUNTED_RELEASE_BOUNDED`, não `COUNTED_EXACT`.

A reachability Geo foi fechada em nível de catálogo por evidência específica: `mowziesmobs:bluff_rod -> #gtbcs_geomancy_plus:geo_focus -> irons_spellbooks:school_focus`, e o audit NON-MERGE `7596802cefa164f0cc61c391b1fae09d12115e7d` / run `34738729721` prova que os dez Geo registrados são subclasses diretas de Iron's `AbstractSpell` sem overrides de `allowCrafting`, `isEnabled` ou `canBeCraftedBy`. Os dois Holy possuem identifiers de loot Umvuthi no artefato exato e o changelog do file 1.1.0 identifica essa aquisição. Generic host config, runtime/protection, Mowzie integration, loot live e multiplayer continuam fail-closed.

PR #226 foi squash-mergeada como `main@4ab4ad990d453938e67f3d2b7cfa878bbe031ef0`; o exact merge SHA passou Black Arcana CI #2654 / run `34738972649` completo e publicou QA artifact `10311522907` (`sha256:c815f684a7a6dec192dd995bb6fbd6784c35faa0b0d21ae39bb9de89b93cec16`). Esta reconciliação promove `gtbcs_geomancy_plus` a componente **#66 / 66/100** e eleva o mínimo estrito de **1332 para 1344**.

## Checkpoint Ars Nouveau: Two-Way Portals — Phase 2BQ canonical

O artefato físico `ars_two_way_portals-2.0.0.jar` / SHA-1 `233846fc30667893c5f36a719da576d5eed43f5c` foi materializado do CurseForge file exato `8515817` em NON-MERGE PR #222 e hash-matched contra a autoridade física. O audit exato fecha **25 classes**, **2 provider items**, **3 recipes**, **7 mixins common required** e dependências exatas NeoForge/Ars/`immersive_portals_core`; não há `AbstractSpell`, `AbstractGlyph`, `SpellRegistry`, `registerSpell`, Ritual, Rite ou Ability nas superfícies estruturais auditadas, nem resources semânticos desses tipos. A classificação é `ZERO_SEMANTIC_PORTAL_INFRA` / `BRIDGE_COMPAT`, com **+0** objetos semânticos.

PR #223 foi squash-mergeada como `main@bc5428b5855e4d5821d5bd901fb591a62ecf3cbe`; o exact merge SHA passou Black Arcana CI #2622 / run `34735586680`, incluindo unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests, dedicated-server smoke e QA artifact `10310957237` (`sha256:de930eaba7f0f5730810747050ec500b4d72ed793cfbdce0c8603e3af8d8cc9d`). Esta reconciliação compartilhada promove `ars_two_way_portals` a componente **#65 / 65/100** sem alterar o mínimo semântico de **1332**. Runtime de portal, configs efetivas, mixin application e interop assembled-host permanecem fail-closed.

## Checkpoint SnackPirate's Aeromancy Additions — Phase 2BP canonical

O artefato físico `aero_additions-1.2.8.jar` / SHA-1 `dee32c9fa84d6e39846608f8f77591ea56f` / CurseForge hash `3079423735` foi reconciliado com o source oficial exato `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, árvore `fcee08e613fbfa030f034268a0240c8693ab7f45` completa. O provider é `MIXED`: possui escola Wind, exatamente **10** registrations `AbstractSpell` ativas e conteúdo adicional de efeitos/entidades/gear/aquisição. As dez identidades entram como **+10 `COUNTED_SOURCE_PINNED`**, elevando o mínimo estrito de **1322 para 1332**.

As identidades ativas são `wind_charge`, `updraft`, `airstep`, `asphyxiate`, `feather_fall`, `wind_shield`, `airblast`, `wind_blade`, `flush` e `dash`. Tornado, Thunderclap, Summon Breeze, Telelink e Shapeshift não entram: suas linhas `registerSpell(...)` estão comentadas no pin auditado. A escola Wind é taxonomia/suporte e não cria uma décima primeira magia.

A rota de aquisição foi fechada em nível de catálogo pelo focus Wind baseado em `minecraft:breeze_rod` e pelo contrato Scroll Forge da linha pública Iron's 3.16.3. O provider também adiciona suporte de Breeze Rod ao normal vault de Trial Chambers por global loot modifier. Updraft Tome e Wind Sword incorporam spells já contados e não criam novas identidades semânticas.

PR #219 HEAD reconciliado `6e39a01273b77ba8accf85d49647b6ceff840e8a` passou CI #2577 / run `34730598682`; squash evidence merge `main@84e9635b446b605140ab349fa2edc51f3462d518` passou exact-SHA post-merge CI #2578 / run `34730783233`. Esta reconciliação compartilhada promove `aero_additions` a componente **#64 / 64/100**.

Isso é fechamento de catálogo, não runtime PASS. Source 1.2.8 usa NeoForge `21.1.228` e Iron's `1.21.1-3.16.1`, enquanto o pack físico usa NeoForge `21.1.248` e Iron's `3.16.3`. O range declarado do Iron's admite a versão física, mas client/server boot, aplicação dos mixins required, três payload registrations observados, Scroll Forge/config físico, casts representativos, persistence/reload e duplicate-processing continuam fail-closed. Iron's/Aeromancy mantêm autoridade sobre casting, mana, cooldown, efeitos e estado do provider; Black Arcana não cria pipeline duplicado.

## Checkpoint Farmer's Spell 'n Spellbooks — Phase 2BO canonical

O artefato físico `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` / SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff` / CurseForge hash `810347191` foi reconciliado com o source oficial exato `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`. O provider é `MIXED`: possui uma escola própria Gluttony, exatamente **6** registrations `AbstractSpell` próprias e conteúdo adicional de cozinha mágica/Foodgeist/gear/efeitos. As seis identidades entram como **+6 `COUNTED_SOURCE_PINNED`**, elevando o mínimo estrito para **1322**.

A rota de aquisição foi fechada em nível de catálogo pelo focus Gluttony (`#minecraft:foods` + `farmers_spell:foodgeist_seasoning`) e pelo contrato Scroll Forge da linha pública Iron's 3.16.3. O provider marca a escola com `allowLooting=false`, então loot aleatório genérico de scroll não é usado como prova. Sete mixins são required (4 common + 3 client), e `NetworkHandler.registerPackets()` registra zero payloads próprios observados no source pin.

PR #214 HEAD corrigido `d3a92c31d7ac5b38183224ef28c6737e721fc758` passou CI #2564 / run `34723967662`; squash merge `main@34a5fd495da744800b32b051e38c6473c6f5ea15` passou exact-SHA post-merge CI #2565 / run `34724351805` e publicou artifact `10307207453` (`sha256:50b94c3efc207dfd143a10367cf234473ede7dbbc1f36b9acdd3d3ca1ccc67fa`). A reconciliação compartilhada promove `farmers_spell` a componente **#63 / 63/100**.

Isso é fechamento de catálogo, não runtime PASS. Source build usa NeoForge `21.1.238` e Farmer's Delight `1.3.2`, enquanto o pack físico usa NeoForge `21.1.248` e Farmer's Delight `1.3.4`; client/server boot, aplicação dos sete mixins, Foodgeist progression, Scroll Forge no host físico e execução representativa dos seis spells continuam fail-closed. GeckoLib é `4.9.2` em source e pack por version label, sem inferir equivalência runtime.

## Checkpoint Ars Sable — Phase 2BN canonical

O artefato físico `ars_sable-1.21.1-1.1.2.jar` / SHA-1 `df43ad58fb9ca3b7acf7f62dc97ed75fd6da3da8` foi reconciliado com o source oficial exato `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba`. A função fechada é de bridge/infra espacial entre Ars Nouveau e Sable: tracking/sublevel, warp/portal, storage, Source Jar, Planarium, Mob Jar, entidades/pathfinding e câmera/render entram por mixins/adapters; o provider não estabelece spell, glyph, ritual, school, mana/resource ou ação mágica independente. O delta semântico é **+0** e o mínimo estrito permanece **1316** nesse checkpoint histórico.

Phase 2BN fecha `ars_sable` como componente **#62 / 62/100** após PR #212 e validação exact-SHA pós-merge CI #2554 / run `34720646567`, com canonical QA artifact `10306246238` (`sha256:a63f42f6746cc62e435e6a1c541daaed973b0b56d3dcc566cbc7cf4e9fa57e96`). Isso é fechamento técnico/source-pinned de catálogo, não um PASS de compatibilidade runtime. A source foi construída contra Sable `1.2.2` e Ars Nouveau `5.11.7.1354`, enquanto o pack físico usa Sable `2.0.5` e Ars Nouveau `5.13.1`; todos os 24 common + 5 client mixins são required. O registrar de rede usa protocolo `2` e registra zero payloads próprios. A metadata declara `LGPLv3`, enquanto o `LICENSE` raiz contém The Unlicense; nenhum direito de reuso é inferido dessa divergência.

## Checkpoint Ars Polymorphia — Phase 2BM canonical

O artefato físico `ars_polymorphia-1.0.3.jar` / SHA-1 `8cce819e83f6360ab9aa8b44ac841511172a6a79` foi reconciliado com o source oficial exato `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`. A função fechada é de bridge de resolução de conflitos de receita entre Ars Storage/Crafting Lectern e o contrato Polymorph; o provider não estabelece spell, glyph, ritual, school, mana/resource ou ação mágica independente. O delta semântico é **+0** e o mínimo estrito permanece **1316** nesse checkpoint histórico.

Phase 2BM fecha `ars_polymorphia` como componente **#61 / 61/100** após PR #210 e validação exact-SHA pós-merge CI #2544 / run `34713268914`. Isso é fechamento técnico/source-pinned de catálogo, não um PASS de compatibilidade runtime. A source exige mod id `polymorph`, enquanto o pack físico expõe `polymorph_plus` `1.3.1+1.21.1`; a source foi construída contra Ars Nouveau `5.4.2.938`, enquanto o pack usa `5.13.1`; e a própria metadata source declara `minecraft_version=1.21.1` junto de `minecraft_version_range=[1.21,1.21.1)`. Esses pontos continuam fail-closed até evidência direta do host atual.

## Checkpoint Leyline Spellbooks — Phase 2BG canonical

The exact physical `leylines-1.0.3.jar` / SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59` was materialized from CurseForge File ID `8565076` and hash-matched. Its current provider registry contains **14 unconditional `AbstractSpell` identities**, superseding the public nine-name lower bound.

Exact Ley-school/default evidence finds no provider-specific spell lock, and the exact Iron's 3.16.3 generic scroll-selection path corroborates ordinary host reachability. `COUNTED_EXACT` treatment is based on the exact unconditional registry; deployed generic host config remains separate runtime QA. Durable PR #195 HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed CI #2503, squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` passed exact-SHA post-merge CI #2504, and the canonical totals at that checkpoint are **888 semantic objects / 56/100 components**.

Runtime numerical tuning, final loot probabilities, pillar/rift persistence/network internals and any Black Arcana adapter remain separate fail-closed gates.

## Checkpoint Somake Spells — Phase 2BF

Historical Phase 2BF evidence materialized `somakespells-1.0.8-1.21.1-fix.jar` / SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7` from File ID `8417850` and hash-matched it. That artifact owns **67 exact spell registrations for 1.0.8-fix** under the optional-provider set at that checkpoint: 61 unconditional, three gated by physical `mowziesmobs`, and three gated by physical `iss_magicfromtheeast`. The current physical provider is 1.0.9, so these 67 registrations are not presented as current.

This does **not** add to the strict semantic numerator. Somake's `enableSpellLockSystem` is a `COMMON` config at `somakespells/general/common.toml`, code-default `false`; the deployed config is not available in authoritative project material, and full per-object survival acquisition/reachability is not closed. At the Phase 2BF closure, the totals remained **874 semantic objects** and **55/100 structural components**; Phase 2BG later supersedes those checkpoint totals with 888 / 56/100. Runtime mechanics, Aqua/T.O coexistence and any Black Arcana adapter remain fail-closed.

## Checkpoint Cataclysm: Spellbooks — Phase 2BE

O artefato físico `cataclysm_spellbooks-1.1.13-1.21.jar` / SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2` foi materializado pelo File ID exato `8792628` em auditoria isolada e bateu criptograficamente com a modlist. O registry exato fecha **59 `AbstractSpell` registrations `COUNTED_EXACT`**. Por implementation package group: 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature e 22 Technomancy; essa distribuição de packages não é promovida automaticamente a uma tabela de escolas/runtime mechanics.

O `en_us` contém 69 root spell keys, mas dez não possuem identidade registrada no 1.1.13 e ficam excluídos como translation-only/WIP-or-residual. O claim genérico/current do publisher de 65 spells não substitui o registry físico instalado; existe inclusive uma 1.1.14 beta posterior ao arquivo do pack.

Esse fechamento é de identidade/contagem. O HEAD exato do PR #189 (`e787699d25b283b8040cd179f605143e8ee396de`) passou CI #2483; o merge `main@cce7f51794e4e65b0d97511eb55f710afc6e02f0` passou CI #2484 attempt 2 completo após um primeiro attempt encerrar por timeout externo no download da API do Iron's. Balance numérico, acquisition, runtime QA específico do provider e qualquer seam futuro Black Arcana↔Cataclysm Spellbooks continuam separados e fail-closed até evidência provider-native segura.

## Checkpoint Alshanex's Familiars — Phase 2BD

O artefato físico `alshanex_familiars-1.21.1_v4.0.3.jar` / SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686` foi materializado pelo File ID exato `8675568` em auditoria isolada e bateu criptograficamente com o pack. O inventário current-version fecha **7 spell registrations** e **11 `alshanex_familiars:ritual_recipe` identities**, totalizando **18 objetos mágicos semânticos `COUNTED_EXACT`**. Sound/Melodic continua pertencendo a Tunes n' Tomes e não é recontado.

Esse fechamento é de catálogo/identidade. Runtime QA, valores numéricos e qualquer adapter Black Arcana↔Alshanex permanecem fail-closed até contrato provider-native seguro.

## Checkpoint Apprentice's Codex — Phase 2L

`apprenticecodex` está source-catalogado contra o artefato instalado `0.9.7.1` e o pin exato `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`:

- 83/83 spells individualizados;
- 9 escolas canônicas do Iron's;
- School Affinity auditado;
- registries de suporte auditados;
- acquisition/learning auditados;
- compat packages reconciliados com a modlist física;
- runtime QA integral do pack ainda pendente.

A cobertura source-level não converte o addon em authority de Black Arcana nem em provider de Mastery do RPG Skill Tree.

## Checkpoint Goety addons — Phase 2BL exact semantic closure

Goety Iron 3.1 e Goety Cataclysm 1.21.1-1.8.2 foram materializados em audits clean-room hash-matched, separados do Goety base 3.1.4. Goety Iron fecha **2 Focus + 12 rituais não-Focus = +14**; Goety Cataclysm fecha **28 Focus + 24 rituais não-Focus = +52**. Recipes de aquisição de Focus são caminhos de obtenção e não segunda identidade semântica. Os registries de Focus não têm branch/config gate de registration observado.

O delta conjunto é **+66**, levando o mínimo estrito a **1316** naquele checkpoint. Como ambos já eram providers abertos no denominador reconciliado, tornam-se componentes **#59 e #60 / 60/100**. Evidência isolada: PR #205 (Goety Iron) e PR #206 (Goety Cataclysm), ambas NON-MERGE. Runtime servant/cast settlement, balance e adapters continuam fail-closed.

## Checkpoint Ignis Soulfires: Spellbooks — Phase 2BK exact zero closure

O artefato físico `ignissoulfires_spellbooks-1.1.0.jar` / SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119` foi materializado do File ID CurseForge exato `8620663` e hash-matched em NON-MERGE PR #203. O JAR possui 11 classes próprias; seus registries são um armor material e exatamente cinco equipment items. Não há `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` ou `Ability` nas classes do provider, nem spell/ritual/action data registry empacotado.

A classificação exata é `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`; semanticamente é `ZERO_BRIDGE_INFRA`, **+0** objetos. O mínimo estrito permanece **1250** naquele checkpoint. Como o provider já era uma unidade aberta do denominador técnico de 100 componentes, seu fechamento exato torna-o componente **#58 / 58/100**. Evidência: audit HEAD `ed807b77345cde1803767d804e26ea972c41d964`, run `34688273425`, text-only artifact `10296406134`. Runtime gear/balance e qualquer adapter Black Arcana continuam fail-closed.

## Checkpoint Gaze — Phase 2BJ exact-artifact semantic promotion

O artefato físico `gaze-1.1.7.1.jar` / SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041` foi materializado da versão Modrinth exata `od4ltbRo` e hash-matched em NON-MERGE PR #201. O registry exato fecha 26 Gaze Spirit Rites player-facing, dois Geas effect types, oito rune items e um Gaze-owned Iron's `AbstractSpell` (Soulward Shield). O pack físico contém Iron's 3.16.3, então o provider gate desse spell está satisfeito e Soulward Shield contribui **+1 `COUNTED_EXACT`**.

Os 26 Rites não são promovidos: `disableGazeRites` é COMMON e o control flow exato suprime o registry quando o valor resolvido é true; o valor implantado não está disponível. Geas e runes são excluídos pela definição atual da métrica. O mínimo semântico naquele checkpoint passa a **1250**, enquanto provider-component closure permanece **57/100**. Evidência: audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`, run `34676660467`, artifact `10292013626`. Runtime/API/balance permanece fail-closed.

## Checkpoint Goety — Phase 2BH canonical

Exact `goety-3.1.4.jar` evidence closes **123 active Focus actions + 238 available distinct non-Focus ritual actions = +361**. Durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published QA artifact `10291461067` with SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical totals naquele checkpoint são **1249 semantic objects / 57 of 100 components**. Runtime/API/provider settlement remains fail-closed.

## Regra de completude

A Wiki só poderá declarar `CATÁLOGO MÁGICO COMPLETO` quando:

- todos os JARs mágicos/relacionados da modlist atual tiverem classificação;
- todo `SPELL_PROVIDER` tiver inventário individual ou regra explícita de composição;
- todo spell tiver assinatura semântica para deduplicação;
- versão/JAR/mod ID estiverem reconciliados com a modlist atual;
- aquisição, custo, dano/efeito, cooldown e scaling forem extraídos do provider/runtime/config, não inferidos;
- sobreposições forem resolvidas por provider-native first;
- novos spells Black Arcana tiverem justificativa de delta mecânico real.

Até esses gates fecharem, Phase 3 permanece bloqueada.