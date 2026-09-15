# Inventário atual de providers mágicos

## Estado

`AUDITORIA EM ANDAMENTO — autoridade física 2026-09-11`

A autoridade de presença/JAR/runtime é a modlist física atual do pack, com **595 entradas top-level**, Minecraft 1.21.1 e NeoForge `21.1.248`. O snapshot físico reconciliado possui SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

O denominador interno corrente do catálogo permanece **100 componentes mágicos/cross-domain**; Phase 2BL fecha `goetyiron` como componente **#59** e `goety_cataclysm` como componente **#60**, Phase 2BM fecha `ars_polymorphia` como componente **#61**, Phase 2BN fecha `ars_sable` como componente **#62**, Phase 2BO fecha `farmers_spell` como componente **#63**, Phase 2BP promove `aero_additions` como componente **#64**, Phase 2BQ promove `ars_two_way_portals` como componente **#65**, Phase 2BR promove `gtbcs_geomancy_plus` como componente **#66**, e esta reconciliação Phase 2BT promove `vampire_spells_addon` como componente **#67** após o fechamento source-pinned da PR #239 e seu exact-SHA post-merge CI verde. Portanto **67 estão canônicos** após esta reconciliação. Esse 67/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.

A métrica principal para o usuário é a cobertura de objetos mágicos semânticos — spells, glyphs/spell-parts, rituais/rites e equivalentes discretos. Seu denominador global ainda está em reconstrução; portanto nenhuma porcentagem final é declarada aqui. Farmer's Spell acrescenta **+6 `COUNTED_SOURCE_PINNED`**, elevando o mínimo estrito de **1316 para 1322**; Aeromancy Additions acrescenta mais **+10 `COUNTED_SOURCE_PINNED`**, elevando-o para **1332**; Ars Polymorphia, Ars Sable, Ars Nouveau: Two-Way Portals e Vampire Spells Addon são fechamentos semânticos **+0**; GTBC's Geomancy Plus acrescenta **+12 `COUNTED_RELEASE_BOUNDED`**, elevando o mínimo estrito para **1344**. Phase 2BT não altera esse mínimo.

Phase 2BS adiciona T.O Magic n' Extras / `traveloptics` 4.4.0.1-1.21.1 ao conjunto **⚠️ parcial/condicionado**: o publisher file exato `6342780` fecha 33 identidades de spell registradas e exclui 32 roots de localization residuais, mas `traveloptics:blackout` permanece sem rota survival objeto-a-objeto fechada e o JAR exato apresenta risco estrutural em `TOLootModifiers` (`KeyLootModifier.CODEC` referenciado duas vezes; `UniversalLootModifier.CODEC` zero). Portanto Phase 2BS contribui **+0 strict**, não cria componente #67 naquele checkpoint e mantém **1344 / 66 de 100** historicamente. Phase 2BT posteriormente fecha o componente #67 com Vampire Spells Addon sem alterar o total semântico.

Capítulos e tabelas históricas abaixo continuam úteis para rastrear deltas, mas não prevalecem sobre o snapshot físico atual.

## Freshness histórica 2026-09-07

O checkpoint de 2026-09-07 registrou updates como:

- Apotheosis `8.7.0 → 8.8.0`;
- Ars 'n' Spells `3.2.4 → 3.3.0` naquele snapshot; o runtime físico atual está em `3.3.2`;
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
- T.O Magic n' Extras;
- Hazen N Stuff;
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

## Phase 2BT — Vampire Spells Addon 0.0.9 — canonical zero-semantic component #67

A PR #239 fechou `vampire_spells_addon-neoforge-1.21.1-0.0.9.jar` contra a release oficial `1.21.1-0.0.9` e o source target exato `xsharov/VampireSpellsAddon@2d36e94e67611a316b7311b11e4574b499025580`. O audit prova que os identificadores mágicos usados pelo addon pertencem ao namespace `irons_spellbooks`, que o entrypoint instala listeners/bridges sobre Iron's e Vampirism e que não existe registrar provider-owned de spell, school, ritual ou ação mágica equivalente.

O estado semântico é `ZERO_BRIDGE_INFRA`: **+0** objetos. A release/source audit foi mergeada na PR #239 como `main@1c5091807a8773d378c34ffac2e737b5f08b545c`; o exact merge SHA passou Black Arcana CI run `34795795283` completo. Com a evidência durável e o post-merge gate já satisfeitos, esta reconciliação compartilhada promove `vampire_spells_addon` a componente **#67 / 67/100** sem alterar o mínimo semântico de **1344**.

Isso não é runtime PASS. Igualdade byte-for-byte do JAR físico, resolução reflexiva assembled-pack, ordem de mixins/events, serverconfig efetivo, settlement de blood/mana/damage/cooldown e coexistência com outros bridges permanecem fail-closed. Iron's/Vampirism continuam authorities dos spells/recursos modificados; Black Arcana não cria identidade ou settlement duplicado.

## Phase 2BS — T.O Magic n' Extras / Traveloptics 4.4.0.1-1.21.1 — partial canonical

O exact publisher release file `6342780` fecha **33** registrations `traveloptics:<id>` no `TOSpells`, com 33 field→classe→ID mappings e zero branches no initializer. Outros **32** root localization spell IDs existem no alpha, mas não estão registrados e são excluídos. `AbstractUniqueSpell.allowCrafting=false`; nove dos dez Unique registrados possuem rotas de loot estruturadas, enquanto `traveloptics:blackout` não possui referência estruturada nem referência provider-owned fora do registry encontrada pelo audit.

O audit de risco também prova que `TOLootModifiers` contém os nomes `key_loot` e `universal_loot`, mas referencia `KeyLootModifier.CODEC` duas vezes e `UniversalLootModifier.CODEC` zero vezes. Um patch de terceiro descreve esse mesmo wiring como defeito de startup, porém Black Arcana não declara crash reproduzido. A promoção fica fail-closed até runtime físico autoritativo e reachability de Blackout. Durable PR #228 mergeou em `main@0bd1c04460e63a03b6b484b785247e75f6e44178`; post-merge CI #2682 / run `34741699505` passou e publicou artifact `10311724779` (`sha256:05e28f0dc516e3b51bbd9016a37816cd1854e45caeaa71745189b20297ae3813`). Estado: **⚠️ parcial/condicionado / +0 strict / componente aberto naquele checkpoint**.

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

The exact physical `somakespells-1.0.8-1.21.1-fix.jar` / SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7` was materialized from File ID `8417850` and hash-matched. The provider owns **67 exact current spell registrations** under the present optional-provider set: 61 unconditional, three gated by physical `mowziesmobs`, and three gated by physical `iss_magicfromtheeast`.

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
