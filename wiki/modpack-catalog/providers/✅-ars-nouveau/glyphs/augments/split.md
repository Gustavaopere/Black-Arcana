# Split

- Registry ID: `ars_nouveau:glyph_split`
- Source class: `AugmentSplit`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **3**
- Default mana: **20**

## Source-pinned behavior

Adds additional simultaneous projectiles where a compatible Form implements Split. Projectile explicitly consumes the Split count to create more projectile entities, each carrying the subsequent spell effects.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:relay_splitter` + `ars_nouveau:wilden_spike` + `minecraft:stonecutter`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Split count, projectile spawning and compatible-glyph rules. Black Arcana projectile counts remain bounded by its own effect/work budgets and must not inherit Ars behavior implicitly.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Mapeamento de perk para Codex — transformação real

- **Source pin:** [`AugmentSplit.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentSplit.java) no Ars Nouveau 5.13.1.
- **Implementação exata:** `AugmentSplit` não sobrescreve `applyModifiers` neste source; a contagem é lida por consumidores com `spellStats.getBuffCount(AugmentSplit.INSTANCE)`. `getDefaultManaCost=20`, tier III. **Forma consumidora comprovada:** `MethodProjectile.summonProjectiles` cria `1+count(Split)` entidades `EntityProjectileSpell` no cast padrão e também no overload em blocos. **Perks:** cada projétil carrega effects posteriores; duplicar cast/settlement não é o mesmo que Split. Limites reais de compatibilidade dependem de `getCompatibleAugments` e config do glyph receptor.
- **Bridge:** `source identified / mutation hook NOT VERIFIED / provider-owned`. Não implementar segundo `SpellStats` no Black Arcana, nem usar atributos RPG sem seam verificado. Testes em modpack/Survival PENDING.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ CATÁLOGO TÉCNICO ESTÁTICO SOURCE-PINNED (5.13.1); ⛔ HOOK MUTADOR DE PERK NÃO COMPROVADO; ⚠️ QA FÍSICO NOT_TESTED.** Esta revisão classifica os campos do augment composicional. Identidade do JAR e comportamento da fonte são provas diferentes; não se certifica configuração implantada, execução de perk ou compatibilidade em jogo.

| Eixo exigido | Contrato estático verificado ou não aplicável | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_split`, classe `AugmentSplit`, augment de tier-padrão III. | [Classe completa][augment], [roster SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento e recebedor | Não sobrescreve `applyModifiers`; o super mantém o builder. Receptores contam `SpellStats#getBuffCount(Split)`. Na Form Projectile, `summonProjectiles` pede `1+count(Split)` entidades, cada uma recebendo o resolver da magia. | [Classe][augment], [base][base-augment], [contagem][spell-stats], [spawn][projectile]. Não é um novo cast independente por entidade. |
| Parâmetros, escala e caps | Projectile padrão cria n=1+s entidades e distribui yaw `round(counter/2.0)×10×opposite`, alternando opposite; velocidade é `max(0.1,0.75+acc/2)` e inaccuracy0.8. O overload legado por BlockPos também cria1+s, mas posiciona offsets laterais e delta(0,−0.1,0). Orbit e Summon Undead usam3+s, demonstrando que o incremento não fixa um total universal. | [Dois spawns Projectile][projectile], [Orbit][orbit], [Undead][undead]. Sem cap numérico próprio no augment; limites configurados e [validação][validation] pertencem ao receptor/receita e não garantem budget global de entidades. |
| Alvo, área, projétil, dano e tempo | Split altera **quantidade interpretada pelo consumidor**. Não define hitbox, alcance, alvo, DamageType ou duração próprios. A Form/effect conserva seu targeting e o resolver subsequente; Orbit/summons têm lifecycle próprio. | [Form e seus overloads][projectile], [base][base-augment]. Não inferir resize, pierce, despawn ou novos custos a partir da quantidade; addFreshEntity é solicitado sem converter cada tentativa em spawn/hit confirmado. |
| Custos, cast, cooldown e aprendizagem | Mana-padrão20, tier III; recipe `ars_nouveau:relay_splitter` + `ars_nouveau:wilden_spike` + `minecraft:stonecutter`, XP-padrão160. Cast/cooldown autônomos **N/A**; config do glyph/receptor pode alterar custo. | [Defaults][augment], [recipe][recipes], [XP][recipe-xp], [custo efetivo][part-cost], [custo por receptor][base-augment], [aquisição](../../ACQUISITION.md). Não acrescentar segundo débito ou XP por projétil. |
| Integração e mutabilidade | O [builder/evento nativo][build-stats] é identificado; não há adapter RPG/BA comprovado para alterar a lista/count antes do spawn preservando validação, mana e correlação. **⛔ SEM_HOOK_SEGURO / NOT_VERIFIED** para perk mutadora. | Observação de criação ou impacto não autoriza duplicar entidades nem reexecutar o resolver. O evento público exige contrato específico; não é integração aceita por esta ficha. |
| Validação e limites da prova | Fonte fixa auditada por consumer, identidade compilada SHA-exata; métodos e comportamento em jogo não foram homologados. | [Prova binária](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), [matriz](../../PERK-ENGINEERING-MATRIX-5.13.1.md). `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`; quantidade final, sync, multiplayer, unload e budgets pendentes. |

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
[augment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentSplit.java#L7-L28
[projectile]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java#L51-L128
[orbit]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectOrbit.java#L24-L55
[undead]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonUndead.java#L35-L68
