# Fangs

- Registry ID: `ars_nouveau:glyph_fangs`
- Source class: `EffectFangs`
- School: Conjuration
- Default tier: **3**
- Default mana: **35**
- Default damage config: **6.0** base + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates provider Evoker Fang entities along a line toward the target. Self-targeting switches to two radial rings around the caster. Duration changes the fang timing and Accelerate shortens the per-fang delay; the exact class notes no Decelerate support in this line.

Compatible augments: Amplify, Dampen, Extend Time, Reduce Time, Accelerate. Amplify is limited to 2 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:prismarine_shard` ×2 + `minecraft:totem_of_undying`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns fang entity lifecycle, timing and damage. Black Arcana summoned hazards must use its own bounded scheduler/damage contracts and cannot treat provider fang timing as a general hazard API.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — classe de efeito

- **Source pin:** [`EffectFangs.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFangs.java), Ars Nouveau 5.13.1.
- **Dano bruto:** `DAMAGE.get()+AMP_VALUE.get()*getAmpMultiplier()` com defaults 6.0 e 3.0; máximo Amplify default 2; danos reais dependem de `EntityEvokerFangs` e defesa do alvo.
- **Alcance/contagem:** cast normal tenta **16 posições** em linha, a cada `1.25*(l+1)` blocos na direção do alvo (até 20 blocos de posição); cast self tenta **13 posições**, em dois anéis com 5 presas a raio 1.5 e 8 a raio 2.5. `spawnFangs` exige chão válido e pode **não gerar entidade** para posição sem suporte.
- **Delay:** por fang `j=(int)((index+durationMultiplier)/(1+count(Accelerate)))` em ambos os ramos. Isto é timer de ativação, **não** duração total de área; não existe Decelerate compatível nesta classe. **Perks:** separar número/velocidade/dano/proteção contra chão ausente; reduzir j não cria novos casts.
- **Status:** ✅ source exato lido; ⚠️ entidade auxiliar, caps runtime e Survival requerem testes; API por efeito não foi validada contra RPG/Black Arcana. Sem autorização para segunda liquidação de dano/recurso/target.
