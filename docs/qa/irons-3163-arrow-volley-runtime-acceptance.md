# Iron's 3.16.3 — protocolo de observação Arrow Volley no modpack real

**Alvo:** Minecraft 1.21.1 · NeoForge **21.1.248** · Java 21 · `irons_spellbooks` **3.16.3** (artefato publicado de referência CurseForge file **8680204**). **Estado:** ✅ fixture compilada, 25/25 testes sintéticos; ⚠️ observação física pendente; ⚠️ GameTest / execução em servidor exato / fingerprint do JAR *instalado* pendentes; ⛔ alteração da contagem de flechas por perks sem contrato do provider. Stage 06.05 **não promovido**.

## 1. Evidência disponível, sem inferir gameplay

- [Prova binária publicada do Iron's](./irons-3163-projectile-bytecode-pending.md) e [Actions #38814840201](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38814840201): `ArrowVolleyEntity.tick()` não chama `super.tick()`, mas lê o contador `tickCount`; `SmallMagicArrow.shoot` usa `setDeltaMovement`.
- [Actions #38814378449](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38814378449) inspecionou o classfile Mojang 1.21.1 e provou `ServerLevel.tickNonPassenger` incrementando `Entity.tickCount` antes de `Entity.tick()`. Portanto **a hipótese anterior de spam infinito apenas pela ausência de `super.tick()` foi retificada**.
- [Modelo determinístico](./irons_3163_arrow_volley_tick_model_test.py): previsão de 25/36/42/56/63/80 projéteis e descarte no tick 26/31/36/41/46/51 conforme os seis níveis de spell. Isso **não** mede o resultado do pack.
- [Observador do mod de QA](../../src/catalogQaProbe/java/dev/gustavopere/blackarcana/qa/catalog/ArrowVolleyRuntimeEvidence.java): eventos públicos NeoForge e registros de entidades, sem importar classes internas do Iron's. Nunca integra o JAR de produção Black Arcana.
- [Validador fail-closed](./irons_3163_arrow_volley_observation_check.py): reavalia um log real, exigindo contagem, separação temporal de fileiras, monotonicidade de idade e descarte. O resultado `TRACE_CONSISTENT_NOT_GAMETEST` indica **somente consistência do trace**, não aprovação de GameTest ou contrato de +flechas.

## 2. Execução física necessária (não realizada)

Executar **somente em cópia de servidor QA do modpack**, com autorização e sem afetar personagens ou regiões permanentes. Instalar a própria build Black Arcana usada na PR e o JAR auxiliar `black_arcana_catalog_qa-0.1.0-dev.jar` construído separadamente. O mod auxiliar exige Black Arcana, Iron's, NeoForge e Minecraft definidos no seu `neoforge.mods.toml`. A build de QA **não substitui** a release do pack.

Pré-condições obrigatórias: coletar `modlist`/carregamento real, fingerprints SHA-256 dos JARs instalados de Iron's e NeoForge, hash do JAR auxiliar e da build Black Arcana, Java, configs e addons relevantes; testar sem outros casters com projéteis de Arrow Volley simultâneos na área. A URL/publisher publicada do Iron's **não demonstra** que o pack instalado corresponde ao SHA-256 `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73`.

Ativar apenas no servidor QA com argumento JVM **antes do boot**:

`-Dblack_arcana.catalog_qa.arrow_volley=true`

Em execução por Gradle, iniciar o processo de servidor configurado para carregar **os mods físicos**; o `runGameTestServer` canônico do Black Arcana sozinho não injeta o modpack nem faz o cast do Iron's. O listener da fixture não inicia casts nem cria flechas.

Em mundo dedicado e controlado, efetuar manualmente **um cast Arrow Volley válido** de nível 1, aguardar pelo menos 100 ticks e verificar descarte. Repetir separadamente nível 6 e, depois, níveis 2–5. Usar um único cast ativo a cada ensaio, ambiente carregado e sem chunks sendo descarregados. Registrar também zero/negativa de cast, blocos e alvos protegidos, interferência de outros mods e tempos de execução. Após os testes em chunks constantes, repetir um caso com unload/reload e um com proteção/spawn recusado.

## 3. O que o observador realmente mede

- `type=armed`: fixture instalada/ativada; não é prova de cast.
- `type=begin`: candidato de entidade `irons_spellbooks:arrow_volley` entrou pelo `EntityJoinLevelEvent`; informa UUID e dimensão. **Este evento acontece antes de confirmação definitiva de inserção.**
- `type=end`: idade inicial/final `tickCount`, monotonicidade amostrada a cada `ServerTickEvent.Post`, contagem de `small_magic_arrow` em eventos Join candidatos, contagem dos UUIDs localizáveis em um tick posterior do servidor, agrupamento por `level.getGameTime()`, motivo de saída reportado pelo `EntityLeaveLevelEvent`, ambiguidade de múltiplos controladores e flag de limite excedido.
- Associação controlador→flecha usa **mesmo owner UUID + mesma dimensão + distância ≤ 8 blocos**, com **apenas um** controlador elegível. Isso é uma **heurística de medição**, não identificador causal nativo. A fixture marca ambiguidades como não verificadas. Nenhuma varredura global é feita: até **4 controladores simultâneos**, **16 sessões por processo**, **100 ticks por sessão** e **256 flechas candidatas por sessão**; quando um limite é atingido, não se declara PASS.

A medição é passiva: **não** chama `onCast`, `addFreshEntity`, `discard`, `setOwner`, muda dano ou reescreve `SummonManager`. O resultado negativo pode significar ausência de fixture, cast negado, evento não disparado ou entidade carregada de disco; não inverter ausência em sucesso. O observador não certifica reload de entidades, API de buffs per-player, custos, cooldown ou propriedades internas do projectile.

## 3A. Regressão de offset temporal e cobertura do observador (2026-10-15)

**Falha reproduzida em testes sintéticos:** [Actions #38821246417](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38821246417) terminou com **FAIL (5 regressões)** porque o analisador original podia aceitar séries artificialmente deslocadas no tempo, contadores iniciais tardios, amostras insuficientes ou descarte muito posterior ao período nominal. Isso **não é bug de Arrow Volley no Minecraft**: é defeito comprovado no **validador do observador de QA**.

**Correção aplicável somente à fixture de testes:** a mensagem `type=end` passou a conter `join_game_tick` originalmente registrado em `type=begin`. O validador exige fileiras exatamente nos ticks `join_game_tick + 5, +10, ..., +5×rows` (não apenas separações de 5 ticks), amostragem desde `first_age=0` ou `1`, pelo menos `5×rows−1` amostras e `last_age` em `[5×rows, 5×rows+1]`. Qualquer dado ausente, cancelamento, chunk unload ou sequência incompatível permanece **FAIL_CLOSED**. O tempo observado é `ServerLevel.getGameTime` e não medição direta do início de cast; a hipótese do offset exato depende de execução real e poderá requerer ajuste **somente com prova física**, nunca relaxando automaticamente o gate.

O teste de regressão agora possui 15 casos, incluindo cinco casos **RED** comprovados no workflow citado. **GREEN corroborado por [Actions #38821874458](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38821874458)**, que executou 20 testes sintéticos e compilou a fixture no Java 21. Não corresponde à execução de servidor NeoForge com os JARs físicos. A comparação dos ticks elimina falso PASS para fileiras deslocadas, **não prova** que eventos Join foram causados pelo controlador: correlação owner/proximidade continua ⚠️ heurística.

## 3B. Fingerprint do JAR realmente carregado (2026-10-15)

A fixture de QA executa **uma vez em `ServerStartedEvent`** o método `ArrowVolleyRuntimeEvidence.emitProviderFingerprint()`, condicionado ao mesmo opt-in do observador. Ele obtém o caminho da instalação ativa por **`ModList.get().getModFileById("irons_spellbooks")`**, verifica que é arquivo regular, limita a leitura a **64 MiB**, calcula SHA-256 em streaming (buffer 8192 bytes) e publica **somente** nome do arquivo, tamanho, hash e correspondência. Não distribui o JAR nem altera dados ou entidades.

O registro necessário é `type=provider_fingerprint mod_id=irons_spellbooks status=OBSERVED ... bytes=13890046 sha256=13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73 expected_match=true`. Em arquivo ausente/inacessível/sob limite inválido, a fixture emite `HASH_UNAVAILABLE`; se a versão do pack difere da publicação já auditada, `expected_match=false`. **Não alterar a expectativa de SHA para forçar aceite**: reauditar a versão do artefato sob cadeia física correta.

O [validador](./irons_3163_arrow_volley_observation_check.py) agora exige **exatamente um** registro de fingerprint no log, com status, tamanho, hash e flag conferidos independentemente. Um registro ausente, duplicado, divergente ou alterado gera `PROVIDER_FINGERPRINT_UNVERIFIED` e saída de falha. Essa é **validação de conteúdo de log**; não autentica a origem do arquivo de log e não comprova sozinha a presença/versão do **NeoForge instalado**. Reter log de servidor do cenário efetivamente executado, launcher, metadata, hash do NeoForge e inventário de mods.

**Prova de regressão:** [Actions #38821612239](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38821612239) reproduziu a falha do validador antigo nos casos negativos de fingerprint (**RED**); o **GREEN foi confirmado em [Actions #38821874458](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38821874458)**: 20/20 testes sintéticos PASS e compilação Java 21 do JAR auxiliar com isolamento da produção PASS. Qualquer resultado de parser permanece classificado como `TRACE_CONSISTENT_NOT_GAMETEST`, não como conclusão de GameTest.

## 3C. Integridade da sequência de idade e entidades não frescas (2026-10-15)

**Evidência de regressão:** [RED #38825091652](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38825091652) executou **25 testes**, dos quais **5 falharam** para condições anteriormente aceitas indevidamente: amostras temporais descontínuas, saltos/duplicação de idade, controlador já com idade positiva ao ingressar no mundo, flecha candidata já envelhecida ao entrar e campo de amostragem ausente. A regressão é do **parser de QA**, não do jogo ou do provider.

**Correção na fixture:** a mensagem `type=end` apresenta `controller_join_age`, `sample_gaps`, `age_step_mismatches` e `nonfresh_arrow_joins`. A amostragem em `ServerTickEvent.Post` agora registra quebra quando `getGameTime` não avança exatamente um tick entre leituras consecutivas, e quando `entity.tickCount` não cresce **exatamente uma unidade** entre leituras contíguas. O evento de Join registra `entity.tickCount` do controlador e de cada flecha associada como candidata. O parser exige **zero nas quatro métricas**; valores ausentes também falham. Isso impede tratar uma sessão temporalmente descontínua como equivalente ao modelo de disparos ininterruptos.

**Evidência GREEN:** [Actions #38825193239](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38825193239) **SUCCESS**, com **25/25 testes sintéticos PASS**, compilação Java 21 de `catalogQaProbeJar` e isolamento do observador no JAR auxiliar **PASS**. O mesmo run continuou verificando o classfile do Iron's publicado e a ordem de ticks Mojang 1.21.1.

**Caveat:** `tickCount>0` na entrada é **indício incompleto de entidade restaurada**, não garantia de detecção de todo reload; entidades recarregadas com idade zerada poderiam escapar deste sinal. Tampouco um trace temporal perfeito assegura origem de projéteis: correlação por owner + proximidade continua heurística. Para certificação, usar execução real no modpack e conferir chunk unload/reload por eventos, NBT e inspeção in-game, sem inferir PASS do parser.

## 4. Processamento e critérios de aceite do trace

Preservar log original integral do **servidor de QA**, com identidade e dados privados redigidos antes de compartilhamento. Executar, na raiz do repositório:

`python3 docs/qa/irons_3163_arrow_volley_observation_check.py --log caminho/do/server.log --spell-level 1 --report build/arrow-volley-level1-report.json`

Se existirem várias sessões, identificar UUID do controlador em `type=begin/end` e passar `--controller UUID` para selecionar uma. Repetir `--spell-level 6` para o outro caso. Não usar logs sintéticos dos testes Python como evidência física.

**Critérios automáticos do validador:** exatamente uma sessão selecionada; `LEFT_LEVEL` e motivo `DISCARDED`; idade monotônica com mínimo de ticks; nenhum budget estourado nem relação ambígua; para o nível declarado, número de candidatos **e de entidades ainda presentes no mundo ao fim do tick** igual ao previsto; número de fileiras e seus tamanhos corretos; distância de **5 ticks** entre entradas de flechas; consistência da soma do mapa com a contagem declarada. Qualquer falha devolve `FAIL_CLOSED` e exit code não-zero.

Mesmo quando esse validador retorna `TRACE_CONSISTENT_NOT_GAMETEST`, **a aceitação física continua ⚠️**, até anexar hash do pack instalado, logs completos, captura real do mundo, casos de chunk unload/reload, condições de servidor e confirmação de que não houve falso pareamento por proximidade. Necessário também medir TPS/desempenho e tentativas de spawn rejeitadas por outros mods, sem extrapolar `EntityJoinLevelEvent` como contagem universal de `addFreshEntity` aceito.

## 5. Estado e próximo gate

| Evidência | Status |
|---|---|
| JAR publicado Iron's e classfile `ArrowVolleyEntity.tick` | ✅ prova binária estática |
| Mojang 1.21.1 `ServerLevel.tickNonPassenger` | ✅ prova binária estática |
| Modelo de seis níveis | ✅ teste determinístico (não GameTest) |
| Código da fixture removível / testes do parser | ✅ compilado e isolado (Actions #38820230432; 20/20 testes sintéticos); ⚠️ ainda sem execução no pack |
| Logs reais NeoForge 21.1.248 com Iron's + modpack | ⚠️ **pendente** |
| Fingerprint do JAR instalado e compatibilidade com o publicado | ⚠️ **pendente** |
| Unload/reload e limites sob mundo protegido | ⚠️ **pendente** |
| Perk de +flechas / alteração de cooldown/owner | ⛔ **bloqueado** sem hook e contrato de segurança |

**Autoridades:** Iron's mantém suas entidades e efeitos; Black Arcana mantém exclusivamente seu próprio runtime; RPG Skill Tree só atributos, Mastery, perks e gates mediante contrato validado. Essa medição não altera essa separação. **Clean-room:** não copiar/decompilar/republicar código/bytecode/recursos de terceiro.
