# Sensitive

- Registry ID: `ars_nouveau:glyph_sensitive`
- Source class: `AugmentSensitive`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **1** (inherited provider default)
- Default mana: **10**

## Source-pinned behavior

Sets Ars Nouveau's Sensitive spell-stat flag. Compatible glyphs change their targeting/behavior when that flag is present. Exact examples in 5.13.1 include Projectile/Orbit targeting motion-nonblocking materials and Touch targeting fluids/air; other effects may define their own Sensitive behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:scaffolding` + `minecraft:poppy` + `minecraft:water_bucket`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Sensitive is not permission to relax Black Arcana target validation. Black Arcana remains server-authoritative for range, LOS, loaded-state and target-kind geometry even when an Ars integration composes with this glyph.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentSensitive.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentSensitive.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.setSensitive()`; default mana 10; tier default herdado conforme ficha. O flag não é uma permissão genérica de targeting fora do protocolo da Form.
- **Consumidores:** `MethodTouch` aceita alvo em ar/fluidos conforme regras provider; `EffectIgnite` cria `MAGIC_FIRE` em vez de fogo normal quando Sensitive; `EffectFreeze` troca água por `FROSTED_ICE`; `EffectPlaceBlock` usa contagem Sensitive 1/2 para direção de fake player; `EffectRune` armazena `runeTile.isSensitive` para uso de inventário.
- **Perks:** o `setSensitive()` binário e a **contagem** de glyphs são dados distintos; não reproduzir o flag como bypass do `WorldEffectPolicy` do Black Arcana.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ contrato técnico estático source-pinned de 5.13.1; ⛔ integração de perk mutadora não comprovada; ⚠️ QA físico NOT_TESTED.** `technical_perk_dossier: 1`. Esta revisão classifica os campos do componente composicional; não certifica o provider inteiro, a configuração implantada ou uma execução em jogo.

| Eixo exigido | Contrato estático e consumidor | Evidência / limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_sensitive`, classe `AugmentSensitive`, augment Ars Nouveau 5.13.1; tier-padrão **I (herdado)**. | [Classe][class]; [roster de identidade binária SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Display e ID não criam uma ação independente. |
| Efeito e comportamento | `applyModifiers(builder,part)` chama `setSensitive()` e devolve o builder; o setter torna o flag true. `getBuffCount` continua independente, permitindo consumidores com regras para uma ou mais cópias. Tier default I vem de AbstractSpellPart, não de override local. [Classe][class], [builder][builder], [counts][stats], [tier/config][config]. | O Form/Effect recebe o augment na composição Ars; setter/contagem não executam um segundo cast. |
| Parâmetros, escala e caps | O flag é boolean, não bônus numérico de alcance. Projectile guarda count da Form: count>0 muda ClipContext.Block de COLLIDER para OUTLINE, mantendo Fluid.NONE; count>1 tem ramo próprio de bounce. Place Block usa count>0 para orientar fake player e count>1 para inverter a referência; limite default2 nesse receptor. Break usa shears e limita Sensitive a1. Não há cap global inferido por esses exemplos. [snapshot][projectile-sensitive], [clip][projectile-clip], [bounce][projectile-bounce], [place][place-sensitive], [place cap][place-cap], [Break][break-sensitive], [cap do Break][break-sensitive-cap]. | Defaults de cada receptor e configuração implantada são evidências separadas; `per_spell_limit` e limites do receptor são [configuráveis][limits]. |
| Targeting, área, projétil, tipo e duração | **N/A como ação autônoma**, porém há mudança de targeting nos consumidores. `AbstractCaster#castSpell` calcula presença na Form antes do ray, passa o flag como hitLiquids a `SpellUtil.rayTrace` e admite um BlockHitResult com MISS quando sensitive. `0.5+BLOCK_INTERACTION_RANGE` é o length do pick de blocos; a mesma função consulta entidades separadamente com `MathUtil.getLookedAtEntity(entity,25)` e prioriza esse resultado quando presente, sem estabelecer range ou garantia de LOS universais. [Caster][caster-sensitive], [ray][ray-sensitive]. | Classificar o campo próprio como não aplicável não elimina a semântica específica no receptor. |
| Custos, cast, cooldown e aprendizagem | Mana default **10**, tier **I (herdado)**; recipe-padrão **minecraft:scaffolding + minecraft:poppy + minecraft:water_bucket**, **27 XP**. Sem cast/cooldown autônomo: o custo compõe a magia Ars e pode ser sobrescrito por config/custo do receptor. Starter default false, sujeito a configuração. | [Classe][class], [recipe gerada][recipe], [getCastingCost/tier][config], [getCostForPart][augment-base] e [aquisição catalogada](../../ACQUISITION.md). Source de mundo e mana do jogador continuam distintos. |
| Integração e autoridade | Ars publica [SpellModifierEvent][modifier-event] com builder após aplicar augments/itens [no build][builder]; existe superfície source. Um adapter RPG/Black Arcana que preserve contexto, custos, caps e deduplicação não foi comprovado. **⛔ SEM_HOOK_SEGURO para a integração de perk proposta / mutating_hook=NOT_VERIFIED**. | Não negar a API pública existente nem promovê-la a integração testada. Não manter SpellStats, loot, seleção ou settlement paralelo. [Matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). |
| Grau de validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY**: source imutável `112920ff774831f204031da75b4c4e73d3765157`; identidade JAR `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Nenhuma comparação integral de método compilado ou execução física é alegada nesta ficha. | [Prova de IDs](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config/modpack/Survival, eventos e mutação por perk permanecem NOT_TESTED/NOT_VERIFIED; nenhum Stage promovido. |

**Consequências por Effect:** Ignite com Sensitive tenta MAGIC_FIRE em bloco substituível; Freeze escolhe FROSTED_ICE no ramo de água; Rune armazena isSensitive no tile para semântica de inventário. Não homogeneizar essas mudanças como permissão genérica ou reaplicar status/blocos pelo Black Arcana. [Ignite][ignite-sensitive], [Freeze][freeze-sensitive], [Rune][rune-sensitive]. Dano, duração, quantidade e proteção finais pertencem a cada consumidor.

**Invalidação:** mudança de release/hash/source, composição, config, consumidor ou contrato de integração exige nova revisão. O ✅ cobre apenas os campos estáticos documentados; Form/Effect e provider mantêm recursos, targeting e efeitos.

[augment-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L32-L60
[stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L57
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L162
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L255
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentSensitive.java#L1-L30
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_sensitive.json#L1-L19
[projectile-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L107-L112
[projectile-clip]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L170-L175
[projectile-bounce]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L418-L433
[place-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPlaceBlock.java#L47-L69
[place-cap]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPlaceBlock.java#L103-L118
[break-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L60-L89
[caster-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractCaster.java#L282-L323
[ray-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java#L191-L195
[ignite-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectIgnite.java#L41-L65
[freeze-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFreeze.java#L74-L90
[rune-sensitive]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRune.java#L42-L61

[break-sensitive-cap]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L123-L127
