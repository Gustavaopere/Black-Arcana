# Hot Chocolate Bottle — fusão de status, clamp nutricional e tipo do alvo de roubo

**DISCOVERY_ONLY / NO_MUTATION.** Complemento finito às PRs #1196, #1198 e #1199, sem dependência de seus arquivos ainda não integrados e sem alterar fichas/índices concorrentes. Publisher 1.0.10, Minecraft 1.21.1, Java 21, distribuição NeoForge 21.1.250. Modlist #019/#001. Cópia instalada e runtime transformado não observados.

## Evidência previamente produzida e agora relida

- [Run 45479066017, job 138746986320](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45479066017/job/138746986320): 113 registros SEMANTIC; relatório 647.857 bytes, SHA-256 `ac206f62678acd71876df7df3321eb16ee51832a15325515bf23db71bc566464`. O log individual registra os Code hashes abaixo.
- [Run 45478556000, job 138745194532](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45478556000/job/138745194532): relatório 1.668.053 bytes, SHA-256 `dd8562887a4740769ec09db6e19d5336a77b9e710d8f125f9eea2a9b12d74314`. Censo publisher e gate de seleção de alvo.

| Método | Code SHA-256 | Resultado delimitado |
|---|---|---|
| FoodData.add(IF)V | `9742a98e4b36cc8bd77a34ce66dca114f66af0208986f179e7db9e212109c7e2` | foodLevel = clamp(foodLevel + nutrition, 0, 20), clamp @10 e escrita @13; saturationLevel = clamp(saturationLevel + saturation, 0F, (float)foodLevel atualizado), clamp @29 e escrita @32. |
| LivingEntity.addEffect(instance,source) | `612bacd43ba4d0a5e2d94df479997582ccc4d2306a14ebbd65c6daa80c400776` | Admissão @3; procura status ativo @19; publica Added @45 antes de ramificar inserção/atualização. Inserção @64, update @89, callback onEffectUpdated @99 somente no ramo verdadeiro; onEffectStarted @107 após a junção. |
| MobEffectInstance.update(instance) | `3a78f4d49785b4657224cc5410bac4642e29b844a26ddfc37a36641a42dde3bf` | Compara amplifier @29/33; maior amplifier substitui o ativo e pode guardar cópia hiddenEffect se a duração recebida for menor. Mesmo amplifier com duração recebida maior substitui duração @117, não soma. Amplifier inferior e duração maior alimentam hiddenEffect @141 ou update recursivo @152. Flags ambient, visible e showIcon também podem mudar. |
| MobEffectInstance.isShorterDurationThan(instance) | `32afcd883827d50f6b9a79172c6a7e3e18ef78fb77049d9f272ac833e27c2205` | Duração infinita tem tratamento especial; não ordenar -1 como duração finita menor. |
| GingerbreadManStealGoal.canStealFromEntityType(Entity) | `45bb21045d88050e186e94235feab21fe14af050e19ffe608f77cdbb9da034f8` | Player criativo rejeitado, segundo teste instanceof @22 sem tipo projetado no relatório anterior. Não assumir qual é o tipo até nova inspeção tipada. |
| ACPlatform$ItemHandlerAccess.takeOne(I)ItemStack | `25727ad1b559496542bd46c92d9b51c2bbe0c3bbed5aca1df3bb69f0a99bbf2c` | extractItem(slot,1,false) do handler; não prova débito ou conservação. |

## Implicações para perks

Sugar Rush de 200 ticks e p=0,02 são pedidos nativos. Mesmo quando admitido, o efeito ativo não deve ser tratado como um timer que sempre recebe +200 ticks. Um perk de duração/amplifier precisa preservar a política de fusão e os efeitos ocultos; um listener Added não é um recibo de aplicação ou mudança de intensidade. Nutrição e saturação são limitadas separadamente: a saturação nominal 2 não é necessariamente o ganho líquido, e a nutrição nominal 4 não é cura. Não multiplicar globalmente ACFoods para um jogador. Não premiar Mastery por chance sorteada, evento publicado ou tentativa de extração.

## Nova sonda — resultado distribuído observado

`docs/qa/alexscaves_1010_chocolate_effect_lifecycle_250_probe.py` projeta CONSTANT_Class dos operands de instanceof/checkcast/new e reusa os seis Code SHA observados, cinco hashes de classes e os pins dos quatro artefatos engine e do publisher. As declarações de métodos de lifecycle em LivingEntity/MobEffectInstance são descoberta por nome e descritor, não uma lista de APIs presumidas. A CI testa o projetor de operandos com casos válidos e inválidos e exige duas execuções com saída idêntica, sem fixar um hash inventado antes do primeiro run. Primeira execução e replay concluídos conforme selo abaixo.

Sem nova raiz, certificado, hook, QA física ou mudança de gameplay. Após a CI do HEAD com o selo fixado, integrar os campos individuais mantendo `NO_MUTATION`.

## Resultado SHA-exato — run 45513909141

[Run 45513909141, job 138868305918](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45513909141/job/138868305918), HEAD observacional `fbe9ca1735c1e34bced9fc0993f5575d0760b54d`: oito checks do projetor/política aprovados; **15 projeções de método em cinco classes**, relatório **161.640 bytes**, SHA-256 `806e5a412cbaed9ef76a9ddff774af5fc9ed3736c0a21b2b6abbf07745a12c21`. O replay em segunda execução reproduziu o mesmo tamanho e hash, e o job concluiu success. Este commit fixa também o hash e o tamanho no workflow; a CI deste novo HEAD ainda não foi observada.

### Filtro de roubo resolvido

`GingerbreadManStealGoal.canStealFromEntityType`: CONSTANT_Class CP#230 @1 instanceof Player e @8 checkcast Player; isCreative @13, guarda @16 e false @19–20. CONSTANT_Class CP#40 @22 identifica **GingerbreadManEntity**, não um tipo genérico de mob: ifne @25 leva a false @32; demais tipos retornam true neste filtro isolado. O filtro não certifica consentimento, autorização de claim, presença de capability, seleção de slot, extração aceita ou perda de chocolate.

### Ciclo de vida e consumidores da engine

| Método | Code SHA-256 | Pivôs |
|---|---|---|
| MobEffectInstance.isInfiniteDuration()Z | `5805732b774db96f0d35ecd33aac6a247d5b8d0a0d2ea107909b648fb576e01b` | duration @1 comparado a -1 @4; sentinela exata, distinta de zero. |
| MobEffectInstance.hasRemainingDuration()Z | `eea3e81e9684ca035b4386f5c3b419f792b714eac9357e87a58b81a641bc1da6` | Infinito ou duração >0. |
| MobEffectInstance.mapDuration(Int2IntFunction)I | `390c7dbad2ec90facdf75722149dd72f8df8134f1ac7aba619dc801842710ae3` | Infinito ou zero conservados; demais valores passam por applyAsInt @19. |
| MobEffectInstance.tickDownDuration()I | `caee198e71dd209819f6a000ca9c78378174b674fb7a6d3f8fbc1ab9e44241c2` | Recursão hiddenEffect.tickDownDuration @11 antes de mapDuration @22 e escrita @26; handle bootstrap #4 lambda$tickDownDuration$3(I)I. O corpo da lambda não pertence a este recorte. |
| MobEffectInstance.tick(LivingEntity,Runnable)Z | `4a9bfe8ef97ab026e65c3ad8eb95e5c3e859c5f49ce2fe25909758590b989b25` | hasRemainingDuration @1; infinito usa tickCount da entidade, finito usa duration; shouldApplyEffectTickThisTick @43, applyEffectTick @66. Retorno falso do apply pede removeEffect @77. tickDownDuration @82; duration zero e hiddenEffect presente levam a setDetailsFrom @105, avanço da cadeia @116 e Runnable.run @120. Retorna hasRemainingDuration @134. |
| LivingEntity.tickEffects()V | `eb89bbcb6f653042c852647a19d1ae918479668c56bc8dbb70719391cc247d00` | Itera activeEffects, chama tick @57. Retorno falso, lado servidor: posta MobEffectEvent.Expired @85, consulta isCanceled @93; só ramo não cancelado remove do iterador @100 e chama onEffectRemoved @107. Retorno verdadeiro pode pedir onEffectUpdated @128 quando duration % 600 == 0, com booleano false. Handle do Runnable: lambda$tickEffects$3, não projeta corpo. |
| LivingEntity.onEffectUpdated(MobEffectInstance,Z,Entity)V | `c00bf61d16442c9b246f21be0c507edcedfb1305a6d173c06c4bb7cc64d4f2cb` | Marca effectsDirty @2. Booleano true e servidor: removeAttributeModifiers @39, addAttributeModifiers com amplifier @52 e refreshDirtyAttributes @56. Servidor envia efeito a passageiros @71. Não deduzir alteração quantitativa sem o efeito próprio e atributos efetivos. |

As instâncias ocultas não devem ser tratadas como fila de timers congelados: o corpo de tickDownDuration as visita recursivamente antes de mapear a duração ativa. O callback Expired cancelado pode impedir a remoção pelo iterador, sem provar duração renovada, bônus ou um tick ativo. Para perks, separar tentativa, admissão, atualização real, expiração e modificação de atributos. Não usar eventos de sincronização/apresentação como autoridade de Mastery.

Limites adicionais: corpos das duas lambdas, setDetailsFrom, callbacks de efeito externo, capability real, listeners efetivos e runtime transformado não fechados. Este relatório não certifica integralmente Hot Chocolate Bottle, Sugar Rush ou os mobs; reuso para Ink Bombs deve preservar identidade/owner e não promove certificado. `NO_MUTATION`, `NOT_CERTIFIED`, `NOT_TESTED`.
