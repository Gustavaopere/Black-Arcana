# Triple Split 1.0.10 — contrato individual SHA-exato

A [ficha individual](enchantments/triple-split.md) conclui somente `alexscaves:triple_split` como **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. O [manifesto individual](EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.json) sela identidade, snapshot de disparo e divisão nativa selecionada do Gumball; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, **`NO_MUTATION`**. `ShotGumItem.acInventoryTick` permanece **PARTIAL**. A arma integral, os encantamentos irmãos, a aceitação de dano/spawn pela engine, a persistência herdada e o provider integral conservam seus limites anteriores. Triple Split acrescenta **zero raízes mágicas** às oito existentes; a divisão de munição nativa não constitui outro cast.

A autoridade física é o publisher CurseForge projeto `1645389`, arquivo `8856293`, `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 **`36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`**. O TOML empacotado declara `alexscaves` **1.0.10**. A fonte pública [`Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e é apenas corroboração adjacente, sem prova de paridade de build. Os parâmetros certificados foram extraídos do JAR 1.0.10.

O manifesto tem **274.472 bytes**, SHA-256 **`b2db8c5daafc2054258780c1a2f59e41de50d01fac3be7c349e41d913c7c1093`**, e sela a ficha SHA-256 **`27824d14c8fc3d042bd517f43f9c5672e14c30af9ecfadbec3d2b179aaeff987`**. A auditoria real retornou **PASS: 1 ficha, 7 classes, 11 recursos, 59 métodos, 1.452 âncoras**. Há **55 corpos completos, somando 1.185 instruções**, e quatro métodos delimitados, somando **267 âncoras**. As classes são `ShotGumItem`, `GumballEntity`, `ACCompat`, `ACEnchantmentRegistry`, `ACItemRegistry`, `ACEntityRegistry` e `ACDamageTypes`, sob `com/github/alexmodguy/alexscaves/`. A contagem não promove os contratos integrais das classes compartilhadas.

| Classe / método | Instruções selecionadas / corpo nativo |
|---|---:|
| `ShotGumItem.<init>`, `getEnchantmentValue`, `isEnchantable` | `8/8`, `2/2`, `8/8` |
| `ShotGumItem.getShootTime`, `setShootTime`, `getCrankAngle`, `setCrankAngle` | `11/11` cada |
| `ShotGumItem.getGumballsLeft`, `setGumballsLeft`, `isShooting`, `setShooting` | `15/15`, `11/11`, `13/13`, `11/11` |
| `ShotGumItem.hasAmmo`, `use`, `findAmmo`, `lambda$static$0`, `<clinit>` | `7/7`, `79/79`, `27/27`, `11/11`, `3/3` |
| `ShotGumItem.acInventoryTick` | **`254/285`, PARTIAL**, janelas `0–10` e `81–607` |
| `GumballEntity.<init>(EntityType,Level)` e `<init>(Level,LivingEntity)` | `19/19`, `10/10` |
| `GumballEntity.defineSynchedData`, `tick`, `bounceFromDirection` | `43/43`, `165/165`, `198/198` |
| `GumballEntity.getMaximumBounces`, `setMaximumBounces`, `getBounces`, `setBounces` | `7/7` cada |
| `GumballEntity.getDamage`, `setDamage`, `getColor`, `setColor` | `7/7` cada |
| `GumballEntity.targetsOnBounce`, `setTargetsOnBounce`, `splitsOnHit`, `setSplitsOnHit`, `isExplosive`, `setExplosive` | `7/7` cada |
| `GumballEntity.getDefaultGravity`, `onHit`, `onHitEntity` | `2/2`, `79/79`, `162/162` |
| `GumballEntity.addAdditionalSaveData`, `readAdditionalSaveData`, `<clinit>` | `9/9`, `9/9`, `29/29` |
| `ACCompat.enchantLevel`, `createEntity`, `getTag`, `getOrCreateTag`, `setTag` | `24/24`, `4/4`, `12/12`, `14/14`, `14/14` |
| `ACCompat.getBoolean`, `getInt(CompoundTag,String)`, `getFloat(CompoundTag,String)`, `usePass`, `useConsume` | `4/4`, `4/4`, `4/4`, `3/3`, `3/3` |
| `ACEnchantmentRegistry.key` e `<clinit>` | `6/6`, **`3/182`, PARTIAL**, offsets `437,440,443` |
| `ACItemRegistry.lambda$static$176` e `<clinit>` | `4/4`, **`5/1382`, PARTIAL**, offsets `3109,3112,3115,3120,3123` |
| `ACEntityRegistry.lambda$static$67` e `<clinit>` | `14/14`, **`5/424`, PARTIAL**, offsets `1163,1166,1169,1174,1177` |
| `ACDamageTypes.causeGumballDamage` | `13/13` |

As duas janelas do produtor contêm **6 + 248 = 254 instruções**. Omitem as **31 instruções** de atualização visual/tag `Prev*` em `@12–78` do corpo nativo de **285**. O prefixo captura estado de disparo e as janelas posteriores cobrem trigger, snapshot, emissão, débito e andamento selecionado. Branches podem apontar para fora de uma seleção delimitada; a seleção não demonstra CFG fechado nem cobertura semântica integral do método. O limite genérico de **256 âncoras por método** e **8.192 por manifesto** permanece preservado. O hash da classe e o fingerprint integral identificam os bytes omitidos, sem convertê-los em cobertura semântica.

Na extração, cada corpo nativo foi normalizado como JSON UTF-8, `ensure_ascii=False`, `sort_keys=True`, `separators=(',',':')`, no objeto `{owner,name,descriptor,instructions}`. `owner` é o caminho do classfile; `instructions` é a lista crescente de `{offset,opcode,operand,symbol}` do parser do auditor. Os fingerprints adicionais dos corpos delimitados seguem abaixo; não ampliam a seleção do manifesto.

| Corpo / quantidade nativa | SHA-256 do corpo normalizado |
|---|---|
| `ShotGumItem.acInventoryTick(ItemStack,Level,Entity,boolean)V` / `285` | `8b7011891909a40ee6b305e6e12c40971ca02e3bcfe92f86975c0959f3ca6a2b` |
| `ACEnchantmentRegistry.<clinit>()V` / `182` | `1ba929dc075622139847f3388c5d9a5b946d20088a59c3e242aeb8164879ebd0` |
| `ACItemRegistry.<clinit>()V` / `1382` | `9c28d234b1512f04688b1b8231966f5bad8872f3b3fbeca88be5f25758359b39` |
| `ACEntityRegistry.<clinit>()V` / `424` | `1b6612b155c3d252ca1c8489ff7b0e59356b62ae96f3acd5a0f8a62fafe25600` |

O scan fresh do constant pool percorreu **1.555 classfiles**, interpretando entradas JVM `Fieldref` e procurando a tripla exata `ACEnchantmentRegistry`, `TRIPLE_SPLIT`, `Lnet/minecraft/resources/ResourceKey;`. Encontrou somente `ACEnchantmentRegistry.class` e `ShotGumItem.class`. O primeiro declara a chave, e o reader direto observado está em `acInventoryTick`; o scan não exclui reflexão, transformadores, mixins ou consumidores externos. A janela `ACEnchantmentRegistry.<clinit>@437–443` liga o literal `triple_split` à chave. Os bootstraps **178** e **183** ligam respectivamente `shot_gum` a `ACItemRegistry.lambda$static$176` e `gumball` a `ACEntityRegistry.lambda$static$67`; o bootstrap **48** liga a factory da entidade ao construtor `(EntityType,Level)`. Os demais registros desses inicializadores não são certificados individualmente.

Os **11 recursos** selam TOML, idiomas `en_us`/`pt_br`, JSON próprio, JSON `targeted_ricochet` somente para exclusão, tag `enchantable/shot_gum`, receita `shot_gum` e quatro tags de aquisição. O JSON próprio tem **361 bytes**, SHA-256 **`fd4f773c48969b4c2537f443cc80d91e1385d545763be78feaefc5816ac551a0`**: máximo **I**, peso **2**, custo mínimo `1+12(L−1)`, máximo `41+10(L−1)`, anvil cost **4**, slot `mainhand`; no nível I, mínimo/máximo **1/41**. Não possui `effects` nem `exclusive_set` próprios. O inglês literal é “Triple Split” / “Gumballs split into three additional Gumballs after hitting their first target”; não há chaves próprias de Triple Split no português examinado. A explicação portuguesa da ficha é uma paráfrase técnica, sem transformar esse texto em prova de primeiro dano aceito, três inserções aceitas ou três hits.

A tag de item, **48 bytes**, SHA-256 `3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d`, contém somente `alexscaves:shot_gum`. As tags `in_enchanting_table`, `non_treasure`, `on_random_loot` e `tradeable` contêm o ID; cada recurso tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. O scan dos **51 JSONs de encantamento** encontra exclusão reversa somente em `targeted_ricochet.json`, **422 bytes**, SHA-256 `adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e`: seu `exclusive_set` inclui `alexscaves:triple_split`. A ausência de exclusão no JSON próprio não prova compatibilidade global, e flags compartilhadas no Java não legitimam essa coexistência.

A receita de equipamento, **493 bytes**, SHA-256 `11851d66a5e83898a166bb8f92fda1660f305bdc20b1dd0c2f8b5939ae2425a1`, declara padrão `SPP / III / IN ` e resultado de **1 Shot Gum**: 1 Sugar Glass, 2 Gumball Piles, 4 ingredientes de `alexscaves:ingots/iron` e 1 de `alexscaves:nuggets/iron`. Não garante Triple Split na stack resultante. Dados efetivos, aquisição e compatibilidade após datapacks/modlist permanecem externos ao selo.

`acInventoryTick@0–10` captura **`S=isShooting(stack)` e `T=getShootTime(stack)`**; somente **`S && T==5`**, testado em `@81–89`, alcança o disparo. O argumento booleano `selected` não é lido. Som e `setShooting(false)` precedem os flags. Em `@154–169`, **`enchantLevel(stack,TRIPLE_SPLIT)>0`** vira booleano local 10, passado a cada primário por `setSplitsOnHit@437–441`. O reader completo retorna o primeiro nível correspondente ou zero, sem clamp próprio ao máximo I ou validação própria de slot/tag. Nível zero/não positivo não habilita; I e qualquer nível externo positivo habilitam o mesmo ramo de três tentativas. Não há escala `3L` ou chance própria de divisão. O snapshot ocorre no tick de disparo; o impacto lê o estado do projétil, sem reler a stack.

Para holder `LivingEntity`, o laço primário tenta criar **dois Gumballs normais** ou **um explosivo**, conforme `EXPLOSIVE_FLAVOR`. Triple Split não determina essa quantidade. O construtor primário `(Level,LivingEntity)` chama `setOwner@18`. O disparo inicial usa dano **4F**, máximo **`4+2×level(BOUNCY_BALL)`**, velocidade **1.5F normal / 0.5F explosivo**, dispersão **5F**, além dos snapshots de targeting e explosivo. São parâmetros nativos selecionados do equipamento; os ramos compartilhados não certificam os contratos individuais dos encantamentos irmãos. Construção e setters precedem a guarda de lado: **somente `addFreshEntity@498–511` nesse laço** exige `!isClientSide`; o booleano é descartado. Essa guarda não se transfere ao débito, a todo o tick ou ao laço de filhos.

Após o laço primário, `acInventoryTick@518–550` poupa cargas de Player creative e, nos demais casos, grava **`max(cargas−1,0)` uma vez**. O débito fica fora da guarda local de inserção servidor, não depende da aceitação do spawn e não se multiplica por descendente. A arma conserva suas quatro cargas por recarga e o consumo survival de uma Gumball Pile no caminho já documentado em [Shot Gum](equipment/shot-gum.md). O impacto/split não pede outra munição, durabilidade, mana, stamina ou XP próprio nesses consumidores; ausência local não prova custo global zero. `anvil_cost=4` pertence à aquisição. As chaves `Shooting`, `ShootTime`, `Gumballs`, `CrankAngle` e `Prev*` mantêm autoridade da stack/equipamento, distintas do snapshot sincronizado no projétil. Não há cooldown ou duração próprios de Triple Split.

`GumballEntity.onHit(HitResult)V`, **79 instruções completas**, chama **`ThrowableProjectile.onHit@2` antes dos filtros locais**. Depois, bloco com collision shape não vazio pede bounce. Entidade que não é o próprio owner nem outro Gumball entra em `hitEntityIds`, e o bounce de entidade só ocorre com `!splitsOnHit()` em `@154–168`. Esses filtros posteriores não bloqueiam previamente o callback da superclasse. `ownedBy` não permite concluir exclusão geral de pets ou entidades pertencentes a terceiros. A lista `hitEntityIds` não deduplica o dano próprio: `onHitEntity` não a consulta e o `List.add` posterior em `onHit` não testa `contains`.

`onHitEntity(EntityHitResult)V`, **162 instruções completas**, captura vítima `@0–4`, owner `@5–9` e dano `@10–14`. Pode retornar antes de todo o restante em `@16–77` quando o owner é Gumbeeper possuído, resolve sua Licowitch e esta classifica uma vítima `LivingEntity` como friendly fire. Esse contexto conserva a prova Gumball, sem homologar a IA dos mobs. Depois cria a fonte por **`causeGumballDamage(registryAccessDaVítima,owner)@78–89`**. O helper completo seleciona a chave nativa `GUMBALL` e constrói `DamageSourceRandomMessages` com o argumento de entidade recebido e inteiro **1**; não recebe um par separado projétil/dono. `ACDamageTypes` é uma classe compartilhada de fontes, e o selo aqui abrange somente esse helper. Triple Split não cria DamageType nem redefine o contrato da fonte [Gumball](damage-types/gumball.md).

Com owner não null, vítima igual ao owner ou aliança **em qualquer sentido** pula o pedido de dano até `@143`; owner null pula esses testes para o caminho de dano. **`Entity.hurt(source,danoCapturado)@139` tem seu retorno descartado em `@142`**. Só então **`splitsOnHit()@144`** controla a divisão. Portanto, o ramo pode ser alcançado após dano pulado por owner/aliança ou após `hurt=false`; a saída especial de friendly fire anterior continua distinta. Colisão despachada, pedido de dano, dano aceito, divisão e kill/Mastery são estados separados. O contrato não diz “primeiro inimigo válido” ou “primeiro dano aceito”.

O laço `onHitEntity@150–342` usa **`i=0,1,2`**, chama **`ACCompat.createEntity(GUMBALL,level)`** a cada iteração e tenta inserir o filho; ao completar as três iterações, pede **descarte do pai em `@345–346`**. São **três tentativas por callback que alcança o ramo**, sem garantia de três spawns aceitos, alvos distintos ou hits. O corpo não contém guarda própria de lado, guarda para factory null, confirmação de spawn, deduplicação ou trava de reentrada. O booleano de `addFreshEntity@329–338` é descartado. Não inferir a guarda servidor do item para este corpo.

Geometria por iteração, em `@182–284`:

```text
u = normalize(deltaMovement atual do pai)
heading = -float(atan2(u.x,u.z)) × 180F / 3.1415927F
s = isExplosive(pai) ? 0.699999988079071D : 1.5D
v_i = Vec3(0,0,s).yRot(float(-toRadians(heading + 30F − 30F×i)))
posiçãoFilho = vítima.eyePosition + v_i
deltaMovementFilho = v_i
```

Os offsets angulares de entrada são **`+30°,0°,−30°`**, relativos ao heading horizontal; o vetor não tem componente Y de lançamento. A origem usa **os olhos da vítima + vetor**. São parâmetros de movimento, sem alcance máximo, raios de targeting ou cone físico final garantido. Heading, flag explosiva e getters são lidos dentro de cada iteração. Como os getters de cópia ocorrem depois do callback externo de dano, não há promessa de snapshot imutável do pai frente a hooks externos de dano/spawn. Movimento zero/vertical e trajetória real exigem QA da engine.

| Propriedade do filho | Operação própria no split |
|---|---|
| `SPLITS_ON_HIT` | **false**, `@287–290`; desativa recursão nesse estado nativo, sem garantia contra mutação externa |
| `DAMAGE` | Getter corrente do pai → setter `@293–299`; distinto do dano capturado antes de `hurt` |
| `TARGETS_ON_BOUNCE` | Getter corrente → setter `@302–308`; não legitima encantamentos incompatíveis |
| `EXPLOSIVE` | Getter corrente → setter `@311–317` |
| `MAXIMUM_BOUNCES` | Getter corrente → setter `@320–326`; copia total **M**, não restante **M−B** |
| Owner | Não é argumento da factory nem recebe `setOwner` nesse laço |
| Cor / bounces / IDs / progresso | Não são copiados explicitamente; o construtor sorteia cor `0..11`, cria lista vazia e o default de bounces é `0` |
| Spawn | `addFreshEntity@329–338`, retorno descartado |

`ACCompat.createEntity`, **4 instruções completas**, delega a **`EntityType.create(Level)`**. A factory registrada usa o construtor **`(EntityType,Level)`**, **19 instruções**, que não atribui owner; o construtor primário **`(Level,LivingEntity)`**, **10 instruções**, é que chama `setOwner`. Ausência de cópia própria não prova owner null sob todos os hooks externos nem defeito físico reproduzido, mas impede conceder automaticamente kills, XP ou Mastery dos filhos ao jogador. Não autoriza adicionar owner, token, cast ou estado paralelo para preencher essa lacuna.

`defineSynchedData`, **43 instruções completas**, define `SPLITS_ON_HIT=false` em **`@61–68`**, além de `DAMAGE=2F`, `TARGETS_ON_BOUNCE=false`, `EXPLOSIVE=false`, `MAXIMUM_BOUNCES=5`, `BOUNCES=0` e `COLOR=0`; o construtor sobrescreve a cor com aleatório `0..11`. Getter e setter de split têm **7 instruções** cada, sem clamp, slot, tag ou nível próprios. Esse estado sincronizado observado não constitui API mutadora segura.

O split não introduz busca de alvo, homing, área, hitbox, status, cura, knockback, DamageType, cooldown ou duração próprios; são **N/A como modificadores diretos** do ID. Usa a vítima do callback e o movimento corrente do pai. O Gumball conserva dimensões nativas **`0.25F×0.25F`**, gravidade **`0.07999999821186066D`** e parâmetros de dano/movimento existentes. O corpo completo `bounceFromDirection`, **198 instruções**, conserva o targeting opcional documentado individualmente em [Targeted Ricochet](enchantments/targeted-ricochet.md): AABB cúbica ±10D ao redor dos olhos, candidatos `LivingEntity`, filtros próprios de owner/aliança e IDs prévios, escolha nearest, vetor nominal `0.8` e fallback por reflexão, sem teste próprio de LOS/isAlive. Essa cobertura compartilhada não recertifica o encantamento irmão nem cria aquisição inicial de alvo para Triple Split.

O lifecycle normal descarta com **`B>M`**; o explosivo trata parada/progresso com **`B>=M`**. Em `tick()V`, **165 instruções completas**, explosivo com `B>=M` incrementa progresso enquanto `<=20F`. Quando o progresso já é `>20F`, no servidor pede **`Level.explode(getOwner(),x,y+0.5,z,2F,false,NONE)`** e descarte. Contagem de bounces e máximo copiado são estados distintos; progresso explosivo não é cooldown ou duração própria de Triple Split. Dano direto e explosão mantêm fontes e autoridades distintas. Três tentativas e dano unitário copiado não demonstram triplo HP perdido ou DPS.

Os overrides completos `addAdditionalSaveData` e `readAdditionalSaveData`, **9 instruções cada**, **chamam super** e gravam/leem diretamente somente **`Color`**. Não serializam explicitamente flag split, dano, targeting, explosivo, máximo, contagem, lista ou progresso. Esses corpos não certificam conservação/perda física, persistência herdada de owner, restauração da cadeia de filhos ou convergência cliente/rede. Save/load, unload, dimensão, latência e autoria permanecem pendentes; o contrato não autoriza estado compensatório, reembolso ou relançamento.

Reprodução a partir da raiz do repositório, com **Java 21** e o mesmo JAR publisher:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile triple_split \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/triple-split-evidence.json

PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_triple_split_cards_test.py -v
```

A auditoria real do builder retornou **PASS: 1 ficha / 7 classes / 11 recursos / 59 métodos / 1.452 âncoras**. A reconstrução externa sequencial repetida retornou PASS e produziu os mesmos bytes do manifesto, com o SHA-256 acima. Os **nove testes semânticos novos passaram**. A suíte completa executada, incluindo os testes de catálogo, retornou **1.259 testes PASS**; esses resultados são verificações estáticas e não substituem QA física.

Os [nove testes semânticos novos](../../../../docs/qa/alexscaves_1010_triple_split_cards_test.py) protegem identidade/rosters/limites; trigger e snapshot positivo; quantidade primária, owner e débito único; supercallback antes dos filtros; ordem de dano pulado/recusado e split; três tentativas sem confirmação; geometria corrente e origem nos olhos; factory/owner/cópias com split false; defaults sincronizados, NBT próprio e contabilidade estática/fila viva. O [auditor literal](../../../../docs/qa/alexscaves_1010_action_contract_audit.py) compara hashes, descritores, opcodes, operandos e símbolos com o artefato físico e mantém a família e o roster singulares. O [workflow compartilhado](../../../../.github/workflows/alexscaves-1010-action-contracts.yml) inclui o perfil `triple_split`, preservando download único e timeout de oito minutos.

As provas anteriores [Gumball](EXACT-GUMBALL-CONTRACTS-1.0.10.json), [split compartilhado](EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json) e [Targeted Ricochet](EXACT-TARGETED-RICOCHET-STATIC-1.0.10.json), assim como equipamento e fichas anteriores, conservam bytes e escopos. Uma ficha individual e **+0 raízes mágicas** não promovem a arma, as vinte fichas parciais anteriores, Stage, provider integral ou adapter executável. Black Arcana conserva seu runtime mágico, e Alex's Caves conserva emissão, movimento, divisão, dano e liquidação nativos; progressão/perks de Enshrouded e RPG Skill Tree exigem boundary demonstrado e crédito único da ação raiz após resultado autorizado. Setters e callbacks observados não são hooks mutadores certificados.

QA física continua pendente para níveis 0/I/externos e troca de stack após snapshot; primários normais/explosivos e cobrança única; dano pulado/recusado, callback/reentrada e descarte do pai; owner, aliados, Gumball e friendly fire especial; filhos com/sem owner, procs e kills; heading zero/vertical, geometria, factory null e spawn recusado; bounces, flags incompatíveis e explosão; defesas, eventos, PvP/claims e datapacks; cliente/dedicado, save/load, unload, dimensão e sincronização; crédito único de Mastery. A próxima identidade é sempre recalculada no [crosswalk alfabético vivo](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md). Estado final do recorte: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, **`NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`**.
