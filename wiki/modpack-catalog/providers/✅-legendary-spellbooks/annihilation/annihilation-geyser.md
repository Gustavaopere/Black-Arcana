# Annihilation Geyser

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, identidade estática `legendary_spellbooks:annihilation_geyser` / classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationGeyserSpell` — [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Valores/custos descritos da fonte continuam **⚠️ sem validação runtime/Survival**; +0 raízes.

- ID: `legendary_spellbooks:annihilation_geyser`
- School: `legendary_spellbooks:annihilation`
- Level: 1
- Min rarity: Legendary
- Cooldown: 60 s
- Cast: Long, 120 ticks; minimum effective field observado no provider: 60 ticks
- Mana neutral: 500
- Spell power neutral: 30
- Duration reported by spell UI: 50 ticks / 2.5 s
- Radius: 8 blocks
- Crafting: desabilitado
- CastSource: somente Spellbook
- Extra gate: exige `Annihilator's Protocol` equipado em Curios
- Looting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Durante o cast, o provider cria o poço gravitacional/pull; na resolução surge o geyser de Annihilation. A spell possui dois gates próprios: source de spellbook e presença do spellbook exclusivo em Curios.

## Acquisition

`Annihilator's Protocol` é item loot do The Obliterator e vem pré-carregado com Geyser I.

## Regra para o Black Arcana

Fail-closed se o item/gate provider-native não puder ser consultado; nunca permitir casting alternativo por bônus genérico.

## Source

`AnnihilationGeyserSpell.java`, `AnnihilatorsProtocolSpellbookItem.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Evidência:** static registry `legendary_spellbooks:annihilation_geyser` COUNTED_EXACT em JAR 0.3.2; código fonte pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`, **⚠️** integração live com Iron's 3.16.3/Legendary Monsters 2.2.2 não executada.

| Eixo | Mecânica comprovada no source | Status da perk |
|---|---|---|
| Admission | `CastType.LONG`, nível único **1**, cooldown **60s**, mana base **500**, power base **30**, castTime base **120 ticks**. `canBeCastedBy` exige simultaneamente `CastSource.SPELLBOOK` **e** `Annihilator's Protocol` ativo em Curios (`findFirstCurio`); falha em outro source. | `⛔` não contornar Curios/CastSource por perk ou comando wrapper. |
| Tempo mínimo | `getEffectiveCastTime=max(super.getEffectiveCastTime,60)`: limite inferior **60 ticks** mesmo sob reduções do host. `onServerCastTick` observa magicData remaining 30 para som, usa VFX camera shake. | Perks de cast speed devem respeitar mínimo provider, sem alterar o field base por reflection. |
| Pull e alvo | A cada `onServerCastTick`, itera multipliers **0,4,7.5**. `GeometryUtils.getCirclePoints` fornece 5 pontos por anel; para centro 0 o loop interrompe após a primeira verificação: no máximo **11 posições de busca por tick** (1+5+5), com `AABB(blockPosition).inflate(1.5)` e filtro `LivingEntity && !target.isAlliedTo(caster)`. | `SEM_HOOK_SEGURO` para raio/targets; possíveis repetições e custo alto em tick precisam cap/QA, sem Mana cobrança adicional. |
| Movimento de pull | `pullVec=getDirection(target.position(),position)×0.1`; `setDeltaMovement(current.subtract(pullVec))`; marca `hurtMarked`. Sem chamada `hurt` durante esse pull. | `N/A` dano on-pull; não gerar Mastery de hit a cada tick de movimento. |
| Spawn terminal | `onCast` chama `doPortalEffect` para raios **7.5 e 4.0**, cinco pontos cada, somente se `RaycastUtils.findGround` der spawn; depois cria sempre **1 portal central**. **Até 11 tentativas de portal** por cast; `lifeTick=50`, parâmetro de dano = spellPower. | `SEM_HOOK_SEGURO` para portal cap, duração e tamanho de hitbox downstream. |
| Tipo/dano e owner | Entidades `AnnihilationPortalEntity` são de Legendary Monsters; addon marca `ISpellSourceFlag.legendarySpellbooks$markSpell()` e delega a elas o hit/damage. O impacto e DamageType físico não foram verificados aqui. | Não aplicar multiplicador de dano duas vezes nem emitir 11 cast XP a partir dos portais. |
| Progression | UI mostra `duration=50 ticks, radius=8`; raio 8 é metadado de descrição, a geometria real examinada usa anéis 4 e 7.5 e AABBs 1.5. | Não equiparar radius de UI a um único raio de colisão. |

**Âncora:** [AnnihilationGeyserSpell.java e callbacks](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/AnnihilationGeyserSpell.java#L41-L161).

**QA:** gates Curios/scroll/command, mudanças no castTime de Iron's, suporte de servidor ao flag interface, loops por tick, non-allies, claim e blobs de entidades, múltiplos casts, anti-magic, reconnect e lifetime/dano portal no Legendary Monsters 2.2.2. **+0 novas raízes.**
