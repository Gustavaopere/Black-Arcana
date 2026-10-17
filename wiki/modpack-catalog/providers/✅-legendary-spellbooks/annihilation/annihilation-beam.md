# Annihilation Beam

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, identidade estática `legendary_spellbooks:annihilation_beam` / classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationBeamSpell` — [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Valores/custos descritos da fonte continuam **⚠️ sem validação runtime/Survival**; +0 raízes.

- ID: `legendary_spellbooks:annihilation_beam`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–3
- Min rarity: Epic
- Cooldown: 45 s
- Cast: Long, 40 ticks; cast-time reduction desabilitada pelo provider
- Mana neutral: 200 / 250 / 300
- Spell power neutral: 8 / 14 / 20
- Max-HP damage: 1% / 2% / 3%
- Beam duration: 80 / 60 / 40 ticks
- Length: 30 / 40 / 50 blocks
- Crafting: desabilitado
- CastSource: somente Spellbook ou Command; scroll falha explicitamente
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria `SpellAnnihilationBeamEntity`, aplica o efeito Beam ao caster durante a duração e combina spell power com dano percentual de vida máxima. O guia do provider registra que o caster fica travado durante o disparo.

## Acquisition

Pool do The Obliterator: níveis 1–3, weight 10. `Annihilator's Protocol` também vem pré-carregado com Beam III.

## Regra para o Black Arcana

Não contornar o gate de CastSource, não aplicar segundo beam tick e não duplicar HP damage.

## Source

`AnnihilationBeamSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Evidência:** identidade física 0.3.2 `legendary_spellbooks:annihilation_beam` exata; corpos source pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` **SOURCE_CAUSALITY**, helpers Iron's 3.16.3 e Legendary Monsters 2.2.2 ainda condicionados.

| Eixo | Cadeia e parâmetros no source | Hook / risco |
|---|---|---|
| Gate/cast | `canBeCastedBy` permite apenas `CastSource.SPELLBOOK` e `COMMAND`, falha nos demais (inclui SCROLL). `castTime=40 ticks`, `baseManaCost=200`, `manaCostPerLevel=50`, cooldown 45 s. Dano neutro de power `8+6×(level−1)`. | `⛔` não contornar gate por perks, nem duplicar debits da Iron's. |
| Origem/range | `onCast` cria entidade em **eyePosition + forward×1.5 blocos**. `getLength=20+10×level` → 30/40/50 blocos. `calculateBeamPos` faz raycast `COLLIDER` de blocos até essa distância; o endpoint é ajustado à colisão. | `SEM_HOOK_SEGURO` para range/retarget/mudar raycast; setter `setMaxRange` em entidade não é contrato de perk aceito. |
| Tempo de efeito | `duration=max(100−20×level,40)` → **80/60/40 ticks**; aplica `BEAM_EFFECT` no caster por esse tempo e cria beam com warmup **1 tick**. Tick server decrementa `lifeTick` e descarta ao chegar 0. | `SEM_HOOK_SEGURO` para duration per-cast, sem QA da ordem warmup/timer. |
| Target/colisão | No servidor, varre `AABB(start,end).inflate(1.0)`, filtra caster, mortos, aliados em ambas direções, invulneráveis. Cada alvo requer interseção de segmento com `target.getBoundingBox().inflate(0.5)` ou conter o início. **AABB broadphase não é a hitbox física final**. | Geometry não é esfera/AOE de raio 1; sem hook de largura de colisão ou target cap. |
| Dano/status | Por tick elegível tenta `spell.getDamageSource(beam,caster)` via `DamageSources.applyDamage` com `getSpellPower(level,caster)+target.maxHealth×(0.01×level)`. **Somente se applyDamage retorna true** aplica `ANNIHILATION` 60 ticks e 40 fire ticks. | Dano composto; não escalar novamente o percentual de HP por proc de RPG. Mastery considera settle e idempotência por cast/tick/vítima. |
| Entidades derivadas | Ao concluir warmup, `spawnExplosions` roda **apenas se abs(direction.y)<0.25**, em pontos do raio para baixo com raycast vertical 3 blocos; gera `SpellAnnihilationExplosionEntity` com parent beam, lifetime ≈ metade. Não contar essas explosões como casts independentes; dano downstream separado exige auditoria. | `SEM_HOOK_SEGURO` para multiplicar explosões, AoE ou lifetime sem confirmar policies e custo. |
| Segurança e autoridade | `onAntiMagic` encaminha limpeza às explosões filhas. Classe do beam é provider-owned e deve preservar clean-up, claims e owner. | Não aplicar `WorldEffectPolicy` própria sobre chamadas externas sem contrato, nem reforçar efeito via segunda entidade. |

**Fonte fixa:** [Spell base e gates](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/AnnihilationBeamSpell.java#L28-L89); [Beam raycast e target/hit](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellAnnihilationBeamEntity.java#L60-L159); [spawn de explosões e anti-magic](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellAnnihilationBeamEntity.java#L176-L240).

**QA:** composição do dano contra HP máximo e shields, i-frames, blocos parciais, vertical pitch, friendly fire, 40/60/80 ticks, filhos e anti-magic, caster logout, client/server, desempenho em múltiplos alvos e provider delta. Valores são source, **não** gameplay aprovado; **+0 IDs**.
