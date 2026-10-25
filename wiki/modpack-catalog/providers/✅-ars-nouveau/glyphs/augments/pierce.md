# Pierce

- Registry ID: `ars_nouveau:glyph_pierce`
- Source class: `AugmentPierce`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **40**

## Source-pinned behavior

On compatible glyphs, Pierce adds depth/continuation semantics. Projectile explicitly permits additional traversal after colliding with a mob or block; some effects such as Break may extend to blocks behind the first target. AOE may combine with Pierce to add depth to affected geometry.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:arrow` + `ars_nouveau:wilden_spike`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Pierce interpretation per glyph. Black Arcana penetration/linked-target geometry remains explicitly bounded by its own server targeting and work budgets.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Mapeamento de perk para Codex — transformação real

- **Source pin:** [`AugmentPierce.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentPierce.java) no Ars Nouveau 5.13.1.
- **Implementação exata:** `AugmentPierce` não sobrescreve `applyModifiers` neste source; consumidores usam `spellStats.getBuffCount(AugmentPierce.INSTANCE)`; custo default 40 e tier II. **Dois significados distintos:** `MethodProjectile` permite atravessar hits adicionais; `EffectBreak` e `EffectFreeze` transferem count de Pierce a `SpellUtil.calcAOEBlocks` como **profundidade de blocos**. **Perks:** mesma tag não autoriza teleport de alvos ou penetração arbitrária; conservar tipo de alvo, claims, bounds, custo e ordem do SpellResolver; hook externo não verificado.
- **Bridge:** `source identified / mutation hook NOT VERIFIED / provider-owned`. Não implementar segundo `SpellStats` no Black Arcana, nem usar atributos RPG sem seam verificado. Testes em modpack/Survival PENDING.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ CATÁLOGO TÉCNICO ESTÁTICO SOURCE-PINNED (5.13.1); ⛔ HOOK MUTADOR DE PERK NÃO COMPROVADO; ⚠️ QA FÍSICO NOT_TESTED.** Esta revisão classifica os campos do augment composicional. Identidade do JAR e comportamento da fonte são provas diferentes; não se certifica configuração implantada, execução de perk ou compatibilidade em jogo.

| Eixo exigido | Contrato estático verificado ou não aplicável | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_pierce`, classe `AugmentPierce`, augment de tier-padrão II. | [Classe completa][augment], [roster físico SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento e recebedor | A classe não sobrescreve `applyModifiers`: herda o retorno inalterado do builder. A semântica vem da **presença/contagem no receptor**, não de um campo próprio `pierceMultiplier`. `Spell#getAugments` recolhe augments contíguos após a parte receptora. | [Classe][augment], [base][base-augment], [scan da receita][recipe-scan], [contagem em stats][spell-stats]. |
| Parâmetros, escala e caps | EntityProjectileSpell inicializa `pierceLeft` por `resolver.spell.getBuffsAtIndex(0,caster,Pierce)`, leitura da receita; `attemptRemoval` decrementa e remove quando `<0`. No caminho normal, p permite p+1 impactos que chamem essa remoção, **não garante p+1 alvos únicos**. Break/Freeze usam p como profundidade `1+p` da grade. Summon Undead usa apenas `hasBuff(Pierce)` para escolher arco em vez de arma melee. | [Snapshot do projétil][projectile-init], [remoção e impactos][projectile-impact], [grade][grid], [Undead][undead]. Sem cap global próprio; caps por receptor/config e contexto de validação [dependem do provider][validation]. |
| Alvo, área, projétil, tipo e duração | Não cria resolver, projétil, raio, DamageType ou timer próprio. O projétil da Form mantém seus filtros/eventos; blocos já atingidos têm hitList, enquanto o ramo de entidade não demonstra ledger por alvo nesta classe. Em Undead, a mesma presença altera equipamento, não penetração. | [Projectile onHit][projectile-impact], [Form compatível][projectile-form], [Undead][undead]. Não tratar todas as interpretações como atravessar blocos/proteções. |
| Custos, cast, cooldown e aprendizagem | Mana-padrão40, tier II; recipe `minecraft:arrow` + `ars_nouveau:wilden_spike`, XP-padrão55. Cast/cooldown autônomos **N/A**; mana efetiva/config/overrides pertencem à composição. | [Defaults][augment], [recipe][recipes], [XP][recipe-xp], [config][part-cost], [custo por receptor][base-augment], [aquisição](../../ACQUISITION.md). |
| Integração e mutabilidade | Há [evento nativo de builder][modifier-event], mas o snapshot `pierceLeft` acima lê a receita, não necessariamente a lista devolvida pelo builder. **⛔ SEM_HOOK_SEGURO / NOT_VERIFIED** para perk que mude penetração/count/targeting com custo e dedup preservados. | Não inferir que acrescentar Pierce ao builder modifique o construtor do projétil ou casts já emitidos. Não reexecutar o efeito para simular penetração. |
| Validação e limites da prova | Contrato estático source-pinned + identidade binária; nenhuma equivalência integral de método/JAR, modpack ou sequência de impactos foi testada. | [Prova da identidade](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), [matriz](../../PERK-ENGINEERING-MATRIX-5.13.1.md); `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`. |

**Autoridade e invalidação:** Ars controla receita, mana, validação e resolução; RPG Skill Tree controla progressão/perks, Black Arcana seu runtime e proteção de mundo, Enshrouded seus efeitos. `SpellModifierEvent` oferece builder nativo antes da resolução, mas um contrato externo precisa provar o consumidor efetivo, custos, fase, caps e deduplicação; a existência do evento não aprova a integração. Nenhum efeito deve ser executado novamente por um observer. Troca de JAR/source, operador, receptor, custo, compatibilidade ou configuração exige revisão.

**Grau:** `STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY`, source `112920ff774831f204031da75b4c4e73d3765157`; JAR `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. O roster binário foi auditado; os métodos desta ficha e a composição instalada não foram equiparados integralmente aos classfiles. QA de configuração/Survival/cliente/servidor e adapters permanece `NOT_TESTED`.

[base-augment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L15-L60
[spell-stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L76
[build-stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[part-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L255
[part-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L149
[validation]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/StandardSpellValidator.java#L38-L72
[recipes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L37-L48
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L14-L33
[augment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentPierce.java#L7-L28
[recipe-scan]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/Spell.java#L246-L272
[projectile-init]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L107-L115
[projectile-impact]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L343-L437
[projectile-form]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java#L125-L138
[grid]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java#L66-L160
[undead]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonUndead.java#L35-L68
