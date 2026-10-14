# Reliquified Ars Nouveau 0.8.1 — fechamento documental das 19 habilidades

**✅ 19/19 raízes de `AbilityTemplate.builder` com identidade estática exata no JAR físico** (prova Java 21 [#38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129)). **✅ 19/19 fichas com engenharia causal source-located** neste PR (3 iniciais + 16 desta continuação). **⚠️** Equivalência dos corpos de métodos ao JAR, estado Relics salvo, config, runtime integrado, Survival/PvP/claims não comprovados. **⛔** Nenhum adapter RPG Mastery/perks homologado.

**Source pin:** `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc` (declara 0.8.1). Mod ID `reliquified_ars_nouveau`, JAR da modlist `reliquified_ars_nouveau-1.21.1-0.8.1.jar`, SHA-1 físico `4be1f4b0fd7fbec6618596e2e7c3705db88a7579`; host Ars Nouveau 5.13.1 / Relics 0.12.8. **+0 novas raízes mágicas.**

| Raiz `AbilityTemplate` | Item e dossiê individual | Mecanismo principal (fonte) |
|---|---|---|
| `bridgecraft` | [architects-staff](abilities/architects-staff.md) | `ArchitectsStaffItem`: bridge em blocos temporários, cobrança de charges e caps 4096 passos |
| `multicasted` | [archmage-glove](abilities/archmage-glove.md) | `ArchmageGloveItem`: SpellCastEvent, filhos em queue/5 ticks, tags e mana refund |
| `ballistary` | [ballistarian-bracer](abilities/ballistarian-bracer.md) | `BallistarianBracerItem`: EntityJoinLevelEvent → projéteis phantom → LivingDamageEvent.Post |
| `absorption` | [cloak-of-concealment](abilities/cloak-of-concealment.md) | `CloakOfConcealmentItem`: LivingIncomingDamageEvent, absorção por mana, cura e distribuição |
| `onslaught` | [emblem-of-assault](abilities/emblem-of-assault.md) | `EmblemOfAssaultItem`: SpellCostCalcEvent, Touch proc, retarget e chain |
| `sentinel` | [emblem-of-defense](abilities/emblem-of-defense.md) | `EmblemOfDefenseItem`: spell Touch em agressor, resistência, nullification |
| `devotion` | [emblem-of-devotion](abilities/emblem-of-devotion.md) | `EmblemOfDevotionItem`: orbs por Curios stack-id e limites temporais |
| `pyroclastic` | [flaming-bracer](abilities/flaming-bracer.md) | `FlamingBracerItem`: MAGIC_FIRE, paralysis, FLARE e bônus de dano |
| `summoner` | [horn-of-the-wild-hunter](abilities/horn-of-the-wild-hunter.md) | `HornOfWildHunterItem`: summon wolves, UUID e cleanup dimensional |
| `deception` | [illusionists-mantle](abilities/illusionists-mantle.md) | `IllusionistsMantleItem`: EntityDummy, barrier e fatal exchange |
| `resonance` | [mana-ring](abilities/mana-ring.md) | `ManaRingItem`: mana max/regen, cura→mana, dívida e repayment |
| `stasis` | [quantum-bubble](abilities/quantum-bubble.md) | `QuantumBubbleItem`: captura de projectile, bubble owner e release |
| `last_will` | [ring-of-last-will](abilities/ring-of-last-will.md) | `RingOfLastWillItem`: dano potencialmente fatal, RewindEvent e revenge |
| `thrift` | [ring-of-thrift](abilities/ring-of-thrift.md) | `RingOfThriftItem`: SpellCostCalcEvent.Pre/Post, free casts e refund delayed |
| `thorn_burst` | [spiked-cloak](abilities/spiked-cloak.md) | `SpikedCloakItem`: incoming damage threshold, chimera spikes e chain tags |
| `spectral` | [staff-of-the-spectral-walker](abilities/staff-of-the-spectral-walker.md) | `StaffOfTheSpectralWalkerItem`: IntangibleAir, claims, movement e safe return |
| `broom` | [whirling-broom](abilities/whirling-broom.md) | `WhirlingBroomItem`: WhirlingBroomEntity, saúde, movimento e projectile impact |
| `petal_lift` | [whirlisprig-petals](abilities/whirlisprig-petals.md) | `WhirlisprigPetalsItem`: gravity, charges, directed lift e airborne bonus |
| `wild_flight` | [wing-of-the-wild-stalker](abilities/wing-of-the-wild-stalker.md) | `WingWildStalkerItem`: fall-flying, PvP damage, flight guard e eletricidade condicionada |

## Prioridades de QA e segurança por família

- **Mana/casting:** multicasted child tags (custo zero do filho), Mana Ring debt, Ring of Thrift Pre/Post, emblems scribed; testar refund, reorder de eventos, distribuição e dedup com vários Curios.
- **Vida/morte:** Last Will intercepta dano antes da aplicação; Illusionist's Mantle manipula `LivingDeathEvent`; Cloak consome mana e cura. Testar prioridade cruzada, PvP, totem, morte, reconexão, inventário e cancelamento.
- **Mundo/entidade:** Architect's Staff coloca MageBlock temporário; Spectral Walker cria IntangibleAir, aplica claim check local; Flaming Bracer coloca Magic Fire; lobos, orbes, spikes e bubble de projétil têm lifecycle provider-owned. Conferir safety/claims, unload/save/restart, caps e causalidade da entidade.
- **Problemas localizados no source (não bugs físicos certificados):** `WhirlisprigPetalsItem.use` credita `projectile_reflect` no ramo `directed_lift` mesmo sem reflexão visível nesse corpo; `RingOfThriftItem` usa token pending free casts no player persistent data sem ligação a um cast UUID local. Abordar por QA do host antes de concluir exploit ou comportamento.
- **Runtime:** o Black Arcana é autoridade apenas do seu próprio casting/world-policy/hazards, Relics/Ars/addon controlam essas ações; RPG Skill Tree pertence à progressão. Nenhuma permissão de escrita é deduzida de um atributo/callback do source.

[Identidades físicas](EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) · [Provider](README.md) · [Ledger](../../meta/PERK-READY-COVERAGE-LEDGER.md).
