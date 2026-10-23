# Thorn

**Dossiê documental — 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita às fontes abaixo; catálogo ⚠️ condicionado para engenharia de perks. **+0 identidades; nenhuma perk, bridge ou implementação.**

- Provider: Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; ID real **`ypfundamentals:thorn`**; taxonomia `spell`; escola default Blood; host Iron's Spellbooks. Classe `com.ypsi.fundamentalism.spells.blood.ThornSpell`; registro [ModSpells#registerSpell][registry].
- Artefato histórico identificado: `ypfundamentals-1.1.7.1.jar`, Minecraft 1.21.1/NeoForge, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503), modlist física #575 e [prova binária de 13/10](../EXACT-BINARY-SPELLS-1.1.7.1.md). `COUNTED_EXACT` prova a identidade estática; não prova estas fórmulas, equivalência de métodos ou execução.
- Source Ypsilon: `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1/MIT, mas dependência declarada **Iron's 3.16.2** ([gradle.properties][versions]). Host examinado separadamente: Iron's **3.16.3**, `e4056af90302d37eb1739f5ff05020b020e6e252`; JAR de referência do pack `irons_spellbooks-1.21.1-3.16.3.jar`. Compatibilidade source→JAR e coexistência **CONDITIONAL**; QA físico **PENDING**.
- Descrição para jogador, paráfrase do [guia oficial][guide]: Projétil que aplica uma marca e consome uma marca existente para aumentar o dano do hit.

`L` = nível entregue ao efeito; `P` = `getSpellPower(L,caster)` no source host: `(base + incremento×(L−1)) × SPELL_POWER × poder da escola × POWER_MULTIPLIER` ([AbstractSpell#getSpellPower][host-power]). “Neutro” assume esses três multiplicadores iguais a 1. Defaults não demonstram configuração implantada. Mana pertence ao host; não há recurso sangue adicional comprovado nesta classe.

## Pipeline e parâmetros

**Ingresso:** a classe recebe `CastSource`/`MagicData` do host. Item, tecla, pacote de entrada e aquisição exata no Survival **NÃO VERIFICADOS** nesta ficha; o caminho server de admissão/início é [AbstractSpell#attemptInitiateCast][host-cast]. Dimensão/chunks/claims externos não são autorizados por este catálogo.

INSTANT → `ThornSpell#onCast` instancia **um** `ThornProjectile`, atribui owner, posição, direção e dano → herança detecta colisão → `onHitEntity` → consulta **`ypfundamentals:marked`** no alvo → aplica/remove marca **antes** do dano → `DamageSources.applyDamage` → descarta. Impacto em bloco e alvo não LivingEntity também descartam. O efeito Marked é `MagicMobEffect` sem listener próprio localizado; o consumo está no projétil ([spawn][s-cast], [impacto][p-impact], [registro][effect-reg]).

| Campo | Default/fórmula e unidade | Origem; fase e boundary | Estado / limite | QA |
|---|---|---|---|---|
| Nível/escola/cooldown | Common; L=1–5; Blood;12 s=240 ticks base | `ThornSpell` config [s-values]; host [host-values]/[host-cooldown] | `NATIVE` config; efetiva NÃO VERIFICADA | Q1 |
| Mana/cast | `int((20+5×(L−1))×MANA_MULTIPLIER)`=20/25/30/35/40; INSTANT0 ticks | construtor/cast type [s-values], host [host-values]/[host-cast] | `NATIVE`; evento custo/nível `CONDITIONAL`; nenhum custo de sangue | Q1 |
| Power/dano base | P neutro10/15/20/25/30; snapshot `d=0.5×P`=5/7.5/10/12.5/15 health points | `getDamage` [s-formula], spawn [s-cast] | `NATIVE` poder Blood/config; evento dano `CONDITIONAL`, não novo cast | Q1/Q3 |
| Spawn/velocidade | posiçãoCaster +Y(`eyeHeight−0.5×alturaThorn`); look×speed2 blocks/tick; owner=caster; sem gravidade/spread local | [s-cast], construtores/`getSpeed` [p-flight]; host [host-projectile] | um projétil; não faz raycast de aquisição; alcance nominal não é constante de seleção | Q2 |
| Hitbox/visual | registry width=height0.5 blocks; sem override de dimensões; renderer modelo2×2×8 unidades de modelo, orientado pela velocidade; trail raio0.25 e2 steps | [entity-reg], [p-render], [p-trail] | dimensões registradas não são raio de dano; VFX/modelo não alteram collision | Q2 |
| Collision/lifetime | host AABB própria expandida no trajeto+0.1; interseção ray/target inflação0.3; owner e aliados de qualquer lado excluídos; expira `tickCount>300` (15 s) | `AbstractMagicProjectile` [host-projectile] | herança3.16.3 **CONDITIONAL** para addon3.16.2; sem cap de alcance remoto próprio nem pierce útil no override que descarta | Q2/Q4 |
| Primeiro hit/mark | sem Marked: aplica `MobEffectInstance(MARKED,300 ticks,amp0)` **antes** de `applyDamage(d)` | `ThornProjectile#onHitEntity` [p-impact] | marca dura15 s; não depende do boolean de dano; apply/remove imunes/cancelados exigem QA | Q3 |
| Hit marcado | com Marked: remove efeito **antes** de `applyDamage(3×d)`=15/22.5/30/37.5/45 health points | [p-impact] | bônus **3×d total**, sem hit adicional d; consome marca mesmo se dano rejeitado; `SEM_HOOK_SEGURO` para alterar regra | Q3/Q4 |
| DamageType/owner | default `irons_spellbooks:blood_magic`; tags Blood/`neoforge:is_magic`; directEntity=projétil, causador=getOwner() no impacto | [p-impact], [host-type], [host-source], [host-tags] | converter tipo `SEM_HOOK_SEGURO`; owner atual pode diferir do caster original após reflexão | Q3/Q4 |
| Área visual de bônus | `rVFX=3×(1+0.5×health/maxHealth)` (3–4.5 blocks para fração0–1); blastwave/som/camera shake10 ticks/alcance20 | [p-impact] | **não há AoE de dano** nem consulta a vizinhos nesse branch; câmera não define alcance ofensivo | Q3 |
| LOS/targeting | nenhum LOS adicional no `onHitEntity`; caminho checa blocos pelo host; alvo precisa LivingEntity para mark/dano | [p-impact], [host-projectile] | single→multi/AoE e seleção segura `SEM_HOOK_SEGURO`; proteção/friendly-fire host no dano não garante rollback de mark | Q2/Q3 |
| Knockback | não configura knockback extra nem implementa NoKnockbackProjectile; segue helper de dano/vanilla | classe [p-impact], helper [host-damage] | força final **NÃO VERIFICADA**; não criar empurrão paralelo | Q3 |
| Estado/saída/recast | marca é estado do alvo sem owner/cast token; qualquer Thorn que a encontre usa branch marcado; projétil descarta após ambos ramos | [effect-reg], [p-impact]; sem recast próprio, host0 [host-recast] | marca compartilhada entre casters; N/A summons/blocos/DoT/lifesteal; persistência final do efeito vanilla NÃO VERIFICADA | Q4 |

**Causalidade e limites:** blastwave e camera shake no branch marcado são visuais, sem dano em área. O projétil ignora o resultado de `applyDamage`; uma marca pode ser criada/consumida sem settlement aceito. Não criar ledger de mark paralelo, reverter consumo por conta própria ou emitir um hit bônus separado. A herança tem APIs genéricas de pierce/ricochet, mas este override descarta incondicionalmente após impacto de LivingEntity e não chama `consumeEntityImpact`; API genérica não prova perk de pierce funcional aqui. Para mastery, ligar cast→UUID do projétil→impacto→ramo→alvo/dano, e tratar Marked como estado compartilhado do provider.

## Perks, autoria e verificação

`NATIVE` nesta ficha significa atributo/config do provider identificado no source; não promete controle isolado por jogador. `CONDITIONAL` exige fechar versão, configuração e adapter; `SEM_HOOK_SEGURO` = ⛔ fail-closed para o parâmetro exato. O host possui `SpellOnCastEvent#setSpellLevel(int)` / `setManaCost(int)` antes de pagar mana e chamar `onCast` ([evento][host-events], [ordem][host-cast]); alterar nível nesse ponto não recalcula necessariamente admissão ou duração já iniciada. `SpellDamageEvent#setAmount(float)` altera apenas o montante que passa por `DamageSources.applyDamage`, antes de resistência/`hurt` ([evento][host-damage-event], [settlement][host-damage]). Nenhum desses eventos prova troca de DamageType, alvos, área ou dimensões. As superfícies permanecem **CONDITIONAL** para este addon/JAR. [Boundaries compartilhados](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

Iron's/Ypsilon conservam cast, mana, cooldown, dano/estados e autoria; RPG Skill Tree conserva progressão/gates por contrato real; Black Arcana só observa ou usa seam validado. Não executar cast, dano, cura, custo ou proc paralelo para simular um parâmetro ausente.

Assinatura semântica ocupada: projétil de alvo único com alternância aplicar/consumir marca compartilhada e dano triplicado no consumo. VFX, escala ou novo nome não criam outra identidade. Uma magia original precisaria de regra causal própria; lacunas de design não autorizam implementação.

**QA documental:** classes, métodos e downstream citados lidos no commit pinado; links/linhas e fórmulas revisados. **Não executado:** comparação destes métodos com JAR, servidor dedicado, GameTest, cliente, Survival, PvP/claims e coexistência no pack; todos **PENDING**. Obtenção concreta por scroll, loot, receita e progressão Survival **NÃO VERIFICADA**, salvo gate explicitamente descrito acima.

- **Q1:** mana/cooldown/config real, power Blood e snapshot após lançamento.
- **Q2:** colisão em bloco/escudo/alvo rápido e tamanho distinto, owner/aliados, gravidade/velocidade/lifetime, client sync e unload/antimagic.
- **Q3:** primeiro/segundo hit, vizinhos próximos sem AoE, dano cancelado/imune e aplicação/consumo de mark independente do sucesso.
- **Q4:** dois casters consumindo a mesma marca, expiração/refresh/save/reload, owner transferido e nenhum hit/cast/proc duplicado.

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L27-L49
[versions]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L36
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L71
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
[s-values]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/ThornSpell.java#L31-L49
[s-cast]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/ThornSpell.java#L63-L77
[s-formula]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/blood/ThornSpell.java#L79-L81
[p-flight]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/thorn/ThornProjectile.java#L38-L52
[p-impact]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/thorn/ThornProjectile.java#L65-L99
[p-trail]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/thorn/ThornProjectile.java#L101-L128
[p-render]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/thorn/ThornRenderer.java#L42-L66
[entity-reg]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/ModEntities.java#L47-L51
[effect-reg]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/effect/ModEffects.java#L24-L25
[host-projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L214
