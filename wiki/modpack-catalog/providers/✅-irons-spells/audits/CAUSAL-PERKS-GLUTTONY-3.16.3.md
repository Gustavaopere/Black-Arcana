# Iron's 3.16.3 — Gluttony: recuperação de mana após consumo de alimento

**Estado:** ✅ `SOURCE-PINNED` (causalidade no código consultado); ⚠️ `CAUSAL-PARTIAL` para binário instalado, config, outros providers, client/server e adapter. **+0 novos spells**: `irons_spellbooks:gluttony` já está no conjunto de 110 identidades. Fonte técnica clean-room `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, versão documental Iron's 3.16.3/Minecraft 1.21.1. [Ficha preexistente](../nature/gluttony.md).

## Pipeline causal e propriedades

1. **Cast e custo:** [GluttonySpell L21–60](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/GluttonySpell.java#L21-L60) fixa Nature, Common, níveis 1–5, cooldown default **90 s**, `INSTANT` e mana base **35** sem custo incremental por nível. `baseSpellPower=30`, `spellPowerPerLevel=0`; não concluir duração fixa sob bônus de spell power/config.
2. **Efeito no usuário:** [GluttonySpell L62–70](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/GluttonySpell.java#L62-L70) aplica `MobEffectRegistry.GLUTTONY` ao `LivingEntity` caster, duração `(int)(getSpellPower(spellLevel,caster)*20)` ticks, amplifier `spellLevel-1`. Com multiplicadores unitários, duração nominal **600 ticks/30 s** em todos os níveis.
3. **Evento real de recompensa:** [GluttonyEffect L14–37](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/GluttonyEffect.java#L14-L37) escuta `LivingEntityUseItemEvent.Finish`; exige lado **servidor**, presença de `FoodProperties` no item consumido e status `GLUTTONY` na entidade que come. Então invoca `MagicData.getPlayerMagicData(entity).addMana(food.nutrition()*ratioForAmplifier(amplifier))`. Não é bônus por kill, cast, dano ou simples ticking do efeito. O comentário no código exclui consumo de **cake blocks** nesse handler; não extrapolar para todos os padrões de alimentação de outros mods.
4. **Fator por nível:** [GluttonyEffect L39–42](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/GluttonyEffect.java#L39-L42): `ratioForAmplifier(a)=(4+a)*0.5`. Com amplifier `level-1`, o multiplicador nominal é **2,0 / 2,5 / 3,0 / 3,5 / 4,0** vezes a `nutrition` do item nos níveis 1–5. O retorno de mana é `float`, não assumir arredondamento inteiro.
5. **Autoridade de mana:** [MagicData L54–76](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/magic/MagicData.java#L54-L76) mostra `addMana(delta)->setMana(old+delta)`. Em `setMana`, o provider cria `ChangeManaEvent`, publica no `NeoForge.EVENT_BUS` **se houver ServerPlayer**, respeita cancelamento, usa `event.getNewMana()` e então limita o total **superiormente** a `AttributeRegistry.MAX_MANA` para ServerPlayer. O método mostrado não aplica clamp inferior geral; isto não implica mana negativa via este ganho positivo. `ChangeManaEvent` possui `getOldMana`, `getNewMana`, `setNewMana(float)` e pode ser cancelado: [ChangeManaEvent L20–47](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/ChangeManaEvent.java#L20-L47). A documentação Java do evento menciona Forge antigo; **o corpo compilável de MagicData usa `NeoForge.EVENT_BUS`**.
6. **Sincronização:** o listener envia `SyncManaPacket` quando o consumidor é `ServerPlayer` após chamar `addMana`. Uma eventual outra modificação/cancelamento pelo evento pode ocorrer antes do sync; não duplicar pacote ou crédito de mana no adapter. [GluttonyEffect L24–36](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/GluttonyEffect.java#L24-L36).
7. **Admissão e custo:** o cast original de 35 mana permanece sob gate de `canBeCastedBy` antes de `SpellOnCastEvent`. Não fazer engenharia de 'cast grátis' apenas alterando a cobrança pós-gate. [AbstractSpell L373–393](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L373-L393). A recuperação por comida acontece em *outro evento*, possivelmente depois de múltiplos casts, e não deve ser somada às ações raiz para Mastery.
8. **Interoperabilidade:** `GLUTTONY` é um efeito `MagicMobEffect` do Iron's e seu processamento é provider-owned; as integrações podem observar `ChangeManaEvent` **sem** criar uma segunda mana de Black Arcana nem transformar `LivingEntityUseItemEvent.Finish` em um segundo `addMana`. Se forem exigidas modificações específicas por magia, o contexto do evento genérico de mana **não comprova** a origem Gluttony por si só.

## Matriz de perks

| Eixo | Mecanismo provado | Situação |
|---|---|---|
| Duração | `(int)(getSpellPower*20)` | ⚠️ atributo de power altera indiretamente múltiplas magias; ⛔ não há setter per-Gluttony validado |
| Mana recuperada | `nutrition * (4+amplifier)*0.5` | ✅ `ChangeManaEvent.setNewMana` existe para ServerPlayer; ⚠️ evento é **genérico**, sem proveniência específica da comida no próprio contrato |
| Amplifier | `spellLevel -1` | ⚠️ nível altera ganho por consumo, mas `ModifySpellLevelEvent` deve ser validado em seu caller antes do adapter |
| Trigger | `LivingEntityUseItemEvent.Finish` + FoodProperties + efeito | ⛔ não contar cake / finish duplicado / outros consumos sem evidência adicional |
| Tipo de alvo | efeito no caster e bônus ao consumidor com efeito | ⛔ nenhum retarget ou distribuição em área segura demonstrada |
| Custo | 35 mana, cooldown 90 s default | ⚠️ poder de compra/custo provider-owned; `SpellOnCastEvent` após gate |
| Cap e persistência | `MAX_MANA` superior para ServerPlayer | ⚠️ event cancellation, outros atributos, relog/client sync precisam QA |

## Aceitação pendente

- [ ] JAR físico exato e config de 3.16.3; equivalência de `ChangeManaEvent` e `MagicData`.
- [ ] Consumir itens com `nutrition` diferentes, food de outro mod, alimento não comestível, cake block e eventos `Finish` concorrentes.
- [ ] Validar `MAX_MANA`, arredondamento float, `ChangeManaEvent` cancelado/alterado, sync, mana cheio, diferentes cast sources e creative.
- [ ] Testar reinício/relog, duração/amplificador, Counterspell/dispel e não duplicação do bônus.
- [ ] Validar progressão RPG somente no cast original e não a cada alimento ingerido sem requisito explícito.

**Clean-room:** evidência de interoperabilidade e links de fonte; nenhum código/asset do provider copiado.
