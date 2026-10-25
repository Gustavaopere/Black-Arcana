# Randomize

- Registry ID: `ars_nouveau:glyph_randomize`
- Source class: `AugmentRandomize`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **1**
- Default mana: **0**

## Source-pinned behavior

Marks Ars Nouveau spell stats as randomized. Compatible glyphs define the resulting behavior. The exact provider description specifically identifies block-selection randomization for glyphs such as Place Block and Exchange, using blocks available through the provider's spell context/hotbar behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:pink_carpet` ×2.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns the randomization algorithm and compatible-glyph interpretation. Black Arcana randomness must remain server-owned, deterministic where required for replay/tests, and bounded independently.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentRandomize.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentRandomize.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** overload de `applyModifiers(builder,part,hit,world,shooter,context)` retorna `builder.randomize()`; default mana 0, tier I. A classe não implementa um RNG global nem retorna um valor de chance.
- **Consumidores comprovados:** `EffectBreak` usa `world.random.nextFloat() < count(Randomize)*0.25F` para **pular** alguns candidatos; `EffectPlaceBlock` usa `InventoryManager.extractRandomItem` em vez de `extractItem`. Ambas são semânticas diferentes.
- **Perks:** exigir RNG server-side, limites e previsão clara da semântica por receptor; nenhum hook de alterar semente/roll externo foi verificado.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ contrato técnico estático source-pinned de 5.13.1; ⛔ integração de perk mutadora não comprovada; ⚠️ QA físico NOT_TESTED.** `technical_perk_dossier: 1`. Esta revisão classifica os campos do componente composicional; não certifica o provider inteiro, a configuração implantada ou uma execução em jogo.

| Eixo exigido | Contrato estático e consumidor | Evidência / limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_randomize`, classe `AugmentRandomize`, augment Ars Nouveau 5.13.1; tier-padrão **I**. | [Classe][class]; [roster de identidade binária SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Display e ID não criam uma ação independente. |
| Efeito e comportamento | O overload `applyModifiers(builder,part,hit,world,shooter,context)` devolve `builder.randomize()`: define flag boolean true. Repetir esse setter não soma uma intensidade; os consumidores também podem consultar a contagem separadamente. Builder aplica os augments antes de publicar `SpellModifierEvent`. [Classe][class], [flag][random-flag], [build][builder], [counts][stats]. | O Form/Effect recebe o augment na composição Ars; setter/contagem não executam um segundo cast. |
| Parâmetros, escala e caps | Sem porcentagem própria universal. No Break, cada candidato é ignorado quando `world.random.nextFloat()<n×0.25F`, `n=count(Randomize)`; não há clamp local dessa expressão. Em `IDamageEffect`, o ajuste é `n×nextIntBetweenInclusive(-1,1)`, portanto −n/0/+n antes do Pre, não n rolls independentes. Place Block/Exchange escolhem `extractRandomItem` no inventário de maior prioridade elegível, sem prova de distribuição uniforme sobre toda hotbar/inventário. [Break][break-rng], [dano][damage-rng], [place][place-rng], [exchange][exchange-rng], [inventário][inventory-rng]. | Defaults de cada receptor e configuração implantada são evidências separadas; `per_spell_limit` e limites do receptor são [configuráveis][limits]. |
| Targeting, área, projétil, tipo e duração | **N/A como delivery próprio:** não define alvo/área/projétil/tipo/duração autônomos. Pode mudar seleção de blocos ou dano somente nos consumidores que leem flag/count; Break continua a testar harvest/claims/blacklist após o roll. Randomizar não é autorização de world mutation ou retarget de outra autoridade. [Break][break-rng], [contrato][augment-base]. | Classificar o campo próprio como não aplicável não elimina a semântica específica no receptor. |
| Custos, cast, cooldown e aprendizagem | Mana default **0**, tier **I**; recipe-padrão **minecraft:pink_carpet ×2**, **27 XP**. Sem cast/cooldown autônomo: o custo compõe a magia Ars e pode ser sobrescrito por config/custo do receptor. Starter default false, sujeito a configuração. | [Classe][class], [recipe gerada][recipe], [getCastingCost/tier][config], [getCostForPart][augment-base] e [aquisição catalogada](../../ACQUISITION.md). Source de mundo e mana do jogador continuam distintos. |
| Integração e autoridade | Ars publica [SpellModifierEvent][modifier-event] com builder após aplicar augments/itens [no build][builder]; existe superfície source. Um adapter RPG/Black Arcana que preserve contexto, custos, caps e deduplicação não foi comprovado. **⛔ SEM_HOOK_SEGURO para a integração de perk proposta / mutating_hook=NOT_VERIFIED**. | Não negar a API pública existente nem promovê-la a integração testada. Não manter SpellStats, loot, seleção ou settlement paralelo. [Matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). |
| Grau de validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY**: source imutável `112920ff774831f204031da75b4c4e73d3765157`; identidade JAR `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Nenhuma comparação integral de método compilado ou execução física é alegada nesta ficha. | [Prova de IDs](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config/modpack/Survival, eventos e mutação por perk permanecem NOT_TESTED/NOT_VERIFIED; nenhum Stage promovido. |

**Fase e deduplicação:** flag, quantidade de augments e chamadas RNG são dados diferentes. O mesmo count tem semânticas distintas por Effect; não prometer bônus sempre positivo, mesma semente por cast ou replay determinístico do provider. A fonte do RNG e a ordem de eventos pertencem ao consumer; um perk exige contrato próprio de cap/causalidade, sem rolar de novo em paralelo.

**Invalidação:** mudança de release/hash/source, composição, config, consumidor ou contrato de integração exige nova revisão. O ✅ cobre apenas os campos estáticos documentados; Form/Effect e provider mantêm recursos, targeting e efeitos.

[augment-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L32-L60
[stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L57
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L162
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L255
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentRandomize.java#L1-L35
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_randomize.json#L1-L16
[random-flag]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L255-L258
[break-rng]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L60-L89
[damage-rng]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L39-L78
[place-rng]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPlaceBlock.java#L79-L89
[exchange-rng]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExchange.java#L70-L107
[inventory-rng]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L111-L124
