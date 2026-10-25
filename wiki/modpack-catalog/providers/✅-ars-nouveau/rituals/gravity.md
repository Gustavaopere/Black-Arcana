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

## Certificação técnica estática de ritual — segundo lote (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` — contrato estático completo da ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Prova não cobre hook seguro, config implantada nem aceitação do modpack.

| Campo de perk | Evidência estática no provider |
|---|---|
| Identidade e release | `ars_nouveau:ritual_gravity`; `RitualGravity`; Ars Nouveau 5.13.1. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualGravity.java) e [registry exato do publisher](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, ramificações e settlement | `RitualGravity extends RangeEffectRitual extends RangeRitual`. O pai `RangeRitual.tick` apenas enfileira a posição em `RitualEventQueue` quando servidor, `gameTime%20==0` e não enfileirada. O pai `RangeEffectRitual.shouldApply` verifica `ServerPlayer`, `!needsSourceNow()` e `BlockUtil.distanceFrom` <= range; `attemptRefresh` marca `setNeedsSource(true)` somente se `applyEffect` retornar sucesso. A classe Gravity declara `GRAVITY_EFFECT`; seu método não implementa diretamente o efeito físico de gravidade nos jogadores. |
| Fórmulas, parâmetros, limites e caps | `getRange()=60`, `getDuration()=60*20=1200 ticks`, amplifier 0 no `RangeEffectRitual.applyEffect`. Campos `public static int renewInterval=20` e `renewThreshold=10*20=200` são **declarações**; este source não demonstra que a fila ou um timer de refresh consome esses campos, então não inferir periodicidade de 20/200 ticks a partir deles. Métrica real depende do helper `BlockUtil.distanceFrom`. |
| Targeting, área/volume, duração, dano e projétil | `ServerPlayer` elegível até range 60 do brazier, sem dano, alvo de Form, projétil ou área destrutiva próprios; `GRAVITY_EFFECT` é aplicado por `MobEffectInstance` do provider. Física, antigravidade, vôo e controle de movimento dependem do consumidor do status, não desta classe. |
| Resource cost, cooldown, receita/admissão | `getSourceCost()` retorna **200 Source**; `RangeEffectRitual.attemptRefresh` solicita Source após efeito aplicado (`setNeedsSource(true)`). Não confundir solicitação de Source com débito atômico garantido; receitas de ativação, source jars, config e cooldown de reapply não estão fechados por este método. Custo de magia `SpellResolver` de Form/Effect é N/A neste ritual. |
| Política de mundo e integração entre projetos | Não duplicar status Gravity nem declarar um hook de movimento por estar estaticamente visível a `getDuration` ou a constantes renew. Compatibilidade com voo, teleport, Epic Fight e outras gravidades exige QA físico. Mastery é no máximo observação causal por contrato futuro, jamais no loop de refresh/efeito. Autoridade de execução e fonte/Source pertence ao Ars; RPG Skill Tree fornece progressão/atributos/Mastery/gates mediante contrato real, Black Arcana detém seu runtime/rituais e WorldEffectPolicy para suas mutações próprias, sem interceptar automaticamente este ritual. |
| Grau de evidência/QA | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` para métodos e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID/classe registrada**. Não foi comprovada equivalência byte-a-byte dos métodos, configuração atual, side/claims reais, multiplayer ou QA físico. |

**Gate fail-closed:** alteração de geometria, itens, persistência, energia/Source ou consumer exige hook real, orçamento, transação e deduplicação provados; o ✅ é documental, não implementação de perk ou promoção de Stage 06.05/09.
