# GTBC's Geomancy Plus 1.1.0 — prova binária estática 12/12

✅ **12/12 `COUNTED_EXACT` no registro estático; ⚠️ runtime, configuração, aquisição em jogo e Survival não verificados.**

## JAR físico e publicador

- Modlist sibling `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`: posição #309; `gtbcs_geomancy_plus-1.1.0-1.21.1.jar`, mod ID `gtbcs_geomancy_plus`, SHA-1 `67e9652799f35f1fbd09968da6f400d0229f5599`.
- CurseForge [project 1352485, file 7041615](https://www.curseforge.com/minecraft/mc-mods/gtbcs-geomancy-plus/files/7041615), release NeoForge 1.21.1; JAR oficial de **475333 bytes**.
- [Auditoria independente Java 21 #38332395627](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38332395627) baixou o JAR do CDN oficial, confirmou `sha1sum --check` igual à modlist física, ZIP íntegro e registries via `javap -p -c`. Branch isolada e não mergeada `audit/gtbc-geomancy-plus-110-physical-registry-20261012`, HEAD `fe21ecdff15bb2e9cad87deeff8284cdde11d4b8`.

## Registry e IDs

O registrador físico `com.gametechbc.gtbcs_geomancy_plus.init.GGSpells` inicializa **12 inscrições `registerSpell`**, sem branches, usando helper `DeferredRegister.register`. `com.gametechbc.gtbcs_geomancy_plus.GeomancyPlusMod` referencia o registrador. Cada classe concreta de spell contém a literal da chave correspondente e `getSpellResource()`.

| # | Escola | Registry ID | Classe física |
|---:|---|---|---|
| 1 | Geo | `gtbcs_geomancy_plus:chunker` | `ChunkerSpell` |
| 2 | Geo | `gtbcs_geomancy_plus:dripstone_bolt` | `DripstoneBoltSpell` |
| 3 | Geo | `gtbcs_geomancy_plus:eroding_boulder` | `ErodingBoulderSpell` |
| 4 | Geo | `gtbcs_geomancy_plus:fissure` | `FissureSpell` |
| 5 | Geo | `gtbcs_geomancy_plus:geo_conductor` | `GeoConductorSpell` |
| 6 | Geo | `gtbcs_geomancy_plus:petrivise` | `PetriviseSpell` |
| 7 | Geo | `gtbcs_geomancy_plus:pillar_of_the_resounding_earth` | `PillarOfTheResoundingEarthSpell` |
| 8 | Geo | `gtbcs_geomancy_plus:seismic_surf` | `SeismicSurfSpell` |
| 9 | Geo | `gtbcs_geomancy_plus:tremor_spike` | `TremorSpikeSpell` |
| 10 | Geo | `gtbcs_geomancy_plus:tremor_step` | `TremorStepSpell` |
| 11 | Holy | `gtbcs_geomancy_plus:solar_beam` | `SolarBeamSpell` |
| 12 | Holy | `gtbcs_geomancy_plus:solar_storm` | `SolarStormSpell` |

Evidências no log: `EXPECTED_REGISTERED_SPELL_CLASS_COUNT=12`; `STATIC_REGISTER_SPELL_INVOCATIONS=12`; `STATIC_INITIALIZER_BRANCHES=0`; `REGISTRY_HELPER_DEFERRED=True`; `ENTRYPOINT_REGISTRAR_REFERENCES=['com/gametechbc/gtbcs_geomancy_plus/GeomancyPlusMod.class']`; `RESULT=EXACT_TWELVE_STATIC_REGISTRY_IDENTITIES_MATCH_PHYSICAL_JAR`.

## Exclusões e limites

- `EarthshatterSpell` está fisicamente no JAR, mas **não entre as 12 inscrições de `GGSpells`**, portanto **+0** spell catalogada para esse protótipo. Earthquake/Storm mixins não são spells próprios adicionais neste registrador.
- 10 Geo + 2 Holy **já integravam a contagem semântica**. Promoção `COUNTED_RELEASE_BOUNDED → COUNTED_EXACT` exclusivamente para identidades estáticas: **+0 novas raízes**, campanha **9/39 exatos / 30/39 pendentes**, mínimos estritos **1851 global / 1849 escopo** inalterados e denominador global desconhecido.
- ⚠️ **Não aprovados:** bootstrap real do modpack, configs Iron's/GTBC, custo/cooldown/dano, efeitos e proteções de world safety, regras de cast-time de Petrivise/Tremor Spike/Pillar, Scroll Forge/foco Geo, Umvuthi loot para Solar Beam/Solar Storm, multiplayer, client/dedicated server real e aquisição Survival.
- Iron's é authority de cast, mana e cooldown; GTBC controla escola Geo e 12 spells; Mowzie's Mobs preserva autoridade sobre mobs/equipamentos, e Black Arcana não duplica efeitos/loot/custos. RPG Skill Tree não assume runtime mágico.
- Stage 06.05 segue 🟡. Nenhum código/asset de terceiros foi incluído; evidência exclusivamente factual/read-only.
