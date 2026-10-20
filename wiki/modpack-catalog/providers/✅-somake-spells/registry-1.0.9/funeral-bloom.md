# `somakespells:funeral_bloom`

- Provider: **Somake Spells** (`somakespells`)
- Artifact: `somakespells-1.0.9-1.21.1.jar`
- Physical / publisher SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`
- Substrate: **Iron's Spells 'n Spellbooks**
- Registry identity: `somakespells:funeral_bloom`
- Registration gate: **Unconditional**
- Current composition registration: **ADMITTED**
- State: `EXACT_PHYSICAL_REGISTRY / CURRENT_REGISTRATION_ADMITTED / STRICT_COUNT_CONDITIONAL`

## Registration evidence

The exact physical 1.0.9 `ModSpells` topology registers this identity without an optional-provider registration predicate.

The exact current artifact has 83 unique Somake spell registry IDs, and the present mod composition satisfies all optional registration predicates. This card records one of those **83/83 currently admitted registrations**.

## Host / progression boundary

Exact 1.0.9 structural evidence found no provider `isEnabled()` override among the 83 spell classes. That does **not** substitute for the effective deployed Iron's spell configuration.

Exact structural audit identifies a provider `allowCrafting()` override for this spell with non-constant logic. The resolved survival acquisition state therefore requires provider/runtime evidence rather than inference from the registry ID.

Still unresolved for strict semantic promotion:

- effective Iron's per-spell/global/datapack `enabled`;
- effective Iron's `allow_crafting` where applicable;
- deployed Somake `enableSpellLockSystem` COMMON value;
- object-level or bounded-set survival acquisition/reachability;
- assembled-pack progression/runtime settlement.

## Counting boundary

This is an exact current registry identity, not yet an independently strict-counted semantic action. Registration presence alone does not add this card to the strict numerator while the host/provider config and reachability gates above remain open.

Do not infer display name, school, level, rarity, mana cost, cooldown, damage, duration, targeting, recipe, loot source or formulas from the registry path.

## Authority

Iron's owns host casting/resource/cooldown settlement. Somake owns this spell identity and its provider progression. Black Arcana catalogs and may observe supported provider state; it does not recreate either runtime.

Sources: `../EXACT-1.0.9-REGISTRY-AUDIT.md`, `../EXACT-1.0.9-REGISTRATION-GATE-MAP.md`, `../SPELL-CATALOG-1.0.9.md`.

**Gate deste spell — `NON_CONSTANT`:** a auditoria provou que o override de `allowCrafting()` possui lógica não constante. Predicados, ordem, parâmetros, estados de jogador/progresso, resultado em Survival e possibilidade de interceptação **NÃO VERIFICADOS**. Uma perk de desbloqueio exige primeiro identificar o predicado completo e um contrato de integração real.

## Dossiê técnico para perks — gate de aquisição (18/10/2026)

**Escopo da prova:** presença do ID na registry e classificação do override `allowCrafting()` no JAR físico 1.0.9. Não é prova de execução de cast, atributos, alvo ou integrabilidade em produção. A linha física está fixada pelo SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` (CurseForge File `8867079`). A árvore de código fonte público exato para o release não foi localizada.

| Dimensão para perk | Fato verificável / limite |
|---|---|
| Registrar | `com.somake.somakespells.registries.ModSpells`, ID deste documento no `DeferredRegister<AbstractSpell>` |
| Classe/método de seleção ou efeito | **Classe de aquisição verificada:** `com.somake.somakespells.spells.blood.FuneralBloomSpell#allowCrafting():boolean` (`()Z`). Métodos de cast, dano, targeting e implementação downstream **NÃO VERIFICADOS** |
| Admissão de casting | `isEnabled()` **não é sobrescrito** pela classe no provider; Iron's host, config e datapack efetivos **NÃO VERIFICADOS** |
| Targeting e LOS | Tipo de alvo, distância de aquisição, alcance do efeito e linha de visão **NÃO VERIFICADOS** |
| Geometria | Raio/ângulo/altura da área, hitbox, velocidade/quantidade de projéteis e multiplicidade de alvos **NÃO VERIFICADOS** |
| Dano/cura | Damage source, tipo/elemento, fórmulas, status, buffs/debuffs, knockback e eventuais procs **NÃO VERIFICADOS** |
| Tempo e recursos | Tempo de cast, cooldown, custos, duração/ticks, scaling e caps **NÃO VERIFICADOS** |
| Causalidade | Cast → efeito secundário → acertos/procs e identidade para deduplicação **NÃO VERIFICADOS**; não atribuir Mastery por evento sem correlação |
| Mutabilidade por perk | **⛔ FAIL_CLOSED** para alterar disponibilidade, geometria, dano, custos ou cast: nenhum hook/adapter mutador foi demonstrado nesta ficha |
| Autoridades | Somake: identidade/gate específico; Iron's: host de casting/custos/cooldowns; RPG Skill Tree: progressão por boundary comprovado; Black Arcana: somente runtime mágico próprio e observação permitida |

**Separar fatos:** `allowCrafting()` decide uma superfície de *craftability* e não comprova proibição de cast nem ausência de loot, comando, equipamento, transferência ou qualquer via especial de obtenção. Um possível gate de perk não pode simplesmente reabrir essa rota sem contrato verificável do host/provider. O code default `enableSpellLockSystem=false` não representa a configuração COMMON implantada.

**Testes pendentes:** comparar os métodos de admissão e as classes de efeito do JAR exato com a config/Datapack do perfil real; medir parâmetros com unidades; inspecionar API/eventos do host 3.16.3; validar fallback, aquisição em Survival, mudança de perk/equipamento, servidor/cliente, deduplicação e ausência de dupla cobrança. Nenhum destes testes é declarado PASS nesta atualização.

**Provas imutáveis:** [auditoria 1.0.9](https://github.com/Gustavaopere/Black-Arcana/blob/511ec03f0da62ebfc1722825def50354594976c3/wiki/modpack-catalog/providers/%E2%9C%85-somake-spells/EXACT-1.0.9-REGISTRY-AUDIT.md) e [gate map](https://github.com/Gustavaopere/Black-Arcana/blob/511ec03f0da62ebfc1722825def50354594976c3/wiki/modpack-catalog/providers/%E2%9C%85-somake-spells/EXACT-1.0.9-REGISTRATION-GATE-MAP.md).

## Prova compilada exata de allowCrafting — 18/10/2026

- Classe do publisher SHA-exato: `com.somake.somakespells.spells.blood.FuneralBloomSpell`.
- Método: `public boolean allowCrafting()` / JVM `()Z`.
- Classificação: `NON_CONSTANT`.
- Compilado: **2 branches**, chamada a `ModConfigSpec$BooleanValue.get()` e `Boolean.booleanValue()`, com leitura do campo exato `com.somake.somakespells.config.Config.DISABLE_WITHERED_ROSE_SPELLS_CRAFTING_AND_LOOTING`. Este símbolo é factual; a tabela verdade do predicado, o valor default e o config COMMON efetivo **não foram verificados**.
- Evidência independente: [GitHub Actions #39186593493](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39186593493), Java21, 7/7 testes sintéticos e 7/7 classes auditadas; [matriz consolidada](../EXACT-BINARY-CRAFTING-METHOD-SEAMS-1.0.9.md).
- **Mutabilidade por perk:** ⛔ nenhum hook/callback por jogador comprovado; `allowCrafting` não informa dano, geometria, mana, castability ou loot ativo.

## Cast e efeito — referências compiladas exatas (18/10/2026)

**Fonte física:** Somake 1.0.9 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [Java21 #39192999780](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39192999780), `PASS_STATIC_METHOD_REFERENCES_ONLY`, [matriz de sete classes](../EXACT-BINARY-CAST-CALLSITES-1.0.9.md).

- getCastType references CastType.LONG; onCast references Utils.raycastForEntity and FuneralBloomControllerEntity construction plus Level.addFreshEntity.
- Parameters passed to the controller are computed via getRadius, getDuration, getWaveInterval, getTelegraphTicks, getMaxTargets, getImpactDamage, getWitherDuration and getWitherAmplifier.
- getRadius references SchoolType.getPowerFor; getImpactDamage references getSpellPower; several time/count functions reference Mth.clamp. No literal formulas/caps or hit/loot/healing behavior have been proven from the controller's compiled methods yet.

**Limite de perks:** apenas assinaturas e referências simbólicas do JAR exato foram certificadas para FuneralBloomControllerEntity. Config ativa, fórmula numérica, tipo/alcance de alvo, colisão, duração efetiva, reentrância, dano/cura aplicado e hook mutador por jogador continuam **⚠️/⛔ NÃO HOMOLOGADOS**. Não transferir casting, custos ou efeitos do provider ao RPG Skill Tree; evitar callbacks de dano repetidos.

## Entidade downstream — auditoria JVM exata (19/10/2026)

**Fonte:** JAR Somake 1.0.9 com SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, [auditoria Java 21 #39195233005](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195233005). Classe: `com.somake.somakespells.entity.FuneralBloomControllerEntity`. Evidência `PASS_STATIC_ENTITY_REFERENCE_DISCOVERY` — sem execução do efeito em jogo.

- `FuneralBloomControllerEntity#launchWave(ServerLevel)` consulta candidatos com `AABB.inflate` e `ServerLevel.getEntitiesOfClass`; `isValidTarget` consulta `LivingEntity.isSpectator`, `isAlliedTo` e `distanceToSqr`.
- Há rotinas `pruneTargets`, `cancelOwnedBuds` e `onAntiMagic`. A classe referencia `FuneralBloomBudEntity` em predicados de limpeza, indicando um consumidor downstream adicional que **não** foi auditado aqui.
- `getRadius/setRadius`, `getDuration/setDuration` e `getWaveInterval/setWaveInterval` são métodos internos presentes; não provam setters públicos de perk nem fórmulas/caps. Dano, cura e multiplicidade de buds exigem auditoria da classe bud.

**Boundary de perks:** ⚠️ métodos/refs comprovados, mas fórmulas, caps, ordem de settlement, config efetiva, alvos e multiplayer pendentes; ⛔ `FAIL_CLOSED` para alterações de dano/área/duração/alvo sem API por jogador real. [Matriz das cinco entidades](../EXACT-BINARY-ENTITY-CALLSITES-1.0.9.md).

## Bud secundário — impacto, cura e estado persistente (19/10/2026)

**Evidência exata:** [Java21 #39197671447](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39197671447), SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, **10 testes sintéticos**, `FuneralBloomBudEntity` (26 métodos compilados de interesse). [Dossiê completo](../EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md).

- `tick()` referencia o controlador, `updatePrediction`, `beginRetreat`, `discard` e `impact(ServerLevel)`. `updatePrediction` localiza alvo por UUID, consulta `isAlive` e `getDeltaMovement`, e referencia `groundPosition` do controller; LOS e ajuste preditivo numérico continuam não aferidos.
- `impact(ServerLevel)` referencia AABB, `getEntitiesOfClass`, `isAlive`, `isAlliedTo`, `hasEffect(WITHER)` e `getOwner()`, além de `impactDamage` e `FuneralBloomSpell.getDamageSource`.
- O método de impacto referencia `io.redspace.ironsspellbooks.damage.DamageSources.applyDamage(...)`, `MobEffects.WITHER`/`LivingEntity.addEffect`, `SpellHealEvent`/`NeoForge.EVENT_BUS.post`/`LivingEntity.heal` e `LivingEntity.push`. **São callsites condicionais; não se comprovou a frequência nem os resultados de cada ramo**.
- `readAdditionalSaveData`/`addAdditionalSaveData` incluem UUIDs de controller/alvo, posição de impacto, telegraph/fall/retreat e parâmetros de dano/Wither. Persistência efetiva em restart, segurança contra NBT malformado e deduplicação de Mastery pendentes.
- `impact` constrói `FuneralBloomImpactEntity` e referencia `ServerLevel.addFreshEntity`; a classe downstream agora foi **auditada quanto aos símbolos JVM** ([dossiê](../EXACT-BINARY-FUNERAL-BLOOM-IMPACT-1.0.9.md)), sem homologação de gameplay.

**Integração de perks:** dano, efeito Wither, cura e knockback são eixos separados. A presença de evento de cura não valida mutação de dano nem acesso a todos os branches. **⛔ FAIL_CLOSED** para alteração per-player de alcance, dano, cura, alvo, tempo, número de buds e efeito visual, até API/evento, semântica e QA reais. Nenhuma nova identidade de spell é somada.

## Entidade final de apresentação/impacto — evidência compilada (19/10/2026)

**Fonte:** [Java21 #39198753251](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39198753251), Somake 1.0.9 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, sete testes sintéticos e **oito métodos** da `FuneralBloomImpactEntity`.

- `defineSynchedData`/`getScale`/`setScale(float)` referenciam `DATA_SCALE` e `Mth.clamp`. Não há limite numérico ou integração com hitbox e perk demonstrados.
- `getOpenProgress(float)` referencia `tickCount`, `Mth.clamp` e `smoothstep`; `tick` referencia `Entity.tick`, `Level.isClientSide` e `discard`. Duração/condição efetiva não determinada.
- Métodos de NBT leem/gravam `float` de Scale; round-trip real e cliente não testados.
- **Nenhuma referência direta de dano, cura ou status** foi encontrada nesses oito métodos. É uma observação negativa **apenas do escopo inspecionado**; a entidade pode herdar/delegar outros comportamentos. Dano/Wither/cura seguem com provas de callsites na bud, não se conclui efeito duplicado.

**Perks:** não homologar `setScale` como ajuste por jogador; continua ⛔ `FAIL_CLOSED` para ampliar raio, dano, efeitos, velocidade e tempo sem API/contrato real do provider e QA. [Dossiê técnico completo](../EXACT-BINARY-FUNERAL-BLOOM-IMPACT-1.0.9.md).

## Fórmulas inteiras comprovadas — Funeral Bloom (19/10/2026)

**Fonte primária:** JAR Somake 1.0.9 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, [Java 21 #39201041605](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39201041605) `SUCCESS`, 15 testes, 4 classfiles, 17 métodos. O verificador só declara fórmula completa se todo o fluxo do getter inteiro for linear, coberto e terminar em `ireturn`. [Dossiê de prova](../EXACT-BINARY-FUNERAL-BLOOM-NUMERIC-1.0.9.md).

Para **L = clamp(level_int,1,5)** nos quatro getters de nível limitado; `getTelegraphTicks` utiliza diretamente o nível recebido e divisão inteira Java truncada em direção a zero. As cinco expressões e saídas foram reconstruídas com prova de pilha JVM:

| Getter | Fórmula de retorno | Para L=1 até 5 |
|---|---|---|
| `getMaxTargets(int)` | `4 + L` | `5, 6, 7, 8, 9` |
| `getDuration(int)` | `240 + 20*(L-1)` | `240, 260, 280, 300, 320` |
| `getWaveInterval(int)` | `18 - L` | `17, 16, 15, 14, 13` |
| `getWitherDuration(int)` | `60 + 12*L` | `72, 84, 96, 108, 120` |
| `getTelegraphTicks(int)` | `max(9, 13 - jvm_idiv(level_int,2))` | `13, 12, 12, 11, 11` para level_int=1..5 |

**Limites técnicos:** os retornos são do bytecode estático para um parâmetro inteiro, não garantem unidade de ticks, consumidor executado ou configuração efetiva no servidor. O argumento `level_int` não foi demonstrado como atributo específico de Mastery, Skill Tree ou item.

Clamps com dois operandos literais diretamente anteriores ao callsite: `getRadius(int,LivingEntity)` usa `Mth.clamp(FFF)F` com argumentos **10.0/15.0**; `FuneralBloomImpactEntity.setScale(float)` usa **0.65/1.6**; `getOpenProgress(float)` tem dois clamps **0.0/1.0**. Não interpretar esses argumentos como raio/hitbox efetivos ou suporte a perks.

Fórmula total **ainda não comprovada** de `getRadius` (2 branches, dependência de `SchoolType.getPowerFor`) e `getWitherAmplifier` (2 branches). A expressão do **retorno float** de `getImpactDamage` foi demonstrada na auditoria de fluxo posterior, sem homologação do dano aplicado. `getTelegraphTicks` tem fórmula matemática comprovada, mas sua aplicação como tempo em jogo depende de consumidores do provider. Os métodos `FuneralBloomBudEntity.impact` e `FuneralBloomControllerEntity.launchWave` têm branches relevantes, portanto literals isolados não resolvem dano real, cura, knockback, quantidade de buds ou hitbox.

**Decisão de integração:** ✅ limites algébricos dos cinco retornos catalogados; ⚠️ consumidores do provider e dimensões reais não validados; ⛔ `FAIL_CLOSED` para alteração per-player de level, área, duração, alvo, dano, custo e escala via RPG Skill Tree sem contrato seguro e QA provider-loaded. Nenhuma nova raiz de magia ou adapter foi criada.

## Dano de impacto — prova integral de retorno float (19/10/2026)

**Proveniência:** JAR Somake 1.0.9, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, [GitHub Actions #39243467444](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39243467444) — `SUCCESS`, 10 testes Java21; [dossiê de fluxo](../EXACT-BINARY-FUNERAL-BLOOM-FLOAT-DATAFLOW-1.0.9.md).

- `FuneralBloomSpell.getImpactDamage(int,LivingEntity):float`: o fluxo de pilha JVM linear demonstrou **`1.5f + (getSpellPower(level_input,caster)*0.75f)`**, com multiplicação float antes da adição float, 0 branches e chamada externa tipada a `getSpellPower`. É a fórmula de **retorno**, não garantia de dano final, canal de evento, crítico, efeito da resistência ou HP reduzido.
- `FuneralBloomSpell.getRadius(int,LivingEntity):float`: 2 branches e `SchoolType.getPowerFor`. Os operandos literais `10.0f`/`15.0f` da chamada a `Mth.clamp(FFF)F` seguem comprovados; a expressão completa de raio permanece **⚠️ `NOT_PROVED`** pelo avaliador linear. Não afirmar alcance físico 10–15 blocos apenas pelo clamp.
- O efeito de `FuneralBloomBudEntity.impact` mantém owner Somake e referencia o helper de dano do Iron's, Wither e `SpellHealEvent`. Ainda não está demonstrado como mutar o retorno por personagem sem afetar outro cast, como resolver o valor real de SpellPower nem como evitar dupla Mastery por bud.

**Boundary:** ✅ retorno JVM de `getImpactDamage` certificado; ⚠️ dano aplicado, evento e `getRadius` integral pendentes; ⛔ `FAIL_CLOSED` para perks de dano, raio, duração, alvo e recursos enquanto não existir contrato real testado. Somake 83/83 identidades segue inalterado.

## Contrato host de poder e CFG de raio — Iron's 3.16.3 (19/10/2026)

**Fonte:** JAR Somake 1.0.9 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` + API oficial Iron's 3.16.3 SHA-256 `69e81104a9fd31a402d9c89ab09c2a6b2fd6d2ab98db5a37bb159517363ee9ad`, [workflow Java21 #39246133056](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39246133056). [Dossiê CFG e host](../EXACT-BINARY-FUNERAL-BLOOM-RADIUS-IRONS-1.0.9.md).

- `getImpactDamage` e `getRadius` recebem `(int,LivingEntity):float`; `getImpactDamage` invoca `getSpellPower(int,Entity):float`. O descriptor invocado **existe em `AbstractSpell` no artefato oficial de API**. Não tratar `Entity` como indicação de evento per-player.
- O método host compilado referencia configuração via `SpellConfigManager.getSpellConfigValue`, atributos com `LivingEntity.getAttributeValue` e poder da escola com `SchoolType.getPowerFor`. Ainda não se comprovou a combinação exata das dependências nem os atributos/config ativos.
- O CFG do raio registra 28 instruções, uma branch `ifnonnull`, um `goto`, uma junção e um retorno, sem loops. `Math.max(float,float)` e `Mth.clamp(float,float,float)` são referências verificadas; somente os limites literais 10.0f e 15.0f estão provados. A fórmula integral permanece ⚠️ `NOT_PROVED`.

**Integração:** ⛔ `FAIL_CLOSED` para perks de dano, raio ou alterações de contexto do caster até prova de contrato de versão exata, condições reais do branch, settings e QA provider-loaded. Nenhuma nova magia ou estágio promovido.

## Raio — prova de dois caminhos JVM com caster (19/10/2026)

**Artefato:** Somake 1.0.9 File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [Java21 #39259507432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39259507432), dez testes `SUCCESS`; [dossiê completo](../EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md). A análise do CFG linear em #834 foi superada por verificação tipada dos **dois caminhos**.

Para `level` inteiro e `caster != null`, o retorno estático segue `Mth.clamp_f32((9.5 + i2f(level)*0.82) + (Math.max_f32(0,d2f(SchoolType.getPowerFor(caster))-1)*0.65), 10.0,15.0)`. Para `caster == null`, substitui a contribuição escolar por `Math.max_f32(0,1-1)*0.65` (= 0). A semântica e ordem float32 são essenciais; não interpretar a apresentação como álgebra de precisão infinita. O `ifnonnull` testa **o argumento caster**.

**Eixos para perks:** nível (coeficiente 0.82), bônus por poder de escola (coeficiente 0.65 e floor 0), clamp com operandos 10..15 e rota sem caster foram identificados em bytecode. A unidade em blocos, a projeção para área/targets, valores efetivos de escola/config, condições downstream, propriedade de eventos e interfaces para alterar por personagem continuam ⚠️/⛔. O getter **não** autoriza mutação de alcance diretamente. Nenhum double-processing de custo/cooldown/Mastery/impact é admissível.

**Estado:** ✅ retorno JVM do raio por ambos os caminhos; ⚠️ efeito em jogo e classe consumidora ainda não comprovados; ⛔ `FAIL_CLOSED` para adapter per-player. Somake 83/83 identidades sem alterações; Stage 06.05 🟡 e Stage 09 condicionado.

## Consumidores estruturais do raio — controller / bud (19/10/2026)

**Fonte:** Somake 1.0.9 JAR File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [Java21 #39262591589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39262591589), 9 testes `SUCCESS` e 3 classfiles inspecionados; [dossiê de consumidores](../EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md).

**Callsites de versão exata:** `FuneralBloomSpell.onCast` referencia `getRadius(int,LivingEntity):float`, `getImpactDamage(int,LivingEntity):float` e o construtor da `FuneralBloomControllerEntity(Level,LivingEntity,float,int,int,int,int,float,int,int)`. `Controller.tick`/`launchWave` possuem chamadas a `getRadius():float`. `launchWave` usa `AABB.inflate(double,double,double)`, `ServerLevel.getEntitiesOfClass` e constrói buds. `FuneralBloomBudEntity.impact` usa outra `AABB.inflate(double,double,double)`, consulta entidades, e referencia `DamageSources.applyDamage`, `SpellHealEvent`, cura e owner. O método `bud.impact` não contém invocação direta ao getter `getRadius`.

**Limite de prova:** referências co-presentes não certificam qual retorno alimenta os float do construtor, quais operandos dimensionam cada AABB, nem como um alvo elegível se transforma em impacto. Existem duas **superfícies diferentes de seleção/área** (controller wave e impacto individual); não tratá-las como sinônimos. Em `onCast` e `launchWave` há `invokedynamic`, contado sem atribuir corpo de lambda.

**Perks:** ⚠️ fórmulas de getter conhecidas e fontes consumidoras estruturais conhecidas; ⛔ `FAIL_CLOSED` para modificar raio, hitbox, quantidade de alvos, dano/Heal ou Mastery por caster sem prova de passagem de parâmetros e interface real. Nenhuma nova magia ou adapter foi criada.

## Controller: parâmetro float ainda sem vínculo causal ao getter (19/10/2026)

**Prova física:** [Java 21 #39286470816](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39286470816), `SUCCESS`, 13 testes, JAR Somake 1.0.9 File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. [Dossiê específico](../EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md).

- `FuneralBloomControllerEntity.<init>` tem argumentos float nos slots JVM 3 e 8; **a função de cada um não está certificada** pelo scanner.
- `FuneralBloomControllerEntity.getRadius():float` retornou `NOT_PROVED / getter_is_not_exact_three_opcode_direct_field_read`; a associação de um campo a esse getter e à atribuição do construtor também retornou `NOT_PROVED / no_certified_getter_field`.
- O padrão direto investigado era uma hipótese de auditoria. Sua rejeição **não** invalida a expressão `FuneralBloomSpell.getRadius(int,LivingEntity)` já demonstrada, porque são getters de **classes diferentes**. Nem implica que a controller ignore raio: falta o dataflow interno.

**Status:** ⚠️ parâmetros do construtor e assinatura conhecidos; ⛔ `FAIL_CLOSED` para perks mutadoras de área/raio/targets e dedução de dimensões de `AABB.inflate`. O complemento de resumo estrutural do getter permanece condicionado ao CI do HEAD final da PR #837. Nenhuma magia ou adapter nova.

## Controller — accessor de raio sincronizado identificado (19/10/2026)

- **Prova:** JAR Somake 1.0.9 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, [Java21 #39288405552](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39288405552) `SUCCESS` / 16 testes, [dossiê](../EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md). O método da controller `getRadius():float` lê **`SynchedEntityData.get(DATA_RADIUS)`** e converte `Float.floatValue()`. A leitura completa de sete instruções foi comprovada, sem cálculos adicionais no getter.
- **Escrita:** a varredura binária de 30 métodos localizou `defineSynchedData`, `setRadius(float)` e o accessor `DATA_RADIUS`; no método `setRadius` coexistem `Float.valueOf`, `SynchedEntityData.set` e carregamento `float` do slot 1. A fórmula inteira do setter e o vínculo com qualquer slot do construtor **não** foram demonstrados pelo interpretador.
- **Efeito em perks:** um `EntityDataAccessor` interno não é API pública para alterar um cast per-player. `onCast → construtor → setRadius → getRadius → wave AABB` permanece **⚠️ condicionado**; impacto da bud é superfície de área independente. ⛔ `FAIL_CLOSED` para perks mutadoras e dupla Mastery.

## Atualização causal do raio — slot do construtor e clamp do setter (19/10/2026, PR #838)

**Prova binária física:** Somake 1.0.9 File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, [workflow #39292948277](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39292948277) `SUCCESS` (31 testes no commit `db24ea4`). [Dossiê com assinatura e limites](../EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md).

| Eixo de perk | Evidência nova / decisão |
|---|---|
| Raio de estado da controller | ✅ primeiro argumento float do `FuneralBloomControllerEntity.<init>(Level,LivingEntity,float,int,int,int,int,float,int,int)` (**slot JVM 3**, não slot 8) passa diretamente a `setRadius(float)` |
| Fórmula do setter | ✅ `Mth.clamp` sobre argumento float do setter com limites **6.0f–18.0f**, grava `Float.valueOf` no accessor `DATA_RADIUS` |
| Leitura de estado | ✅ `getRadius()` lê `SynchedEntityData.get(DATA_RADIUS)`, converte `Float.floatValue()`, sem aritmética adicional |
| Input de spell / níveis / atributos | ⚠️ a expressão de `FuneralBloomSpell.onCast` passada ao primeiro float **não** está ligada por dataflow nesta auditoria; `getRadius(int,LivingEntity)` tem outra prova numérica isolada, que não substitui a chamada concreta |
| Targeting, área e dano/cura | ⚠️ `launchWave` referencia `getRadius`, `AABB.inflate` e criação de buds; `bud.impact` usa outra AABB. **Sem prova da propagação do valor aos dois volumes e às vítimas** |
| Modificação via RPG Skill Tree | ⛔ `FAIL_CLOSED`: `setRadius` interno não é hook público per-player; não inferir mudanças em raio, hitbox, tipo de alvo ou procs por disponibilidade de método |

**Escopo:** estreita e confirma a cadeia interna de dados sincronizados, sem criar magia, permitir perk ou demonstrar QA carregado/Survival. Esta seção **substitui exclusivamente a pendência antiga do setter/slot** nas auditorias históricas acima; os demais `NOT_PROVED` continuam vigentes. Identidade Somake segue 83/83 e esta magia permanece uma única raiz.

## Proveniência do primeiro `float` do `onCast` — prova exata (19/10/2026, PR #839)

- **Auditoria:** [GitHub Actions #39296264174](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39296264174), Java 21 `SUCCESS` / **45 testes**, Somake File 8867079 SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, [dossiê da cadeia](../EXACT-BINARY-FUNERAL-BLOOM-CONTROLLER-RADIUS-1.0.9.md).
- **Método/callsite:** `com.somake.somakespells.spells.blood.FuneralBloomSpell#onCast` invoca `getRadius(int,LivingEntity):float`, e **seu retorno é o primeiro `float`** transmitido diretamente à `FuneralBloomControllerEntity.<init>(Level,LivingEntity,float,int,int,int,int,float,int,int)` (argumento ordinal 3, posição que vira slot JVM 3 no construtor). Janela de 31 instruções da chamada verificada por pilha tipada e checagem estrita de descritores.
- **Cadeia de estado:** no construtor, esse float alimenta `setRadius(float)`, cujo corpo linear grava `DATA_RADIUS` após `Mth.clamp(input,6.0f,18.0f)`. O getter lê exatamente esse accessor.
- **Raio numérico de origem:** `FuneralBloomSpell.getRadius` possui expressão independente de nível/poder escolar e clamp `10.0f–15.0f`, com ramos `LivingEntity` nulo/não nulo certificados em [auditoria numérica](../EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md). Os valores numéricos indicam **estado interno** para entradas finitas; não provaram raio de `AABB` nem alcance real do cast.
- **Limites:** o scanner não estabelece identidade efetiva do `LivingEntity` enviado a `getRadius`, nem atribuição do segundo float, raio de `launchWave`, volume do impacto da bud, bloqueios PvP/claims, execução ao vivo ou hook seguro para perk. ⛔ `FAIL_CLOSED` na mutação, geração de dano/cura e Mastery; não repetir `onCast`.

Resultado: uma **única identidade** `somakespells:funeral_bloom`, ainda condicional para alcance/Survival e **sem adapter mutador**. A pendência de origem do primeiro float registrada em etapas históricas da ficha fica superada por esta auditoria específica, sem promover as demais.

## Área de seleção da controller — operandos `AABB.inflate` comprovados (19/10/2026; PR #840)

- **Evidência:** [Java 21 SHA-exata #39304248399](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39304248399), `SUCCESS`, **21 testes**, JAR Somake 1.0.9 File 8867079 / SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. [Dossiê de consumidores](../EXACT-BINARY-FUNERAL-BLOOM-RADIUS-CONSUMERS-1.0.9.md).
- **Classe/método de efeito:** `com.somake.somakespells.entity.FuneralBloomControllerEntity#launchWave(ServerLevel)`. A chamada interna compilada `net.minecraft.world.phys.AABB.inflate:(DDD)AABB` recebe **X = `f2d(getRadius())`**, **Y = literal `10.5d`**, **Z = `f2d(getRadius())`**. A prova exige os getters da própria controller e a sequência completa de conversões e argumentos sem ingresso de branch no meio.
- **Origem do raio:** `FuneralBloomSpell.getRadius(int,LivingEntity)` tem caminho de retorno com clamp `10f–15f` para entradas finitas; `onCast` passa o resultado ao primeiro `float` do construtor; o `setRadius` da controller aplica clamp adicional `6f–18f` antes de `SynchedEntityData.DATA_RADIUS`. Ambas as auditorias upstream são provas independentes.
- **Impacto no design de perks:** dimensões dos **argumentos da expansão AABB** agora têm evidência tipada para a versão física. **Não** equivalem à geometria efetivamente consultada em `getEntitiesOfClass`, ao dano/hitbox, ao limite de aquisição do `onCast` nem à área independente de `FuneralBloomBudEntity.impact`. ⛔ Nenhuma API pública por jogador para modificar raio/altura/targets foi homologada; `FAIL_CLOSED` mantém custos, aplicação e Mastery provider-native.
- **Status:** ✅ prova local de operandos de área X/Y/Z; ⚠️ propagação da AABB retornada à seleção real de entidades, cardinalidade e filtros não certificados; ⛔ mutações via perks bloqueadas. A classe/ficha já integra as **5/83** auditadas downstream; esta atualização acrescenta profundidade, **não uma nova magia**.

## Seleção da wave: AABB expandida efetivamente fornecida à query (20/10/2026; PR #841)

- **Fonte física:** Somake 1.0.9 File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; [auditoria Java21 #39466062186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39466062186), `SUCCESS` / **29 testes**, gate `PASS_SHA_EXACT_WAVE_XZ_RADIUS_Y_10_5_AND_QUERY_AABB_LINK`.
- **Classe/membro:** `FuneralBloomControllerEntity.launchWave(ServerLevel)` (196 instruções). A AABB criada pela expansão `inflate((double)controller.getRadius(),10.5d,(double)controller.getRadius())` é atribuída ao **slot local JVM 3** e lida do mesmo slot para o argumento `AABB` em `ServerLevel.getEntitiesOfClass(Class,AABB,Predicate)`, com `Class=LivingEntity`.
- **Predicate/seleção:** existe criação de `Predicate` por `invokedynamic` com capturas tipadas da controller e de `LivingEntity`, mas **nenhum filtro concreto nem resultado por alvo foram provados**. A query recebe os parâmetros; isso não certifica aceitação ou número de entidades.
- **Encadeamento técnico:** `FuneralBloomSpell.getRadius → primeiro float do construtor → setRadius(clamp 6–18) → DATA_RADIUS → controller.getRadius → AABB.inflate(R,10.5d,R) → astore_3 → aload_3 → getEntitiesOfClass`. O clamp próprio de `FuneralBloomSpell.getRadius` (10–15 para entradas finitas) segue evidência distinta; a caixa receptora, a condição do `Predicate`, a transformação da lista em buds e `bud.impact` ainda carecem de prova.
- **Perks/hook:** potencial eixo de área de **consulta de candidatos** identificado, mas sem contrato público seguro para aumentar X/Z, substituir Y ou modificar seleção por jogador. ⛔ `FAIL_CLOSED` para mutadores, procs/dano e Mastery. Ficha continua uma única identidade catalogada e já compõe as **5/83** fichas com downstream nesta campanha.
