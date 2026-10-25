# Extract

- Registry ID: `ars_nouveau:glyph_extract`
- Source class: `AugmentExtract`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **30**

## Source-pinned behavior

Compatible Break usage simulates Silk Touch. Explosion selects DESTROY instead of DESTROY_WITH_DECAY when Extract is present; final block destruction and drops remain engine-owned. The provider description declares incompatibility with Fortune/Luck, whose effective enforcement is not established here.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:emerald`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns loot/extraction semantics and its compatibility matrix. Black Arcana destructive block effects remain governed by `WorldEffectPolicy`; this glyph cannot be used as a generic bypass for protection, drops or world-mutation policy.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentExtract.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentExtract.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** a classe `AugmentExtract` não sobrescreve `applyModifiers` nesta versão; consumers verificam `spellStats.getBuffCount(AugmentExtract.INSTANCE)`/`hasBuff`. Mana default 30, tier II.
- **Break:** usa count Extract como nível simulado de `SILK_TOUCH` no `ItemStack` da ferramenta. **Explosion:** seleciona `Explosion.BlockInteraction.DESTROY` em vez de `DESTROY_WITH_DECAY` quando tem Extract; as consequências de drops são liquidadas pela engine.
- **Perks:** Extract e Fortune são descritos como incompatíveis pelo provider. Não transformar o augment em uma duplicação direta dos blocos/itens; claims e eventos do provider continuam mandatórios.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ contrato técnico estático source-pinned de 5.13.1; ⛔ integração de perk mutadora não comprovada; ⚠️ QA físico NOT_TESTED.** `technical_perk_dossier: 1`. Esta revisão classifica os campos do componente composicional; não certifica o provider inteiro, a configuração implantada ou uma execução em jogo.

| Eixo exigido | Contrato estático e consumidor | Evidência / limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_extract`, classe `AugmentExtract`, augment Ars Nouveau 5.13.1; tier-padrão **II**. | [Classe][class]; [roster de identidade binária SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Display e ID não criam uma ação independente. |
| Efeito e comportamento | A classe não sobrescreve `applyModifiers`: o método herdado devolve o builder. `SpellStats#getBuffCount/hasBuff` preserva a presença/contagem; os efeitos consumidores executam extração/loot. No Break, count de Extract determina Silk Touch na ferramenta simulada quando supera o encantamento atual. Em `AbstractEffect`, presença significa Silk Touch **1**; esses dois consumidores não são equivalentes. [Classe][class], [herança][augment-base], [counts][stats], [Break][break], [helper][effect-tool]. | O Form/Effect recebe o augment na composição Ars; setter/contagem não executam um segundo cast. |
| Parâmetros, escala e caps | `n=count(Extract)` por receptor; não é dano nem chance universal. Break usa `SILK_TOUCH=n`; o helper genérico usa nível1 por presença. Explosion escolhe `DESTROY` com Extract e `DESTROY_WITH_DECAY` sem ele: a seleção não garante conservar blocos ou drops finais. Não há cap próprio nesta classe nem entrada de Extract no mapa de limites default do Break; os limites de composição/config continuam aplicáveis. [Break][break], [limite receptor][break-cap], [explosion][explosion], [config][limits]. | Defaults de cada receptor e configuração implantada são evidências separadas; `per_spell_limit` e limites do receptor são [configuráveis][limits]. |
| Targeting, área, projétil, tipo e duração | **N/A como ação autônoma:** o augment não seleciona alvo, área, projétil, tipo de dano ou duração. Break/Explosion/Knockback/Toss podem interpretar sua presença de modos diferentes. Break mantém harvest, claims e blacklist antes de tentar quebrar o bloco; não inferir permissão de mundo pelo augment. [Break][break], [contrato][augment-base]. | Classificar o campo próprio como não aplicável não elimina a semântica específica no receptor. |
| Custos, cast, cooldown e aprendizagem | Mana default **30**, tier **II**; recipe-padrão **minecraft:emerald**, **55 XP**. Sem cast/cooldown autônomo: o custo compõe a magia Ars e pode ser sobrescrito por config/custo do receptor. Starter default false, sujeito a configuração. | [Classe][class], [recipe gerada][recipe], [getCastingCost/tier][config], [getCostForPart][augment-base] e [aquisição catalogada](../../ACQUISITION.md). Source de mundo e mana do jogador continuam distintos. |
| Integração e autoridade | Ars publica [SpellModifierEvent][modifier-event] com builder após aplicar augments/itens [no build][builder]; existe superfície source. Um adapter RPG/Black Arcana que preserve contexto, custos, caps e deduplicação não foi comprovado. **⛔ SEM_HOOK_SEGURO para a integração de perk proposta / mutating_hook=NOT_VERIFIED**. | Não negar a API pública existente nem promovê-la a integração testada. Não manter SpellStats, loot, seleção ou settlement paralelo. [Matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). |
| Grau de validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY**: source imutável `112920ff774831f204031da75b4c4e73d3765157`; identidade JAR `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Nenhuma comparação integral de método compilado ou execução física é alegada nesta ficha. | [Prova de IDs](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config/modpack/Survival, eventos e mutação por perk permanecem NOT_TESTED/NOT_VERIFIED; nenhum Stage promovido. |

**Compatibilidade declarada versus enforcement:** o texto de `getBookDescription` declara incompatibilidade com Fortune. Estas classes não definem um veto do par; Break lista ambos como compatíveis e aplica os encantamentos em dois `if` independentes. `invalidCombinations` parte de configuração nula e o default de combos é vazio. A rejeição efetiva do par em configuração/runtime **NÃO FOI VERIFICADA**; não transformar a descrição em guard confirmado. [Texto][class], [Break][break-cap], [combos][combos], [default combos][default-combos].

**Invalidação:** mudança de release/hash/source, composição, config, consumidor ou contrato de integração exige nova revisão. O ✅ cobre apenas os campos estáticos documentados; Form/Effect e provider mantêm recursos, targeting e efeitos.

[augment-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L32-L60
[stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L57
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L162
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L255
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentExtract.java#L1-L28
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_extract.json#L1-L13
[break]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L52-L89
[break-cap]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L98-L127
[effect-tool]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L116-L124
[explosion]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExplosion.java#L37-L44
[combos]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L73-L96
[default-combos]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L299-L305
