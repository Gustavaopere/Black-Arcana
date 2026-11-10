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
| Construção e autoria inicial | `SeekingArrowEntity(EntityType,Level)` (5 instruções), `SeekingArrowEntity(Level,double,double,double)` (17) e `SeekingArrowEntity(Level,LivingEntity)` (15) | O construtor usado pelo evento é o terceiro; **transferência/atribuição final de owner deve ser auditada no corpo/engine** |
| Targeting e movimento | `tick()` (185), `lambda$tick$0(SeekingArrowEntity,Entity)` (4), `getArcTowardsID()` (7), `setArcTowardsID(int)` (7) | O predicado e o setter possuem provas de presença; seleção efetiva, sincronização e retarget completo exigem CFG e testes |
| Rede / estado sincronizado | `defineSynchedData(Builder)` (10), `getAddEntityPacket(ServerEntity)` (4) | Somente membros declarados e fingerprints; conteúdo de pacote, autoridade e save/load reais **não estão certificados** |
| Impacto | `doPostHurtEffects(LivingEntity)` (4), `getDefaultHitGroundSoundEvent()` (4), `getDefaultPickupItem()` (7) | O método pós-hit existe, mas hit aceito, dano/tipo e consequências não foram certificados |

**Ausência delimitada na classe:** nenhum método **declarado** denominado `onHitEntity`, `onHitBlock`, `addAdditionalSaveData` ou `readAdditionalSaveData` consta do roster compilado de 12 membros. Isso **não prova ausência desses comportamentos** no runtime: callbacks de impacto e serialização herdados de `AbstractArrow`, mixins, dados sincronizados e outros consumers continuam fora desta inspeção.

O contrato antigo conserva `Level.addFreshEntity` seguido de descarte da flecha inicial, mesmo sem checagem do retorno do spawn; a prova nova **não** altera essa conclusão. Nenhum método registrado no roster autoriza por si só um hook mutador, uma mudança de dano, um credit de XP/Mastery ou a conclusão da ficha.

**Estado:** ⚠️ `NOT_CERTIFIED` para o contrato individual completo. **Prova da expansão da auditoria:** 1 consumidor de evento + 12 membros declarados de projétil fixados por hashes do JAR; 7 testes sintéticos novos executados na auditoria inicial; sem QA física. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Pendências seguintes: dissecar execução dos construtores e `doPostHurtEffects`; reconstruir CFG de `tick` e predicate; validar persistência, filtros, spoofing e sucesso de dano/spawn.

## 7. Validação, pendências e conclusão desta etapa

- ✅ **Verificado:** SHA-exato do JAR publisher, JSON de identidade e configuração, dois classfiles, descriptors, hashes de métodos e chamadas/operandos delimitados; sonda read-only.
- ✅ **Reproduzível pela CI:** `docs/qa/alexscaves_1010_arrow_inducting_probe.py --jar <JAR exato> --javap <JDK21/javap> --seal <manifesto>`; o gate compara integralmente o manifesto ao resultado observado.
- ⚠️ **Pendente:** CFG/guardas completos, comportamento de impacto/dano, salvamento do alvo, autorização de servidor, datapacks, mods concorrentes e potencial de hook.
- ⛔ **Bloqueadas:** perks mutadoras de alcance, tipo de alvo, dano, tamanho, cooldown, velocidade e afins sem API/contrato e QA adequados.
- ⚠️ **QA física:** `NOT_TESTED`. CI de bytecode não é sessão de jogo.
- **Contabilidade:** uma nova ficha técnica parcial do encantamento; **+0 contratos estáticos certificados, +0 raízes mágicas e +0 providers concluídos**. A cobertura global por ficheiros detectados pode aumentar seu denominador, sem presumir que os demais 50 encantamentos estejam fora do trabalho.

**Próximo item alfabético:** `alexscaves:astral_transferring` (referências nominais existentes; ficha individual ainda não auditada). A fila global permanece em Alex's Caves Continued.
