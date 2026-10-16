# Iron's 3.16.3 — Blight: redução de cura recebida e dano causado por listeners gerais

**Identidade:** `irons_spellbooks:blight` · escola Nature · Minecraft 1.21.1 / NeoForge / Iron's documental 3.16.3. ✅ ID já presente entre 110; 🟡 aprofundamento causal de perks; ✅ classfiles do JAR publicado auditados; ⚠️ servidor físico pendente; ⛔ alterações em multiplicadores, listeners e alcance sem boundary real. **+0 identidade mágica nova.**

**Source pin:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`. Conteúdo clean-room de interoperabilidade, não port do provider.

## Prova binária publicada — Java 21

[Actions Java 21 #38834814254](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38834814254) **SUCCESS** confirmou no publisher JAR `BlightSpell.onCast` com alvo `TargetEntityCastData`/efeito `BLIGHT` e os listeners `BlightEffect.reduceHealing` (`LivingHealEvent.setAmount`) e `reduceDamageOutput` (`LivingIncomingDamageEvent.setAmount`). Os fatores de 10% e 5% por nível vêm da fonte fixada e **não** são medições de resultados no servidor. [Relatório binário](../../../../../docs/qa/irons-3163-healing-heartstop-blight-bytecode-evidence.md).

## Cadeia causal com duas entradas de evento

1. **Spell e defaults:** `irons_spellbooks:blight` é Nature / RARE, `CastType.LONG`, `castTime=50` ticks nominais, níveis **1–8**, cooldown-base **90 s**, mana-base `60` mais `20×(level−1)` → **60–200**, spell power base `1`, por nível `0`, antes de multiplicadores/config. [`BlightSpell.java` L28–L53](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/BlightSpell.java#L28-L53), [`BlightSpell.java` L55–L68](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/BlightSpell.java#L55-L68). Não extrapolar tempo de canal para casts separados.
2. **Gate de targeting:** `checkPreCastConditions` utiliza `Utils.preCastTargetHelper(level,entity,playerMagicData,this,32,.35f)`, portanto alcance nominal de **32** e margem indicada **0,35**, mas filtros, visibilidade e linha de visão vêm do helper; verificar a implementação exata antes de declarar que atravessa blocos ou alvos. [`BlightSpell.java` L81–L84](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/BlightSpell.java#L81-L84).
3. **Aplicação:** `onCast` consulta `playerMagicData.getAdditionalCastData()`, exige `TargetEntityCastData`, resolve alvo no `ServerLevel` e adiciona efeito `MobEffectRegistry.BLIGHT` se alvo não nulo. Se data/target falhar, esse método **não aplica efeito** e ainda chega a `super.onCast`. A contabilidade de mana/cooldown/cast bem-sucedido depende do pipeline real e gate de pre-cast, não é garantida apenas pelo `onCast`. [`BlightSpell.java` L87–L96](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/BlightSpell.java#L87-L96).
4. **Amplifier e duração:** `getAmplifier(level,caster)=level−1`, logo níveis 1–8 resultam amplifiers 0–7. `getDuration=(int)(getSpellPower(level,caster)×20×30)` → base nominal **600 ticks/30 s** com power unitário, **não** 600 segundos. [`BlightSpell.java` L98–L104](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/BlightSpell.java#L98-L104).
5. **Primeiro listener — redução de cura recebida:** `BlightEffect.reduceHealing(LivingHealEvent)` busca `BLIGHT` **no alvo sendo curado**. Com `lvl=amplifier+1` aplica `event.setAmount(event.getAmount()×(1−0.10×lvl))`. Nível-base 1: **90%** do `LivingHealEvent` de entrada; nível 8: **20%** do valor de entrada, se nenhum outro modificador/ordem interferir. É multiplicador do **evento de cura geral**, não só de `HealSpell` do Iron's. [`BlightEffect.java` L13–L33](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/BlightEffect.java#L13-L33).
6. **Segundo listener — redução de dano causado:** `BlightEffect.reduceDamageOutput(LivingIncomingDamageEvent)` obtém `event.getSource().getEntity()` e exige atacante `LivingEntity` com BLIGHT ativo; usa `event.setAmount(event.getAmount()×(1−0.05×lvl))`. Nível-base 1: **95%** do valor de entrada; nível 8: **60%**. Portanto não reduz necessariamente o dano **recebido** pelo alvo afetado: o filtro é o **atacante que carrega o efeito**. Em `DamageSource` sem atacante LivingEntity, esta rotina não age. [`BlightEffect.java` L35–L48](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/BlightEffect.java#L35-L48).
7. **Amplitude e escopo:** as duas rotinas estão anotadas `@SubscribeEvent` em `@EventBusSubscriber`; a redução resulta de **listeners gerais de NeoForge enquanto o efeito existe**, sem precisar que o caster de Blight esteja presente. O evento de cura `SpellHealEvent` é independente e anterior ao `entity.heal` nos spells `heal`/Greater Heal; Blight age no `LivingHealEvent` que a engine emite, não modifica `SpellHealEvent.healAmount`. [`BlightEffect.java` L9–L24](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/BlightEffect.java#L9-L24), [`HealSpell.java` L63–L67](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L63-L67), [`GreaterHealSpell.java` L63–L69](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java#L63-L69).
8. **Ordem de prioridades, outros mods e limites:** `event.setAmount` atua sobre o valor corrente do evento, de modo que dois listeners de cura/dano de mods distintos podem compor efeitos conforme ordem de inscrição/priority. Este source não certifica valores finais de HP/dano ou interações com claims/resistências; medir `LivingHealEvent`, `LivingIncomingDamageEvent`, `LivingDamageEvent.Post` e HP real no modpack. Não realizar multiplicação duplicada em Black Arcana nem recalcular após outro provider.
9. **Causalidade de Mastery:** um cast raiz entrega 1 efeito BLIGHT no alvo; o efeito pode afetar **N tentativas futuras de cura e dano** ao longo dos ticks de duração. Nenhum dos N eventos derivados representa nova conjuração. Sem atribuição validada de efeito ao caster, não creditar XP para cada golpe ou cura parcialmente bloqueada, sob risco de farm e proc chains ilimitados.
10. **Perks e custos:** `getSpellPower` pode influenciar **duração**, mas os percentuais por nível estão em constantes de `BlightEffect`, que não fornecem setter de percentuais per-player no código observado. Sem boundary público realmente compilado, ⛔ amplificação de percentuais/range e bypass de resistências. Custos e cooldown são exclusivamente do Iron's.

## Matriz de cálculo nominal

| Nível | Amplifier | `LivingHealEvent` (fração do valor de entrada) | `LivingIncomingDamageEvent` do atacante afetado |
|---:|---:|---:|---:|
| 1 | 0 | 0,90× | 0,95× |
| 2 | 1 | 0,80× | 0,90× |
| 3 | 2 | 0,70× | 0,85× |
| 4 | 3 | 0,60× | 0,80× |
| 5 | 4 | 0,50× | 0,75× |
| 6 | 5 | 0,40× | 0,70× |
| 7 | 6 | 0,30× | 0,65× |
| 8 | 7 | 0,20× | 0,60× |

**Atenção:** percentuais são fatores na entrada do listener, **não HP/dano final medido**, e só se aplicam se o efeito ativo e o source corresponderem.

## Testes e bloqueios

- [ ] JAR publisher: classfiles `BlightSpell`, `BlightEffect` e método do targeting helper; SHA-256 instalado não verificado.
- [ ] Separar número de casts raiz de número de `LivingHealEvent`/`LivingIncomingDamageEvent` modificados; provar fase e prioridade em servidor NeoForge.
- [ ] Verificar HP 100%, Blight num caster de Heal/Greater Heal, cura recebida de poção/comida/outro mod e `DamageSource` sem `getEntity()`.
- [ ] Testar permissões de PvP/claims, duplos buffs/debuffs e ordem de callbacks após remoção, morte/relog e chunk unload.
- [ ] Sem adapter seguro e idempotência comprovada, `Mastery` só credita cast legítimo, não o número de eventos de efeito.
- [ ] Stage 06.05 🟡 e Stage 09 pendente; nenhuma alteração de runtime ou merge por esta ficha.

**Conclusão:** Blight afeta **cura do alvo** e **dano produzido pelo atacante afetado** por dois listeners de eventos gerais; ambos são derivados do efeito aplicado por um único cast.
