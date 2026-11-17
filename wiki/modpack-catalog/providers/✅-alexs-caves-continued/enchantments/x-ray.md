# X-Ray — seleção de extremos e busca de entidades da Raygun (1.0.10)

**Contrato técnico estático individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Integração executável:** `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`. O recorte fecha os sete eixos documentais de `alexscaves:x_ray` no publisher SHA-exato **1.0.10**. A [Raygun](../damage-types/raygun.md) e o universo integral do provider conservam seus escopos abertos. O [DamageType Tremorzilla Beam](../damage-types/tremorzilla-beam.md) já possui certificado estático individual, sem encerrar a entidade Tremorzilla inteira.

X-Ray é um encantamento nativo da Raygun. **Nível positivo** escolhe o extremo geométrico calculado pelo item para os locais 13/14 e habilita uma busca segmentada de entidades. O primeiro retorno não nulo dessa busca substitui o resultado de trace inicial; um resultado final de entidade reposiciona o centro da consulta de dano na **posição da entidade**. Esses fatos não são uma garantia de atravessar qualquer parede, selecionar a entidade globalmente mais próxima, atingir todas as entidades do feixe ou vencer proteção PvP/claims. Nenhuma nova raiz mágica é criada.

## 1. Identidade e autoridade das fontes

| Objeto | Evidência publisher 1.0.10 |
|---|---|
| Provider / mod ID | Alex's Caves Continued / `alexscaves` |
| Plataforma | Minecraft 1.21.1 / NeoForge / Java 21 |
| Mod instalado | `alexscaves-1.0.10-neoforge+1.21.1.jar`, entrada 019 da [modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md) |
| Artefato publisher | [CurseForge, arquivo 8856293](https://www.curseforge.com/minecraft/mc-mods/alexs-caves-continued/files/8856293), **75.279.314 bytes** |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Identidade / símbolo | `alexscaves:x_ray` / `ACEnchantmentRegistry.X_RAY` |
| Recurso individual | `data/alexscaves/enchantment/x_ray.json`, **406 bytes**, SHA-256 `612b1f7b126cea12085dea00736115b05fd4789bf9fc9ff6c4344a427135b0f8` |
| Consumer | `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`, SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| Método principal | `onUseTick(Level,LivingEntity,ItemStack,int)V`; descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V` |
| Corpo compilado | **523 instruções**, **57 branches diretos**; SHA-256 canônico do parse `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5` |

**Prova individual:** [manifesto causal X-Ray](../EXACT-XRAY-CAUSAL-1.0.10.json), [reprodução e limites](../EXACT-XRAY-CAUSAL-1.0.10.md), [auditor SHA-exato](../../../../../docs/qa/alexscaves_1010_xray_causal_audit.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-xray-causal.yml). A extração nova do JAR físico substitui a limitação de janelas isoladas desta ficha anterior; não transforma inspeção JVM em QA de combate.

O selo compõe as provas de [Gamma Ray](../EXACT-GAMMA-RAY-CAUSAL-1.0.10.json) e [Energy Efficiency](../EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json), que já identificam o mesmo corpo integral de 523 instruções/57 branches e **12 corpos causais selecionados**, incluindo os helpers de nível, charge, dano, fontes e Irradiated. Os consumidores visuais selados por Gamma também são preservados no contrato herdado. Essa reutilização mantém suas fronteiras: não torna todos os métodos da Raygun, o renderizador inteiro ou a autorização C2S certificados.

O censo literal de `X_RAY` no JAR encontra somente **`ACEnchantmentRegistry.class` e `RaygunItem.class`**. O registro declara a identidade; a lógica própria selecionada está em `onUseTick`. Não se excluem consumidores por reflexão, mixins externos ou outros mods a partir de um censo literal.

A [wiki comunitária](https://alexscaves.wiki.gg/wiki/Raygun#Enchantments) oferece contexto funcional. A fonte adjacente [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1**: serve para localizar candidatos, sem autoridade numérica ou presunção de paridade com o publisher **1.0.10**.

## 2. JSON, aquisição e leitura do nível

| Campo | Valor publisher | Interpretação delimitada |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.x_ray` | Identidade da localização |
| `supported_items` | `#alexscaves:enchantable/raygun` | Tag física contém somente `alexscaves:raygun` |
| `weight` | `10` | Peso declarativo de aquisição, não probabilidade de acerto |
| `max_level` | `1` | Nível I declarado |
| `min_cost` | base `1`, incremento `12` | `1+12×(L−1)`; no nível I: **1** |
| `max_cost` | base `41`, incremento `10` | `41+10×(L−1)`; no nível I: **41** |
| `anvil_cost` | `1` | Custo do sistema de encantamento, não custo por disparo |
| `slots` | `["mainhand"]` | Slot declarado no recurso |
| `exclusive_set` | `["alexscaves:gamma_ray"]` | Exclusão declarada pelo próprio JSON de X-Ray |
| `effects` | Ausente | Comportamento observado no consumidor compilado |

A tag `data/alexscaves/tags/item/enchantable/raygun.json` tem **46 bytes**, SHA-256 `8e7cb71ff2c706004fba0493f2237e96da3af53dea6e3ae414542b5150cc012d`. Dados publisher não comprovam tags efetivas do mundo, aquisição em mesa/bigorna, troca de mãos ou comportamento de stacks modificadas por comandos/datapacks.

`gamma_ray.json` é outro recurso e não declara `exclusive_set` próprio. O consumer lê Gamma e X-Ray separadamente: não há nesse corpo um gate que rejeite a coexistência forçada dos dois. A intenção declarativa de exclusividade não é uma prova de que todos os caminhos de obtenção apliquem a restrição em runtime.

`ACCompat.enchantLevel` retorna o inteiro da entrada correspondente da stack, ou 0 quando ausente. `X_RAY @44` → `enchantLevel @47` → `ifle @50` seleciona **1 se nível>0; 0 se nível<=0**. O local inteiro **9** recebe uma única escrita, `istore 9 @58`, e exatamente três leituras, em **`@105`, `@122`, `@569`**. Níveis positivos forçados acima de I escolhem os mesmos ramos nesse método; não há multiplicação de range, dano ou número de alvos pelo nível de X-Ray.

## 3. Extremos, busca segmentada, orientação e consulta de alvos

O item calcula `elapsed=getUseDuration(stack,null)−remainingUseTicks` no local 5. O progresso local 7 é **`p=elapsed/15F` enquanto elapsed<15**, senão **`p=1F`**, sem clamp inferior próprio nesse trecho. O range local 8 é **`r=25F×p`**. O valor 25 é o parâmetro nominal de trace no progresso completo; não é prova de uma distância máxima universal de dano, pois há segmentos, caixas e reposicionamento pelo alvo.

| Local / região JVM | Definição ou consumidor |
|---|---|
| local 10, `@60–72` | Resultado inicial de `ProjectileUtil.getHitResultOnViewVector(usuario,predicate,(double)r)` |
| local 11, `@74–83` | Resultado de `usuario.pick((double)r,0F,false)` |
| local 12, `@85–103` | `usuario.getViewVector(0F).scale((double)r).add(usuario.getEyePosition())` |
| local 13, `@105–120` | Com X-Ray: local 12; sem X-Ray: **local 11.getLocation()** |
| local 14, `@122–137` | Mesma escolha inicial: local 12 versus **local 11.getLocation()** |
| local 13, `@217–233`, `@491–560` | Alimenta `setRayPosition` no cliente e a posição das partículas com deslocamentos próprios |
| local 14, `@764–766`, `@891–917` | Pode ser substituído pela posição de uma entidade; depois centra a caixa de candidatos do dano |

Os dois extremos iniciais usam a posição do trace **local 11**, não o resultado inicial local 10. A trilha visual do local 13 é estabelecida antes da busca segmentada; não se deve usar a imagem do feixe ou sua partícula como recibo da localização final do dano.

**Busca exclusiva do ramo X-Ray `@569–666`:**

1. `if local9==0 @571` segue para o ramo normal de bloco em `@669`. Com X-Ray, o local 22 é **`usuario.getBoundingBox().inflate((double)r)`**: a caixa original do usuário expandida por `r` em cada direção. Não é o cubo final de dano nem uma nova hitbox de projétil.
2. O contador **float** local 23 começa em **`1F @586–587`**; o local 24 começa em **`getEyePosition() @589–593`**. O teste `fcmpg @599` / `ifge @600→666` continua apenas enquanto **contador<r**.
3. Em cada iteração, o local 24 avança por **`getViewVector(1F)`** (`@603–613`); o local 25 é **local24 + `getViewVector(1F)`** (`@615–625`). Portanto, a primeira consulta usa o segmento de **olho+vetor** até **olho+2×vetor**, se a direção se mantiver; não começa no olho nem divide o passo por `r`.
4. `ProjectileUtil.getEntityHitResult @640` recebe **Level, usuário, local24, local25, local22 e predicate**. O bootstrap 0 fixa o predicate como **`Entity.canBeHitByProjectile`**, também usado no trace inicial e na consulta final. O corpo interno de `ProjectileUtil`, sua escolha de entidade mais próxima dentro do segmento e desempates não são recertificados pelo classfile do provider.
5. **Primeiro retorno não nulo:** `@645–654` grava o resultado no local 10 e sai por `goto @654→666`. Retorno nulo: `@657–661` soma **`1F`** ao contador e `goto @663→595` repete. A saída `@666→734` pula o ramo normal de bloco.

Se nenhuma consulta retornar entidade, **o local 10 conserva o resultado inicial de `@69`**. Com progresso completo (`r=25F`), o caminho sem retorno não nulo pode executar **24 consultas**, para contadores 1F…24F; isso não é 24 acertos nem 24 vítimas. Com `r<=1F`, o corpo do laço não executa. O término usa a comparação float com `r`; não há clamp de cada extremo segmentado ao ponto local 12. Um retorno por segmento também não prova a seleção da entidade **globalmente mais próxima** do usuário. O método guarda um resultado de trace, mas a consulta posterior pode enumerar vários candidatos.

**Ramo normal de bloco `@669–732`:** somente sem X-Ray, se o local 10 for `BlockHitResult`, lê `BlockPos`, `BlockState` e `getDirection` (local 20). Se o estado não for ar e **`isFaceSturdy(level,pos,direction)`** retornar true, coloca `HitResult.getLocation()` no local 21, usado pelo impacto visual. A direção é a face retornada pelo hit, sem inversão/oposto demonstrado. Esse bloco **não reescreve o local 14** nem é um gate separado da consulta final de dano. X-Ray pula essa preparação de orientação/superfície; não há nessa seleção uma alteração de blocos ou autorização de território.

**Resultado de entidade comum aos dois caminhos `@734–766`:** se o local 10 final for `EntityHitResult`, o local 21 recebe **`getEntity().position()`**, o local 20 recebe **`Direction.UP`** e o local 14 recebe o local 21. A posição escolhida é a origem da entidade, não necessariamente o ponto exato de interseção do raio. Sem resultado de entidade, X-Ray mantém o centro local 14 no extremo geométrico local 12; no caminho normal mantém a posição inicial do local 11.

Quando local 21 não é nulo e `elapsed%2==0`, `@768–871` solicita `RAYGUN_BLAST`, deslocado na direção local 20 por **`0.05F+nextFloat()×0.09F`**, e usa `direction.get3DDataValue()` como argumento da partícula. É feedback de impacto; não é explosão de dano, hit confirmado ou novo cast.

O salto **`ifnull @770→874`** contorna apenas esse feedback: **local21 não nulo não é pré-requisito da consulta final de dano**. Sem novo `EntityHitResult`, inclusive quando o fallback local10 é `BlockHitResult`, X-Ray pode chegar à consulta no extremo geométrico local14, sujeito a carga, lado, cadência e filtros. Isso descreve o CFG do provider, sem garantir vítima ou atravessamento físico de uma parede específica.

Os números de locals são slots JVM reutilizados: **local23 é float no laço (`@587`, `@661`), referência `BlockPos` no ramo normal (`astore @689`) e inteiro de amplifier depois (`istore @932`)**. Não se trata de um contador único persistente nem de uma relação entre distância, posição de bloco e dose de status.

| Consulta final no servidor | Contrato estático |
|---|---|
| Geometria `@891–920` | `AABB(local14+(-1,-1,-1), local14+(1,1,1))`: **cubo de lado 2**, não esfera, largura do feixe inteiro ou expansão própria concedida por X-Ray |
| Lista `@934–951` | `Level.getEntities(usuario,AABB,Entity.canBeHitByProjectile)`; percorre os candidatos retornados |
| Filtros `@975–1008` | Exclui identidade do usuário, aliança alvo→usuário, aliança usuário→alvo e mesmo veículo |
| Encerramento `@953–1160` | Percorre a lista, com gates próprios por alvo; não há quota literal de vítimas nem promessa de aceitação de todos os hits |
| LOS / nearest / paredes | O laço próprio não chama trace de blocos, e a iteração de candidatos não acrescenta teste separado de LOS. Internos do helper, distância global mínima, penetrabilidade física e regras PvP/claims continuam **NOT_VERIFIED** |

Essas relações fecham o **contrato estático do targeting selecionado pelo encantamento**. A capacidade física de atingir entidades atrás de materiais específicos, a ordem efetiva de resultados e o total de vítimas exigem QA. Não se deduz atravessamento irrestrito do nome X-Ray, do tamanho da AABB de busca ou da ausência de uma chamada adicional de bloco nessa região.

## 4. Cadência, dano, Irradiated e visuais herdados

**Gate de dano no servidor:** `isClientSide @875` / `ifne @878→1160` excluem o cliente; `@881–888` exige **`(elapsed−15)%3==0`**. Não existe nesse gate uma condição adicional `elapsed>=15`. A congruência admite oportunidades em **0/3/6/9/12**, além de 15 e seguintes, se houver callback e os demais gates forem alcançados. O aquecimento de 15 ticks do consumo cliente é outro ramo; não limita automaticamente esse gate servidor. Oportunidade de consulta não é hit aceito nem DPS.

| Seleção compartilhada | Contrato herdado; relação com X-Ray |
|---|---|
| Dano direto `@1026–1041` | `causeRaygunDamage(registryAccess,usuario)` e `ACCompat.hurt`: **2F com Gamma positivo; 1.5F sem Gamma**. A seleção usa local **18**, não local 9 |
| Amplifier `@922–932` | **4 com Gamma; 0 sem Gamma**. X-Ray não aumenta essa dose |
| Instância `@1091–1119` | Solicita `Irradiated` por **800 ticks**, com o amplifier acima; duração pedida não garante duração efetiva |
| Partículas e render | Gamma seleciona variantes azuis de partículas, textura e desenho do feixe. X-Ray muda o extremo inicial do local 13; não é dono da escolha azul |
| Pacote visual `@1125–1154` | `UpdateEffectVisualityEntityMessage(targetId,usuarioId,4/0,800)`, somente após `addEffect=true` |

O JSON publisher exclui Gamma para X-Ray, mas o código não força essa exclusão. Uma stack com coexistência imposta pode alcançar os ramos de Gamma; esses números continuam sendo do **outro objeto**, não um bônus causado por X-Ray. O censo visual herdado identifica `ACItemstackRenderer.renderByItem` e `RaygunRenderHelper.renderRaysFor`, com hashes de corpo e pivôs selecionados no [selo Gamma](../EXACT-GAMMA-RAY-CAUSAL-1.0.10.json). Esses owners não contêm token literal `X_RAY`; o seu reuso não adiciona outro consumer direto de X-Ray nem certifica pixels ou todo o CFG gráfico.

**Aceitação e exceção Tremorzilla:** para alvos normais, o retorno true de `ACCompat.hurt` torna o local 26 verdadeiro. `instanceof TremorzillaEntity @1013` / `ifne @1016→1047` pula `hurt` e seleciona esse verdadeiro diretamente. Logo, dano aceito não é pré-requisito universal da continuação para status. A continuação ainda exige alvo `LivingEntity` e tipo **fora** de `RESISTS_RADIATION @1082–1088`.

A tag publisher `data/alexscaves/tags/entity_type/resists_radiation.json` tem **270 bytes**, SHA-256 `1bb63c275f31f6744c071cda8ced3e1225401c5aa1dff2ea7fa3c7949e46a6c4`; inclui **Tremorzilla**, Nucleeper, Radgill, Brainiac, Gammaroach e Raycat. Portanto, o desvio de `hurt` não basta para conceder Irradiated à Tremorzilla com os dados empacotados. O runtime consulta a tag resolvida; overrides de datapack não são resultados de QA desta ficha.

Depois desses gates, `addEffect @1119` precisa retornar true para permitir o pacote visual. Dano solicitado, dano aceito, status aceito, envio de pacote e entrega visual são resultados distintos. O ID do usuário na mensagem não autentica um custo nem determina autoria de todo dano posterior.

**Autoria direta versus DoT:** a fonte Raygun recebe o usuário; o contrato separado de [Irradiated](../effects/irradiated.md) / [Radiation](../damage-types/radiation.md) preserva o dano periódico **sem atacante na factory `causeRadiationDamage(RegistryAccess)`**. `IrradiatedEffect.shouldTick(duration,a)` retorna false para **a<=0**; para a>0 usa `j=200/a` inteiro: quando `j>1`, exige a fase `duration%j==j/2`; quando `j<=1`, retorna true. No caso herdado de Gamma, **a=4 → j=50**, fase 25, sujeito a Hazmat, exclusão Raycat e RNG no tick. Amplifier 0 não executa esse tick próprio, embora a presença do status tenha outros consumidores. Não atribuir automaticamente o DoT, kill, lifesteal, XP ou **Mastery** ao caster direto, nem transferir esses parâmetros downstream ao encantamento X-Ray.

## 5. Custos, duração, estado e campos próprios N/A

| Campo | Contrato delimitado |
|---|---|
| Carga da arma | `ChargeUsed` é carga **usada**; `hasCharge` exige `getCharge(stack)<1000`. X-Ray não escreve charge por ramo próprio |
| Consumo sustentado | [Energy Efficiency](energy-efficiency.md) sela o ramo **cliente**: progresso>=1, `elapsed%(2+floor(1.5×L_EE))==0`, sem gasto para Player Creative; solicita `setCharge(min(used+1,1000))` |
| Cadências independentes | Aquecimento cliente de **15 ticks** e período de gasto sob EE não são o gate servidor **`(elapsed−15)%3==0`** |
| Recarga | Sistema nativo Raygun: `URANIUM_ROD`; ramo de recarga com `ItemStack.shrink(1)` e reset de charge. Não é mana ou combustível adicional de X-Ray |
| Duração de uso | `getUseDuration=72000` ticks é o limite declarado do item em uso. Não é duração de X-Ray, vida de projétil, cooldown ou duração do status |
| Esgotamento | `onUseTick @139–209` solicita `stopUsingItem` e retorna quando não há carga; no cliente também envia `UpdateItemTagMessage` |
| Estado do encantamento | Nível relido da stack a cada callback; local 9 é booleano transitório. Não há snapshot persistente próprio de cast X-Ray |
| Estado nativo compartilhado | `ChargeUsed`, `UseTime`, `PrevUseTime`, `RayX/Y/Z` e `PrevRayX/Y/Z` pertencem ao item. `setRayPosition` atualiza o extremo visual no cliente; serialização não prova aceitação remota ou conservação após reload |
| Rede | Provas históricas de pacote/receptor/codec preservadas; `network_authorization=NOT_VERIFIED`, sem nova homologação de remetente, saneamento, antirreplay ou persistência |

**Projétil próprio, velocidade, homing, dimensões corporais, quantidade de projéteis e vida de entidade: N/A para X-Ray.** O ramo usa vetores, AABB e resultados de trace; não instancia entidade de projétil própria. A caixa expandida da busca e o cubo final são consultas do item, não tamanho de uma entidade nova. **Duração, cooldown, mana/stamina, cura, familiar, contador persistente e mutação de blocos próprios: N/A**, pois o consumidor selecionado não os define para o encantamento. Duração de uso, animação, charge e Irradiated pertencem aos sistemas compartilhados identificados acima.

Os manifestos históricos de [controle](../EXACT-RAYGUN-CONTROL-1.0.10.json), [rede](../EXACT-RAYGUN-NETWORK-ABI-1.0.10.json), [pacote e munição](../EXACT-RAYGUN-PACKET-AMMO-1.0.10.json), [receptor](../EXACT-RAYGUN-RECEIVER-1.0.10.json) e [codec](../EXACT-RAYGUN-PACKET-CODEC-1.0.10.json) conservam seus bytes e limites. Enviar `UpdateItemTagMessage` não prova custo autenticado pelo servidor. Não interceptar/reemitir o pacote, duplicar débito ou transferir autoridade de `ChargeUsed` a um adapter de perks imaginário.

## 6. Sete eixos e fronteira de integração

| Eixo da rubrica | Contrato técnico estático | Fronteira de integração |
|---|---|---|
| **Identidade** | JAR/JSON/tag/registry SHA-exatos, nível I, custos e exclusão declarada de Gamma | Fonte 1.1.1 adjacente; aquisição e tags efetivas do mundo sem QA |
| **Comportamento** | Booleano local 9; três leituras; extremos locais 13/14; busca segmentada com primeiro retorno e fallback inicial | Não promover nome, imagem ou branch a penetrabilidade universal ou novo cast |
| **Parâmetros** | `r=25F×p`, aquecimento 15, contador float1/+1/<r, AABB do usuário inflada por r; campos próprios N/A delimitados | Valores não são setters/hooks homologados, quota de hits ou promessa de alcance real |
| **Targeting** | Resultado final de entidade centra local14; cubo ±1 e filtros de self/aliança/veículo; ramo de orientação de bloco separado | Internos do helper, nearest global, LOS físico, PvP e claims **NOT_VERIFIED** |
| **Custos** | Charge<1000, gasto cliente sob EE e recarga nativa; cadência servidor independente | Sem custo adicional X-Ray, segunda mana, duplicação de débito ou C2S homologado |
| **Integração** | Raygun tem fonte direta com usuário; Irradiated/Radiation têm contrato downstream separado; Gamma é outro objeto | Sem transferir DoT/kill/XP/Mastery, duplicar dano/status ou reabrir mutação de blocos; `NO_MUTATION` |
| **Validação** | Selo individual, extração SHA-exata, branches/pivôs e composição das provas Gamma/EE; universo publisher de 51 JSONs delimitado | `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`; provider integral aberto |

Para design de perks, os candidatos documentais são **distância calculada**, **escolha do extremo**, **predicado de busca**, **geometria dos segmentos**, **centro/volume da consulta final** e **gates de aquisição**. Cada um tem ownership e efeitos diferentes; não há seam mutador seguro certificado para qualquer deles. Alterar a consulta compartilhada pode afetar a Raygun sem X-Ray; alterar Gamma ou Irradiated afeta outros objetos/produtores. Essas relações exigem um contrato real, lado autoritativo, caps e deduplicação antes de qualquer integração executável.

Alex's Caves mantém targeting, charge, fonte, aceitação, status e feedback da Raygun. Black Arcana governa seu próprio runtime mágico; RPG Skill Tree fornece progressão/perks/Mastery por contratos reais no projeto dono. Um uso pode produzir vários callbacks e candidatos: tick, segmento, partícula, pacote ou tentativa de `hurt` não é recibo único de cast/hit/kill. **+0 raízes mágicas, +0 hooks homologados, `NO_MUTATION`.**

## 7. Reprodução, QA pendente e encerramento do recorte

O [auditor causal X-Ray](../../../../../docs/qa/alexscaves_1010_xray_causal_audit.py) lê o JAR SHA-exato com `javap` Java21, confere recursos/classes/métodos, o corpo integral e branches de `onUseTick`, o slot9, os operandos de extremos/busca/bloco/candidatos e o [manifesto individual](../EXACT-XRAY-CAUSAL-1.0.10.json). O [registro de reprodução](../EXACT-XRAY-CAUSAL-1.0.10.md) informa comandos e resultados; o [workflow](../../../../../.github/workflows/alexscaves-1010-xray-causal.yml) automatiza a reprodução. Composição de provas antigas preserva seus hashes e escopos; não é uma nova alegação de QA física ou de execução passada da CI.

Os recortes históricos de [X-Ray/targeting](../EXACT-RAYGUN-XRAY-TARGET-1.0.10.json), [branches condicionais](../EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json), [consumidores](../EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) e [guardas de radiação](../EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) continuam disponíveis, sem reescrever seu estado anterior de certificação. O novo selo é a autoridade causal individual atual, junto dos contratos Gamma/EE explicitamente reutilizados.

**QA física `NOT_TESTED`:** nível0/I e níveis forçados; coexistência forçada com Gamma; elapsed antes/depois15, range fracionário e interrupção; alvos no primeiro segmento, nas fronteiras e após obstáculos; fallback do trace inicial, primeiro retorno, posição/origem de entidades com tamanhos diversos e cubo ±1; múltiplos candidatos, aliados e veículos; superfícies, materiais, LOS e ordem efetiva; Survival/Creative, EE, carga esgotada, recarga, troca de slot/mão e tick delay; alvo normal/Tremorzilla, resistência publisher/override, `hurt=false`, `addEffect=false` e status prévio; cliente/servidor dedicado, multiplayer, pacotes, reconexão, morte, save/reload, unload e dimensão; PvP, claims, datapacks/outros mods e autoria/crédito único de XP/Mastery. Nenhum cenário recebe `PASS` por inspeção estática.

**Estados finais:** `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `network_authorization=NOT_VERIFIED`, `mutation=NO_MUTATION`, `provider_universe_closed=false`.

**Contabilidade delimitada:** **+1 contrato técnico estático individual certificado**, **+0 fichas novas**, **+0 raízes mágicas**, **+0 hooks mutadores homologados**, **+0 QA física**, **+0 providers encerrados**, **+0 promoção de Stage**. X-Ray encerra o recorte dos **51/51 encantamentos publisher 1.0.10**; esse fechamento não amplia o universo inventariado. O provider fica em **80/81 fichas certificadas**, com Raygun ainda parcial e o DamageType Tremorzilla Beam certificado individualmente. Não há próximo encantamento parcial nesse recorte; **os índices decidem a próxima família pendente dentro do provider**, sem avanço alfabético de provider enquanto ele permanecer aberto.
