# Deepsight — intensidade visual e poções

**Provider:** Alex's Caves Continued (`alexscaves`), **versão física 1.0.10**. **ID:** `alexscaves:deepsight`; campo `ACEffectRegistry.DEEPSIGHT`; implementação `server.potion.DeepsightEffect`. Categoria `BENEFICIAL`, cor `0x002972`. Modifica consumidores visuais de neblina e luz; não é spell independente nem amplia o número das [oito raízes mágicas](../actions/INDEX.md).

**Autoridade:** JAR publisher de 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, sem paridade comprovada com 1.0.10. Parâmetros abaixo `VERIFIED_EXACT_BINARY`; hook mutador `NOT_VERIFIED`; QA física `NOT_TESTED`. [Proveniência e reprodução](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

## Identidade e lifecycle

`ACEffectRegistry.<clinit>()V @105–118` registra `deepsight`; `lambda$static$5()Lnet/minecraft/world/effect/MobEffect; @0–7` constrói a classe. `DeepsightEffect.<init>()V @0–20` fixa categoria/cor e inicializa os campos de instância `lastDuration=-1` e `firstDuration=-1`. Não adiciona modificador de atributo no construtor e não sobrescreve `ACMobEffect.tick`, cujo corpo é vazio.

`shouldTick(II)Z @0–41` escreve `lastDuration=duration`; com `duration<=0`, zera o acompanhamento para `-1`; se `firstDuration==-1`, escreve a duração recebida; retorna `duration>0`. O argumento amplifier não é usado. `getActiveTime()I @0–9` calcula **`firstDuration-lastDuration`**. O bridge `ACMobEffect.shouldApplyEffectTickThisTick(II)Z` chama `shouldTick`, enquanto `applyEffectTick(Lnet/minecraft/world/entity/LivingEntity;I)Z` executa o tick vazio herdado e retorna `true`.

`onEffectStart(Lnet/minecraft/world/entity/LivingEntity;I)V @0–10` e `onEffectEnd(Lnet/minecraft/world/entity/LivingEntity;)V @0–10` recolocam **ambos** os campos em `-1`. O `LivingEntityMixin` conecta esses métodos aos callbacks de adição (`ac_onEffectAdded @0–34`), atualização apenas quando o booleano recebido é verdadeiro (`ac_onEffectUpdated @0–47`, chama end e start), e remoção (`ac_onEffectRemoved @0–28`). Descritores completos:

- `ac_onEffectAdded(Lnet/minecraft/world/effect/MobEffectInstance;Lnet/minecraft/world/entity/Entity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V`.
- `ac_onEffectUpdated(Lnet/minecraft/world/effect/MobEffectInstance;ZLnet/minecraft/world/entity/Entity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V`.
- `ac_onEffectRemoved(Lnet/minecraft/world/effect/MobEffectInstance;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V`.

**Limite de estado:** os dois campos pertencem ao objeto do efeito registrado, e não a um mapa por entidade nem à `MobEffectInstance`. Os métodos recebem entidade, mas os resets não a usam. Essa estrutura não permite prometer isolamento de fade entre jogadores/entidades. Interferência observável, sincronização entre lados e comportamento com reaplicação precisam de teste; não há defeito multiplayer reproduzido nesta auditoria.

## Intensidade e parâmetros

O consumidor comum é `getIntensity(Lnet/minecraft/world/entity/player/Player;F)F`:

| Caso / parâmetro | Contrato do binário |
|---|---|
| Jogador sem instância | Retorna `0F` (`@0–24`) |
| Instância de duração infinita | Retorna `1F` imediatamente (`@25–33`) |
| Duração finita | `min(20F,min(getActiveTime()+partialTicks,duration+partialTicks))*0.05F` (`@34–75`) |
| Fade nominal | Limite superior chega a `1F` com 20 ticks acompanhados; também cai perto do fim da duração |
| Amplifier | Não é consultado nessa fórmula nem em `shouldTick`; nível maior não dá visão adicional por si só |
| Limite inferior | Não há `max(0,...)` explícito na fórmula; não substituir o acompanhamento real por um clamp presumido |

Esses 20 ticks são de acompanhamento do efeito, não cooldown ou tempo de cast. Duração nominal depende da instância; não há timer próprio de persistência ou NBT na classe. A categoria benéfica não prova que todos os clientes/shaders irão renderizar o mesmo resultado.

## Consumidores reais: luz e neblina

`ACLightmapAdditions.ambientBonus()F @105–164` consulta o **jogador local**, exige Deepsight e `isUnderWater()`, e calcula `min(1F,ambientAnterior+0.05F*getIntensity(player,frameTime))`. O método ainda aplica ajuste de boss ao resultado depois (`@165–181`); isso não estabelece luz de bloco, iluminação emitida no mundo ou detecção de inimigos. O cálculo depende do caminho de lightmap do cliente.

`ClientEvents.acFogRender(Lnet/neoforged/neoforge/client/event/ViewportEvent$RenderFog;)Z` devolve `false` se o evento já está cancelado (`@0–8`). Usa posição/fluido/bloco da câmera para escolher o meio, mas consulta Deepsight do **jogador local**, não necessariamente da entidade câmera. Os ramos exatos são:

| Meio / gate | Cálculo com intensidade `I` |
|---|---|
| Fluido no tag `ACID` (`@60–149`) | Far `10F*(1F+1.5F*I)`; near `0F` |
| Fluido no tag `PURPLE_SODA` (`@150–259`) | Far `20F*(1F+1.5F*I)`; near `-8F*(1F-I)` |
| Bloco `PRIMAL_MAGMA` ou `FISSURE_PRIMAL_MAGMA` (`@260–364`) | Far `2F*(1F+1.5F*I)`; near `0F` |
| `FogType.WATER` e `CLIENT_CONFIG.biomeWaterFogOverrides` verdadeiro (`@365–471`) | Multiplica `lastSampledWaterFogFarness` por `1F+1.5F*I`; se o fator resultante difere de `1F`, far recebe `shaderFogEnd*fator` |

No máximo nominal `I=1F`, o multiplicador é `2.5F` nesses ramos, não “alcance global +150%”. Valores de acid/soda/magma são distâncias do plano de fog, sem efeito demonstrado sobre targeting, linha de visão do servidor, alcance de ataque ou projétil. A configuração em execução, overrides de shader e a aplicação final do evento não foram testados. Alterar amplifier sozinho não altera `I`.

## Poções, obtenção, targeting e custos

`ACEffectRegistry.lambda$static$10()Lnet/minecraft/world/item/alchemy/Potion; @0–40` constrói a poção `deepsight` com uma instância de **3600 ticks**; `lambda$static$11()` de mesmo descritor constrói `long_deepsight` com **9600 ticks**. Ambos usam `MobEffectInstance(Holder,int)`, sem amplifier adicional. São durações nominais de 180 e 480 segundos a 20 TPS, não novas magias ou garantia de permanência. O registro das duas poções está em `<clinit> @186–215`.

`registerBrewing(Ljava/util/function/Consumer;)V @87–131` cria `ProperBrewingRecipe`: poção vanilla **Awkward + `ACItemRegistry.LANTERNFISH` → Deepsight**. Em `@136–169`: **Deepsight + redstone → Long Deepsight**. O helper `ProperBrewingRecipe.isInput(Lnet/minecraft/world/item/ItemStack;)Z @0–20` exige stack não nulo e `ACCompat.sameItemSameData(template,input)`, evitando interpretar “qualquer frasco” como entrada. O custo/combustível e execução do brewing ficam no sistema de brewing; não existe custo de mana, durabilidade ou cooldown próprio no efeito.

O efeito não escolhe destinatário, área ou projétil. Aplicação por bebida, splash, lingering, flecha, comando ou outro mod deve seguir as regras do respectivo aplicador; o catálogo de poções não homologa automaticamente esses caminhos. A obtenção via brewing acima é a relação diretamente auditada. O JSON `data/alexscaves/advancement/alexscaves/deepsight.json` usa `minecraft:effects_changed` com `alexscaves:deepsight` e parent `alexscaves:alexscaves/abyssal_bucket`; seu trigger observa o efeito, sem exigir diretamente ingrediente ou brewing. Portanto, o texto traduzido da conquista não é uma segunda prova de receita.

## Integração e validação

Duração da instância e a função `getIntensity` são superfícies diferentes. Uma perk de duração deve preservar o lifecycle e provar que os campos compartilhados não contaminam o acompanhamento desejado. Uma perk de visão deve escolher explicitamente o consumidor de fog/lightmap e manter a separação entre efeito visual cliente e alcance/targeting servidor. Não foi validado hook mutador Black Arcana/Enshrouded/RPG Skill Tree, nem contrato de alteração de campos privados ou overrides de shader.

Os bytes fixos e localizadores dos sete campos estáticos estão documentados na [prova técnica dos efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.md). QA pendente: duração finita/infinita, entrada/saída/reaplicação, duas entidades com tempos diferentes, multiplayer, respawn/reload, câmera remota, primeira/terceira pessoa, fluidos/magma e shaders com configurações reais. O auditor de evidências não executa essas situações. **`STATIC_TECHNICAL_CATALOG_ONLY`; hooks `NOT_VERIFIED`; QA física `NOT_TESTED`.**
