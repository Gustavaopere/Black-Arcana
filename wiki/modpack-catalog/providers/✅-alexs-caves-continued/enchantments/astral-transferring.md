# Astral Transferring — `alexscaves:astral_transferring` (1.0.10)

**Contrato técnico individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. A ficha conclui a identidade publisher, o ramo nativo de transferência e seus helpers de vínculo, custo e sincronização no recorte estático descrito. **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION`. O runtime transformado do pack permanece não verificado. O encantamento modifica a [ação nativa do Totem of Possession](../actions/totem-possession-remote-control.md): **+0 raízes mágicas**, nenhuma nova ação de cast e nenhuma perk executável.

## 1. Identidade, registro e proveniência

- **Provider / ID:** Alex's Caves Continued / `alexscaves:astral_transferring`; encantamento do `alexscaves:totem_of_possession`.
- **Publisher:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**. O `META-INF/neoforge.mods.toml` declara mod ID `alexscaves`, versão `1.0.10`, Minecraft `[1.21.1]`, NeoForge e dependência obrigatória `codxlib >=1.3.6`; a análise usa Java 21.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Classe principal:** `com/github/alexmodguy/alexscaves/server/item/TotemOfPossessionItem.class`, SHA-256 `bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e`.
- **Nome / descrição literais em `en_us.json`:** “Astral Transferring” / “Mobs possessed by the Totem of Possession can swap possessed status with other, healthier mobs they fight”. O `pt_br.json` contém “Totem de Possessão” para o item, mas **não contém nome nem descrição deste encantamento**. O texto técnico em português nesta ficha é uma paráfrase; a descrição inglesa não substitui os predicados compilados.
- **Prova atual:** [manifesto individual SHA-exato](../EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json), [contrato técnico consolidado](../EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.md) e [regressão semântica da ficha](../../../../../docs/qa/alexscaves_1010_astral_transferring_cards_test.py). O manifesto sela recursos, classes, âncoras e a ficha final.

O inicializador de `ACEnchantmentRegistry` liga o literal `astral_transferring @347` a `key @350` e ao campo `ASTRAL_TRANSFERRING @353`; `key(String)` completo constrói a ResourceKey em `Registries.ENCHANTMENT` com namespace `alexscaves`. O registro de item liga `totem_of_possession @2313` ao supplier de bootstrap **131**; seu handle resolve `lambda$static$126`, cujo corpo completo cria `TotemOfPossessionItem`.

O censo de Fieldrefs da chave exata encontra a escrita de registro e **um leitor direto**, `TotemOfPossessionItem.onUseTick @920`. A descoberta por constantes brutas só apontou essas duas classes; ela não é, isoladamente, prova de leitura nem exclui consumidores indiretos, reflexão ou transformações de runtime. O censo separado do marcador `TotemPossessed` inclui os dois mixins descritos abaixo.

A fonte pública [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e serve somente de contexto adjacente. Os valores e os offsets desta ficha têm autoridade no publisher **1.0.10**.

## 2. Configuração, aplicação e aquisição

| Campo de `data/alexscaves/enchantment/astral_transferring.json` | Valor publisher 1.0.10 | Significado delimitado |
|---|---|---|
| SHA-256 | `41133c10af9c9e8d5e33d1b8339b734f81547b141f83fc0144aa9cf89f1f04c2` | Recurso de 379 bytes |
| `description.translate` | `enchantment.alexscaves.astral_transferring` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/totem_of_possession` | Tag nativa contém somente `alexscaves:totem_of_possession` |
| `weight` / `max_level` | `2` / `1` | Peso declarativo e nível nativo I |
| `min_cost` | `base=1`, `per_level_above_first=12` | `1 + 12 × (L−1)`; para I: **1** |
| `max_cost` | `base=41`, `per_level_above_first=10` | `41 + 10 × (L−1)`; para I: **41** |
| `anvil_cost` / `slots` | `4` / `mainhand` | Dados de aplicação; o consumidor lê a stack em uso |

O JSON não declara `effects` nem `exclusive_set`; a troca é implementada em Java. A varredura das **51 definições nativas de encantamento** encontra uma única exclusão reversa deste ID: `detonating_death.json` declara `exclusive_set: ["alexscaves:astral_transferring"]`, SHA-256 `8402461954ff5b249ae675b51d7dcc23d933b2b06c494b327bf608371298646e`. Isso fecha as exclusões declaradas no publisher; não certifica datapacks ou modos de aplicação não convencionais.

Astral aparece explicitamente nas quatro tags nativas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable`; cada arquivo tem 1.631 bytes e SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. São dados de disponibilidade, sem chance observada de mesa, loot ou trade. A tag de item tem 59 bytes, SHA-256 `185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf`. A resolução final de tags e encantamentos depende dos datapacks ativos.

A receita shaped do Totem é `DED` / `DBD` / `DBD`: **seis `moth_dust`, dois `thornwood_branch` e um `occult_gem`**, resultado `alexscaves:totem_of_possession`, com `count` omitido (uma unidade por padrão da receita). O recurso tem 415 bytes, SHA-256 `66abfc1425daee7e89b87f145c4148747a00a29fd45b96222869783e42ed710b`. A receita fabrica o equipamento; não é custo de ativação de Astral.

`ACCompat.enchantLevel` completo retorna o primeiro nível armazenado cujo Holder corresponde à ResourceKey, ou zero. Não aplica clamp próprio de nível máximo, slot ou tag de item. O ramo Astral exige **nível >0**; níveis positivos forçados passam pelo mesmo predicado, **sem escala por nível ou chance aleatória própria de transferência** nesse ramo. O nível zero ou negativo o rejeita.

## 3. Entrada, duração e seleção de candidatos

O `onUseTick(Level,LivingEntity,ItemStack,int)V` tem **478 instruções / 59 branches**, digest do parse JVM `4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39`. Digest de parse não é hash do classfile. Todos os offsets desta seção e da próxima pertencem a esse método exato.

O método resolve a entidade controlada **uma vez**, em `getControlledEntity @3`, conservando-a na **local 5 @6**. As guardas iniciais consultam vínculo, existência/vida e dano máximo do item. O caminho de encerramento chama `setPossessed(entity,false) @109`, `resetBound @113` e `stopUsingItem @117`; no cliente pode enviar `UpdateItemTagMessage`. O corpo contém antes disso um ramo de **Detonating Death**, explicitamente fora das janelas atuais. A prova não atribui essa explosão a Astral.

A continuação exige vínculo resolvido e o helper `isEntityLookingAt(user,controlled,5D)` ou Sightless. O helper completo usa o parâmetro ajustado por `1 + 0.1 × distância`, produto escalar entre vetores normalizados, limiar dependente da distância até o alvo e `hasLineOfSight`; **`5D` não é raio de cinco blocos**. Um Player controlado também passa pela configuração geral em `@177–203`; quando ela é falsa, esse caminho interrompe o uso. O valor lido da configuração do pack permanece desconhecido.

`getUseDuration` retorna **72.000 ticks** e `getUseAnimation` retorna **BLOCK**. Em `@275–284`, a local 6 recebe **`elapsed = 72000 − timeLeft`**, onde `timeLeft` é o argumento inteiro da chamada. Esse valor define a cadência Astral; não é um cooldown persistido nem garantia de uma possessão durante 72.000 ticks. Navegação/movimento e sua rampa pertencem a outro trecho nativo, omitido do selo atual; não fornecem um alcance novo para Astral.

**Guarda de lado:** `Level.isClientSide @652; ifeq @655 → 717` entra na consulta somente pelo ramo servidor. O caminho cliente de partículas sai por `goto @714 → 1084`. Portanto o ramo nativo de candidatos/ataque/transferência abaixo está atrás da guarda de servidor. Isso não certifica autenticação de pacotes, transformações por outros mods ou settlement efetivo.

| Etapa do seletor servidor | Predicado nativo completo nas janelas |
|---|---|
| Área | `controlled.getBoundingBox @719`, inflada em **3 por eixo** (`@722–725`); é uma AABB, sem raio esférico ou AoE de dano declarado |
| Tipo do controlado | Precisa ser `Player` ou `Mob` (`@730–743`) para entrar na iteração |
| Consulta | `Level.getEntities(controlled,box,predicate) @756` exclui a entidade fornecida; bootstrap **1** do predicado resolve diretamente `Entity.canBeHitByProjectile()Z` |
| Filtros do loop | Rejeita identidade com o controlado, `controlled.isAlliedTo(candidate)`, identidade com o usuário, `candidate.isAlliedTo(controlled)`, veículo compartilhado e candidato que não seja `LivingEntity` (`@788–850`) |
| Ramo Mob | `controlled instanceof Mob @854` chama `Mob.setTarget(candidate) @871` e `setLastHurtByMob(candidate) @878`, depois avalia Astral |
| Ramo Player | A alternativa `@1054–1078` pede `Player.attack(candidate)` e reseta o attack ticker; **não entra no ramo Astral** |

Apesar do texto publisher dizer “mobs”, o candidato exigido pelo ramo é **LivingEntity**, podendo incluir **Player** sujeito aos demais predicados; quem precisa ser **Mob** para Astral é o controlado original.

O bootstrap **0** é distinto: resolve `lambda$onUseTick$0`, que combina `canBeHitByProjectile` com diferença em relação à entidade capturada, para a consulta de visão/movimento fora das janelas atuais. Não substituir o predicado da AABB por esse lambda nem importar a geometria de navegação para a transferência.

## 4. Cadência, comparação e sequência da transferência

Para cada candidato que passou pelos filtros e pelo ramo do **Mob originalmente controlado**, a sequência é:

1. **Cadência:** `elapsed % 4 == 0` (`@881–885`); resto diferente de zero volta ao loop. Isso permite a avaliação em ticks de uso múltiplos de quatro, sem cooldown próprio gravado e sem interpretação de quatro segundos.
2. **Saúde:** lê `candidate.getHealth @890` e `originalMob.getHealth @895`; `fcmpl @898` e `ifle @899 → 1081` exigem **vida atual do candidato estritamente maior** em valores normais finitos. Não compara vida máxima, nível, raridade ou porcentagem de saúde.
3. **Resistência:** `RESISTS_TOTEM_OF_POSSESSION @910`, `Holder.is @913` e `ifne @916` rejeitam o tipo resistente.
4. **Nível:** `ASTRAL_TRANSFERRING @920`, `enchantLevel @923`, `ifle @926` exigem nível positivo na stack.
5. **Marcador e vínculo:** `setPossessed(candidate,true) @932`; obtém cópia/tag nova do item, escreve o UUID do candidato em `BoundEntityUUID @951` e serializa o candidato por `ACPlatform.serializeEntity @956`.
6. **Snapshot do item:** inclui o ID do tipo em `"id" @982`, põe o composto serializado em `BoundEntityTag @992` e comita via `ACCompat.setTag @999`. Solicita `TOTEM_OF_POSSESSION_USE @1002–1014`.
7. **Sincronização condicional:** somente com `Level instanceof ServerLevel` e usuário `instanceof Player` chama `updateEntityIdFromServer @1048`.

A tag publisher de resistência tem 287 bytes, SHA-256 `6ae5d98cd4b12739d3d1d7dc78d37053b2e5b0eb3b1093e3f8a9a6d9768df209`, e lista `#c:bosses`, `minecraft:warden`, `minecraft:armor_stand`, `alexscaves:hullbreaker`, `alexscaves:forsaken`, `alexscaves:atlatitan` e `alexscaves:tremorzilla`. O conjunto resolvido, especialmente `#c:bosses`, depende do pack; a lista não é exaustiva de todos os alvos resistentes efetivos.

**A iteração continua:** `goto @1081 → 766` retoma `hasNext`. Não existe comparação de distância para escolher o mais próximo nem `break` depois de uma troca. As gravações no UUID **não reatribuem a local 5**: candidatos posteriores no mesmo tick continuam sendo comparados ao **Mob original**, inclusive sua vida e relações. Múltiplas sobrescritas do vínculo são possíveis nesse fluxo compilado; múltiplas transferências efetivamente aceitas no pack **não foram testadas**.

O intervalo `@929–1051` tem uma única chamada a `setPossessed`, com argumento `true`. Ele **não limpa ali o marcador do controlado anterior**. Os caminhos de limpeza em `use` e no início de `onUseTick` não demonstram a transação `unset(old) → set(new)` dentro de Astral. Isso delimita o código local; não demonstra ausência de limpeza externa, nem um bug reproduzido.

Na aquisição inicial, `acHurtEnemy` verifica resistência e a configuração de Player (`@7–38`). O construtor de `ACServerConfig` define `totem_of_possession_works_on_players` com padrão **true** (`@675–686`); configuração ativa continua `NOT_VERIFIED`. A continuação geral reavalia essa configuração para Player controlado, mas o ramo de candidato Astral **não repete um teste independente dela antes de escrever o novo vínculo**. Esse gate posterior não é autorização transacional de transferência para Player.

## 5. Custo do equipamento e fronteiras de dados/rede

O construtor completo declara **durabilidade 1.000**, raridade **UNCOMMON** e modificadores de equipamento **+2 de attack damage** e **−2.4000000953674316 de attack speed**. `acModifiers` fornece a tabela no `MAINHAND`; o despacho de atributos chama o helper de compatibilidade. Esses valores são defaults de equipamento, sem dano mágico próprio de Astral. O item declara `getEnchantmentValue=1` e `isEnchantable(stack)` quando `stack.count==1`.

**Desgaste nativo observado:** `onUseTick @230–272` incrementa o damage da stack em **1** quando **`timeLeft % 2 == 0` e `Level.isClientSide == true`**. Um usuário `Player` criativo pula esse incremento; outros usuários seguem a condição de lado/tempo. A instrução é **cliente**, não uma cobrança de durabilidade no servidor demonstrada por esta prova, e não conta transferências Astral. O ramo de transferência não contém débito próprio de mana, munição, durabilidade, cooldown ou chamada direta a `hurt`. Custos de mesa, bigorna e receita não são recurso por cast.

`releaseUsing` completo resolve a entidade atual, remove seu glowing quando não nula, envia mensagem cliente→servidor no cliente e chama **`shrink(1)` quando damage ≥ maxDamage**. Esse corpo não chama `resetBound` nem `setPossessed(false)`; soltar o item não comprova remoção do vínculo ou do marcador. Quebra real, Unbreaking, concorrência e settlement aceito de desgaste exigem QA de cliente/servidor.

| Estado / helper completo | Semântica e limite |
|---|---|
| `ACCompat.getTag` / `getOrCreateTag` | Leem `DataComponents.CUSTOM_DATA` e devolvem **cópia** por `CustomData.copyTag`, ou null/novo composto. Alterar a cópia não comita a stack |
| `ACCompat.setTag` | Grava `CustomData.of(tag)` no componente; argumento null remove `CUSTOM_DATA` |
| `setPossessed(Entity,boolean)` — 16 instruções | Obtém `Entity.getPersistentData` pelo helper; true grava `TotemPossessed=true`, false remove a chave; entidade null retorna. Não percorre donos anteriores |
| `resetBound(ItemStack)` — 16 | Remove **do item** `BoundEntityTag`, `BoundEntityUUID`, `ControllingEntityID` e comita; não limpa por si o marcador persistente de outra entidade |
| `ACPlatform.serializeEntity` — 5 | Delega a `Entity.serializeNBT(entity.registryAccess())`; o retorno é snapshot, não spawn, remoção ou save em disco confirmado |
| `getControlledEntity` — 44 | Cliente resolve o **ID numérico** `ControllingEntityID` por `Level.getEntity(int)`; servidor resolve `BoundEntityUUID` no **ServerLevel atual**. Ausência/sentinela `−1` pode retornar null |
| `updateEntityIdFromServer` — 49 | Resolve o UUID, grava ID ou **−1**, comita e envia `UpdateItemTagMessage` para todos **somente quando ID antigo e novo diferem**. Não envia apenas porque o snapshot/UUID mudou |
| `appendHoverText` — 37 | Lê `BoundEntityTag`, resolve o tipo e acrescenta sua descrição em cinza quando disponível; não demonstra entidade viva ou vínculo resolvido |

`UpdateItemTagMessage` sela construtor, leitura, escrita e handler completos. Transporta um ID de entidade e uma ItemStack; os codecs da stack são delegados a `PacketBufferUtils`, fora deste contrato. O handler usa o sender ou, no cliente, o Player local para obter o nível; resolve ali a entidade pelo **ID fornecido**, exige `LivingEntity` e procura uma stack do **mesmo tipo de item** nas mãos. **Mainhand tem prioridade sobre offhand**. Se o item implementa `UpdatesStackTags` e a tag recebida não é null, chama `updateTagFromServer`.

O Totem herda a implementação default completa de quatro instruções de `UpdatesStackTags`, que delega a `ACCompat.setTag`. O handler inspecionado não contém teste explícito **`entityId == sender.id`**, nem identidade da mesma stack além do tipo de item. Essa é uma observação local do método; não certifica vulnerabilidade explorável, registro/direção da rede, autenticação global, destinatário, ordem, replay, proteção ou cobrança aceita pelo servidor. Mensagem enviada, tag escrita e UUID resolvido não são recibo de ação ou crédito de combate.

## 6. Consumidores do marcador e contexto de targeting

`alexscaves.mixins.json` lista `IllagerMixin` e `LivingEntityMixin`; os classfiles e anotações relevantes estão selados. Eles leem **`TotemPossessed`**, sem ler diretamente o encantamento:

- `IllagerMixin.ac_isAlliedTo` completo, **14 instruções**, injeta em **HEAD** de `isAlliedTo(Entity)Z`, `cancellable=true`. Define retorno false se o próprio Illager ou o outro não nulo estiver possuído. Seu `isPossessed` completo tem cinco instruções e lê o marcador persistente.
- `LivingEntityMixin.ac_onSetLastHurtByMob` completo, **28 instruções**, injeta em **TAIL** de `setLastHurtByMob`. Se o argumento é um **Raider possuído**, o receptor é Raider ou AbstractIllager e também Mob, solicita `Mob.setTarget(argumento)`. Seu helper de cinco instruções lê o mesmo marcador.

Esses consumidores publicados contextualizam as duas direções de aliança e a chamada a `setLastHurtByMob` do loop. Não é suficiente presumir somente a implementação original da engine para explicar a seleção. Aplicação e ordem reais dos mixins, eventos de outros mods, PvP e claims continuam não verificados. As chaves `BoundEntity*` também aparecem em Holocoder/Hologram; ocorrências de `CommonEvents` inspecionadas são condicionadas a **HOLOCODER**, sem expandir o contrato de Astral para esses sistemas.

## 7. Sete eixos e fronteira de integração

| Eixo de perk | Contrato estático individual | Fronteira de integração |
|---|---|---|
| **1. Targeting** | Ramo servidor de Mob controlado, candidato LivingEntity, filtros nas duas direções de aliança, saúde atual estritamente maior, resistência e nível positivo; Player controlado tem ramo de ataque separado | Não escolher alvo por proximidade presumida, importar Player/config como autorização transacional ou ignorar consumidores do marcador |
| **2. Range / área** | AABB do controlado inflada em 3 por eixo; look helper usa ângulo/distância e LOS | Não converter box em raio de dano nem parâmetro de visão/navegação em alcance de transferência |
| **3. Velocidade / direção** | Transferência troca dados de vínculo; não declara vetor, teleporte ou velocidade próprios. Movimento/rampa do Totem estão fora das janelas atuais | Não reexecutar movimento ou ampliar navegação por um suposto multiplicador de Astral |
| **4. Projétil / tamanho** | Não cria projétil ou entidade no ramo de troca; serialização e consulta não são spawn. `canBeHitByProjectile` é um predicado de elegibilidade | Não presumir hit de projétil, quantidade, escala ou nova hitbox |
| **5. Dano / tipo** | Mob recebe target/last-hurt; não há `hurt` ou DamageType próprio no ramo Astral. Player usa `attack` na alternativa sem transferência | Pedido de target/ataque não prova dano aceito; não duplicar dano nem criar tipo mágico/elétrico |
| **6. Duração / recursos** | `elapsed=72000−timeLeft`, `%4==0`; nível positivo sem escala/chance própria. Desgaste cliente par, exceção criativo, shrink ao liberar gasto; custos de enchanting separados | Sem hook seguro para intervalo, custo ou duração; cobrança servidor e quebra efetiva permanecem sem QA física |
| **7. Autoria / proteção / procs** | Item guarda UUID/snapshot/ID; entidade guarda marcador. Original permanece local no tick, loop continua e não limpa marcador anterior nesse trecho | Tags não constituem owner autenticado, permissão, transação ou recibo único de kill/XP/Mastery; sincronização não certifica destinatário/replay |

A possessão, o ataque e seu ciclo de vida pertencem ao provider. O Black Arcana preserva esse processamento nativo; o RPG Skill Tree mantém progressão/Mastery/gates sob contrato real. Setter, tag NBT, método chamável ou descriptor JVM observado **não é API mutadora estável**. Esta conclusão estática não autoriza adapter, transferência/dano reexecutados, proc ou recibo de RPG Mastery. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`.

## 8. Cobertura da prova, histórico e validação

O [manifesto individual atual](../EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json) sela **10 classes, 50 métodos selecionados e 1.045 âncoras**, além dos 13 recursos relevantes: metadados TOML, as duas locales, definições Astral/Detonating, tags de item/resistência, receita, quatro tags de aquisição e configuração de mixins. Separa hashes de classfile, digests de parse, censo de leitores, varredura das 51 definições e a cobertura de instruções selecionadas.

| Corpo / janela | Cobertura atual declarada |
|---|---|
| `onUseTick` | **254/478 instruções — PARTIAL**: `@0–39` (19), `@106–284` (83), `@651–655` (3), `@714–1084` (149) |
| Omissões de `onUseTick` | **224 instruções omitidas**: `@41–103` Detonating Death; `@286–648` rampa/navegação/movimento; `@658–711` partículas. A fronteira de seleção `@39` / `@106` omite inclusive `ifnull @41 → 106`; não é uma sequência linear selada |
| Outros 21 métodos do Totem | **Corpos completos**, total **502 instruções**; incluem construtor, encantabilidade, use/release, animação/duração, atributos e lambda, tooltip, vínculo/resolução/sync, look helper, aquisição, marcador e predicado lambda |
| Helpers e consumidores selecionados | Corpos completos de cópia/escrita/leitura de dados, leitor de encantamento, serialização, mensagem/default interface e consumidores/helpers de marcador; completude desses corpos não significa classe inteira auditada |
| Inicializadores compartilhados e config | Janelas **PARTIAL** de `ACEnchantmentRegistry.<clinit> @347–353`, `ACItemRegistry.<clinit> @2310–2324` e construtor `ACServerConfig @668–686`; `key` e supplier selecionado completos, bindings de bootstrap selados |

São **quatro corpos com seleção PARTIAL**, incluindo `onUseTick`. A cobertura fecha os caminhos e helpers necessários ao **contrato estático individual de Astral**, com fronteiras explícitas para os ramos omitidos. Não se declara `onUseTick` integralmente coberto, CFG executado, engine-base reauditada ou provider integral certificado. As 59 branches e o roster anterior auxiliam o cruzamento de destinos; não promovem 254 âncoras a 478 instruções observadas no selo atual.

A [prova histórica inicial](../EXACT-ASTRAL-TRANSFERRING-1.0.10.json) e a [prova histórica de lifecycle](../EXACT-ASTRAL-TRANSFERRING-LIFECYCLE-1.0.10.json), com suas [sonda inicial](../../../../../docs/qa/alexscaves_1010_astral_transfer_probe.py) e [sonda de lifecycle](../../../../../docs/qa/alexscaves_1010_astral_lifecycle_probe.py), conservam seus limites **PARTIAL**, hashes e bytes. O roster de 22/22 métodos e as 69 âncoras daquela etapa eram insuficientes para o contrato atual; não equivalem à prova consolidada. O estado parcial histórico não é o estado atual desta ficha.

A regressão atual exige o publisher SHA-exato e protege guardas, elapsed/módulo/saúde, continuidade do loop e local original, lado do desgaste, dados copiados, ID/UUID, mensagem, mixins e limites de integração. Testes estáticos e mutações negativas verificam o contrato documental; não executam Minecraft nem homologam hooks.

QA física continua **NOT_TESTED**: níveis 0/I/forçados, datapacks/config reais, cliente e servidor dedicado, desgaste aceito, Player/PvP/claims, visão/LOS/Sightless, alianças/ordem dos mixins, múltiplos candidatos e local original, limpeza do marcador anterior, totems duplicados, sender/destinatário/replay, unload/reload/morte/dimensões, resolução de UUID/ID, dano aceito e crédito único de kill/XP/Mastery. Esses limites de runtime não são lacunas ocultas de identidade ou do ramo estático fechado.

**Conclusão delimitada:** uma ficha individual concluída em `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, **+0 raízes mágicas** e **+0 providers integrais concluídos**. O provider e os contratos de Stage/equipamento permanecem abertos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. O próximo encantamento parcial alfabético é `alexscaves:bonking`.
