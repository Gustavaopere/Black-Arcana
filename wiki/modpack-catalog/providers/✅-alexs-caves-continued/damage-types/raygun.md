# Raygun — tipo de dano `alexscaves:raygun` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED + SHA_EXACT_SELECTED_BYTECODE_OBSERVED` (escopo parcial). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:raygun`.
- **Caminho ZIP:** `data/alexscaves/damage_type/raygun.json`.
- **SHA-256 do JSON:** `dc1095e92e0695b302100993af8fafd72c8d6b948d90717e667a6ced2ae1bc35`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `raygun` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.3` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- `minecraft:bypasses_cooldown`
- `minecraft:is_explosion`
- `minecraft:is_projectile`

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.
O tag `minecraft:bypasses_cooldown` corresponde à classificação de tipo de dano do Minecraft, **não** demonstra redução/bypass do cooldown de lançamento de magias.


## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | ⚠️ argumento caster observado em `causeRaygunDamage`; atribuição final/kill/PvP ainda não verificados |
| Fórmula de dano, mitigação, críticos e resistências | ⚠️ `ACCompat.hurt` recebe 1,5f ou 2,0f conforme flag local; causa e aceitação líquida ainda abertas |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | ⚠️ ray trace, AABB, exclusões de aliados/mesmo veículo observados; alcance/volume efetivos pendentes |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | ⚠️ seletores por ray trace e entidades; nenhum spawn direto observado em `onUseTick`, mas indiretos não descartados |
| Duração, intervalo de hits, custo de ação e cooldown de casting | ⚠️ `getUseDuration=72000`, `ChargeUsed` e 800 ticks de status observados; fórmula de custo/intervalos/cooldown pendentes |
| Persistência, ordenação de eventos, server authority e deduplicação | ⚠️ tags `ChargeUsed`/`UseTime` e `UpdateItemTagMessage` observadas; handler, reload e antirreplay não testados |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeRaygunDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `RAYGUN` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class` | `public void onUseTick(net.minecraft.world.level.Level, net.minecraft.world.entity.LivingEntity, net.minecraft.world.item.ItemStack, int)` | `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V` | 1026 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Auditoria de controle nativo — `RaygunItem` compilado 1.0.10

**Recorte novo:** `SHA_EXACT_1010_RAYGUN_SELECTED_METHOD_REFERENCES_AND_NUMERIC_OPERANDS_ONLY`. [Manifesto imutável de parâmetros e métodos](../EXACT-RAYGUN-CONTROL-1.0.10.json) · [probe e testes da PR #985](https://github.com/Gustavaopere/Black-Arcana/pull/985) · [workflow de evidência](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41256261358).

A inspeção automatizada baixou e validou a versão publisher **1.0.10** do JAR pelos SHA-1/SHA-256 e tamanho físico registrados acima, verificou a classe compilada `server/item/RaygunItem.class` (SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`), inspecionou **26 métodos declarados** e exportou **18 métodos selecionados**. O manifesto fixa digest de oito métodos e 14 âncoras numéricas/simbólicas; o resultado da CI não é teste de gameplay nem reconstrução completa do CFG.

### Alvo, range e geometria — não confundir conceitos

| Método e offset compilado | Evidência estática exata | Limite para perks |
|---|---|---|
| `onUseTick @11` | Calcula tempo utilizado a partir de `getUseDuration - remainingUseTicks` e inicializa um valor inteiro **15** no início de uma sequência de comparação/proporção. | `15` é um operando do cálculo de uso; não anunciar como alcance ou cooldown sem rastrear o resultado. |
| `onUseTick @35` | Literal **25.0f** em uma região inicial; mais adiante `getHitResultOnViewVector @69` e `LivingEntity.pick @80` recebem distâncias calculadas. | Há caminhos de ray trace distintos. O literal não basta para certificar o alcance efetivo de cada modo ou um parâmetro público modificável. |
| `onUseTick @44–50` | Consulta `ACEnchantmentRegistry.X_RAY` via `ACCompat.enchantLevel`. | Enchantment nativo participa da escolha dos caminhos; efeito sobre oclusão/alcance efetivo ainda não está completamente certificado. |
| `onUseTick @575–640` | Obtém a bounding box do usuário, executa `AABB.inflate` e usa `ProjectileUtil.getEntityHitResult` com vetores e predicado. | AABB de busca, distância do raio e vítima realmente elegível são medidas distintas; não converter caixa em raio circular ou área de dano. |
| `onUseTick @875–943` | Consulta `Level.isClientSide` e, no caminho de servidor observado, usa `Level.getEntities(source, AABB, Predicate)` para enumerar alvos. | Há um segundo domínio de seleção por entidades. Sem CFG/medidas completas, não declarar cone, número máximo de hits, LOS universal ou tamanho de hitbox. |
| `onUseTick @978–1008` | Verificações `Entity.is`, `Entity.isAlliedTo`, `LivingEntity.isAlliedTo` e `isPassengerOfSameVehicle`, com saídas de ramo antes de solicitar dano. | Não permitir que uma perk elimine exclusões de autocausação, aliados ou passageiros. Proteção/PvP externa permanece sem teste. |

O recorte de `onUseTick` exportado não mostra chamada simbólica direta a `Level.addFreshEntity`; os caminhos observados recorrem a ray traces, seleção de entidades e partículas. Isso **não** prova ausência de entidades em todos os caminhos indiretos, variantes ou interações com outros mods.

### Charge, uso e encantamentos

| Superfície exata | Dado identificado | Condição de integração |
|---|---|---|
| `getUseDuration(ItemStack,LivingEntity)` | Retorna literal inteiro **72000 ticks**. | Tempo máximo declarado para uso mantido, **não cooldown** nem duração obrigatória de cada disparo. |
| `getCharge / setCharge` | Armazenam/lêem tag de `ItemStack` **`ChargeUsed`**, com fallback de leitura zero quando não há tag. | Unidade de estado do item; não é mana Black Arcana. Persistência/migração real precisa de QA. |
| `hasCharge` | Compara `getCharge` com **1000** (`if_icmpge` salta para o falso). | O predicado indica elegibilidade enquanto `ChargeUsed < 1000` no método examinado. Não confundir valor gasto com energia disponível. |
| `use` | Consulta `hasCharge`, depois `findAmmo`, `Player.isCreative`, `ItemStack.isEmpty`, `ItemStack.shrink(1)` e `setCharge`, além de sons de início/recarga/sem munição. | Recarga nativa pode consumir item conforme os guards; não autorizar custo adicional em segundo pipeline. Tipo exato de munição e cada branch de consumo ainda requerem a auditoria do helper `findAmmo`. |
| `onUseTick @246–319` | Consulta `ENERGY_EFFICIENCY` e usa `Math.floor`, `Math.min`, `getCharge`, `setCharge`, o limite **1000** e literal **1.5f**. | Essa é a região de custo/consumo por tick; a fórmula completa e todos os guards ainda não estão selados para mudança de eficiência. |
| `onUseTick @332–352` | Consulta `GAMMA_RAY` via nível do encantamento e um sorteio booleano. | Não converter presença de encantamento em mudança garantida de dano/status; conferir branches e valores dos modos. |
| `setUseTime` | Tags `PrevUseTime` e `UseTime`. | Dados de animação/timing do item; não presumir que replicação ou salvamento prove autoridade do cliente. |
| `getBarWidth` | Usa literais **13.0f** e **1000.0f** junto de `getCharge`. | Escala do indicador visual, não alcance ou tamanho da colisão. |

Em `onUseTick` e `releaseUsing` são encontradas mensagens `UpdateItemTagMessage` enviadas por `sendMSGToServer`. A inspeção do **sender** não comprova autenticação no handler, integridade de `ChargeUsed`, antirreplay, autorização do ID de entidade nem enforcement de custos no servidor. Nenhuma perk pode tratar o pacote enviado como fonte autoritativa sem prova do receptor.

### Dano, owner e efeito secundário

- `RaygunItem.onUseTick @1013–1047` distingue `TremorzillaEntity` num ramo próprio, chama `ACDamageTypes.causeRaygunDamage(registryAccess, caster)` em `@1026` e solicita `ACCompat.hurt(target, damageSource, amount)` em `@1041`. Na decisão local imediatamente anterior a `hurt`, os operandos possíveis são **`2.0f`** e **`1.5f`**, condicionados a flag local `iload 18`. A origem completa da flag, o resultado de mitigação e a aceitação de cada hit não são certificados por esses números.
- O `DamageSource` recebe o *caster* como argumento da factory no trecho inspecionado; isso não garante crédito de kill, procs, Mastery ou políticas de PvP de mods externos. O retorno booleano de `ACCompat.hurt` participa dos guards posteriores; um evento visual ou um alvo dentro da AABB não certifica dano aceito.
- `onUseTick @1076–1119` verifica `ACTagRegistry.RESISTS_RADIATION`, referencia `ACEffectRegistry.IRRADIATED` e, em ramo condicionado, solicita `LivingEntity.addEffect` com `MobEffectInstance(..., **800 ticks**, amplifier local)`. Os 800 ticks são a duração **solicitada ao aplicar o efeito**, não duração universal do DamageType e nem prova de sucesso para todo hit. A ficha [Irradiated](../effects/irradiated.md) conserva o contrato de tick, exaustão e redução Hazmat.
- `onUseTick @1125–1154` monta `UpdateEffectVisualityEntityMessage`. Esse tráfego é downstream visual e não deve gerar um segundo proc de ataque ou ser usado como confirmação de aplicação do status.

### Requisitos antes de perks mutadoras

1. Fechar CFG e limites efetivos de distância/área, distinguir `X_RAY`, `GAMMA_RAY` e `ENERGY_EFFICIENCY` e os predicados usados nas buscas; não sobrescrever `ProjectileUtil` ou a filtragem de aliados.
2. Identificar `findAmmo`, custo completo de `ChargeUsed`, servidor autoritativo de tags e validação do `UpdateItemTagMessage`. Não duplicar recarga ou cobrança por feitiço.
3. Confirmar `ACCompat.hurt`, critérios de sucesso, hits múltiplos/por-tick, atribuição causal, escala de dano, imunidades, `Irradiated` e deduplicação de XP/procs.
4. Executar cliente/servidor dedicados com casos de níveis de enchantment, alvos aliados/mesmo veículo, Tremorzilla, resistência à radiação, `ItemStack` duplicado, save/reload e proteção de claims.

**Decisão:** a ficha continua `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; nenhum `COMPLETE_PERK_READY`, avanço de 24/30, nova raiz mágica ou promoção de Stage. Os parâmetros acima são **observações estáticas compiladas**, não contratos de intervenção seguros.

## Emissão C2S e recarga — auditoria do receiver no JAR 1.0.10

**Escopo estrito:** `SHA_EXACT_1010_RAYGUN_AMMO_AND_UPDATE_ITEM_TAG_C2S_SELECTED_BYTECODE`. A [evidência selada](../EXACT-RAYGUN-PACKET-AMMO-1.0.10.json) fixa a identidade do JAR, SHA-256 de `RaygunItem.class` e `UpdateItemTagMessage.class`, **13 métodos selecionados** (nove do item e quatro da mensagem) e os offsets dos dois envios. [PR do probe, testes e CI](https://github.com/Gustavaopere/Black-Arcana/pull/986). A auditoria não distribui implementações completas nem valida um cliente real.

### Munição / recharge

- `RaygunItem.findAmmo(Player)` percorre `Inventory.getContainerSize` e `Inventory.getItem`, testando `RaygunItem.AMMO` nos stacks. O predicado é preenchido pelo método compilado `lambda$static$0(ItemStack)`: compara o item com `ACBlockRegistry.URANIUM_ROD` convertido via `Block.asItem()`. **Identidade do insumo nativo:** item de `URANIUM_ROD`, não combustível genérico nem nova mana.
- `findAmmo` possui um ramo próprio para `Player.isCreative` e retorna `ItemStack.EMPTY` nesse ramo. Portanto, distinguir modo criativo do fluxo de procura/consumo; o retorno vazio do helper **não prova** falha automática da recarga criativa.
- `RaygunItem.use` consulta `hasCharge`, `findAmmo`, `isCreative`, `isEmpty`; contém `ItemStack.shrink(1) @65` e `setCharge(ItemStack,int) @79`. O literal `1` é o débito potencial de **uma unidade de munição no ramo correspondente**, não cobrança por cada tick de raio. O `0` passado ao setter no caminho de recarga é distinto do limite **1000** de `hasCharge`.
- `hasCharge` compara `ChargeUsed` com `1000` (`if_icmpge`) e `getCharge/setCharge` usam a tag `ChargeUsed`. A relação exata entre `ENERGY_EFFICIENCY`, custo por tick e todas as transições do item continua exigindo análise completa do fluxo de `onUseTick`.

### Transporte e dispatcher: quem pode ser alterado?

| Local compilado | Relação demonstrada | Limite |
|---|---|---|
| `onUseTick @162 / @165` | Constrói `UpdateItemTagMessage(entityId, itemStack)` e invoca `AlexsCaves.sendMSGToServer(Object)`. | O client envia dados, não prova que eles foram aceitos nem tratados como autoridade. |
| `releaseUsing @25 / @28` | Mesmo par construtor/envio, sob ramo que consulta `Level.isClientSide`. | Não equiparar mensagem enviada a liquidação de custo, dano ou cooldown. |
| `UpdateItemTagMessage.read/write` | Serializam `entityId` como inteiro e `itemStackFrom` via `PacketBufferUtils.readItemStack/writeItemStack`. | A serialização não valida semântica, propriedade da entidade, cooldown ou direitos do jogador. |
| `UpdateItemTagMessage.handle` | Consulta `ACNetworkContext.getSender` e `isClientSide`, com seleção de nível/contexto; usa `Level.getEntity(entityId)`, verifica tipo do item nas mãos MAIN_HAND/OFF_HAND e alcança `UpdatesStackTags.updateTagFromServer`. | **Não foi homologado** o vínculo de `entityId` com o remetente, o tipo concreto de item autorizado, a sanitização das tags ou o escopo de atualizações. |
| `handle @158 / @171 / @174` | Obtém tags de `ItemStack` por `ACCompat.getTag` e chama `UpdatesStackTags.updateTagFromServer(Entity, ItemStack, CompoundTag)`. | O efeito real depende da implementação de `UpdatesStackTags` do item selecionado e de guards prévios; não presumir cópia irrestrita de NBT sem provar o consumidor. |

**Distinção revisada na PR #990:** o `RaygunItem` **implementa diretamente** `UpdatesStackTags` (JAR 1.0.10); entre seus 26 métodos declarados não há override de `updateTagFromServer`, mas a interface fornece uma **implementação `default` compilada**. O método padrão chama `ACCompat.setTag`, que grava ou remove `DataComponents.CUSTOM_DATA`. O destino estático está identificado; autorização do pacote, limites de atualização e efeitos físicos permanecem `NOT_VERIFIED`.

### Fronteira de segurança e pending QA

A evidência de referência da mensagem confirma *resolução por ID de entidade* e *seleção de mão por igualdade de item*, mas não substitui revisão de seu fluxo de controle, da identidade do remetente, do código do implementador de `UpdatesStackTags`, das regras de rede e do resultado em servidor. **Não há vulnerabilidade demonstrada, tampouco garantia demonstrada de autorização segura.** Nenhuma perk deve confiar no `ItemStack` recebido como estado de carga autoritativo.

Próxima auditoria obrigatória: identificar a hierarquia concreta do `RaygunItem`, quem implementa `UpdatesStackTags`, quais tags o callback admite, origem de `entityId` e política real de rate-limit/replay; depois executar no modpack exato cliente manipulado/servidor dedicado, mãos distintas, troca de item em trânsito, entityId de outro jogador, reconnect e reload. O Black Arcana não deve alterar esse pacote nem introduzir segundo pipeline de recarga.

**Estado após a auditoria:** `raygun` ⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. Sem atualização dos índices, contagem de 24/30, Stage ou homologação global.

## Contrato SHA-exato — receiver real, interface e `CUSTOM_DATA` (PR #990)

**Escopo:** `SHA_EXACT_1010_RAYGUN_C2S_RECEIVER_JVM_DISPATCH_ONLY`. [Manifesto de quatro classes](../EXACT-RAYGUN-RECEIVER-1.0.10.json) · [PR #990](https://github.com/Gustavaopere/Black-Arcana/pull/990) · [workflow JDK 21](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-raygun-receiver.yml). O manifesto fixa o JAR publisher 1.0.10 por SHA-1/SHA-256/tamanho, quatro SHA-256 de classes, cinco descritores/digests de métodos e 13 anchors de emissão/recepção. Os dados são de bytecode compilado — não observação de cliente ou autorização de servidor.

### Implementação que recebe a atualização

- `RaygunItem.class` — SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`. Declaração JVM: estende diretamente `net.minecraft.world.item.Item` e **implementa `com.github.alexmodguy.alexscaves.server.item.UpdatesStackTags`**, além de outras interfaces. Os 26 métodos declarados não sobrescrevem `updateTagFromServer`.
- `UpdatesStackTags.class` — SHA-256 `1ba03e1d244a0a6ad49a888cb406bf518858c52988b4210db204c0bbd1e6e0ad`. Seu único método declarado é **`public default void updateTagFromServer(Entity,ItemStack,CompoundTag)`**, cuja implementação compilada chama `ACCompat.setTag(ItemStack,CompoundTag)` em `@2`. Isto resolve a rota herdada pelo Raygun sem inventar um override no item.
- `ACCompat.class` — SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`. `setTag(ItemStack,CompoundTag)` usa `DataComponents.CUSTOM_DATA`: com tag nula, invoca `ItemStack.remove(CUSTOM_DATA) @8`; com tag presente, constrói `CustomData.of(tag) @20` e invoca `ItemStack.set(CUSTOM_DATA,value) @23`. Trata-se de escrita em dados do item, **não** da aplicação de dano, mana, status ou cooldown.

### Gates observados no pacote

| Offset em `UpdateItemTagMessage.handle` | Decisão / referência compilada | Limitação |
|---|---|---|
| `@8`, `@15`, `@20–31` | Consulta `ACNetworkContext.getSender`, `isClientSide` e, no ramo cliente, `PROXY.getClientSidePlayer`; sai caso não exista jogador | Ter um sender/contexto é diferente de verificar a autoria de cada `entityId` recebido |
| `@39–50` | Resolve `entityId` via `Level.getEntity(int)` no nível do jogador; exige `LivingEntity` | Não foi comprovado vínculo obrigatório entre remetente e entidade escolhida |
| `@70–129` | Compara o tipo do item do payload com o item da mão principal e, se necessário, secundária; escolhe o `ItemStack` correspondente | Igualdade de tipo do item não certifica que o stack e seu `CUSTOM_DATA` foram originados do servidor |
| `@131–161` | Exige stack de mão não nulo, `instanceof UpdatesStackTags` e `ACCompat.getTag(payloadStack) != null` | O guard aceita um `CompoundTag` presente, mas não demonstra validação semântica dos campos `ChargeUsed`/`UseTime` |
| `@171–174` | Extrai a tag do payload e chama `UpdatesStackTags.updateTagFromServer(entity,heldStack,tag)` | O método `default` repassa essa tag ao setter de `CUSTOM_DATA` do stack selecionado, sujeito aos caminhos anteriores |

**Distinção de autoridade:** a cadeia de referências `RaygunItem.onUseTick/releaseUsing → UpdateItemTagMessage → handle → UpdatesStackTags.default → ACCompat.setTag → DataComponents.CUSTOM_DATA` está confirmada estaticamente para a versão 1.0.10. Isso não comprova que o servidor aceite qualquer mensagem arbitrária, pois o registro/validação do canal, sua direção, os checks de autorização fora do handler e o resultado em sessão real **não foram auditados integralmente**. Também não comprova que os valores de carga ou de tempo estejam saneados por outros consumidores. Não declarar exploit nem segurança demonstrada a partir de uma inspeção local.

**Pontos de QA / perks:** investigar política de rede e vínculo remetente-`entityId`, alteração de mão ou stack durante trânsito, validação de `ChargeUsed` e `UseTime`, persistência de `CUSTOM_DATA`, replay, efeitos de encantamentos, proteção em PvP e origem de XP/Mastery. Qualquer perk de custo ou duração deve operar via boundary nativa comprovada e server-authoritative; nenhuma modificação do pacote fica autorizada por esse manifesto.

**Status:** ⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. Contador de Alex's Caves Continued **24/30 (80%)**, sem promoção de objetos, hooks ou Stage. O suporte de `UpdatesStackTags` é um contrato de atualização de estado de item, não uma nova magia.

## Registro nativo C2S — descoberta delimitada sem certificação

Nova trilha independente de [inspeção do registro do pacote e aceitação](../../../../../docs/qa/alexscaves-1010-raygun-network-handoff.md), com [probe read-only](../../../../../docs/qa/alexscaves_1010_raygun_registration_probe.py) e [CI JAR SHA-exata](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-raygun-registration.yml).

O recorte busca classes candidatas que referenciam `UpdateItemTagMessage` ou `ACNetworkContext` no binário exato. Esses tokens e callsites não demonstram, por si, registro do canal, direção da mensagem, validação de `entityId`, pertencimento do `ItemStack` ou sanitização de `CUSTOM_DATA`. A associação causal do dano com o caster deve continuar condicionada à aceitação nativa de `ACCompat.hurt` e aos guards de alvo do provider. O novo probe não reimplementa as funções nem substitui os três manifestos Raygun existentes.

**Estado inalterado:** ⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. Sem novo contrato estático ou alteração de contadores/Stage.

## Registro nativo verificado por ABI — ACNetwork 1.0.10

O manifesto SHA-exato [EXACT-RAYGUN-NETWORK-ABI-1.0.10.json](../EXACT-RAYGUN-NETWORK-ABI-1.0.10.json) acrescenta aos recortes de sender/receiver as entradas do registro de rede nativo do provider, extraídas do JAR publisher 1.0.10 (classe `ACNetwork.class`, SHA-256 `8544a3436444be3248f9176bbcdee5fa30ee45ec2fbcf7a35a5e4fe4d9d88482`). O [probe e seus testes](../../../../../docs/qa/alexscaves_1010_raygun_network_abi_probe.py) selam três métodos, descritores, digests, offsets e sete âncoras. Evidência de execução SHA-exata: [Actions 41333495556](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41333495556).

| Entrada real | Contrato ABI observado | Limite de uso por perks |
| --- | --- | --- |
| `ACNetwork.registerMessages()` | `ldc UpdateItemTagMessage @151`; `register(Class,BiConsumer,Function,BiConsumer) @168` | Entrada da mensagem na tabela interna; não é prova isolada de autorização de `entityId` |
| `ACNetwork.registerPayloads(RegisterPayloadHandlersEvent)` | `registerMessages @0`; `registrar @12`; `PayloadRegistrar.playBidirectional @22` | O **envelope/payload comum** usa registro bidirecional NeoForge; não foi observado registro exclusivo de `UpdateItemTagMessage` como payload separado |
| `ACNetwork.lambda$registerPayloads$0(ACPayload,IPayloadContext)` | `ACNetwork$NeoForgeContext.<init> @24`; `ACNetwork$Entry.handle @27` | Callback encaminha via entrada interna, sem prova de validação de autoria, alvo, mão, `ChargeUsed` ou `UseTime` |

**Boundary:** os opcodes acima não autorizam modificar `DataComponents.CUSTOM_DATA`, duplicar consumo nativo, nem alterar seleção/dano do Raygun. Os guards do receiver não comprovam vínculo sender–`entityId`, limites semânticos de payload, replay protection ou QA física. `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`; sem mudanças em contadores/Stage.
