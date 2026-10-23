# Burning Spirit

**Dossiê documental — 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita às fontes abaixo; catálogo ⚠️ condicionado para engenharia de perks. **+0 identidades; nenhuma perk, bridge ou implementação.**

- Provider: Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; ID real **`ypfundamentals:grantstrength`**; taxonomia `spell`; escola default Fire; host Iron's Spellbooks. Classe `com.ypsi.fundamentalism.spells.fire.BurningSpiritSpell`; registro [ModSpells#registerSpell][registry].
- Artefato histórico identificado: `ypfundamentals-1.1.7.1.jar`, Minecraft 1.21.1/NeoForge, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503), modlist física #575 e [prova binária de 13/10](../EXACT-BINARY-SPELLS-1.1.7.1.md). `COUNTED_EXACT` prova a identidade estática; não prova estas fórmulas, equivalência de métodos ou execução.
- Source Ypsilon: `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1/MIT, mas dependência declarada **Iron's 3.16.2** ([gradle.properties][versions]). Host examinado separadamente: Iron's **3.16.3**, `e4056af90302d37eb1739f5ff05020b020e6e252`; JAR de referência do pack `irons_spellbooks-1.21.1-3.16.3.jar`. Compatibilidade source→JAR e coexistência **CONDITIONAL**; QA físico **PENDING**.
- Descrição para jogador, paráfrase do [guia oficial][guide]: Buff pessoal que limpa alguns estados e emite pulsos ofensivos; seus ataques diretos também incendeiam.

`L` = nível entregue ao efeito; `P` = `getSpellPower(L,caster)` no source host: `(base + incremento×(L−1)) × SPELL_POWER × poder da escola × POWER_MULTIPLIER` ([AbstractSpell#getSpellPower][host-power]). “Neutro” assume esses três multiplicadores iguais a 1. Defaults não demonstram configuração implantada. Mana pertence ao host; não há recurso sangue adicional comprovado nesta classe.

## Pipeline e parâmetros

**Ingresso:** a classe recebe `CastSource`/`MagicData` do host. Item, tecla, pacote de entrada e aquisição exata no Survival **NÃO VERIFICADOS** nesta ficha; o caminho server de admissão/início é [AbstractSpell#attemptInitiateCast][host-cast]. Dimensão/chunks/claims externos não são autorizados por este catálogo.

Admissão padrão do host ([mana/cooldown/learning][host-admission]) → LONG → `BurningSpiritSpell#onCast` aplica **`ypfundamentals:flame_boost`** (nome de exibição Life Flame), duração truncada e amplifier `L−1` → `FlamePoweredEffect#applyEffectTick` → `DamageSources.applyDamage`. O caster é simultaneamente portador e autor do pulso; o efeito não guarda um token de cast/owner separado ([aplicação][s-cast], [registro do efeito][effect-reg], [pulso][effect-tick]).

| Campo | Default/fórmula e unidade | Origem; fase e boundary | Estado / limite | QA |
|---|---|---|---|---|
| Nível/escola/cooldown | Epic; L=1–3; Fire; 54 s = 1080 ticks antes dos modificadores do host | `BurningSpiritSpell` config [s-values]; `getSpellCooldown` [host-values]; server cooldown [host-cooldown] | `NATIVE` config; efetiva NÃO VERIFICADA | Q1 |
| Mana | `int((100+20×(L−1))×MANA_MULTIPLIER)`; neutro 100/120/140 por settlement | construtor [s-values], `AbstractSpell#getManaCost` [host-values]; host paga antes de `onCast` [host-cast] | `NATIVE` config; desconto por evento `CONDITIONAL`; sem segunda cobrança | Q1 |
| Cast/interrupção | LONG; 20 ticks = 1 s; override retorna `getCastTime(L)` e ignora a fórmula de cast reduction herdada | `getEffectiveCastTime` [s-time]; server inicia no host [host-cast] | duração fixa nesta classe; mutação seletiva `SEM_HOOK_SEGURO` | Q1 |
| Power/duração | P neutro 30/40/50; duração `int(P×20)` = 600/800/1000 ticks (30/40/50 s); amplifier `L−1` = 0/1/2 | construtor [s-values]; `onCast` [s-cast]; server effect | `NATIVE` power muda duração; não muda diretamente dano/raio por pulso | Q2 |
| Targeting/alcance | Self na aplicação. Pulso consulta AABB do portador expandida por `r=2×(amp+1)` = 2/4/6 blocks em cada eixo | `FlamePoweredEffect#applyEffectTick` [effect-tick]; server, consulta por pulso | **Não é esfera**: sem corte por distância, LOS, ordenação ou teto numérico de alvos no addon; área `SEM_HOOK_SEGURO` | Q2/Q3 |
| Filtros | exclui o portador na consulta; aceita LivingEntity com `!target.isAlliedTo(portador)`; demais gates em `DamageSources` | loop [effect-tick]; host friendly-fire [host-damage] | filtro local unilateral; claims/proteção externa NÃO VERIFICADOS; single→multi já é AoE nativa, sem seam para mudá-la | Q3 |
| Dano/tipo | `3×amp` = **0/3/6 health points** por alvo/pulso, antes do settlement; source direto = portador, causador = portador; default `irons_spellbooks:fire_magic` | [effect-tick]; school/type [host-type], source [host-source], tag Fire + `neoforge:is_magic` [host-tags] | montante por evento `CONDITIONAL`; trocar tipo `SEM_HOOK_SEGURO`; não presumir `minecraft:is_fire` | Q2/Q3 |
| Periodicidade/cleanse | roda quando **duração restante %40=0**, não por contador próprio; server remove Poison e Wither e zera freeze a cada pulso | `shouldApplyEffectTickThisTick` [effect-period]; cleanse [effect-tick] | 40 ticks = 2 s entre pulsos; recast/refresh pode mudar fase; sem hook seletivo de cadência | Q2/Q4 |
| Ignite derivado | listener `LivingDamageEvent.Pre`: se `directEntity` é LivingEntity com efeito, `igniteForSeconds(2+(amp+1))` = 3/4/5 s | `FlamePoweredEffect#setOnFire` [effect-ignite]; server antes do settlement desse evento | sem teste local de dano final >0, tipo, equipe ou origem do cast; dano de projétil com directEntity projectile não satisfaz esse filtro | Q3/Q4 |
| Projétil/hitbox/visual | N/A: nenhum projétil; Blastwave usa r apenas para VFX; não define hitbox ofensiva esférica | [effect-tick] | redimensionamento visual não altera AABB da consulta; `SEM_HOOK_SEGURO` para nova geometria | Q2/Q3 |
| Summon/mundo/recast | N/A summons/teleporte/mutação de blocos; sem recast próprio observado; host base retorna 0 | classe [s-cast], base [host-recast] | refresh de MobEffect não é novo ledger de pulsos; persistência exata vanilla NÃO VERIFICADA | Q4 |

**Correções e causalidade:** nível 1 realmente recebe amplifier 0 e calcula pulso de dano 0; não “corrigir” por perk. O pulso usa o portador como `directEntity`, portanto pode passar também pelo listener de ignite se o host emitir `LivingDamageEvent.Pre`; a chegada desse evento para dano zero é **NÃO VERIFICADA**. Limpeza, pulso e ignite são resultados do mesmo efeito, sem child-spell independente. Para observação, distinguir aplicação/refresh do efeito, portador, tick do pulso, alvo e evento direto; não reemitir ignite nem contabilizar cada pulso como outro cast.

## Perks, autoria e verificação

`NATIVE` nesta ficha significa atributo/config do provider identificado no source; não promete controle isolado por jogador. `CONDITIONAL` exige fechar versão, configuração e adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para o parâmetro exato. O host possui `SpellOnCastEvent#setSpellLevel(int)` / `setManaCost(int)` antes de pagar mana e chamar `onCast` ([evento][host-events], [ordem][host-cast]); alterar nível nesse ponto não recalcula necessariamente admissão ou duração já iniciada. `SpellDamageEvent#setAmount(float)` altera apenas o montante que passa por `DamageSources.applyDamage`, antes de resistência/`hurt` ([evento][host-damage-event], [settlement][host-damage]). Nenhum desses eventos prova troca de DamageType, alvos, área ou dimensões. As superfícies permanecem **CONDITIONAL** para este addon/JAR. [Boundaries compartilhados](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

Iron's/Ypsilon conservam cast, mana, cooldown, dano/estados e autoria; RPG Skill Tree conserva progressão/gates por contrato real; Black Arcana só observa ou usa seam validado. Não executar cast, dano, cura, custo ou proc paralelo para simular um parâmetro ausente.

Assinatura semântica ocupada: buff pessoal com limpeza periódica, AoE recorrente e ignite em dano direto. VFX, escala ou novo nome não criam outra identidade. Uma magia original precisaria de regra causal própria; lacunas de design não autorizam implementação.

**QA documental:** classes, métodos e downstream citados lidos no commit pinado; links/linhas e fórmulas revisados. **Não executado:** comparação destes métodos com JAR, servidor dedicado, GameTest, cliente, Survival, PvP/claims e coexistência no pack; todos **PENDING**. Obtenção concreta por scroll, loot, receita e progressão Survival **NÃO VERIFICADA**, salvo gate explicitamente descrito acima.

- **Q1:** comparar configs e custo/cooldown reais; testar LONG com cast reduction e cancelamento.
- **Q2:** níveis 1/2/3, duração com power não inteiro e fase `%40`; observar dano zero, cleanse e refresh.
- **Q3:** cantos da AABB, paredes, aliados/PvP, evento de dano cancelado e resistência; separar raio visual da seleção.
- **Q4:** dano melee, outro spell direto, projétil e pulso do próprio efeito; reaplicação, logout/morte e deduplicação dos procs.

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L27-L49
[versions]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L36
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L67
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
[s-values]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/BurningSpiritSpell.java#L32-L45
[s-time]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/BurningSpiritSpell.java#L47-L59
[s-cast]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/BurningSpiritSpell.java#L61-L72
[effect-reg]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/ModEffects.java#L36-L37
[effect-tick]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/custom/FlamePoweredEffect.java#L36-L60
[effect-ignite]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/custom/FlamePoweredEffect.java#L61-L71
[effect-period]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/custom/FlamePoweredEffect.java#L73-L76
