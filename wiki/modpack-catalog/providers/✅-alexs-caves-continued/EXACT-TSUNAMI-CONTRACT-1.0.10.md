# Tsunami 1.0.10 — contrato individual SHA-exato

A [ficha individual](enchantments/tsunami.md) conclui somente `alexscaves:tsunami` como **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. O [manifesto individual](EXACT-TSUNAMI-CONTRACT-1.0.10.json) sela identidade, reader positivo no release, tentativa de onda única e superfícies nativas selecionadas; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, **`NO_MUTATION`**. `OrtholanceItem.releaseUsing`, `WaveEntity.tick` e os três `<clinit>` de registro permanecem **PARTIAL**. A arma integral, os encantamentos irmãos, a aceitação de spawn/dano, a física e a persistência efetiva conservam seus limites. Tsunami acrescenta **zero raízes mágicas** às oito existentes: emissão, ataque direto, onda e movimento do usuário são fases nativas da ação de Ortholance, sem novo cast.

A autoridade física é o publisher CurseForge projeto `1645389`, arquivo `8856293`, `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 **`36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`**. O TOML empacotado declara `alexscaves` **1.0.10**. A fonte pública [`Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e é corroboração adjacente, sem prova de paridade de build. Os parâmetros certificados vêm do JAR publisher 1.0.10, para Minecraft 1.21.1 / NeoForge / Java 21.

O recorte contém **1 ficha, 6 classes, 11 recursos, 51 métodos e 901 âncoras**: **46 corpos completos / 524 instruções** e **cinco métodos delimitados / 377 âncoras**. As classes são `OrtholanceItem`, `WaveEntity`, `ACCompat`, `ACEnchantmentRegistry`, `ACItemRegistry` e `ACEntityRegistry`, sob `com/github/alexmodguy/alexscaves/`. Os recursos são TOML, idiomas `en_us`/`pt_br`, JSONs Tsunami e Second Wave, tag Ortholance, loot de barter e quatro tags de aquisição. A seleção não promove contratos integrais das classes compartilhadas.

| Artefato local selado | Bytes | SHA-256 |
|---|---:|---|
| [`enchantments/tsunami.md`](enchantments/tsunami.md) | 23.375 | `a24941756d818a0e04d68f1664c81120d6ccf7980615178dcdddbd1fe98517e6` |
| [`EXACT-TSUNAMI-CONTRACT-1.0.10.json`](EXACT-TSUNAMI-CONTRACT-1.0.10.json) | 177.013 | `748e78f92ab0da6fdca2a33f01ce6626bbbbb0a2dd23f2ffa4feb5c47fb9b1f2` |

Os hashes abaixo identificam as entradas completas do JAR; a contagem de métodos e âncoras identifica somente o recorte selado. Os caminhos de classe partem de `com/github/alexmodguy/alexscaves/`.

| Classfile | Métodos | Âncoras | SHA-256 da entrada completa |
|---|---:|---:|---|
| `server/item/OrtholanceItem.class` | 9 | 275 | `996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09` |
| `server/entity/item/WaveEntity.class` | 23 | 485 | `93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e` |
| `server/misc/ACCompat.class` | 13 | 97 | `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b` |
| `server/enchantment/ACEnchantmentRegistry.class` | 2 | 9 | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |
| `server/item/ACItemRegistry.class` | 2 | 16 | `114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1` |
| `server/entity/ACEntityRegistry.class` | 2 | 19 | `7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072` |
| **Total selecionado** | **51** | **901** | — |

| Recurso empacotado | Bytes | SHA-256 da entrada completa |
|---|---:|---|
| `META-INF/neoforge.mods.toml` | 1.066 | `54dfb8cdba886fd5ef8e64d2a51c487ce4bf2400995884937ee5fd6d89df68fa` |
| `assets/alexscaves/lang/en_us.json` | 121.372 | `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f` |
| `assets/alexscaves/lang/pt_br.json` | 84.238 | `080bfaf05b6d710383579dfd0d3c01443f9fa873b0c697f5e6ee0740931018a7` |
| `data/alexscaves/enchantment/tsunami.json` | 358 | `37f1f8c3f8b98084b73b23aa2ec49ba9a925bb9a37089f622cf992234a086242` |
| `data/alexscaves/enchantment/second_wave.json` | 413 | `68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c` |
| `data/alexscaves/tags/item/enchantable/ortholance.json` | 50 | `1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac` |
| `data/alexscaves/loot_table/gameplay/deep_one_knight_barter.json` | 6.197 | `57c4a14e6a92f963e726ed92136034a091bdf8929398e8ba2b9d94a6c302c818` |
| `data/minecraft/tags/enchantment/in_enchanting_table.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/non_treasure.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/on_random_loot.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/tradeable.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |

| Classe / método | Instruções selecionadas / corpo nativo |
|---|---:|
| `OrtholanceItem.<init>`, `acModifiers`, `getDefaultAttributeModifiers` | `30/30`, `8/8`, `8/8` |
| `OrtholanceItem.getUseAnimation`, `getEnchantmentValue`, `getUseDuration` | `2/2` cada |
| `OrtholanceItem.use`, `lambda$getDefaultAttributeModifiers$0` | `20/20`, `4/4` |
| `OrtholanceItem.releaseUsing` | **`199/435`, PARTIAL**, janelas `0–244` e `705–869` |
| `WaveEntity.<init>(EntityType,Level)`, `<init>(Level,LivingEntity)` | `5/5`, `10/10` |
| `WaveEntity.setOwner`, `getOwner`, `defineSynchedData`, `getSlamAmount` | `12/12`, `27/27`, `31/31`, `13/13` |
| `WaveEntity.getYRot`, `setYRot`, `getLifespan`, `setLifespan`, `getWaitingTicks`, `setWaitingTicks` | `7/7` cada |
| `WaveEntity.isSlamming`, `setSlamming`, `getWaveScale`, `setWaveScale` | `7/7` cada |
| `WaveEntity.attackEntities`, `onSyncedDataUpdated`, `getDimensions`, `<clinit>` | `81/81`, `10/10`, `7/7`, `21/21` |
| `WaveEntity.readAdditionalSaveData`, `addAdditionalSaveData` | `19/19`, `14/14` |
| `WaveEntity.tick` | **`165/318`, PARTIAL**, janelas `0–186` e `486–619` |
| `ACCompat.enchantLevel`, `hurtAndBreakUsedHand`, `slotOf`, `attackDamageBonus` | `24/24`, `8/8`, `7/7`, `12/12` |
| `ACCompat.lambda$attackDamageBonus$2`, `knockback`, `useFail`, `useConsume` | `14/14`, `6/6`, `3/3`, `3/3` |
| `ACCompat.isInWaterOrBubble`, `hasUUID`, `getUUID`, `putUUID`, `getInt(CompoundTag,String)` | `3/3`, `4/4`, `4/4`, `5/5`, `4/4` |
| `ACEnchantmentRegistry.key`, `<clinit>` | `6/6`, **`3/182`, PARTIAL**, offsets `239,242,245` |
| `ACItemRegistry.lambda$static$110`, `<clinit>` | `11/11`, **`5/1382`, PARTIAL**, offsets `2072,2075,2078,2083,2086` |
| `ACEntityRegistry.lambda$static$47`, `<clinit>` | `14/14`, **`5/424`, PARTIAL**, offsets `823,826,829,834,837` |

O produtor seleciona **123+76=199 instruções** e omite **236** dos ramos normal/Second Wave em `@247–702`. O tick seleciona **98+67=165** e omite **153** de interpolação/partículas cliente em `@189–483`. Branches podem apontar para fora das janelas: elas não demonstram CFG fechado ou cobertura semântica integral. Os limites genéricos de **256 âncoras por método** e **8.192 por manifesto** permanecem preservados. Hashes integrais identificam os bytes omitidos sem convertê-los em cobertura.

Cada corpo nativo foi normalizado em JSON UTF-8, `ensure_ascii=False`, `sort_keys=True`, `separators=(',',':')`, no objeto `{owner,name,descriptor,instructions}`. `owner` é o caminho do classfile; `instructions` é a lista crescente de `{offset,opcode,operand,symbol}` do parser do auditor. Os fingerprints integrais adicionais dos métodos delimitados não ampliam suas seleções:

| Corpo PARTIAL | Selecionadas / nativas / omitidas | SHA-256 do corpo normalizado integral |
|---|---:|---|
| `OrtholanceItem.releaseUsing(ItemStack,Level,LivingEntity,int)V` | `199/435/236` | `8be8e96b62eb3e06c22e5124942352d7c9224990add4b2c7818babe0a1ab5b1a` |
| `WaveEntity.tick()V` | `165/318/153` | `ac23c8547dd701e75d02fc2166b09b825af989c7ecf81da8f44a3a56280c5656` |
| `ACEnchantmentRegistry.<clinit>()V` | `3/182/179` | `1ba929dc075622139847f3388c5d9a5b946d20088a59c3e242aeb8164879ebd0` |
| `ACItemRegistry.<clinit>()V` | `5/1382/1377` | `9c28d234b1512f04688b1b8231966f5bad8872f3b3fbeca88be5f25758359b39` |
| `ACEntityRegistry.<clinit>()V` | `5/424/419` | `1b6612b155c3d252ca1c8489ff7b0e59356b62ae96f3acd5a0f8a62fafe25600` |

O scan fresh percorreu **1.555 classfiles**, interpretando `Fieldref` exato de `ACEnchantmentRegistry.TSUNAMI:Lnet/minecraft/resources/ResourceKey;`: encontrou somente `ACEnchantmentRegistry.class` e `OrtholanceItem.class`. O registro liga literal `tsunami@239`, `key@242` e `putstatic TSUNAMI@245`; o reader direto observado está em `releaseUsing@26–41`. O censo não exclui reflexão, transformadores, mixins ou consumidores externos. Os bootstraps **117**, **163** e **68** ligam respectivamente a supplier Ortholance, a supplier Wave e a factory `WaveEntity(EntityType,Level)`; outros registros das classes compartilhadas não são certificados por associação.

O JSON próprio tem **358 bytes**, SHA-256 **`37f1f8c3f8b98084b73b23aa2ec49ba9a925bb9a37089f622cf992234a086242`**: máximo **I**, peso **1**, custo mínimo `1+20(L−1)`, máximo `41+10(L−1)`, bigorna **8**, slot `mainhand`. No nível I os custos são **1/41**. Não contém `effects` nem `exclusive_set` próprios. O inglês literal é “Tsunami” / “Ortholance launch summons a single, gigantic wave”; o português examinado não tem chaves próprias do ID, e a ficha usa paráfrase técnica. A tag `enchantable/ortholance`, **50 bytes**, SHA-256 `1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac`, contém somente `alexscaves:ortholance`.

O scan dos **51 JSONs de encantamento** encontra exclusão reversa somente em `second_wave.json`, **413 bytes**, SHA-256 `68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c`, cujo `exclusive_set` inclui `alexscaves:tsunami`. A ausência de exclusão própria não prova compatibilidade global. As tags `in_enchanting_table`, `non_treasure`, `on_random_loot` e `tradeable` contêm o ID; cada recurso tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. O loot `gameplay/deep_one_knight_barter.json`, **6.197 bytes**, SHA-256 `57c4a14e6a92f963e726ed92136034a091bdf8929398e8ba2b9d94a6c302c818`, inclui **Ortholance com weight 10**, sem função de encantamento nessa entrada; não promete Tsunami na stack. Não foi encontrado caminho de receita empacotada contendo `ortholance` ou `tsunami`; isso não prova impossibilidade global de obtenção. Aquisição, elegibilidade e compatibilidade efetivas dependem de datapacks/modlist.

No produtor, `C=clamp(getUseDuration(stack,null)−remainingUseTicks,0,60)`. `getUseDuration` retorna **72.000**, duração de uso da arma, distinta da duração da onda. Flinging é lido como `F`, e **`enchantLevel(stack,TSUNAMI)>0`** vira booleano local 7 antes do retorno por `C<=0`. O reader retorna o primeiro nível correspondente ou zero, sem clamp próprio ao máximo I ou validação própria de slot/tag. Zero/não positivo desabilita; I e qualquer nível externo positivo habilitam o mesmo ramo, sem escala por nível Tsunami, chance ou multiplicador de nível II forçado. O snapshot é feito no release da stack recebida.

Com operações float nativas, **`P=0.1F×C+0.1F×F`** e **`V=movimentoAtualDoUsuário + normalize(viewVector(1F)).multiply((double)P,(double)(P×0.15F),(double)P)`**. `V` incorpora movimento anterior e inclinação do olhar. Somente **`C>=10 && !level.isClientSide()`** alcança som, pedido de desgaste, emissão e ataque direto em `@95–833`. Cargas positivas 1–9 e chamadas cliente ainda podem alcançar o movimento final `@836–866`; a guarda de servidor não cobre todo o release.

Após som e **um pedido de desgaste de 1**, o ramo Tsunami fixa **`B=5`**, constrói `WaveEntity(level,usuário)` e tenta inserir **uma onda**, com **lifespan20, waveScale5F, waitingTicks2**. A posição usa **X/Z de `usuário.position()+V` e Y do usuário**; yaw é **`−float(atan2(V.x,V.z)×57.2957763671875D)`**. O produtor não chama `setDeltaMovement` na onda: `V` não é copiado como velocidade dela. O construtor atribui owner e UUID pelo setter. `addFreshEntity@240` tem retorno descartado em `@243`; uma tentativa não demonstra inserção aceita, colisão, dano ou sobrevivência.

O **`goto@244→705`** pula tanto o loop primário normal `@247–456` como o reader e loop de Second Wave `@459–702`. Mesmo com ambos os níveis forçados, esse caminho Tsunami não consulta Second Wave. A exclusão reversa de dados permanece autoridade independente; não aplicar `max(1,B−1)` do ramo normal a B=5 para prometer ondas retardadas. As provas individuais anteriores permanecem intactas.

Em `@705–833`, o ataque direto seleciona `LivingEntity` na AABB entre **`posiçãoDoUsuário`** e **`posiçãoDoUsuário+V×B`**, inflada em **1D**, com B=5. Usa **`mobAttack(usuário)`**, exclui o próprio usuário, aliados no sentido `usuário.isAlliedTo(vítima)` e alvos sem LOS. Pede **`hurt(source,(float)attackDamageBonus(stack))@824`**, descarta o resultado `@827` e depois pede **`stopRiding@830`**. Dano recusado não bloqueia esse callsite de desmontar. O helper soma quantidades dos modificadores MAINHAND de `ATTACK_DAMAGE`; não aplica ali a base do atributo do usuário nem todas as operações de uma engine completa. O equipamento registra ataque **+5D**, velocidade **−2.4000000953674316D**, durabilidade **340** e raridade **UNCOMMON**; esses parâmetros não equivalem a dano final fixo de Tsunami. O movimento final do usuário é **`V+(0,(onGround?0.2F:0F)+0.1F×F,0)`**, com arredondamentos nativos, sem alcance final fixo.

Wave tem dimensões registradas **`0.9F×0.9F`**, updates de velocidade habilitados e intervalo **1**. `getDimensions` escala as dimensões herdadas por `waveScale`, e a atualização sincronizada de escala pede `refreshDimensions`. Com escala5, as dimensões nominais são **4.5F**; a AABB corrente e as colisões efetivas continuam sob a engine. `attackEntities(S)` procura `LivingEntity` na **própria AABB corrente inflada em `(0.5D,0.5D,0.5D)`**, usa **`mobProjectile(onda,campo owner)`** e exclui aliados à onda, Deep Ones e, se owner não null, o owner e seus aliados. Esse volume, fonte e filtros são distintos do ataque direto; o corpo não testa LOS nem deduplica vítimas.

Para cada candidato elegível, o corpo pede **`hurt(source,S+1F)@123`**, descarta o booleano `@126`, pede **`setSlamming(true)@129`** e depois knockback de magnitude **`0.1D+0.5D×(double)S`**, com direção `(sin(yaw×0.017453292F),−cos(yaw×0.017453292F))`. Dano recusado não bloqueia slam ou knockback; slam também não encerra o loop. O helper apenas delega a `LivingEntity.knockback`. O tick passa **`S=2F×getSlamAmount(1F)+1F+getWaveScale()`**. Com escala5 preservada, dano bruto pedido é nominalmente **`7+2×slamAmount`**, e knockback pedido **`3.1+slamAmount`**. O interpolante próprio é nominalmente 0–1, derivado de progresso até10. Essas expressões não demonstram HP perdido, deslocamento, DPS, frequência de hits aceitos ou ataque único.

Quando `waitingTicks>0`, o tick **decrementa somente no servidor**, pede invisibilidade e **retorna nos dois lados**, inclusive no tick que leva a espera a zero. Fora da espera, atualiza progresso de slam e pede descarte quando slamming/progresso10; não há retorno imediato após esse callsite. A gravidade é **`−0.03999999910593033D`** quando aplicável fora de água/bolha. A aceleração horizontal é `Vec3(0,0,(double)(a×a×0.2F))` rotacionado por −yaw, com **`a=min(activeWaveTicks/10F,1F)`**, sem fator de escala. O ataque `@502–527` exige servidor e precede o move desse trecho. O movimento pedido usa **`deltaAtual×0.8999999761581421D+aceleração`**, e o delta posterior recebe multiplicadores **`(0.9900000095367432D,0.9800000190734863D,0.9900000095367432D)`**. Lifespan20 é limiar estrito **`activeWaveTicks>lifespan`** para pedir slam, também pedido se **`activeWaveTicks>10 && horizontalDistance(delta)<0.04D`**. Não significa descarte exatamente em20 ticks, velocidade cinco vezes maior ou alcance certificado.

O custo solicitado é único e anterior à tentativa de spawn, sem depender do retorno de inserção. `hurtAndBreakUsedHand` usa a mão em uso, converte para slot e delega a `ItemStack.hurtAndBreak`; o release e esse wrapper não têm gate creative próprio. A engine decide o desgaste físico. Esses consumidores não pedem munição, mana, stamina, fome, XP ou cooldown próprio; ausência local não prova custo global zero. Bigorna8 pertence à aquisição, e espera2/lifespan20/progresso são estados distintos de cooldown.

`getOwner` pode resolver `ownerUUID` no `ServerLevel` quando chamado, mas **`attackEntities` lê o campo owner diretamente**. A presença do getter não certifica restauração automática da autoria de dano após reload. Os overrides completos de save/load **não chamam super** e leem/gravam diretamente somente **`Owner` UUID e `Lifespan`**. Não serializam ali escala, espera, yaw, slamming/progresso, contador ativo, nível Tsunami ou identidade do ramo. Esses corpos não demonstram perda/restauração física ou convergência de rede; também não autorizam owner novo, estado paralelo, reembolso, repetição de dano ou relançamento compensatório. Os defaults sincronizados são **slamming=false, lifespan10, espera0, yaw0F, escala1F**; os setters observados não são hooks mutadores certificados.

Reprodução a partir da raiz do repositório, com **Java 21** e o mesmo JAR publisher:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile tsunami \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TSUNAMI-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/tsunami-evidence.json

PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_tsunami_cards_test.py -v

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/qa -p 'alexscaves_1010_action_contract_audit_test.py' -v

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/qa -p 'alexscaves*_test.py'

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s scripts/catalog -p '*_test.py'
```

Verificações executadas sobre o selo final, com Java 21 disponível em `JAVA_HOME` e `PATH`:

| Verificação | Resultado observado |
|---|---|
| CLI real `--profile tsunami`, JAR publisher e manifesto final | **PASS**: 1 ficha, 6 classes, 11 recursos, 51 métodos, 901 âncoras |
| Rebuild repetido do manifesto | Bytes idênticos; SHA-256 `748e78f92ab0da6fdca2a33f01ce6626bbbbb0a2dd23f2ffa4feb5c47fb9b1f2`, 177.013 bytes |
| Novos casos Tsunami no auditor compartilhado | **12/12 PASS**, incluídos nos **237/237 PASS** do arquivo de testes do auditor |
| Regressões semânticas `alexscaves_1010_tsunami_cards_test.py` | **13/13 PASS** |
| Suíte `docs/qa/alexscaves*_test.py` | **1.119/1.119 PASS**, incluindo os 25 casos novos acima |
| Suíte `scripts/catalog/*_test.py` | **165/165 PASS**; total pertinente **1.284/1.284 PASS** |
| Índices gerados de perks | **544 índices**, **2.391 candidatos**, **0 erros** |

A execução ampliada de `docs/qa/*_test.py` com Java 21 executou **2.470 testes**, com **uma falha e zero erros**: `RequiemPhysicalLedgerTests.test_matrix_29_exact_and_scope_corrected_by_one` esperava 29 entradas e encontrou 38. O teste e seus dois arquivos de entrada são byte a byte idênticos aos de `main`; essa falha histórica não foi promovida a PASS nem alterada neste recorte. As verificações acima são estáticas e não substituem QA física.

As provas anteriores [Sea Swing](EXACT-SEA-SWING-STATIC-1.0.10.json), [Second Wave](EXACT-SECOND-WAVE-DISCOVERY-1.0.10.json) e [Flinging](EXACT-FLINGING-1.0.10.json), assim como suas fichas, conservam bytes e escopos. Uma ficha individual e **+0 raízes mágicas** não promovem Ortholance integral, as vinte fichas parciais anteriores, Stage, provider integral ou adapter executável. Black Arcana conserva seu runtime mágico; Alex's Caves conserva emissão, movimento, dano e liquidação nativos. Enshrouded e RPG Skill Tree exigem boundary demonstrado e crédito único da ação raiz após resultado autorizado. Spawn tentado/aceito, pedido de dano/dano aceito, desmontagem, knockback e kill/Mastery são estados distintos; retornos descartados não fornecem recibo de crédito.

QA física permanece pendente para C0/1–9/10/60 e cargas externas; níveis0/I/externos, stack e snapshot; custo/creative/mãos; flags forçadas Tsunami/Second Wave; posição com movimento prévio, yaw zero/vertical e Y; spawn recusado, dimensões e colisões; filtros/fontes/LOS/Deep One separados; dano recusado e efeitos posteriores, repetição de vítimas e invulnerabilidade; espera/lifespan/progressos, água e gravidade; cliente/dedicado, eventos, PvP/claims e datapacks; save/load de escala/espera/yaw/owner, unload, dimensão e sincronização; kills/XP/Mastery. A próxima identidade é recalculada no [crosswalk alfabético vivo](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md). Estado final: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, **`NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`**.
