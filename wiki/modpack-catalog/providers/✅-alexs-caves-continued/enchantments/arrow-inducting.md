# Arrow Inducting — encantamento do Resistor Shield (1.0.10)

**Estado:** ⚠️ catalogação técnica **parcial/condicionada**; identidade, JSON publisher e consumidor JVM selecionado conferidos. **Não certificado integralmente para perks.** Sem reprodução física de combate: `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `NO_MUTATION`; `NOT_CERTIFIED`.

## 1. Identidade reproduzível

- **Provider / ID:** Alex's Caves Continued / `alexscaves:arrow_inducting`.
- **Tipo:** encantamento passivo reativo em escudo; **não** é nova raiz de cast, magia ou projétil independente do inventário semântico.
- **Versão:** Minecraft 1.21.1 / NeoForge / JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`.
- **JAR:** 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/arrow_inducting.json`; SHA-256 `80d52e42318ad732b32ba6118dea8f5b315b8d2d702da32d202ff95246a973e5`.
- **Prova delimitada:** [manifesto exato e selado](../EXACT-ARROW-INDUCTING-1.0.10.json); [sonda read-only](../../../../../docs/qa/alexscaves_1010_arrow_inducting_probe.py); [workflow](../../../../../.github/workflows/alexscaves-1010-arrow-inducting.yml).
- **Fonte adjacente:** [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1**, logo **não** determina os valores nem a implementação da release 1.0.10. Os parâmetros abaixo vêm do JAR auditado.

A descrição literal para jogador não foi validada em arquivo de idioma da release exata. O resumo comportamental adiante é interpretação das chamadas estáticas selecionadas, sem reproduzir a redação do provider.

## 2. Dados reais do encantamento (JSON 1.0.10)

| Campo | Valor publicado | Limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.arrow_inducting` | Chave de tradução, não descrição textual do jogador |
| `supported_items` | `#alexscaves:enchantable/resistor_shield` | Conteúdo efetivo da tag e alterações por datapack não observados |
| `weight` | `2` | Peso de configuração de encantamento; não chance observada |
| `max_level` | `1` | Limite declarado no recurso publisher |
| `min_cost` | `base=1`, `per_level_above_first=18` | Valores do recurso, sem assumir mecânica externa de aquisição |
| `max_cost` | `base=41`, `per_level_above_first=10` | Idem |
| `anvil_cost` | `4` | Valor do JSON, não consumo de mana nem durabilidade |
| `slots` | `mainhand`, `offhand` | Referência de slot do encantamento; equipagem efetiva depende do jogo/pack |

A auditoria **não** conferiu tiers de loot, disponibilidade em Survival, relações de exclusividade vindas de outros tags, nem restrições reais dos datapacks carregados.

## 3. Ingresso e condições de aplicação — consumidor compilado

**Owner:** `com/github/alexmodguy/alexscaves/server/event/CommonEvents.class`, SHA-256 `d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43`.

**Método selecionado:** `acLivingAttack(Lnet/neoforged/neoforge/event/entity/living/LivingIncomingDamageEvent;)Z`, digest do parse `3b6a9d9699a101ff2c4aa61dc08308857a1480fdd11f711c5ce04e2638244368`, **91 instruções**.

Na região compilada observada, o fluxo consulta o `DamageSource.getDirectEntity`, o `LivingEntity.isBlocking`, o `LivingEntity.getUseItem` e a igualdade do item com `ACItemRegistry.RESISTOR_SHIELD`. Em seguida:

1. Lê `ACEnchantmentRegistry.ARROW_INDUCTING @63` e chama `ACCompat.enchantLevel @66`. O ramo `ifle @69 → 158` desvia se o nível não for positivo.
2. Compara o tipo do projétil com `ACEntityRegistry.SEEKING_ARROW @76`. O ramo `if_acmpeq @84 → 158` evita converter a própria flecha buscadora nessa região.
3. Instancia `SeekingArrowEntity @87–102`, passando a entidade defensora como argumento ao construtor `(Level,LivingEntity)`; copia a posição da flecha original em `@110`.
4. Lê a velocidade original, aplica `Vec3.scale(-0.4D) @119–125`; lê `YRot` e acrescenta `180F @131–138`.
5. Chama `Level.addFreshEntity @150`, **descarta o booleano de retorno em `@153`** e chama `AbstractArrow.discard @155`. Não há, nesse segmento, confirmação de sucesso do novo spawn antes do descarte do projétil anterior.

**Limites do fluxo:** a sonda reconhece janelas JVM selecionadas e símbolos, não reconstitui todas as arestas do grafo de controle ou os handlers terceiros do evento. Não afirmar cancelamento de dano ao defensor, autenticação do evento, sucesso do spawn, reversão de autoria de todos os tipos de flecha, preservação de NBT/enchantments do projétil anterior ou execução apenas no servidor a partir desses offsets.

## 4. Seleção de alvo e movimento posterior

**Owner:** `server/entity/item/SeekingArrowEntity.class`, SHA-256 `1102754436829c3dcadb1450d6ab15efb354a3f4e58a2a262a78c5013d7f0e25`.

**Método:** `tick()V`, digest do parse `eb936d76c3fbdcf1be042312dd7dba664af91244529443c7806aa6a4a2c7e152`, **185 instruções**.

- O trecho `@45–59` compila `min(10, 3 + tickCount / 4)` e `@73` o passa a `AABB.inflate` para busca de entidades (`Level.getEntities @82`). É **expansão da caixa de busca**, não hitbox do projétil, dano em área nem alcance máximo do disparo.
- Existem consultas de `getOwner @41`, `ownedBy @136`, `Entity.isAlliedTo @149` e `Entity.distanceTo @121/@126`. A lista completa de exclusões, a seleção em todos os caminhos e os overrides de terceiros **não** foram certificados.
- A região `getEntity(id) @199`/geometria `@208–237` precede `setDeltaMovement @269`. O trecho compilado `@247–269` aplica escala de aproximadamente `0.3` à velocidade atual e `0.7` à direção normalizada do alvo, somando os vetores sob condições não integralmente reconstituídas.
- `setArcTowardsID @188` indica armazenamento do ID do alvo. Não foi certificado o comportamento de sincronização/serialização após desconexão, save/load ou reatribuição do ID a outro objeto.
- Partículas e outros visuais (`addParticle @391`) não demonstram colisão, dano ou atribuição de kill.

**Não auditados:** dano solicitado/aceito no impacto, intervalo e número de hits, lifetime total, persistência de `stopSeeking`, retenção da autoria, PvP/claims, proteção por chunks, limites de carga, canHitEntity/colisão efetivos e implicações de mixins ModLauncher.

## 5. Eixos de perks e decisões de integração

| Eixo | Evidência estática útil | Limite para alteração |
|---|---|---|
| **Targeting** | Expansão da AABB, consulta de owner/aliados e `setArcTowardsID` | ⛔ **Sem hook seguro confirmado** para mudar filtro/alvo antes da escolha nativa |
| **Range / área** | `min(10,3+tickCount/4)` para busca, não dano em área | ⛔ Não reinterpretar como raio de ataque nem alterar range por perk |
| **Velocidade/direção** | Inversão inicial `-0.4D`; ajuste posterior `0.3/0.7` | ⛔ Sem ponto mutador pré-settlement por jogador validado |
| **Projétil/tamanho** | Nova entidade `SeekingArrowEntity` gerada | ⛔ Escala visual, hitbox e colisão não certificados; sem redimensionamento |
| **Dano/tipo** | Encantamento reage ao evento; dano do novo projétil não auditado | ⛔ Não duplicar `hurt`, alterar `DamageSource` ou inventar dano |
| **Duração/recursos** | Janela condicionada por evento; JSON tem custo de encantamento | ⛔ Sem prova de cooldown, gasto, lifetime ou transação por ativação |
| **Autoria, proteção e procs** | Defensor passado no construtor; consultas de owner/aliados na busca | ⛔ Não atribuir proc/XP/Mastery de volta ao usuário sem cadeia nativa e testes |

Não há autorização para adaptar `LivingIncomingDamageEvent` com interceptação mutadora apenas porque o método foi localizado; verificar fase lógica, precedência de handlers, cancelamento, progressão, identidade e prevenção de duplo processamento. O RPG Skill Tree continua responsável por perks/Mastery, e o Black Arcana não assume o cálculo nativo deste encantamento.

## 6. Auditoria adicional — roster nativo SHA-exato de ciclo de vida (2026-11-10)

A inspeção read-only do JAR físico **1.0.10** ampliou a cobertura de `SeekingArrowEntity.class` de `tick()` para **todos os 12 métodos declarados** (incluindo três construtores), mantendo o consumidor `CommonEvents.acLivingAttack` com digest e offsets já fixados. O [manifesto de roster](../EXACT-ARROW-INDUCTING-LIFECYCLE-ROSTER-1.0.10.json) é gerado das provas publicadas no workflow e verificado novamente pela [sonda de ciclo de vida](../../../../../docs/qa/alexscaves_1010_arrow_inducting_lifecycle_probe.py). A auditoria original continua independente.

| Categoria observada | Membros declarados verificados na classe 1.0.10 | Limite |
|---|---|---|
| Construção e autoria inicial | `SeekingArrowEntity(EntityType,Level)` (5 instruções), `SeekingArrowEntity(Level,double,double,double)` (17) e `SeekingArrowEntity(Level,LivingEntity)` (15) | O construtor usado pelo evento é o terceiro; a chamada herdada a `setOwner` foi verificada no binário de compilação (seção 8), mas o runtime transformado e as regras de crédito continuam pendentes |
| Targeting e movimento | `tick()` (185), `lambda$tick$0(SeekingArrowEntity,Entity)` (4), `getArcTowardsID()` (7), `setArcTowardsID(int)` (7) | O predicado e o setter possuem provas de presença; seleção efetiva, sincronização e retarget completo exigem CFG e testes |
| Rede / estado sincronizado | `defineSynchedData(Builder)` (10), `getAddEntityPacket(ServerEntity)` (4) | Somente membros declarados e fingerprints; conteúdo de pacote, autoridade e save/load reais **não estão certificados** |
| Impacto | `doPostHurtEffects(LivingEntity)` (4), `getDefaultHitGroundSoundEvent()` (4), `getDefaultPickupItem()` (7) | O método pós-hit existe, mas hit aceito, dano/tipo e consequências não foram certificados |

**Ausência delimitada na classe:** nenhum método **declarado** denominado `onHitEntity`, `onHitBlock`, `addAdditionalSaveData` ou `readAdditionalSaveData` consta do roster compilado de 12 membros. Isso **não prova ausência desses comportamentos** no runtime: callbacks de impacto e serialização herdados de `AbstractArrow`, mixins, dados sincronizados e outros consumers continuam fora desta inspeção.

O contrato antigo conserva `Level.addFreshEntity` seguido de descarte da flecha inicial, mesmo sem checagem do retorno do spawn; a prova nova **não** altera essa conclusão. Nenhum método registrado no roster autoriza por si só um hook mutador, uma mudança de dano, um credit de XP/Mastery ou a conclusão da ficha.

**Estado:** ⚠️ `NOT_CERTIFIED` para o contrato individual completo. **Prova da expansão da auditoria:** 1 consumidor de evento + 12 membros declarados de projétil fixados por hashes do JAR; 7 testes sintéticos novos executados na auditoria inicial; sem QA física. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Pendências seguintes: dissecar execução dos construtores e `doPostHurtEffects`; reconstruir CFG de `tick` e predicate; validar persistência, filtros, spoofing e sucesso de dano/spawn.

## 7. Auditoria causal aprofundada — guardas, autoria e estado do projétil (2026-11-10)

**Fonte estática exata:** [manifesto de referências, desvios e constantes do JAR 1.0.10](../EXACT-ARROW-INDUCTING-CAUSAL-FLOW-1.0.10.json), reproduzido pela [sonda read-only](../../../../../docs/qa/alexscaves_1010_arrow_causal_flow_probe.py). O manifesto guarda, para **1 método do evento e os 12 métodos declarados da flecha**, descriptor, digest do método, referências simbólicas com offsets, saltos com destinos JVM e operandos numéricos. Complementa o roster anterior, sem alegar recuperação de toda a CFG, corpos herdados ou resultado físico.

### 7.1. Gates de conversão no evento

Em `CommonEvents.acLivingAttack(LivingIncomingDamageEvent)Z`, **cinco guardas convergem para o offset `@158`**: `ifeq @12`, `ifeq @27`, `ifeq @51`, `ifle @69` e `if_acmpeq @84`. As chamadas adjacentes atestam a origem `DamageSource.getDirectEntity @4`, o teste `LivingEntity.isBlocking @24`, o item efetivamente usado `getUseItem @34/@58`, o nível do encantamento via `ACCompat.enchantLevel @66` e a exclusão do tipo nativo `SEEKING_ARROW @76–84`. Os desvios **não** autorizam declarar o resultado final do evento de dano, o cancelamento efetivo do hit, o comportamento de outros handlers ou o lado lógico do evento como um todo.

Na região de substituição, a classe instancia `SeekingArrowEntity(Level,LivingEntity)` a partir do **defensor** (`@92–102`), reaproveita posição `@110`, aplica fator `-0.4D` à velocidade `@119–125`, soma `180F` à rotação `@134–138`, chama `addFreshEntity @150` e descarta o projétil original `@155`. O booleano do spawn segue descartado em `@153`; trata-se de risco de substituição **sem confirmação de criação**, não prova de que todo spawn falhe ou de que o dano tenha sido negado.

### 7.2. Autoria: sequência de construtores

O construtor exato `SeekingArrowEntity(Level,LivingEntity)` possui **15 instruções** e delega em `@33` a `AbstractArrow.<init>(EntityType,LivingEntity,Level,ItemStack,ItemStack)`, passando `ACEntityRegistry.SEEKING_ARROW` e `ACItemRegistry.SEEKING_ARROW` como referências do objeto nativo. A chamada do evento fornece o defensor como `LivingEntity`. **Conclusão delimitada:** a autoria inicial é encaminhada pela rota do construtor de `AbstractArrow` com uma entidade viva, e o setter interno foi agora identificado em `Projectile` no **binário de compilação**, incluindo `ownerUUID` e `cachedOwner` (seção 8); a persistência efetiva no runtime transformado, o crédito de kill/XP/Mastery e a QA física **não foram auditados**.

O overload `SeekingArrowEntity(Level,DDD)` (17 instruções) delega a `AbstractArrow.<init>(EntityType,DDD,Level,ItemStack,ItemStack)` em `@37`, **sem parâmetro LivingEntity** nessa assinatura. Não presumir equivalência automática de owner entre construtores nem atribuir proc de perk com base apenas em `getOwner`.

### 7.3. Targeting, sincronização e fim da busca

- `defineSynchedData(Builder)` (10 instruções) chama a implementação herdada em `@2` e registra `ARC_TOWARDS_ENTITY_ID` por `Builder.define @13`, com **sentinela inteira `-1` em `@9`**. `getArcTowardsID()` usa `SynchedEntityData.get @7`; `setArcTowardsID(int)` usa `SynchedEntityData.set @11`. Isto comprova **dado de entidade sincronizado**, **não** persistência em NBT ou estabilidade do ID entre mundos/restarts.
- `tick()` testa `inGround @10` com desvio `@13 → 272` e `stopSeeking @17` com `@20 → 272`. O teste `Level.isClientSide @32` precede `@35 → 272`, delimitando o caminho de seleção observado; há outro `isClientSide @276`, ligado a segmento posterior da rotina. Não inferir que toda a entidade só executa no servidor.
- `doPostHurtEffects(LivingEntity)` (4 instruções) grava **`stopSeeking=true`** por `iconst_1 @1` / `putfield @2`. O ramo do `tick @20` permite relacionar esse flag ao desvio da etapa de busca **quando o callback pós-hit é efetivamente chamado**. O método declarado **não contém chamada própria de `hurt`**, efeito de status nem fórmula de dano. O impacto e dano herdados de `AbstractArrow` permanecem **não certificados**.
- `tick @82` consulta candidatos por `Level.getEntities`; `ownedBy @136` e `Entity.isAlliedTo @149` são chamadas compiladas no recorte; `setArcTowardsID @188` registra um ID, e `Level.getEntity(int) @199` resolve a referência durante o seguimento. Sua duração válida, filtros de entidades injetados, colisão e reatribuição do ID após reload ainda exigem análise causal completa.
- Na perseguição, `setDeltaMovement @269` recebe a combinação vetorial com as constantes `0.3000000119D` e `0.6999999881D` (offsets `@250/@260`), conforme as chamadas adjacentes do método. Essa interpolação **não representa** dano, radius de AoE ou multiplicador de tamanho. O recorte inclui `5.0F @177`, `0.65F @212` e `0.5F @315/@328/@341`, mas **não** os promove a parâmetros de perk sem associação integral de operandos e caminhos.

### 7.4. Elementos auxiliares e limites

`getDefaultPickupItem()` referencia `ACItemRegistry.SEEKING_ARROW @4`, e `getDefaultHitGroundSoundEvent()` referencia `ACSoundRegistry.SEEKING_ARROW_HIT @0`. São recursos nativos associados a pickup/som, **não comprovação** de drop, hit/dano aceito ou recuperação física da flecha. A classe continua sem overrides **declarados** de `onHitEntity`, `onHitBlock`, `addAdditionalSaveData` ou `readAdditionalSaveData`; não excluir callbacks herdados, componentes base ou transformações por mixin.

**Fronteira de perks:** não alterar alvo, owner, `ARC_TOWARDS_ENTITY_ID`, `stopSeeking`, velocidade, lifetime, colisão, impacto ou Mastery por simples manipulação do campo. Exigir hook estável pré-efeito, autorização do servidor, prevenção de dupla atribuição, prova de persistência e QA física. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. **A nova evidência aprofunda a ficha ⚠️ parcial; não incrementa contratos estáticos certificados, providers nem raízes de cast.**

## 8. Contrato de herança — `AbstractArrow` / `Projectile` no artefato de compilação (2026-11-10)

**Escopo e autoridade:** [manifesto de bytecode herdado](../EXACT-ARROW-INDUCTING-INHERITED-ENGINE-1.0.10.json) e [sonda de proveniência](../../../../../docs/qa/alexscaves_1010_arrow_inherited_engine_probe.py), executados na CI sobre o **classpath efetivo de compilação** de Minecraft `1.21.1`, NeoForge `21.1.248` e ModDevGradle `2.0.144`, em paralelo à validação SHA-exata do JAR publisher Alex's Caves Continued `1.0.10`. O arquivo do motor escolhido possui SHA-256 `fd58bb47e9ebbeefaa42871888e113b0bd1e643babc6877a237b6c8713a7a1c4`, tamanho `22.702.897` bytes. Os classfiles mapeados têm hashes `AbstractArrow=2cc85f8cb1bacba5c59c462c636f7bfad754db859253b75900a55f9888acccef` e `Projectile=42e5b3a088bd4446abab0fe8cd2e61368095fe664aa38d6b256ab0424625326d`.

**Diferenciação obrigatória:** o cache de desenvolvimento também contém variantes `rename`, `binaryPatch`, `copyUnpatchedClasses`, `binaryWithNeoForge` e `applyDevTransforms` com **hashes de classe diferentes**. A prova seleciona o JAR presente no classpath do compilador, não a primeira entrada do cache. Esta é evidência do **binário de desenvolvimento compilável**, **não** prova do código final transformado por ModLauncher/mixins na instalação física com todos os mods ativos.

### 8.1. Caminho de impacto e solicitação de dano

| Fronteira compilada | Evidência JVM na build fixada | Conclusão e limite |
|---|---|---|
| `Projectile.onHit(HitResult)` | 69 instruções; chamadas virtuais `onHitEntity @72` e `onHitBlock @111` | Existe encaminhamento por categoria do hit, com ramos de deflexão; não demonstra que um hit determinado foi aceito |
| `AbstractArrow.onHitEntity(EntityHitResult)` | 323 instruções; `DamageSources.arrow @47`, `EnchantmentHelper.modifyDamage @92`, `Entity.hurt @298`, ramo `ifeq @301 → 609` | Há solicitação de dano por fonte de flecha e processamento de retorno; a quantidade efetiva não pode ser reduzida ao `baseDamage` e depende do pipeline do jogo |
| Callback pós-impacto | `AbstractArrow.onHitEntity` invoca virtualmente `doPostHurtEffects(LivingEntity) @397`; o override em `SeekingArrowEntity` fixa `stopSeeking=true` | A chamada está num trecho que segue a checagem de retorno `@301`, com outros guardas entre os pontos; não afirmar execução incondicional em todo hit |
| Dano inicial do tipo base | `AbstractArrow(EntityType,Level)`: `baseDamage=2.0D @14–17`; `setBaseDamage(D)` e `getBaseDamage()` declarados | Valor inicial do **tipo base** no binário de compilação, não valor final, fixo ou aceito de cada Seeking Arrow; velocidade, encantamentos e engine ainda alteram o envelope |

Os hashes individuais dos métodos (e seus descriptors, branch targets e referências simbólicas) estão selados no manifesto, sem reprodução de implementação proprietária.

### 8.2. Autoria do defensor e resolução após carregamento

A cadeia agora é comprovada **no binário de compilação**: o evento `CommonEvents.acLivingAttack` passa o defensor para `SeekingArrowEntity(Level,LivingEntity)`; o construtor do provider delega a `AbstractArrow(EntityType,LivingEntity,Level,ItemStack,ItemStack)`; este chama `setOwner(Entity) @28`. O setter em `Projectile` grava `ownerUUID @9` e `cachedOwner @14`. `Projectile.getOwner()` consulta `ownerUUID` e a entidade de `ServerLevel.getEntity(UUID) @52` para repor o cache quando aplicável.

O armazenamento base usa `Projectile.addAdditionalSaveData` e `readAdditionalSaveData`, com os nomes NBT publisher-independent `Owner`, `LeftOwner` e `HasBeenShot`. `AbstractArrow` delega essas operações e acrescenta campos como `life`, `inGround`, `damage`, `pickup`, `crit`, `PierceLevel`, `item` e `weapon` (conforme constantes e referências dos métodos compilados). Isso comprova **uma rota de persistência herdada do owner** na base, não que toda resolução sobreviva a unload, cross-dimension, ausência do owner ou conflito com mixins.

Os estados próprios do provider `stopSeeking` e `ARC_TOWARDS_ENTITY_ID` **não possuem overrides de leitura/escrita NBT declarados** em `SeekingArrowEntity` na versão auditada. Não presumir salvamento de `stopSeeking` ou ID de alvo a partir de `SynchedEntityData`; também não inferir perda efetiva/reprodução física sem testar save/restart e transformações adicionais.

### 8.3. Consequências para targeting, perks e Mastery

`AbstractArrow.canHitEntity` delega a `Projectile.canHitEntity` com filtros próprios; `Projectile.onHit` contém ramos envolvendo deflexão e encaminhamento `EntityHitResult`/ `BlockHitResult`. Isso reforça que **mudar a busca do `tick` não é igual a modificar a elegibilidade de colisão**, e que converter o projétil pode alterar owner e credit de combate nativos.

Para qualquer perk candidata, requerer: prova do hit realmente aplicado, owner válido no servidor no momento da liquidação, prevenção de dano duplicado, respeito a proteção/PvP/claims e comportamento após save/reload. Nenhuma chamada virtual ou campo deste manifesto equivale a um **hook mutador estável**. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, `perk_certification=NOT_CERTIFIED`.

**Status desta etapa:** ⚠️ auditoria da herança **ampliada e verificável no binário de compilação**, mas contrato estático integral do encantamento continua parcial. Permanecem pendentes transformação efetiva ModLauncher/pack, cálculo final e aceitação de dano, variantes de colisão e deflexão, serialização dos campos específicos, datapacks/atributos e QA física. **+0** certificados estáticos, **+0** novas raízes de cast e **+0** providers concluídos.

## 9. Validação, pendências e conclusão desta etapa

- ✅ **Verificado:** SHA-exato do JAR publisher, JSON de identidade e configuração, dois classfiles, descriptors, hashes de métodos e chamadas/operandos delimitados; sonda read-only.
- ✅ **Reproduzível pela CI:** `docs/qa/alexscaves_1010_arrow_inducting_probe.py --jar <JAR exato> --javap <JDK21/javap> --seal <manifesto>`; o gate compara integralmente o manifesto ao resultado observado.
- ⚠️ **Pendente:** CFG/guardas completos, comportamento de impacto/dano, salvamento do alvo, autorização de servidor, datapacks, mods concorrentes e potencial de hook.
- ⛔ **Bloqueadas:** perks mutadoras de alcance, tipo de alvo, dano, tamanho, cooldown, velocidade e afins sem API/contrato e QA adequados.
- ⚠️ **QA física:** `NOT_TESTED`. CI de bytecode não é sessão de jogo.
- **Contabilidade:** uma nova ficha técnica parcial do encantamento; **+0 contratos estáticos certificados, +0 raízes mágicas e +0 providers concluídos**. A cobertura global por ficheiros detectados pode aumentar seu denominador, sem presumir que os demais 50 encantamentos estejam fora do trabalho.

**Próximo item alfabético:** `alexscaves:astral_transferring` (referências nominais existentes; ficha individual ainda não auditada). A fila global permanece em Alex's Caves Continued.
