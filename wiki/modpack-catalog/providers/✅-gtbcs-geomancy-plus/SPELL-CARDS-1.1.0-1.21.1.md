# GTBC's Geomancy Plus — 12 fichas individuais de magia (1.1.0-1.21.1)

Status: **✅ 12/12 objetos catalogados / `COUNTED_RELEASE_BOUNDED` / sem validação física de execução no modpack.**

## Fontes e regra de contagem

- **Versão identificada na modlist física congelada:** `gtbcs_geomancy_plus-1.1.0-1.21.1.jar`; mod id `gtbcs_geomancy_plus`. Minecraft 1.21.1, NeoForge.
- **Registry examinado:** `GGSpells` do artefato publicado CurseForge File `7041615`; 12 `Supplier<AbstractSpell>` mapeados a 12 `registerSpell(...)`, com zero branches no inicializador. Consulta: [inventário canônico do provider](README.md) e [auditoria de JAR/release](EXACT-1.1.0-ARTIFACT-AUDIT.md).
- **Provenance:** hash do artefato publisher SHA-1 `67e9652799f35f1fbd09968da6f400d0229f5599`. Este trabalho não extraiu nem revalidou o JAR da instalação. Preservar `COUNTED_RELEASE_BOUNDED` e o gate de execução física.
- **Escopo:** dez registros Geo e dois Holy. Cada root de `GGSpells` aparece uma vez; subclasses não registradas, escolas, mixins, loot, itens e feitiços preexistentes do Iron's não somam objetos adicionais.
- **Nomenclatura:** os cabeçalhos combinam o mod id declarado e o root exato do registry para indexação. O arquivo **não** prova a resolução final de `ResourceLocation`, configuração efetiva, interface de conjuração, aquisição no mundo ou comportamento vivo do servidor, ainda pendentes em QA.

## Índice das 12 identidades

| Nº | Família | Root do registry | Classe concreta |
|---:|---|---|---|
| 1 | Geo | `chunker` | `ChunkerSpell` |
| 2 | Geo | `dripstone_bolt` | `DripstoneBoltSpell` |
| 3 | Geo | `eroding_boulder` | `ErodingBoulderSpell` |
| 4 | Geo | `fissure` | `FissureSpell` |
| 5 | Geo | `geo_conductor` | `GeoConductorSpell` |
| 6 | Geo | `petrivise` | `PetriviseSpell` |
| 7 | Geo | `pillar_of_the_resounding_earth` | `PillarOfTheResoundingEarthSpell` |
| 8 | Geo | `seismic_surf` | `SeismicSurfSpell` |
| 9 | Geo | `tremor_spike` | `TremorSpikeSpell` |
| 10 | Geo | `tremor_step` | `TremorStepSpell` |
| 11 | Holy | `solar_beam` | `SolarBeamSpell` |
| 12 | Holy | `solar_storm` | `SolarStormSpell` |

## Fichas por spell

### 01 — `gtbcs_geomancy_plus:chunker`

- **Nome editorial do root:** Chunker (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `chunker`
- **Classe concreta:** `ChunkerSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 02 — `gtbcs_geomancy_plus:dripstone_bolt`

- **Nome editorial do root:** Dripstone Bolt (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `dripstone_bolt`
- **Classe concreta:** `DripstoneBoltSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 03 — `gtbcs_geomancy_plus:eroding_boulder`

- **Nome editorial do root:** Eroding Boulder (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `eroding_boulder`
- **Classe concreta:** `ErodingBoulderSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 04 — `gtbcs_geomancy_plus:fissure`

- **Nome editorial do root:** Fissure (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `fissure`
- **Classe concreta:** `FissureSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 05 — `gtbcs_geomancy_plus:geo_conductor`

- **Nome editorial do root:** Geo Conductor (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `geo_conductor`
- **Classe concreta:** `GeoConductorSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 06 — `gtbcs_geomancy_plus:petrivise`

- **Nome editorial do root:** Petrivise (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `petrivise`
- **Classe concreta:** `PetriviseSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Exceção de cast-time documentada:** 1.1.0: a release registra exceção à redução de cast-time, para evitar descompasso de animação; não forçar redução por adaptador.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 07 — `gtbcs_geomancy_plus:pillar_of_the_resounding_earth`

- **Nome editorial do root:** Pillar Of The Resounding Earth (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `pillar_of_the_resounding_earth`
- **Classe concreta:** `PillarOfTheResoundingEarthSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Exceção de cast-time documentada:** 1.1.0: a release registra exceção à redução de cast-time, para evitar descompasso de animação; não forçar redução por adaptador.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 08 — `gtbcs_geomancy_plus:seismic_surf`

- **Nome editorial do root:** Seismic Surf (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `seismic_surf`
- **Classe concreta:** `SeismicSurfSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 09 — `gtbcs_geomancy_plus:tremor_spike`

- **Nome editorial do root:** Tremor Spike (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `tremor_spike`
- **Classe concreta:** `TremorSpikeSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Exceção de cast-time documentada:** 1.1.0: a release registra exceção à redução de cast-time, para evitar descompasso de animação; não forçar redução por adaptador.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 10 — `gtbcs_geomancy_plus:tremor_step`

- **Nome editorial do root:** Tremor Step (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Geo
- **Root exato de registro:** `tremor_step`
- **Classe concreta:** `TremorStepSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os dez Geo herdam os gates Iron's de crafting/enabled/player (`allowCrafting`, `isEnabled`, `canBeCraftedBy`) sem override provider-native observado; rota estrutural de foco por `mowziesmobs:bluff_rod` e `#gtbcs_geomancy_plus:geo_focus`.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 11 — `gtbcs_geomancy_plus:solar_beam`

- **Nome editorial do root:** Solar Beam (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Holy
- **Root exato de registro:** `solar_beam`
- **Classe concreta:** `SolarBeamSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os identificadores `gtbcs_geomancy_plus:solar_beam` e `gtbcs_geomancy_plus:solar_storm` constam em dados de loot de Umvuthi; a release documenta obtenção após derrotar esse boss. Taxas/drops reais e gates Iron's efetivos continuam em QA.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.


### 12 — `gtbcs_geomancy_plus:solar_storm`

- **Nome editorial do root:** Solar Storm (normalização de leitura, não tradução/localização oficial).
- **Família confirmada:** Holy
- **Root exato de registro:** `solar_storm`
- **Classe concreta:** `SolarStormSpell`
- **Confiança:** `COUNTED_RELEASE_BOUNDED`; identidade registrada na release exata e materializada no catálogo, sem promoção para `COUNTED_EXACT` do JAR local.
- **Aquisição / gate sustentado:** Os identificadores `gtbcs_geomancy_plus:solar_beam` e `gtbcs_geomancy_plus:solar_storm` constam em dados de loot de Umvuthi; a release documenta obtenção após derrotar esse boss. Taxas/drops reais e gates Iron's efetivos continuam em QA.
- **Política individual de cast-time:** não estabelecida nesta auditoria para este registro.
- **Mecânica individual, targeting, dano, duração, rank, custo, cooldown e efeitos de mundo:** não comprovados pela base documental aqui utilizada; não inferir do nome nem duplicar o casting/mana do Iron's.
- **Proprietário semântico:** GTBC's Geomancy Plus; hospedeiro de casting, recursos e cooldown genérico: Iron's. Integração de conteúdo/loot de Mowzie permanece provider-native.

## Não contar duas vezes

- `EarthshatterSpell` existe como classe, mas não integra os 12 fornecedores registrados de `GGSpells`: **excluído (+0)**.
- **Earthquake** e **Stomp** são feitiços já pertencentes ao Iron's cuja escola pode ser reatribuída a Geo pelo addon: não constituem identidades novas deste provider.
- `EarthquakeMixin` e `StormSpellMixin` não são registros `GGSpells`; adaptar/observar um cast existente não cria outro.
- School, foco, runa, orbe, Codex, The Stonecaller, atributos Geo, loot de Umvuthi, projéteis e efeitos são conteúdos/superfícies próprios mas não registros extras na métrica de spell roots.
- Nomes adicionais da página genérica de projeto ou builds 1.20.1 mais recentes não substituem o registry de 1.1.0-1.21.1.

## Matriz de estado

| Dimensão | Estado |
|---|---|
| Fichas da release | ✅ **12/12** |
| Identidades de root novas neste PR | **0** — já incluídas no mínimo estrito reconstruível |
| Prova do registry do artefato publisher da versão | ✅ 12 campos / 12 registros / 0 branches |
| Byte equality do JAR local, configuração implantada e casts em Survival | ⚠️ **PENDENTE** |
| Compatibilidade host Iron's 3.16.3, Mowzie 1.8.2, GTBC SpellLib 2.2.0 | ⚠️ **PENDENTE em runtime** |
| Stage 06.05 / Stage 07 | 🟡 auditoria / ⛔ bloqueada respectivamente |

**Autoridade:** a modlist/JAR físico define presença/versão; o registry auditado define os roots; os providers mantêm a execução nativa. Black Arcana conserva exclusivamente seu casting, hazards, Corruption, Strain e `WorldEffectPolicy` para efeitos próprios. RPG Skill Tree fornece somente progressão/atributos/gates por contrato real. Esta documentação não instala código nem duplica pipeline de magia.
