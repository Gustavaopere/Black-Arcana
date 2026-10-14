# Ars Nouveau 5.13.1 — mapa técnico para Codex e perks

Status: ✅ `SOURCE-LOCATED DOSSIERS FOR 85/85 GLYPH PARTS + 24/24 RITUALS` / ⚠️ execução física/adapter RPG ainda não validada · **85/85 partes de spell com auditoria de perks e localizador** · **24/24 rituais** · hooks externos e gameplay físico ⚠️/⛔ conforme linha.

## Identidade física e limite

- Modlist física atual do sibling `neoforge-rpg-skilltree/main`: `ars_nouveau-1.21.1-5.13.1.jar`, `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` (dossiê físico de 22/09/2026).
- Code pin: [`baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`](https://github.com/baileyholl/Ars-Nouveau/tree/112920ff774831f204031da75b4c4e73d3765157); fonte de evidência factual read-only; não implica hash binário provado neste PR.
- Inventário: 5 Forms + 67 Effects + 13 Augments = 85 Glyph Parts; 24 rituais separados. **A cadeia completa é composição do player**, não 85 magias predefinidas.
- Autoridade: Ars controla SpellResolver/SpellContext/SpellStats, casting, mana, Source, itens, efeitos e world mutations; RPG Skill Tree pode oferecer progressão/perks/gates por seam real; Black Arcana responde apenas por seu próprio casting, hazards e WorldEffectPolicy.

## Contratos de geometria e duração realmente lidos

- `SpellUtil.calcAOEBlocks` recebe `SpellStats`, calcula `aoeBonus=getAoeMultiplier()`, `pierceBonus=count(Pierce)` e no overload double define `width=(int)(1+floor(aoeBonus))`, `height=(int)(1+ceil(aoeBonus))`, `depth=1+pierceBonus`. A grade é orientada pela direção da face atingida; coordenadas e filtros pertencem ao helper; não tratar AOE como raio em blocos.
- `IPotionEffect.applyPotion` aplica `ticks=baseDurationSeconds*20+durationBuffSeconds*getDurationInTicks()`; `SpellStats.getDurationInTicks=(int)(20*durationMultiplier)`, amplifier `(int)getAmpMultiplier()`. Formula específica em fichas Harm/Wither/Snare; outras durações podem usar lógicas diferentes.
- `ANExplosion.explode` resolve dano por distância, exposição e teto `baseDamage+amps*ampDamageScalar`; intensidade inicial, seleção de blocos e evento de veto são outros eixos.
- `LightningEntity` considera água/chuva, amplificação, capacidade de energia por slot e AABB de colisão; `SHOCKED_EFFECT` é evento subsequente, não outro cast.
- `RuneTile` persiste outra forma de execução: runa temporária é removida após disparo; runa permanente usa Source para recarga; não criar dupla cobrança em black Arcana.

## Fichas aprofundadas neste checkpoint

| Tipo | Páginas com mapa | Dados que Codex já pode ler | Mutabilidade externa |
|---|---|---|---|
| Form 5/5 | [Projectile](glyphs/forms/projectile.md), [Self](glyphs/forms/self.md), [Touch](glyphs/forms/touch.md), [Underfoot](glyphs/forms/underfoot.md), [Pantomime](glyphs/forms/pantomime.md) | spawn, targeting, sobrecargas por contexto, status SUCCESS/FAILURE/RUNE | ⛔ sem hook provado |
| Effect 67/67 — ofensivos | [Harm](glyphs/effects/harm.md), [Explosion](glyphs/effects/explosion.md), [Lightning](glyphs/effects/lightning.md), [Ignite](glyphs/effects/ignite.md), [Wither](glyphs/effects/wither.md) | dano/duration branches, formula downstream, wet bonus, efeito por tick | ⛔ sem hook provado |
| Effect 67/67 — world | [Break](glyphs/effects/break.md), [Freeze](glyphs/effects/freeze.md), [Grow](glyphs/effects/grow.md), [Place Block](glyphs/effects/place-block.md) | AOE/depth e claim/event gates, item/loot, world mutation | ⛔ sem hook provado |
| Effect 67/67 — controle/utilidade | [Blink](glyphs/effects/blink.md), [Snare](glyphs/effects/snare.md), [Summon Wolves](glyphs/effects/summon-wolves.md), [Rune](glyphs/effects/rune.md), [Heal](glyphs/effects/heal.md) | teleporte, debuffs, summons, delayed casts, healing/dano invertido | ⛔ sem hook provado |
| Effect 67/67 — transformação e summons | [Burst](glyphs/effects/burst.md), [Cut](glyphs/effects/cut.md), [Intangible](glyphs/effects/intangible.md), [Summon Undead](glyphs/effects/summon-undead.md), [Wololo](glyphs/effects/wololo.md) | child-context em esfera, shearing/strip, restauração temporária, summon owners, dye/items | ⚠️ helpers/WorldEffectPolicy e adapters RPG pendentes |
| Effect 67/67 — condições e consumíveis | [Access Ender Inventory](glyphs/effects/access-ender-inventory.md), [Animate Block](glyphs/effects/animate-block.md), [Bubble](glyphs/effects/bubble.md), [Cold Snap](glyphs/effects/cold-snap.md), [Conjure Water](glyphs/effects/conjure-water.md), [Crush](glyphs/effects/crush.md), [Firework](glyphs/effects/firework.md), [Flare](glyphs/effects/flare.md), [Hex](glyphs/effects/hex.md), [Infuse](glyphs/effects/infuse.md), [Knockback](glyphs/effects/knockback.md), [Sense Magic](glyphs/effects/sense-magic.md) | menu Ender, block-summon, Bubble pop, Cold Snap, recipes, Soaked, firework, Cinders, Hex, potions, knockback e Magic Find | ⚠️ efeito por executor, config e runtime; adapter RPG ⛔ |
| Effect 67/67 — utility | [Bounce](glyphs/effects/bounce.md), [Conjure Mageblock](glyphs/effects/conjure-mageblock.md), [Conjure Magelight](glyphs/effects/conjure-magelight.md), [Craft](glyphs/effects/craft.md), [Evaporate](glyphs/effects/evaporate.md), [Fell](glyphs/effects/fell.md), [Glide](glyphs/effects/glide.md) | status timed, world place, menu, fluid/neighbors, DFS bounded e perk Ars interna | ⚠️ calls/side effects source-pinned, adapter RPG ⛔ |
| Effect 67/67 — access | [Harvest](glyphs/effects/harvest.md), [Interact](glyphs/effects/interact.md), [Invisibility](glyphs/effects/invisibility.md), [Item Pickup](glyphs/effects/item-pickup.md), [Launch](glyphs/effects/launch.md), [Leap](glyphs/effects/leap.md) | loot/crop, fake-player, pickup events, launch e ground gate | ⚠️ calls/side effects source-pinned, adapter RPG ⛔ |
| Effect 67/67 — worldctx | [Name](glyphs/effects/name.md), [Prestidigitation](glyphs/effects/prestidigitation.md), [Pull](glyphs/effects/pull.md), [Redstone Signal](glyphs/effects/redstone-signal.md), [Reset](glyphs/effects/reset.md), [Rotate](glyphs/effects/rotate.md) | contextos Reset, RedstoneSavedData, partículas, direção e world mutations | ⚠️ calls/side effects source-pinned, adapter RPG ⛔ |
| Effect 67/67 — entities | [Slowfall](glyphs/effects/slowfall.md), [Summon Decoy](glyphs/effects/summon-decoy.md), [Summon Steed](glyphs/effects/summon-steed.md), [Summon Vex](glyphs/effects/summon-vex.md), [Toss](glyphs/effects/toss.md), [Wind Burst](glyphs/effects/wind-burst.md), [Wind Shear](glyphs/effects/wind-shear.md) | summon/owner/sickness, manipulação de stacks, blast e altitude | ⚠️ calls/side effects source-pinned, adapter RPG ⛔ |
| Augment 13/13 — primeiros 4 | [Amplify](glyphs/augments/amplify.md), [AOE](glyphs/augments/aoe.md), [Split](glyphs/augments/split.md), [Pierce](glyphs/augments/pierce.md) | estatísticas transformadas versus contagem de augments, consumidores distintos | ⛔ sem hook provado |
| Effect 67/67 — temporal e dispel | [Rewind](glyphs/effects/rewind.md), [Exchange](glyphs/effects/exchange.md), [Delay](glyphs/effects/delay.md), [Dispel](glyphs/effects/dispel.md), [Gravity](glyphs/effects/gravity.md) | event queue, time/teleport, DispelEvent, falling blocks e source policy | ⚠️ evento público observado; adapter ⛔ |
| Effect 67/67 — campos e processamento | [Wall](glyphs/effects/wall.md), [Linger](glyphs/effects/linger.md), [Orbit](glyphs/effects/orbit.md), [Smelt](glyphs/effects/smelt.md), [Fangs](glyphs/effects/fangs.md) | child-context, entities, counters, receitas e spawn condicionado | ⚠️ API genérica de effect; comportamento auxiliar condicionado |
| Augment 9 restantes | [Accelerate](glyphs/augments/accelerate.md), [Decelerate](glyphs/augments/decelerate.md), [Dampen](glyphs/augments/dampen.md), [Extend Time](glyphs/augments/extend-time.md), [Reduce Time](glyphs/augments/reduce-time.md), [Extract](glyphs/augments/extract.md), [Fortune](glyphs/augments/fortune.md), [Randomize](glyphs/augments/randomize.md), [Sensitive](glyphs/augments/sensitive.md) | operadores, efeitos dependentes da contagem, config/caps e regras de alvo | ⚠️ alguns setters reais via evento EffectResolve, adapter ⛔ |
| Ritual 24/24 | [Flight](rituals/flight.md), [Binding](rituals/binding.md), [Disintegration](rituals/disintegration.md), [Scrying](rituals/scrying.md), [Warping](rituals/warping.md), [Sanctuary](rituals/sanctuary.md), [Moonfall](rituals/moonfall.md), [Gravity](rituals/gravity.md), [Harvest](rituals/harvest.md), [Burrowing](rituals/burrowing.md), [Restoration](rituals/restoration.md), [awakening](rituals/awakening.md), [challenge](rituals/challenge.md), [containment](rituals/containment.md), [fertility](rituals/fertility.md), [flowering](rituals/flowering.md), [forestation](rituals/forestation.md), [cloudshaping](rituals/cloudshaping.md), [conjure-island-desert](rituals/conjure-island-desert.md), [conjure-island-plains](rituals/conjure-island-plains.md), [overgrowth](rituals/overgrowth.md), [summon-animals](rituals/summon-animals.md), [summon-wilden](rituals/summon-wilden.md), [sunrise](rituals/sunrise.md) | range, ticks, Source cost, refresh/jump/packet | ⛔ sem hook provado |

**As onze linhas Effect distribuem 67 fichas (5+4+5+5+5+5+12+7+6+6+7); Augments somam 4+9=13.** A contagem é de dossiês source-pinned, não de novas identidades semânticas.


## Análises adicionais de rituais e mundo

- **Binding:** conversão de FamiliarRegistry → Bound Script/item provider-owned, sem death proc.
- **Disintegration:** remoção sem kill comum; discrepância do Source quando não há XP positiva permanece aberta.
- **Scrying:** persistência `an_scryer`, efeito 6000/18000 ticks; efeito de descoberta pertence a Ars.
- **Warping:** scroll válido e aplicação `teleportTo(x,y,z)`; passagem entre dimensões não comprovada apenas pela admissão.
- **Sanctuary:** veto event-driven de NATURAL spawns, persistência do raio e Source periódico.
- **Moonfall:** progresso avança tanto a cada 20 ticks quanto em ticks extras quando o threshold de noite foi atingido; não declarar timer linear.
- **Gravity:** range 60, duration 1200 e Source 200; consumo/refresh de RangeEffectRitual.
- **Harvest:** grade de 9×3×9 com processamento a cada 200 ticks e ledger de Source agrupado.
- **Burrowing:** quatro blocos por camada com checagens de hardness/claims e fake player.
- **Restoration:** cura 10, ataque fake-player 10 a undead/inverted, conversão Zombie Villager, Source pendente.

## Alertas de source — lote 59/85

- **Crush:** método de transformação de blocos não traz `destroyRespectsClaim` local, mas a admissão completa não foi validada; não declarar exploit.
- **Conjure Water:** `POTION_TIME` configura 20 segundos, mas o getter sem config usa fallback de 30; `Sense Magic` configura 60/15 segundos, getters sem config retornam 30/8. Apenas config carregada determina valores efetivos.
- **Cold Snap:** Snare só é aplicada quando `attemptDamage` retorna sucesso, enquanto o caminho de shards segue após admissão do alvo e independentemente desse retorno. Máster/procs precisam separar branches.
- **Containment:** jarros em cubo ±3, entidades em AABB inflate(5) de cada jarro, divergindo da descrição generalizada.
- **Awakening:** DFS limitada a 350 por árvore candidata e conversão de entidades não é uma série de casts independente.
- **Rituais 24/24:** mapeamento de entrada/source, laços, estados e bloqueios existe para cada ficha; **não** significa que efeitos auxiliares/JAR físico, plugins de proteção ou provider-native QA estejam aprovados.

## Alertas adicionais do fechamento source-located 109/109

- **Wind Shear:** o loop `numBlocks <= 10` pode incrementar até 11 posições, diferente da descrição; config `airDamage=0.75` é declarada, mas não usada no cálculo local de dano.
- **Toss:** `64*pow(2,amp)` não apresenta clamp no método local; qualquer alteração de AMP depende de caps verificados em admissões/recipes/pack.
- **Rotate:** `rotateVec` fornece graus aos métodos trigonométricos de Java sem converter explicitamente para radianos. Potencial erro source-level, não confirmado em execução.
- **Glide e Magelight:** `GlidingPerk` do Ars não é a API do RPG Skill Tree; block/mob branches são distintos.
- **Interact e Item Pickup:** FakePlayer/inventário e eventos reais de NeoForge podem disparar efeitos/retornos variados; Post não prova quantidade efetivamente coletada.
- **Prestidigitation e Reset:** apresentação VFX e `IContextManipulator` não devem gerar Mastery genérica por clone, target secundário ou tick.
- **Claims:** múltiplas classes (Crush, Evaporate, Harvest, Rotate, Redstone Sensitive, Prestidigitation e outros) não mostram `destroyRespectsClaim` **no método local**. Não inferir ausência de proteção geral; auditar completo pipeline e ensaios pack.
- **Critério de continuidade:** as 109 fichas core Ars têm classe pinada/causalidade descrita; **nenhum adapter RPG** ou compatibilidade global está testado/implementado. Agora aprofundar outros providers e regressões físicas.

## Riscos e bloqueios concretos para futuras perks

1. **Amplificação não é sempre dano.** Pode significar Poison, harvest strength, intensidade, alcance etc. Só aplicar por consumidor e limites da receita.
2. **Área e penetração não são universais.** Em `SpellUtil` AOE/Pierce geram largura/altura/profundidade. Em `Freeze` um candidato ainda tenta seis vizinhos. World-cap e claims permanecem QA.
3. **Executor downstream manda.** `EffectLightning` configura `LightningEntity`, `EffectExplosion` configura `ANExplosion`, `Rune` configura `RuneTile`. Hooks sobre a classe de glyph podem perder dano/procs/cooldowns reais.
4. **Possível desvio de restauração de dano no lightning — exige QA.** No source `LightningEntity.tick()`, após `setDamage(adjusted)`, um evento cancelado faz `continue` antes de restaurar `origDamage`. Isso é achado estático, não incidente de runtime comprovado; nenhum patch upstream/Black Arcana foi realizado.
5. **Recursos não se duplicam.** Runas persistentes recarregam Source; próprias magias usam player mana Ars. Sem prova de boundary, é proibido criar um segundo ledger, cast ou Mastery por every-hit.
6. **Eventos públicos existem, mas não são perks implementadas.** `EffectResolveEvent.Pre` permite examinar `SpellStats` antes do efeito; há setters concretos (amp, speed, damageModifier, duration) e eventos de custo separados. `setAoeMultiplier` não existe na instância construída; efeitos que leem `getBuffCount` podem ignorar multiplicadores. Ver [contratos exatos de eventos](VERIFIED-EVENT-SURFACES-5.13.1.md) e testar causalidade, clamps e paridade de custos. ⛔ nenhum adapter RPG aprovado.

## Próximas verificações

- Nenhuma ficha base de Ars core pendente: **0 Forms, 0 Effects, 0 Augments e 0 rituais**. Isto mede localização de source/engenharia documental, não integridade de todos os contratos de integração/testes, sempre ficha a ficha.
- `SpellCastEvent`, `SpellResolveEvent`, `EffectResolveEvent`, `SpellCostCalcEvent` e `DispelEvent` já foram source-pinados; agora falta adapter RPG com testes de sucesso/veto/exactly-once, custo Pre/Post e conflitos com addons.
- Limites reais em `SpellResolver`, `SpellStats.Builder`, `SpellUtil`, claims, `RuneTile` e efeitos persistentes; validar config efetivamente carregada.
- Ensaios em NeoForge 1.21.1/Ars 5.13.1 e modpack/Survival. **Nenhum realizado neste PR**.

[Norma universal](../../meta/PERK-READY-TECHNICAL-STANDARD.md) · [Ledger global](../../meta/PERK-READY-COVERAGE-LEDGER.md) · [PR #795 Iron's](https://github.com/Gustavaopere/Black-Arcana/pull/795).
