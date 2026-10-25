# AOE

- Registry ID: `ars_nouveau:glyph_aoe`
- Source class: `AugmentAOE`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **35**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's AOE spell stat. Compatible glyphs interpret the stat to expand their affected area around a target.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:firework_star`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns this AOE stat and its per-glyph interpretation. Black Arcana area geometry remains explicitly server-bounded and cannot inherit an unbounded Ars radius contract.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Mapeamento de perk para Codex — transformação real

- **Source pin:** [`AugmentAOE.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAOE.java) no Ars Nouveau 5.13.1.
- **Transformação exata:** `applyModifiers` chama `builder.addAOE(1.0)`. `getDefaultManaCost=35`, tier II. **Interpretação:** o glyph receptor decide a geometria, p.ex. `EffectBreak` usa `SpellUtil.calcAOEBlocks`, `EffectFreeze` calcula AOE e depois examina seis vizinhos por posição e `EffectExplosion` usa o multiplicador para intensidade. **Perks:** +1 AOE do Ars não representa +1 bloco de raio universal; sem analisar o consumidor e seus caps/work budgets, mutação externa da área continua ⛔.
- **Bridge:** `source identified / mutation hook NOT VERIFIED / provider-owned`. Não implementar segundo `SpellStats` no Black Arcana, nem usar atributos RPG sem seam verificado. Testes em modpack/Survival PENDING.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ CATÁLOGO TÉCNICO ESTÁTICO SOURCE-PINNED (5.13.1); ⛔ HOOK MUTADOR DE PERK NÃO COMPROVADO; ⚠️ QA FÍSICO NOT_TESTED.** Esta revisão classifica os campos do augment composicional. Identidade do JAR e comportamento da fonte são provas diferentes; não se certifica configuração implantada, execução de perk ou compatibilidade em jogo.

| Eixo exigido | Contrato estático verificado ou não aplicável | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_aoe`, classe `AugmentAOE`, augment de tier-padrão II. | [Classe completa][augment], [roster físico SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md); não é spell independente. |
| Comportamento e recebedor | `applyModifiers` soma **+1,0** ao campo AOE do builder por aplicação, depois retorna o super. `SpellStats#getAoeMultiplier` entrega esse valor ao receptor. | [Operador][augment], [acumulador][aoe-builder], [getter][spell-stats], [pipeline de build][build-stats]. O campo é um escalar sem unidade espacial própria. |
| Parâmetros, escala e caps | No overload usado por Break/Freeze: `width=1+floor(a)`, `height=1+ceil(a)`, `depth=1+p`, onde `a=getAoeMultiplier` e `p=count(Pierce)`. Para a/p inteiros não negativos, a grade candidata tem `(1+a)²×(1+p)` posições antes dos filtros; orientação/face determinam os eixos. Explosion usa `I=BASE+AMP_VALUE×amp+AOE_BONUS×a−0.5×count(Dampen)`, com AOE_BONUS default1.5. | [SpellUtil][grid], [Break][break], [Freeze][freeze], [Explosion][explosion]. Não existe raio universal nem cap próprio em AugmentAOE. Compatibilidade/limites/config pertencem ao receptor; [validação de criação e casts condicionados][validation] não equivale a um teto mundial de trabalho. |
| Alvo, área, projétil, dano e tempo | Não seleciona alvo, instancia projétil, muda DamageType ou programa duração. **Área é modificada como stat**, não como forma geométrica autônoma. Break filtra harvest/claims/blacklist; Freeze ainda examina seis vizinhos de cada posição, portanto sua área de trabalho não é só a grade inicial. | [Base composicional][base-augment], [filtros Break][break], [vizinhos Freeze][freeze]. AOE não autoriza resize do projétil nem single→AOE fora de um receptor compatível. |
| Custos, cast, cooldown e aprendizagem | Mana-padrão35, tier II; recipe `minecraft:firework_star`, XP-padrão55. Cast/cooldown autônomos **N/A**; são da composição. Custo efetivo pode vir da config do glyph e do custo por receptor. | [Defaults][augment], [recipe][recipes], [XP][recipe-xp], [custo efetivo][part-cost], [custo por parte][base-augment], [aquisição](../../ACQUISITION.md). Config implantada não foi observada. |
| Integração e mutabilidade | O operador do provider e seu [evento de builder][modifier-event] são localizados; adapter RPG/BA, budget, validação da área e dedup continuam **⛔ SEM_HOOK_SEGURO / NOT_VERIFIED** para mutação por perk. | Evento nativo não prova que toda geometria ou custo use o valor alterado. Não inserir uma segunda seleção de blocos, explosão ou pagamento. |
| Validação e limites da prova | Fonte fixa e identidade binária certificam este contrato estático; métodos/JAR e runtime composto não foram equiparados integralmente. | [Identidade binária](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), [matriz source](../../PERK-ENGINEERING-MATRIX-5.13.1.md). `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`. |

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
[augment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAOE.java#L11-L37
[aoe-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L214-L222
[grid]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java#L66-L160
[break]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L51-L89
[freeze]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFreeze.java#L40-L60
[explosion]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExplosion.java#L36-L84
