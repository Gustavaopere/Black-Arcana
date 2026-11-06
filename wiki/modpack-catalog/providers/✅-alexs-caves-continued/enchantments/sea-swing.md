# Sea Swing — onda corpo a corpo da Ortholance (Alex's Caves Continued 1.0.10)

**Estado: ⚠️ ficha individual parcial/condicionada.** O JAR publisher exato confirma identidade, JSON, classes e produtor de uma onda, mas o controle de fluxo e a integração mutadora não foram integralmente certificados. Situação independente: mutating_hook=NOT_VERIFIED, physical_qa=NOT_TESTED, perk_certification=NOT_CERTIFIED, mutation=NO_MUTATION.

## Identidade e proveniência verificadas

| Campo | Evidência do JAR físico 1.0.10 |
|---|---|
| Provider / mod ID | Alex's Caves Continued / alexscaves |
| Plataforma | Minecraft 1.21.1, NeoForge, Java 21 |
| Arquivo | alexscaves-1.0.10-neoforge+1.21.1.jar; 75.279.314 bytes |
| Fingerprint | SHA-1: 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570; SHA-256: 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c |
| Enchantment | alexscaves:sea_swing; campo compilado ACEnchantmentRegistry.SEA_SWING |
| JSON exato | data/alexscaves/enchantment/sea_swing.json, 360 bytes, SHA-256 f5e7985f7941b02a47966fa1135f3fc3ceff05b60d9eee015cbb6b33c7eb9c3a |
| Item/tag | #alexscaves:enchantable/ortholance, contendo alexscaves:ortholance no JAR |
| Produtor | OrtholanceItem.acHurtEnemy(ItemStack, LivingEntity, LivingEntity):boolean; 49 instruções |
| Wrapper | OrtholanceItem.hurtEnemy(ItemStack, LivingEntity, LivingEntity):boolean; 6 instruções |
| Consumidores | WaveEntity.tick():void (318 instruções); WaveEntity.attackEntities(float):void (81 instruções) |

A [sonda read-only](../../../../../docs/qa/alexscaves_1010_sea_swing_probe.py), os [testes de regressão](../../../../../docs/qa/alexscaves_1010_sea_swing_probe_test.py) e o [workflow SHA-exato](../../../../../.github/workflows/alexscaves-1010-sea-swing.yml) confrontam o JAR 1.0.10 e os SHA-256 das três classes com o [inventário anterior de Flinging](../EXACT-FLINGING-1.0.10.json). As janelas JVM e o recurso JSON estão congelados no [manifesto exato](../EXACT-SEA-SWING-DISCOVERY-1.0.10.json), comparado via --seal em CI. O manifesto é evidência de interoperabilidade: não distribui o JAR nem afirma CFG integral ou QA física.

A árvore [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara versão **1.1.1**. Ela auxilia a encontrar consumidores, mas **não é** a autoridade dos parâmetros instalados da versão 1.0.10. Todos os valores citados apenas dessa fonte ficam identificados como hipóteses.

## JSON publisher — valores exatos

| Propriedade | Valor |
|---|---|
| description.translate | enchantment.alexscaves.sea_swing |
| supported_items | #alexscaves:enchantable/ortholance |
| weight | 2 |
| max_level | 1 |
| min_cost | base=1, per_level_above_first=10 |
| max_cost | base=41, per_level_above_first=10 |
| anvil_cost | 4 |
| slots | mainhand |
| exclusive_set | Não declarado no recurso |

Weight e os custos acima são metadados de aquisição/encantamento: não são chance de acerto, dano, mana, cooldown ou custo por onda. O nível máximo I é declarativo; regras efetivas alteradas por datapacks não foram testadas.

## Produtor e comportamento identificado

**Produtor SHA-exato:** o método acHurtEnemy (49 instruções; digest JVM 7da3fd607d1275f0410f54f3bc713ae1242dd13ba33fb1e78d5d942a05a62c93) solicita ACCompat.hurtAndBreak(stack, 1, atacante, MAINHAND) **antes** de verificar Sea Swing (@0–6). Assim, um ponto de desgaste é solicitado pelo ataque da arma, não como custo adicional do encantamento. Obtém o vetor de visão do atacante com argumento 1.0F (@9–14). Lê ACEnchantmentRegistry.SEA_SWING em ACCompat.enchantLevel (@17–20), e o guard ifle @23 salta a @97 se o nível for zero ou negativo. **Não existe clamp do nível no método observado**; para níveis positivos, o efeito abaixo não escala numericamente com L. O método pertence ao callback de ataque do item, distinto do releaseUsing que resolve carga e ondas de lançamento.

No ramo de nível positivo, constrói WaveEntity(hurt.level(), atacante) (@26–35), coloca a onda na posição **(atacante.x, alvoAtingido.y, atacante.z)** (@40–54), solicita **lifespan 5** (@57–60) e yaw igual a **-atan2(view.x, view.z) × 57.2957763671875** (@63–84). Pede player.level().addFreshEntity(wave) em @87–93; o retorno booleano é descartado (@96). Não existe guarda explícita isClientSide neste método compilado; isso não prova spawn duplicado ou física real client/server, e exige verificação em runtime. O método retorna true tanto no ramo não encantado quanto após a tentativa de onda (@97–98).

**Distinção causal:** a entidade atingida no callback define a **altura inicial da onda**, não é automaticamente a única vítima de sua área posterior. O ataque original, o pedido de spawn e os danos subsequentes da WaveEntity são fases distintas de um único evento nativo; não devem gerar três casts, três custos ou três procs atribuídos pelo Black Arcana.

**Consumidor SHA-exato:** WaveEntity.attackEntities(float) (81 instruções; digest f7d6b5c19cec219a1cbfa24ada582b81631528236fd459af40aa8e41196cb6e8) consulta uma **AABB própria inflada por (0.5D,0.5D,0.5D)** (@0–16), enumera LivingEntity e compõe DamageSource **mobProjectile(onda, campo owner)** (@17–40). Os filtros compilados excluem alvos aliados à onda, DeepOneBaseEntity e, caso owner não seja null, o próprio owner e aliados do owner (@69–117). Para candidato elegível, solicita **hurt(source, scale+1F)** (@117–126), **descarta o resultado** e na sequência chama setSlamming(true) (@127–129) e ACCompat.knockback com magnitude **0.1D + 0.5D × scale** e direção baseada em sin/cos do yaw (@132–169). A magnitude é argumento solicitado, não deslocamento/resultado de knockback certificado. Um resultado de hurt falso não bloqueia esses callsites posteriores.

**Tick SHA-exato:** WaveEntity.tick (318 instruções; digest d018fb4b1c90bd6104a52f875e097b9ef3818e36d038045f3668d75c6e120765) decrementa getWaitingTicks no servidor quando positivo, oculta e retorna até encerrar essa espera (@12–44). O ramo selecionado calcula o argumento de attackEntities como **2 × getSlamAmount(1F) + 1 + getWaveScale** (@518–527). Portanto, a solicitação bruta do método de dano é **2 × getSlamAmount(1F) + 2 + getWaveScale**, não DPS nem acerto comprovado. O movimento observado aplica gravidade condicional aproximadamente -0.04, arrasto 0.9 antes do move e multiplicador (0.99,0.98,0.99) após mover (@105–132, @530–567). O contador activeWaveTicks maior que lifespan ou a combinação activeWaveTicks>10 e movimento horizontal <0.04 chama setSlamming(true) (@570–606); descarte posterior aparece em @101–102. O lifecycle total, owner após reload e efeitos em dimensões/chunks não foram validados em jogo.

A fonte adjacente 1.1.1 confirma que o mesmo conceito de onda existe nessa árvore, mas **todos os números e offsets acima foram extraídos das janelas exatas do JAR 1.0.10**, não transpostos da 1.1.1. Restam sem certificação: o CFG completo de tick (p.ex. todos os ramos de cancelamento), condições efetivas de eventos externos, damage modifiers, retorno de spawn, atributos dimensionais e comportamento físico.

## Matriz de integração para perks

| Eixo | Contrato observado | Limite de autoridade |
|---|---|---|
| Trigger / alvo | Ataque do item com duas LivingEntity e enchantLevel | Não transformar em novo cast, evitar contabilizar hit e onda como raízes separadas |
| Quantidade | Um pedido de addFreshEntity após nível positivo; retorno booleano descartado | Não inferir inserção aceita, um hit garantido, múltiplos procs ou spawn sem duplicações de rede |
| Duração, direção, posição | Lifespan solicitado 5; origem atacante.x / alvo.y / atacante.z; yaw via atan2 | Duração final em mundo, colisões, dimensão e comportamento cliente/servidor não testados |
| Dano / tipo | mobProjectile(onda, owner); dano solicitado 2 × slamAmount(1F) + 2 + waveScale | Não é dano aceito, DPS, crítico, dano elemental nem base fixa; não reaplicar hurt |
| Alcance / área | AABB própria inflada 0.5 por eixo em ataque da onda | Não é raio de alcance da Ortholance nem prova de todos os acertos; dimensões e movimento dinâmicos |
| Knockback | Solicita 0.1 + 0.5 × scale após hurt, mesmo quando resultado do hurt é false | Não transformar em deslocamento garantido, nem reexecutar knockback em outro pipeline |
| Custos | Ataque solicita 1 de desgaste MAINHAND antes do teste de enchantLevel | Não cobrar a cada onda/tick/hit; sucesso do desconto e modos criativos não testados |
| Persistência | Métodos próprios de NBT e descarte localizados | Examinar estado realmente gravado, limpeza e owner após reload |
| Hooks mutadores | NOT_VERIFIED | ⛔ fail-closed; nenhuma alteração de parâmetros, spawn ou dano autorizada |

Sea Swing é settlement nativo da Ortholance. O Black Arcana continua autoridade do seu próprio runtime, enquanto o RPG Skill Tree pode fornecer progressão/perks apenas por boundaries reais. Nenhuma bridge, hook, classe compilada, evento, nova mana ou gameplay foi implementado.

## Pendências para certificação estática e execução

Fechar o CFG do produtor, guardas de lado servidor, constantes 1.0.10, e o caminho de WaveEntity com targeting, caixa de colisão, dano, knockback, escala, ciclos, NBT, owner e descarte. Verificar compatibilidade com outros encantamentos e regras de datapack. QA real deverá cobrir cliente/servidor, PvP, dano negado, bloqueio de spawn, perda do owner, reload e proteção de mundo. **O índice individual permanece ⚠️ e não eleva o numerador de contratos estáticos certificados até essa evidência existir.**
