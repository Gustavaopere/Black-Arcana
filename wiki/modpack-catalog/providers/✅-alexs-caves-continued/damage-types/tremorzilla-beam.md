# Tremorzilla Beam — tipo de dano `alexscaves:tremorzilla_beam` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED + SHA_EXACT_SELECTED_BYTECODE_OBSERVED` (recorte parcial, sem certificação). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:tremorzilla_beam`.
- **Caminho ZIP:** `data/alexscaves/damage_type/tremorzilla_beam.json`.
- **SHA-256 do JSON:** `a059d2c010509db8d56f984d6d403a8901d1442d0ba47eff2f009c6998b58e9a`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `tremorzilla_beam` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.3` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- Nenhuma entrada direta para este ID nos seis arquivos `tags/damage_type/*.json` encontrados no artefato.

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.

## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | ⚠️ `DamageSource` usa o Tremorzilla como argumento no ramo do feixe; crédito final e PvP não certificados |
| Fórmula de dano, mitigação, críticos e resistências | ⚠️ chamadas do `tickBreath` passam `20.0f` como argumento de dano ao helper; mitigação e aceitação reais pendentes |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | ⚠️ AABB, `NO_CREATIVE_OR_SPECTATOR`, aliados e `canEntityBeHurtByBeam` observados; geometria efetiva/LOS pendentes |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | ⚠️ seleção `getEntitiesOfClass`, posicionamento `beamServerTarget` e clip observados; não há contrato de projétil mutável |
| Duração, intervalo de hits, custo de ação e cooldown de casting | ⚠️ `tickBreath`/`tickBeamTargeting`, `beamTime` e charge nativos observados; frequência, custos e cooldown pendentes |
| Persistência, ordenação de eventos, server authority e deduplicação | ⚠️ `killCountFromBeam`, flags e `SynchedEntityData` observados; autoridade de servidor, reload e deduplicação pendentes |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeTremorzillaBeamDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `TREMORZILLA_BEAM` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/living/TremorzillaEntity.class` | `public boolean hurtEntitiesAround(net.minecraft.world.phys.Vec3, float, float, float, boolean, boolean, boolean)` | `(Lnet/minecraft/world/phys/Vec3;FFFZZZ)Z` | 76 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Auditoria exata do consumidor e dos emissores — TremorzillaEntity 1.0.10

**Alcance da prova:** `SHA_EXACT_1010_TREMORZILLA_BEAM_SELECTED_JVM_CONSUMER_AND_CALLERS_ONLY`. [Manifesto selado](../EXACT-TREMORZILLA-BEAM-1.0.10.json) · [PR #989](https://github.com/Gustavaopere/Black-Arcana/pull/989) · [workflow da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-tremorzilla-beam.yml). A inspeção recompõe somente um recorte de referências/operandos do bytecode compilado original; não exporta fonte/classe integral nem valida gameplay em cliente/servidor.

- Arquivo JVM: `com/github/alexmodguy/alexscaves/server/entity/living/TremorzillaEntity.class`, SHA-256 `e1ac60a8005f9414dde1d25a92a2110df65cef145c3225e9c2557c96672fe8dc`.
- Universo desta classe compilada: **116 métodos declarados** (não equivale ao inventário total do provider). Manifesto conserva **nove SHA-256 de métodos**, **24 âncoras** de bytecode e os **dez callsites nativos do helper** agrupados em três métodos distintos. Distingue a factory customizada do caminho vanilla.
- O método central é `hurtEntitiesAround(Vec3,float,float,float,boolean,boolean,boolean):boolean`, descriptor `(Lnet/minecraft/world/phys/Vec3;FFFZZZ)Z`, 169 instruções registradas pelo parser e factory exata `causeTremorzillaBeamDamage @76`.

### Seleção de tipo de dano — o helper não é exclusivo do feixe

| Produtor compilado | Chamadas para `hurtEntitiesAround` | Distinção observada |
|---|---|---|
| `tickBreath()` | `@552`, `@578` | Passa a primeira flag booleana `true` e utiliza o ramo `causeTremorzillaBeamDamage` do helper; há um operando `20.0f` na posição de *damage amount*. |
| `tick()` | `@1455`, `@1537`, `@1558`, `@1579`, `@1599`, `@1619`, `@1863` | Emite chamadas por partes do corpo/ataques próprios; os pontos observados incluem primeira flag `false` e operando `10.0f` de dano. **Não atribuir automaticamente tipo `tremorzilla_beam`**. |
| `stompEffect(boolean,float,float,float,float)` | `@357` | Primeira flag `false`, com parâmetros próprios de pisão; não é um disparo do feixe. |

Em `hurtEntitiesAround`, a primeira flag é testada em `@63–65`. O ramo verdadeiro monta `ACDamageTypes.causeTremorzillaBeamDamage(registryAccess, this) @76`; o ramo alternativo constrói `DamageSources.mobAttack(this) @82–87`. O `DamageSource` usa o mob Tremorzilla nesse trecho; não há prova de atribuição final de kill, evento de Mastery ou regra de PvP de terceiros. **Não aplicar uma perk de feixe a toda chamada desse helper.**

### Alvos, geometria, dano e status

- O helper constrói uma `AABB` a partir de `Vec3`, ajusta limites verticais com `AABB.setMinY @42` e `setMaxY @56`, incluindo `3.0d` no cálculo de um limite. **Esse `3.0d` não é alcance máximo do feixe** nem raio circular certificado. O box de busca é distinto da linha de tiro.
- Busca `LivingEntity` por `Level.getEntitiesOfClass @104`, usando `EntitySelector.NO_CREATIVE_OR_SPECTATOR @101`. Na iteração consulta autocorrespondência `LivingEntity.is @139`, aliados `isAlliedTo @148`, igualdade de tipo, distância quadrática `distanceToSqr @193`, predicado `canEntityBeHurtByBeam @213` e tipo `KaijuMob @226`. Os saltos para `@352/355` demonstram condições de descarte de candidatos, mas não homologam cobertura de PvP/claims de outros mods.
- O predicado compilado `canEntityBeHurtByBeam(LivingEntity,Vec3)` recorre a `ClipContext` com `Block.COLLIDER` e `Fluid.NONE` e `Level.clip`. Há uma superfície de oclusão por blocos separada do box de busca; o resultado booleano exato e possíveis exceções dependem do CFG, não de uma lista de símbolos.
- `ACCompat.hurt(target, DamageSource, amount) @237` recebe o segundo parâmetro `float` do helper (`fload_3`). Os dois callsites de `tickBreath` passam `20.0f` nessa posição. **20 é dano solicitado antes de mitigação**, não range, duração, raio, número de ticks ou garantia de dano aceito. `ifeq @240` interrompe o caminho de pós-acerto quando o retorno de `hurt` é falso.
- Depois do retorno verdadeiro há referência a `knockbackTarget @285` e consultas `LivingEntity.getHealth @295`, `Enemy @305`, `killCountFromBeam @313–318`; a existência do incremento condicionado não certifica contagem de abates ou pontuação canônica de Mastery.
- O mesmo caminho contém `ACEffectRegistry.IRRADIATED @327`, construtor de `MobEffectInstance @345` com **duração solicitada de 6.000 ticks e amplifier 2** (`sipush 6000 @341`, `iconst_2 @344`) e `LivingEntity.addEffect @348`. Isso não implica aplicação incondicional ou duração final em alvo imune; a [ficha de Irradiated](../effects/irradiated.md) preserva a semântica nativa do efeito.

### Targeting, energia e efeitos de mundo

- `tickBeamTargeting()` lê `getTarget`, `getControllingPassenger`, `Player.getViewVector` e atualiza `beamServerTarget`; `createInitialBeamVec` e `getBeamShootFrom` constituem outras superfícies de origem/direção. Não usar parâmetros da busca por AABB como distância de tiro do beam nem assumir que controle por passageiro seja autorização de cliente.
- `tickBreath` verifica lado lógico, usa `Level.clip` com `COLLIDER/NONE` e acessa `ACServerConfig.devastatingTremorzillaBeam`. O ramo de destruição de blocos, sua extensão, limite de chunks e a política de permissões **não estão certificados por esta inspeção parcial**; qualquer integração com Black Arcana requer `WorldEffectPolicy` e testes de mundo antes de alterar esse comportamento.
- `getCharge()` lê o campo sincronizado `CHARGE` via `SynchedEntityData`; `getMaxBeamBreakLength()` consulta `MAX_BEAM_BREAK_LENGTH`. As referências a `beamTime`, `maxBeamTime` e `beamServerTarget` são estado do provider, não nova mana, cooldown Black Arcana ou setter seguro automaticamente exposto a perks.

### Controle de fluxo normal SHA-exato — guards e desvio de raycast (PR #1006)

A [auditoria de dominadores do CFG normal compilado](../../../../../docs/qa/alexscaves-1010-tremorzilla-normal-cfg-handoff.md) e o [manifesto 1.0.10](../EXACT-TREMORZILLA-NORMAL-CFG-1.0.10.json) acrescentam uma verificação de **caminhos normais intramétodo**; não inclui arestas de exceção, dispatch, mixins ou gameplay.

- `breakBlocksAround`: `ACPlatform.canEntityGrief @12` e `Level.isClientSide @22` **dominam** os pontos `destroyBlock @249`, `onBlockExploded @268`, `createEntity @296` e `addFreshEntity @349` no CFG normal. **Isso não certifica a semântica do retorno do predicate, claims de terceiros, loaded chunks ou aplicação da `WorldEffectPolicy`.**
- `tickBreath`: `Level.isClientSide @4` domina os sites de mundo `breakBlocksAround @525/@620` e de dano `hurtEntitiesAround @552/@578`. Já `Level.clip @393` **não os domina**: há trajetórias normais de execução que contornam essa chamada específica. Isso **não** prova ausência de LOS, ataque através de paredes nem falha de autorização — outro caminho de `canEntityBeHurtByBeam` usa `Level.clip @37`.
- `canEntityBeHurtByBeam`: seu `Level.clip @37` domina `BlockHitResult.getType @40` no CFG normal. O significado booleano completo dos ramos e permissões permanece pendente.

**Consequência para perks:** não unificar o clip do endpoint, o predicado de LOS por entidade e a política de destruição; o fluxo nativo possui condicionais distintas. Preservar `NO_MUTATION`, `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`. **Nenhuma nova ficha ou certificação.**

### Helpers compilados — NeoForge grief, early return e callbacks do mundo (PR #1007)

A inspeção [SHA-exata do publisher 1.0.10](../../../../../docs/qa/alexscaves-1010-tremorzilla-grief-helper-handoff.md) e seu [manifesto de ABI](../EXACT-TREMORZILLA-GRIEF-HELPERS-1.0.10.json) identificam a implementação da delegação e os **sentidos dos ramos iniciais** de `breakBlocksAround`, além da dominância registrada na PR #1006:

- `isBaby @1` com `ifne 28 @4` retorna `false` em `@28–29`; `ACPlatform.canEntityGrief @12` com `ifeq 28 @15` também retorna `false` quando o evento retorna falso. `Level.isClientSide @22` com `ifeq 30 @25` impede que o trecho destrutivo prossiga no lado cliente. Esses ramos são **JVM 1.0.10**, não demonstração de modpack transformado.
- `ACPlatform.canEntityGrief(Level,Entity)` contém quatro instruções e delega diretamente a `net.neoforged.neoforge.event.EventHooks.canEntityGrief @2`, seguida de `ireturn @5`. **A semântica de `EventHooks` e suas integrações de claims ainda dependem de auditoria do NeoForge 21.1.248 e do modpack real.**
- `ACCompat.onBlockExploded @4` delega a `BlockState.onBlockExploded`, enquanto `ACCompat.createEntity @2` delega a `EntityType.create`. Wrapper compilado não equivale a `WorldEffectPolicy`, autorização de explosão ou spawn seguro.
- `Level.destroyBlock @249`, `ACCompat.onBlockExploded @268`, `ACCompat.createEntity @296` e `Level.addFreshEntity @349` continuam operações distintas e condicionadas; não presumir que ocorram no mesmo tick ou em toda ativação.

**Estado de integração inalterado:** ⚠️ `NOT_CERTIFIED` / `NO_MUTATION` / `mutating_hook=NOT_VERIFIED` / `physical_qa=NOT_TESTED`. Nenhuma promoção de ficha ou perk só por comprovação de delegação.

### Encaminhamento NeoForge 21.1.248 compilado — grief event (PR #1008)

O [relatório de auditoria do NeoForge 21.1.248](../../../../../docs/qa/neoforge-211248-grief-event-handoff.md) e seu [manifesto SHA-exato](../NEOFORGE-211248-GRIEF-EVENT-ABI.json) estendem a delegação da PR #1007 **sem alterar o runtime de Alex's Caves**. O JAR oficial analisado (SHA-256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`) contém a bifurcação `entity == null` para `GameRules.RULE_MOBGRIEFING` e o outro ramo para `NeoForge.EVENT_BUS.post(new EntityMobGriefingEvent(level, entity)).canGrief()`. No evento, `canGrief` é inicializado pela gamerule e pode receber novo booleano por `setCanGrief`.

**Limites:** a API não recebe uma posição de bloco nem um contexto de claim no método auditado. Listener instalado, semântica de proteções territoriais e mutações subsequentes permanecem desconhecidos; o NeoForge 21.1.248 é baseline de build, enquanto o snapshot físico da modlist registra 21.1.250. Não há evidência de permissão de `WorldEffectPolicy`, loaded chunks, atribuição de jogador ou hook mutador autorizado. **`NO_MUTATION`, `NOT_CERTIFIED`, QA física `NOT_TESTED`**; o índice continua 28/30.

### Matriz de integração / pendências

| Perk pretendida | Consumer que exige auditoria adicional | Decisão |
|---|---|---|
| Aumentar dano do feixe | `tickBreath` → `hurtEntitiesAround` com flag do beam → `ACCompat.hurt` | Não alterar o dano de `stompEffect` ou `tick` por engano; prevenir segundo `hurt`/segundo proc. |
| Alterar alvo/alcance/raio | `tickBeamTargeting`, `canEntityBeHurtByBeam`, `Level.clip`, caixa AABB e ponto final do feixe | Sem CFG/QA de colisão e aliados: `NO_MUTATION`. |
| Reduzir charge/cooldown | `getCharge`, setters, `beamTime`, config e persistência nativa | Nenhum contrato seguro de custo/cooldown comprovado. |
| Aumentar tempo/nível de Irradiated | `hurtEntitiesAround` pós-`ACCompat.hurt` e `Irradiated` nativo | Não duplicar efeito, contagem ou eventos de XP; duração da instância não é cooldown. |
| Ampliar destruição | `tickBreath`, `devastatingTremorzillaBeam`, alteração de blocos e mundo | ⛔ Sem aprovação `WorldEffectPolicy` e verificação de claims. |

**Status mantido:** ⚠️ `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. **+0 raízes e +0 fichas certificadas**; não promover `COMPLETE_PERK_READY`, índices, estágios ou integração RPG Skill Tree. Próxima etapa: mapear integralmente o CFG dos guards de raycast, tick/charge, grieffing e persistência, depois validar servidor/client modpack exato.
