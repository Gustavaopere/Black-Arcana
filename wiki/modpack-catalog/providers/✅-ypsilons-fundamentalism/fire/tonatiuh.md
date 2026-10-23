# Tonatiuh

**Dossiê documental — 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita às fontes abaixo; catálogo ⚠️ condicionado para engenharia de perks. **+0 identidades; nenhuma perk, bridge ou implementação.**

- Provider: Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; ID real **`ypfundamentals:sol`**; taxonomia `spell`; escola default Fire; host Iron's Spellbooks. Classe `com.ypsi.fundamentalism.spells.fire.SolSpell`; registro [ModSpells#registerSpell][registry].
- Artefato histórico identificado: `ypfundamentals-1.1.7.1.jar`, Minecraft 1.21.1/NeoForge, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503), modlist física #575 e [prova binária de 13/10](../EXACT-BINARY-SPELLS-1.1.7.1.md). `COUNTED_EXACT` prova a identidade estática; não prova estas fórmulas, equivalência de métodos ou execução.
- Source Ypsilon: `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1/MIT, mas dependência declarada **Iron's 3.16.2** ([gradle.properties][versions]). Host examinado separadamente: Iron's **3.16.3**, `e4056af90302d37eb1739f5ff05020b020e6e252`; JAR de referência do pack `irons_spellbooks-1.21.1-3.16.3.jar`. Compatibilidade source→JAR e coexistência **CONDITIONAL**; QA físico **PENDING**.
- Descrição para jogador, paráfrase do [guia oficial][guide]: Lança um astro reduzido cujo tamanho e dano dependem do horário consultado pelo caster.

`L` = nível entregue ao efeito; `P` = `getSpellPower(L,caster)` no source host: `(base + incremento×(L−1)) × SPELL_POWER × poder da escola × POWER_MULTIPLIER` ([AbstractSpell#getSpellPower][host-power]). “Neutro” assume esses três multiplicadores iguais a 1. Defaults não demonstram configuração implantada. Mana pertence ao host; não há recurso sangue adicional comprovado nesta classe.

## Pipeline e parâmetros

**Ingresso:** a classe recebe `CastSource`/`MagicData` do host. Item, tecla, pacote de entrada e aquisição exata no Survival **NÃO VERIFICADOS** nesta ficha; o caminho server de admissão/início é [AbstractSpell#attemptInitiateCast][host-cast]. Dimensão/chunks/claims externos não são autorizados por este catálogo.

O host exige aprendizado → LONG → `SolSpell#onCast` instancia **um** `SolProjectile`, snapshot de dano/tamanhos e owner → voo herdado → `SolProjectile#onHit` executa AoE manual → se griefing ativo, executa também uma `Explosion` → VFX/som → `discard`. O source não faz um cast filho independente para essa explosão ([spawn][s-cast], [impacto][p-impact]).

| Campo | Default/fórmula e unidade | Origem; fase e boundary | Estado / limite | QA |
|---|---|---|---|---|
| Nível/escola/cooldown | Legendary; L=1; Fire; 300 s = 6000 ticks base | `SolSpell` config [s-values]; host [host-values]/[host-cooldown] | `NATIVE` config; não supor L>1 permitido pela config efetiva | Q1 |
| Mana/cast | `int((450+120×(L−1))×MANA_MULTIPLIER)`; neutro L1=450; LONG 200 ticks =10 s antes da redução herdada | construtor [s-values], host custo [host-values], duração [host-power] | `NATIVE`; ao contrário de Burning Spirit, não sobrescreve `getEffectiveCastTime` | Q1 |
| Aprendizado | `requiresLearning=true`; listener server de morte do FireBossEntity aprende para `source.getEntity()` que seja ServerPlayer e ainda não aprendeu | [s-learning], `ModEvents#onFireBossDeath` [unlock] | não concede a participantes, summons ou nearby players por inferência; hook de unlock próprio NÃO VERIFICADO | Q1/Q5 |
| Tempo solar | boost `b` usa `level.getDayTime()` **sem `%24000`**; fallback 1 para null ou valor fora das faixas | `getTimeBoost` [s-formula]; server no snapshot | constante privada `SEM_HOOK_SEGURO`; após 24000 não presumir ciclo solar repetido | Q2 |
| Dano | `D=P×b` health points; P neutro 30 em L1 → 7.5/22.5/30/45/75 conforme b | `getDamage` [s-formula], `setDamage` [s-cast]; snapshot server | `NATIVE` power também muda R; evento montante `CONDITIONAL` só no AoE via helper | Q2/Q4 |
| Raio base/hitbox | `R=√L+0.15×P×b`; `setRadius(R)` sincroniza `min(R,48)`; dimensões dinâmicas width=height=`2×getRadius()` blocks | [s-formula], [s-cast], `SolProjectile#setRadius/getDimensions` [p-size] | cap 48 é do raio de dimensões, **não** do raio explosivo; dimensão máxima96×96; abaixo0.1 descarta em sync | Q2/Q3 |
| ExplosionRadius | snapshot **bruto** `X=4×R`, sem clamp local; AoE manual usa X; Explosion usa força `3×X=12×R` | [s-cast], [p-impact], setter herdado [host-projectile-values] | `SEM_HOOK_SEGURO` para perk de área; não confundir R, X, força e alcance visual | Q3/Q4 |
| Spawn/velocidade | olhos + `0.5×alturaCaster` vertical + um `forward`; `shoot(look)` com speed0.7 blocks/tick; sem gravidade/spread local | [s-cast], construtores [p-flight], speed [p-speed], host [host-projectile] | 1 projétil; sem aceleração local; não é alcance de targeting | Q3 |
| Collision/lifetime | registry base12×12 substituído pelas dimensões dinâmicas; host expira `tickCount>300` (15 s); consulta AABB expandida no trajeto+0.1, interseção ray/target com inflação0.3 | registry [entity-reg], [p-size], `AbstractMagicProjectile` [host-projectile] | hitbox grande não prova colisão esférica de raio R: etapa estreita usa ray; owner/aliados excluídos pelo host; lifetime `CONDITIONAL` na herança3.16.3 | Q3/Q5 |
| AoE/LOS/filtros | consulta AABB do projétil inflate(X), exige `distance²(hit)<X²`, `canHitEntity` e LOS até centro do alvo; origem LOS é ray de posição a posição+2Y | `SolProjectile#onHit` [p-impact] | sem teto de alvos; falloff `D×(1−distance²/X²)`; alcance seleção N/A; claims externos NÃO VERIFICADOS | Q4 |
| DamageType/owner | default `irons_spellbooks:fire_magic`, tags Fire/`neoforge:is_magic`; directEntity=Sol, causador=owner, na AoE e Explosion | [p-impact], [host-type], [host-source], [host-tags] | trocar tipo `SEM_HOOK_SEGURO`; owner pode mudar por outra mecânica; não fixa dono no cast token | Q4/Q5 |
| Mundo/segunda fase | `SPELL_GREIFING=true`: Explosion em posição do projétil, source explícito, força3X, gera fogo, `DESTROY`; posta `ExplosionEvent.Start` e respeita cancelamento antes de explode/finalize | [p-impact] | cancelar essa Explosion **não desfaz AoE manual anterior**; dano/knockback vanilla da Explosion não passa pelo helper do AoE; política externa `CONDITIONAL` | Q4 |
| Pierce/knockback | não configura pierce/ricochet; `onHit` descarta sem consumir continuations; nenhum incremento de knockback próprio no AoE; fase Explosion usa pipeline vanilla | [p-impact], defaults da herança [host-projectile-defaults] | API de pierce herdada não demonstra continuação nesse override; knockback final **NÃO VERIFICADO** | Q3/Q4 |
| Visual/recast | renderer gira cubo de aresta0.5 escalado por bbWidth; partículas usam X; camera shake20 ticks/alcance120 a cada20 ticks e tick1; sem recast próprio | [p-render], [p-tick], [p-impact], [host-recast] | visual não é esfera/hitbox; N/A summon; não adicionar segunda explosão nem novo cast | Q3/Q5 |

### Ordem exata de horário e limites

| `getDayTime()` absoluto em ticks | b |
|---|---|
| `15000<t<21000` | 0.25 |
| `12000≤t≤15000` ou `21000≤t≤24000` | 0.75 |
| `0≤t≤3000` ou `9000≤t<12000` | 1 |
| `4500≤t≤7500` | 2.5 |
| `3000<t<9000` após os testes acima | 1.5 |
| Fora disso, incluindo `t>24000` | 1 |

As linhas seguem a ordem `if/else if` ([fonte][s-formula]); 4500–7500 recebe 2.5 antes do teste amplo 3000–9000. Em L1/P30, `R=1+4.5b`: R=2.125/4.375/5.5/7.75/12.25; X=8.5/17.5/22/31/49 blocks; força da Explosion=25.5/52.5/66/93/147. A força vanilla não é promessa de raio exato de blocos destruídos. Power extremo pode acionar cap de dimensões enquanto X continua crescendo sem cap local.

**Causalidade/persistência:** AoE e Explosion são duas fases reais do mesmo impacto, não duplicação a ser “compensada”. O source salva Radius/Age/Damage e chama a persistência herdada; o override de leitura tenta fallback Damage0→1 e testa Radius via `getInt` antes de ler float, mas chama `super` por último ([save/load][p-save]). No host3.16.3 examinado, `AbstractMagicProjectile#readAdditionalSaveData` relê `Damage` e o reatribui, podendo restaurar0; portanto esse fallback não é um resultado final garantido, e a persistência efetiva no JAR permanece **CONDITIONAL** ([save/load do host][host-save]). Não há token global de dedup, cap por cast de alvos ou coordenação com explosões externas. O host interrompe o loop de hits de entidades ao detectar remoção, mas ainda pode despachar a colisão de bloco no mesmo tick; `SolProjectile#onHit` não verifica `isRemoved` antes de executar. Logo, entity+block no mesmo tick é caso de reentrada a testar, **não garantia de impacto único nem bug reproduzido no JAR** ([detecção][host-projectile]). Correlacionar caster/UUID do Sol/impacto/fase/alvo; um listener de `SpellDamageEvent` cobre o helper manual, não toda a fase vanilla.

## Perks, autoria e verificação

`NATIVE` nesta ficha significa atributo/config do provider identificado no source; não promete controle isolado por jogador. `CONDITIONAL` exige fechar versão, configuração e adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para o parâmetro exato. O host possui `SpellOnCastEvent#setSpellLevel(int)` / `setManaCost(int)` antes de pagar mana e chamar `onCast` ([evento][host-events], [ordem][host-cast]); alterar nível nesse ponto não recalcula necessariamente admissão ou duração já iniciada. `SpellDamageEvent#setAmount(float)` altera apenas o montante que passa por `DamageSources.applyDamage`, antes de resistência/`hurt` ([evento][host-damage-event], [settlement][host-damage]). Nenhum desses eventos prova troca de DamageType, alvos, área ou dimensões. As superfícies permanecem **CONDITIONAL** para este addon/JAR. [Boundaries compartilhados](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

Iron's/Ypsilon conservam cast, mana, cooldown, dano/estados e autoria; RPG Skill Tree conserva progressão/gates por contrato real; Black Arcana só observa ou usa seam validado. Não executar cast, dano, cura, custo ou proc paralelo para simular um parâmetro ausente.

Assinatura semântica ocupada: astro-projétil com escala por horário absoluto e impacto em duas fases: AoE com falloff e explosão opcional destrutiva. VFX, escala ou novo nome não criam outra identidade. Uma magia original precisaria de regra causal própria; lacunas de design não autorizam implementação.

**QA documental:** classes, métodos e downstream citados lidos no commit pinado; links/linhas e fórmulas revisados. **Não executado:** comparação destes métodos com JAR, servidor dedicado, GameTest, cliente, Survival, PvP/claims e coexistência no pack; todos **PENDING**. Obtenção concreta por scroll, loot, receita e progressão Survival **NÃO VERIFICADA**, salvo gate explicitamente descrito acima.

- **Q1:** learning FireBoss por dano direto/indireto e permissões, custo/config e LONG com redução/cancelamento.
- **Q2:** limites exatos de horário, segundo dia (`>24000`), dimensões sem céu e power alto/fracionário; provar snapshot.
- **Q3:** hitbox/renderer/collision de blocos e entidades, cap48 versus X sem clamp, velocidade/lifetime e client sync.
- **Q4:** distâncias/LOS, parede/escudo, aliado/PvP/claims, griefing on/off e `ExplosionEvent.Start` cancelado; medir AoE e Explosion separadamente.
- **Q5:** unload/save/reload/antimagic, mudança de owner/reflexão, morte do caster e entity+block no mesmo tick, reentrada e ausência de proc/custo adicional da bridge.

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L27-L49
[versions]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L36
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L69
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
[s-values]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/SolSpell.java#L40-L53
[s-cast]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/SolSpell.java#L56-L72
[s-formula]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/SolSpell.java#L83-L116
[s-learning]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fire/SolSpell.java#L125-L133
[unlock]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L1103-L1127
[p-flight]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sol/SolProjectile.java#L41-L51
[p-impact]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sol/SolProjectile.java#L98-L137
[p-size]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sol/SolProjectile.java#L139-L168
[p-save]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sol/SolProjectile.java#L170-L188
[p-tick]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sol/SolProjectile.java#L190-L202
[p-render]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sol/SolRenderer.java#L37-L76
[entity-reg]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/ModEntities.java#L41-L45
[host-projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L214
[host-projectile-values]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L445-L459
[p-speed]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/sol/SolProjectile.java#L98-L100
[host-projectile-defaults]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L310-L315
[host-save]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L324-L358
