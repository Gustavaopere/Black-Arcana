# Dispel

- Registry ID: `ars_nouveau:glyph_dispel`
- Source class: `EffectDispel`
- School: Abjuration
- Default tier: **1**
- Default mana: **30**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Posts Ars Nouveau `DispelEvent.Pre` and honors cancellation before resolution. On living entities it removes milk-curable effects except provider-tagged deny entries, plus explicitly provider-tagged allow entries; it then invokes `IDispellable` where supported and posts `DispelEvent.Post`. Blocks/block entities implementing `IDispellable` receive the same provider dispel callback/event framing.

Compatible augments: none in the exact 5.13.1 class.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:milk_bucket` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

This is a real Ars-supported event/interface surface, but it remains Ars authority. A future Black Arcana adapter may observe/use a supported seam only after exact API-contract review; it must not reinterpret Dispel as authority over Black Arcana state, Corruption, Strain or arbitrary third-party effects.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / API CANDIDATE SEAM IDENTIFIED / RUNTIME QA PENDING`.

## Dossiê de engenharia para perks — cadeia e interfaces

- **Source pin:** [`EffectDispel.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDispel.java), Ars Nouveau 5.13.1.
- **Boundary real:** `NeoForge.EVENT_BUS.post(new DispelEvent.Pre(hit,world,shooter,spellStats,spellContext))` antes da resolução, com `isCanceled()`; `DispelEvent.Post` depois, condicionado ao ramo. Evento concreto é prova de veto/observação para **Dispel**, não de mutação universal das magias Ars. **Mob effects:** remove `EffectCures.MILK` exceto `PotionEffectTags.DISPEL_DENY`, também remove exceções `DISPEL_ALLOW`; chama `IDispellable.onDispel(shooter)` em entidades vivas. Blocos/BlockEntities `IDispellable` recebem callback próprio. **Augments:** nenhum na classe.
- **Estado:** ✅ classe exata lida; ⚠️ helpers/config real e Survival pendentes; mutabilidade via RPG Skill Tree ⛔ sem interface comprovada que altere esses parâmetros. Ars conserva authority de recursos/efeitos.

## API pública do Dispel — assinatura e escopo comprovados

- Fonte do evento: [`com.hollingsworth.arsnouveau.api.event.DispelEvent`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/DispelEvent.java); `Pre extends DispelEvent implements ICancellableEvent` e `Post extends DispelEvent` (não cancelável).
- Payload público exato: `HitResult rayTraceResult`, `Level world`, `LivingEntity shooter`, `SpellStats augments`, `SpellContext context`. `EffectDispel` publica `Pre` e usa `isCanceled()` antes de resolver; publica `Post` nos caminhos que prosseguem.
- **Hooks demonstrados:** veto de Dispel em Pre; observação de Post com ressalva de caminhos precoces; `IDispellable.onDispel(LivingEntity)` para alvos elegíveis. Reatribuir campos do evento não prova que `EffectDispel` passará a consumir valores substituídos, pois o corpo continua usando suas variáveis locais.
- **RPG perk:** candidato de bridge de veto/observação, ainda não conectado. Ver [matriz geral de eventos](../../VERIFIED-EVENT-SURFACES-5.13.1.md). Sem teste do evento no modpack e sem contrato de deduplicação, não conceder Mastery por simples Post.

## Certificação estática: status e Dispel — 25/10/2026

**✅ Ficha técnica source-pinned completa somente para planejamento; ⛔ `mutating_hook=NOT_VERIFIED` e ⚠️ `physical_qa=NOT_TESTED`.** Certificação documental não prova que existe perk implementada ou modpack validado.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e release | `ars_nouveau:glyph_dispel`, `EffectDispel`, Ars Nouveau **5.13.1**, tier I. [Source no commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDispel.java); [identidades no publisher JAR](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, causalidade e efeitos downstream | Nos dois overloads, `NeoForge.EVENT_BUS.post(new DispelEvent.Pre(...))` ocorre **antes** de processar alvo, e retorno com `isCanceled()` aborta a resolução. **Entidade viva:** itera uma cópia de efeitos, remove os curáveis por `EffectCures.MILK` salvo tag `DISPEL_DENY`, e efeitos não curáveis por milk explicitamente presentes em `DISPEL_ALLOW`; se depois o alvo está morto/removido retorna **sem Post**; caso ainda elegível, chama `IDispellable.onDispel(shooter)` e então publica `DispelEvent.Post`. **Bloco:** após Pre, chama `IDispellable` separadamente no `BlockState` e no `BlockEntity` quando presentes e publica Post inclusive quando nenhum suporta a interface. Para `EntityHitResult` não Living, o método publica Pre, mas não Post. |
| Parâmetros, caps e augments | `getCompatibleAugments()` retorna `augmentSetOf()` **vazio**; não há parâmetro escalável de radius/duration/damage/amp nesta classe e nem `IPotionEffect`. Evento público `DispelEvent.Pre` implementa `ICancellableEvent`; `Post` não é cancelável. Payload contém `HitResult rayTraceResult`, `Level world`, `LivingEntity shooter`, `SpellStats augments`, `SpellContext context`, mas a classe usa variáveis locais após o evento — **mutar os campos públicos do evento não prova que os novos valores serão consumidos**. `Post` não significa efeito removido: bloco sem `IDispellable` ainda pode emitir Post. |
| Target, geometria, dano e duração | Alvo de entidade viva com efeitos removíveis/tags e callbacks, ou bloco e block entity implementando `IDispellable`. Não é dispel universal de rituais Black Arcana, mana, Corruption/Strain ou status externos sem tags/callbacks compatíveis. Sem dano, projétil, área, tempo, targeting alternativo ou busca de alcance internos; Form decide delivery. |
| Custos e aprendizagem | Mana default **30**, tier I, recipe datagen `ars_nouveau:abjuration_essence` + `minecraft:milk_bucket` ×3, XP default **27**, starter default **não**; [aquisição 85/85](../../ACQUISITION.md). Cooldown, pagamento e admissão pertencem à magia composta/provider; tempo de status não é cooldown. |
| Authority, eventos e integração | **VETO/OBSERVAÇÃO provider-native SOURCE_VERIFIED**, não adapter RPG implementado, não hook genérico mutador. Se futuramente integrar `Pre`, respeitar cancelamento, contexto, side, escopo exato e custo/cast já registrado; se observar `Post`, não conceder Mastery com base em Post sozinho. QA de event bus no cliente/modpack e semântica de terceiros pendentes. `mutating_hook=NOT_VERIFIED` para modificações arbitrárias. RPG Skill Tree é sibling de progressão/perks apenas por contrato comprovado. Black Arcana conserva seus próprios casting, Corruption, Strain, WorldEffectPolicy e causalidade, não assume a semântica nativa de Ars. |
| Evidência/validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, **prova compilada somente de ID/classe**. Config instalada, correspondência exata do bytecode de todos os métodos, consumer behavior e clientes/modpack físicos: **não verificados**; `physical_qa=NOT_TESTED`. |

**Invalidação:** mudança de JAR, source, receitas, configs ou listeners de eventos exige reauditoria. Nenhum spell, hook, cast, status mutável ou cap de gameplay foi implementado neste checkpoint.
