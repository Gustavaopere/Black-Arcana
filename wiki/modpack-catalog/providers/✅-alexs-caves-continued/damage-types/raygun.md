# Raygun — tipo de dano `alexscaves:raygun` e contrato nativo do item (1.0.10)

**Estado de catalogação:** ✅ contrato técnico estático individual certificado nos **sete eixos**, com recurso, factory e comportamento dos **26 métodos declarados de `RaygunItem`**. **Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY`. **Hook mutador:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Certificação de perks executáveis:** `NOT_CERTIFIED`. **Integração:** `NO_MUTATION`. **Universo do provider:** aberto.

A Raygun é um item de uso mantido que calcula traces e consulta candidatos para dano; esta ficha reúne seu DamageType, carga, munição, lifecycle, targeting, efeitos, animação e UI. O [selo individual](../EXACT-RAYGUN-CONTRACT-1.0.10.json), a [prova reproduzível](../EXACT-RAYGUN-CONTRACT-1.0.10.md) e o [auditor](../../../../../docs/qa/alexscaves_1010_raygun_contract_audit.py) compõem os contratos já certificados de [Energy Efficiency](../enchantments/energy-efficiency.md), [Solar](../enchantments/solar.md), [Gamma Ray](../enchantments/gamma-ray.md) e [X-Ray](../enchantments/x-ray.md). Fingerprints identificam corpos; as relações causais e os limites descritos abaixo constituem o contrato estático.

O [arquivo histórico da ficha](EXACT-RAYGUN-HISTORICAL-CARD-1.0.10.md) preserva, sem reescrita, os checkpoints parciais anteriores: SHA-256 `75f033bc9c27195c85ca952e0b70bc18ff00f5f1aba1955e58242c98c11e0f87`. Seus estados e contadores registram aquela etapa. O presente contrato substitui a conclusão parcial para o recorte estático individual, sem promover hooks, QA física ou o provider integral.

## 1. Identidade, recurso e fonte de dano

| Campo | Identidade publisher auditada |
|---|---|
| Provider / mod ID | Alex's Caves Continued / `alexscaves` |
| Runtime | Minecraft **1.21.1**, NeoForge, Java **21** |
| JAR da modlist | `alexscaves-1.0.10-neoforge+1.21.1.jar`; CurseForge arquivo **8856293**; **75.279.314 bytes** |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| DamageType / item | `alexscaves:raygun`; registros de tipos diferentes com o mesmo ID textual |
| Recurso do DamageType | `data/alexscaves/damage_type/raygun.json` |
| JSON SHA-256 | `dc1095e92e0695b302100993af8fafd72c8d6b948d90717e667a6ced2ae1bc35` |
| Classe do item | `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class` |
| Classe do item SHA-256 | `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| Classe da factory SHA-256 | `ACDamageTypes.class`: `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6` |
| Universo de métodos próprios | **26 métodos**, **1.111 instruções JVM**, **107 branches diretos**; `onUseTick` contém 523 instruções e 57 branches |

A fonte pública [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e serve somente como referência adjacente. Os valores desta ficha vêm do binário publisher **1.0.10** SHA-exato; não se presume equivalência entre versões.

| Campo literal do JSON | Valor | Significado delimitado |
|---|---|---|
| `message_id` | `raygun` | Identificador da mensagem de morte |
| `scaling` | `never` | Política declarativa do DamageType; não fixa dano, críticos ou curva de perks |
| `exhaustion` | `0.3` | Exaustão do tipo de dano; não é mana, stamina ou custo do item |
| Tags diretas | `minecraft:bypasses_cooldown`, `minecraft:is_explosion`, `minecraft:is_projectile` | Entradas textuais publisher; não certificam tags finais resolvidas por datapacks |

`bypasses_cooldown` classifica o dano no Minecraft; não configura cooldown de casting. `is_projectile` e `is_explosion` não instanciam projétil ou explosão de mundo. O [manifesto de recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e o [manifesto de consumidores](EXACT-CONSUMERS-1.0.10.json) preservam a origem desses dados.

`ACDamageTypes.causeRaygunDamage(RegistryAccess,Entity)` obtém o registro `DAMAGE_TYPE`, resolve o holder de `RAYGUN` (`@19–22`) e constrói `DamageSourceRandomMessages(holder,entity,1)` (`@27–29`). O construtor com entidade delega ao `DamageSource(Holder,Entity)` e armazena a quantidade de variantes de mensagem. Em `RaygunItem.onUseTick @1026`, o argumento Entity é o **usuário do item**. O censo do binário localiza um callsite direto dessa factory, em uma classe; isso não conta hits por uso. Crédito final de kill, PvP, procs e Mastery dependem dos consumidores e do modpack. O descritor JVM da factory é `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`; o caller direto selado é `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`.

## 2. Comportamento dos 26 métodos próprios

`RaygunItem` estende `Item` e implementa `UpdatesStackTags`, `AlwaysCombinableOnAnvil`, `ACClientExtensionItem`, `ACEnchantableItem` e `ACTickingItem`. Métodos de interfaces, engine, proxy e eventos mantêm seus owners. O [selo de identidade dos 26 corpos](../EXACT-RAYGUN-ALL-METHODS-1.0.10.json) é reutilizado pelo selo atual; a tabela dá uma disposição comportamental a **cada** método, sem tratar seus hashes isolados como prova de gameplay.

| Método próprio | Papel e contrato estático |
|---|---|
| `RaygunItem()` | Cria `Item.Properties().stacksTo(1)` e chama o construtor de `Item`; nenhuma reserva própria de mana ou timer é inicializada |
| `initializeClient(Consumer)` | Entrega ao consumer as propriedades de renderer obtidas por `PROXY.getISTERProperties()`; delegação visual |
| `getEnchantmentValue()` | Retorna **1**, valor nativo de encantabilidade |
| `isEnchantable(ItemStack)` | Retorna verdadeiro quando `stack.getCount()==1` |
| `hasCharge(ItemStack)` | Retorna `getCharge(stack)<1000`, sem clamp inferior próprio |
| `use(Level,Player,Hand)` | Inicia uso quando há carga; esgotado, tenta recarga criativa/munição, sons e retorno de falha da interação; detalhado abaixo |
| `findAmmo(Player)` | Creative retorna `EMPTY`; nos demais casos percorre o inventário e retorna a primeira stack aceita por `AMMO`, ou `EMPTY` |
| `getUseAnimation(ItemStack)` | Retorna `UseAnim.NONE`; render/animação próprios usam os campos e helpers abaixo |
| `getUseDuration(ItemStack,LivingEntity)` | Retorna **72000 ticks**, limite declarado de uso mantido |
| `acInventoryTick(ItemStack,Level,Entity,boolean)` | Servidor: recuperação Solar condicionada. Cliente: atualização de `PrevUseTime` e subida/descida de `UseTime` |
| `onUseTick(Level,LivingEntity,ItemStack,int)` | Calcula progresso/distância, bloqueia carga esgotada, atualiza estado/consumo cliente, seleciona targeting e solicita dano/status no servidor |
| `setUseTime(ItemStack,int)` | Copia o `UseTime` anterior para `PrevUseTime`, grava o inteiro recebido e reaplica a tag; sem clamp próprio |
| `setRayPosition(ItemStack,double,double,double)` | Copia a posição anterior para `PrevRayX/Y/Z`, grava `RayX/Y/Z` recebidos e reaplica a tag; sem clamp de coordenadas próprio |
| `getUseTime(ItemStack)` | Lê `UseTime`; tag ausente retorna **0** |
| `getCharge(ItemStack)` | Lê `ChargeUsed`; tag ausente retorna **0** |
| `setCharge(ItemStack,int)` | Grava o inteiro recebido em `ChargeUsed` e reaplica a tag; sem clamp próprio |
| `getRayPosition(ItemStack)` | Com tag e chave `RayX`, lê o vetor `RayX/Y/Z`; nos outros caminhos retorna `Vec3.ZERO` |
| `getLerpedUseTime(ItemStack,float)` | Retorna `prev+partial×(current−prev)`; valores ausentes usam zero; não limita `partial` neste corpo |
| `getLerpedRayPosition(ItemStack,float)` | Sem tag retorna **null**; com tag interpola cada coordenada anterior/atual, após estreitamento **double→float→double** dos valores lidos |
| `releaseUsing(ItemStack,Level,LivingEntity,int)` | Chama `Item.releaseUsing`; no cliente envia atualização de tags; limpa o cache de som pelo proxy. Não zera charge, tempos ou posição neste corpo |
| `isBarVisible(ItemStack)` | Mostra a barra quando `ChargeUsed!=0`, inclusive para valores forçados fora da faixa normal |
| `getBarWidth(ItemStack)` | Retorna `round(13F−ChargeUsed×13F/1000F)`; sem clamp próprio da largura |
| `getBarColor(ItemStack)` | Calcula cor HSV pulsante com charge e tempo do proxy; é feedback de UI, sem gasto ou dano |
| `appendHoverText(...)` | Para charge diferente de zero adiciona `item.alexscaves.raygun.charge`, verde, com valores **1000−ChargeUsed** e **1000** |
| `shouldCauseReequipAnimation(old,new,slotChanged)` | Retorna falso quando ambas as stacks são o item Raygun; retorna verdadeiro nos demais casos. `slotChanged` não participa da decisão própria |
| `lambda$static$0(ItemStack)` | Compara o item da stack com `URANIUM_ROD.asItem()`; predicado de identidade da munição |

O censo soma **26 métodos próprios**, incluindo construtor e predicado sintético; **exclui o inicializador `static {}`**. Esse inicializador instala o predicado em `AMMO`, sem criar reserva de carga ou contador por stack, e recebe prova separada em `static_initialization`. Os descritores, corpos selados e pivôs dos 26 métodos estão em `method_dispositions` do [contrato JSON](../EXACT-RAYGUN-CONTRACT-1.0.10.json).

## 3. Uso, carga, munição e encerramento

Defina **D=`ChargeUsed`**, o consumo acumulado da stack. D=0 representa a posição lógica de carga plena; `hasCharge` aceita **D<1000**. Os setters nativos gravam valores brutos: a invariância `0≤D≤1000` não é garantida por `setCharge` isolado. Não transferir essa responsabilidade a uma perk nem anunciar saneamento universal do estado.

| Caminho de `use` | Sequência causal |
|---|---|
| Há carga, `@7–40` | `hasCharge=true` → `startUsingItem(hand)` → som `RAYGUN_START` → `ACCompat.useConsume(stack)` |
| Esgotado, `@41–79` | Busca `findAmmo`; inicializa elegibilidade com `Player.isCreative`; uma stack não vazia sofre `shrink(1)` e torna a recarga elegível; elegível solicita `setCharge(stack,0)` |
| Recarga elegível, `@82–122` | Solicita som `RAYGUN_RELOAD`; não chama `startUsingItem` nesse ramo |
| Sem recarga, `@125–162` | Solicita som `RAYGUN_EMPTY` |
| Saída de ambos os ramos de recarga, `@165–170` | Retorna `ACCompat.useFail(stack)`, inclusive após o reset de carga; não começa automaticamente o disparo nesse callback |

`findAmmo` procura em ordem de índices de `Inventory.getContainerSize/getItem`; o primeiro predicado positivo é o item de **`URANIUM_ROD`**, não combustível genérico. No modo Creative o helper retorna vazio, mas a flag separada em `use` permite resetar a carga sem consumir rod. O débito de **uma unidade** é da recarga elegível, não de cada callback, alvo ou hit. Esse corpo não acrescenta um gate próprio de lado lógico; a execução e aceitação reais da interação continuam dependentes do dispatcher.

Em `onUseTick @139–209`, a falta de carga leva, no cliente, ao envio de `UpdateItemTagMessage`; em seguida o fluxo solicita `stopUsingItem`, som de vazio e retorna antes do restante da ação. `releaseUsing` chama a implementação de `Item`, envia a mensagem somente no cliente (`@13–28`) e chama `PROXY.clearSoundCacheFor(usuario) @35`. Não há reset local explícito de `ChargeUsed`, `UseTime` ou `RayX/Y/Z` na liberação. O decaimento visual ocioso pertence ao callback de inventário, não a um novo timer de spell.

**Uso máximo de 72000 ticks, recarga, consumo e cadência de dano são superfícies separadas.** Nenhum dos corpos próprios declara cooldown de casting, custo de mana/stamina, vida de projétil, contador de casts ou custo adicional por Gamma/X-Ray. Acesso a um método público não constitui hook mutador seguro.

### Consumo durante uso — Energy Efficiency

Em `onUseTick`, **T=`getUseDuration(stack,null)−remainingUseTicks`**. O progresso **p=T/15F se T<15; caso contrário p=1F** (`@11–33`) não tem clamp inferior próprio. A distância calculada é **r=25F×p** (`@35–41`). A rampa de 15 ticks controla o progresso e o gate de gasto; não impõe sozinha um atraso mínimo ao dano do servidor.

O ramo de custo é **cliente** (`@210–319`). Com nível `L` de Energy Efficiency, calcula **I=2+floor(1.5F×L)**. Para níveis normais não negativos 0/1/2/3/4, os intervalos aritméticos são **2/3/5/6/8 ticks**. Só solicita gasto com **p≥1**, **T%I==0** e usuário que não seja Player Creative. A escrita desse caminho é **D'=min(D+1,1000)**: há clamp superior no consumidor, sem alterar o caráter bruto de `setCharge`.

O intervalo é uma oportunidade de débito condicionada aos guards; não é intervalo de dano ou prova de cobrança autenticada no servidor. O [contrato causal de Energy Efficiency](../EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json) e o [selo de charge/cost](../EXACT-RAYGUN-CHARGE-COST-1.0.10.json) preservam fórmula e branches, incluindo a independência da cadência ofensiva.

### Inventário e recuperação Solar

`acInventoryTick` calcula `usingThisStack`: para LivingEntity compara `living.getUseItem().equals(stack)`; para outro Entity usa falso. O parâmetro `selected` não é usado como guarda própria. O despacho `ItemStackTickMixin` → `ACTickingItem` e o helper solar são selados no [contrato Solar](../EXACT-SOLAR-STATIC-1.0.10.json).

No **servidor** (`@38–143`), a recuperação exige cumulativamente: Solar de nível positivo, stack fora do uso calculado, **D>0**, `nextFloat()<0.02F`, `canSeeSky(entity.blockPosition().above())`, `isDay()`, dimensão sem horário fixo e `ACCompat.sunAboveHorizon`. O proc solicita **D'=D−1** e **`setUseTime(stack,0)`**. O helper solar testa `getTimeOfDay(1F)<0.259F` ou `>0.74F`; isso não substitui o gate separado de dia. A chance é por callback elegível, sem taxa física garantida em segundos ou escala pelo nível.

No **cliente** (`@146–230`), o callback sincroniza o marcador anterior e eleva `UseTime` de uma unidade enquanto a stack é a de uso e o tempo lido é menor que **5**; fora de uso, diminui uma unidade quando o tempo é positivo. Esses guards operam sobre o estado lido; não são saneamento universal de valores forçados. Solar não cria novo ataque, mana, spell, projétil ou recibo de Mastery.

## 4. Targeting, geometria e cadência ofensiva

O [contrato causal X-Ray](../EXACT-XRAY-CAUSAL-1.0.10.json) fecha os ramos compartilhados de targeting. **X-Ray positivo** é um booleano transitório no local 9, relido da stack por callback; nível acima de I não multiplica r nesse corpo. O recurso publisher de X-Ray exclui Gamma, mas o código não impõe essa exclusão a uma stack cuja coexistência tenha sido forçada.

| Etapa de `onUseTick` | Seleção estática |
|---|---|
| Trace inicial, `@60–83` | Local 10 recebe `ProjectileUtil.getHitResultOnViewVector(usuario,predicate,r)`; local 11 recebe **outro** resultado, `usuario.pick(r,0F,false)` |
| Extremo geométrico, `@85–103` | Local 12=`eyePosition+getViewVector(0F)×r` |
| Extremos iniciais, `@105–137` | Locais 13 e 14 recebem local 12 com X-Ray; sem X-Ray recebem **local11.getLocation()** |
| Extremo visual, `@217–233` | Cliente escreve o local 13 em `setRayPosition`; isso ocorre antes da busca segmentada e não confirma o centro final do dano |
| Busca X-Ray, `@569–666` | Caixa do usuário inflada por r; contador **float** inicia em 1F e continua enquanto `<r`; avança a posição por `getViewVector(1F)` e consulta o segmento até posição+outro vetor de visão |
| Saída do laço | Primeiro retorno não nulo substitui local 10 e encerra a busca; se todos forem nulos, conserva o resultado inicial de `@69` |
| Bloco sem X-Ray, `@669–732` | `BlockHitResult`, bloco não ar e face sturdy preparam posição/direção de impacto visual. Não reescrevem o local 14 nesse ramo |
| Resultado de entidade, `@734–766` | Usa **`getEntity().position()`**, define direção `UP` e substitui local 14 pela posição da entidade; não é necessariamente o ponto de interseção do trace |
| Consulta final, `@891–951` | `AABB(local14−(1,1,1),local14+(1,1,1))`: **cubo de lado 2**; consulta `Level.getEntities(usuario,box,Entity.canBeHitByProjectile)` |
| Filtros por candidato, `@975–1008` | Exclui identidade do usuário, aliança alvo→usuário, aliança usuário→alvo e mesmo veículo |

O primeiro segmento adicional X-Ray começa em olho+view(1F), até esse ponto+view(1F); o laço não adiciona um primeiro segmento olho→olho+view. Para r=25F, o caminho sem retorno não nulo pode consultar contadores 1F…24F; **24 consultas não são 24 hits**. Com r≤1F o corpo do laço não executa. A seleção não compara por conta própria uma entidade globalmente mais próxima entre todos os segmentos. Os internos de `ProjectileUtil`, a ordem de resultados e a penetração física de materiais específicos permanecem fora desse corpo.

O cubo final, a caixa de busca inflada, r e o extremo visual são medidas distintas. A consulta pode enumerar vários candidatos; não há quota literal de vítimas nesse laço. Não se deduz esfera, cone, largura de feixe, hitbox de projétil ou alcance físico universal do literal 25. O predicado e os filtros descritos não homologam proteção de PvP/claims ou tags finais do mundo.

**Gate servidor de dano:** `!isClientSide && (T−15)%3==0` (`@874–888`). **Não existe condição adicional T≥15 nesse gate.** A congruência admite oportunidades em **0/3/6/9/12**, além de 15 e seguintes, se o callback e os demais gates forem alcançados. Não anunciar “15 ticks sem dano” nem derivar DPS garantido: consulta, tentativa, dano aceito e número de candidatos são resultados separados.

## 5. Dano direto, Irradiated, Gamma e feedback

| Etapa por candidato | Contrato estático |
|---|---|
| Fonte direta, `@1026` | `causeRaygunDamage(registryAccess,usuario)` com o usuário do item |
| Dano solicitado, `@1029–1041` | **1.5F sem Gamma positivo; 2F com Gamma positivo**, passados a `ACCompat.hurt` |
| Exceção Tremorzilla, `@1013–1052` | `TremorzillaEntity` pula `hurt` e seleciona verdadeiro para a continuação; para outros alvos, `hurt=false` bloqueia essa continuação na mesma iteração |
| Guardas de status, `@1054–1088` | Continuação verdadeira, alvo `LivingEntity` e tipo fora da tag resolvida `RESISTS_RADIATION` |
| Efeito solicitado, `@1091–1119` | `Irradiated` por **800 ticks**, amplifier **0 sem Gamma / 4 com Gamma** |
| Confirmação do status, `@1122` | `addEffect=false` bloqueia o pacote visual |
| Feedback, `@1125–1154` | `UpdateEffectVisualityEntityMessage(targetId,usuarioId,4/0,800)` enviado somente após `addEffect=true` |

Os branches de Gamma consultam nível positivo; RNG visual não decide a presença de Gamma ou a seleção de 1.5F/2F. A tag publisher `resists_radiation` inclui **Tremorzilla, Nucleeper, Radgill, Brainiac, Gammaroach e Raycat**. Assim, o desvio de `hurt` não basta para aplicar Irradiated à Tremorzilla com os dados empacotados. O runtime consulta a tag resolvida; overrides não foram testados.

O [contrato Gamma](../EXACT-GAMMA-RAY-CAUSAL-1.0.10.json), o [selo pós-hurt](../EXACT-RAYGUN-POST-HIT-GUARDS-1.0.10.json) e as [guardas de radiação](../EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) distinguem tentativa de dano, retorno de `hurt`, resistência, retorno de `addEffect` e envio visual. Mitigação, críticos, imunidades da engine, duração efetiva e entrega de mensagens não são aprovados por esses argumentos de chamada.

**DoT tem outro contrato e outra fonte.** [Irradiated](../effects/irradiated.md) usa [Radiation](radiation.md), cuja factory `causeRadiationDamage(RegistryAccess)` não recebe caster. No tick próprio de Irradiated, amplifier a≤0 não executa o efeito periódico; para a>0 calcula j=200/a inteiro e usa fase `duration%j==j/2` quando j>1, ou todos os ticks quando j≤1. Gamma solicita a=4, portanto j=50 e fase 25, ainda sujeito a Hazmat, exclusão Raycat e RNG. A presença de amplifier 0 pode ter outros consumidores. Não transferir automaticamente o caster direto a kill, lifesteal, XP ou Mastery do dano periódico.

### Animação, partículas e UI

`initializeClient` delega o renderer ao proxy. Os campos `UseTime/PrevUseTime` e `RayX/Y/Z/PrevRayX/Y/Z` alimentam interpolação visual, com os fallbacks da tabela de métodos. O contrato Gamma sela também os consumidores compartilhados `ACItemstackRenderer.renderByItem` e `RaygunRenderHelper.renderRaysFor`: variantes azuis de textura/feixe pertencem à seleção Gamma. A ficha não certifica pixels ou toda a implementação gráfica desses owners.

`onUseTick @348–566` seleciona partículas por Gamma, sorteio e progresso; chama `Level.addParticle` com o extremo visual e offsets próprios. `@768–871` solicita `RAYGUN_BLAST` quando existe posição de impacto e T é par, deslocado na direção por `0.05F+nextFloat()×0.09F`. A ausência dessa posição pula o feedback, **não bloqueia a consulta final de dano**. Partícula de explosão não é chamada de explosão de mundo ou recibo de hit. O proxy recebe `playWorldSound(usuario,8)` no ramo cliente.

A barra usa largura `round(13F−D×13F/1000F)`. Na cor, define f=2F×D/1000F e tempo do proxy t=`playerTime+partialTicks`; o pulso é `0.5F×(1+sin(t×f))`, passado a `hsvToRgb(0.3F,0.2F+0.6F×pulso,1F)`. Tooltip apresenta 1000−D sobre 1000 quando D≠0. São leituras de UI sem clamp próprio para estados forçados; não são setters de capacidade ou confirmação de carga remota.

### Anvil e reparo

`AlwaysCombinableOnAnvil` é um marcador vazio, implementado pela Raygun; não é um dos 26 métodos próprios. O consumidor delimitado `CommonEvents.onUpdateAnvil` testa o marcador, mesmo item e ambos os itens encantados antes do caminho que copia a stack esquerda e combina encantamentos. Essa delegação não contém chamada de reposição de carga da Raygun no caminho selado. **Combinação de encantamentos em anvil, recarga por Uranium Rod e reparo de durabilidade são contratos distintos.** A Raygun não declara método próprio de reparo nem consumo de durabilidade nos corpos auditados; não anunciar Uranium Rod como reparo de durabilidade ou converter `anvil_cost` de encantamentos em custo de disparo. Regras completas de reparo da engine e overrides de mods permanecem externas.

## 6. Estado persistível, rede e fronteira de integração

As chaves nativas são `ChargeUsed`, `UseTime`, `PrevUseTime`, `RayX/Y/Z` e `PrevRayX/Y/Z`. Os setters passam por `ACCompat.getOrCreateTag` e `ACCompat.setTag`, cuja delegação usa `DataComponents.CUSTOM_DATA`. Esse caminho identifica o recipiente persistível; não prova conservação, ordenação de escritas, rollback, reconciliação ou cleanup físico após morte, troca de mão/slot, unload, dimensão, reconnect ou save/reload.

| Boundary já auditada | Resultado estático e limite conservado |
|---|---|
| Sender de tags | `onUseTick @162/165` no esgotamento cliente e `releaseUsing @25/28` constroem/enviam `UpdateItemTagMessage(entityId,stack)` |
| Receiver | Há resolução por entityId, seleção de mãos por igualdade de item e chamada condicionada de `UpdatesStackTags.updateTagFromServer`; ter um destino identificado não autentica o remetente |
| Interface e callback default | Raygun implementa diretamente `UpdatesStackTags`, sem override próprio; o método default encaminha a tag a `ACCompat.setTag`, que grava/remove `CUSTOM_DATA` |
| Codec | Leitura/escrita de entityId e ItemStack encaminhadas pelos helpers identificados; limites efetivos dos codecs Minecraft e aceitação do payload completo continuam delegados/sem homologação |
| Autoridade real | `network_authorization=NOT_VERIFIED`: vínculo remetente/entityId, autorização de mãos, saneamento por chave, antirreplay/rate-limit e resultados do mundo não são certificados |

As provas de [receptor](../EXACT-RAYGUN-RECEIVER-1.0.10.json), [identidade](../EXACT-RAYGUN-RECEIVER-IDENTITY-1.0.10.json), [CFG condicional do receptor](../EXACT-RAYGUN-RECEIVER-CFG-1.0.10.json), [ABI de rede](../EXACT-RAYGUN-NETWORK-ABI-1.0.10.json), [codec](../EXACT-RAYGUN-PACKET-CODEC-1.0.10.json) e [helper ItemStack](../EXACT-RAYGUN-ITEMSTACK-HELPER-1.0.10.json) preservam seus escopos. O contrato estático registra essa delegação conhecida; não reabre a auditoria integral da rede nem infere vulnerabilidade ou autorização segura. Carga enviada pelo cliente não é recibo autenticado de custo.

**Campos próprios N/A:** entidade de projétil, quantidade/velocidade/homing/dimensões/vida de projétil; summon/familiar; cura; mana/stamina; cooldown de casting; timer autônomo de spell; mutação de blocos e explosão de mundo nos métodos próprios auditados. O feixe usa traces e consultas, sem spawn próprio de projétil nesse conjunto. `is_projectile`/`is_explosion` são classificações do DamageType. Uso de 72000 ticks, rampa de 15, cadência de 3, animação até 5 e status de 800 pertencem a sistemas diferentes e não preenchem esses campos por analogia.

Alex's Caves conserva o settlement nativo de uso, charge, targeting, fonte, aceitação, status e visuais. Black Arcana governa seu runtime mágico; RPG Skill Tree integra atributos, perks e Mastery por contratos reais no projeto dono. Distância calculada, volume da consulta, predicado, dano solicitado, período EE e chance Solar são parâmetros documentados, **sem seam mutador homologado**. Nenhum setter público autoriza adapter imaginário, reemissão de pacote, segunda cobrança ou double-processing. Callback, candidato, segmento, partícula, tentativa de hurt e pacote não representam um cast/hit/kill único para XP.

## 7. Sete eixos, reprodução e limites finais

| Eixo da rubrica | Contrato técnico estático certificado | Fronteira preservada |
|---|---|---|
| **Identidade** | Recurso/tags diretas, item, factory, JAR e classes SHA-exatos | Fonte 1.1.1 adjacente; tags/datapacks efetivos sem QA |
| **Comportamento** | Disposição dos 26 métodos; lifecycle de uso/recarga/liberação; callbacks Solar e visuais; fonte e status | Dispatch externo e resultados físicos não são inferidos dos fingerprints |
| **Parâmetros** | D<1000, uso72000, p/r, EE, Solar, dano/status, interpolação/UI e campos próprios N/A | Valores são argumentos/cálculos nativos, sem hook mutador ou clamps globais presumidos |
| **Targeting** | Traces distintos, X-Ray primeiro retorno/fallback, centro local14, cubo±1, predicado e filtros | Alcance físico, nearest global, materiais, LOS, PvP e claims sem homologação |
| **Custos/tempo** | Recarga por uma rod/Creative, charge cliente sob EE, recuperação Solar servidor; cadência ofensiva independente | Sem mana extra, cooldown inventado, cobrança duplicada ou carga C2S autenticada |
| **Integração** | Owners item/factory/efeito/UI/anvil/rede delimitados; Raygun direta e Radiation periódica separadas | `NO_MUTATION`; autoria de kill/XP/Mastery e deduplicação executável não certificadas |
| **Validação** | Extração do JAR, censo26/1111/107, pivôs por método e composição dos contratos EE/Solar/Gamma/X-Ray | `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`; provider aberto |

A [prova individual](../EXACT-RAYGUN-CONTRACT-1.0.10.md) registra os resultados efetivamente executados. O [auditor de contrato](../../../../../docs/qa/alexscaves_1010_raygun_contract_audit.py) e o [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-raygun-contract.yml) confrontam o JAR exato, recurso, classe, todos os métodos e disposições/pivôs, compondo os selos anteriores em seus escopos. O [fluxo de charge/munição](../EXACT-RAYGUN-CHARGE-AMMO-FLOW-1.0.10.json) fixa oito métodos, 168 instruções e 15 branches; o contrato atual dá contexto causal ao conjunto de 26, sem contar corpos compartilhados em duplicidade. Uma execução local ou da CI valida a prova estática, não combate em jogo.

**QA física pendente (`NOT_TESTED`):** Survival/Creative; carga0/999/1000 e valores forçados; recarga e nova interação; tempo antes/depois15 e diferentes níveis EE; Solar fora/em uso, céu/dimensão e concorrência com gasto; X-Ray primeiro segmento/fallback, obstáculos, extremos e entidades de tamanhos diversos; múltiplos candidatos, aliados e veículos; Gamma e coexistência forçada; Tremorzilla/resistência publisher e override; `hurt=false`, `addEffect=false`, status anterior e Hazmat; troca de mão/slot, liberação e cache de som; cliente/servidor dedicado, latência, mensagens, reconnect, morte, unload, dimensão e save/reload; datapacks, PvP/claims e crédito único de kill/XP/Mastery. Nenhum cenário recebe PASS por inspeção estática.

**Estados finais:** `static_technical_contract=CERTIFIED_STATIC_7_AXES`, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `network_authorization=NOT_VERIFIED`, `mutation=NO_MUTATION`, `provider_universe_closed=false`.

**Contabilidade:** **+1 contrato técnico estático individual**, **+0 fichas novas**, **+0 raízes mágicas**, **+0 hooks homologados**, **+0 QA física**, **+0 providers encerrados**, **+0 promoção de Stage**. O recorte de encantamentos publisher permanece **51/51**; o recorte observado do provider alcança **81/81 fichas certificadas**. Outras famílias do inventário ainda não foram individualizadas: o universo integral permanece **OPEN**, sem avanço automático para o próximo provider alfabético.
