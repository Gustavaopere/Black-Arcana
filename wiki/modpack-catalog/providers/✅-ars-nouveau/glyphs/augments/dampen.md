# Dampen

- Registry ID: `ars_nouveau:glyph_dampen`
- Source class: `AugmentDampen`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **0**

## Source-pinned behavior

Adds **-1.0** amplification. Compatible glyphs interpret that lower-power state. Pantomime separately uses Dampen as a target-distance reduction and caps it to one instance for that Form.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:nether_brick`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns the interpretation and compatible-glyph surface. Zero default mana is a provider source default, not permission for Black Arcana to treat reduced-power magic as globally cost-free.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentDampen.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDampen.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.addAmplification(-1.0)`, custo default 0, tier II.
- **Diferença por consumidor:** [`MethodPantomime.findPosition`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodPantomime.java#L36-L43) examina a **presença/contagem** de Dampen e fixa `offset=-1` ([max default 1](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodPantomime.java#L89-L93)), enquanto `EffectExplosion` subtrai `0.5*count(Dampen)` da intensidade; outros consumidores leem `getAmpMultiplier()`.
- **Perks:** custo zero da parte não significa cast total grátis. Um buff global de spell damage não reproduz corretamente a semântica de Dampen e seus efeitos por consumidor.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ CATÁLOGO TÉCNICO ESTÁTICO SOURCE-PINNED (5.13.1); ⛔ HOOK MUTADOR DE PERK NÃO COMPROVADO; ⚠️ QA FÍSICO NOT_TESTED.** Esta revisão classifica os campos do augment composicional. Identidade do JAR e comportamento da fonte são provas diferentes; não se certifica configuração implantada, execução de perk ou compatibilidade em jogo.

| Eixo exigido | Contrato estático verificado ou não aplicável | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_dampen`, classe `AugmentDampen`, augment de tier-padrão II. | [Classe completa][augment], [roster SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento e recebedor | `applyModifiers` executa `builder.addAmplification(−1.0)`, depois delega ao super. Isso subtrai1 do stat de amplificação por aplicação aceita. O builder não impõe piso nesse operador. | [Operador][augment], [acumulador][amp-builder], [getter][spell-stats]. Não equivale a desconto percentual universal ou mana negativa. |
| Parâmetros, escala e caps | Harm direto usa `D=DAMAGE+AMP_VALUE×amp`, defaults5+2×amp; se houver augment de tempo e alvo Living, muda para Poison. Break usa amplificação para harvest. Explosion usa amp na intensidade e ainda subtrai separadamente `0.5×count(Dampen)`; com AMP_VALUE default0.5, cada Dampen reduz a intensidade em1.0 nessa fórmula. ANExplosion também usa teto de dano `baseDamage+amp×ampDamageScalar`, defaults6+2.5×amp. | [Harm][harm], [Break][break], [Explosion][explosion], [terminal ANExplosion][explosion-terminal]. Defaults são do receptor, não parâmetros próprios de Dampen. Não inferir clamp universal, imunidade ou cura para valores negativos; resultado final/combinações exigem QA. Caps/compatibilidade/config e [validação][validation] são por contexto. |
| Alvo, área, projétil, tipo e tempo | Target, DamageType, duração, hitbox e resolver autônomos **N/A** neste augment. Ele altera o stat de amplificação; área, dano, status ou equipamento podem mudar indiretamente conforme o consumidor. Não instancia ataque ou projétil. | [Base composicional][base-augment], [receptores Harm/Break][harm], [Explosion][explosion]. Não atribuir uma geometria ou tipo de dano fixo ao nome Dampen. |
| Custos, cast, cooldown e aprendizagem | Mana-padrão0, tier II; recipe `minecraft:nether_brick` (item), XP-padrão55. Cast/cooldown autônomos **N/A**. Zero é default deste glyph, não garantia de custo total nulo da composição ou ausência de overrides. | [Defaults][augment], [recipe][recipes], [XP][recipe-xp], [custo efetivo][part-cost], [custo por receptor][base-augment], [aquisição](../../ACQUISITION.md). |
| Integração e mutabilidade | Método do builder e [SpellModifierEvent][modifier-event] são superfícies nativas identificadas; contrato externo de alteração, cap, custo e dedup permanece **⛔ SEM_HOOK_SEGURO / NOT_VERIFIED**. Não substituir o operador por um debuff RPG ou segundo hurt/heal. | [Pipeline de build][build-stats] não é aceite de adapter. Somar/subtrair um stat no evento não prova equivalência a adicionar a ocorrência Dampen que Explosion também conta. |
| Validação e limites da prova | `STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY`, sem equivalência integral dos métodos/JAR ou execução física. | [Prova da identidade](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), [matriz](../../PERK-ENGINEERING-MATRIX-5.13.1.md); `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`. |

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
[augment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDampen.java#L9-L36
[amp-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L204-L212
[harm]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarm.java#L31-L49
[break]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L51-L89
[explosion]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExplosion.java#L36-L84
[explosion-terminal]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/ANExplosion.java#L85-L112
