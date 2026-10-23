# Pyrokinesis

**Dossiê documental — 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita às fontes abaixo; catálogo ⚠️ condicionado para engenharia de perks. **+0 identidades; nenhuma perk, bridge ou implementação.**

- Provider: Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; ID real **`ypfundamentals:pyrokinesis`**; taxonomia `spell`; escola default Fire; host Iron's Spellbooks. Classe `com.ypsi.fundamentalism.spells.fire.PyrokinesisSpell`; registro [ModSpells#registerSpell][registry].
- Artefato histórico identificado: `ypfundamentals-1.1.7.1.jar`, Minecraft 1.21.1/NeoForge, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503), modlist física #575 e [prova binária de 13/10](../EXACT-BINARY-SPELLS-1.1.7.1.md). `COUNTED_EXACT` prova a identidade estática; não prova estas fórmulas, equivalência de métodos ou execução.
- Source Ypsilon: `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1/MIT, mas dependência declarada **Iron's 3.16.2** ([gradle.properties][versions]). Host examinado separadamente: Iron's **3.16.3**, `e4056af90302d37eb1739f5ff05020b020e6e252`; JAR de referência do pack `irons_spellbooks-1.21.1-3.16.3.jar`. Compatibilidade source→JAR e coexistência **CONDITIONAL**; QA físico **PENDING**.
- Descrição para jogador, paráfrase do [guia oficial][guide]: Canaliza o controle de projéteis de fogo próximos e limpa fogo do próprio caster.

`L` = nível entregue ao efeito; `P` = `getSpellPower(L,caster)` no source host: `(base + incremento×(L−1)) × SPELL_POWER × poder da escola × POWER_MULTIPLIER` ([AbstractSpell#getSpellPower][host-power]). “Neutro” assume esses três multiplicadores iguais a 1. Defaults não demonstram configuração implantada. Mana pertence ao host; não há recurso sangue adicional comprovado nesta classe.

## Pipeline e parâmetros

**Ingresso:** a classe recebe `CastSource`/`MagicData` do host. Item, tecla, pacote de entrada e aquisição exata no Survival **NÃO VERIFICADOS** nesta ficha; o caminho server de admissão/início é [AbstractSpell#attemptInitiateCast][host-cast]. Dimensão/chunks/claims externos não são autorizados por este catálogo.

Pré-cast cria **uma área de targeting visual** com owner e `TargetAreaCastData` → CONTINUOUS do host → `onServerCastTick` limpa fogo e percorre entidades → reatribui owner e velocidade/direção dos elegíveis → efeitos terminais continuam pertencendo à classe de cada projétil. `onCast` só delega ao host; a reflexão não depende de um hit ou dano novo ([pré-cast][s-pre], [loop][s-loop]).

| Campo | Default/fórmula e unidade | Origem; fase e boundary | Estado / limite | QA |
|---|---|---|---|---|
| Nível/escola/cooldown | Rare; L=1–5; Fire; cooldown base 5 s = 100 ticks | `PyrokinesisSpell` config [s-values]; host [host-values]/[host-cooldown] | `NATIVE` config; efetiva NÃO VERIFICADA | Q1 |
| Canal/duração | CONTINUOUS; `getCastTime(L)=20+20×(L−1)` = 20/40/60/80/100 ticks (1–5 s) antes do modifier herdado | [s-values], [s-time]; `getEffectiveCastTime` [host-power] | host contínuo usa CAST_TIME_REDUCTION como multiplicador de duração; não afirmar canal invariável | Q1/Q2 |
| Mana | `int((10+2×(L−1))×MANA_MULTIPLIER)` = 10/12/14/16/18 **por settlement**, não total do canal | [s-values], [host-values]; `MagicManager#tick` [host-channel], pagamento [host-cast] | host chama castSpell em intervalos de 10 ticks e na conclusão; testa reserva de 2×custo para continuar; nenhum custo por projétil no loop | Q1/Q2 |
| Power | base 1 + 1×(L−1); não lido no efeito de reflexão | construtor [s-values] e loop completo [s-loop] | `NATIVE` atributo existe; aumentar power não prova bônus de raio/velocidade/quantidade | Q2 |
| Geometria/alvos | `getEntities(caster,caster.getBoundingBox().inflate(3))`; extensão 3 blocks em cada face da AABB atual | `onServerCastTick` [s-loop]; server a cada tick ativo | **Não é esfera de raio 3**; não há corte por distância, LOS, teto numérico, owner ou equipe | Q3 |
| Elegibilidade | AbstractMagicProjectile cuja string de classe uppercase contém `FIRE`; ou AbstractArrow em fogo; ou Fireball; ou FireworkRocketEntity | cadeia if/else [s-loop] | nome de classe não é escola/tag; AbstractMagicProjectile sem FIRE não cai nos ramos posteriores | Q3/Q4 |
| Direção/velocidade | magic projectile: `setOwner(caster); shoot(look)` usa `getSpeed()` da classe; outros três: `shoot(x,y,z,3,0)` = velocidade 3 e inaccuracy 0 | [s-loop]; `AbstractMagicProjectile#shoot` [host-projectile-shoot] | `SEM_HOOK_SEGURO` para modificar política seletivamente; lifetime/hitbox/dano do projétil não são reiniciados explicitamente | Q3/Q4 |
| Repetição/owner | nenhuma marca one-shot, filtro contra owner atual ou ledger de refletidos; a variável `reflected` é reiniciada **por entidade e tick** | [s-loop] | pode reassumir/refletir de novo enquanto estiver na AABB; dois casters disputam owner; não prometer reflexão única | Q4 |
| Dano/DamageType | nenhum `applyDamage` próprio; não altera damage, DamageType ou explosão; dano futuro usa a implementação do projétil e owner que ela consultar | loop completo [s-loop] | N/A dano direto; atribuição final/causador pode mudar com setOwner; requer auditoria por classe elegível | Q4 |
| Visual/hitbox | área visual radius=3, owner=caster; host dimensões width=6/height=0.8 blocks, `noPhysics`; **não** é a AABB da reflexão | pré-cast [s-pre]; `TargetedAreaEntity` [host-area] | alterar visual não altera consulta; summons ofensivos N/A | Q2/Q3 |
| Saída/cleanup | override de conclusão só chama super; host reseta casting/additional data e `EntityCastData#reset` descarta marcador | [s-end], [host-complete], [host-reset], [host-entity-data] | lifetime visual de fallback >400 ticks sem duração e owner inválido descarta; não confundir com duração do canal | Q2 |
| Mundo/recast | sem bloco/explosão própria; nenhum recast local; host base 0 | [s-loop], [s-end], [host-recast] | reflexão não é novo cast do projétil nem autoriza segundo mana/cooldown por hit | Q4 |

**Correção de authority:** o source **não implementa** uma reflexão única por projétil. A bridge deve preservar a repetição nativa ao observar, sem adicionar outro `shoot`/`setOwner`. Cleansing roda a cada tick ativo, não a cada intervalo de pagamento. Som/8 partículas são emitidos a cada reflexão reconhecida; não são sucesso de dano. Deduplicação para mastery precisa separar sessão de canal, settlements de 10 ticks, tick+UUID do projétil e dano terminal; a mesma entidade pode gerar várias observações legítimas.

## Perks, autoria e verificação

`NATIVE` nesta ficha significa atributo/config do provider identificado no source; não promete controle isolado por jogador. `CONDITIONAL` exige fechar versão, configuração e adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para o parâmetro exato. O host possui `SpellOnCastEvent#setSpellLevel(int)` / `setManaCost(int)` antes de pagar mana e chamar `onCast` ([evento][host-events], [ordem][host-cast]); alterar nível nesse ponto não recalcula necessariamente admissão ou duração já iniciada. `SpellDamageEvent#setAmount(float)` altera apenas o montante que passa por `DamageSources.applyDamage`, antes de resistência/`hurt` ([evento][host-damage-event], [settlement][host-damage]). Nenhum desses eventos prova troca de DamageType, alvos, área ou dimensões. As superfícies permanecem **CONDITIONAL** para este addon/JAR. [Boundaries compartilhados](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

Iron's/Ypsilon conservam cast, mana, cooldown, dano/estados e autoria; RPG Skill Tree conserva progressão/gates por contrato real; Black Arcana só observa ou usa seam validado. Não executar cast, dano, cura, custo ou proc paralelo para simular um parâmetro ausente.

Assinatura semântica ocupada: canal de limpeza de fogo e redirecionamento repetível de classes específicas de projéteis, com transferência de owner. VFX, escala ou novo nome não criam outra identidade. Uma magia original precisaria de regra causal própria; lacunas de design não autorizam implementação.

**QA documental:** classes, métodos e downstream citados lidos no commit pinado; links/linhas e fórmulas revisados. **Não executado:** comparação destes métodos com JAR, servidor dedicado, GameTest, cliente, Survival, PvP/claims e coexistência no pack; todos **PENDING**. Obtenção concreta por scroll, loot, receita e progressão Survival **NÃO VERIFICADA**, salvo gate explicitamente descrito acima.

- **Q1:** medir pagamentos completos e cancelados por fonte de cast, config, mana insuficiente e efeito do atributo de duração.
- **Q2:** início/fim/cancelamento/desconexão, marcador visual e cleanup; confirmar quantidade de ticks efetivos do loop.
- **Q3:** cantos da AABB, parede, projétil do caster/aliado, cada classe e subclass com/sem FIRE no nome; separar marcador e volume real.
- **Q4:** mesma entidade em ticks consecutivos, dois casters, foguete e fireball com aceleração própria, collision/lifetime preservados e autoria final; nenhum cast/dano/custo duplicado.

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L27-L49
[versions]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L36
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L68
[host-values]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L174
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[host-admission]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L371-L402
[host-recast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L227-L232
[host-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L65
[host-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[host-type]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L59-L67
[host-tags]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/datagen/DamageTypeTagGenerator.java#L29-L94
[host-events]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L29-L74
[host-damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L51
[host-cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L123
[s-values]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/PyrokinesisSpell.java#L41-L55
[s-time]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/PyrokinesisSpell.java#L57-L67
[s-pre]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/PyrokinesisSpell.java#L69-L80
[s-loop]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/PyrokinesisSpell.java#L82-L118
[s-end]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/PyrokinesisSpell.java#L120-L128
[host-channel]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L44-L83
[host-projectile-shoot]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L74-L85
[host-area]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/target_area/TargetedAreaEntity.java#L61-L117
[host-complete]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L413-L424
[host-reset]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/magic/MagicData.java#L107-L143
[host-entity-data]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/EntityCastData.java#L8-L28
