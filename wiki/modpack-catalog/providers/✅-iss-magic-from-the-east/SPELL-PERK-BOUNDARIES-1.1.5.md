# Magic From The East 1.1.5 — contratos comuns para perks

**27/10/2026 · documentação condicionada.** As 22 identidades estão comprovadas no [registry binário](EXACT-BINARY-SPELLS-1.1.5.md). As fórmulas locais das fichas vêm da fonte candidata **`f2a095cbbc89f8d8428dca758140663adf54ae88`**, `RELEASE_BOUNDED_SOURCE`; a [reconciliação de proveniência](RELEASE-SOURCE-RECONCILIATION-1.1.5.md) descreve os confrontos estreitos com o JAR e as divergências das fontes anteriores. Não há equivalência integral fonte↔JAR, config implantada ou integração por perk homologadas.

## Versões, escolas e parâmetros

O [source candidato][versions] declara MC **1.21.1**, MFTE **1.1.5**, NeoForge **21.1.187**, Iron’s **3.14.8**, GeckoLib **4.7.5.1** e Curios **9.2.2**. O pack de referência usa NeoForge **21.1.250** e Iron’s **3.16.3**. O host consultado abaixo é **`iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`**, que [declara 3.16.3][host-version]. A compatibilidade entre o addon compilado e esse host permanece condicionada.

`MFTESchoolRegistries` [declara][schools] **`iss_magicfromtheeast:symmetry`**, **`iss_magicfromtheeast:spirit`** e **`iss_magicfromtheeast:dune`**. As 22 spells ativas se distribuem em **11 Symmetry + 11 Spirit**; escola declarada sem spell não acrescenta identidade mágica. Esses nomes não são aliases de escolas nativas do Iron’s. Os atributos próprios de power/resistência têm [default 1, faixa −100..100 e sync][attributes]; uma faixa declarada não significa que valores extremos sejam balanceados ou aprovados por perk.

No [host][power], `getSpellPower(L,caster)` calcula **`(base + incremento × (L−1)) × SPELL_POWER × schoolPower × POWER_MULTIPLIER`**. O helper `getEntityPowerMultiplier` omite a parcela base/nível. Só parâmetros cujo consumidor chama esses métodos acompanham tais multiplicadores. Quantidade, raio, HP, velocidade, duração e dano de arma podem seguir cálculos próprios; a ficha identifica cada consumidor.

O custo do host é **`int((baseMana + incrementoMana × (L−1)) × MANA_MULTIPLIER)`**, com conversão para inteiro. Cooldown configurado em segundos vira **`int(segundos × 20)` ticks**. `getCastTime` retorna zero para `INSTANT`; os demais casts usam seu tempo base em ticks. [`getEffectiveCastTime`][cast-time] arredonda o produto desse tempo por `CAST_TIME_REDUCTION` para `CONTINUOUS`, ou por `2 − softCapFormula(CAST_TIME_REDUCTION)` para os demais, quando há caster; sem caster o multiplicador é 1. A [soft cap][cast-soft-cap] é uma fórmula de atributo, não um teto fixo de ticks. Alterar cast time não altera automaticamente cooldown, recast, vida do summon ou DOT. [Custo e cooldown][host-formulas].

A [config MFTE][config] é registrada como **`ModConfig.Type.SERVER`** no [bootstrap][bootstrap], arquivo `iss_magicfromtheeast-server.toml`. Impermanence tem default **0.2**, `passChallenging=false`, Soulburn máximo **10.0** e escala **5**; somente entradas marcadas individualmente com `worldRestart()` recebem essa exigência no source. Não há `allowBlockProvidingSoulburn` nessa configuração candidata. Defaults não substituem a configuração efetivamente carregada. A [metadata][metadata] exige Iron’s **`[1.21.1-3.14.0,)`**; satisfazer esse intervalo não prova compatibilidade comportamental com 3.16.3.

## Ordem causal e eventos do host

No wrapper de jogador, [admissão][admission] é server-side: disponibilidade/cooldown e condições da spell precedem `SpellPreCastEvent`; cancelamento impede o início nesse caminho. Depois vêm o estado de casting, `onServerPreCast` e os pacotes. Esse evento não confirma impacto, spawn ou pagamento concluído.

Em [`castSpell`][cast], o host cria `SpellOnCastEvent` com o nível recebido e o custo já calculado, publica o evento, debita mana quando a origem/recast/creative permitem e só então chama `onCast` com o nível resultante. Recasts são atualizados e o cooldown é aplicado ou adiado depois. Alterar o nível nesse evento não recalcula automaticamente o custo original, não refaz a admissão nem os snapshots de pré-cast. A invocação de [`super.onCast`][base-oncast] por um filho não reentra, por si só, no wrapper de pagamento; a base toca o som de conclusão.

| Superfície comprovada no source do host | O que permite | Limite para uma perk |
|---|---|---|
| [`ModifySpellLevelEvent`][level-event], publicado por `getLevelFor` | `setLevel` / `addLevels` sobre o nível consultado; caster pode ser nulo | Só vale quando o resultado dessa consulta é realmente consumido; distinto da edição posterior no cast |
| [`SpellPreCastEvent`][pre-event] | Cancelar a admissão no produtor examinado | Não tem setter de custo/nível; não é sinal de sucesso terminal |
| [`SpellOnCastEvent`][cast-event] | Setters de nível e mana; evento não cancelável | Efeito ainda não executado. Custo editado só é debitado nas condições do wrapper; não há setter universal de raio, alvo ou projétil |
| [`SpellDamageEvent`][damage-event] via [`DamageSources.applyDamage`][damage-helper] | Editar amount e cancelar antes da resistência/friendly-fire/`hurt` | Caminho exige alvo `LivingEntity` e `SpellDamageSource`. `hurt` direto e fontes comuns não passam automaticamente pelo helper; tentativa não equivale a HP removido |
| [`SpellSummonEvent`][summon-event] | Substituir a referência `creature` | Não cancelável; sem setters de count/duração. Só existe onde o produtor publica e consome a referência; examinar casts de tipo, init, spawn e cleanup por spell |
| [`SpellCooldownAddedEvent.Pre`][cooldown-event] | Editar cooldown efetivo ou cancelar | [`MagicManager`][cooldown-manager] consome Pre antes de gravar/sincronizar; scroll/cancelamento retornam. Post observa o caminho de adição; timers filhos continuam separados |
| [`SpellHealEvent`][heal-event] | Observar caster, target, school e quantidade proposta | Sem setter/cancelamento/spell ID. O [produtor HealSpell][heal-producer] publica antes de `heal`, logo não mede HP restaurado; cura direta de outro consumidor não recebe o evento automaticamente |

A existência dessas APIs comprova seu **contrato de source**, não um adapter MFTE/RPG já implementado. Para conversão de tipo de dano, target único→área, novo resolver de alcance, contagem e redimensionamento de projétil, manter **⛔ SEM_HOOK_SEGURO** até localizar e validar o produtor/consumidor específico antes do settlement. Um setter de quantidade de dano não troca `DamageType`. Um observador de impacto não é um mutador universal de geometria.

## Entidades, geometria e autoria

[`AbstractMagicProjectile#shoot(Vec3)`][projectile] multiplica o vetor recebido por `getSpeed()` sem normalizá-lo. O caminho de tick da base tem expiry **`tickCount > 300`** e descarte fora do ticking range; [`travel`][projectile-travel] aplica gravidade quando `isNoGravity()` é falso. Uma subclasse que substitui o tick ou sua colisão precisa ser auditada separadamente. O getter de velocidade isolado não prova movimento real quando outro caminho grava delta diretamente.

A [detecção herdada][collision] usa swept AABB inflada **0.1**, interseção com inflação default **0.3**, ordenação por distância e supressão de repetição no mesmo tick. No ramo de colisão com entidade, `ProjectileImpactEvent` pode cancelar o callback; o ramo de bloco chama `onHit` diretamente. A [lógica de escudo e helpers de impacto][impact] pode produzir caminhos adicionais; chamar `super` e continuar executando requer observar remoção, ricochete, pierce e callbacks. Nunca inferir que cada instância produz exatamente uma tentativa de dano.

Hitbox declarada no registry, AABB reconstruída, raio de consulta, distância de origem e escala visual são dimensões diferentes. [`AoeEntity`][aoe] tem filtros e raio próprios, mas overrides MFTE podem substituí-los, [deixar `refreshDimensions` vazio][mfte-aoe-override] ou executar suas próprias queries. [`setRadius` nativo][aoe-radius] não garante que um literal de distância numa subclasse também mude. Separar alcance de aquisição, deslocamento, colisão e área terminal em cada ficha.

[`SpellDamageSource`][damage-source] carrega spell, entidade direta e causadora; ler esses campos na construção concreta. Fonte de summon pode apontar para o dono, para o mob ou para um caminho comum sem spell. Dano proposto, dano aceito, HP efetivo, heal direto, DOT, teleporte, reownership e summon são fases distintas. Correlacionar **cast pai/origem/owner/recast/entidade/vítima/fase/tick**, sem premiar VFX ou cada callback como outro cast e sem segunda aplicação de dano/mana/cooldown.

## Contratos atuais dos três projetos

O RPG foi consultado na `main` **`59ff2a0e827fd08faa603f4482f8104ac433383c`**. Seu [gate ArcaneAccess][rpg-gate] pode cancelar o pré-cast, com exceções explícitas para FakePlayer/COMMAND. O [listener LOWEST][rpg-cast] lê `SpellOnCastEvent` para Mastery: é ingresso de cast do host, anterior ao resultado da magia. A [política de origem][rpg-origin] limita as origens elegíveis; o [cálculo de Mastery][rpg-policy] descarta `procDepth > 0` e não autoriza prêmio por cada filho.

Há uma incompatibilidade de contrato a preservar: [`normalizeSchool`][rpg-normalize] produz **`iss_magicfromtheeast/symmetry`** e **`iss_magicfromtheeast/spirit`**. Porém [`MasteryLaneCatalog`][rpg-token] usa o token sem `/` no domínio Iron’s; [`ironsDiscipline`][rpg-lane] chega à [validação que rejeita esse caractere][rpg-validation]. Uma chamada Java isolada ao método da fonte atual confirmou `IllegalArgumentException` para ambas as strings. É prova do contrato do método, **não reprodução de falha no modpack**. Não declarar as lanes custom integradas, remover namespace ou inventar aliases `irons:symmetry`/`irons:spirit`; a integração segue **CONTRATO_CONDICIONAL** no projeto dono.

Enshrouded permanece em **`a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`**. Seu [adapter Iron’s][ens-adapter] reconhece nove damage IDs base; os IDs MFTE não estão nessa lista. O [classificador][ens-classifier] usa tags explícitas `enshrouded:magic` e `enshrouded:magic_bypass`; o [redutor único][ens-reducer] atua em `LivingDamageEvent.Pre` sob seus gates. A classificação concreta de um DamageType MFTE depende das tags/adapters efetivos. Nome de escola não concede autoridade sobre Shroud/exposure, nova resistência ou mutadores de cast/geometria.

Black Arcana mantém seu casting, rituais e política de mundo. MFTE/Iron’s mantêm execução, custos, entidades e cleanup; RPG mantém progressão, Mastery, perks e gates; Enshrouded mantém seus sistemas. `minecraft-mod-factory` continua referência de tooling futuro, sem dependência adicionada por esta documentação.

## Aceite ainda necessário

**PENDING:** equivalência dos campos/métodos não confrontados no JAR, config/datapacks efetivos, aquisição Survival, casts de origens alternativas, dedicated/client/multiplayer, PvP/claims/aliados/LOS, budgets, spawn recusado, owner ausente, unload/relog/restart, persistência/sync, reentrância e ausência de duplicação. Cada ficha lista casos pertinentes. CI Black Arcana não é teste das 22 magias carregadas no modpack. **+0 certificados estritos; nenhum Stage promovido.**

[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L10-L36
[host-version]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/gradle.properties#L7-L21
[schools]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESchoolRegistries.java#L32-L64
[attributes]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEAttributeRegistries.java#L27-L51
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L241
[host-formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L173
[cast-time]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L244-L257
[cast-soft-cap]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L177-L184
[config]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/configs/MFTEServerConfigs.java#L15-L45
[bootstrap]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/ISS_MagicFromTheEast.java#L35-L51
[metadata]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/META-INF/neoforge.mods.toml#L26-L47
[admission]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L298
[cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L305-L332
[base-oncast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L359-L367
[level-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/ModifySpellLevelEvent.java#L17-L70
[pre-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellPreCastEvent.java#L21-L49
[cast-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L20-L73
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L50
[damage-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[summon-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellSummonEvent.java#L7-L38
[cooldown-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellCooldownAddedEvent.java#L26-L55
[cooldown-manager]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L107
[heal-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellHealEvent.java#L18-L40
[heal-producer]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HealSpell.java#L63-L66
[projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L114
[projectile-travel]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L203-L213
[collision]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L200
[impact]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L361-L405
[aoe]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AoeEntity.java#L114-L149
[aoe-radius]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AoeEntity.java#L222-L243
[mfte-aoe-override]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/bagua_array/BaguaCircle.java#L63-L73
[damage-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L46-L51
[rpg-gate]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsSpellbookProgressionEvents.java#L26-L33
[rpg-cast]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsSpellbookProgressionEvents.java#L79-L94
[rpg-origin]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronMasterySourcePolicy.java#L3-L8
[rpg-policy]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryPolicies.java#L5-L12
[rpg-normalize]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/irons/IronsSpellbookProgressionEvents.java#L96-L100
[rpg-token]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L7-L11
[rpg-lane]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L82-L84
[rpg-validation]: https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/59ff2a0e827fd08faa603f4482f8104ac433383c/src/main/java/dev/gustavopere/rpgskilltree/core/MasteryLaneCatalog.java#L125-L129
[ens-adapter]: https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/integration/irons/IronsSpellbooksMagicAdapter.java#L20-L47
[ens-classifier]: https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/combat/magic/DefaultMagicDamageClassifier.java#L18-L36
[ens-reducer]: https://github.com/Gustavaopere/Enshrouded/blob/a41dbb51aacb94b7b5db6517f1514b0b7aee3e83/src/main/java/com/gustavaopere/enshrouded/combat/magic/MagicResistanceRuntime.java#L17-L68
