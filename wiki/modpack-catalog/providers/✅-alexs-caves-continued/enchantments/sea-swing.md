# Sea Swing — onda corpo a corpo da Ortholance (Alex's Caves Continued 1.0.10)

**Estado: ✅ contrato técnico estático individual concluído no escopo delimitado.** JAR publisher 1.0.10: identidade, localização, produtor, construtores, targeting, parâmetros, movimento, dano solicitado, custo, NBT e descarte têm prova nos métodos completos selecionados. **Não é autorização de perk mutadora ou QA em jogo.** `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `mutation=NO_MUTATION`.

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

A árvore [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara versão **1.1.1**, usada só como corroboração. O símbolo `getStepHeight`, presente naquela fonte, não foi encontrado como método próprio no classfile 1.0.10 e não integra o contrato exato.

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

Weight e custos acima são metadados do encantamento: não são chance de acerto, dano, mana, cooldown ou custo por onda. O máximo I é declarativo; datapacks não foram testados. A descrição do arquivo `assets/alexscaves/lang/en_us.json` do **JAR 1.0.10** (SHA-256 `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f`) é parafraseada assim: **o ataque com a Ortholance produz uma onda à frente do atacante**. Não há cópia literal do texto do provider.

## Produtor e comportamento identificado

**Produtor SHA-exato:** o método acHurtEnemy (49 instruções; digest JVM 7da3fd607d1275f0410f54f3bc713ae1242dd13ba33fb1e78d5d942a05a62c93) solicita ACCompat.hurtAndBreak(stack, 1, atacante, MAINHAND) **antes** de verificar Sea Swing (@0–6). Assim, um ponto de desgaste é solicitado pelo ataque da arma, não como custo adicional do encantamento. Obtém o vetor de visão do atacante com argumento 1.0F (@9–14). Lê ACEnchantmentRegistry.SEA_SWING em ACCompat.enchantLevel (@17–20), e o guard ifle @23 salta a @97 se o nível for zero ou negativo. **Não existe clamp do nível no método observado**; para níveis positivos, o efeito abaixo não escala numericamente com L. O método pertence ao callback de ataque do item, distinto do releaseUsing que resolve carga e ondas de lançamento.

No ramo de nível positivo, constrói WaveEntity(hurt.level(), atacante) (@26–35), coloca a onda na posição **(atacante.x, alvoAtingido.y, atacante.z)** (@40–54), solicita **lifespan 5** (@57–60) e yaw igual a **-atan2(view.x, view.z) × 57.2957763671875** (@63–84). Pede player.level().addFreshEntity(wave) em @87–93; o retorno booleano é descartado (@96). Não existe guarda explícita isClientSide neste método compilado; isso não prova spawn duplicado ou física real client/server, e exige verificação em runtime. O método retorna true tanto no ramo não encantado quanto após a tentativa de onda (@97–98).

**Distinção causal:** a entidade atingida no callback define a **altura inicial da onda**, não é automaticamente a única vítima de sua área posterior. O ataque original, o pedido de spawn e os danos subsequentes da WaveEntity são fases distintas de um único evento nativo; não devem gerar três casts, três custos ou três procs atribuídos pelo Black Arcana.

**Consumidor SHA-exato:** WaveEntity.attackEntities(float) (81 instruções; digest f7d6b5c19cec219a1cbfa24ada582b81631528236fd459af40aa8e41196cb6e8) consulta uma **AABB própria inflada por (0.5D,0.5D,0.5D)** (@0–16), enumera LivingEntity e compõe DamageSource **mobProjectile(onda, campo owner)** (@17–40). Os filtros compilados excluem alvos aliados à onda, DeepOneBaseEntity e, caso owner não seja null, o próprio owner e aliados do owner (@69–117). Para candidato elegível, solicita **hurt(source, scale+1F)** (@117–126), **descarta o resultado** e na sequência chama setSlamming(true) (@127–129) e ACCompat.knockback com magnitude **0.1D + 0.5D × scale** e direção baseada em sin/cos do yaw (@132–169). A magnitude é argumento solicitado, não deslocamento/resultado de knockback certificado. Um resultado de hurt falso não bloqueia esses callsites posteriores.

**Tick SHA-exato:** WaveEntity.tick (318 instruções; digest d018fb4b1c90bd6104a52f875e097b9ef3818e36d038045f3668d75c6e120765) decrementa getWaitingTicks no servidor quando positivo, oculta e retorna até encerrar essa espera (@12–44). O ramo selecionado calcula o argumento de attackEntities como **2 × getSlamAmount(1F) + 1 + getWaveScale** (@518–527). Portanto, a solicitação bruta do método de dano é **2 × getSlamAmount(1F) + 2 + getWaveScale**, não DPS nem acerto comprovado. O movimento observado aplica gravidade condicional aproximadamente -0.04, arrasto 0.9 antes do move e multiplicador (0.99,0.98,0.99) após mover (@105–132, @530–567). O contador activeWaveTicks maior que lifespan ou a combinação activeWaveTicks>10 e movimento horizontal <0.04 chama setSlamming(true) (@570–606); descarte posterior aparece em @101–102. O lifecycle total, owner após reload e efeitos em dimensões/chunks não foram validados em jogo.

O [manifesto estático fechado](../EXACT-SEA-SWING-STATIC-1.0.10.json), a [sonda](../../../../../docs/qa/alexscaves_1010_sea_swing_static_probe.py) e o [workflow --seal](../../../../../.github/workflows/alexscaves-1010-sea-swing-static.yml) ampliam a descoberta: auditam **20 métodos próprios completos** e os dois construtores, confrontam hashes e janelas anteriores e selam texto de localização. A validação de métodos da entidade não equivale à implementação integral de Minecraft/ACCompat, nem a testes de eventos externos, dano efetivo, spawn, claims ou física.

## Evidência aprofundada — estado, autoria, dano e ciclo de vida

**Construtor e autoria (JAR 1.0.10).** WaveEntity(Level, LivingEntity) acessa ACEntityRegistry.WAVE, encadeia com o construtor (EntityType, Level) e chama setOwner(LivingEntity) no offset 18. O setter grava o objeto no campo owner e o UUID em ownerUUID. Portanto, a autoria inicial é atribuída à entidade passada pelo produtor, não presumida pela existência do parâmetro.

**Defaults e geometria.** defineSynchedData inicia SLAMMING=false, LIFESPAN=10, WAITING_TICKS=0, Y_ROT=0F e WAVE_SCALE=1F. Sea Swing sobrescreve LIFESPAN para 5 e o yaw; não sobrescreve escala ou espera nesse produtor. getDimensions(Pose) escala as dimensões básicas por WAVE_SCALE; onSyncedDataUpdated atualiza as dimensões se a escala mudar. A região de dano é a AABB dinâmica da onda inflada 0,5D por eixo, não uma esfera com raio fixo e tampouco o alcance da Ortholance.

**Fórmulas que a perk precisará respeitar.** getSlamAmount(partialTicks) = (prevSlamProgress + (slamProgress - prevSlamProgress) × partialTicks) × 0,1F. O tick passa partialTicks=1F, calcula S = 2 × getSlamAmount(1F) + 1 + waveScale; attackEntities solicita hurt com S + 1 e knockback com 0,1 + 0,5 × S. Com waveScale inicial 1, o pedido bruto de dano é 3 + 0,2 × slamProgress. O resultado de hurt é descartado antes de setSlamming e knockback, e nenhum desses valores prova dano ou empurrão efetivamente aplicado.

**Tempo e lado de execução.** WAITING_TICKS positivo retorna cedo: seu contador só é decrementado no servidor. attackEntities é chamado no caminho não cliente do tick (@503–530) antes do movimento de cada atualização. activeWaveTicks incrementa ao final (@609–616); quando excede LIFESPAN ou, depois de 10 ticks, a velocidade horizontal é inferior a 0,04, pede setSlamming(true). SlamProgress cresce até 10 e então tick solicita discard, sem retorno imediatamente após a chamada. Logo, LIFESPAN=5 não é descarte comprovado no quinto tick. O producer acHurtEnemy não possui guarda explícita própria isClientSide: o comportamento completo depende de quem chama o callback e da execução real.

**NBT e perda de owner.** addAdditionalSaveData grava Owner (UUID, somente se existente) e Lifespan; readAdditionalSaveData reconstitui apenas esses dois próprios campos. Os métodos não registram SLAMMING, WAITING_TICKS, WAVE_SCALE, activeWaveTicks ou referência direta owner. getOwner pode resolver ownerUUID via ServerLevel.getEntity(UUID), mas attackEntities lê diretamente o campo owner, sem invocar getOwner. Após reload, a autoria no pedido de dano e as exclusões de aliados dependem de que algum consumidor tenha resolvido owner antes; isso não foi demonstrado como automático. O Black Arcana não deve deduzir crédito de Mastery/kill da existência do UUID NBT.

**Fronteiras de interoperabilidade.** São 8 raízes sobrenaturais do inventário do provider, inalteradas: Sea Swing modifica o ataque da arma e seu settlement, não acrescenta raiz de magia deliberada. O provider controla spawn, hit, dano, custo, movimentação, NBT e sincronização. RPG Skill Tree somente poderá oferecer perks após boundary/hook mutador real; sem tal contrato, NO_MUTATION e anti-duplicação são obrigatórios.

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
| Persistência | NBT próprio grava UUID Owner se existente e Lifespan; getOwner resolve ownerUUID no ServerLevel | attackEntities usa campo owner direto, sem getOwner: não presumir owner reidratado após reload sem outro consumidor |
| Hooks mutadores | NOT_VERIFIED | ⛔ fail-closed; nenhuma alteração de parâmetros, spawn ou dano autorizada |

Sea Swing é settlement nativo da Ortholance. O Black Arcana continua autoridade do seu próprio runtime, enquanto o RPG Skill Tree pode fornecer progressão/perks apenas por boundaries reais. Nenhuma bridge, hook, classe compilada, evento, nova mana ou gameplay foi implementado.

## Limites do certificado estático e QA pendente

**✅ O contrato estático individual está concluído no recorte exato e reproduzível; a execução não.** O produtor não apresenta guarda própria isClientSide; WaveEntity.tick condiciona seu ataque ao servidor. Não inferir spawn protegido, sucesso de hurt, crédito de kill/XP, hook, modificação segura ou política PvP/claims. QA físico ainda deve cobrir cliente e servidor, dano negado, spawn recusado, PvP, world protection, alterações por datapack, reload de owner, cooldown, colisões, logout e interação com outros mods. A autoridade do runtime e os limites de Black Arcana/RPG Skill Tree permanecem inalterados.
