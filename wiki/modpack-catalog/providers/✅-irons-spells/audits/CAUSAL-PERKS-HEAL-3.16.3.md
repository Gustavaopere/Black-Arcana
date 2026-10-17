# Iron's 3.16.3 — Heal: intenção de cura versus vida recuperada

**Identidade:** `irons_spellbooks:heal` · escola Holy · Iron's 3.16.3 / Minecraft 1.21.1 / NeoForge. ✅ magia entre as 110 identidades catalogadas; 🟡 este é apenas aprofundamento causal; ✅ classfile publicado inspecionado; ⚠️ observação física ausente; ⛔ hook de multiplicação de cura ou Mastery por evento sem QA/contrato. **+0 objeto semântico.**

**Fonte versionada:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`. Prova de fonte orientada a interoperabilidade e clean-room, não implementação de spell para Black Arcana.

## Prova binária publicada — Java 21

[Actions Java 21 #38834814254](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38834814254) **SUCCESS** confirmou no classfile publicado a criação/publicação de `SpellHealEvent` **antes da invocação de `LivingEntity.heal`**. A inspeção estática registra explicitamente `net_hp_recovery=REQUIRES_LIVE_HP_SNAPSHOT`; não conclui que o evento equivale a HP útil recuperado e não autoriza Mastery por duas notificações. [Relatório binário](../../../../../docs/qa/irons-3163-healing-heartstop-blight-bytecode-evidence.md).

## Encadeamento causal

1. **Configuração:** [`HealSpell.java` L22–L45](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L22-L45) define Holy / UNCOMMON, níveis **1–8**, cooldown-default **30 segundos**, cast `INSTANT` e `castTime=0`, custo nominal `30+15×(level−1)` = **30–135 mana**. `baseSpellPower=5`, `spellPowerPerLevel=1` → **5–12 unidades nominais** antes dos multiplicadores de entidade/escola/config.
2. **Alvo e evento de intenção:** [`HealSpell.java` L63–L67](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L63-L67) calcula `healAmount=getSpellPower(spellLevel,entity)`, então publica `new SpellHealEvent(entity,entity,healAmount,getSchoolType())` na `NeoForge.EVENT_BUS`. Alvo é o **próprio caster** neste método, sem pesquisa de alvos externos. O evento de cura é uma **notificação pré-chamada**, não evento de confirmação de HP.
3. **Estrutura do evento:** `SpellHealEvent` estende `LivingEvent`; armazena `targetEntity`, `healAmount` e escola, sem `setHealAmount` e sem `ICancellableEvent` na declaração mostrada. A Javadoc da fonte o descreve não cancelável. [`SpellHealEvent.java` L9–L40](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellHealEvent.java#L9-L40). Um listener de Mastery não pode concluir que 5–12 HP realmente foram restaurados apenas pelo `getHealAmount()`.
4. **Cura aplicada depois:** `entity.heal(healAmount)` usa o valor local calculado **sem ler retorno ou mutação do `SpellHealEvent`**, no passo seguinte à postagem. [`HealSpell.java` L63–L77](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L63-L77). A quantidade real é condicionada a vida faltante, limites de HP, `LivingHealEvent` do NeoForge e modificadores de outros mods. A ordem dentro de `LivingEntity.heal` requer prova da versão mapeada/JAR, não está demonstrada por esta fonte.
5. **Separação de eventos:** um cast pode provocar **`SpellHealEvent`** do Iron's e **`LivingHealEvent`** do NeoForge quando `heal` é chamado. O primeiro é intenção/valor proposto; o segundo pode transformar quantidade de cura. Se Blight está ativo no alvo, seu listener atua no **`LivingHealEvent`**, não no `SpellHealEvent`; [`BlightEffect.java` L22–L33](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/BlightEffect.java#L22-L33). Um observador que soma ambos **duplica a mesma tentativa** de cura.
6. **Efeitos visuais e super:** `HealSpell.onCast` cria anel de partículas HEART com 16 posições e chama `super.onCast` em seguida, sem criar novo feitiço ou entidade de dano. [`HealSpell.java` L67–L77](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L67-L77). Mana e cooldown permanecem responsabilidade da pipeline de Iron's `AbstractSpell.castSpell`, não de listeners externos. [`AbstractSpell.java` L305–L332](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L305-L332).
7. **Mastery correto:** distinguir **cast autorizado (raiz)**, `SpellHealEvent` emitido, `LivingHealEvent` emitido, `healthBefore/After` efetivamente observado e quantidade líquida de vida restaurada. Se o alvo está na vida máxima, `SpellHealEvent` ainda é publicado pelo callsite; **não** contabilizar `getHealAmount` como vida útil curada em tal caso sem medir HP. Sem correlação estável e gate para casts reais, atribuições automáticas ficam ⚠️/⛔.

## Matriz de perks e integrações

| Eixo | Prova da fonte | Estado |
|---|---|---|
| Identidade e cast | `irons_spellbooks:heal`, `INSTANT`, somente caster | ✅ catalogado e source-pinned |
| Cura nominal | `getSpellPower`, base 5–12 | ⚠️ atributo/config e vida faltante não validados |
| `SpellHealEvent` | evento pré-`heal`, `healAmount` sem setter | ✅ contrato estrutural de fonte; ⚠️ classe API/javap no pack a confirmar |
| `LivingHealEvent` | listener Blight reduz a cura do alvo | ⚠️ ordem NeoForge físico e plugins não medidos |
| Quantidade efetiva | `entity.heal` após evento | ⛔ sem leitura de HP real não derivar progresso por quantidade |
| Custos/cooldown | 30–135 mana; cooldown 30 s base | ⚠️ provider-owned; não debitar segundo recurso |
| Perk de amplificação | `getSpellPower` afetável por atributos de Holy, sujeito aos contratos reais | ⛔ não inventar setter per-caster de evento ou hook de sobrecura |
| FX | 16 HEART particles de cast | ⛔ não contabilizar como feitiços/curas |

## Critérios físicos pendentes

- [ ] Auditar bytecode publicado e JAR instalado: `HealSpell.onCast`, `SpellHealEvent`, chamadas `NeoForge.EVENT_BUS.post` e `entity.heal`.
- [ ] Medir `healthBefore`/depois e `LivingHealEvent` no servidor com HP cheio, faltando 1, faltando 10, Blight ativo, resistência à cura e modificadores externos.
- [ ] Confirmar cancelamentos/reduções do motor e ordem por prioridade de listener; impedir XP por `SpellHealEvent` emitido sem cura concreta quando política requer HP útil.
- [ ] Testar custo, cooldown, nível modificado via evento e clientes/dedicated server no modpack físico (NeoForge 21.1.248).
- [ ] Não implementar alteração de efeitos de Iron's, cura dupla ou Mastery por notificações duplicadas até boundary genuíno.

**Conclusão:** `SpellHealEvent` é prova de tentativa de cura, não certificado de HP restaurado. Conteúdo mágico canônico inalterado; Stage 06.05 🟡, Stage 09 pendente.
