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

## Nova sonda — pendente de primeiro resultado

`docs/qa/alexscaves_1010_chocolate_effect_lifecycle_250_probe.py` projeta CONSTANT_Class dos operands de instanceof/checkcast/new e reusa os seis Code SHA observados, cinco hashes de classes e os pins dos quatro artefatos engine e do publisher. As declarações de métodos de lifecycle em LivingEntity/MobEffectInstance são descoberta por nome e descritor, não uma lista de APIs presumidas. A CI testa o projetor de operandos com casos válidos e inválidos e exige duas execuções com saída idêntica, sem fixar um hash inventado antes do primeiro run. O resultado novo e os tipos concretos ainda não foram observados.

Sem nova raiz, certificado, hook, QA física ou mudança de gameplay. Após o primeiro resultado, registrar relatório SHA-exato e completar os campos individuais com evidência, mantendo `NO_MUTATION`.
