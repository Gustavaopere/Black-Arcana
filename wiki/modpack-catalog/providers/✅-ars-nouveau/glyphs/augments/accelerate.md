# Accelerate

- Registry ID: `ars_nouveau:glyph_accelerate`
- Source class: `AugmentAccelerate`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **10**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's acceleration modifier. Provider glyphs that declare Accelerate compatible interpret that stat; Projectile uses it to increase projectile velocity.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:powered_rail` + `minecraft:sugar` + `minecraft:clock`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns augment compatibility, acceleration semantics and effective configured cost. Black Arcana must not treat this modifier as a universal projectile-speed API.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentAccelerate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAccelerate.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers(SpellStats.Builder,AbstractSpellPart)` chama `builder.addAccelerationModifier(1.0F)`; custo default 10, tier II.
- **Consumidor comprovado:** `MethodProjectile.summonProjectiles` usa `velocity=Math.max(0.1f,0.75f+spellStats.getAccMultiplier()/2)`. O +1.0 do operador contribui +0.5 à expressão de velocidade quando não há outros modificadores, **não** +1 bloco/tick universal.
- **Perks:** velocidade e quantidade de projéteis são variáveis distintas. Respeitar `getCompatibleAugments` da Form e permitir apenas bridges com assinatura verificável.
- **Mutação externa:** o contrato de integração por perk RPG/Black Arcana continua **NOT_VERIFIED**; a revisão abaixo identifica a API pública sem presumir um adapter validado. Config real, Survival e integração permanecem condicionados.

## Revisão técnica para índice de perks — 25/10/2026

`technical_perk_dossier: 1`. **Escopo: contrato técnico estático SOURCE-PINNED 5.13.1; ⛔ contrato mutador RPG/Black Arcana não comprovado; ⚠️ QA físico NOT_TESTED.** A classificação estática exige revisão do manifesto e não concede autoridade para executar uma segunda magia.

| Eixo exigido | Contrato auditado | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_accelerate`, classe `com.hollingsworth.arsnouveau.common.spell.augment.AugmentAccelerate`, augment tier-padrão II. | [Classe][ta-class] no commit 112920ff774831f204031da75b4c4e73d3765157; [identidade compilada SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. |
| Comportamento e recebedor | `addAccelerationModifier(+1.0F)` sobre `A=aceleração acumulada`. O overload de applyModifiers altera o builder e retorna o super, que retorna o mesmo builder. A Form interpreta o stat: MethodProjectile usa A no parâmetro de shoot; o overload legado de emissão sobre BlockPos usa delta(0,−0.1,0) e não lê A. | [Operador][ta-class], [AbstractAugment][ta-base], [build e ordem][ta-build]. O builder executa cada augment aceito antes dos modificadores de item e do evento final. |
| Parâmetros, escala e caps | Cada aplicação aceita soma **+1,0** a A. Na emissão normal de Projectile, `v=max(0.1,0.75+A/2)`; mantidos os outros modificadores, uma ocorrência muda o termo de velocidade em **+0,5** (exemplo A inicial 0: 0.75→1.25). Não é aceleração física contínua ou bônus universal em blocks/tick. Compatibilidade e limites pertencem à Form/Effect receptora e suas configs; Projectile declara Accelerate/Decelerate compatíveis. getAugmentLimit/augment_limits e per_spell_limit são contratos distintos, não cap físico global. [Stats][ta-stats], [emissão][ta-consumer], [compatibilidade][ta-compatible], [limites][ta-limits], [mapa][ta-cap-map]. | Valores de config implantada, combinação aceita e efeitos de terceiros não foram observados. Não inferir dose, alvo ou budget universal. |
| Targeting, área, projétil, dano e duração | **N/A como parâmetros próprios:** alvo, LOS, área, hitbox, tipo de dano e duração. A Form/Effect e a entidade executora os definem. Este augment não cria projétil nem fixa lifetime; seu stat pode influenciar a velocidade inicial apenas onde lido. [Base][ta-base], [consumidor][ta-consumer]. | O alvo é da composição; N/A não apaga os efeitos downstream que leem o stat ou a contagem. |
| Custos, cast, cooldown e aprendizado | Mana-padrão **10**; tier II, recipe glyph-padrão**55 XP**, starter default **não**. Receita e ingredientes acima. Sem cast ou cooldown próprios; Ars controla mana da composição e aprendizagem. | [Default][ta-class], [recipe gerada][ta-recipe], [custo após config][ta-cost], [custo por receptor][ta-base], [config][ta-limits], [starter][ta-starter], [aquisição](../../ACQUISITION.md). Overrides do receptor e config podem alterar o custo; Source de mundo/crafting não é player mana. |
| Integração, autoridade e mutabilidade | Há superfície pública source-localizada: `SpellStats.Builder.build` publica `SpellModifierEvent` após augments/itens e antes de retornar stats; o evento expõe builder mutável. Isso não valida um adapter de perk com custo, compatibilidade, caps, origem e dedup. **⛔ SEM_HOOK_SEGURO para integração RPG/Black Arcana neste catálogo; mutating_hook=NOT_VERIFIED.** | [Build][ta-build], [evento][ta-event], [matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). Não negar a API pública nem tratá-la como bridge implementada; preservar Ars como dono de SpellStats/resolver/settlement. |
| Validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY.** Revisão de operadores e consumidores nas referências fixas, sem comparação integral dos métodos/classfiles ou execução de efeito. | Fonte 112920ff774831f204031da75b4c4e73d3765157 e [IDs JAR SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config implantada, Survival/cliente/multiplayer, pacote de mods, adapter e QA físico **NOT_TESTED**. Nenhum Stage promovido. |

A velocidade de lançamento não redefine a hitbox, a quantidade Split ou o lifespan. `EntityProjectileSpell` compara age com `getExpirationTime()`, que lê o lifespan da Form×20; esse é outro consumidor. [Lifecycle][ta-lifetime], [expiry][ta-expiry].

**Invalidação:** alteração do source/JAR/config, operador, compatibilidade/caps do receptor, recipe/tier ou novo contrato mutador exige revisão por campo. Este dossiê classifica o componente estático, não certifica todas as combinações Ars ou todo o provider.

[ta-class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAccelerate.java#L9-L37
[ta-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L15-L60
[ta-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L131-L152
[ta-stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L224-L243
[ta-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L125-L145
[ta-limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L268
[ta-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[ta-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_accelerate.json#L1-L19
[ta-cap-map]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/util/SpellPartConfigUtil.java#L34-L64
[ta-consumer]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java#L51-L95
[ta-compatible]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java#L125-L138
[ta-lifetime]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L138-L158
[ta-expiry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L226-L228

[ta-starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
