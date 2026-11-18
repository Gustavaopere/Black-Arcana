# ACDestroyedItem — contrato de callback de destruição de item (1.0.10)

**Estado:** ⚠️ PARCIAL — descoberta SHA-exata; contrato estático individual **NOT_CERTIFIED**; hook mutador **NOT_VERIFIED**; QA física **NOT_TESTED**; integração **NO_MUTATION / fail-closed**; universo do provider **OPEN**. Este objeto é um suporte/consumidor técnico, com **zero novas raízes de magia**.

## Identidade e autoridade

- Provider: Alex's Caves Continued; mod ID **alexscaves**; Minecraft **1.21.1**, **NeoForge**, Java **21**.
- JAR publisher correspondente à versão da modlist: **alexscaves-1.0.10-neoforge+1.21.1.jar**; **75.279.314 bytes**; SHA-1 **6960b299a39a039ac8a5eb9b07be4ad0e3e0a570**; SHA-256 **36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c**. CurseForge projeto 1645389, arquivo 8856293.
- Interface **com.github.alexmodguy.alexscaves.server.item.ACDestroyedItem** (classfile SHA-256 **2ccc084cf825941414561ed02362fc3776b5ddddd699c8c62952818956771100**).
- Assinatura declarada, abstrata, pública: **onDestroyed(ItemEntity, DamageSource):void**; JVM descriptor **(Lnet/minecraft/world/entity/item/ItemEntity;Lnet/minecraft/world/damagesource/DamageSource;)V**; access flags **1025**. A interface não contém corpo.
- Único implementador direto no censo dos **1.555 classfiles**: **RadioactiveOnDestroyedBlockItem**, classfile SHA-256 **853e1f6318cfaa2c97ab27955e6b068e4e5f34ab94f4354092233e69bc502f24**. Nenhuma subclasse implementadora adicional foi encontrada no grafo do publisher.
- Superclasse do implementador **RadioactiveBlockItem**, classfile SHA-256 **1c769a4b64f0e4b3b9a2f5589bfc44ce3e27ec46c616b447d4e1359ffb21bd4b**. Ela não declara o overload de dois argumentos na classe publisher: o corpo herdado externo e seus efeitos permanecem **NÃO VERIFICADOS**.
- O método do implementador tem **170 bytes** de código JVM; Code SHA-256 **34f73b931946ae63544f4cbe9e35d1bd10fcab90f25b000bbdc54b98bc8b8881**; nenhum exception handler no próprio método.

A fonte pública em Codx-org/AlexsCavesContinued, commit **523308608422ab8e31974befa7111ecdf495dd37**, declara **versão 1.1.1** e **não é usada como prova dos valores 1.0.10**. Todas as constantes e offsets abaixo vieram do JAR publisher 1.0.10 auditado no GitHub Actions.

## Ativação, ordem e condições

A interface declara um callback, **não** um cast/feitiço independente, um registro de evento ou uma permissão para perks. No binário publisher, o censo encontrou **zero referências tipadas de chamada à interface**; não demonstra ausência de despacho por interfaces externas, engine NeoForge, reflexão ou transformações. O real ponto de invocação segue **NÃO VERIFICADO**.

O método **RadioactiveOnDestroyedBlockItem.onDestroyed** tem a seguinte sequência, identificada por bytecode:

1. **@0–3:** encaminha para **RadioactiveBlockItem.onDestroyed(ItemEntity,DamageSource)** por invokespecial; a resolução efetiva desse supermétodo depende de código externo não analisado neste recorte.
2. **@6–10:** consulta **DamageSource.isCreativePlayer()**; se verdadeiro, salta ao retorno **@169**.
3. **@13–17:** consulta **ItemEntity.isRemoved()**; se verdadeiro, salta ao retorno **@169**.
4. **@20–21:** chama **ItemEntity.discard()**.
5. **@24–138:** constrói/configura uma nuvem e solicita **Level.addFreshEntity**; seu retorno booleano é descartado por **pop @138**.
6. **@139–168:** solicita **Level.explode**, sem condicionar a chamada ao sucesso de **addFreshEntity**, e retorna em **@169**.

Guardas externos de lado cliente/servidor, ownership, eventos de dano e cancelamento, regras de permissionamento/claims e comportamento do engine **não foram certificados**. Os pedidos observados não comprovam que a nuvem e a explosão foram aplicadas fisicamente.

## Efeitos, parâmetros e consumidores exatos

| Campo | Valor / operação solicitada no bytecode 1.0.10 | Limitação |
|---|---|---|
| Item drop | **discard() @21**, após os dois guardas | Estado persistido/reload não testado |
| Instância de nuvem | **new AreaEffectCloud(level, x, y, z) @24–44** | Sem caster explicitamente configurado neste corpo |
| Partícula | **ACParticleRegistry.GAMMAROACH @49–60** | Partícula não é tipo de dano |
| Cor | **ACCompat.setCloudColor(7853582) @64–66**; hexadecimal **0x77D60E** | Propriedade visual |
| Status | **ACEffectRegistry.IRRADIATED**, instância com duração **9600 ticks** e amplificador **1**, passada a **AreaEffectCloud.addEffect @95** | Aplicação a vítimas e frequência não verificadas |
| Raio inicial | **2.0f @99–100** | Raio da nuvem, não tamanho da explosão |
| Duração da nuvem | **12000 ticks @104–107** | Distinta da duração 9600 do status |
| Tempo de espera | **0 @111–112** | Outros delays da engine não inspecionados |
| Contração radial | **-getRadius()/((float)getDuration()) @115–127**; parâmetros imediatamente anteriores dão **-2/12000 = -1/6000 unidade por tick** ao setter | Clamps e resultado físico não provados |
| Spawn da nuvem | **Level.addFreshEntity(cloud) @135**; resultado descartado | Não há guarda de sucesso antes da explosão |
| Explosão | **Level.explode(null, x, y+0.5, z, 1.8f, ExplosionInteraction.BLOCK) @139–165** | Null como fonte explícita; execução, proteção e dano final dependem do engine |
| Targeting e dano direto | O corpo não seleciona vítimas nem chama diretamente **LivingEntity.hurt** | Alvos/filtragem/dano efetivo pertencem aos consumidores externos |
| Custos e cooldown | **N/A no callback próprio**: não há operação observada de mana, stamina, munição, cobrança ou cooldown | Não inferir custos do item/engine externo |

Separar **parâmetros fornecidos** de efeitos **aceitos** pelo motor: a chamada a **Level.explode** demonstra uma tentativa de efeito potencialmente destrutivo, não comprova destruição de blocos no modpack, nem aplicação de dano a entidades.

## Autoria, persistência, rede e world safety

O callback recebe **ItemEntity** e **DamageSource**. A nuvem usa o mundo e a posição do item descartado; o método não chama setter de owner na nuvem. A explosão recebe **null** como argumento de entidade-fonte. **Kill credit, owner efetivo, XP, Mastery, loot, logs, persistência do cloud, save/reload, chunks, replicação de rede e isolamento multiplayer permanecem NÃO VERIFICADOS**.

A presença de **ExplosionInteraction.BLOCK** demanda avaliação do contrato de proteção territorial e do **WorldEffectPolicy** do Black Arcana. **Não presumir** que uma chamada nativa de terceiro passe automaticamente por esse contrato. Guards de Creative e remoção não demonstram proteção de claims, cancelamento do evento ou autorização de um perk.

## Interoperabilidade e gates para perks

- O provider continua autoridade do descarte, nuvem, estado irradiado e explosão. Black Arcana não deve emitir um segundo spawn/explode nem duplicar XP, dano ou cast.
- RPG Skill Tree continua autoridade apenas de progressão, atributos, perks, Mastery e gates por boundary real.
- A interface expõe uma declaração de callback; **não há hook mutador seguro verificado** para alterar raio, duração, tipo de alvo, potência ou autor de dano por jogador. O parâmetro DamageSource não é prova de caster ou titular de perk.
- **Estado obrigatório: NO_MUTATION/fail-closed**. Relevância conceitual para perks de área, resistência ou efeitos não certifica mutação executável.

## Evidências reproduzíveis, testes e pendências

O auditor **docs/qa/alexscaves_1010_destroyed_item_probe.py** está presente nesta branch e utiliza os parsers existentes do projeto. O workflow **.github/workflows/alexscaves-1010-destroyed-item-probe.yml** valida SHA-1, SHA-256 e tamanho do JAR, censa as 1555 classes, disassembla o método e arquiva JSON limitado. Execução do workflow no commit de auditoria **f7adadedb746f0c84f7b308088bc85600f682927**: [job de descoberta SHA-exata, resultado SUCCESS](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44212177669/job/134493028293); [artefato JSON temporário](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44212177669/artifacts/14386187733).

Reprodução de leitura somente (com artefato publisher exato e JDK 21): **python3 docs/qa/alexscaves_1010_destroyed_item_probe.py --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar --javap /caminho/jdk-21/bin/javap --output /caminho/novo/destroyed-item-discovery.json**.

A ferramenta produz **evidência de descoberta, não selo de sete eixos completo**. Pendências explícitas antes de certificação: resolução da superchamada e ciclo NeoForge ItemEntity/ItemStack; guardas server-side e dano que dispara o callback; consumação de status e parâmetros/targeting reais de AreaEffectCloud; proteção do mundo; atribuição de autoria e persistência; eventos, rede, configurações; testes semânticos negativos e testes físicos em cliente/servidor/modpack. O censo de 1555 classes **não fecha universo do provider**.

**Conclusão: ⚠️ ficha parcial, NOT_CERTIFIED, NOT_VERIFIED, NOT_TESTED, NO_MUTATION.**
