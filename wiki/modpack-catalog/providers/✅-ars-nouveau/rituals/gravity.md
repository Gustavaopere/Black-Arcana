# Gravity

Status: `SOURCE-PINNED 5.13.1 / RANGE-EFFECT RITUAL`

- Registry id: `ars_nouveau:ritual_gravity`
- Class: `RitualGravity`
- Effect: provider `GRAVITY_EFFECT`
- Effect duration: `60 × 20 = 1200 ticks`
- Range: `60` blocks
- Source cost declaration: `200`
- Class constants: `renewInterval = 20`, `renewThreshold = 200`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Gravity extends Ars Nouveau's `RangeEffectRitual`, sharing its server-only range admission and Source-backed refresh semantics. The ritual applies the provider `GRAVITY_EFFECT`, described as forcing nearby players to the ground, and can refresh the effect while the player remains within range.

A successful `RangeEffectRitual.attemptRefresh` marks the ritual as needing Source, so effect application and Source settlement remain coupled inside Ars Nouveau's ritual runtime.

## Black Arcana boundary

Gravity-effect application, refresh cadence and Source debit are Ars Nouveau authority. Black Arcana must not add a second gravity state or charge a second resource when observing the ritual.

The capability overlaps battlefield control/Space thematically but does not transfer Ars' effect state into Black Arcana's domain runtime.

## QA

The source class and shared range-effect contract are pinned to 5.13.1. Exact external refresh scheduling and interactions with flight/mobility providers remain runtime QA.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualGravity.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualGravity.java), versão Ars Nouveau 5.13.1.
- **Implementação:** `RitualGravity extends RangeEffectRitual`, declara `ModPotions.GRAVITY_EFFECT`, `getRange()=60` blocos, `getDuration()=60*20=1200` ticks e `getSourceCost()=200`.
- **Constantes fonte:** `renewInterval=20` e `renewThreshold=10*20` são campos estáticos da classe; a assinatura do provider genérico `RangeEffectRitual` controla `attemptRefresh`, `getEffect` e marca consumo de Source. Não presumir que os campos estáticos signifiquem um timer independente de 20 ticks sem identificar callsites.
- **Perks:** alcance do ritual não equivale a raio de um spell de gravidade ou velocidade da queda. Alterações externas em getDuration/getRange exigem adapter real; não somar débito de Source ou estado de flight bloqueado.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.
