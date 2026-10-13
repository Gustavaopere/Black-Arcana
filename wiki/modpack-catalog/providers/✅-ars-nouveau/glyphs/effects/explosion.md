# Explosion

- Registry ID: `ars_nouveau:glyph_explosion`
- Source class: `EffectExplosion`
- School: Elemental Fire
- Default tier: **2**
- Default mana: **200**
- Default source config: intensity **0.75**, amplification intensity **0.5**, AOE intensity **1.5**, damage **6.0**, damage per Amplify **2.5**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates Ars Nouveau's custom explosion at the resolved position. AOE raises blast size without directly raising the configured damage term; Amplify affects size and damage; Dampen reduces size/damage. Extract changes block interaction from decay-style destruction to full-destroy/drop behavior. NeoForge's explosion-start hook can veto execution.

Compatible augments: Amplify, Dampen, AOE, Extract. Amplify is limited to 2 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:tnt` ×3 + `minecraft:fire_charge`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

This is a destructive provider-native capability. Black Arcana must never route its own explosions through this as a way around `WorldEffectPolicy`; its destructive effects remain independently budgeted and policy-controlled.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / HIGH-RISK WORLD EFFECT / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectExplosion.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExplosion.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectExplosion` no Ars 5.13.1, método `onResolve`.
- **Raio/intensidade:** `BASE.get()+AMP_VALUE.get()*ampMultiplier+AOE_BONUS.get()*aoeMultiplier-0.5*count(Dampen)`; defaults BASE=0.75, AMP=0.5, AOE_BONUS=1.5. **Dano:** `ANExplosion.baseDamage=DAMAGE.get()` (default 6.0) e `ampDamageScalar=AMP_DAMAGE.get()` (default 2.5), dano por entidade definido downstream em `ANExplosion`, não diretamente nesta classe. **Blocos:** Extract escolhe `DESTROY`, senão `DESTROY_WITH_DECAY`; `EventHooks.onExplosionStart` pode cancelar a explosão. Pacote enviado a jogadores dentro de distância quadrada 4096 é sincronização e **não** raio de explosão. **Perks:** intensidade, dano, proteção e drops são eixos separados; sem API de mutação comprovada.
- **Limite de integração:** ✅ fonte estática identificada; ⚠️ parâmetros condicionados à configuração carregada; ⛔ nenhum hook externo de mutação verificado. Mana, targeting e settlement pertencem a Ars; RPG Skill Tree não substitui o resolver. Gameplay/Survival e adapter real: PENDING.
