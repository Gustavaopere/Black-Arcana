# Hematite Trishula

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:hematite_trishula`, classe `dev.higurashi.legendary_spellbooks.common.spells.blood.HematiteTrishulaSpell`; [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) / [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Parâmetros efetivos e Survival ⚠️, +0 raízes.

- ID: `legendary_spellbooks:hematite_trishula`
- School: Blood
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 30 s
- Cast-time field: 60 ticks
- Mana neutral: 200 / 250 / 300
- Spell power neutral: 20 / 30 / 40
- UI damage field: `spellPower / 2` → 10 / 15 / 20 antes dos multiplicadores aplicáveis
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Carrega e arremessa uma trishula/soul trident própria do addon. A entidade projectile e o pipeline de Blood do provider são autoridade do impacto, efeitos e damage source; a página não converte o campo de UI em uma segunda aplicação de dano.

## Acquisition

Pool do Possessed Paladin: níveis 1–3, weight 10. Crafting não é desabilitado no config da spell.

## Regra para o Black Arcana

Não adicionar segundo projectile hit, Blood proc ou dano calculado a partir do mesmo `spellPower`.

## Source

`HematiteTrishulaSpell.java`, `SpellSoulTridentEntity.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast/custo | Níveis 1–3, cooldown 30s, castTime 60 ticks; mana 200+50×(nível−1), power 20+10×(nível−1). | Host mana, cooldown e school Blood. |
| Projétil/spawn | onCast cria um SpellSoulTridentEntity com owner caster, damage=getSpellPower e posição GeometryUtils.getRelativePos(caster,0,-1.25,0.33). Velocidade/trajectória não inferidas destes argumentos. | SEM_HOOK_SEGURO para velocidade, tamanho, trajectory, fan-out. |
| Impacto/dano | SpellSoulTridentEntity.onHitEntity exclui aliados e tenta DamageSources.applyDamage com HEMATITE_TRISHULA_SPELL.getDamageSource(caster), damage integral, depois descarta; não testa retorno da aplicação para o descarte. | Hit aceito ≠ onHit invocado; não duplicar procs da perk. |
| Expiração/efeito filho | Em tick >=400 no servidor cria SoulPillarExplosionEntity se findGround (5,2) encontrar posição, dano getDamage()/2 e vida construtor 20, e descarta. spawnSpiralStrike também pode criar pilares downstream de chamadas herdadas. | Custo e cap de filhos, dano/area de SoulPillar externo e quem chama spiral ainda NÃO VERIFICADOS. |

**Âncoras de código:** [HematiteTrishulaSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/blood/HematiteTrishulaSpell.java#L26-L72) · [SpellSoulTridentEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellSoulTridentEntity.java#L44-L88).

**QA / fail-closed:** Verificar lifetime 400, hit vs expiração, owner null, SoulPillar multipliers, água/obstáculos, PvP e beam-like procs. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
