# Legendary Spellbooks 0.3.2 — prova exata de 30 feitiços físicos

**✅ `COUNTED_EXACT` para 30/30 registros estáticos incondicionais** no JAR oficial fisicamente correspondente. Campanha de 39 providers: **21/39 exatos / 18/39 pendentes**. Novas raízes semânticas: **+0**, pois as 30 identidades já estavam no ledger. Mínimos estritos **1857 global / 1855 escopo** inalterados. Compatibilidade de runtime/Survival **⚠️**.

## Proveniência física e limites

- Modlist física do sibling, item **#372**, `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, mod ID `legendary_spellbooks`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`.
- Distribuição [CurseForge file 8255715](https://www.curseforge.com/minecraft/mc-mods/legendary-spellbooks/files/8255715), **510127 bytes**, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, igual à modlist física do pack.
- [Primeiro discovery Java 21 #38452766615](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38452766615) **SUCCESS**; [auditoria Java 21 com 30 asserções de ResourceLocation #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) **SUCCESS**.
- Workflow temporário clean-room preservado apenas na branch [`audit/legendary-spellbooks-032-20261013`](https://github.com/Gustavaopere/Black-Arcana/tree/audit/legendary-spellbooks-032-20261013). Nenhum JAR/binário, bytecode ou recurso de terceiros é distribuído pelo Black Arcana.

## Topologia compilada de registry

- Entry point `dev.higurashi.legendary_spellbooks.LegendarySpellbooks` chama `LSSpellRegistry.register`.
- `dev.higurashi.legendary_spellbooks.registries.LSSpellRegistry` usa `DeferredRegister<AbstractSpell>` com `SpellRegistry.SPELL_REGISTRY_KEY` e namespace `legendary_spellbooks`; seu wrapper compilado é `register(AbstractSpell)`.
- O inicializador instancia e registra exatamente **30 classes**, com **30** chamadas ao wrapper e nenhuma instrução de desvio condicional nesse bloco; 30 IDs são distintos.
- Cada classe possui `ResourceLocation` literal (namespace + sufixo) em inicializador estático, transmitido à base do spell. As escolas abaixo foram verificadas como **referências compiladas a recursos escolares padrão**, não prova de configuração efetiva em runtime.
- A classe `PossessedFallingSoulBladeSpell` citada no source não participa do registrador binário ativo; não é uma 31ª magia.

## 30 identidades verificadas individualmente

| # | Nome catalogado | ResourceLocation física | Classe compilada | Ficha |
|---:|---|---|---|---|
| 1 | Annihilation Arrow | `legendary_spellbooks:annihilation_arrow` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationArrowSpell` | [Ficha](annihilation/annihilation-arrow.md) |
| 2 | Annihilation Beam | `legendary_spellbooks:annihilation_beam` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationBeamSpell` | [Ficha](annihilation/annihilation-beam.md) |
| 3 | Annihilation Bomb | `legendary_spellbooks:annihilation_bomb` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationBombSpell` | [Ficha](annihilation/annihilation-bomb.md) |
| 4 | Annihilation Shockwave | `legendary_spellbooks:annihilation_shockwave` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationShockwaveSpell` | [Ficha](annihilation/annihilation-shockwave.md) |
| 5 | Annihilation Resonance | `legendary_spellbooks:annihilation_resonance` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationResonanceSpell` | [Ficha](annihilation/annihilation-resonance.md) |
| 6 | Annihilation Geyser | `legendary_spellbooks:annihilation_geyser` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationGeyserSpell` | [Ficha](annihilation/annihilation-geyser.md) |
| 7 | Summon Flameborn Knights | `legendary_spellbooks:summon_flameborn_knights` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.SummonFlamebornKnightsSpell` | [Ficha](annihilation/summon-flameborn-knights.md) |
| 8 | Release Riftwalker Predator | `legendary_spellbooks:release_riftwalker_predator` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.ReleaseRiftwalkerPredatorSpell` | [Ficha](annihilation/release-riftwalker-predator.md) |
| 9 | Flameborn Drift | `legendary_spellbooks:flameborn_drift` | `dev.higurashi.legendary_spellbooks.common.spells.annihilation.FlamebornDriftSpell` | [Ficha](annihilation/flameborn-drift.md) |
| 10 | Possessed Soul Blade | `legendary_spellbooks:possessed_soul_blade` | `dev.higurashi.legendary_spellbooks.common.spells.blood.PossessedSoulBladeSpell` | [Ficha](blood/possessed-soul-blade.md) |
| 11 | Hematite Trishula | `legendary_spellbooks:hematite_trishula` | `dev.higurashi.legendary_spellbooks.common.spells.blood.HematiteTrishulaSpell` | [Ficha](blood/hematite-trishula.md) |
| 12 | Possessed Wings | `legendary_spellbooks:possessed_wing` | `dev.higurashi.legendary_spellbooks.common.spells.blood.PossessedWingSpell` | [Ficha](blood/possessed-wing.md) |
| 13 | Collapsed Kingdom's Legion | `legendary_spellbooks:collapsed_kingdoms_legion` | `dev.higurashi.legendary_spellbooks.common.spells.evocation.CollapsedKingdomsLegionSpell` | [Ficha](evocation/collapsed-kingdoms-legion.md) |
| 14 | Flame Eater | `legendary_spellbooks:flame_eater` | `dev.higurashi.legendary_spellbooks.common.spells.fire.FlameEaterSpell` | [Ficha](fire/flame-eater.md) |
| 15 | Flame Sector | `legendary_spellbooks:flame_sector` | `dev.higurashi.legendary_spellbooks.common.spells.fire.FlameSectorSpell` | [Ficha](fire/flame-sector.md) |
| 16 | Sentinel Saturation | `legendary_spellbooks:sentinel_saturation` | `dev.higurashi.legendary_spellbooks.common.spells.fire.SentinelSaturationSpell` | [Ficha](fire/sentinel-saturation.md) |
| 17 | Glacier Eruption | `legendary_spellbooks:glacier_eruption` | `dev.higurashi.legendary_spellbooks.common.spells.ice.GlacierEruptionSpell` | [Ficha](ice/glacier-eruption.md) |
| 18 | Glacier Ringburst | `legendary_spellbooks:glacier_ringburst` | `dev.higurashi.legendary_spellbooks.common.spells.ice.GlacierRingburstSpell` | [Ficha](ice/glacier-ringburst.md) |
| 19 | Cloud Rail | `legendary_spellbooks:cloud_rail` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.CloudRailSpell` | [Ficha](lightning/cloud-rail.md) |
| 20 | Cloud Ring | `legendary_spellbooks:cloud_ring` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.CloudRingSpell` | [Ficha](lightning/cloud-ring.md) |
| 21 | Nimbus Array | `legendary_spellbooks:nimbus_array` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.NimbusArraySpell` | [Ficha](lightning/nimbus-array.md) |
| 22 | Triple Nimbus Array | `legendary_spellbooks:triple_nimbus_array` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.TripleNimbusArraySpell` | [Ficha](lightning/triple-nimbus-array.md) |
| 23 | Thunder Fanburst | `legendary_spellbooks:thunder_fanburst` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.ThunderFanburstSpell` | [Ficha](lightning/thunder-fanburst.md) |
| 24 | Tornado | `legendary_spellbooks:tornado` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.TornadoSpell` | [Ficha](lightning/tornado.md) |
| 25 | Quad Tornado | `legendary_spellbooks:quad_tornado` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.QuadTornadoSpell` | [Ficha](lightning/quad-tornado.md) |
| 26 | Energy Beam | `legendary_spellbooks:energy_beam` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.EnergyBeamSpell` | [Ficha](lightning/energy-beam.md) |
| 27 | Cumulo Charge | `legendary_spellbooks:cumulo_charge` | `dev.higurashi.legendary_spellbooks.common.spells.lightning.CumuloChargeSpell` | [Ficha](lightning/cumulo-charge.md) |
| 28 | Ambush Thorns | `legendary_spellbooks:ambush_thorns` | `dev.higurashi.legendary_spellbooks.common.spells.nature.AmbushThornsSpell` | [Ficha](nature/ambush-thorns.md) |
| 29 | Overgrown Shockwave | `legendary_spellbooks:overgrown_shockwave` | `dev.higurashi.legendary_spellbooks.common.spells.nature.OvergrownShockwaveSpell` | [Ficha](nature/overgrown-shockwave.md) |
| 30 | Fossilized Fury | `legendary_spellbooks:fossilized_fury` | `dev.higurashi.legendary_spellbooks.common.spells.nature.FossilizedFurySpell` | [Ficha](nature/fossilized-fury.md) |

**Distribuição no registry:** Annihilation 9; Blood/dual-school 3; Evocation 1; Fire 3; Ice 2; Lightning 9; Nature 3.

**Escolas verificadas no bytecode:** Annihilation aponta a `LSSchoolRegistry.ANNIHILATION_RESOURCE`; Blood, Evocation, Fire, Ice, Lightning e Nature apontam a recursos `SchoolRegistry` do Iron's. `PossessedSoulBladeSpell` referencia explicitamente `SchoolRegistry.EVOCATION_RESOURCE` e `SchoolRegistry.BLOOD`, coerente com tratamento dual-school catalogado na fonte; o nível/condição efetiva de cada escola não foi testado no modpack.

**PUBLISHER_EQUALS_PHYSICAL_SHA1=PASS**

**PHYSICAL_SPELL_REGISTRATIONS=30**

**STATIC_INITIALIZER_BRANCHES=0**

**NEW_SEMANTIC_ROOTS=0**

**EXACT_STATIC_REGISTRY_AUDIT=PASS**

**RUNTIME_SURVIVAL_NOT_VERIFIED=TRUE**

## Exclusões, authority e gates

- `PossessedFallingSoulBladeSpell` é excluída do inventário ativo e `PossessedWingSpell` tem ID exato singular `legendary_spellbooks:possessed_wing` — nomes visíveis no plural não determinam IDs.
- `Annihilation` é escola própria do provider. Legendary Monsters conserva autoridade sobre encounters/mobs; Iron's Spells sobre casting, mana/cooldown e slots; Legendary Spellbooks sobre os 30 spells e seus efeitos/loot/affinity. Black Arcana conserva autoridade sobre seu runtime próprio. RPG Skill Tree é somente provider sibling de progressão/perks/gates.
- **⚠️** O pin source do addon usava Iron's **3.16.1** e Legendary Monsters **2.1.14**, enquanto o modpack físico registra Iron's **3.16.3** e Legendary Monsters **2.2.2**. Esta auditoria **não** prova execução, carga com essas dependências, configs ativos, acquisition/Survival, spellbook/loot, mana, cooldown, summons, duração, multiplayer ou deduplicação causal.
- **⚠️** Os pontos de QA source-pinned de Glacier Ringburst (max-level versus loot), Stormbound tooltip, Fossilized Fury e Annihilation Resonance continuam condicionados até QA funcional.
- Não copiar código/assets do provider, inventar APIs ou implementar bridge de loot/weather/summon/affinity sem contrato real.
