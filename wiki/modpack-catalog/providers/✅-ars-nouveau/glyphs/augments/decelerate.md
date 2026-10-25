# Decelerate

- Registry ID: `ars_nouveau:glyph_decelerate`
- Source class: `AugmentDecelerate`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **5**

## Source-pinned behavior

Adds **-0.5** to Ars Nouveau's acceleration modifier. Compatible provider glyphs interpret that value; Projectile uses it to reduce projectile velocity.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:soul_sand` + `minecraft:cobweb` + `minecraft:clock`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns compatible-glyph selection, acceleration semantics and configured mana cost. This is not a Black Arcana-wide speed modifier.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentDecelerate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDecelerate.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.addAccelerationModifier(-0.5F)`; custo default 5, tier II.
- **Consumo:** `MethodProjectile` usa `velocity=Math.max(0.1f,0.75f+getAccMultiplier()/2)`; um Decelerate contribui −0.25 no termo antes do piso de 0.1 (mantidos os demais modificadores).
- **Perks:** velocidade menor não equivale a maior duração de entidade, controle temporal nem penetração; o lifetime default do Projectile permanece configurável por outro campo.
- **Mutação externa:** o contrato de integração por perk RPG/Black Arcana continua **NOT_VERIFIED**; a revisão abaixo identifica a API pública sem presumir um adapter validado. Config real, Survival e integração permanecem condicionados.

## Revisão técnica para índice de perks — 25/10/2026

`technical_perk_dossier: 1`. **Escopo: contrato técnico estático SOURCE-PINNED 5.13.1; ⛔ contrato mutador RPG/Black Arcana não comprovado; ⚠️ QA físico NOT_TESTED.** A classificação estática exige revisão do manifesto e não concede autoridade para executar uma segunda magia.

| Eixo exigido | Contrato auditado | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_decelerate`, classe `com.hollingsworth.arsnouveau.common.spell.augment.AugmentDecelerate`, augment tier-padrão II. | [Classe][ta-class] no commit 112920ff774831f204031da75b4c4e73d3765157; [identidade compilada SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. |
| Comportamento e recebedor | `addAccelerationModifier(−0.5F)` sobre `A=aceleração acumulada`. applyModifiers altera o builder e delega ao super. MethodProjectile interpreta A como input da velocidade inicial de shoot. O overload legado sobre BlockPos define delta(0,−0.1,0) sem ler A; reduzir velocidade nesse caminho não está demonstrado. | [Operador][ta-class], [AbstractAugment][ta-base], [build e ordem][ta-build]. O builder executa cada augment aceito antes dos modificadores de item e do evento final. |
| Parâmetros, escala e caps | Cada aplicação aceita soma **−0,5** a A. Na emissão normal de Projectile, `v=max(0.1,0.75+A/2)`; mantidos os outros modificadores, contribuição **−0,25** antes do piso 0.1 (exemplo A inicial 0: 0.75→0.5). O piso pertence a esse consumidor, sem cap universal de velocidade ou duração. Compatibilidade e limites pertencem à Form/Effect receptora e suas configs; Projectile declara Accelerate/Decelerate compatíveis. getAugmentLimit/augment_limits e per_spell_limit são contratos distintos, não cap físico global. [Stats][ta-stats], [emissão][ta-consumer], [compatibilidade][ta-compatible], [limites][ta-limits], [mapa][ta-cap-map]. | Valores de config implantada, combinação aceita e efeitos de terceiros não foram observados. Não inferir dose, alvo ou budget universal. |
| Targeting, área, projétil, dano e duração | **N/A como parâmetros próprios:** alvo, LOS, área, hitbox, tipo de dano e duração. A Form/Effect e a entidade executora os definem. Este augment não cria projétil nem fixa lifetime; seu stat pode influenciar a velocidade inicial apenas onde lido. [Base][ta-base], [consumidor][ta-consumer]. | O alvo é da composição; N/A não apaga os efeitos downstream que leem o stat ou a contagem. |
| Custos, cast, cooldown e aprendizado | Mana-padrão **5**; tier II, recipe glyph-padrão**55 XP**, starter default **não**. Receita e ingredientes acima. Sem cast ou cooldown próprios; Ars controla mana da composição e aprendizagem. | [Default][ta-class], [recipe gerada][ta-recipe], [custo após config][ta-cost], [custo por receptor][ta-base], [config][ta-limits], [starter][ta-starter], [aquisição](../../ACQUISITION.md). Overrides do receptor e config podem alterar o custo; Source de mundo/crafting não é player mana. |
| Integração, autoridade e mutabilidade | Há superfície pública source-localizada: `SpellStats.Builder.build` publica `SpellModifierEvent` após augments/itens e antes de retornar stats; o evento expõe builder mutável. Isso não valida um adapter de perk com custo, compatibilidade, caps, origem e dedup. **⛔ SEM_HOOK_SEGURO para integração RPG/Black Arcana neste catálogo; mutating_hook=NOT_VERIFIED.** | [Build][ta-build], [evento][ta-event], [matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). Não negar a API pública nem tratá-la como bridge implementada; preservar Ars como dono de SpellStats/resolver/settlement. |
| Validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY.** Revisão de operadores e consumidores nas referências fixas, sem comparação integral dos métodos/classfiles ou execução de efeito. | Fonte 112920ff774831f204031da75b4c4e73d3765157 e [IDs JAR SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config implantada, Survival/cliente/multiplayer, pacote de mods, adapter e QA físico **NOT_TESTED**. Nenhum Stage promovido. |

A velocidade de lançamento não redefine a hitbox, a quantidade Split ou o lifespan. `EntityProjectileSpell` compara age com `getExpirationTime()`, que lê o lifespan da Form×20; esse é outro consumidor. [Lifecycle][ta-lifetime], [expiry][ta-expiry].

**Invalidação:** alteração do source/JAR/config, operador, compatibilidade/caps do receptor, recipe/tier ou novo contrato mutador exige revisão por campo. Este dossiê classifica o componente estático, não certifica todas as combinações Ars ou todo o provider.

[ta-class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDecelerate.java#L9-L37
[ta-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L15-L60
[ta-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L131-L152
[ta-stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L224-L243
[ta-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L125-L145
[ta-limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L268
[ta-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[ta-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_decelerate.json#L1-L19
[ta-cap-map]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/util/SpellPartConfigUtil.java#L34-L64
[ta-consumer]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java#L51-L95
[ta-compatible]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java#L125-L138
[ta-lifetime]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L138-L158
[ta-expiry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L226-L228

[ta-starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
