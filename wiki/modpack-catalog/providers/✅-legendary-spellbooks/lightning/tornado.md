# Tornado

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:tornado` / `dev.higurashi.legendary_spellbooks.common.spells.lightning.TornadoSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Dados numéricos source-pinned; execução/Survival ⚠️; +0.

- ID: `legendary_spellbooks:tornado`
- School: Lightning
- Levels: 1–10
- Min rarity: Common
- Cooldown: 6 s
- Cast-time field: 25 ticks
- Mana neutral: 60 / 65 / 70 / 75 / 80 / 85 / 90 / 95 / 100 / 105
- Duration: 15 / 20 / 25 / 30 / 35 / 40 / 45 / 50 / 55 / 60 ticks
- Target helper range: 12 blocks; provider fallback raycast: 42 blocks
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Spawna um tornado estacionário provider-native no alvo/posição resolvida. A duração usa `min(10 + 5 × spellLevel,100)`. O addon também possui `TornadoEntityHandler`; motion/damage/lifecycle permanecem autoridade do provider.

## Acquisition

Pool do Cloud Golem: níveis 3–10, weight 6. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não somar outro vortex/impulse ao mesmo tornado nem duplicar sua duração.

## Source

`TornadoSpell.java`, `TornadoEntityHandler.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast / targeting | Níveis 1–10, cooldown 6s, castTime=25, mana 60+5×(nível−1). checkPreCastConditions chama preCastTargetHelper com **12** e retorna true mesmo sem alvo; fallback onCast usa RaycastBuilder **range 42** checkForBlocks. | São dois parâmetros distintos: não anunciar alcance único 42/12 sem entender branch. ⛔ re-target. |
| Destino/spawn | Se TargetEntityCastData resolvida no ServerLevel, usa target.position. Senão raycast 42: entidade → posição; bloco → findGround(hitLocation−forward+Y2,20,10); MISS → não cria tornado, mesmo assim super.onCast é chamado. | O cast pode progredir sem entidade, portanto sucesso de cast ≠ tornado efetivo. |
| Duração/physics | Se spawn definido, cria um Tornado (Legendary Monsters) com velocity (0,0.1,0), caster e duration=min(10+5×level,100)=15..60 ticks. Body não chama hurt. | Dano/drag/target cap/knockback pertencem ao provider externo; perks de duração/tamanho ⛔. |

**Âncoras:** [TornadoSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/TornadoSpell.java#L30-L84).

**QA e fail-closed:** QA alvo helper12 vs fallback42, cast em MISS, block behind wall, entidades PvP, lifetime externo, anti-magic e owner. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
