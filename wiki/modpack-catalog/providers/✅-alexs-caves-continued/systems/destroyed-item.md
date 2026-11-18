# ACDestroyedItem — callback de destruição de item (1.0.10)

**Contrato técnico estático:** ✅ `CERTIFIED_STATIC_7_AXES`, com escopo `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hook mutador e execução no modpack:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perks executáveis:** `NOT_CERTIFIED`. **Política:** `NO_MUTATION`. O provider permanece `OPEN`; esta ficha de suporte acrescenta **+0 raízes mágicas**.

## 1. Identidade, autoridade e escopo

`com.github.alexmodguy.alexscaves.server.item.ACDestroyedItem` é uma interface de suporte: **zero campos, zero superinterfaces e um método público abstrato**, `onDestroyed(ItemEntity,DamageSource):void`. Seu descritor JVM é `(Lnet/minecraft/world/entity/item/ItemEntity;Lnet/minecraft/world/damagesource/DamageSource;)V`; access flags **1025**. Ela não contém corpo, registro de evento, scheduler, custo ou implementação de cast.

Autoridade nativa: **`alexscaves-1.0.10-neoforge+1.21.1.jar`**, Minecraft **1.21.1**, NeoForge, Java **21**; CurseForge projeto **1645389**, arquivo **8856293**; **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A [prova delimitada](../EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.md) e o [manifesto nativo](../EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.json) sustentam os sete eixos desta ficha. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve somente como corroboração adjacente.

O censo das **1.555 entradas `.class`** encontra **um implementador direto**, `RadioactiveOnDestroyedBlockItem`, e nenhuma subclasse adicional desse implementador no JAR. Sua hierarquia é `RadioactiveOnDestroyedBlockItem` → `RadioactiveBlockItem` → `com.github.alexmodguy.alexscaves.citadel.item.BlockItemWithSupplier` → `BlockItem` externo. A cópia Citadel é relocada no mesmo artefato; não acrescenta provider ou ficha individual.

| Objeto nativo | SHA-256 do classfile |
|---|---|
| `ACDestroyedItem` | `2ccc084cf825941414561ed02362fc3776b5ddddd699c8c62952818956771100` |
| `RadioactiveOnDestroyedBlockItem` | `853e1f6318cfaa2c97ab27955e6b068e4e5f34ab94f4354092233e69bc502f24` |
| `RadioactiveBlockItem` | `1c769a4b64f0e4b3b9a2f5589bfc44ce3e27ec46c616b447d4e1359ffb21bd4b` |

O certificado cobre a ABI, o callback completo, a hierarquia nativa relevante, a factory/ponte de registro delimitada, os helpers de cor e holder e o consumidor nativo finito de `IRRADIATED`. Os corpos integrais de `AreaEffectCloud`, explosão, seleção de vítimas, eventos, proteção territorial e sincronização da engine não são promovidos a contratos certificados desta ficha.

## 2. Ativação, despacho e ordem de execução

O censo nativo encontra **zero referências tipadas de chamada à interface `ACDestroyedItem`**. A chamada nativa ao overload de dois argumentos observada é a própria superchamada do implementador, com owner simbólico `RadioactiveBlockItem`. Portanto o marcador não demonstra um dispatcher próprio do provider, nem exclui chamadas externas, reflexão ou transformações.

A referência externa oficial NeoForge **21.1.250** / Minecraft **1.21.1**, selada em [manifesto próprio](../EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json) e descrita na [prova comum](../EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.md), comprova dois defaults e um trecho de despacho. A sequência distingue essa prova direta da derivação condicionada pela hierarquia externa:

1. O trecho oficial selecionado de `ItemEntity.hurt` mostra a redução da saúde do drop e, quando ela fica `<=0`, a chamada `getItem().onDestroyed(this,damageSource)` **antes** do `discard` posterior da engine. Esse trecho não certifica o corpo integral, todos os guards ou os caminhos de lado do método.
2. O default `IItemStackExtension.onDestroyed(ItemEntity,DamageSource)` obtém o item do stack e encaminha os dois argumentos ao item concreto.
3. O item concreto declara esse overload no JAR nativo. **Assumida a hierarquia externa padrão `BlockItem` → `Item`, sem outro corpo do overload no caminho**, a regra JVM de resolução da superchamada conduz ao default de `IItemExtension`, que chama virtualmente `onDestroyed(ItemEntity)` de um argumento. O trecho oficial 21.1.250 prova que `Item` implementa `IItemExtension`; a relação `BlockItem` → `Item` foi inspecionada somente na referência compilada auxiliar 21.1.248, sem equivalência física declarada. Esse elo é uma derivação condicionada, não uma certificação independente da hierarquia externa 21.1.250 ou transformada.
4. O overload de um argumento fornecido pelo `BlockItemWithSupplier` relocado faz limpeza de conteúdo **somente se o supplier produz `ShulkerBoxBlock`**: troca `DataComponents.CONTAINER` por `ItemContainerContents.EMPTY` e, se o conteúdo anterior não é nulo, encaminha `nonEmptyItems()` a `ItemUtils.onContainerDestroyed`. Esse corpo não chama `discard`. O supplier nativo positivo desta ficha produz `WasteDrumBlock`.

`RadioactiveBlockItem` não declara o overload de dois argumentos. O nome do owner na `invokespecial` não é prova de um corpo ausente nessa classe; a resolução envolve a hierarquia e o default externo. As pontes e o trecho de despacho combinam patches oficiais pinados de userdev com bytecode dos defaults no universal: **`PINNED_USERDEV_PATCH_PLUS_UNIVERSAL_BYTECODE_REFERENCE`**. Isso não autentica a hierarquia externa integral, a engine instalada, a execução física ou alterações de outros mods.

O callback completo tem **170 bytes de `Code`**, SHA-256 `34f73b931946ae63544f4cbe9e35d1bd10fcab90f25b000bbdc54b98bc8b8881`, sem exception handler próprio:

| Ordem / offsets | Operação e condição |
|---|---|
| `@0–3` | Executa a superchamada de dois argumentos; ela precisa retornar normalmente para alcançar os guards locais |
| `@6–10` | Se `DamageSource.isCreativePlayer()` é verdadeiro, retorna em `@169` |
| `@13–17` | Se `ItemEntity.isRemoved()` é verdadeiro, retorna em `@169` |
| `@20–21` | Descarta o `ItemEntity` recebido |
| `@24–127` | Constrói e configura uma `AreaEffectCloud` no mundo e posição desse item |
| `@130–138` | Solicita `Level.addFreshEntity(cloud)`; descarta o retorno booleano |
| `@139–168` | Solicita a explosão e descarta seu retorno; retorna em `@169` |

Os guards de Creative e remoção estão **depois** da superchamada. Não há guard local de lado cliente/servidor, seleção de player beneficiário, validação de nulos, cooldown ou teste aleatório de destruição. Um retorno **`false`** de `addFreshEntity` não impede a explosão; uma exceção que interrompa a execução anterior pode impedi-la. O método não recupera falhas próprias, não desfaz o descarte anterior e não verifica o sucesso físico dos pedidos.

## 3. Registro nativo, parâmetros e saídas

A ponte é `ACBlockRegistry.registerBlockAndItem(String,Supplier,int)` → `getBlockSupplier(int,Supplier)`. O **seletor 5**, ramo `@87–93`, usa bootstrap **8** → `lambda$getBlockSupplier$441`, que instancia `RadioactiveOnDestroyedBlockItem` e passa **`0.01f`** ao construtor. O censo do inicializador encontra **uma** inscrição com esse seletor:

| Consumidor positivo | Janela de registro / supplier |
|---|---|
| `alexscaves:waste_drum` / `WASTE_DRUM` | Literal `@2192`, supplier bootstrap **166** `@2195` → `lambda$static$154` → `new WasteDrumBlock`; seletor **5** `@2200`, registro `@2201`, campo `@2204` |

**Controle negativo de identidade:** `radrock_uranium_ore`, `block_of_uranium` e `unrefined_waste` usam **seletor 4**, ramo `@80–86`, bootstrap **7** → `lambda$getBlockSupplier$440` → **`RadioactiveBlockItem` comum**, com `0.001f`. Esses três registros não recebem a implementação de destruição desta ficha. A proximidade no registro ou o nome radioativo não os transforma em consumidores desse callback.

O construtor do implementador somente encaminha supplier, `Item.Properties` e float ao pai. O pai guarda o float em `randomChanceOfRadiation`; seu `acInventoryTick` usa `stackCount × randomChanceOfRadiation` e um fator Hazmat em outro fluxo. **`0.01f` não é chance da nuvem/explosão:** o callback de destruição não lê esse campo, o tamanho do stack ou RNG.

| Campo | Valor / operação exata do callback | Interpretação delimitada |
|---|---|---|
| Drop consumido | `ItemEntity.discard() @21` | Descarta a entidade do stack; não há `shrink(1)` ou multiplicação por contagem |
| Origem da nuvem | `new AreaEffectCloud(item.level(),x,y,z) @24–44` | Coordenadas do item, sem deslocamento vertical adicional |
| Partícula | `ACParticleRegistry.GAMMAROACH @49–60` | Apresentação, sem tipo de dano implícito |
| Cor | `ACCompat.setCloudColor(cloud,7853582) @64–66` / **`0x77D60E`** | Helper monta `PotionContents` sem potion base, com cor customizada e lista vazia, e chama `setPotionContents`; o status é acrescentado depois |
| Status bruto | `IRRADIATED`, **9600 ticks**, **amplificador 1**, `MobEffectInstance(Holder,int,int) @70–95` | Parâmetros entregues à nuvem; não duração final garantida em cada vítima |
| Raio inicial | **`2.0f @99–100`** | Raio da nuvem, sem equivalência com potência/raio de dano da explosão |
| Duração da nuvem | **`12000 ticks @104–107`** | Duração nominal distinta da instância de status; 600 s somente sob 20 ticks/s |
| Espera | **`0 @111–112`** | Não elimina outros intervalos, delays ou filtros do consumidor externo |
| Variação radial | **`-getRadius()/((float)getDuration()) @115–127`** | Com os valores fornecidos: **`-2/12000 = -1/6000` unidade/tick**; clamps, expiração e trajetória efetiva dependem da engine |
| Spawn | `Level.addFreshEntity(cloud) @135`, `pop @138` | Uma solicitação; aceitação e replicação não verificadas |
| Explosão | `Level.explode(null,x,y+0.5,z,1.8f,ExplosionInteraction.BLOCK) @139–165` | Uma solicitação independente do booleano do spawn; fonte explícita nula e potência **1.8**, sem raio de dano fixo comprovado |

`ACCompat.effect(MobEffect)` usa `BuiltInRegistries.MOB_EFFECT.wrapAsHolder`. Nenhum desses helpers cria caster, perk ou owner. O corpo próprio produz **uma nuvem e uma solicitação de explosão por passagem normal pelos guards**, não uma por unidade do stack. Reentrada, despacho externo adicional e aceitação física não foram testados.

## 4. Targeting, dano e ownership

O callback não percorre entidades, não faz raycast/LOS, não seleciona aliados/inimigos e não chama diretamente `LivingEntity.hurt`. A nuvem e a explosão delegam seleção, distância, proteção, dano e aplicação de status à engine. Não há parâmetro de alcance de cast, projétil, cura, knockback ou quantidade máxima de alvos no contrato próprio.

O consumidor nativo delimitado de `IRRADIATED` acrescenta informação útil sem certificar o pipeline integral da nuvem:

| Consumidor / decisão | Comportamento nativo observado |
|---|---|
| `IrradiatedEffect.<init>` | Categoria `HARMFUL`, cor `7853582` |
| `ACMobEffect.shouldApplyEffectTickThisTick` | Encaminha duração e amplificador para `shouldTick` e retorna o resultado |
| `IrradiatedEffect.shouldTick(duration,amplifier)` | Amplificador `<=0`: falso. Para positivo, `interval=200/amplifier` por divisão inteira; se `interval>1`, testa `duration % interval == interval/2`; caso contrário, verdadeiro. **Amplificador 1 pede `duration % 200 == 100`**, se o scheduler externo consultar esse método com esses argumentos |
| `ACMobEffect.applyEffectTick` | Chama virtualmente `tick(entity,amplifier)` e retorna verdadeiro se a chamada retorna normalmente |
| `HazmatArmorItem.getWornAmount` | Conta identidades exatas: `HAZMAT_MASK` em HEAD, `HAZMAT_CHESTPLATE` em CHEST, `HAZMAT_LEGGINGS` em LEGS e `HAZMAT_BOOTS` em FEET, de 0 a 4 |
| `IrradiatedEffect.tick` | Calcula **`r=1-0.25×peçasHazmat`**. Para `Player` com zero peças, solicita **`causeFoodExhaustion(0.4f)`**. Para entidades que **não são `RaycatEntity`**, se `nextFloat() < r+0.1f`, solicita **`hurt(causeRadiationDamage(registryAccess),r)`** e ignora o booleano retornado |
| `ACDamageTypes.causeRadiationDamage` | Busca o holder de `RADIATION` no registry `DAMAGE_TYPE` e constrói `DamageSourceRandomMessages(holder,2)`; não recebe o destruidor do drop ou um player |
| `IrradiatedEffect.getCurativeItems` | Retorna `List.of()`; a declaração nativa isolada não comprova binding nem eficácia das rotas de cura da engine atual |

O amplificador controla o agendamento nativo por divisão inteira; `tick` não o usa como multiplicador direto do valor `r`. Com quatro peças, o corpo ainda pode solicitar `hurt(...,0)` quando o teste aleatório passa; isso não prova dano aceito, imunidade global, proteção contra explosão ou imunidade à aquisição do status. A exclusão de Raycat pertence ao pedido de dano desse tick, sem garantia sobre a explosão.

A duração **9600** é entrada bruta de `addEffect`; não se deriva daqui número de ticks aplicados, pulsos, DPS ou dano total. A frequência real de consulta, a duração entregue à vítima, reaplicação e interação com outros efeitos pertencem aos consumidores externos. A ficha de [Irradiated](../effects/irradiated.md) conserva seu escopo próprio.

O `DamageSource` recebido pelo callback serve ao superencaminhamento e ao guard de Creative. **Não é prova de caster ou titular de perk.** A nuvem não recebe `setOwner` neste corpo; a explosão recebe `null` como entidade-fonte; o helper de radiação não recebe entidade. Crédito de kill, XP, Mastery, loot, logs e autoria efetiva continuam `NOT_VERIFIED`.

## 5. Custos, tempo, configuração, persistência e rede

O consumo próprio observável é o descarte do **`ItemEntity` inteiro**. O callback não lê quantidade de itens nem cobra mana, souls, stamina, XP, munição extra ou durabilidade; não contém cooldown, recarga, nível de perk, configuração numérica ou scheduler próprio. Isso não elimina custos de aquisição, dano anterior ao drop ou regras de outros owners.

Os tempos são distintos: **12000 ticks de nuvem**, **9600 ticks no payload de status**, **waitTime 0**, contração radial fornecida ao setter e agendamento do consumidor nativo de Irradiated. Não há base para um único multiplicador de duração que preserve todas essas relações. O float **0.01** pertence ao fluxo de radiação de inventário, que tem guards próprios de servidor, entidade viva, exclusão de Player Creative e ausência prévia de Irradiated; não é recurso ou cooldown de destruição.

Não há campo próprio no implementador, UUID, armazenamento por jogador, packet, handler de reload ou leitura/escrita de save no callback. Construir entidades e chamar o mundo não certifica persistência, unload de chunk, save/reload, sincronização de partícula/status, alcance de tracking ou execução única em multiplayer. O descarte, a nuvem e a explosão permanecem sob autoridade de suas classes e da engine.

## 6. Integração e sete eixos de decisão para perks

O provider mantém a autoridade do descarte, spawn, status e pedido de explosão. RPG Skill Tree mantém a progressão, atributos, perks, Mastery e seus gates. Black Arcana precisa de um boundary real antes de alterar esses pedidos e de uma atribuição de jogador comprovada antes de conceder progressão; esta interface não fornece ambos por si.

| Eixo | Informação utilizável / gate de integração |
|---|---|
| Identidade e ativação | Interface de suporte, um implementador e **`waste_drum` seletor 5**. Não conceder perk aos três itens de seletor 4 nem transformar destruição em novo cast |
| Comportamento e potência | Descarte → nuvem → explosão; parâmetro **1.8** da explosão é distinto do dano `r` do status. Não duplicar `explode`, `hurt`, spawn, XP ou Mastery |
| Parâmetros e escala | Raio **2**, duração **12000**, status **9600/amp1**, contração **-raio/duração**. Uma alteração de área/tempo exige definir qual parâmetro e qual consumidor controla |
| Targeting e ownership | Não há seleção própria ou player confiável; `DamageSource` e posição do drop não autorizam bônus por jogador. Raycat/Hazmat têm efeitos delimitados no consumidor de radiação |
| Custo, cooldown e estado | O drop inteiro é descartado; nenhum custo de skill ou cooldown próprio. Não acrescentar cobrança ou reexecução para simular mutação sem hook transacional |
| Compatibilidade e proteção | `ExplosionInteraction.BLOCK` e ausência de guard local de claims exigem boundary de `WorldEffectPolicy`. O despacho de referência não valida chamadas externas, guards de lado, claims, PvP, eventos ou composições com Epic Fight/Enshrouded |
| Validação e execução | Contrato estático fechado no recorte e referências pinadas identificadas; engine instalada, hook de mutação, crédito, rede e QA física seguem sem homologação |

Perks conceituais de área, duração, tolerância à radiação ou redução de consequências têm parâmetros identificados para investigação. **Nenhum hook mutador por player foi verificado.** Alterar constantes globais, o supplier ou o default externo não equivale a um perk isolado por jogador. **Integração executável: `NOT_CERTIFIED` / `NO_MUTATION`.**

## 7. Evidência reproduzível, histórico e limites de validação

O [auditor estático delimitado](../../../../../docs/qa/alexscaves_1010_destroyed_item_contract_audit.py), seus [testes semânticos negativos](../../../../../docs/qa/alexscaves_1010_destroyed_item_contract_audit_test.py) e o [workflow](../../../../../.github/workflows/alexscaves-1010-destroyed-item-contract.yml) são novos e separados do probe de descoberta. O manifesto relaciona hashes de classe/código, corpos completos, referências tipadas, bootstrap/factory, registro positivo e controles negativos. A [prova comum](../EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.md) registra a autoridade e os limites da ponte externa pinada.

Reprodução nativa de leitura somente, com JDK 21 e o JAR publisher exato: `python3 docs/qa/alexscaves_1010_destroyed_item_contract_audit.py --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar --javap /caminho/jdk-21/bin/javap --output /caminho/novo/destroyed-item-contract.json`. A forma exata dos comandos e da comparação com o manifesto está na prova comum; gerar o JSON não executa Minecraft.

O [checkpoint histórico parcial](EXACT-DESTROYED-ITEM-HISTORICAL-CARD-1.0.10.md) preserva **os 9.143 bytes originais**, SHA-256 `80e185f57698f54181bf49bf11998fb67499f158d8c9ec50d3aee01fbb2bec9d`. Seu estado `NOT_CERTIFIED` e suas pendências refletem a descoberta daquele momento; não são reescritos retroativamente. O probe histórico `docs/qa/alexscaves_1010_destroyed_item_probe.py`, workflow `.github/workflows/alexscaves-1010-destroyed-item-probe.yml`, [job SUCCESS de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44212177669/job/134493028293) no commit `f7adadedb746f0c84f7b308088bc85600f682927` e [artefato JSON temporário](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44212177669/artifacts/14386187733) conservam somente o escopo de descoberta SHA-exata.

QA física pendente: dano admitido/recusado e limites da saúde do drop; Creative, item já removido e superchamada; lado cliente/servidor e invocações externas; stack de várias unidades; spawn recusado e exceções; nuvem, aplicação/reaplicação e duração efetiva do status; Hazmat/Raycat e dano aceito; explosão, claims/PvP e eventos; autoria/crédito único; save/reload, chunks, dimensão, tracking, multiplayer e integração no modpack. Não se certifica toda a engine de área/dano para concluir o contrato estático próprio.

**Contabilidade:** uma ficha técnica **já existente**, **+0 candidatos novos**, **+1 certificado estático delimitado**, **+0 raízes mágicas**, **+0 fichas de itens/efeitos/providers derivadas**. Estados finais: `static_technical_contract=CERTIFIED_STATIC_7_AXES`, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`, `provider_universe_closed=false`.
