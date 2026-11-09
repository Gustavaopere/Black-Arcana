# Triple Splash 1.0.10 — contrato individual SHA-exato

A [ficha individual](enchantments/triple-splash.md) conclui somente `alexscaves:triple_splash` como **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. O [manifesto individual](EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.json) sela quantidade, geometria de lançamento e os consumidores nativos selecionados; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, **`NO_MUTATION`**. O tick/CFG integral do projétil, a execução da engine, os contratos individuais dos encantamentos irmãos e o provider integral permanecem abertos. Triple Splash acrescenta **zero raízes mágicas** às oito existentes; a raiz continua [Sea Staff — Water Bolt](actions/sea-staff-water-bolt.md).

A autoridade física é o publisher CurseForge projeto `1645389`, arquivo `8856293`, `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O TOML empacotado declara `alexscaves` **1.0.10**. A fonte pública [`Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e é apenas corroboração adjacente, sem prova de paridade de build. Nenhum parâmetro certificado foi tomado desse snapshot.

O manifesto tem **198.031 bytes**, SHA-256 **`2aa947c84a1e429b1786d21dfae2b325ead6198e31c6a24343db171a232a976d`**, e sela a ficha SHA-256 `585bd82f16a6b22352e061e7a63a7679523e34b7692235361076f79023422ae9`. A auditoria real retornou **PASS: 1 ficha, 5 classes, 11 recursos, 33 métodos, 1.063 âncoras**. Há **30 corpos completos, somando 878 instruções**, e três métodos explicitamente delimitados, somando 185 âncoras. O limite de **256 âncoras por método** e **8.192 por manifesto** foi preservado.

| Classe / método | Instruções selecionadas / corpo nativo |
|---|---:|
| `SeaStaffItem.<init>`, `use`, `getClosestLookingAtEntityFor`, `getEnchantmentValue`, `isEnchantable` | `4/4`, `189/189`, `119/119`, `2/2`, `8/8` |
| `WaterBoltEntity.<init>(EntityType,Level)` e `<init>(Level,LivingEntity)` | `27/27`, `28/28` |
| `WaterBoltEntity.defineSynchedData`, `getArcingTowards`, `setArcingTowards`, `<clinit>` | `12/12`, `19/19`, `7/7`, `11/11` |
| `WaterBoltEntity.onHitEntity`, `onHitBlock`, `damageMobs`, `onRicochetHit` | `37/37`, `28/28`, `105/105`, `122/122` |
| `WaterBoltEntity.isBubbling`, `setBubbling`, `remove`, `lambda$tick$0` | `7/7`, `7/7`, `59/59`, `4/4` |
| `WaterBoltEntity.readAdditionalSaveData`, `addAdditionalSaveData` | `6/6`, `6/6` |
| `WaterBoltEntity.tick` | **`177/362`, PARTIAL** |
| `ACCompat.enchantLevel`, `hurt`, `hurtAndBreak` com mão, `slotOf`, `useSidedSuccess`, `isInWaterOrBubble`, `getBoolean` | `24/24`, `5/5`, `7/7`, `7/7`, `4/4`, `3/3`, `4/4` |
| `ACEnchantmentRegistry.key` e `<clinit>` | `6/6`, **`3/182`, PARTIAL**, offsets `302,305,308` |
| `ACItemRegistry.lambda$static$108` e `<clinit>` | `11/11`, **`5/1382`, PARTIAL**, offsets `2038,2041,2044,2049,2052` |

`tick()V` contém quatro janelas contínuas locais: **`0–158` (83 instruções), `281–402` (58), `553–559` (5), `655–721` (31)**. Cobrem supertick/prefixo de homing, movimento/descartes, posição no ramo servidor e colisão/contador final. Partículas, interpolação cliente e trecho de trail ficam fora dessas janelas. Destinos de branches podem sair delas; não há afirmação de CFG fechado ou de cobertura semântica integral. Hashes de classe selam os bytes omitidos, sem converter essa identidade em auditoria de todos os ramos.

Na extração independente, cada corpo completo foi também normalizado como JSON UTF-8, `ensure_ascii=False`, `sort_keys=True`, `separators=(',',':')`, com objeto `{owner,name,descriptor,instructions}`; `owner` é o caminho do classfile e `instructions` a lista crescente de `{offset,opcode,operand,symbol}` do parser do auditor. Os fingerprints dos três corpos delimitados são:

| Corpo / quantidade nativa | SHA-256 do corpo normalizado |
|---|---|
| `WaterBoltEntity.tick()V` / `362` | `ed771f9dc9fe2f7b01064354e25d6f6362a8338b1447a60990dd10a2b1c79fc7` |
| `ACEnchantmentRegistry.<clinit>()V` / `182` | `1ba929dc075622139847f3388c5d9a5b946d20088a59c3e242aeb8164879ebd0` |
| `ACItemRegistry.<clinit>()V` / `1382` | `9c28d234b1512f04688b1b8231966f5bad8872f3b3fbeca88be5f25758359b39` |

Esses fingerprints são comparações adicionais de extração, não campos que ampliem a seleção semântica do manifesto. A reconstrução mantém disassembly, builder e relatórios externos ao repositório.

O scan novo do constant pool percorreu **1.555 classfiles**, interpretando entradas JVM `Fieldref` e procurando a tripla exata `ACEnchantmentRegistry`, `TRIPLE_SPLASH`, `Lnet/minecraft/resources/ResourceKey;`. Encontrou somente `ACEnchantmentRegistry.class` e `SeaStaffItem.class`. O primeiro declara a chave; o consumidor direto nativo observado está em `use`. Isso não exclui reflexão, transformadores ou código externo. A janela de registro liga `triple_splash` à chave; o bootstrap **115** liga `sea_staff` ao supplier **`lambda$static$108`**, cujo corpo declara **durabilidade 850** e **raridade UNCOMMON**. Os demais registros desses inicializadores não foram certificados individualmente.

Os **11 recursos** selam TOML, idiomas `en_us`/`pt_br`, JSON próprio, JSON `bouncing_bolt` somente para exclusão, tag `enchantable/sea_staff`, loot `deep_one_mage_barter` e quatro tags de aquisição. O recurso próprio tem **363 bytes**, SHA-256 `6946e2d21814f3e398925f2886a6284b140032b255a05f9598c8e00e2bc315be`: máximo **I**, peso **2**, custo mínimo `1+15(L−1)`, máximo `41+10(L−1)`, anvil cost **4**, `mainhand`; no nível I, mínimo/máximo **1/41**. Não possui `effects` nem `exclusive_set` próprios. O inglês literal é “Triple Splash” / “Sea Staff fires two additional water bolts”; não há chaves próprias no português examinado.

As tags `in_enchanting_table`, `non_treasure`, `on_random_loot` e `tradeable` contêm o ID. Um scan novo dos **51 JSONs de encantamento** encontrou uma exclusão reversa: `bouncing_bolt.json` contém `alexscaves:triple_splash` em `exclusive_set`. Esse dado foi selado sem concluir o contrato próprio de Bouncing Bolt. O barter contém o **item Sea Staff**, peso **12**, sem prometer Triple Splash na stack. A enumeração dos caminhos `data/alexscaves/recipe/` não encontrou caminho contendo `sea_staff`; isso delimita a ausência observada, sem inventar receita. Dados efetivos e elegibilidade após datapacks continuam externos ao selo.

`use@95–111` faz **`enchantLevel(stack,TRIPLE_SPLASH)>0 ? 3 : 1`**. O reader completo devolve o primeiro nível correspondente ou zero, sem clamp próprio, validação de slot ou tag. Qualquer nível positivo externo conserva três iterações, não `1+2L`. A criação é restrita ao ramo servidor; o alvo é adquirido uma vez antes do loop, com argumento **128D**. O helper completo conserva clip `VISUAL/NONE`, busca/filtros e escolha por distância ao ponto de hit. O ramo `EntityHitResult` existe no corpo, sem garantia de que a chamada externa `Level.clip` o produzirá. O mesmo UUID pode ser atribuído aos três bolts; não se trata de busca separada por spread.

As três iterações usam yaw adicional **`0/−50/+50°`**, velocidade passada **`2/1/1F`**, offset de pitch **`−20F`** e imprecisão **`12F`**. A posição usa ângulo `yHeadRot + 45°` na mão principal ou `−45°` na outra, largura multiplicada pelo double **`1.100000023841858D`**, seno/cosseno do ângulo float em radianos e Y igual a `eyeY−0.4000000059604645D`. Não há termo do índice/spread nessa origem; direção usa `getYRot()`, distinto da rotação da cabeça. O construtor atribui o jogador como owner. Os booleanos de `addFreshEntity` são descartados: o contrato é de **tentativas de inserção**, sem garantia de três entidades aceitas, hits distintos, leque físico final ou triplo dano.

Os corpos de impacto completos preservam os gates próprios: entidade exige servidor, hit diferente do próprio owner (sem generalizar a pets ou outros alvos associados) e `tickCount>2`; bloco exige servidor sem esse gate de idade. O dano é solicitado por `mobProjectile(this,owner LivingEntity ou null)`, em candidatos `LivingEntity` na AABB inflada **2D por eixo**, com filtros de aliança, owner e `DeepOneBaseEntity`, e **3F** por candidato elegível. `ACCompat.hurt` delega à engine; dano aceito ou HP perdido não foi medido. O gate `dieIn==−1` inicializa o contador **5**, sem bloquear toda chamada posterior a `damageMobs`; a janela final de tick conserva o cancelamento por `EventHooks.onProjectileImpact`, decremento e descarte ao chegar a zero. Descarte por blocos sem ar fora de água/bolha, arrasto nominal **0.9F** e gravidade nominal **−0.07F** aparecem na janela de movimento. Esses valores não são alcance máximo, duração máxima ou cadência garantida.

O corpo de ricochete completo serve para distinguir descendência e autoria: o último candidato elegível é guardado em `damageMobs@129–131` **antes** de saber se `hurt@139` retornou true. Depois do loop, a flag é consumida em `@231–233`, antes do callback `onRicochetHit@239`. O filho usa construtor com owner LivingEntity, copia posição/Bubbling e recebe UUID/impulso; mantém defaults próprios `seekAmount=0.3F` e `ricochet=false`. Não é uma segunda ativação de Triple Splash. Os ramos de Soak Seeking, Enveloping Bubble e Bouncing Bolt no corpo compartilhado não recebem certificados individuais por essa cobertura. Em particular, **`(double)0.3F > 0.3D`** é verdadeiro por arredondamento: não converter a comparação em teste simples de presença de Soak Seeking ou Triple Splash.

Som/swing, stat e custo estão fora da guarda local de criação servidor. Após o loop, o corpo pede **1 de durabilidade** uma vez sob `!instabuild`, pelo wrapper que converte a mão em slot e chama `ItemStack.hurtAndBreak`; o pedido não depende do retorno dos spawns. O método não pede munição, mana, fome, stamina ou XP e não chama cooldown próprio. Isso é ausência no caminho completo observado, sem prova de custo físico, cobrança duplicada cliente/servidor ou ausência de hooks externos. A manutenção passiva de [Seapairing](enchantments/seapairing.md) conserva contrato separado.

Os dados sincronizados próprios são `BUBBLING` e UUID opcional de alvo, defaults false/vazio. Os overrides NBT completos leem/gravam somente **`Bubbling`**, sem chamada a super; não serializam ali owner, alvo, `seekAmount`, `ricochet`, `dieIn` ou índice/nível Triple Splash. Isso não certifica persistência herdada, perda/restauração física ou autoria após reload. Não autoriza criar estado, reembolso ou relançamento compensatório.

Reprodução, a partir da raiz do repositório, com Java 21 e o mesmo JAR publisher:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile triple_splash \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/triple-splash-evidence.json

PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_triple_splash_cards_test.py -v
```

A CLI foi executada com o JAR físico e retornou **PASS: 1/5/11/33/1.063**. A reconstrução externa repetida produziu os mesmos bytes do manifesto. Os [testes semânticos](../../../../docs/qa/alexscaves_1010_triple_splash_cards_test.py) protegem os gates de quantidade, geometria, targeting, custo, janelas/precisão, colisão, lifecycle, NBT e limites do contrato. O [auditor literal](../../../../docs/qa/alexscaves_1010_action_contract_audit.py) mantém o roster singular, família e escopo; hashes, descritores, opcodes, operandos e símbolos são comparados com o artefato real. O [workflow compartilhado](../../../../.github/workflows/alexscaves-1010-action-contracts.yml) executa o novo perfil com os vinte perfis anteriores, download único e timeout preservado de oito minutos.

As provas antigas, a ação raiz e as fichas anteriores conservam bytes e escopos; os novos arquivos não reescrevem seus selos. O provider integral continua aberto, com oito raízes semânticas, nenhuma promoção de Stage ou adapter mutador. Quantidade aceita, colisão, dano, custos/creative, cliente/dedicado, permissões/claims, datapacks, save/load, unload, dimensão e sincronização continuam **QA física pendente**. Estado final: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, **`NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`**.
