# Quad Tornado

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:quad_tornado`, classe `dev.higurashi.legendary_spellbooks.common.spells.lightning.QuadTornadoSpell` ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179); [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md)). Valores e mecânicas source-pinned; runtime/Survival ⚠️; +0 raízes.

- ID: `legendary_spellbooks:quad_tornado`
- School: Lightning
- Levels: 1–5
- Min rarity: Epic
- Cooldown: 12 s
- Cast-time field: 40 ticks
- Mana neutral: 120 / 130 / 140 / 150 / 160
- Tornado count: 3 / 4 / 5 / 6 / 7 from `2 + spellLevel`
- Duration: 30 / 40 / 50 / 60 / 70 ticks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria múltiplos tornados móveis/radiais. Apesar do nome `Quad`, o número real varia com o nível e só é quatro no nível 2; o catálogo preserva a fórmula do source em vez de normalizar o nome para uma contagem fixa.

## Acquisition

Pool do Cloud Golem: níveis 1–4, weight 11.

## Regra para o Black Arcana

Não tratar o nome como contrato de quatro entidades. Não duplicar movement/physics ou damage callbacks.

## Source

`QuadTornadoSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast/custo | Níveis 1–5, cooldown 12s, castTime 40, mana 120+10×(nível−1). Não há baseSpellPower definida no corpo específico, então não atribuir valor de damage não observado. | Stats host e Tornado entity. |
| Fanout/geometria | getTornadoCount=2+level → **3/4/5/6/7** Tornado entities; spawn em círculo de **raio 1.5** centrado no caster. A partir do ponto do círculo calcula direção radial e yaw. | Apesar do nome Quad, não são necessariamente quatro tornados. |
| Movimento/tempo | Construtor Tornado recebe direção X/Z×0.1, Y=0.1, duration=min(20+10×level,100)=30/40/50/60/70 ticks, owner caster. Sem dano no onCast. | Não confundir velocidade de origem com dano ou knockback da classe externa; ⛔ multiplicação. |
| Causalidade | Até 7 entidades derivadas do mesmo cast; nenhum DamageType específico desta spell é criado no body auditado. | Atribuir procs apenas a hits reais do runtime, sem autonomia de Black Arcana. |

**Âncoras:** [QuadTornadoSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/QuadTornadoSpell.java#L24-L72).

**QA e fail-closed:** QA lvl1=3 vs nome Quad, trajetória, colisão, sync, claims, pvp, partículas e onHit downstream. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
