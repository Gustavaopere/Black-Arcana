# Annihilation Bomb

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, identidade estática `legendary_spellbooks:annihilation_bomb` / classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationBombSpell` — [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Valores/custos descritos da fonte continuam **⚠️ sem validação runtime/Survival**; +0 raízes.

- ID: `legendary_spellbooks:annihilation_bomb`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 20 s
- Cast: Long, 27 ticks; cast-time reduction desabilitada
- Mana neutral: 125 / 140 / 155 / 170 / 185 / 200
- Spell power neutral: 6 / 10 / 14 / 18 / 22 / 26
- Max-HP damage: 0.5% / 1% / 1.5% / 2% / 2.5% / 3%
- Secondary projectile count: 30 / 35 / 40 / 45 / 50 / 55
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Lança uma `SpellAnnihilationBombEntity`; no impacto, o provider resolve a detonação e a dispersão dos orbs secundários. A spell já carrega dano mágico e componente percentual de HP.

## Acquisition

Pool do The Obliterator: níveis 1–4, weight 14.

## Regra para o Black Arcana

Não adicionar segunda explosão, segunda dispersão ou dano percentual paralelo.

## Source

`AnnihilationBombSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast / stats | Níveis 1–6; cooldown 20 s; castTime=27; mana base 125 +15/nível; spell power 6+4×(nível−1) antes de buffs. | Iron's controla mana e cast. Nenhum adapter homologado. |
| Spawn / quantidades | Um SpellAnnihilationBombEntity começa no olho+look×1; parâmetros base dano e 0.005×level de vida máxima; bulletAmount=25+5×level (30,35,40,45,50,55). | Não multiplicar um root por número de projéteis. |
| AOE inicial | No onHit server-only aplica dano na AABB da bomba inflate(2), exclui caster e aliados em ambas as direções, usa spell.getDamageSource(bomb,caster), status ANNIHILATION 60 e fire 40 **somente se applyDamage retornar true**. | Tamanho AABB não é esfera exata; perk de radius sem hook ⛔. |
| Fragmentação | Depois do impacto chama shootBullet com velocidades 0.4 e 0.6. Cada chamada itera i < bulletAmount/2 com divisão inteira: total 2×floor(bulletAmount/2) = **30/34/40/44/50/54** tiros tentados em níveis 1–6, não 30/35/.../55 para níveis pares. Cada filho recebe metade do dano base, mesma proporção de HP e dispersão vertical randômica. | Causalidade uma bomba→fragmentos; attributions/on-hit/Mastery dedup; falta limite de projéteis físico. |
| Lifetime / alvo | Dano e duração de SpellSmallAnnihilationBombEntity downstream ainda não homologados com runtime pack, assim como collision shape e alcance. | ⛔ alteração de velocidade/contagem/vida por perks sem seam. |

**Âncoras de código:** [AnnihilationBombSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/AnnihilationBombSpell.java#L29-L89) · [SpellAnnihilationBombEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellAnnihilationBombEntity.java#L44-L81).

**QA / fail-closed:** Conferir quantidade exata em níveis pares, aplicação AOE no impacto e filhos, 50+ entidades por cast, owner logout, anti-magic, PvP/claims, plugin de cancelamento. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
