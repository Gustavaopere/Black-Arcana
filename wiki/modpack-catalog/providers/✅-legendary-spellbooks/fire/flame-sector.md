# Flame Sector

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:flame_sector` / `dev.higurashi.legendary_spellbooks.common.spells.fire.FlameSectorSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Números/comportamentos source-pinned; execução/Survival ⚠️; +0 magias.

- ID: `legendary_spellbooks:flame_sector`
- School: Fire
- Levels: 1–4
- Min rarity: Epic
- Cooldown: 15 s
- Mana neutral: 80 / 100 / 120 / 140
- Spell power neutral: 3 / 6 / 9 / 12
- Rings: 4 / 6 / 8 / 10
- Approx. flame count from provider formula `floor(1.5 × rings)`: 6 / 9 / 12 / 15
- Flame lifetime: 20 / 25 / 30 / 35 ticks = 1 / 1.25 / 1.5 / 1.75 s
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria setores/anéis de flame entities em torno do caster. Quantidade, duração, posicionamento e damage source permanecem provider-owned.

## Acquisition

Pool do Lava Eater: níveis 1–4, weight 18.

## Regra para o Black Arcana

Não reprocessar cada flame entity como cast separado nem adicionar AoE paralelo.

## Source

`FlameSectorSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** identificação física `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5` (30/30 registros). Corpo de método proveniente de `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` com nível de evidência **SOURCE_CAUSALITY**. Não equivale a QA do pack Iron's 3.16.3/Legendary Monsters 2.2.2 nem a assinatura de adapter RPG homologada.

| Eixo | Comportamento comprovado no source 0.3.2 | Status |
|---|---|---|
| Cast/custo | Estende `BaseOverheadMeleeSwingSpell`; níveis 1–4, cooldown 15s, mana `80+20×(level−1)`, power neutro `3+3×(level−1)`. `onCast` trunca `(int)getSpellPower` antes de distribuir às entidades. | Casting/custo host, sem hook per-caster validado. |
| Geometria/contagem | `ringCount=min(2×level+2,10)` = **4/6/8/10**; `flameCount=floor(1.5×rings)` = **6/9/12/15 por anel**. Total máximo **24/54/96/150** colunas por cast, condicionado a `RaycastUtils.findGround(level,point,5,3)`. Raios: `1.25+i×1.75`; último **6.5/10/13.5/17** blocos por nível. | **SEM_HOOK_SEGURO** para aumentar área/quantidade; alto risco de custo e chunk load. |
| Duração e warmup | `lifeTick=min(15+5×level,60)` = **20/25/30/35 ticks**. Coluna recebe warmup `i×2 ticks`. `SpellFireColumnEntity.tick` usa `warmupTick()` e só aplica dano após fase de aquecimento, com descarte quando `getLifeTicks()<0`. | Não interpretar duration como tempo total incluindo warmup sem medição física. |
| AOE/hitbox | Coluna busca `LivingEntity` em `getBoundingBox().inflate(0.2,1.75,0.2)` no **servidor**; por entidade valida alive, !invulnerable, target != caster, !caster.isAlliedTo(target) e `tickCount%5==0`. AABB não é uma esfera e pode haver hit tentado repetido ao longo da vida. | Sem hook seguro para alterar dimensões/intervalos/cap; QA por i-frames e dedup. |
| Tipo de dano divergente | **Achado no source:** `SpellFireColumnEntity.applyDamage` consulta `LSSpellRegistry.FLAME_EATER_SPELL.get()` e usa `spell.getDamageSource(this,caster)` mesmo quando a coluna foi criada por **Flame Sector**. Isso pode afetar tipo/escola/atribuição/procs, mas **não é bug físico reproduzido** na build 0.3.2. | **⛔** não supor damageSource de Flame Sector, nem corrigir silenciosamente em bridge; testar publisher bytecode e evento de dano. |
| Incêndio/settlement | Após `DamageSources.applyDamage` a entidade chama `target.setRemainingFireTicks(80)` **sem checar retorno**, então alvo pode pegar fogo mesmo se dano negado por outro sistema. | Mastery de dano versus burn deve ter validação própria e não creditar hit não aceito. |

**Âncoras:** [FlameSectorSpell — spawn e geometria](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/fire/FlameSectorSpell.java#L24-L85); [SpellFireColumnEntity — dano/tempo](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellFireColumnEntity.java#L25-L65).

**QA crítico:** confrontar JAR exato e `LSSpellRegistry.FLAME_EATER_SPELL` vs `FLAME_SECTOR_SPELL`, inspecionar damageSource real e finalidade de fogo, PvP, respawn, proteção, 150 colunas e limites; não criar proc novo. **+0 novas magias.**
