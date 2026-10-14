# Ars Nouveau — Summon Undead

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_summon_undead`
- Display name: Summon Undead
- School: Conjuration
- Default tier: 3
- Default mana cost: 150
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify, Split, Pierce
- Source default duration: 15 s
- Source default Extend Time increment: 10 s
- Base summon count: 3 + Split count

## Provider-native behavior

Summons temporary allied `SummonSkeleton` entities. Pierce switches them to bows; Amplify upgrades weapon quality, including stronger swords/axes or bow Power enchantment depending on amplification. Split adds additional skeletons. The caster receives Summoning Sickness for the summon lifetime.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:bone` + `minecraft:wither_skeleton_skull`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns these temporary undead summons, their loadout scaling, ownership/lifetime and Summoning Sickness. Black Arcana Souls & Death content must not reinterpret them as Black Arcana souls/minions or double-settle their attacks.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSummonUndead`).

## Engenharia de perks — evidência de execução individual

- **Classe versionada:** [`EffectSummonUndead.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonUndead.java) no Ars Nouveau 5.13.1.
- **Admission/duração:** `canSummon(shooter)`; `ticks=(int)(20*(GENERIC_INT.get()+EXTEND_TIME.get()*durationMultiplier))`, defaults 15s e 10s, retorna se ticks <=0. **Contagem:** `count=3+getBuffCount(Split)`; cria `SummonSkeleton` com spawn position aleatória próxima, `setOwner(shooter)`, `setLimitedLife(ticks)`, `summonLivingEntity` e `SUMMONING_SICKNESS_EFFECT` do caster por igual duração.
- **Equipamento:** Pierce flag fornece bow; com Amplify aplica POWER `max(4,(int)amp)-1` em bow, se amp>0; sem Pierce, amp >1 dá diamond sword, >2 netherite sword, >=3 netherite axe. A quantidade do summon não equivale a duração/qualidade da arma.
- **Perks:** Split aumenta pressão de summons; ownership/caps/sickness pertencem a Ars. Não creditar kills de cada minion como novo cast sem contrato causal.
- **Status:** ✅ code pin/identidade; ⚠️ downstream, config e Survival pendentes; mutação por RPG perk só pode ocorrer via [eventos reais](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e adapter validado, não por inferência temática.
