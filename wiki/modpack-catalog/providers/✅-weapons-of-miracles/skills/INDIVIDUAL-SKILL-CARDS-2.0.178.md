# Weapons of Miracles 2.0.178 — 64 fichas individuais

**64/64 IDs com ficha dedicada**: 51 fichas marciais/passivas/movimento/tecnológicas novas + 13 ações existentes enriquecidas. Este 100% mede presença de ficha por ID com parâmetros e localizadores estáticos; **completude downstream, API mutadora e QA não estão em 100%**. Sem novos objetos na métrica mágica.

![64 de 64 IDs com ficha dedicada; campos downstream parciais](../../../meta/progress/complete.svg)

JAR exato SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`; 58 JSONs próprios + seis ausentes. [Proveniência, consumidores base e limites](EXACT-TECHNICAL-BOUNDARIES-2.0.178.md).

| ID exato | Categoria | Disposição mágica | Parâmetros próprios | Classe concreta |
|---|---|---|---|---|
| [`wom:ender_step`](../actions/ender-step.md) | Dodge | `COUNTED_EXACT` | `consumption`, `xp_requirement` | `EnderStepSkill` |
| [`wom:ender_obscuris`](../actions/ender-obscuris.md) | Dodge | `COUNTED_EXACT` | `consumption`, `xp_requirement` | `EnderObscurisSkill` |
| [`wom:shadow_step`](../actions/shadow-step.md) | Dodge | `COUNTED_EXACT` | `consumption`, `xp_requirement` | `ShadowStepSkill` |
| [`wom:precise_roll`](individual/precise-roll.md) | Dodge | `EXCLUDED` | `consumption`, `xp_requirement` | `PreciseRollSkill` |
| [`wom:dodge_master`](individual/dodge-master.md) | Dodge | `EXCLUDED` | `consumption`, `xp_requirement` | `DodgeMasterSkill` |
| [`wom:bull_charge`](individual/bull-charge.md) | Dodge | `EXCLUDED` | `consumption`, `xp_requirement` | `RavangerForceSkill` |
| [`wom:time_travel`](../actions/time-travel.md) | Dodge | `COUNTED_EXACT` | `consumption`, `xp_requirement` | `TimeTravelSkill` |
| [`wom:punishment_kick`](individual/punishment-kick.md) | Dodge | `EXCLUDED` | `consumption`, `xp_requirement` | `PunishmentKickSkill` |
| [`wom:counter_attack`](individual/counter-attack.md) | Guard | `EXCLUDED` | `xp_requirement`, `penalizer` | `CounterAttack` |
| [`wom:vengeful_parry`](individual/vengeful-parry.md) | Guard | `EXCLUDED` | `xp_requirement`, `penalizer` | `VengefulParry` |
| [`wom:perfect_bulwark`](individual/perfect-bulwark.md) | Guard | `EXCLUDED` | `xp_requirement`, `penalizer` | `PerfectBulwarkSkill` |
| [`wom:soul_protection`](individual/soul-protection.md) | Guard | `EXCLUDED` | `xp_requirement` | `SoulProtectionSkill` |
| [`wom:shulker_cloak`](individual/shulker-cloak.md) | Guard | `EXCLUDED` | `xp_requirement` | `ShulkerCloakSkill` |
| [`wom:buster_parade`](individual/buster-parade.md) | Guard | `EXCLUDED` | `xp_requirement` | `DreadFullBusterSkill` |
| [`wom:arrow_tenacity`](individual/arrow-tenacity.md) | Passive | `EXCLUDED` | `xp_requirement` | `ArrowTenacitySkill` |
| [`wom:pain_anticipation`](individual/pain-anticipation.md) | Passive | `EXCLUDED` | `xp_requirement` | `PainAnticipationSkill` |
| [`wom:latent_retribution`](individual/latent-retribution.md) | Passive | `EXCLUDED` | `xp_requirement` | `LatentRetributionSkill` |
| [`wom:vampirize`](individual/vampirize.md) | Passive | `EXCLUDED` | `xp_requirement` | `VampirizeSkill` |
| [`wom:critical_knowledge`](individual/critical-knowledge.md) | Passive | `EXCLUDED` | `xp_requirement` | `CriticalKnowledgeSkill` |
| [`wom:heart_shield`](individual/heart-shield.md) | Passive | `EXCLUDED` | `xp_requirement` | `HeartShieldSkill` |
| [`wom:mindset`](individual/mindset.md) | Passive | `EXCLUDED` | `xp_requirement` | `MindSetSkill` |
| [`wom:adrenaline`](individual/adrenaline.md) | Passive | `EXCLUDED` | `xp_requirement` | `AdrenalineSkill` |
| [`wom:dancing_blade`](individual/dancing-blade.md) | Passive | `EXCLUDED` | `xp_requirement` | `DancingBladeSkill` |
| [`wom:meditation`](individual/meditation.md) | Passive | `EXCLUDED` | `xp_requirement` | `MeditationSkill` |
| [`wom:inner_growth`](individual/inner-growth.md) | Passive | `EXCLUDED` | `xp_requirement` | `InnerGrowthSkill` |
| [`wom:dopamine`](individual/dopamine.md) | Passive | `EXCLUDED` | `xp_requirement` | `DopamineSkill` |
| [`wom:manipulator`](individual/manipulator.md) | Passive | `EXCLUDED` | `xp_requirement` | `ManipulatorSkill` |
| [`wom:lethal_focus`](individual/lethal-focus.md) | Passive | `EXCLUDED` | `xp_requirement` | `LethalFocusSkill` |
| [`wom:spider_techniques`](individual/spider-techniques.md) | Mover | `EXCLUDED` | `xp_requirement` | `SpiderTechniquesSkill` |
| [`wom:aqua_maneuvre`](individual/aqua-maneuvre.md) | Mover | `EXCLUDED` | `xp_requirement` | `AquaManeuvreSkill` |
| [`wom:natural_sprinter`](individual/natural-sprinter.md) | Mover | `EXCLUDED` | `xp_requirement` | `NaturalSprinterSkill` |
| [`wom:lunatic_vivacity`](individual/lunatic-vivacity.md) | Identity | `EXCLUDED` | `xp_requirement` | `LunaticVivacitySkill` |
| [`wom:voodoo_magic`](../actions/voodoo-magic.md) | Identity | `COUNTED_EXACT` | `xp_requirement`, `attribute_modifiers` | `VoodooMagicSkill` |
| [`wom:back_and_forth`](individual/back-and-forth.md) | Identity | `EXCLUDED` | `xp_requirement` | `BackAndForthSkill` |
| [`wom:shooting_style`](individual/shooting-style.md) | Identity | `EXCLUDED` | `xp_requirement` | `ShootingStyleSkill` |
| [`wom:proximity_exploiter`](individual/proximity-exploiter.md) | Identity | `EXCLUDED` | `xp_requirement` | `ProximityExploiterSkill` |
| [`wom:all_eyes_on_you`](individual/all-eyes-on-you.md) | Identity | `EXCLUDED` | `xp_requirement` | `AllEyesOnYouSkill` |
| [`wom:all_eyes_on_me`](individual/all-eyes-on-me.md) | Identity | `EXCLUDED` | `xp_requirement` | `AllEyesOnMeSkill` |
| [`wom:avatar_of_might`](../actions/avatar-of-might.md) | Identity | `COUNTED_EXACT` | ausente | `AvatarOfMightSkill` |
| [`wom:charybdis`](individual/charybdis.md) | Weapon Innate | `EXCLUDED` | `consumption` | `CharybdisSkill` |
| [`wom:agony_plunge`](../actions/sky-dive.md) | Weapon Innate | `COUNTED_EXACT` | `consumption`, `max_stacks` | `SkyDiveSkill` |
| [`wom:true_berserk`](../actions/true-wrath.md) | Weapon Innate | `COUNTED_EXACT` | `consumption`, `max_duration` | `TrueBerserkSkill` |
| [`wom:demonic_ascension`](../actions/demonic-ascension.md) | Weapon Innate | `COUNTED_EXACT` | `consumption`, `max_duration` | `DemonicAscensionSkill` |
| [`wom:plunder_perdition`](../actions/ender-ritual.md) | Weapon Innate | `COUNTED_EXACT` | `consumption`, `max_stacks` | `EnderRitualSkill` |
| [`wom:regierung`](individual/regierung.md) | Weapon Innate | `EXCLUDED` | `consumption`, `max_duration` | `RegierungSkill` |
| [`wom:sakura_state`](individual/sakura-state.md) | Weapon Innate | `EXCLUDED` | `consumption`, `max_stacks` | `SakuraStateSkill` |
| [`wom:ender_blast`](individual/ender-blast.md) | Weapon Innate | `EXCLUDED` | `consumption`, `max_stacks` | `EnderBlastSkill` |
| [`wom:ender_fusion`](individual/ender-fusion.md) | Weapon Innate | `EXCLUDED` | `consumption`, `max_stacks` | `EnderFusionSkill` |
| [`wom:lunar_eclipse`](../actions/lunar-eclipse.md) | Weapon Innate | `COUNTED_EXACT` | `consumption`, `max_stacks` | `LunarEclipseSkill` |
| [`wom:solar_arcano`](../actions/solar-arcano.md) | Weapon Innate | `COUNTED_EXACT` | `consumption` | `SolarArcanaSkill` |
| [`wom:rechargement`](individual/rechargement.md) | Weapon Innate | `EXCLUDED` | `consumption` | `RechargementSkill` |
| [`wom:orbital_beam`](individual/orbital-beam.md) | Weapon Innate | `EXCLUDED` | `consumption`, `max_stacks` | `OrbitalBeamSkill` |
| [`wom:flash_mutilation`](../actions/flash-mutilation.md) | Weapon Innate | `CONDITIONAL` | `consumption`, `max_stacks` | `FlashMutilatorSkill` |
| [`wom:unbreakable`](individual/unbreakable.md) | Weapon Innate | `EXCLUDED` | `consumption`, `max_stacks` | `UnbreakableSkill` |
| [`wom:satsujin_passive`](individual/satsujin-passive.md) | Weapon Passive | `EXCLUDED` | `consumption` | `SatsujinPassive` |
| [`wom:demon_mark_passive`](individual/demon-mark-passive.md) | Weapon Passive | `EXCLUDED` | `consumption` | `DemonMarkPassiveSkill` |
| [`wom:ruine_passive`](individual/ruine-passive.md) | Weapon Passive | `EXCLUDED` | objeto vazio | `RuinePassive` |
| [`wom:herrscher_passive`](individual/herrscher-passive.md) | Weapon Passive | `EXCLUDED` | ausente | `HerrscherPassive` |
| [`wom:torment_passive`](individual/torment-passive.md) | Weapon Passive | `EXCLUDED` | objeto vazio | `TormentPassiveSkill` |
| [`wom:lunar_echo_passive`](individual/lunar-echo-passive.md) | Weapon Passive | `EXCLUDED` | ausente | `LunarEchoPassiveSkill` |
| [`wom:solar_passive`](individual/solar-passive.md) | Weapon Passive | `EXCLUDED` | objeto vazio | `SolarPassiveSkill` |
| [`wom:napoleon_passive`](individual/napoleon-passive.md) | Weapon Passive | `EXCLUDED` | ausente | `NapoleonBusterPassive` |
| [`wom:evil_tachi_passive`](individual/evil-tachi-passive.md) | Weapon Passive | `EXCLUDED` | ausente | `EvilTachiPassive` |
| [`wom:unbreakable_passive`](individual/unbreakable-passive.md) | Weapon Passive | `EXCLUDED` | ausente | `UnbreakablePassive` |

Os 51 EXCLUDED estão excluídos **somente do numerador mágico**, permanecendo integralmente no escopo de integração técnica. Flash Mutilation segue CONDITIONAL pela aquisição normal de Nova aberta; a ficha técnica não resolve essa pendência.

[Manifesto com assinaturas, descritores e PCs](individual-skill-cards-2.0.178.json) · [disposição semântica anterior](SKILL-DISPOSITION-2.0.178.md) · [progresso geral e por mod](../../../meta/PROGRESSO-CATALOGO-ATUAL.md).
