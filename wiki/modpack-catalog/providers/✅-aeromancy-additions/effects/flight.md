# Flight — efeito de Feather Flight

- Registro: `aero_additions:flight`, `MobEffect`, classe `FlightEffect`, categoria `BENEFICIAL`, cor `0xd3ebea`.
- Ativação: **REGISTERED** em `AASpells.MobEffects`; produtor ativo: [Feather Fall](../spells/feather-fall.md). Não é uma magia adicional; contribuição estrita **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Contrato estático do source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites de fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md). O SHA do publisher não prova o JAR instalado; seu SHA-1 histórico de 35 caracteres continua desconhecido/inválido.

## Aplicação, movimento e duração

`FeatherFallSpell` resolve alvo pelo helper de alcance **32**, tolerância **0.35**, com fallback no próprio caster. No cast percorre `LivingEntity` em AABB inflada em **3**, exige distância quadrática `<9`, `Utils.shouldHealEntity(caster,victim)` e máximo de **5** vítimas. Aplica este efeito por `(int)(getSpellPower(level,caster)×20)` ticks, amplifier **0**. Não há dano nem projétil no efeito; alcance de aquisição e raio da seleção pertencem à magia.

O registro adiciona `WATER_MOVEMENT_EFFICIENCY` **+1 ADD_VALUE** e `MOVEMENT_SPEED` **+0.15 ADD_MULTIPLIED_BASE**, ambos com ID `aero_additions:effect.flight` em seus respectivos atributos. São valores base dos modificadores; a aplicação/escalonamento padrão por amplifier pertence ao host de `MobEffect`. Não existe amplificação por nível no produtor, que sempre usa amplifier 0.

`shouldApplyEffectTickThisTick` sempre retorna true. A cada `entity.tickCount % 20 == 0`, recalcula um peso sobre **todos os `EquipmentSlot.values()`**, incluindo mãos e slots de armadura, não apenas peças de armadura. A precedência por slot é: vazio ou `flight_light` → **0**; `flight_heavy` → **4**; `minecraft:anvil` → **10**; qualquer outro item → **2**. Para soma `W`, remove primeiro `aero_additions:flight.gravity`; se `W!=0`, adiciona um modificador transitório em `GRAVITY`, `ADD_VALUE=(W/4f)-0.08`. Com `W=0` não instala modificador de gravidade: não equivale a gravidade zero. Um slot comum (`W=2`) produz **+0.42**; mudanças de equipamento só entram no próximo pulso de 20 ticks. Amplifier não participa desse cálculo.

Na remoção, exige atributo `GRAVITY` não nulo e retira o mesmo modifier antes de chamar o superclass. O callback de tick tolera atributo ausente; o de remoção usa `Objects.requireNonNull`, distinção a validar em entidades customizadas. O efeito não define NBT próprio: duração/amplifier são `MobEffectInstance` do host; o modifier de gravidade é transitório e recalculado. Não há concessão local de `mayfly`/voo criativo nem cancelamento local de dano de queda.

## Consumidores e matriz para perks

| Eixo | Consumidor real | Fronteira de mutação por perk |
|---|---|---|
| Aplicação/duração | `FeatherFallSpell.onCast`; `getDuration` usa spell power efetivo do caster | Atributo de power é input nativo; custo, alvo, cap e duração não são API nova de progressão. Hook por jogador **NOT_VERIFIED**. |
| Gravidade/peso | `FlightEffect.applyEffectTick`, `calculateWeightScore`, `onEffectRemoved` | Tags de peso e ID fixo do modifier são provider-owned. Mudanças globais nas tags afetam todos os usuários; não são perk individual. |
| Movimento em água | `AAServerEvents.Game.activateFlight(PlayerSwimEvent)` devolve `EventResult.SUCCESS` quando tem efeito | É o evento Expandability de natação, sem check local de alvo/caster adicional. Comportamento efetivo e compatibilidade não testados. |
| Atributos | Modificadores registrados de água e velocidade | Não sobrescrever `effect.flight`/`flight.gravity`; empilhamento com outros providers depende do host. |
| Causalidade | Nenhum `hurt`, damage source ou contador de acertos no efeito | Aplicação, pulso e recálculo de peso não provam dano nem justificam Mastery ofensiva. |

QA restante: pesos/precedência de tags nas mãos e armadura, equipamento alterado durante efeito, remoção/reaplicação/reload, atributo ausente, natação em servidor dedicado, queda e compatibilidade de movimento. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro e atributos L165–167](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L165-L167).
- [FlightEffect.java — pulso e remoção L25–54](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FlightEffect.java#L25-L54); [peso L56–69](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FlightEffect.java#L56-L69).
- [FeatherFallSpell.java — seleção L65–96](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FeatherFallSpell.java#L65-L96); [duração L104–106](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FeatherFallSpell.java#L104-L106).
- [AAServerEvents.java — natação L121–124](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L121-L124).
