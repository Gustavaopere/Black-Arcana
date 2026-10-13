# Ars Nouveau 5.13.1 — mapa técnico para Codex e perks

Status: 🟡 `SOURCE CAUSALITY IN PROGRESS` · **42/85 partes de spell com auditoria de perks e localizador** · **6/24 rituais** · hooks externos e gameplay físico ⚠️/⛔ conforme linha.

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
| Effect 24/67 — ofensivos | [Harm](glyphs/effects/harm.md), [Explosion](glyphs/effects/explosion.md), [Lightning](glyphs/effects/lightning.md), [Ignite](glyphs/effects/ignite.md), [Wither](glyphs/effects/wither.md) | dano/duration branches, formula downstream, wet bonus, efeito por tick | ⛔ sem hook provado |
| Effect 24/67 — world | [Break](glyphs/effects/break.md), [Freeze](glyphs/effects/freeze.md), [Grow](glyphs/effects/grow.md), [Place Block](glyphs/effects/place-block.md) | AOE/depth e claim/event gates, item/loot, world mutation | ⛔ sem hook provado |
| Effect 24/67 — controle/utilidade | [Blink](glyphs/effects/blink.md), [Snare](glyphs/effects/snare.md), [Summon Wolves](glyphs/effects/summon-wolves.md), [Rune](glyphs/effects/rune.md), [Heal](glyphs/effects/heal.md) | teleporte, debuffs, summons, delayed casts, healing/dano invertido | ⛔ sem hook provado |
| Augment 13/13 — primeiros 4 | [Amplify](glyphs/augments/amplify.md), [AOE](glyphs/augments/aoe.md), [Split](glyphs/augments/split.md), [Pierce](glyphs/augments/pierce.md) | estatísticas transformadas versus contagem de augments, consumidores distintos | ⛔ sem hook provado |
| Effect 24/67 — temporal e dispel | [Rewind](glyphs/effects/rewind.md), [Exchange](glyphs/effects/exchange.md), [Delay](glyphs/effects/delay.md), [Dispel](glyphs/effects/dispel.md), [Gravity](glyphs/effects/gravity.md) | event queue, time/teleport, DispelEvent, falling blocks e source policy | ⚠️ evento público observado; adapter ⛔ |
| Effect 24/67 — campos e processamento | [Wall](glyphs/effects/wall.md), [Linger](glyphs/effects/linger.md), [Orbit](glyphs/effects/orbit.md), [Smelt](glyphs/effects/smelt.md), [Fangs](glyphs/effects/fangs.md) | child-context, entities, counters, receitas e spawn condicionado | ⚠️ API genérica de effect; comportamento auxiliar condicionado |
| Augment 9 restantes | [Accelerate](glyphs/augments/accelerate.md), [Decelerate](glyphs/augments/decelerate.md), [Dampen](glyphs/augments/dampen.md), [Extend Time](glyphs/augments/extend-time.md), [Reduce Time](glyphs/augments/reduce-time.md), [Extract](glyphs/augments/extract.md), [Fortune](glyphs/augments/fortune.md), [Randomize](glyphs/augments/randomize.md), [Sensitive](glyphs/augments/sensitive.md) | operadores, efeitos dependentes da contagem, config/caps e regras de alvo | ⚠️ alguns setters reais via evento EffectResolve, adapter ⛔ |
| Ritual 6/24 | [Flight](rituals/flight.md), [Binding](rituals/binding.md), [Disintegration](rituals/disintegration.md), [Scrying](rituals/scrying.md), [Warping](rituals/warping.md), [Sanctuary](rituals/sanctuary.md) | range, ticks, Source cost, refresh/jump/packet | ⛔ sem hook provado |

**As cinco sublinhas Effect distribuem 24 fichas (5+4+5+5+5); Augments somam 4+9=13.** A contagem é de dossiês source-pinned, não de novas identidades semânticas.


## Riscos e bloqueios concretos para futuras perks

1. **Amplificação não é sempre dano.** Pode significar Poison, harvest strength, intensidade, alcance etc. Só aplicar por consumidor e limites da receita.
2. **Área e penetração não são universais.** Em `SpellUtil` AOE/Pierce geram largura/altura/profundidade. Em `Freeze` um candidato ainda tenta seis vizinhos. World-cap e claims permanecem QA.
3. **Executor downstream manda.** `EffectLightning` configura `LightningEntity`, `EffectExplosion` configura `ANExplosion`, `Rune` configura `RuneTile`. Hooks sobre a classe de glyph podem perder dano/procs/cooldowns reais.
4. **Possível desvio de restauração de dano no lightning — exige QA.** No source `LightningEntity.tick()`, após `setDamage(adjusted)`, um evento cancelado faz `continue` antes de restaurar `origDamage`. Isso é achado estático, não incidente de runtime comprovado; nenhum patch upstream/Black Arcana foi realizado.
5. **Recursos não se duplicam.** Runas persistentes recarregam Source; próprias magias usam player mana Ars. Sem prova de boundary, é proibido criar um segundo ledger, cast ou Mastery por every-hit.
6. **Eventos públicos existem, mas não são perks implementadas.** `EffectResolveEvent.Pre` permite examinar `SpellStats` antes do efeito; há setters concretos (amp, speed, damageModifier, duration) e eventos de custo separados. `setAoeMultiplier` não existe na instância construída; efeitos que leem `getBuffCount` podem ignorar multiplicadores. Ver [contratos exatos de eventos](VERIFIED-EVENT-SURFACES-5.13.1.md) e testar causalidade, clamps e paridade de custos. ⛔ nenhum adapter RPG aprovado.

## Próximas verificações

- Demais **0 Forms, 43 Effects, 0 Augments e 18 rituais**, sempre ficha a ficha.
- `SpellCastEvent`, `SpellResolveEvent`, `EffectResolveEvent`, `SpellCostCalcEvent` e `DispelEvent` já foram source-pinados; agora falta adapter RPG com testes de sucesso/veto/exactly-once, custo Pre/Post e conflitos com addons.
- Limites reais em `SpellResolver`, `SpellStats.Builder`, `SpellUtil`, claims, `RuneTile` e efeitos persistentes; validar config efetivamente carregada.
- Ensaios em NeoForge 1.21.1/Ars 5.13.1 e modpack/Survival. **Nenhum realizado neste PR**.

[Norma universal](../../meta/PERK-READY-TECHNICAL-STANDARD.md) · [Ledger global](../../meta/PERK-READY-COVERAGE-LEDGER.md) · [PR #795 Iron's](https://github.com/Gustavaopere/Black-Arcana/pull/795).
