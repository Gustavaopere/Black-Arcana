# Amplify

- Registry ID: `ars_nouveau:glyph_amplify`
- Source class: `AugmentAmplify`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **1**
- Default mana: **20**

## Source-pinned behavior

Adds **+1.0** amplification. Compatible Ars Nouveau glyphs decide what amplification means; provider documentation/source examples include increased spell damage and higher Break harvest capability.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:diamond_pickaxe`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Amplification is an Ars spell stat, not a universal Black Arcana damage scalar. Black Arcana power remains governed by its own caps, budgets and diminishing-return contracts.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Mapeamento de perk para Codex — transformação real

- **Source pin:** [`AugmentAmplify.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAmplify.java) no Ars Nouveau 5.13.1.
- **Transformação exata:** `applyModifiers(SpellStats.Builder builder, AbstractSpellPart spellPart)` chama `builder.addAmplification(1.0)`. `getDefaultManaCost=20`, tier I. **Interpretação:** efeitos escolhem como usar `spellStats.getAmpMultiplier()`; Harm aumenta dano/Poison, Explosion aumenta intensidade e altera dano via `ANExplosion`, Break altera capacidade de harvest. **Limites:** caps são declarados por cada glyph receptor, por exemplo Harm/Explosion limit 2 e Wither limit 4; Amplify não autoriza todas as combinações e um bonus RPG genérico que supere limites não é automaticamente seguro.
- **Bridge:** `source identified / mutation hook NOT VERIFIED / provider-owned`. Não implementar segundo `SpellStats` no Black Arcana, nem usar atributos RPG sem seam verificado. Testes em modpack/Survival PENDING.

## Revisão técnica para índice de perks — 25/10/2026

**Escopo de conclusão: ✅ CATÁLOGO TÉCNICO ESTÁTICO SOURCE-PINNED (5.13.1); ⛔ CONTRATO DE PERK MUTADORA NÃO COMPROVADO; ⚠️ QA FÍSICO PENDENTE.** O ✅ nesta ficha **não significa** que um perk de Amplify já possa ser implementado nem que a configuração ou o cliente instalados tenham sido homologados.

| Eixo exigido | Contrato verificado ou não aplicável | Evidência / limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_amplify`, augment do Ars Nouveau 5.13.1, tier-padrão I. | Registro compilado dentro do roster exato 85 glyphs + 24 rituals: [IDs SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Implementação-fonte [`AugmentAmplify.java` no commit fixo](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAmplify.java). |
| Efeito e comportamento | `applyModifiers(SpellStats.Builder, AbstractSpellPart)` executa `builder.addAmplification(1.0)`, depois delega ao super. A interpretação de amplificação pertence ao glyph consumidor, **não** a um dano universal. | Método-fonte no commit fixo, [matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). |
| Parâmetro, escala e cap | Incremento **+1,0 por aplicação aceita**, não `+100% damage` universal. Compatibilidade, multiplicação efetiva e limite máximo são definidos pelo componente receptor, não por este augment; nenhum cap global é inferido. | `AugmentAmplify.applyModifiers`, consumidores e limites parciais documentados na matriz de engenharia; qualquer cap específico exige evidência do glyph receptor. |
| Alvo, área, projétil, tipo de dano e duração | **NÃO APLICÁVEIS COMO PARÂMETROS PRÓPRIOS DESTE AUGMENT:** ele altera exclusivamente o builder de `SpellStats`; Form/Effect da composição estabelece delivery/target/área/tipo de dano/tempo. Não é spell de ataque independente. | Contrato da classe `AbstractAugment` e implementação `AugmentAmplify`; [modelo composicional do provider](../../README.md). |
| Custos, cast, cooldown e aprendizagem | Mana-padrão **20** para o glyph em composição; tier I; recipe-padrão `minecraft:diamond_pickaxe` e **27 XP** para aprendizado. **Não há cast ou cooldown autônomos do augment**: são propriedades da magia composta/provedor. Valores de config implantada não foram lidos. | `getDefaultManaCost`, `defaultTier`, [datagen/XP e aquisição 85/85](../../ACQUISITION.md). |
| Integração, autoridade e mutabilidade | A alteração de `SpellStats` é provider-owned. A API pública `SpellModifierEvent` expõe o builder antes da resolução, mas não há contrato de adapter RPG Skill Tree/Black Arcana com caps, custos e deduplicação validado; **⛔ SEM_HOOK_SEGURO** para considerar a perk integrada. Ver [fases e limites da API](../../AUGMENT-STATIC-CERTIFICATION-5.13.1.md). Não criar segundo `SpellStats`, não reexecutar efeitos nem confundir Source com player mana. | [matriz técnica](../../PERK-ENGINEERING-MATRIX-5.13.1.md), [decisões de arquitetura](../../../../../../plans/DECISIONS.md). |
| Grau de validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY**: fonte fixada em `112920ff774831f204031da75b4c4e73d3765157` e identidade de glyph documentada para JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. O classfile `applyModifiers` e o fluxo de composição instalados não foram comparados linha a linha; **nenhuma execução real / QA de config ou modpack** foi realizada nesta certificação. | [auditoria da identidade binária](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) e [matriz source-pinned](../../PERK-ENGINEERING-MATRIX-5.13.1.md). |

**Condição de invalidação:** troca de JAR/commit, alteração de `applyModifiers`, custo/tier/config ou inclusão de hooks reais exige revisão. **O ✅ certifica somente que os campos relevantes ao contrato estático do componente estão devidamente classificados (inclusive os não aplicáveis e bloqueados)**. Não homologa integração, recast, Mastery, gameplay, Stage ou compatibilidade real. Outros glifos continuam individualmente pendentes.
