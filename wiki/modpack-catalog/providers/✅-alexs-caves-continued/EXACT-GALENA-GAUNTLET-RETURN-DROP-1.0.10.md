# Galena Gauntlet — retorno da arma, fallback de drop e lifecycle nativo (Alex's Caves Continued 1.0.10)

**Estado:** ⚠️ **subcontrato estático parcial SHA-exato, somente leitura**. O presente recorte documenta solicitações nativas de retorno, remoção e spawn, **não comprova restituição física de itens, transação de inventário, ausência de perda/duplicação, aceitação do spawn nem hook seguro**. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `NO_MUTATION` · `provider_universe_closed=false`. A Galena permanece **um equipamento com ação própria**, não uma nova raiz de cast criada por este subcontrato.

## 1. Proveniência, identidade e reprodução

- **Mod e artefato do publisher:** Alex's Caves Continued, mod ID `alexscaves`, 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A modlist sibling `Gustavaopere/neoforge-rpg-skilltree` identifica o mesmo nome, mod ID, versão e SHA-1 na posição física #19 da lista atual registrada. A paridade contra **novo dump efetivo da instalação** ainda é `NOT_VERIFIED`.
- **Classes publisher:** `GalenaGauntletItem` (`com/github/alexmodguy/alexscaves/server/item/`, SHA-256 `5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0`) e `MagneticWeaponEntity` (`com/github/alexmodguy/alexscaves/server/entity/item/`, SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071`). O helper `com/github/alexmodguy/alexscaves/server/misc/ACCompat` possui classfile SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b` (200 métodos declarados); **somente `spawnAtLocation(Entity,ItemStack)`** foi acrescentado a este recorte, sem certificação dos outros membros.
- **Cadeia de evidência:** relatório Galena anterior `report.json` de **1.780.492 bytes**, SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`, reconstruído em CI com o mesmo publisher; novo relatório de **188.299 bytes**, SHA-256 `8cff541420b4bbca8820aa419ed73cf01478c4a881c7f6afa12e256f6a9ae916`, gerado no [workflow inicial #45080911861](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45080911861), artefato #14777325666.
- **Reprodução:** [sonda read-only](../../../../docs/qa/alexscaves_1010_galena_return_drop_probe.py), [manifesto SHA-exato](EXACT-GALENA-GAUNTLET-RETURN-DROP-1.0.10.json), [verificador com falsificações adversariais](../../../../docs/qa/alexscaves_1010_galena_return_drop_checks.py) e [workflow de CI](../../../../.github/workflows/alexscaves-1010-galena-return-drop-audit.yml). São fixados **423 pivôs JVM** em nove métodos (oito corpos de item/entidade e um helper), com atributos `Code`, instruções, descritores e callsites; o verificador local rejeitou **61 mutações de opcode/branch/operando em cópias do relatório cujos digests foram recalculados**. Isso não constitui testagem do jogo. A CI precisa confirmar novamente o mesmo relatório na HEAD final da PR.

## 2. Entrada do item, autoria e criação sem contrato de rollback

`GalenaGauntletItem.onUseTick(Level,LivingEntity,ItemStack,int)` tem **120 instruções** observadas. Após seleção da stack oposta e comparação com armas já controladas, o ramo de criação @186–262:

1. Solicita `ItemStack.copy()` da stack oposta @193.
2. Solicita `ItemStack.setCount(0)` sobre a stack original **antes da criação e inclusão da entidade** @201.
3. Solicita `ACCompat.createEntity` @216 e atribui o resultado a `MagneticWeaponEntity`; solicita `setItemStack(cópia)` @228, `setPos` @243 e `setControllerUUID(livingEntity.getUUID())` @252.
4. Solicita `Level.addFreshEntity(entity)` @258, cujo booleano é **descartado por `pop` @261**. Nesta janela **não existe rollback explícito** no caso de retorno negativo da adição.

A ausência de rollback local **não prova uma perda reproduzível de item**. A semântica dos callbacks, das permissões, da engine, de eventos e de outros mods não foi auditada. O `ControllerUUID` por si não demonstra posse contínua nem equivalência ao jogador em outro mundo/dimensão; o contrato de controller já foi [auditado em separado](EXACT-GALENA-GAUNTLET-PERSISTENCE-SYNC-1.0.10.md).

## 3. Condições de owner e retorno

`MagneticWeaponEntity.isOwnerWearingGauntlet()` tem **26 instruções**. Recupera `getController` @1 e só alcança retorno verdadeiro quando o controlador é `LivingEntity`, seu `getUseItem` é `ACItemRegistry.GALENA_GAUNTLET`, a entidade está viva e o campo `returnFlag` é falso (@6–57). O campo `returnFlag` **não é sinônimo** de `comingBack` e não foi encontrado como persistido pela sobrescrita NBT examinada.

No `tick()` de **744 instruções**, o ramo de `Player` começa @470, preenche `CONTROLLER_ID` na estrutura sincronizada e solicita `IDLING=false`; define `comingBack=!isOwnerWearingGauntlet()` @517–530. Se o player continua usando a Gauntlet, `hadPlayerController=true` @540–549; outros ramos (alvo, ataque, mineração) permanecem sob seus próprios contratos. Se não, entra na janela **@1416–1551**:

- Atualiza `returnProgress = min(1.0F, returnProgress + 0.2F)` enquanto o valor atual for menor que 1 (@1417–1438), e limpa o indicador de trinca do bloco previamente selecionado usando `Level.destroyBlockProgress(...,-1)` @1441–1467. O getter interpola `prevReturnProgress + parcial × (returnProgress-prevReturnProgress)`; isso é **estado de progressão/visual**, não confirmação de item restituído.
- Define destino de movimentação na posição do player somando `(0,1,0)` @1470–1481. Se a distância **entidade arma → player** for inferior a **1,4 bloco** @1483–1493, e a entidade não estiver removida @1496–1500, entra na liquidação local. **1,4** não é o alcance nominal de ataque nem garantia de contato final.
- Se `spawnedItem=false`, solicita `Player.addItem(getItemStack())` @1503–1519. **Quando essa chamada retorna `true`**, marca `spawnedItem=true` @1522–1524 e solicita `remove(DISCARDED)` @1527–1531. O booleano é observado localmente, mas não certifica transação atômica, aceitação por plugins ou estado de inventário persistido.
- Se `spawnedItem=true` ou o `addItem` retorna `false`, solicita `plopItem()` @1537–1538. Depois disso, havendo destino não nulo, o tick ainda pode solicitar `directMovementTowards(destino, velocidade)` @1541–1551. O movimento usa operações `Vec3`/`setDeltaMovement`, e o tick ao final solicita `move(SELF,delta)` e damping por **0,8999999761581421d** @1571–1593. Movimento acumulado não prova restituição.

**Limite da autoridade de lado:** há guarda `!Level.isClientSide` no trecho inicial de `tick` antes das condições de remoção por ausência de owner/stack. A janela de devolução no ramo de player @1416–1538 não apresenta por si mesma uma segunda guarda explícita equivalente. Isso **não** demonstra escrita autoritativa do cliente; os métodos externos e a engine tratam suas próprias regras de lado. Não executar mutações de inventário a partir de uma apresentação cliente por inferência deste método.

## 4. `plopItem`: flag antes do spawn e descarte terminal

`MagneticWeaponEntity.plopItem()` contém **19 instruções**. Se `spawnedItem` já é verdadeiro, salta o caminho de spawn (@1–4). Caso contrário, marca imediatamente `spawnedItem=true` @8–9, solicita `ACCompat.spawnAtLocation(this,getItemStack())` @12–17 e, se a `ItemEntity` resultante não for nula, solicita `ItemEntity.setNoPickUpDelay()` @21–26. Independentemente do retorno nulo ou não, solicita `remove(DISCARDED)` @29–33. O flag **antecede** a chamada: não serve como recibo comprovado de spawn bem-sucedido.

A nova inspeção do classfile exato mostra que `ACCompat.spawnAtLocation(Entity,ItemStack)` é uma **ponte direta de quatro instruções**, com atributo `Code` SHA-256 `505d89864837abd20cf36829273586fcff20e07d7cbe828010d73481e2311ed6`: recebe dois argumentos, chama virtualmente `Entity.spawnAtLocation(ItemStack)` @2 e retorna a referência @5. Não há guarda, validação ou fallback adicional **no corpo desse wrapper**. A decisão real de materializar a entidade-item é externa e continua `NOT_VERIFIED`.

**Distinção causal:** `Player.addItem` pode retornar `false` e provocar o fallback; `ACCompat.spawnAtLocation` pode retornar `null` e o método de fallback ainda solicitar remoção. Nenhum dos casos demonstra automaticamente item perdido, item duplicado, drop criado, pickup permitido ou ausência de intervenção externa. São **ramos de risco de liquidação**, que exigem QA físico e exame dos métodos engine nas versões instaladas.

## 5. Controller ausente, expiração e persistência não garantida

No começo do `tick`, a janela **@30–124** executa no servidor. Se o controller é nulo e `tickCount>20`, ou se a stack da arma está vazia, considera um ramo de descarte. **Somente quando `hadPlayerController=true`** solicita `plopItem()` @101–109; depois zera `hadPlayerController` @112–114 e solicita `remove(DISCARDED)` @117–121. Se `hadPlayerController` está falso, a chamada a `plopItem` não é alcançada nessa janela antes da remoção.

`hadPlayerController` e `spawnedItem` são campos transientes da entidade, inicializados no construtor e utilizados nos métodos apresentados. `addAdditionalSaveData`/`readAdditionalSaveData`, já inspecionados no [subcontrato de NBT](EXACT-GALENA-GAUNTLET-PERSISTENCE-SYNC-1.0.10.md), escrevem/leem **`WeaponStack` e `ControllerUUID`**, mas não esses flags, nem `comingBack` ou `returnProgress`. **Inferência de risco:** após reload, os flags podem não refletir operações anteriores; a combinação com owner ausente e expiração precisa de teste real para caracterizar eventual perda, repetição de drop ou remoção segura. Nenhuma dessas consequências foi demonstrada fisicamente.

O `tick` pode continuar a executar outras janelas após solicitar `remove`, pois não há `return` imediato logo depois de @121; o efeito sobre a entidade já removida depende do ciclo de vida implementado pela engine. Isto não constitui uma segunda invocação obrigatória de efeitos.

## 6. Fronteira de integração, Mastery e QA pendente

- **Proibição de emissão automática de progressão:** `spawnedItem`, `hadPlayerController`, `returnProgress`, `Player.addItem` e `Entity.spawnAtLocation` não formam um contrato de evento de restituição confirmado. Não contar retorno/queda como cast, kill, perk ou XP.
- **Inventário e owner:** a restituição exigiria autoria canônica, um resultado servidor-autorativo observado, deduplicação em concorrência/reload e consistência entre inventário e entidade; nenhum hook mutador apropriado foi certificado.
- **Política de mundo:** o Black Arcana mantém `WorldEffectPolicy` e autoridade sobre qualquer efeito próprio. Nunca presumir que interceptar flags do provider confere autoridade para criar drop ou alterar inventário. O RPG Skill Tree recebe somente boundary real, não controla o runtime.
- **QA física necessária:** mãos alternadas e troca de item, retirada da luva durante ataque/mineração, inventário cheio, `Player.addItem` negativo, `Entity.spawnAtLocation` nulo, owner logout/dimensão, unload/reload, save/restart/crash entre cópia e spawn ou entre flag e criação de item, side cliente/servidor, múltiplos jogadores e proteção territorial. Testar item real, contagens e persistência, não apenas partículas ou UI.

**Estado final deste recorte:** evidência técnica estática de **solicitações** e dependências, **sem** contrato estático integral da Galena, hook mutador, perks executáveis, QA física ou fechamento do universo. Manter `NO_MUTATION` / fail-closed. Fonte clean-room: diagramas e descrições próprias de interoperabilidade; não copiamos implementação proprietária para o Black Arcana.
