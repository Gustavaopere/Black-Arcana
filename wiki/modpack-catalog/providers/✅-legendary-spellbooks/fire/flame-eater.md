# Flame Eater

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:flame_eater` / `dev.higurashi.legendary_spellbooks.common.spells.fire.FlameEaterSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Números/comportamentos source-pinned; execução/Survival ⚠️; +0 magias.

- ID: `legendary_spellbooks:flame_eater`
- School: Fire
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 10 s
- Mana neutral: 100 / 120 / 140 / 160 / 180 / 200
- Spell power neutral: 10 / 13 / 16 / 19 / 22 / 25
- Target/recast capacity: `1 + spellLevel` → 2 / 3 / 4 / 5 / 6 / 7
- Target range: 32 blocks
- Fire-column lifetime: 30 / 40 / 50 / 60 / 70 / 80 ticks = 1.5 / 2 / 2.5 / 3 / 3.5 / 4 s
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

O provider usa recasts para acumular alvos e resolve colunas de fogo sobre os UUIDs armazenados. O target ledger, recast count e as fire columns são parte da própria spell.

## Acquisition

Pool do Lava Eater: níveis 3–6, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não criar segundo target ledger, não disparar coluna adicional ao mesmo recast e não recontar um target provider-native como novo cast.

## Source

`FlameEaterSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro de 30/30 spells COUNTED_EXACT ([auditoria Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas abaixo **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; equivalência integral do bytecode e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não testadas**. Nenhum adapter RPG aprovado.

| Eixo | Evidência fonte | Boundary da perk |
|---|---|---|
| Cast/gates | School FIRE, níveis 1–6, cooldown 10s, mana 100+20×(nível−1), power 10+3×(nível−1). checkPreCastConditions delega Utils.preCastTargetHelper(..., range=32, radius/tolerance=0.15f). | O helper de alvo do Iron's é contrato upstream; ⛔ retarget/range sem validar helper físico. |
| Recast e aquisição de vítimas | getRecastCount(level)=1+level; onCast se TargetEntityCastData inicia RecastInstance de 40 ticks com MultiTargetEntityCastData, ou adiciona targetUUID à lista existente. O corpo não garante que número de targets distintos seja sempre max recasts. | Mastery deve distinguir recast sequencial, cast raiz e alvo, sem duplicar custos ou skills. |
| Settlement na finalização | onRecastFinished (ServerPlayer) lê UUIDs, obtém Entity no ServerLevel, busca solo com RaycastUtils.findGround(...,6,2) e cria uma SpellFireColumnEntity por alvo válido; se uma busca de solo falha retorna do método, afetando restantes. lifeTick=min(20+10×level,400) =30–80 ticks. | Criar coluna só após recast finished, não na mera ativação. Mundo/claims/limites condicionados. |
| Dano/tipo/área | SpellFireColumnEntity consulta LSSpellRegistry.FLAME_EATER_SPELL.getDamageSource(column,caster), atinge getBoundingBox.inflate(.2,1.75,.2) a cada 5 ticks, e define fire ticks 80 sem verificar retorno de applyDamage. | Hook de DamageType/espessura/cooldown sem homologação; cuidado com DoT e atribuição de procs. |

**Âncoras de código:** [FlameEaterSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/fire/FlameEaterSpell.java#L33-L120) · [SpellFireColumnEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellFireColumnEntity.java#L39-L65).

**QA / fail-closed:** Recast de targets N distintos, cancelamento e distâncias, vítima invisível/descarregada, primeiro ground null, token de Mastery, n colunas e dano efetivo. Não criar segundo cast/cooldown/mana, não conceder Mastery sem settlement server-authoritative e dedup do cast pai. **+0 novos spells.**
