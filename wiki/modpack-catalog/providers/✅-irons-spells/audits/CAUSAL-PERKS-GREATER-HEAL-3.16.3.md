# Iron's 3.16.3 — Greater Heal: canal longo, valor de evento versus cura efetiva

**Identidade:** `irons_spellbooks:greater_heal` · escola Holy · Iron's 3.16.3 / Minecraft 1.21.1 / NeoForge. ✅ identidade entre as 110 já inventariadas; 🟡 novo aprofundamento causal; ⚠️ binário/execução e lifecycle de canal não comprovados; ⛔ novos recursos/casts derivados sem contrato. **+0 objeto semântico global.**

**Provenance:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; leitura para interoperabilidade, clean-room. Esta ficha complementa [Heal](./CAUSAL-PERKS-HEAL-3.16.3.md), não duplica esse spell.

## Caminho causal

1. **Configuração e escala:** [`GreaterHealSpell.java` L23–L46](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java#L23-L46) define `irons_spellbooks:greater_heal`, Holy, raridade RARE, **nível máximo 1**, cooldown-base **45 segundos**, custo nominal **100 mana**, `castTime=120` ticks de canal/preparação (**6 s a 20 TPS**) e `CastType.LONG`. Potência-base `0` e ganho por nível `0`; a cura **não** é `getSpellPower` escalado, ao contrário de `heal`. Tempo efetivo e interrupções podem ser modificados por casting speed/pipeline e precisam de prova in-game. [`GreaterHealSpell.java` L48–L60](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java#L48-L60).
2. **Alvo próprio e valor de evento:** em `onCast`, `float healAmount=entity.getMaxHealth()`, sem depender do quanto de HP falta. Em seguida publica `new SpellHealEvent(entity,entity,healAmount,getSchoolType())` e chama `entity.heal(healAmount)`. [`GreaterHealSpell.java` L63–L70](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java#L63-L70). Assim `SpellHealEvent.getHealAmount` pode reportar **vida máxima total**, ainda que o jogador esteja a 99% de HP ou já esteja cheio; isso **não** representa HP realmente restaurado.
3. **Contrato do evento:** `SpellHealEvent` é `LivingEvent`, contém `targetEntity`, quantidade proposta e school; não declara método setter para alterar a quantidade nem `ICancellableEvent` na classe inspecionada. [`SpellHealEvent.java` L18–L40](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellHealEvent.java#L18-L40). Como `GreaterHealSpell` usa a variável local `healAmount` depois do `post`, um listener de evento não obtém automaticamente um modificador seguro da quantidade de cura. A ação `LivingEntity.heal` pode envolver outro evento e outros mods, exigindo leitura real da ordem NeoForge.
4. **Separação entre proposta e recuperação:** a quantidade de vida que `entity.heal` pode devolver depende do déficit de HP, máximo de HP, `LivingHealEvent`, efeitos e customizações de outro mod; sem snapshot de `healthBefore` e `healthAfter`, não informar `100%` da vida máxima como cura útil nem converter diretamente valor do evento em Mastery. [`GreaterHealSpell.java` L63–L69](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java#L63-L69), [`BlightEffect.java` L22–L32](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/BlightEffect.java#L22-L32).
5. **Canal `LONG` e recorte de eventos:** `castTime=120` não significa 120 casts, 120 eventos `SpellHealEvent` ou 120 aplicações por tick. O código de `onCast` tem **uma** postagem e **uma** chamada `heal`. Atribuição do momento da aplicação ao fim de canal e cancelamentos depende do `AbstractSpell` e da engine de conjuração, não desta classe isolada.
6. **Visual em rede:** `PacketDistributor.sendToPlayersTrackingEntityAndSelf(entity,new HealParticlesPacket(entity.position()))` transmite efeito para observadores; pacote de partículas não aplica HP extra e não é nova habilidade. [`GreaterHealSpell.java` L63–L70](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java#L63-L70). Confirmar servidor-cliente e observer tracking em GameTest; packet send no código não prova entrega.
7. **Custos e progresso:** mana/cooldown são do Iron's; Black Arcana não duplica cobrança e RPG Skill Tree não assume canal. Um cast LONG terminado pode gerar 1 evento de intenção de cura, 1 tentativa `heal`, 1 packet FX e no máximo uma recuperação útil observável. Sem boundary seguro, XP por duração, por callback de packet ou por `SpellHealEvent` proposto é ⛔ bloqueado.

## Comparação causal com Heal

| Campo | `heal` | `greater_heal` |
|---|---|---|
| Tipo | INSTANT | LONG, 120 ticks nominais |
| Níveis | 1–8 | 1 |
| Cooldown nominal | 30 s | 45 s |
| Mana nominal | 30–135 | 100 |
| Valor passado para `SpellHealEvent` | `getSpellPower(level,caster)` | `caster.getMaxHealth()` |
| Call ao motor | `entity.heal(healAmount)` | `entity.heal(healAmount)` |
| Intensidade de efeitos | anel de partículas HEART | `HealParticlesPacket` rastreado |
| Quantidade real de HP | ⚠️ condicionada ao déficit/NeoForge | ⚠️ condicionada ao déficit/NeoForge |

Referências: [`HealSpell.java` L32–L45](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L32-L45), [`HealSpell.java` L63–L76](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L63-L76), [`GreaterHealSpell.java` L33–L69](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/GreaterHealSpell.java#L33-L69).

## Gates de aceitação

- [ ] Verificar classfile `GreaterHealSpell`, assinatura do `SpellHealEvent` e contrato de `LONG` para o JAR publicado 3.16.3 e arquivo do modpack instalado.
- [ ] Instrumentar cura com HP máximo, 1 HP faltante, 20 HP faltantes, Blight e bloqueios customizados; comparar valores de evento, `LivingHealEvent`, HP anterior e posterior.
- [ ] Ensaiar interrupção de cast `LONG`, mortes durante canal, cooldown por interrupção e tempo sob atributos de velocidade; nunca assumir 120 triggers.
- [ ] Confirmar pacote de partículas tracking e comportamento de client/dedicated server com NeoForge 21.1.248, sem contar FX como cura.
- [ ] Medir idempotência da premiação Mastery com um token de cast autorizado, evitando duplo processamento dos eventos de `heal`/Greater Heal.

**Status de engenharia:** ✅ identidade catalogada e fonte pin; ⚠️ contrato de retorno real de HP e timing live em aberto; ⛔ perks que alteram cura/tempo sem seam seguro. Stage 06.05 🟡.
