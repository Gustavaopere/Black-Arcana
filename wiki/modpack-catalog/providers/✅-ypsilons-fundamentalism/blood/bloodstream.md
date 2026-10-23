# Bloodstream

**Dossiê documental — 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita às fontes abaixo; catálogo ⚠️ condicionado para engenharia de perks. **+0 identidades; nenhuma perk, bridge ou implementação.**

- Provider: Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; ID real **`ypfundamentals:bloodstream`**; taxonomia `spell`; escola default Blood; host Iron's Spellbooks. Classe `com.ypsi.fundamentalism.spells.blood.BloodstreamSpell`; registro [ModSpells#registerSpell][registry].
- Artefato histórico identificado: `ypfundamentals-1.1.7.1.jar`, Minecraft 1.21.1/NeoForge, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503), modlist física #575 e [prova binária de 13/10](../EXACT-BINARY-SPELLS-1.1.7.1.md). `COUNTED_EXACT` prova a identidade estática; não prova estas fórmulas, equivalência de métodos ou execução.
- Source Ypsilon: `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1/MIT, mas dependência declarada **Iron's 3.16.2** ([gradle.properties][versions]). Host examinado separadamente: Iron's **3.16.3**, `e4056af90302d37eb1739f5ff05020b020e6e252`; JAR de referência do pack `irons_spellbooks-1.21.1-3.16.3.jar`. Compatibilidade source→JAR e coexistência **CONDITIONAL**; QA físico **PENDING**.
- Descrição para jogador, paráfrase do [guia oficial][guide]: Buff pessoal que aumenta eficiência física, com modificadores de ataque, movimento e salto.

`L` = nível entregue ao efeito; `P` = `getSpellPower(L,caster)` no source host: `(base + incremento×(L−1)) × SPELL_POWER × poder da escola × POWER_MULTIPLIER` ([AbstractSpell#getSpellPower][host-power]). “Neutro” assume esses três multiplicadores iguais a 1. Defaults não demonstram configuração implantada. Mana pertence ao host; não há recurso sangue adicional comprovado nesta classe.

## Pipeline e parâmetros

**Ingresso:** a classe recebe `CastSource`/`MagicData` do host. Item, tecla, pacote de entrada e aquisição exata no Survival **NÃO VERIFICADOS** nesta ficha; o caminho server de admissão/início é [AbstractSpell#attemptInitiateCast][host-cast]. Dimensão/chunks/claims externos não são autorizados por este catálogo.

Admissão/custo padrão do host → INSTANT → `BloodstreamSpell#onCast` aplica **`ypfundamentals:bloodstream`**, duração `int(P×20)`, amplifier `L−1`, ambient=false/particles=false/icon=true → atributos registrados em `ModEffects`; `BloodstreamEffect` só delega `onEffectAdded` e retorna true no predicado de tick. Não há dano, cura, consumo de vida ou geração de sangue nessa implementação ([aplicação][s-cast], [efeito completo][effect], [registro][effect-reg]).

| Campo | Default/fórmula e unidade | Origem; fase e boundary | Estado / limite | QA |
|---|---|---|---|---|
| Nível/escola/cooldown | Epic; L=1–3; Blood; 60 s =1200 ticks base | `BloodstreamSpell` config [s-values]; host [host-values]/[host-cooldown] | `NATIVE` config; efetiva NÃO VERIFICADA | Q1 |
| Mana/cast | `int((60+30×(L−1))×MANA_MULTIPLIER)` =60/90/120; INSTANT,0 ticks | construtor [s-values], cast type [s-type], host custo/pagamento [host-values]/[host-cast] | `NATIVE`; desconto/nível por evento `CONDITIONAL`; mana authority=host | Q1 |
| Power/duração | P neutro30/40/50; `int(P×20)` =600/800/1000 ticks (30/40/50 s); amp=L−1 | [s-values], `onCast` [s-cast] | `NATIVE` power afeta duração; não altera coeficientes dos atributos na classe | Q1/Q2 |
| Alcance/targeting | apenas caster; sem seleção remota, ray, LOS, AoE ou máximo de alvos | `onCast` [s-cast] | self→ally/área `SEM_HOOK_SEGURO`; claims externos N/A nesta seleção self | Q2 |
| Attack Speed | coeficiente-base0.10; operação `ADD_MULTIPLIED_TOTAL`; tooltip mostra10/20/30% em L1/2/3 | constantes [effect], `ModEffects` [effect-reg], tooltip/fórmulas [s-tooltip] | `NATIVE` atributo de saída; coeficiente do efeito `SEM_HOOK_SEGURO`; aplicação efetiva depende da semântica vanilla amp+1 e demais modifiers, não auditada no JAR | Q2/Q3 |
| Movement Speed | coeficiente-base0.20; `ADD_MULTIPLIED_TOTAL`; tooltip20/40/60% | [effect], [effect-reg], [s-tooltip] | `NATIVE` atributo de saída; coeficiente do efeito `SEM_HOOK_SEGURO`; não equivale velocidade absoluta em blocks/tick, nem acumulação independente com outro buff | Q2/Q3 |
| Jump Strength | coeficiente-base0.15; `ADD_MULTIPLIED_TOTAL`; tooltip15/30/45% | [effect], [effect-reg], [s-tooltip] | `NATIVE` atributo de saída; coeficiente do efeito `SEM_HOOK_SEGURO`; porcentagem do atributo, não altura em blocks comprovada | Q2/Q3 |
| Step Height | coeficiente-base+0.4; `ADD_VALUE`; chave do modifier `ypfundamentals:bloodstream` | `ModEffects` [effect-reg]; resolução de atributos após efeito | coeficiente do efeito `SEM_HOOK_SEGURO`; escala final por amp, clamp e coexistência vanilla **CONDITIONAL**, sem source vanilla/JAR auditado | Q2/Q3 |
| Scale/hitbox | coeficiente-base+0.03; `ADD_MULTIPLIED_BASE`; mesma chave por atributo | [effect-reg]; atributo do LivingEntity | coeficiente do efeito `SEM_HOOK_SEGURO`; altera atributo SCALE; dimensões finais, reach e sync não derivadas aqui; não é projétil nem raio visual | Q2/Q3 |
| Dano/cura/DamageType | N/A: nenhuma chamada de dano/heal/mark; escola Blood não demonstra dano Blood | classe [s-cast], efeito [effect] | não criar lifesteal/healing reduction por afinidade de escola; `SEM_HOOK_SEGURO` para acrescentar resultado | Q4 |
| Tick/refresh/saída | `shouldApplyEffectTickThisTick` retorna true, mas classe não implementa tick de gameplay; modifiers seguem lifecycle MobEffect | [effect], base host [host-effect] | não inventar pulso por tick; merge/refresh/remove/persistência finais delegados a vanilla, **NÃO VERIFICADOS** | Q3/Q4 |
| Projétil/summon/mundo/recast | N/A velocidade/traçado/lifetime/pierce/summons/blocos; sem recast próprio, host base0 | classe [s-cast], [host-recast] | dedup pela aplicação/refresh/remoção do efeito, não cada consulta de atributo | Q4 |

**Escala e ownership:** os valores-base são comprovados no registro. O tooltip implementa `L×coeficiente×100` para os três primeiros atributos; ele não calcula Step Height/Scale nem prova o valor final com outros modifiers. Se o runtime vanilla resolver cada modifier por `amp+1`, os adicionais isolados esperados seriam Step +0.4/+0.8/+1.2 e Scale +0.03/+0.06/+0.09 sobre a base; isso é expectativa de QA, **não medição física nem equivalência auditada do JAR**. Modifiers usam uma chave por atributo e efeito; uma perk não deve duplicar esses modifiers. O MobEffect não armazena token de cast ou caster remoto; o portador é a autoridade local do estado.

## Perks, autoria e verificação

`NATIVE` nesta ficha significa atributo/config do provider identificado no source; não promete controle isolado por jogador. `CONDITIONAL` exige fechar versão, configuração e adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para o parâmetro exato. O host possui `SpellOnCastEvent#setSpellLevel(int)` / `setManaCost(int)` antes de pagar mana e chamar `onCast` ([evento][host-events], [ordem][host-cast]); alterar nível nesse ponto não recalcula necessariamente admissão ou duração já iniciada. `SpellDamageEvent#setAmount(float)` altera apenas o montante que passa por `DamageSources.applyDamage`, antes de resistência/`hurt` ([evento][host-damage-event], [settlement][host-damage]). Nenhum desses eventos prova troca de DamageType, alvos, área ou dimensões. As superfícies permanecem **CONDITIONAL** para este addon/JAR. [Boundaries compartilhados](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

Iron's/Ypsilon conservam cast, mana, cooldown, dano/estados e autoria; RPG Skill Tree conserva progressão/gates por contrato real; Black Arcana só observa ou usa seam validado. Não executar cast, dano, cura, custo ou proc paralelo para simular um parâmetro ausente.

Assinatura semântica ocupada: buff self de atributos físicos com duração por spell power e intensidade por amplifier/nível. VFX, escala ou novo nome não criam outra identidade. Uma magia original precisaria de regra causal própria; lacunas de design não autorizam implementação.

**QA documental:** classes, métodos e downstream citados lidos no commit pinado; links/linhas e fórmulas revisados. **Não executado:** comparação destes métodos com JAR, servidor dedicado, GameTest, cliente, Survival, PvP/claims e coexistência no pack; todos **PENDING**. Obtenção concreta por scroll, loot, receita e progressão Survival **NÃO VERIFICADA**, salvo gate explicitamente descrito acima.

- **Q1:** comparar mana/cooldown/config e duração com power Blood fracionário.
- **Q2:** níveis1/2/3: registrar valores base/finais dos cinco atributos, dimensão e client sync; separar tooltip e valor efetivo.
- **Q3:** coexistência com outros modifiers/escala, reaplicação de mesmo/menor/maior nível, expiração/remoção; detectar stacking indevido.
- **Q4:** logout/morte/reload/counterspell; confirmar ausência de heal/dano/pulso e uma única atribuição de mastery por cast autorizado.

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L27-L49
[versions]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L36
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L70
[host-values]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L174
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[host-admission]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L371-L402
[host-recast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L227-L232
[host-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L65
[host-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[host-type]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L109-L116
[host-tags]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/datagen/DamageTypeTagGenerator.java#L29-L94
[host-events]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L29-L74
[host-damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L51
[host-cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L123
[s-values]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/BloodstreamSpell.java#L26-L40
[s-type]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/BloodstreamSpell.java#L42-L55
[s-cast]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/BloodstreamSpell.java#L57-L69
[s-tooltip]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/BloodstreamSpell.java#L77-L97
[effect]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/custom/BloodstreamEffect.java#L16-L33
[effect-reg]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/ModEffects.java#L39-L51
[host-effect]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/MagicMobEffect.java#L11-L47
