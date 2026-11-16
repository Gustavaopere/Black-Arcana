# Gamma Ray — dano, radiação e feedback da Raygun (1.0.10)

**Contrato técnico estático individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Integração executável:** `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`. O recorte fecha os sete eixos documentais do encantamento no publisher SHA-exato **1.0.10**; não homologa uma perk, a Raygun inteira ou o universo do provider.

`alexscaves:gamma_ray` é um encantamento nativo da Raygun. Seu nível **positivo** seleciona dano direto solicitado de **2F** em vez de **1.5F**, instância de **Irradiated por 800 ticks com amplifier 4** em vez de 0 e variantes visuais azuis. A aplicação exige os gates nativos descritos abaixo. Nenhum desses valores representa HP perdido, DPS, acerto garantido ou uma nova magia do Black Arcana.

## 1. Identidade e autoridade das fontes

| Objeto | Evidência publisher 1.0.10 |
|---|---|
| Provider / mod ID | Alex's Caves Continued / `alexscaves` |
| Plataforma | Minecraft 1.21.1 / NeoForge / Java 21 |
| Mod instalado | `alexscaves-1.0.10-neoforge+1.21.1.jar`, entrada 019 da [modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md) |
| Artefato publisher | [CurseForge, arquivo 8856293](https://www.curseforge.com/minecraft/mc-mods/alexs-caves-continued/files/8856293), **75.279.314 bytes** |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Identidade / símbolo | `alexscaves:gamma_ray` / `ACEnchantmentRegistry.GAMMA_RAY` |
| Recurso individual | `data/alexscaves/enchantment/gamma_ray.json`, **356 bytes**, SHA-256 `4873ef951ef2afff56e8734740e68c0e4bec4b2d69e893632a9f97dc317630fd` |
| Consumer | `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`, SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| Método principal | `onUseTick(Level,LivingEntity,ItemStack,int)V`; descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V` |
| Corpo compilado | **523 instruções**, **57 branches diretos**; SHA-256 canônico do parse `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5` |

**Prova individual atual:** [manifesto causal](../EXACT-GAMMA-RAY-CAUSAL-1.0.10.json), [reprodução e limites](../EXACT-GAMMA-RAY-CAUSAL-1.0.10.md), [auditor SHA-exato](../../../../../docs/qa/alexscaves_1010_gamma_ray_causal_audit.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-gamma-ray-causal.yml). O hash integral identifica o corpo extraído; os branches e operandos sustentam as relações causais, sem executar combate.

Os manifestos históricos de [controle](../EXACT-RAYGUN-CONTROL-1.0.10.json), [branches](../EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json), [consumidores](../EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) e [guardas de radiação](../EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) conservam seus bytes e escopos anteriores. A certificação de [Energy Efficiency](../EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json) já sela o mesmo `onUseTick` integral e os helpers de charge; é reutilizada para esse custo, sem promover a [ficha Raygun](../damage-types/raygun.md) ou sua autorização de rede.

A [wiki comunitária](https://alexscaves.wiki.gg/wiki/Raygun#Enchantments) oferece referência funcional. A fonte adjacente [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1**: serve para localizar candidatos, sem autoridade numérica ou presunção de paridade com **1.0.10**.

## 2. JSON, aquisição e compatibilidade

| Campo | Valor publisher | Interpretação delimitada |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.gamma_ray` | Identidade da localização |
| `supported_items` | `#alexscaves:enchantable/raygun` | Tag física contém somente `alexscaves:raygun` |
| `weight` | `2` | Peso declarativo de aquisição; não chance de hit ou radiação |
| `max_level` | `1` | Nível I declarado |
| `min_cost` | base `1`, incremento `18` | `1+18×(L−1)`; no nível I: **1** |
| `max_cost` | base `41`, incremento `10` | `41+10×(L−1)`; no nível I: **41** |
| `anvil_cost` | `4` | Custo do sistema de encantamento, não custo por disparo |
| `slots` | `["mainhand"]` | Slot declarado no recurso |
| `effects` / `exclusive_set` | Ausentes no JSON de Gamma Ray | Mecânica observada no código; ausência local não prova compatibilidade global |

A tag `data/alexscaves/tags/item/enchantable/raygun.json` tem **46 bytes**, SHA-256 `8e7cb71ff2c706004fba0493f2237e96da3af53dea6e3ae414542b5150cc012d`.

**Exclusão reversa comprovada:** `data/alexscaves/enchantment/x_ray.json` declara `exclusive_set=["alexscaves:gamma_ray"]`; **406 bytes**, SHA-256 `612b1f7b126cea12085dea00736115b05fd4789bf9fc9ff6c4344a427135b0f8`. Não atribuir esse campo ao JSON de Gamma Ray. Os dados publisher documentam a intenção de exclusividade; aplicação por mesa/bigorna, editores, comandos e datapacks resolvidos continua sem QA física. O consumer consulta ambos separadamente, sem um gate próprio que rejeite sua coexistência forçada.

## 3. Leitura do nível, targeting e geometria

`ACCompat.enchantLevel` lê as entradas de encantamento da stack e retorna o inteiro correspondente, ou 0 se ausente. Em `onUseTick @331–346`, `GAMMA_RAY @332` e `enchantLevel @335` alimentam `ifle @338`: **nível >0 vira 1; nível <=0 vira 0**. Há uma única escrita no local inteiro **18**, em `@346`, e cinco leituras: `@367`, `@402`, `@922`, `@1029`, `@1138`. Portanto, níveis positivos forçados acima de I selecionam o mesmo ramo nesse corpo; não são uma escala linear de potência.

O método calcula `elapsed=getUseDuration(stack,null)−remainingUseTicks` no local 5. O progresso local 7 vale `elapsed/15F` enquanto `elapsed<15`, senão `1F`, sem clamp inferior próprio nesse trecho. A distância local 8 é **`25F×progresso`**, usada pelos traces `ProjectileUtil.getHitResultOnViewVector @69` e `LivingEntity.pick @80`. **Gamma Ray não modifica essa fórmula.** Distância de trace não comprova alcance final, LOS aceito ou distância real de dano.

`X_RAY`, lido separadamente, escolhe os pontos iniciais locais 13/14 e sua busca adicional `@569–666`; seus efeitos não pertencem a Gamma. Sem esse ramo, o local 14 começa na posição do trace de blocos. Quando o resultado final é `EntityHitResult`, `@734–766` coloca a **posição da entidade** no local 14. Assim, o centro da consulta de dano depende do targeting nativo, não do deslocamento das partículas.

| Etapa nativa | Contrato estático |
|---|---|
| Predicate dos traces e consulta | Bootstrap 0 referencia `Entity.canBeHitByProjectile`; não é um filtro de perk |
| Volume consultado `@891–920` | `AABB(local14+(-1,-1,-1), local14+(1,1,1))`: **cubo de lado 2**, não esfera de raio 2 nem volume de todo o feixe |
| Candidatos `@934–951` | `Level.getEntities(usuario,AABB,predicate)` e iteração da lista; múltiplos candidatos são possíveis, sem quantidade garantida |
| Exclusões `@975–1008` | Identidade do usuário, aliança alvo→usuário, aliança usuário→alvo e mesmo veículo |
| Relação com Gamma | Nenhuma leitura do local 18 altera distância, AABB, predicate ou filtros |

**Projétil/hitbox próprios: N/A.** Gamma não instancia entidade de projétil, nem define velocidade, homing, tamanho corporal ou vida de um projétil. O cubo acima é uma consulta de alvos do item; não é dimensão de uma nova entidade ou aumento de área concedido pelo encantamento. O método não adiciona um teste separado de LOS para cada candidato desse cubo; isso não autoriza inferir penetração, acesso a claims ou proteção PvP.

## 4. Cadência, dano, status e visuais

**Gate de dano no servidor:** `isClientSide @875` / `ifne @878` excluem o ramo cliente; `@881–888` exige **`(elapsed−15)%3==0`**. Esse trecho **não exige `elapsed>=15`**. A expressão admite restos zero também em 0/3/6/9/12 ticks, se houver callback e os demais gates forem alcançados. São oportunidades matemáticas, sem garantia de alvo, hit aceito ou dano durante o aquecimento. A guarda de aquecimento do consumo cliente é separada; não transferir seus 15 ticks para o gate servidor nem converter a periodicidade em DPS.

| Seleção pelo local 18 | Com Gamma (`>0`) | Sem Gamma (`<=0`) | Limite causal |
|---|---:|---:|---|
| Dano direto solicitado `@1029–1041` | **2F** | **1.5F** | Argumento de `ACCompat.hurt`, sujeito à aceitação e mitigação |
| Amplifier do status `@922–932` | **4** | **0** | *Irradiated V* / *Irradiated I*; não dano ou número de vítimas |
| Duração pedida `@1111–1116` | **800 ticks** | **800 ticks** | Instância construída; 40 s nominais a 20 TPS, sem duração efetiva garantida |
| Partículas `@367–432` | `BLUE_RAYGUN_EXPLOSION` / `BLUE_HAZMAT_BREATHE` | Variantes sem prefixo `BLUE_` | Escolha visual, com branches de RNG/progresso próprios |
| Payload visual `@1138–1154` | `4`, `800` | `0`, `800` | Após `addEffect=true`; não uma segunda aplicação do status |

**Outros consumidores visuais no cliente.** O censo compilado de `GAMMA_RAY` contém quatro owners: registry, `RaygunItem`, `ACItemstackRenderer` e `RaygunRenderHelper`. Os dois últimos recebem uma prova visual separada em `visual_consumers`, sem serem contados como outros métodos de dano ou novos casts.

| Consumer visual | Trecho específico verificado | Limite |
|---|---|---|
| `ACItemstackRenderer.renderByItem` | Nível positivo em `@1968–1982` seleciona `RAYGUN_BLUE_TEXTURE @1989` em vez de `RAYGUN_TEXTURE @1995` | Hash do corpo de 1.771 instruções e pivôs selecionados; não é certificação integral de todos os itens renderizados |
| `RaygunRenderHelper.renderRaysFor` | Leituras Gamma em `@64` e `@294`, nos caminhos de desenho das mãos, formam o booleano local 11 encaminhado ao desenho do raio | Corpo identificado de 209 instruções, com pivôs visuais selecionados; não reconstrói targeting ou aceitação de dano |

Essas referências completam a disposição dos owners literais de Gamma no JAR. Seleção de textura e argumento de desenho não comprovam renderização efetiva em toda GPU, transmissão de pacote, hit, status ou crédito. Também não homologam uma API para perks de cor. Os campos de partículas, o payload de status e a aparência do item/feixe continuam distintos.

**Fonte direta e aceitação:** `causeRaygunDamage(registryAccess,usuario) @1026` cria a fonte nativa `RAYGUN` com a entidade usuária; `ACCompat.hurt @1041` repassa ao `Entity.hurt` e retorna seu booleano. Para entidades normais, o local 26 só fica verdadeiro se essa chamada retornar true. Isso não mede HP perdido, dano líquido, kill ou crédito de Mastery.

**Exceção Tremorzilla:** `instanceof TremorzillaEntity @1013` / `ifne @1016` pula a chamada de `hurt` e alcança `iconst_1 @1047`, tornando o local 26 verdadeiro. Portanto, “todo status exige dano aceito” seria incorreto. Mesmo nesse ramo, a rota seguinte ainda exige `LivingEntity` e ausência na tag de resistência.

**Gates do status e do feedback:** local 26 verdadeiro → alvo `LivingEntity @1061` → tipo **fora** de `RESISTS_RADIATION @1082–1088` → construção de `MobEffectInstance(IRRADIATED,800,amplifier)` → `addEffect @1119`. Somente retorno true em `@1122` permite `UpdateEffectVisualityEntityMessage(targetId,usuarioId,4/0,800)` / `sendMSGToAll @1154`. O ID do usuário no pacote visual não prova autoria do dano periódico.

A tag publisher `data/alexscaves/tags/entity_type/resists_radiation.json` tem **270 bytes**, SHA-256 `1bb63c275f31f6744c071cda8ced3e1225401c5aa1dff2ea7fa3c7949e46a6c4`; inclui **Tremorzilla**, Nucleeper, Radgill, Brainiac, Gammaroach e Raycat. Logo, o desvio de `hurt` da Tremorzilla **não basta para conceder Irradiated** com os dados empacotados. O runtime consulta a tag resolvida; datapacks podem alterar essa composição, sem homologação nesta ficha.

## 5. Irradiated downstream, custo e lifecycle

A semântica de [Irradiated](../effects/irradiated.md) e do [DamageType Radiation](../damage-types/radiation.md) já possui certificados separados: [efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.md) e [Radiation](../EXACT-RADIATION-CONTRACT-1.0.10.json). Reutilizar esses contratos não reabre nem promove todos os produtores do status.

`IrradiatedEffect.shouldTick(duration,a)` retorna false para **a<=0**. Para a>0 usa `j=200/a` inteiro; com Gamma, **a=4 → j=50**, elegível quando `duration%50==25`. O ramo sem Gamma, amplifier 0, não executa esse tick periódico. Isso não elimina os outros consumidores da presença do status, como o cancelamento condicionado de `LivingHealEvent`, documentados na ficha do efeito.

O tick periódico conta peças Hazmat, calcula `s=1F−0.25F×h`, exclui Raycat e usa RNG com limiar `s+0.1F` antes de solicitar `hurt(radiationSource,s)`. Assim, **amplifier 4 não é dano 4 por tick** e o período nominal 50 não é dano aceito a cada 50 ticks. `causeRadiationDamage(RegistryAccess)` não recebe entidade atacante: a autoria direta da Raygun **não é transferida automaticamente** ao dano posterior, kill, lifesteal, XP ou Mastery. Não reconstruí-la a partir da cor ou do pacote visual.

| Custo / estado | Contrato delimitado |
|---|---|
| Carga da arma | `ChargeUsed` significa carga **usada**; `hasCharge` exige `getCharge(stack)<1000`. Gamma não altera o limite nem escreve charge por ramo próprio |
| Consumo sustentado | [Energy Efficiency](energy-efficiency.md) sela a sequência cliente: após progresso>=1, `elapsed % (2+floor(1.5×L_EE))==0`, com isenção Creative, solicita `setCharge(min(used+1,1000))` |
| Aquecimento | 15 ticks governa progresso e o gate cliente de charge; não é guarda adicional do dano servidor |
| Recarga e uso | Contrato contextual da [Raygun](../damage-types/raygun.md) e provas históricas: munição nativa `URANIUM_ROD`, indicador de charge e duração declarada de uso de 72000 ticks. Não é mana de Gamma, cooldown próprio ou recarga automática garantida |
| Fim por esgotamento | `onUseTick @139–209` solicita `stopUsingItem` e retorna quando não há carga; o cliente também envia `UpdateItemTagMessage` |
| Estado/persistência | Gamma é relido da stack por callback; local 18 não é snapshot persistente de cast. Charge, `UseTime`/`PrevUseTime` e posições do raio pertencem ao estado nativo do item |

Os detalhes de `use`, `releaseUsing`, helpers de animação e serialização continuam sob os escopos históricos da Raygun/Energy Efficiency; esta revisão não certifica seus lifecycles integrais. O consumidor não define contador, mana, stamina, cooldown, familiar, cura ou mutação de blocos **próprios de Gamma Ray**. A duração de Irradiated é estado do alvo, separada da vida do uso da arma. Dados locais/serializados não comprovam conservação física após morte, unload/reload, troca de mãos, dimensão ou reconexão.

As provas anteriores de [rede](../EXACT-RAYGUN-NETWORK-ABI-1.0.10.json), [pacote](../EXACT-RAYGUN-PACKET-AMMO-1.0.10.json), [receptor](../EXACT-RAYGUN-RECEIVER-1.0.10.json) e [codec](../EXACT-RAYGUN-PACKET-CODEC-1.0.10.json) mantêm seus escopos. Não houve nova homologação de codec, vínculo do remetente, saneamento de `ChargeUsed`, aceitação de C2S, antirreplay ou autoridade de persistência. `network_authorization=NOT_VERIFIED` permanece independente da certificação estática de Gamma.

## 6. Sete eixos do contrato e limites para perks

| Eixo da rubrica | Contrato técnico estático | Fronteira de integração |
|---|---|---|
| **Identidade** | ID, JSON/tag, nível I, custos de encantamento e JAR SHA-exatos; exclusão declarada pelo JSON de X-Ray | Não aplicar fonte 1.1.1 ou tags finais presumidas à instalação 1.0.10 |
| **Comportamento** | Booleano nível>0 escolhe dano pedido, amplifier e visuais; gates servidor/hurt/status distintos e exceção Tremorzilla | Preservar fluxo nativo; nenhum segundo `hurt`, `addEffect` ou cast compensatório |
| **Parâmetros** | 2F/1.5F, 800 ticks, amplifier4/0; período servidor `(elapsed−15)%3==0`; charge e EE separados | Valores observáveis não são setters ou hooks homologados; sem alterar nível/dose/cadência por adapter imaginário |
| **Targeting** | Traces nativos, local14, cubo lado2, predicate e filtros de identidade/aliança/veículo; Gamma não amplia range | Não inventar projétil, AoE do feixe inteiro, bypass de LOS, claims ou PvP |
| **Custos** | ChargeUsed<1000, gasto cliente sob EE, recarga nativa; duração de uso e status independentes | Não duplicar débito, refund, munição, cooldown ou uma segunda mana; autoridade C2S pendente |
| **Integração** | Dano direto com usuário; DoT Radiation sem caster na factory; aceitação de efeito e visual separadas | Crédito de XP/Mastery exige resultado autorizado, autoria e deduplicação reais; `mutating_hook=NOT_VERIFIED` / `NO_MUTATION` |
| **Validação** | Selo causal, reprodução SHA-exata e testes de fidelidade estática; contratos EE/Irradiated/Radiation reutilizados | `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`; nenhum resultado de gameplay, datapack ou rede promovido |

Para design de perks, os candidatos úteis são **dano solicitado**, **duração/amplifier da instância**, **resistência ao status**, **frequência downstream**, **variante visual** e **gates de aquisição**. Cada um pertence a um ponto causal diferente. Mudar Hazmat ou `shouldTick` afeta o efeito downstream e seus outros produtores; mudar Gamma não deve alterar Energy Efficiency ou X-Ray. As assinaturas identificadas são superfícies de pesquisa, sem API de mutação segura certificada.

Alex's Caves mantém targeting, custos, fonte, aceitação, status e feedback da Raygun. Black Arcana governa seu próprio runtime mágico; RPG Skill Tree fornece progressão/perks/Mastery por contrato real no projeto dono. Um mesmo uso pode alcançar vários candidatos e callbacks: contagem de tick, pacote, partícula ou chamada de dano não é crédito de cast/hit/kill. Exigir causalidade e deduplicação antes de qualquer integração executável.

## 7. Reprodução e validação ainda pendente

O [auditor causal](../../../../../docs/qa/alexscaves_1010_gamma_ray_causal_audit.py) lê o JAR exato com `javap` Java21, confere recursos/classes/métodos, o corpo integral e branches de `onUseTick`, os pivôs causais e o [selo Gamma Ray](../EXACT-GAMMA-RAY-CAUSAL-1.0.10.json). A [prova individual](../EXACT-GAMMA-RAY-CAUSAL-1.0.10.md) registra o comando reproduzível e os limites. Os testes de documentação e evidência não simulam o modpack.

**QA física pendente:** nível0/I e níveis forçados; primeiras chamadas durante aquecimento e após15, interrupção e tick delay; comparação 1.5F/2F solicitados contra dano aceito; caixa lado2, blocos, LOS, múltiplos candidatos, aliados e veículos; Tremorzilla com tag publisher e override; status prévio mais forte, recusa de `addEffect`, resistência, amplifier0/4, Hazmat/RNG e cura; Survival/Creative, recarga, carga esgotada, troca de slot/mão e cancelamento; servidor dedicado/multiplayer, pacotes, reconexão, save/reload, unload e dimensão; PvP, claims, datapacks e outros mods; autoria do DoT e crédito único de XP/Mastery. Nenhum cenário recebe `PASS` por esta auditoria estática.

**Estados finais:** `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `network_authorization=NOT_VERIFIED`, `mutation=NO_MUTATION`, `provider_universe_closed=false`.

**Contabilidade delimitada:** **+1 contrato técnico estático individual certificado**, **+0 fichas novas**, **+0 raízes mágicas**, **+0 hooks mutadores homologados**, **+0 QA física**, **+0 providers encerrados**, **+0 promoção de Stage**. Contagens vigentes pertencem aos índices gerados; próxima ficha parcial alfabética: **`alexscaves:x_ray`**.
