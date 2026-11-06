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

A [sonda read-only](../../../../../docs/qa/alexscaves_1010_sea_swing_probe.py), os [testes de regressão](../../../../../docs/qa/alexscaves_1010_sea_swing_probe_test.py) e o [workflow SHA-exato](../../../../../.github/workflows/alexscaves-1010-sea-swing.yml) confrontam o JAR 1.0.10 e os SHA-256 das três classes com o [inventário anterior de Flinging](../EXACT-FLINGING-1.0.10.json). A extração é restrita a janelas JVM, sem transferência de código de terceiros.

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

A descoberta SHA-exata localizou no mesmo método compilado acHurtEnemy: uma referência a SEA_SWING, uma consulta ACCompat.enchantLevel, uma solicitação ACCompat.hurtAndBreak e chamadas únicas a setPos, setLifespan, setYRot e Level.addFreshEntity. O método pertence ao callback de **ataque corpo a corpo da Ortholance**, distinto de releaseUsing, que resolve carga e ondas do lançamento. A mera presença de um callsite não prova que o ramo seja percorrido sempre, nem que addFreshEntity retorne sucesso.

Na fonte **adjacente 1.1.1**, um nível positivo seleciona criação de WaveEntity com owner atacante, posição horizontal do atacante e altura do alvo atingido; solicita lifespan de 5 e yaw conforme o vetor de visão. O mesmo método pede um ponto de durabilidade. **Essas constantes, posição e custo precisam de confirmação direta do bytecode 1.0.10 antes de serem promovidas à prova exata.** Nesse recorte-fonte o método não possui um teste explícito próprio de lado servidor; isso não comprova duplicação ou autoridade do runtime instalado.

O binário 1.0.10 confirma em WaveEntity.tick referências a attackEntities, getLifespan, getWaitingTicks, discard e setDeltaMovement. O consumidor attackEntities contém getEntitiesOfClass, mobProjectile, hurt, knockback, isAlliedTo e getBoundingBox. As janelas não encerram integralmente AABB, ordem de efeitos, retorno do dano, ownership, política de alvos, persistência nem os cálculos de knockback.

Na fonte **adjacente 1.1.1**, o dano é solicitado com fonte mobProjectile(this, owner) e a área usa a AABB própria inflada; há exclusões para aliados e Deep Ones. A chamada de hurt não equivale à confirmação de dano aceito. Os detalhes acima são *pistas de investigação*, não parâmetros numéricos já certificados do JAR 1.0.10.

## Matriz de integração para perks

| Eixo | Contrato observado | Limite de autoridade |
|---|---|---|
| Trigger / alvo | Ataque do item com duas LivingEntity e enchantLevel | Não transformar em novo cast, evitar contabilizar hit e onda como raízes separadas |
| Quantidade | Produtor solicita addFreshEntity no ramo Sea Swing | Não inferir inserção aceita, uma onda sempre ou número de danos |
| Duração, direção, posição | Chamadas compiladas setLifespan / setYRot / setPos | Valor, lifecycle, geometria e lado lógico ainda pendentes |
| Dano / tipo | WaveEntity usa mobProjectile e hurt | Sem DPS, dano efetivo nem reembolso de custos comprovados; não aplicar segundo hurt |
| Alcance / área | WaveEntity consulta getBoundingBox e getEntitiesOfClass | Não reinterpretar box como raio ou alcance de cast; escala exata ainda pendente |
| Knockback | WaveEntity possui chamada knockback | Magnitude, condições, causalidade e proteção ainda não certificados |
| Custos | Callsite hurtAndBreak no ataque; JSON de encantamento fechado | Não inserir custo próprio ou duplicar desgaste |
| Persistência | Métodos próprios de NBT e descarte localizados | Examinar estado realmente gravado, limpeza e owner após reload |
| Hooks mutadores | NOT_VERIFIED | ⛔ fail-closed; nenhuma alteração de parâmetros, spawn ou dano autorizada |

Sea Swing é settlement nativo da Ortholance. O Black Arcana continua autoridade do seu próprio runtime, enquanto o RPG Skill Tree pode fornecer progressão/perks apenas por boundaries reais. Nenhuma bridge, hook, classe compilada, evento, nova mana ou gameplay foi implementado.

## Pendências para certificação estática e execução

Fechar o CFG do produtor, guardas de lado servidor, constantes 1.0.10, e o caminho de WaveEntity com targeting, caixa de colisão, dano, knockback, escala, ciclos, NBT, owner e descarte. Verificar compatibilidade com outros encantamentos e regras de datapack. QA real deverá cobrir cliente/servidor, PvP, dano negado, bloqueio de spawn, perda do owner, reload e proteção de mundo. **O índice individual permanece ⚠️ e não eleva o numerador de contratos estáticos certificados até essa evidência existir.**
