# Apprentice's Codex 0.9.7.1 — exact spell/content provider catalog

## Status

`EXACT INSTALLED ARTIFACT 0.9.7.1 / EXACT SOURCE VERSION PIN 305ea6a / MIT CODE + CC0 ORIGINAL ASSETS / IRON'S 3.16.3 BASELINE MATCHES PACK / 83/83 SPELLS SOURCE-CATALOGED / 9 IRON'S SCHOOLS / SCHOOL AFFINITY AUDITED / SUPPORT REGISTRIES AUDITED / ACQUISITION SURFACES AUDITED / OPTIONAL COMPAT MATRIX RECONCILED WITH PACK / RUNTIME QA PENDING`

## Installed identity

Current physical modlist authority:

- provider: **Apprentice's Codex**;
- installed JAR: `apprentice_codex-0.9.7.1+mc1.21.1.jar`;
- mod id: `apprenticecodex`;
- runtime version: `0.9.7.1`;
- mixin config: `mixins.apprenticecodex.json`;
- SHA-1: `b514315add32b93b0049c8673075627d7ef812e0`;
- package fingerprint: `702285225`;
- loader/game: NeoForge `21.1.248` / Minecraft 1.21.1.

The physical modlist remains authoritative for the binary actually installed.

## Exact release/source checkpoint

Publisher repository: `hexqua/apprentice_codex`.

Exact version commit:

`305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

The commit's only codebase delta is the version change `0.9.7 -> 0.9.7.1` in `gradle.properties`, which makes it a strong source pin for the installed release line.

Exact checkpoint metadata includes:

- Minecraft `1.21.1`;
- NeoForge `21.1.228` source build baseline;
- Java 21 project line;
- mod id `apprenticecodex`;
- mod version `0.9.7.1`;
- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Iron's Lib `1.21.1-2.1.0`;
- Curios `9.5.1+1.21.1`;
- GeckoLib `4.8.3`;
- Create `6.0.10` development/optional-compat baseline;
- Sable `2.0.3` development/optional-compat baseline.

The pack uses Iron's `3.16.3`, Iron's Lib `2.1.0`, Curios `9.5.1+1.21.1`, Create `6.0.10` and compatible/newer GeckoLib. Optional provider versions are reconciled in [`COMPATIBILITY.md`](COMPATIBILITY.md); source-dev baselines are not silently promoted to pack runtime versions.

## Provenance

Exact source evidence is internally coherent:

- `LICENSE.txt`: MIT License, copyright 2026 Aquid;
- `gradle.properties`: `mod_license=MIT`;
- `ASSETS_LICENSE.md`: original project assets are CC0-1.0 unless otherwise noted;
- upstream `THIRD_PARTY_NOTICES.md`: third-party assets keep their own terms.

Black Arcana uses the source read-only for factual cataloging. No upstream code/assets are copied or adapted by this catalog.

## Critical registry correction — 83 spells, not approximately 60

The public project description can describe the addon as containing roughly 60 spells. The exact 0.9.7.1 `SpellRegistry` registers **83** spells.

For the installed build, the exact source registry supersedes an approximate marketing count.

| Iron's school | Exact count |
|---|---:|
| Blood | 3 |
| Ender | 15 |
| Evocation | 17 |
| Fire | 5 |
| Holy | 11 |
| Ice | 3 |
| Lightning | 10 |
| Nature | 12 |
| Eldritch | 7 |
| **Total** | **83** |

Apprentice's Codex creates **no new spell school** in this registry. It registers into Iron's canonical school resources.

## Exact spell registry — 83/83

### Blood — 3

- `apprenticecodex:higanbana`
- `apprenticecodex:mist_form`
- `apprenticecodex:blood_brand`

### Ender — 15

- `apprenticecodex:arcane_blast`
- `apprenticecodex:arcane_beam`
- `apprenticecodex:personal_shelf`
- `apprenticecodex:assist_wings`
- `apprenticecodex:manifestation_grimoire`
- `apprenticecodex:mantis_leap`
- `apprenticecodex:auto_magnet`
- `apprenticecodex:remote_eye`
- `apprenticecodex:mana_slash`
- `apprenticecodex:long_stride`
- `apprenticecodex:rift_hole`
- `apprenticecodex:demicreator_wings`
- `apprenticecodex:mirage_avoidance`
- `apprenticecodex:anchor_blink`
- `apprenticecodex:servant_gaze`

### Evocation — 17

- `apprenticecodex:archer_multiple`
- `apprenticecodex:feather_rush`
- `apprenticecodex:slash_blade`
- `apprenticecodex:precision_jack`
- `apprenticecodex:auto_turret`
- `apprenticecodex:companion_trunk`
- `apprenticecodex:search_beacon`
- `apprenticecodex:tamers_pocket`
- `apprenticecodex:silent_assassin`
- `apprenticecodex:tiro_volley`
- `apprenticecodex:bound_sword`
- `apprenticecodex:bound_bow`
- `apprenticecodex:lethal_assault`
- `apprenticecodex:edge_dancer`
- `apprenticecodex:linear_build`
- `apprenticecodex:fujin`
- `apprenticecodex:call_broom`

### Fire — 5

- `apprenticecodex:thermal_process`
- `apprenticecodex:magic_spear`
- `apprenticecodex:artisan_smash`
- `apprenticecodex:combustion_jet`
- `apprenticecodex:catch_flame`

### Holy — 11

- `apprenticecodex:mage_light`
- `apprenticecodex:phalanx_charge`
- `apprenticecodex:mana_charge`
- `apprenticecodex:force_field`
- `apprenticecodex:sense_evil`
- `apprenticecodex:illuminate_stellar`
- `apprenticecodex:unite_luna`
- `apprenticecodex:mystic_shield`
- `apprenticecodex:divine_possession`
- `apprenticecodex:mana_mending`
- `apprenticecodex:wizardlamp`

### Ice — 3

- `apprenticecodex:frost_rune`
- `apprenticecodex:inscribe_ice`
- `apprenticecodex:totem_of_permafrost`

### Lightning — 10

- `apprenticecodex:sky_edge`
- `apprenticecodex:commence_fire`
- `apprenticecodex:quick_arms`
- `apprenticecodex:breaching_enemy`
- `apprenticecodex:bullet_stream`
- `apprenticecodex:fly_swatter`
- `apprenticecodex:shock`
- `apprenticecodex:dual_acrobat`
- `apprenticecodex:field_overseer`
- `apprenticecodex:shiden`

### Nature — 12

- `apprenticecodex:compound_phial`
- `apprenticecodex:tiny_lumberjack`
- `apprenticecodex:graced_rain`
- `apprenticecodex:world_flatter`
- `apprenticecodex:earth_forge`
- `apprenticecodex:grind_runner`
- `apprenticecodex:treasure_divination`
- `apprenticecodex:healing_bloom`
- `apprenticecodex:harvest_moon`
- `apprenticecodex:extract`
- `apprenticecodex:heavenly_fist`
- `apprenticecodex:terra_resonance`

### Eldritch — 7

- `apprenticecodex:palette_shift`
- `apprenticecodex:moon_light`
- `apprenticecodex:deep_sensor`
- `apprenticecodex:spectral_wing`
- `apprenticecodex:echo_cast`
- `apprenticecodex:otherworld_lens`
- `apprenticecodex:mana_transcription`

Each registry entry now has a source-pinned per-spell page under its school directory. Numeric formulas, duration/range constants, acquisition restrictions and delegated manager/entity details are recorded at the highest confidence supported by the exact 0.9.7.1 source; unknown entity/config/runtime values remain explicitly pending rather than inferred.

## Release 0.9.7.1 additions

The exact public 0.9.7.1 changelog calls out four new spells:

- Combustion Jet;
- Blood Brand;
- Shiden;
- Catch Flame.

All four are present in the exact 83-spell registry.

## Provider-wide systems

Phase 2L also audits the provider surfaces that materially affect deduplication and integration:

- [`SCHOOL-AFFINITY.md`](SCHOOL-AFFINITY.md) — 25-slot dynamic affinity system, exact modifiers and potion variants;
- [`SUPPORT-CONTENT.md`](SUPPORT-CONTENT.md) — block/effect/attribute registries plus provider equipment/casting-item families;
- [`ACQUISITION.md`](ACQUISITION.md) — spell eligibility rules, recipes, Errand Mage, loot and learning boundaries;
- [`COMPATIBILITY.md`](COMPATIBILITY.md) — exact compat package inventory reconciled against the physical pack;
- [`INTEGRATION-RULES.md`](INTEGRATION-RULES.md) — Black Arcana/RPG authority and deduplication contracts.

## Provider identity

Apprentice's Codex is an Iron's-native **spell/content/equipment/utility addon** rather than a second magic engine. Its spells use Iron's spell-school and mana semantics unless a specific provider item deliberately modifies casting.

Source-confirmed capability families include:

- summoned magical firearms/blades/weapons;
- barriers, guard and evasion;
- remote vision and sensing;
- mobility/gliding/flight zones;
- companion constructs;
- private/pet storage;
- structure/treasure detection;
- healing/mana recovery;
- block placement/excavation/harvesting/processing;
- potion/flask interaction;
- enchantment transcription;
- spellcasting equipment and alternative cast triggers;
- a server-owned Spell Dispenser surface for supported spells.

## Authority consequence

Apprentice's Codex remains authority for its spell implementations, custom items/entities/blocks, temporary states and optional compatibility behavior. Iron's remains authority for the core spell registry, schools, mana and standard spell lifecycle that the addon uses.

Black Arcana must not:

- duplicate these 83 capabilities merely under different names/VFX;
- create a second mana payment for their casts;
- re-settle their damage/healing/world effects;
- treat an Apprentice spell as a Black Arcana cast unless a real cross-provider contract says so;
- infer optional compat activation from source development dependencies alone;
- convert School Affinity into RPG Mastery or Black Arcana Arcane Danger state.

## Canonical navigation

- [`blood/`](blood/README.md)
- [`ender/`](ender/README.md)
- [`evocation/`](evocation/README.md)
- [`fire/`](fire/README.md)
- [`holy/`](holy/README.md)
- [`ice/`](ice/README.md)
- [`lightning/`](lightning/README.md)
- [`nature/`](nature/README.md)
- [`eldritch/`](eldritch/README.md)

## Validation state

`SOURCE REGISTRY EXACT / 83 SPELL PAGES PRESENT / SUPPORT SYSTEMS SOURCE-AUDITED / INSTALLED JAR IDENTITY EXACT / FULL RUNTIME QA NOT YET COMPLETE`

The exact source pin supports factual source-derived cataloging. It does not by itself prove every optional mod bridge is active in the user's full 612-mod runtime. Phase 2L therefore closes source/catalog coverage while preserving runtime-QA flags wherever provider/environment behavior still requires execution.

## Mapas de implementação para Codex / RPG Skill Tree

Esta campanha acrescenta às **83 fichas já source-catalogadas** localizadores exatos de classes Java verificados pelo `SpellRegistry` do commit `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; seis fichas de risco recebem cadeia causal detalhada. Não há novo spell registry, API de setter de geometria ou QA físico certificado. Regras de campos e estados: [padrão global](../../meta/PERK-READY-TECHNICAL-STANDARD.md).

## Engenharia causal de oito magias sensíveis — 2026-10-13

**🟡 Cobertura técnica aprofundada 14/83** (seis dossiês anteriores, oito adicionais); **✅ identidade/source-class 83/83** preservada. [Matriz de alto risco 0.9.7.1](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) documenta Anchor Blink, Rift Hole, Remote Eye, Auto Magnet, Linear Build, Earth Forge, Force Field e Demi-creator Wings com métodos concretos de runtime no source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. **69/83** esperam a mesma profundidade de engenharia, mas continuam **catalogadas**.

A análise acrescentou sequenciamento de projétil e blink, expiração e restauração de túnel, ancoragem de Remote Eye, lote de coleta e débito do Auto Magnet, cobranças/rollback de Linear Build, agendamento de Earth Forge, defesa contra dano no Force Field e remoção de voo no Demicreator Wings. **⚠️** Configuração física, bytecode dos métodos, reprodução em Minecraft cliente/servidor, claims, jogo real e integração com mods opcionais ainda exigem QA; **⛔** perks/Mastery dependem de contrato efetivo com RPG Skill Tree. A instrumentação do Black Arcana não foi alterada e `Stage 06.05` permanece no status operacional existente.

## Engenharia causal de entidades e jobs — 2026-10-13

**🟡 24/83** magias têm agora dossiês source-level de lifecycle aprofundado: seis da campanha original, oito da [matriz de alto risco](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) e dez da [matriz de entidades/jobs](PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md). Todas as **✅ 83/83** permanecem catalogadas; **59/83** aguardam o mesmo detalhamento. **+0** raízes novas.

Este incremento documenta callbacks, estado owner/UUID, recuperação de itens, reservas do Search Beacon, entidades temporárias, agendamento de jobs, fluxo de mana e separação de efeitos derivados em dez fichas existentes. **⚠️** Método Java source não comprova JAR byte-idêntico, configuração ativa, QA no modpack ou segurança de mods externos. **⛔** Não há adapter homologado de perks/Mastery; nenhuma alteração do runtime mágico BA foi feita.


## Engenharia causal de 10 magias persistentes — 2026-10-14

**🟡 34/83** fichas com dossiê source-located aprofundado (6 originais + 8 alto risco + 10 lifecycle + 10 [persistentes](PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md)); **✅ 83/83** identidades permanecem inventariadas e **49/83** ainda esperam engenharia desse nível. **+0** raízes globais. Três famílias críticas tratadas: entidades/itens gerados, efeitos periódicos de dano/cura e intervenções sobre blocos/sessões.

Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` e JAR instalado 0.9.7.1 da modlist sibling. **⚠️** Leitura de callbacks no source não comprova equivalência binária dos métodos ou QA Survival no modpack. **⛔** perks/Mastery sem contrato interoperável; o runtime Black Arcana não foi alterado.

## Engenharia causal de mundo, channel e defesa — 2026-10-14

**🟡 44/83** magias com dossiê source-level aprofundado (34 prévias + 10 deste lote); **✅ 83/83** identidades continuam catalogadas e **39/83** aguardam mesma profundidade; +0 roots. [Matriz de mundo/combate](PERK-ENGINEERING-MATRIX-WORLD-COMBAT-0.9.7.1.md) cobre Frost Rune, Inscribe Ice, Harvest Moon, Field Overseer, Graced Rain, Mage Light, Mystic Shield, Mirage Avoidance, Feather Rush e Phalanx Charge a partir do source fixado `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

⚠️ Bytecode compilado, config efetiva, Survival/dedicated-modpack, claims, PvP, estado NBT e concorrência ainda aguardam QA. ⛔ Sem adapter real de perks/Mastery e sem promoção de Stage 06.05. Nenhuma mudança de runtime.

## Engenharia causal de armas conjuradas e efeitos derivados — 2026-10-14

**🟡 54/83** dossiês aprofundados (44 anteriores + 10 source-auditados neste lote); **✅ 83/83** identidades catalogadas, **29/83** pendentes, **+0 roots**. A [matriz de armas conjuradas](PERK-ENGINEERING-MATRIX-SUMMONED-WEAPONS-0.9.7.1.md) rastreia Commence Fire, Breaching Enemy, Dual Acrobat, Fujin, Silent Assassin, Lethal Assault, Moon Light, Shiden, Fly Swatter e Precision Jack com classes/métodos da versão declarada 0.9.7.1. **⚠️** Sem equivalência binária JAR/QA físico de config, Survival, dedicated, claims, PvP ou performance; **⛔** adapter Mastery/perks sem contrato. Java/runtime, Stage 06.05 e autoridade de mana/casts inalterados.

## Engenharia causal de utilidades, persistência e recursos — 2026-10-14

**🟡 64/83** magias com dossiê source-level causal aprofundado (54 integradas +10 deste lote); **✅ 83/83** identidades já catalogadas, restam **19/83** nesta profundidade e +0 roots. [Matriz de utilidades/lifecycle](PERK-ENGINEERING-MATRIX-UTILITY-LIFECYCLE-0.9.7.1.md) contém Combustion Jet, Catch Flame, Wizardlamp, Grind Runner, Spectral Wing, Mana Transcription, Servant Gaze, Compound Phial, Extract e Terra Resonance, com classe/método do source fixado `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

⚠️ Leitura de source não é prova física do JAR/corpos de métodos, config, Survival, dedicated/multiplayer, claims/PvP, persistência nem economia de itens; ⛔ perks/Mastery continuam sem adapter real homologado. Nenhum runtime Java nem Stage modificado.

## Engenharia causal de ofensiva, movimento e detecção — 2026-10-14

**🟡 74/83** magias com dossiês causais aprofundados (64 integradas + 10 neste lote); **✅ 83/83** identidades source-catalogadas, **9/83** faltando na mesma profundidade e +0 roots. [Matriz de ofensiva/movimento](PERK-ENGINEERING-MATRIX-OFFENSE-MOVEMENT-0.9.7.1.md) cobre Arcane Beam, Mantis Leap, Mana Slash, Long Stride, Slash Blade, Tiro Volley, Magic Spear, Artisan Smash, Mana Charge e Sense Evil, com callbacks e classes auxiliares source-pinned. `ArcaneBeamEntity.tick` exibe divergência entre comentário e condição de tick de dano: ⚠️ achado source-only, **não** bug reproduzido no JAR instalado. QA bytecode/config, dedicated/Survival, PvP/claims, lifecycle, carga e network pendentes. ⛔ Sem adapter de perks/Mastery; nenhum runtime alterado nem Stage promovido.

## Engenharia causal — fechamento documental das 83 magias (2026-10-14)

**✅ 83/83 identidades** de magias source-catalogadas e **🟡 83/83** dossiês com engenharia causal aprofundada em código-fonte declarado 0.9.7.1 (74 anteriores + 9 neste lote). **0 fichas restantes nesta profundidade documental**, +0 roots. [Matriz de fechamento source-level](PERK-ENGINEERING-MATRIX-FINAL-NINE-0.9.7.1.md) cobre Illuminate Stellar, Unite Luna, Mana Mending, Sky Edge, Quick Arms, Shock, Treasure Divination, Palette Shift e Deep Sensor. Achados source: antimagia de Unite Luna desencadeia burst com **3× dano**; Palette Shift consome recepção ao **cancelar próximo SpellPreCastEvent**; Mana Mending compara a **identidade da instância de ItemStack**, referência não persistida. A porcentagem **não** certifica bytecode do JAR físico, config, dedicated, multiplayer, claims, PvP, GameTest/Survival ou interoperabilidade. ⛔ Sem adapter RPG Skill Tree; nenhum Java/runtime/Stage alterado.
