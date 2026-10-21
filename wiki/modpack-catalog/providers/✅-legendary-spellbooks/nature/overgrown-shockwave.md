# Overgrown Shockwave

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:overgrown_shockwave`, classe `dev.higurashi.legendary_spellbooks.common.spells.nature.OvergrownShockwaveSpell` ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179); [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md)). Valores e mecânicas source-pinned; runtime/Survival ⚠️; +0 raízes.

- ID: `legendary_spellbooks:overgrown_shockwave`
- School: Nature
- Levels: 1–4
- Min rarity: Epic
- Cooldown: 30 s
- Mana neutral: 150 / 165 / 180 / 195
- Spell power neutral: 4 / 8 / 12 / 16
- Provider recasts: 1 / 2 / 3 / 4
- Recast window: 80 ticks
- Shockwave count: 3 / 4 / 5 / 6
- Outer radius reported by provider formula: 5.75 / 7.25 / 8.75 / 10.25 blocks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

A primeira ativação abre um recast window com count igual ao spell level; cada resolução gera as ondas/poisonous shockwaves provider-native. O count usa `min(spellLevel + 2,10)` e a geometria deriva dele.

## Acquisition

Pool do Overgrown Colossus: níveis 1–4, weight 10.

## Regra para o Black Arcana

Não transformar recasts em novos casts independentes para cooldown, mastery ou proc. Não duplicar as shockwaves já criadas pelo provider.

## Source

`OvergrownShockwaveSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast/recast | Níveis 1–4, cooldown 30s, mana 150+15×(nível−1), power 4+4×(nível−1) int ao criar entidade. getRecastCount(level)=level; onCast só cria RecastInstance(80 ticks) quando fora de cooldown e sem recast existente, mas ainda segue para gerar ondas. | Recast count é provider-owned; não premiar cada tentativa como cast sem contrato. |
| Geometria/fanout | getShockwaveCount=min(level+2,10)=3/4/5/6; cada anel i raio=1.25+1.5×i e `poisonCount=shockwaveCount×4` pontos por **cada** anel. Máximo teórico = rings×(rings×4)=**36/64/100/144** entidades, se findGround(level,point,4,6) sempre der posição. | Importante: if spawnPos==null usa **return** em onCast, não continue; encerra imediatamente o restante do cast e não chega ao super.onCast neste ramo. Mutação por perk ⛔. |
| Damage/status/hitbox | SpellPoisonousShockwaveEntity usa AABB inflate(.2,0,.2), tentativa de dano a cada 5 ticks (source spell.getDamageSource), aplica POISON por **80 ticks amplifier 2** sem testar retorno de applyDamage; lifeTicks construtor 15, warmup i×2. | Dano e Poison precisam ser registrados separadamente; tentar procs on-hit quando damage negado é inseguro. |
| Target/range | Centro caster.position, sem raycast de entity no cast; UI radius=1.25+shockwaveCount×1.5, enquanto último raio realmente spawnado é 1.25+(shockwaveCount−1)×1.5: divergência **1.5 bloco**. | Não confundir UI radius com alcance de splash nem modificar sem validacao. |

**Âncoras:** [OvergrownShockwaveSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/nature/OvergrownShockwaveSpell.java#L27-L85) · [SpellPoisonousShockwaveEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellPoisonousShockwaveEntity.java#L45-L90).

**QA e fail-closed:** QA null ground early return, recast settlement, 144 entidades em level4, POISON com dano cancelado, PvP, chunks unload, UI radius e claims. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
