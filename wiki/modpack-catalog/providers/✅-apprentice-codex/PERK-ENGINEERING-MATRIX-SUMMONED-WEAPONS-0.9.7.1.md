# Apprentice's Codex 0.9.7.1 — matriz causal de armas conjuradas e efeitos derivados

**Checkpoint:** 2026-10-14; modlist sibling `Gustavaopere/neoforge-rpg-skilltree/main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46`: `apprentice_codex-0.9.7.1+mc1.21.1.jar`, mod ID `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`. Mecanismos a partir de source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1).

✅ **83/83** identidades source-catalogadas; 🟡 **54/83** com auditoria causal aprofundada (44 anteriores + 10 nesta matriz); **29/83** pendentes. Não foram registradas novas magias; sem Java/runtime/adapters.

| Spell ID | Dossiê | Método(s) no source | Risco/limite específico |
|---|---|---|---|
| `apprenticecodex:commence_fire` | [commence_fire](lightning/commence-fire.md) | `CommenceFire.onCastWithWeapon/onPreRecastWithWeapon` | recoil/cast damage vs VFX tracer |
| `apprenticecodex:breaching_enemy` | [breaching_enemy](lightning/breaching-enemy.md) | `BreachingEnemyShotgunEntity.fire` | aggregation por pellet/target e impactos de bloco |
| `apprenticecodex:dual_acrobat` | [dual_acrobat](lightning/dual-acrobat.md) | `DualAcrobatSmgEntity.tickOnServer; DualAcrobatCounterSpellEvent.onCounterSpell` | SMG tick de fogo alternado e cleanup CounterSpell |
| `apprenticecodex:fujin` | [fujin](evocation/fujin.md) | `FujinKatanaEntity.tickOnServer; FujinSlashProjectileEntity.damageEntities` | slash periódico e victimUuids por projétil |
| `apprenticecodex:silent_assassin` | [silent_assassin](evocation/silent-assassin.md) | `SilentAssassin.onCastCompleteWithWeapon` | headshot/unaware, awareness conditional |
| `apprenticecodex:lethal_assault` | [lethal_assault](evocation/lethal-assault.md) | `LethalAssaultRifleEntity.tickOnServer` | três disparos e descarte em tick 20 |
| `apprenticecodex:moon_light` | [moon_light](eldritch/moonlight.md) | `MoonLightChargeCutEntity.tick; MoonLightCounterspellEffect.applyAfterSuccessfulDamage` | segmento dedup por UUID e efeito somente após damage |
| `apprenticecodex:shiden` | [shiden](lightning/shiden.md) | `ShidenKatanaEntity.slash` | blockOccluded e dano com multiplicador |
| `apprenticecodex:fly_swatter` | [fly_swatter](lightning/fly-swatter.md) | `FlySwatter.onCastCompleteWithWeapon; FlySwatterProjectileEntity.onImpact` | locks, cancellation edge e exclusão direct-hit do splash |
| `apprenticecodex:precision_jack` | [precision_jack](evocation/precision-jack.md) | `PrecisionJackLootingEvent.onLivingDrops` | looting e second loot-roll por fonte exata |

## Invariantes e cenários de validação

- **Causalidade:** channel, recast e arma temporária não permitem multiplicar cast identities; tiros, pellets, VFX/tracers, efeitos por dano e drops são resultados do cast do Iron's. Mastery/rewards jamais devem ser inferidos por impacto. A licença/source serve só para documentação clean-room.
- **Dano e dedup:** Breaching Enemy agrupa pellets no source; Fujin guarda vítimas por projétil; Moon Light guarda vítimas no segmento da entidade, mas o slash da katana e o segmento são efeitos separados do mesmo cast. Fly Swatter evita acertar o direct-hit target novamente no splash.
- **Recasts e ciclo de vida:** Commence Fire faz gate de recoil; Dual Acrobat pode descartar SMG em CounterSpell; Lethal Assault mantém sua própria sequência temporal; Silent Assassin condiciona awareness ao tiro final; no source do Fly Swatter, onCastCompleteWithWeapon não verifica explicitamente o flag cancelled ao processar locks — pendência de QA, não bug certificado.
- **Loot:** PrecisionJackLootingEvent só age no LivingDropsEvent do damage type PRECISION_JACK com a entidade knife, com limites de looting e chance; não reexecutar drops/XP ou atribuir cada rolagem a casts separados.
- **Autoridade:** Iron's é authority de mana/casting/recast/cooldown; Apprentice's Codex dos efeitos; Black Arcana apenas governa seu próprio runtime via boundaries reais; RPG Skill Tree owns Mastery/perks/gates, sem integração homologada neste lote.
- **⚠️** JAR bytecode, config física, Survival/dedicated/multiplayer, PvP, claims, modded-entities, eventos de loot de terceiros, logout/reload e performance não foram fisicamente testados. **⛔** Sem hook/recibo seguro para perks/Mastery; fail-closed e nenhuma promoção de Stage 06.05.

[Registry](README.md) · [High-risk](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) · [Lifecycle](PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md) · [Persistent](PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md) · [World/Combat](PERK-ENGINEERING-MATRIX-WORLD-COMBAT-0.9.7.1.md).
