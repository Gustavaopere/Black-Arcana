# Annihilation Arrow

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, identidade estática `legendary_spellbooks:annihilation_arrow` / classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationArrowSpell` — [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Valores/custos descritos da fonte continuam **⚠️ sem validação runtime/Survival**; +0 raízes.

- ID: `legendary_spellbooks:annihilation_arrow`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–8
- Min rarity: Rare
- Cooldown: 10 s
- Long cast field: 30 ticks
- Mana neutral: 80 / 90 / 100 / 110 / 120 / 130 / 140 / 150
- Spell power neutral: 8 / 10 / 12 / 14 / 16 / 18 / 20 / 22
- Max-HP damage: `0.25% × spellLevel`
- Crafting: habilitado no config
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Dispara `AnnihilationArrowEntity`; o projectile recebe o spell power e uma parcela adicional de vida máxima do alvo. O provider é autoridade da explosão/impacto e do damage source.

## Acquisition

Não aparece no custom `LSSpellScrollLootProvider`; o config não desabilita crafting. Não inventar boss drop adicional.

## Regra para o Black Arcana

Não adicionar segundo dano percentual, explosão ou projectile callback.

## Source

`AnnihilationArrowSpell.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast / mana | Cooldown 10 s; níveis 1–8; castTime=30 ticks; baseManaCost=80, +10 por nível; spell power neutro=8+2×(nível−1). | Host Iron's; custo efetivo e cooldown do modpack NÃO VERIFICADOS. |
| Origem/lançamento | onCast cria uma AnnihilationArrowEntity em eyePosition + forward (1 bloco), owner caster, recebe damage=getSpellPower e componente percentual HP 0.0025×spellLevel. | Alteração de spawn/velocidade/range por perk ⛔ sem hook. |
| Hit / DamageSource | AnnihilationArrowEntity.onHitEntity usa getDamage + target.maxHealth×hpDamage; DamageSources.applyDamage(..., spell.getDamageSource(arrow,caster)). Apenas se resultado positivo aplica 40 fire ticks e ANNIHILATION por 60 ticks. | Não inferir dano aceito do lançamento; multiplicador percentual não deve ser cobrado de novo. |
| Filho no impacto | onHit executa raycast vertical de até 3 blocos no local de impacto; se a superfície permite, cria SpellAnnihilationExplosionEntity com raio construtor 4 e warmup 0. Esse filho não é novo cast. | Separar dano de flecha e explosão, ownership e cleanup; QA de claims/anti-magic. |
| Alcance/tipo | Range, gravidade, escala de colisão do projétil principal e dano do filho não foram homologados em gameplay; nenhuma AOE foi criada diretamente pelo método onCast. | NÃO VERIFICADO; fail-closed. |

**Âncoras de código:** [AnnihilationArrowSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/AnnihilationArrowSpell.java#L26-L69) · [AnnihilationArrowEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/AnnihilationArrowEntity.java#L41-L88).

**QA / fail-closed:** Checar bloqueios, solo/água, crítica e sem LOS, aplicação de fogo em dano cancelado, amizade e explosão filha em loaded/unloaded chunk. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
