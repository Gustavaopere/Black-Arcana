# Inventário atual de providers mágicos

## Estado

`AUDITORIA EM ANDAMENTO — categoria física Magic atual reconciliada 84/84 / cross-domain provider queue ainda PENDING REBASE`

O bloco de 595 entradas / NeoForge `21.1.248` abaixo é um **checkpoint histórico de 2026-09-11**. A autoridade corrente para presença/versão combina a modlist física do Project Library com os dossiês físicos sibling mais novos quando estes a supersedem; a taxonomia status-prefixed do sibling não é usada para negar um JAR diretamente observado. O denominador global de providers continua `PENDING REBASE`: a categoria física `Magic` está mapeada, mas o universo cross-domain/root-level é maior que essa pasta.

O antigo denominador interno de **100 componentes mágicos/cross-domain** permanece apenas como checkpoint histórico: ele foi construído antes da rodada física sibling de 22/09 revelar componentes mágicos adicionais, incluindo Hazen N Stuff. Os fechamentos até Mobstein continuam válidos como **68 componentes canônicos daquele conjunto**, mas `68/100` não deve mais ser publicado como fração técnica corrente. Hazen N Stuff fecha o próximo componente conhecido; o novo denominador global fica `PENDING REBASE` até reconciliação integral da modlist física atual.

A árvore canônica atual possui **115 diretórios top-level de provider = 100 ✅ + 15 ⚠️**. Esse número já elimina a duplicata histórica `vampiric-ageing`/`vampiricageing` do mesmo mod id `vampiricageing`. É uma métrica estrutural do catálogo, não uma fração de cobertura: não substitui o denominador técnico cross-domain `PENDING REBASE` e não deve ser usado para calcular porcentagem semântica.

A métrica principal para o usuário é a cobertura de objetos mágicos semânticos — spells, glyphs/spell-parts, rituais/rites e equivalentes discretos. Seu denominador global ainda está em reconstrução; portanto nenhuma porcentagem final é declarada aqui. O mínimo estrito de **1496** foi posteriormente ampliado por Hexalia 1.3.7 (**+4**), Reliquified Ars Nouveau 0.8.1 (**+19**), Reliquified Artifacts 1.0.8 (**+52**), Reliquified Iron's Spells 'n Spellbooks 0.2.7 (**+25**), More Relics (**+61**), Ozymandias Sundries (**+2**), Mowzie's Mobs (**+10 strict**), Ice And Fire CE (**+8 strict**) e Reliquified L_Ender's Cataclysm 0.1.1 (**+7 `COUNTED_EXACT`**), levando o mínimo estrito corrente a **1684**. Ars 'n' Spells 3.3.4, Traveloptics, KubeJS bridges e os novos layers de UI/compat foram reclassificados sem outro delta estrito nesta rodada. Tombstone, Gaze rites, Not Enough Glyphs, Somake e outros blockers abaixo continuam fail-closed onde configuração/inventário atual não está fechado.

Phase 2BS adiciona T.O Magic n' Extras / `traveloptics` 4.4.0.1-1.21.1 ao conjunto **⚠️ parcial/condicionado**: o publisher file exato `6342780` fecha 33 identidades de spell registradas e exclui 32 roots de localization residuais, mas `traveloptics:blackout` permanece sem rota survival objeto-a-objeto fechada e o JAR exato apresenta risco estrutural em `TOLootModifiers` (`KeyLootModifier.CODEC` referenciado duas vezes; `UniversalLootModifier.CODEC` zero). Portanto Phase 2BS contribui **+0 strict**, não cria componente #67 naquele checkpoint e mantém **1344 / 66 de 100** historicamente. Phase 2BT posteriormente fecha o componente #67 com Vampire Spells Addon sem alterar o total semântico.

Capítulos e tabelas históricas abaixo continuam úteis para rastrear deltas, mas não prevalecem sobre o snapshot físico atual.

## Reconciliação física Magic — snapshot sibling atual

A autoridade física corrente é `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7`. Aplicando o critério ao **campo de categoria** da modlist, existem **84 linhas cuja categoria contém `Magic`**. O nome do mod não é usado como atalho de classificação.

Após normalização de ownership/aliases e a reconciliação de 27/09:

- **71 ✅ catalogados** com diretório Black Arcana correspondente;
- **13 ⚠️ parciais/condicionados** com diretório Black Arcana correspondente;
- **0 ❌** linhas físicas `Magic` sem classificação;
- **0 🟡** de implementação ativa;
- **0 ⛔** por ausência total de evidência.

Assim, **84/84** linhas da categoria física `Magic` estão mapeadas em Black Arcana (**71 ✅ + 13 ⚠️**). Isso é um subtotal físico/categorial, não o denominador semântico global.

O delta contra o snapshot anterior de 67 linhas é **+17**. Onze dessas linhas já possuíam provider canônico e não geram nova contagem. Seis foram inicialmente materializadas como ⚠️: Reliquified L_Ender's Cataclysm, ShadowsZ, Simply Swords: Cataclysm, Simply More, Simply Swords e Waystones. Reliquified L_Ender's Cataclysm 0.1.1 agora está ✅ `COUNTED_EXACT 7`. Os outros cinco permanecem ⚠️. ShadowsZ 1.1.9 já tem denominador exato de **10** ações semânticas, mas segue `+0 strict` até capturar `shadowszRestrictPowers` efetivo e `fusionEnabled`. Simply More Alpha 5 agora tem denominador corrente exato de **24** ações (10 API ativa + 13 legacy de uso direto + 1 Mimicry compartilhada), mas segue `+0 strict` até fechar Awakening/aquisição/Mimicry/config implantados. O delta estrito desta reconciliation continua **+7** e o mínimo global permanece **1684**. Ver [PHYSICAL-MAGIC-RECONCILIATION-2026-09-27.md](./PHYSICAL-MAGIC-RECONCILIATION-2026-09-27.md).

**Cross-domain note:** o subtotal físico `Magic` continua sem representar o universo global. Gaze permanece ⚠️ com um spell contado + 26 rites config-condicionais; Ender's Spells and Stuff: Requiem é ✅ com 53 ações strict; Reliquified Ars Nouveau, Reliquified Artifacts e Reliquified Iron's são ✅ com 19, 52 e 25 ability roots source-pinned; Reliquified L_Ender's Cataclysm 0.1.1 é ✅ com 7 ability roots exact-current; Iron's Spellbooks KubeJS agora também aparece nessa categoria sibling e permanece ⚠️ por inventário mutável de scripts; More Relics é ✅ com 61 ability roots exatas; Ozymandias Sundries agora é ✅ com 2 spells exatos; Mowzie's Mobs é ⚠️ com 10 poderes strict + 1 Tunneling config-condicional; Traveloptics permanece ⚠️ +0 strict pendente de fechamento exato-current. Spell Actionbar, Specs, Recolor e Immersive Portal estão ✅ catalogados com +0 identidades independentes; QA técnico/runtime permanece separado.
**Traveloptics current-physical override:** Project Library physical evidence directly records `traveloptics-4.4.0.1-1.21.1.jar` / SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`. This outranks the absence of a status-prefixed sibling row for presence/version. The installed digest differs from the audited publisher alpha and known patch artifact, so Traveloptics is a current **⚠️ `OTHER_VERIFIED` / +0 strict** provider blocker until its installed-byte registry and reachability are closed.

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
- ⚠️ Corail Tombstone 9.5.6 — Project Library physical SHA-1 equals audited File `8842741`; **10 `COUNTED_EXACT` actions** strict-counted (6 prayer + 4 Ritual Flute); 12 config-sensitive castable magic-item actions remain conditional.
- ✅ Relics 0.12.8 — exact physical/publisher artifact equality; **39 base abilities + 2 distinct synergies = 41 `COUNTED_EXACT` provider powers**; runtime/config QA remains fail-closed.
- ⚠️ Somake 1.0.9 — physical SHA-1 equals exact publisher File `8867079`; exact physical registry is **83 IDs**, gate topology is **67 unconditional + 16 optional**, current mod composition admits **83/83**, and all 83 current identities now have individual cards. Remaining blockers are effective deployed Iron's/provider config and survival reachability.
- ✅ Ars 'n' Spells 3.3.4 — **5** ritual identities retained; `COUNTED_RELEASE_BOUNDED`; current version delta **+0**.
- ✅ Hexalia 1.3.7 — **29 `COUNTED_SOURCE_PINNED`** semantic actions (23 Nature's Ritual + 6 Celestial Infusion), **+4** versus the prior line.
- ✅ Reliquified Ars Nouveau 0.8.1 — **19 `COUNTED_SOURCE_PINNED`** owner-scoped ability roots.
- ✅ Reliquified Artifacts 1.0.8 — **52 `COUNTED_SOURCE_PINNED`** owner-scoped ability roots.
- ✅ Reliquified Iron's Spells 'n Spellbooks 0.2.7 — **25 `COUNTED_SOURCE_PINNED`** provider-owned relic ability roots.
- ✅ Reliquified L_Ender's Cataclysm 0.1.1 — exact publisher/physical SHA-1 equality; **5 relic owners / 7 owner-scoped ability roots = +7 `COUNTED_EXACT`**; exact-current loot routes for all five owners closed by audit run `36416011761`; assembled/runtime QA remains separate.
- ✅ More Relics 1.7.7-forRelics-0.12.8-1.0 — exact physical/publisher File `8859015` equality; **29 owners / 61 owner-scoped ability roots = +61 `COUNTED_EXACT`**; exact builder/localization root sets agree, runtime/config/evolution QA remains separate.
- ✅ Ozymandias Sundries physical 0.0.5 / embedded 0.0.1 — exact File `6978561` hash match; **2 unconditional registered spells = +2 `COUNTED_EXACT`** (`levitate`, `lightning_warp`); unregistered class/localization residue excluded; runtime/config QA separate.
- ⚠️ Mowzie's Mobs 1.8.2 — exact File `7760267` hash match; **13 active player-ability slots**, reconciled to **10 strict `COUNTED_EXACT` powers + 1 `CONDITIONAL` Tunneling power**; `hit_boulder`/`backstab` technical-subaction slots and four inactive ids excluded.
- ⚠️ Ice And Fire Community Edition 2.1.2 — exact File `8757837`; **8 action families strict `COUNTED_EXACT` + 1 `CONDITIONAL`** after exact current-JAR reachability run `36323035696` plus current-pack NeoForge 21.1.250 runtime audit `36327488231`; only Ghost Sword deployed `phantasmalBladeAbility` remains open.
- ✅ Photon 2.2.6.a — exact physical/publisher File `8824095` equality; VFX/editor infrastructure only under the semantic metric; **+0 `ZERO_SEMANTIC_VFX_INFRA`**.
- ✅ RunicLib 5.0.7 — exact physical/publisher File `8188562` equality; reusable effect/attribute/damage/trade/services library surface only; **+0 `ZERO_SEMANTIC_LIBRARY_INFRA`**.
- ✅ Mowzie's Cataclysm 1.2.2 — exact File `8196282` equality; quatro Eyes de localização + recipes/tags, **+0 `ZERO_SEMANTIC_LOCATOR_BRIDGE`**.
- ✅ Pickable Orbs 1.21.1-1.0.0 — exact File `8660158` equality; oito definições de pickup e `OrbEntity`, **+0 `ZERO_SEMANTIC_PICKUP_EFFECT_INFRA`**.
- ✅ IronSable X Wind's Spellbooks 1.0.0 — exact File `8598265` equality; bridge física sobre Tornado/Almighty Push/Wind Blade/Aeropic já pertencentes a Wind's Spellbooks, **+0 `ZERO_SEMANTIC_EXISTING_SPELL_PHYSICS_BRIDGE`**.
- ✅ Iron's Gems 'n Jewelry 1.21.1-2.0.2 — exact File `8365016` equality; oito codecs `IAction` são payloads de proc/bônus de joia, não casts independentes, **+0 `ZERO_SEMANTIC_EQUIPMENT_PROC_FRAMEWORK`**.
- ✅ Integrated Villages 1.3.3+1.21.1-neoforge — exact File `8161672` equality; worldgen/structures/loot/data integration, **+0 `ZERO_SEMANTIC_WORLDGEN_INTEGRATION`**.
- ⚠️ Traveloptics 4.4.0.1-1.21.1 — current physical provider; installed artifact is `OTHER_VERIFIED`; publisher-baseline 33 spells are not promoted as exact-current; **+0 strict**.
- ⚠️ Iron's Spellbooks KubeJS 4.0.3 / KubeJS Ars Nouveau 1.3.2 — **+0 fixed built-in identities**, current pack script/mutation inventory still open.
- ✅ Immersive Portal Iron's bridge, Iron's Recolor, Spell Actionbar and Specs — semantic catalogs closed at **+0 independent identities**; runtime/interop QA remains separate and fail-closed.

O mínimo semântico estrito corrente é **1684**. O denominador semântico final e o denominador técnico cross-domain continuam abertos; não publicar percentual global.

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