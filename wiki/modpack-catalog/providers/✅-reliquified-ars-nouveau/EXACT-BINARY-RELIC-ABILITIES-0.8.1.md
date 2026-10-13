# Reliquified Ars Nouveau 0.8.1 — 19 habilidades de relíquias SHA-exatas

**✅ `COUNTED_EXACT` em identidade estática de 19 itens nativos Relics/Ars e 19 raízes `AbilityTemplate.builder`**, não spells adicionais de Ars Nouveau. Campanha de 39 providers: **25/39 exatos / 14/39 pendentes**. Acréscimo de raízes **+0**, pois as 19 já estavam no ledger. Mínimos semânticos **1857 global / 1855 escopo** preservados. Runtime e Survival ⚠️.

## Autoridade do artefato

- Modlist física sibling: `reliquified_ars_nouveau-1.21.1-0.8.1.jar`, mod ID `reliquified_ars_nouveau`, SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579`.
- [CurseForge file 8104341](https://www.curseforge.com/minecraft/mc-mods/reliquified-ars-nouveau/files/8104341), **1183912 bytes**, SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` corresponde ao JAR físico 0.8.1 para NeoForge 1.21.1.
- [Discovery Java21 #38461345067](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461345067), [enumeração classes e ability builders #38461576047](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461576047) e [19 vínculos estritos #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129) **SUCCESS**.
- O workflow temporário clean-room está apenas em [`audit/reliquified-ars-nouveau-081-20261013`](https://github.com/Gustavaopere/Black-Arcana/tree/audit/reliquified-ars-nouveau-081-20261013), sem JAR/bytecode/código externo na `main`.

## Registro e raízes compiladas

`it.hurts.shatterbyte.reliquified_ars_nouveau.init.ItemRegistry` registra **19 `DeferredHolder<Item>`** via `DeferredRegister<Item>`, com 19 identificadores `reliquified_ars_nouveau:*` e sem branches nesse inicializador. Cada uma das **19 classes concretas** de relíquia tem exatamente uma chamada compilada de `AbilityTemplate.builder`; o ID de habilidade primária é o primeiro literal associado ao builder na classe, comprovado individualmente.

A presença de sub-habilidades, modificadores de rank, estatísticas, triggers e outputs nas mesmas classes não cria uma nova identidade semântica principal. Se uma habilidade delega a um spell Ars, não duplicar esse spell. As rotas de loot constam na [reconciliação source-pinned](README.md), mas a mutação efetiva do loot do modpack não foi inspecionada em execução.

| # | Item físico | Classe concreta | ID de habilidade principal | Nome localizado | Ficha |
|---:|---|---|---|---|---|
| 1 | `reliquified_ars_nouveau:architects_staff` | `items.ArchitectsStaffItem` | `bridgecraft` | Arcane Masonry | [Ficha](abilities/architects-staff.md) |
| 2 | `reliquified_ars_nouveau:archmage_glove` | `items.hands.ArchmageGloveItem` | `multicasted` | Echo Spell | [Ficha](abilities/archmage-glove.md) |
| 3 | `reliquified_ars_nouveau:ballistarian_bracer` | `items.bracelet.BallistarianBracerItem` | `ballistary` | Spectral Volley | [Ficha](abilities/ballistarian-bracer.md) |
| 4 | `reliquified_ars_nouveau:cloak_of_concealment` | `items.back.CloakOfConcealmentItem` | `absorption` | Mana Barrier | [Ficha](abilities/cloak-of-concealment.md) |
| 5 | `reliquified_ars_nouveau:emblem_of_assault` | `items.charm.EmblemOfAssaultItem` | `onslaught` | Battle Echo | [Ficha](abilities/emblem-of-assault.md) |
| 6 | `reliquified_ars_nouveau:emblem_of_defense` | `items.charm.EmblemOfDefenseItem` | `sentinel` | Runic Watch | [Ficha](abilities/emblem-of-defense.md) |
| 7 | `reliquified_ars_nouveau:emblem_of_devotion` | `items.charm.EmblemOfDevotionItem` | `devotion` | Orbit of Devotion | [Ficha](abilities/emblem-of-devotion.md) |
| 8 | `reliquified_ars_nouveau:flaming_bracer` | `items.bracelet.FlamingBracerItem` | `pyroclastic` | Pyroclastics | [Ficha](abilities/flaming-bracer.md) |
| 9 | `reliquified_ars_nouveau:horn_of_the_wild_hunter` | `items.head.HornOfWildHunterItem` | `summoner` | Call of the Pack | [Ficha](abilities/horn-of-the-wild-hunter.md) |
| 10 | `reliquified_ars_nouveau:illusionists_mantle` | `items.back.IllusionistsMantleItem` | `deception` | Deceptive Response | [Ficha](abilities/illusionists-mantle.md) |
| 11 | `reliquified_ars_nouveau:mana_ring` | `items.ring.ManaRingItem` | `resonance` | Arcane Reserve | [Ficha](abilities/mana-ring.md) |
| 12 | `reliquified_ars_nouveau:quantum_bubble` | `items.head.QuantumBubbleItem` | `stasis` | Quantification | [Ficha](abilities/quantum-bubble.md) |
| 13 | `reliquified_ars_nouveau:ring_of_last_will` | `items.ring.RingOfLastWillItem` | `last_will` | Last Will | [Ficha](abilities/ring-of-last-will.md) |
| 14 | `reliquified_ars_nouveau:ring_of_thrift` | `items.ring.RingOfThriftItem` | `thrift` | Mana Thrift | [Ficha](abilities/ring-of-thrift.md) |
| 15 | `reliquified_ars_nouveau:spiked_cloak` | `items.back.SpikedCloakItem` | `thorn_burst` | Thorn Burst | [Ficha](abilities/spiked-cloak.md) |
| 16 | `reliquified_ars_nouveau:staff_of_the_spectral_walker` | `items.StaffOfTheSpectralWalkerItem` | `spectral` | Spectral Dash | [Ficha](abilities/staff-of-the-spectral-walker.md) |
| 17 | `reliquified_ars_nouveau:whirling_broom` | `items.WhirlingBroomItem` | `broom` | Whirling Flight | [Ficha](abilities/whirling-broom.md) |
| 18 | `reliquified_ars_nouveau:whirlisprig_petals` | `items.WhirlisprigPetalsItem` | `petal_lift` | Petal Lift | [Ficha](abilities/whirlisprig-petals.md) |
| 19 | `reliquified_ars_nouveau:wing_of_the_wild_stalker` | `items.body.WingWildStalkerItem` | `wild_flight` | Predatory Flight | [Ficha](abilities/wing-of-the-wild-stalker.md) |

**PUBLISHER_EQUALS_PHYSICAL_SHA1=PASS**

**PHYSICAL_RELIC_ITEM_REGISTRATIONS=19**

**UNIQUE_ROOT_ABILITY_BUILDERS=19**

**STATIC_REGISTRY_BRANCHES=0**

**NEW_SEMANTIC_ROOTS=0**

**EXACT_STATIC_REGISTRY_AUDIT=PASS**

**RUNTIME_SURVIVAL_NOT_VERIFIED=TRUE**

## Boundary

Reliquified Ars Nouveau responde pelos 19 itens e implementações de suas abilities específicas; **Relics** pelo framework/progressão de relíquias; **Ars Nouveau** pelo casting, glyphs, source/mana e seus recursos nativos. **Black Arcana** mantém autoridade sobre seu runtime. **RPG Skill Tree** é sibling de progressão/Mastery/perks/gates por contratos reais, não executor dessas habilidades.

**⚠️** Prova estática não certifica boot/cast em cliente e servidor com Relics 0.12.8 / Ars Nouveau 5.13.1, aquisição em Survival, loot injection efetiva, custos, cooldown, autorizações, efeitos, persistência, PvP, multiplayer, reload nem deduplicação dinâmica. Sem contrato real de integração, permanecer fail-closed.
