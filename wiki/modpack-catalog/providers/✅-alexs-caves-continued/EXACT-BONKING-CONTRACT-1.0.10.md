# Bonking 1.0.10 — contrato individual SHA-exato

A [ficha individual](enchantments/bonking.md) conclui somente `alexscaves:bonking` como **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. O [manifesto individual](EXACT-BONKING-CONTRACT-1.0.10.json) sela a definição publicada, o corpo integral de `CommonEvents.livingDie`, os 16 corpos declarados do Primitive Club, os helpers e as três bridges de loot selecionadas. Os dois inicializadores compartilhados de registros continuam **PARTIAL**. Esta conclusão individual preserva `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` e **`NO_MUTATION`**; acrescenta **zero raízes mágicas** às oito existentes e não promove o equipamento Primitive Club, Dazing Sweep, Swiftwood, Stage, o provider integral ou um adapter executável.

A autoridade é o publisher CurseForge projeto **1645389**, arquivo **8856293**, `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 **`36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`**. O TOML empacotado declara `alexscaves` **1.0.10**, para Minecraft 1.21.1 / NeoForge / Java 21. A fonte pública [`Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e serve como corroboração adjacente, sem demonstrar paridade de build. Os parâmetros deste contrato vêm dos bytes do JAR publisher 1.0.10, sem execução do jogo transformado nem nova auditoria da engine base.

| Artefato local selado | Bytes | SHA-256 |
|---|---:|---|
| [`enchantments/bonking.md`](enchantments/bonking.md) | 23.018 | `9aef69b6b06336615ba0498d211fd393032a01244eafb1ef902712b310d389b5` |
| [`EXACT-BONKING-CONTRACT-1.0.10.json`](EXACT-BONKING-CONTRACT-1.0.10.json) | 158.228 | `239d960fd09e4f01111bf981321aa75cd1746199a564943ab68c9382180e2e99` |

O recorte contém **1 ficha, 7 classfiles, 11 recursos, 26 corpos/janelas selecionados e 678 âncoras** — seis classes com métodos no mapa `classes` e uma interface declarativa em `native_metadata`: **24 corpos completos / 670 instruções** e **dois corpos PARTIAL / oito âncoras**. Os 16 corpos declarados do Primitive Club somam **381 instruções**; o maior tem 171. `livingDie` tem **229/229 instruções**, incluindo os entornos independentes de Bonking. Interface selada e hash de classfile completo identificam artefatos; não ampliam o roster de corpos selecionados. Os caminhos abaixo partem de `com/github/alexmodguy/alexscaves/`.

| Classfile | Corpos/janelas | Âncoras | Bytes da entrada | SHA-256 da entrada completa | Cobertura selecionada |
|---|---:|---:|---:|---|---|
| `server/event/CommonEvents.class` | 1 | 229 | 41.772 | `d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43` | `livingDie` integral; demais listeners fora do recorte |
| `server/item/PrimitiveClubItem.class` | 16 | 381 | 12.822 | `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac` | 16/16 corpos declarados integrais; contexto da arma |
| `server/misc/ACCompat.class` | 2 | 28 | 70.539 | `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b` | `enchantLevel` e `createEntity` integrais |
| `mixin/MobMixin.class` | 3 | 17 | 2.120 | `38381f9b5b3908e813711f031161a1e25b46e68d220ed34c137948e6b59dac3e` | Três bridges integrais; sombras/target são metadados |
| `server/entity/util/EntityDropChanceAccessor.class` | 0 | 0 | 429 | `e702802393eda342e252acc517baf735c830d715bcc422a9acdee36bf24ab4ba` | Interface selada; três declarações sem corpo |
| `server/enchantment/ACEnchantmentRegistry.class` | 2 | 9 | 10.318 | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` | `key` integral e `<clinit>` PARTIAL |
| `server/item/ACItemRegistry.class` | 2 | 14 | 61.242 | `114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1` | Supplier integral e `<clinit>` PARTIAL |
| **Total selecionado** | **26** | **678** | — | — | **24 completos + 2 PARTIAL** |

Os recursos abaixo são entradas completas do publisher. Seus hashes não certificam a composição efetiva de tags, recipes ou loot do pack carregado.

| Recurso empacotado | Bytes | SHA-256 da entrada completa |
|---|---:|---|
| `META-INF/neoforge.mods.toml` | 1.066 | `54dfb8cdba886fd5ef8e64d2a51c487ce4bf2400995884937ee5fd6d89df68fa` |
| `assets/alexscaves/lang/en_us.json` | 121.372 | `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f` |
| `assets/alexscaves/lang/pt_br.json` | 84.238 | `080bfaf05b6d710383579dfd0d3c01443f9fa873b0c697f5e6ee0740931018a7` |
| `data/alexscaves/enchantment/bonking.json` | 362 | `f03c4e8c2f8b00b3668b8d7bf14276647b3e0324c159c6336b189a258571a86a` |
| `data/alexscaves/tags/item/enchantable/primitive_club.json` | 54 | `71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43` |
| `data/alexscaves/recipe/primitive_club.json` | 330 | `b93f005c5632388ca6f34e3a114a8e0a4cf1c2ae99ae9bb0ed2edc2c73dddcc0` |
| `data/minecraft/tags/enchantment/in_enchanting_table.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/non_treasure.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/on_random_loot.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/tradeable.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `alexscaves.mixins.json` | 5.312 | `6e120e2d2cf226a25cbe3d0605968a184384194354eac0b1153108f74632c140` |

O roster completo de nomes, descritores JVM e instruções selecionadas está no [manifesto JSON](EXACT-BONKING-CONTRACT-1.0.10.json). Os fingerprints abaixo identificam corpos integrais particularmente relevantes ou PARTIAL. O normalizador usa JSON UTF-8 com `ensure_ascii=False`, `sort_keys=True`, `separators=(',',':')` para **`{owner,name,descriptor,instructions}`**: `owner` é o caminho do classfile e `instructions` contém linhas completas `{offset,opcode,operand,symbol}` em ordem crescente. Um digest de corpo inteiro é diferente do hash do classfile e do digest do parser histórico. Incluir instruções omitidas no fingerprint de um método PARTIAL apenas identifica esse corpo; não as converte em evidência selecionada.

| Classe / método | Selecionadas / nativas / omitidas | SHA-256 normalizado do corpo integral |
|---|---:|---|
| `CommonEvents.livingDie` | 229/229/0 | `40737aefdb49418028737a4b0a8ede771dd68b7baffad512769d58c66ee974cd` |
| `PrimitiveClubItem.acHurtEnemy` | 171/171/0 | `9750039604b875f32b516cd18fa6ad26d062b88594926980f0bacb37d4ed9cdf` |
| `ACCompat.enchantLevel` | 24/24/0 | `b4dddfa6748810de27f35ac6fa8be385fb913c992c9248e1b93f64ccbee79ed0` |
| `MobMixin.ac_dropCustomDeathLoot` | 8/8/0 | `58866d2d48355707ad95f18f9cb3c470a9752609bf2c519ea3fb43878b332a44` |
| `ACEnchantmentRegistry.<clinit>` | **3/182/179, PARTIAL** | `1ba929dc075622139847f3388c5d9a5b946d20088a59c3e242aeb8164879ebd0` |
| `ACItemRegistry.<clinit>` | **5/1382/1377, PARTIAL** | `9c28d234b1512f04688b1b8231966f5bad8872f3b3fbeca88be5f25758359b39` |

`ACEnchantmentRegistry.<clinit>` seleciona somente **`132,134,137`**, ligando `bonking`, `key` e `putstatic BONKING`; `ACItemRegistry.<clinit>` seleciona somente **`967,970,973,978,981`**, ligando o supplier, o literal `primitive_club`, o registro e `putstatic PRIMITIVE_CLUB`. O bootstrap **52** liga esse supplier a **`lambda$static$40`**, cujo corpo integral de nove instruções cria `PrimitiveClubItem` com durabilidade **120**. O helper integral `ACEnchantmentRegistry.key`, de seis instruções, fixa o namespace `alexscaves`. Os dois inicializadores PARTIAL somam **8 selecionadas / 1.564 nativas / 1.556 omitidas**; não representam fechamento dos registros compartilhados. Os limites genéricos de **256 âncoras por método** e **8.192 por manifesto** permanecem preservados, sem exceção por perfil.

O censo de **1.555 classfiles** interpreta o **Fieldref** exato `ACEnchantmentRegistry.BONKING:Lnet/minecraft/resources/ResourceKey;`, incluindo owner, nome e descritor: encontra somente `ACEnchantmentRegistry.class` e `CommonEvents.class`. Nenhum dos 16 corpos declarados do Primitive Club contém esse Fieldref. Isso limita referências diretas no publisher, sem excluir reflexão, mixins, transformadores, consumidores indiretos ou mods externos.

O texto inglês publicado é **“Bonking”** / **“Primitive Club has a chance to drop heads from slain mobs, as if a charged Creeper killed them”**. O `pt_br.json` contém nomes do Primitive Club, mas não nome/descrição de Bonking; a explicação técnica em português é uma **paráfrase**. A descrição publicada não substitui os gates compilados nem garante cabeça de toda espécie.

O JSON próprio tem **362 bytes**, máximo **I**, peso **1**, custo mínimo `1+18(L−1)`, máximo `41+10(L−1)`, bigorna **8**, slot `mainhand` e suporte `#alexscaves:enchantable/primitive_club`; no nível I, os custos declarados são **1/41**. Não contém `effects` nem `exclusive_set` próprios. A tag nativa de suporte lista somente `alexscaves:primitive_club`. Todas as quatro tags de aquisição — `in_enchanting_table`, `non_treasure`, `on_random_loot` e `tradeable` — contêm Bonking; cada uma tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. O scan separado dos **51 JSONs nativos de definição de encantamento** não encontra menção reversa a Bonking em `exclusive_set`. Estes dados documentam disponibilidade publicada e ausência daquela referência nativa, sem certificar probabilidade de aquisição, compatibilidade efetiva ou dados de terceiros.

A receita empacotada do Primitive Club usa o padrão diagonal **`["  C", " C ", "B  "]`**, dois `cycad` e um `heavy_bone`, para um club. `getEnchantmentValue()` retorna **1** e `isEnchantable(stack)` testa **`stack.count==1`**. Os atributos próprios da arma incluem **+8** de dano e velocidade calculada pelo caminho separado de Swiftwood. `hurtEnemy` delega a `acHurtEnemy`; este pede **1** de desgaste por `ACCompat.hurtAndBreak@6` antes do gate de lado e dos efeitos de stun/Dazing Sweep. `mineBlock` pede **2** no caminho apropriado. Estes são callbacks da arma; não estabelecem custo por proc, fórmula de dano ou escala por nível de Bonking, nem certificam o débito efetivo de durabilidade. Animações, sons, stun, busca de área e Dazing Sweep presentes nesses corpos permanecem separados deste encantamento de loot.

O consumidor principal é `CommonEvents.livingDie(Lnet/neoforged/neoforge/event/entity/living/LivingDeathEvent;)V`. A anotação empacotada é `net.neoforged.bus.api.SubscribeEvent`, **sem argumentos explícitos**; ela sozinha não prova registro/dispatch, prioridade, política de evento cancelado ou ordenação efetiva. O corpo integral selecionado **`@0–547`** contém **229 instruções, 21 desvios e zero handlers JVM de exceção**. O prefixo **`@0–72`**, sobre magma cube/frog primordial e `CARMINE_FROGLIGHT`, e a cauda **`@432+`**, sobre `GREEN_SOYLENT`/`STINKY_FISH`, são consumidores independentes: **não são efeitos de Bonking**. As 21 branches pertencem ao método inteiro; não são 21 condições exclusivas deste encantamento. `branch_edges` no manifesto registra cada operação de desvio e seu destino, com fallthrough implícito; não é uma enumeração completa de arestas de CFG nem sua execução.

| Porta do ramo Bonking | Offsets SHA-exatos | Consequência estática |
|---|---|---|
| Lado e vítima | `isClientSide@80`, `ifne@83 → 432`; `Mob@94`, `ifeq@97 → 432` | Exige nível não cliente e vítima `Mob`; não constitui contrato de morte de Player |
| Fonte e ator direto | `getSource@107`, `ifnull@110 → 432`; `getDirectEntity@117`, `LivingEntity@124`, `ifeq@127 → 432` | Ator direto deve ser `LivingEntity`; não consulta aqui o dono indireto de um projétil |
| Item atual | `getItemInHand@140`, `PRIMITIVE_CLUB@143`, `ItemStack.is@154`, `ifeq@157 → 432` | Testa o Primitive Club na mão principal no momento desta consulta |
| Segunda leitura e nível | `getItemInHand@164`, `BONKING@167`, `enchantLevel@170`, `ifle@173 → 432` | Lê a mão principal novamente e exige nível positivo; não conserva snapshot imutável do stack do golpe |
| Tentativa aleatória | `getRandom@183`, `nextFloat@186`, `0.33F@191`, `ifge@194 → 432` | Guard **`nextFloat < 0.33F`**, nominalmente 33% por oportunidade elegível; não é probabilidade final de cabeça |
| Creeper temporário | `CREEPER@197`, `createEntity@204`, `ifnull@214 → 432` | Referência nula evita o restante do ramo |
| Preparação de raio | `ServerLevel@228`, `ifeq@231 → 274`; `LIGHTNING_BOLT@241`, `createEntity@246`, `ifnull@256 → 274`; `setVisualOnly(true)@262`, `thunderHit@271` | Preparação condicionada do contexto de Creeper eletrificado; referência nula de raio pula esta preparação e segue para `@274` |
| Origem sintética | `DamageSources.mobAttack(fakeCreeper)@283` | Fonte passada ao callback de loot; não aplica um segundo ataque |
| Primeiro loop | `EquipmentSlot.values@303`; `if_icmpge@320 → 366`; `ac_getEquipmentDropChance@338`, `HashMap.put@346`, `ac_setDropChance(0F)@355`; `goto@363 → 316` | Salva chances anteriores e as zera por slot antes do callback |
| Callback de loot | `ac_dropCustomDeathLoot@372`; constantes `0,false@370–371` | Chama a bridge na vítima original com a origem sintética |
| Segundo loop | `EquipmentSlot.values@377`; `if_icmpge@394 → 432`; `HashMap.get@412`, `floatValue@418`, `ac_setDropChance@421`; `goto@429 → 390` | Restaura os valores salvos **no fluxo normal** após o callback |

O helper integral `ACCompat.enchantLevel`, de **24 instruções**, retorna o primeiro nível correspondente ou zero, sem clamp próprio ao máximo I e sem validar ali slot/tag. O consumidor usa apenas **`level>0`**: I e níveis positivos forçados seguem o mesmo ramo, sem multiplicador de chance, escala ou benefício de nível II demonstrados. No ramo Bonking não há requisito explícito de ator Player, allowlist de espécies, filtro de distância, seleção de vizinhos, novo ataque ou validação de proteção/claims. A elegibilidade vem da vítima e da fonte do evento. A consulta de item atual duas vezes não autentica a arma usada num golpe anterior, o dono indireto nem a aceitação final daquela morte.

O helper integral **`ACCompat.createEntity` tem quatro instruções** e delega a `EntityType.create(Level)`. O ramo Bonking não chama `addFreshEntity` para o Creeper nem para o raio: construir essas referências não demonstra inserção no mundo, projétil, hitbox adicional, raio lançado ou dano elétrico na vítima. `setVisualOnly(true)` e `thunderHit` são preparação do contexto usado no loot. Os caminhos nulos e a delegação posterior impedem tratar essa preparação como garantia de Creeper carregado efetivo ou de cabeça produzida.

Após a preparação, os papéis dos locais são **vítima original `Mob = 2`**, **ator direto `LivingEntity = 3`**, **Creeper temporário = 4**, **DamageSource sintética = 5** (`astore@286`), **mapa de chances salvas = 6** (`astore@295`) e **accessor da vítima = 7** (`astore@301`). Os locais 5/6 também servem temporariamente à preparação anterior de nível/raio; os papéis descritos valem a partir desses stores. O fake Creeper não substitui a vítima nem autentica o ator original. O `HashMap` é backup local dos slots, sem recibo persistente de Bonking.

`EntityDropChanceAccessor` declara `ac_getEquipmentDropChance(EquipmentSlot)F`, `ac_setDropChance(EquipmentSlot,float)V` e `ac_dropCustomDeathLoot(DamageSource,int,boolean)V`, sem corpos na interface. `MobMixin` implementa essa interface e tem target empacotado **`net.minecraft.world.entity.Mob`**, com quatro sombras: o campo `canPickUpLoot:Z` e os métodos `getEquipmentDropChance`, `setDropChance` e `dropCustomDeathLoot(ServerLevel,DamageSource,boolean)`. `alexscaves.mixins.json` o declara no grupo `mixins`, package `com.github.alexmodguy.alexscaves.mixin`. Os três corpos bridge completos têm **4/5/8 instruções**, respectivamente; os dois primeiros delegam getter/setter. O terceiro consulta `level@2`, faz cast para `ServerLevel@5`, carrega a fonte `aload_1@8` e o boolean `iload_3@9`, e chama o método sombreado **`@10`**. **Seu argumento `int` não é lido**: o `0` presente no callsite não é um parâmetro de looting efetivo encaminhado por esta bridge. Assinaturas, configuração, target e sombras selados não provam aplicação ou ordem do Mixin no runtime transformado.

O primeiro loop salva e zera chances de equipamento; o segundo as restaura depois do callback no fluxo normal. Há **zero entradas JVM de handlers em `livingDie`**, portanto não há `try/finally` compilado ali protegendo toda a sequência backup → zero → loot → restauração. Se uma chamada lançar exceção, ela **pode interromper** a restauração. Esta é uma **observação estática condicional de exception safety**, sem bug reproduzido, prova de corrupção permanente, garantia de rollback externo ou certificação de mutação segura. A prova tampouco executa reentrância, callbacks de terceiros ou tratamento externo de exceções.

O callback invoca a rotina de loot customizado da **vítima original**, com `mobAttack(fakeCreeper)` e boolean `false`, e mantém a implementação vanilla/modded como fronteira delegada. Não há aqui tabela de loot própria de Bonking selada como autoridade final, recibo dedicado, marcador persistente ou escrita de deduplicação. **Evento de morte, RNG aprovado, callback invocado, tabela avaliada, `ItemEntity` criado/inserido, item coletado e XP/Mastery creditados são resultados distintos.** A fonte sintética e a chamada não demonstram quantidade, tipo de cabeça, chance final, spawn aceito, coleta, crédito de kill ou recompensa única. Os `spawnAtLocation` no prefixo/cauda de `livingDie` pertencem aos outros consumidores já delimitados. O contrato não reaudita a engine base para substituir esta fronteira por uma promessa de loot final.

| Eixo obrigatório | Contrato estático individual | Fronteira de runtime/perks |
|---|---|---|
| Alvo / targeting | Vítima `Mob`, lado não cliente, fonte existente, ator direto `LivingEntity`, duas leituras de mainhand/club, nível positivo e RNG | Sem autenticação de Player, owner indireto, arma original ou morte aceita |
| Alcance / área | **N/A para Bonking**: não há busca espacial no ramo de morte; o evento fornece vítima/fonte | Não importar AoE de Dazing Sweep nem distância do golpe herdado |
| Velocidade / direção | **N/A para Bonking**: modificador de loot sem trajetória, steering ou quantidade direcional própria | Swing/Swiftwood continuam contexto separado da arma |
| Projétil / tamanho | **N/A para parâmetros próprios**: Creeper/raio são referências temporárias de contexto, com caminhos nulos | Sem projétil, spawn no mundo ou hitbox adicional certificados |
| Dano / tipo | `mobAttack(fakeCreeper)` é encaminhado somente ao callback de loot | Sem dano extra, stun, dano elétrico ou aceitação de ataque provados por Bonking |
| Duração / recursos | Oportunidade no evento, guard `0.33F`, nível sem escala; backup/restauração normal de chances de equipamento | Sem mana, XP ou cooldown próprio debitado no ramo; desgaste da arma e aquisição são separados; exceções continuam condicionais |
| Autoria / proteção / procs | Distingue vítima, ator direto, fake Creeper, stack atual e origem sintética; ausência local de recibo/deduplicação | Proteção, reentrada/replay, loot aceito, coleta, kill e XP/Mastery únicos **não certificados** |

As duas provas anteriores continuam **parciais históricas**, preservadas byte a byte: [EXACT-BONKING-1.0.10.json](EXACT-BONKING-1.0.10.json), **50.142 bytes**, SHA-256 `120704b8168411c0b5278a017e117b42f030317c326765b15a235db2a6732583`, e [EXACT-BONKING-CAUSAL-1.0.10.json](EXACT-BONKING-CAUSAL-1.0.10.json), **12.835 bytes**, SHA-256 `10d2c46fb59a9accfe6d395105840d175246b0360357f58e9c2b86d6a6d35b86`. A primeira seleciona janelas/símbolos; a segunda fixa os **21 desvios do método inteiro**, dois loops, zero handlers e as bridges, com pivôs selecionados. Nenhuma ganha retroativamente cobertura integral de instruções ou execução de CFG. Ambas usam o digest histórico de `livingDie` **`03c56101acdb5aa18c6d253f49b914bef1c1f2723aa5de548b126d4d864020dd`**; o fingerprint normalizado novo é **`40737aefdb49418028737a4b0a8ede771dd68b7baffad512769d58c66ee974cd`**. A diferença de encoding não é drift de corpo nativo. A conclusão individual pertence ao novo manifesto, sem mudar os limites, bytes ou alegações dos selos antigos.

Reprodução a partir da raiz do repositório, com **Java 21** no `PATH` e o JAR publisher identificado acima:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile bonking \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BONKING-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/bonking-evidence.json

PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_bonking_cards_test.py -v

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/qa -p 'alexscaves_1010_action_contract_audit_test.py'

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/qa -p 'alexscaves*_test.py'

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s scripts/catalog -p '*_test.py'

PYTHONDONTWRITEBYTECODE=1 python3 scripts/catalog/generate_perk_ready_indexes.py --check

PYTHONDONTWRITEBYTECODE=1 python3 scripts/catalog/check_perk_ready_indexes.py
```

Validações estáticas executadas sobre a ficha congelada e o manifesto final:

| Verificação | Resultado observado |
|---|---|
| CLI real `--profile bonking`, JAR publisher e selo final | **PASS**: 1 ficha, 6 classes com métodos + 1 interface declarativa, 11 recursos, 26 corpos/janelas e 678 âncoras; `native_metadata_checked=true` |
| Duas reconstruções completas e sequenciais após congelar a ficha | Bytes idênticos: **158.228 bytes**, SHA-256 `239d960fd09e4f01111bf981321aa75cd1746199a564943ab68c9382180e2e99` |
| Rejeições reais de CLI: promoção de hook, remoção de âncora integral, hash da interface, argumentos da anotação, target Mixin, ABI da sombra, supplier/bootstrap, fechamento indevido de registro PARTIAL, destino de branch e handlers do helper | **10/10 rejeitadas**, exit code **1**, com motivo específico |
| Auditor compartilhado | **273/273 PASS**, incluindo os **261 anteriores** e **12 novos** casos |
| Regressões semânticas e certificado/contabilidade Bonking | **29/29 PASS** |
| Duas sondas históricas de Bonking contra o publisher e seus selos preservados | **SEALED**, exit code **0**; `livingDie` 229 instruções / 21 desvios no método inteiro |
| Suíte `docs/qa/alexscaves*_test.py`, com Java 21 disponível | **1.278/1.278 PASS**, incluindo os 273 casos do auditor e 29 desta ficha |
| Suíte `scripts/catalog/*_test.py` | **165/165 PASS**; total pertinente **1.443/1.443 PASS** |
| Índices gerados e snapshot `--check` | **544 índices**, **2.393 candidatos**, **199 contratos estáticos**, **449 fichas catalogadas**, **0 erros** |

Os 273 e 29 casos já estão incluídos nos 1.278, sem soma em duplicidade. O teste Astral agora deixa a próxima ficha derivada do manifesto e do crosswalk, preservando seus testes nativos, de certificado e de limites de runtime.

As verificações acima são de catálogo, parser, fronteiras semânticas e selos; não são combate nem sessão física. A identidade completa das instruções e dos metadados não transforma referências externas em loot aceito ou hook mutador seguro.

A contabilidade individual acrescenta **+1 contrato estático** e conserva **+0 raízes mágicas**. O índice do provider passa a **61/81 fichas catalogadas**; o universo dos **51 encantamentos nativos** possui **33 contratos individuais estáticos e 18 fichas ainda parciais/condicionadas**. O próximo ID alfabético pendente é **`alexscaves:bouncing_bolt`**. Esses números não encerram o provider, o equipamento ou as oito raízes mágicas.

A integração permanece somente de catálogo. Black Arcana conserva seu runtime mágico, Alex's Caves conserva a morte/loot nativos e RPG Skill Tree conserva progressão, atributos e Mastery. Enshrouded/RPG Skill Tree exigem boundary demonstrado no servidor, owner autorizado e crédito único depois do resultado válido; observar `LivingDeathEvent`, a fonte sintética ou o callback não satisfaz esse contrato. Não reexecutar loot nativo, simular outro Creeper, editar chances de equipamento ou conceder drops/XP/Mastery para reproduzir Bonking.

QA física permanece pendente para níveis **0/I/forçados**, tag/acquisition/datapacks efetivos, cliente/dedicado, ator direto vs projétil/dono indireto, troca de mão/stack entre golpe e morte, cancelamento/ordem de listeners, aplicação/ordem de Mixin, entidades com/sem cabeça, nulos na criação de entidades temporárias, loot vanilla/modded, equipamentos com chances customizadas antes/depois, exceções/reentrância/rollback, múltiplos jogadores e replay, proteção/claims, morte/unload/reload/dimensão, spawn/coleta reais e crédito único de kill/XP/Mastery. Esta pendência limita alegações físicas e hooks mutadores; não impede a conclusão **estática individual** nos limites documentados. Estado final: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, **`NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`**, **+0 raízes mágicas** e **+0 providers encerrados**.
