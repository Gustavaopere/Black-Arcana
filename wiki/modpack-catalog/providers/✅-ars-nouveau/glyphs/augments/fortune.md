# Fortune / Luck

- Registry ID: `ars_nouveau:glyph_fortune`
- Source class: `AugmentFortune`
- Source display name: `Luck`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **80**

## Source-pinned behavior

Increases relevant drop chances for compatible provider behavior, including mobs killed through the provider damage path and blocks broken through Break. Its description declares incompatibility with Extract; effective rejection of that pair is not established here.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:rabbit_foot`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns its loot/fortune calculations and compatible-glyph semantics. Black Arcana must preserve provider causal identity and must not double-apply external Fortune/Looting-style rewards.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentFortune.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentFortune.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `AugmentFortune` não sobrescreve `applyModifiers` em 5.13.1; mana default 80, tier II, ID de registry `glyph_fortune` embora display `Luck`.
- **Break:** `getBuffCount(AugmentFortune.INSTANCE)` determina nível de `FORTUNE` aplicado à ferramenta simulada quando o item ainda não o tem nesse nível; limite default da `EffectBreak`: 4. Outros consumos de loot dependem de classes de efeito específicas (não presumir chance universal de drop).
- **Perks:** não dar double drops ao RPG por evento de break/hit; preservar incompatibilidade semântica com Extract.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo: ✅ contrato técnico estático source-pinned de 5.13.1; ⛔ integração de perk mutadora não comprovada; ⚠️ QA físico NOT_TESTED.** `technical_perk_dossier: 1`. Esta revisão classifica os campos do componente composicional; não certifica o provider inteiro, a configuração implantada ou uma execução em jogo.

| Eixo exigido | Contrato estático e consumidor | Evidência / limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_fortune`, classe `AugmentFortune`, augment Ars Nouveau 5.13.1; tier-padrão **II**. | [Classe][class]; [roster de identidade binária SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Display e ID não criam uma ação independente. |
| Efeito e comportamento | `AugmentFortune` (display Luck) não sobrescreve `applyModifiers`; o builder herdado é devolvido. Os consumidores leem `count(Fortune)`. Break eleva Fortune da ferramenta simulada ao count se o nível atual for menor; `IDamageEffect#attemptDamage` grava luckLevel somente quando a fonte é `DamageUtil.SpellDamageSource`, antes dos eventos/settlement. [Classe][class], [herança][augment-base], [counts][stats], [Break][break], [dano/loot][damage-loot]. | O Form/Effect recebe o augment na composição Ars; setter/contagem não executam um segundo cast. |
| Parâmetros, escala e caps | Count é o nível solicitado, não porcentagem universal de drops. Limite default **4 no receptor EffectBreak**, não cap global do augment. Nos mixins de loot, o ramo que consulta spellLuck exige atributo DRYGMY do atacante e usa `max(spellLuck,lootingOriginal)+(int)DRYGMY`; sem esse atributo conserva o valor original. Drops finais continuam com a loot table/engine/config do provider. [Cap][break-cap], [chance de loot][loot-chance], [quantidade][loot-count]. | Defaults de cada receptor e configuração implantada são evidências separadas; `per_spell_limit` e limites do receptor são [configuráveis][limits]. |
| Targeting, área, projétil, tipo e duração | **N/A próprios:** não cria ataque, alvo, área, projétil ou duração. Aplica-se ao Form/Effect que o aceita, com filtros, permissões e autoria daquele consumidor. Break respeita harvest/claims/blacklist; o helper de dano pode vetar alvo, cancelar no Pre ou falhar em hurt antes do Post. Não gerar drops ou XP extras no RPG por observar esses eventos. [Break][break], [dano][damage-loot]. | Classificar o campo próprio como não aplicável não elimina a semântica específica no receptor. |
| Custos, cast, cooldown e aprendizagem | Mana default **80**, tier **II**; recipe-padrão **minecraft:rabbit_foot**, **55 XP**. Sem cast/cooldown autônomo: o custo compõe a magia Ars e pode ser sobrescrito por config/custo do receptor. Starter default false, sujeito a configuração. | [Classe][class], [recipe gerada][recipe], [getCastingCost/tier][config], [getCostForPart][augment-base] e [aquisição catalogada](../../ACQUISITION.md). Source de mundo e mana do jogador continuam distintos. |
| Integração e autoridade | Ars publica [SpellModifierEvent][modifier-event] com builder após aplicar augments/itens [no build][builder]; existe superfície source. Um adapter RPG/Black Arcana que preserve contexto, custos, caps e deduplicação não foi comprovado. **⛔ SEM_HOOK_SEGURO para a integração de perk proposta / mutating_hook=NOT_VERIFIED**. | Não negar a API pública existente nem promovê-la a integração testada. Não manter SpellStats, loot, seleção ou settlement paralelo. [Matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). |
| Grau de validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY**: source imutável `112920ff774831f204031da75b4c4e73d3765157`; identidade JAR `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Nenhuma comparação integral de método compilado ou execução física é alegada nesta ficha. | [Prova de IDs](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config/modpack/Survival, eventos e mutação por perk permanecem NOT_TESTED/NOT_VERIFIED; nenhum Stage promovido. |

**Compatibilidade:** as descrições de Fortune/Extract dizem que o par é incompatível. Não foi comprovada rejeição default desse par: Break aceita ambos e tem `if` separados para Fortune e Silk Touch; `AbstractSpellPart` não adiciona uma combinação inválida no default. A configuração de combos e a validação aplicada à composição precisam ser preservadas, sem prometer que a descrição já impõe veto. [Classe][class], [Break][break-cap], [default combos][default-combos].

**Invalidação:** mudança de release/hash/source, composição, config, consumidor ou contrato de integração exige nova revisão. O ✅ cobre apenas os campos estáticos documentados; Form/Effect e provider mantêm recursos, targeting e efeitos.

[augment-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L32-L60
[stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L57
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L162
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L255
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentFortune.java#L1-L28
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_fortune.json#L1-L13
[break]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L52-L89
[break-cap]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java#L98-L127
[damage-loot]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L39-L78
[loot-chance]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/looting/LootItemRandomChanceWithEnchantedBonusConditionMixin.java#L20-L35
[loot-count]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/looting/EnchantedCountIncreaseFunctionMixin.java#L20-L35
[default-combos]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L299-L305
