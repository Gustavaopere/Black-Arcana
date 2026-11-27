# Galena Gauntlet — guardas de recusa de spawn (engine NeoForge 21.1.248)

**Estado:** ⚠️ subcontrato de interoperabilidade **estático e read-only**, com classfiles oficiais de `--installServer` examinados por SHA exato. Não é certificação individual da Galena, instrumentação de jogo ou demonstração de perda/duplicação da arma. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · universo de provider aberto.

## 1. Proveniência, alvo e resultado verificável

- **Objeto/publisher:** `alexscaves:galena_gauntlet`, Alex's Caves Continued **1.0.10** (Minecraft 1.21.1/NeoForge/Java 21); modlist sibling: `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; publisher JAR analisado: 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Novo dump físico ainda não cotejado.
- **Engine oficial:** `neo_version=21.1.248` nos `gradle.properties` Black Arcana e RPG Skill Tree. Instalação `--installServer` do NeoForge 21.1.248; overlay `neoforge-21.1.248-server.jar` SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`; base Minecraft SRG SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`. Os binários são da **distribuição upstream**, antes de modificações da ModLauncher/modpack.
- **Classfiles fixados:** `ServerLevel.class` SHA-256 `19b42e51848fd27df3683dacf694baa5126ee9f0665f12afdc65f82493a1e5a3`; `PersistentEntitySectionManager.class` SHA-256 `6351fcb7c7370b77b8d9618474783b58ab3e037c224b5c83481c23908db1fbf4`.
- **Coleta inicial bem-sucedida:** [GitHub Actions #45232344296](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45232344296), job `137894927228`, HEAD `7bd94be896b2423aa883ab676bc7f21486dbcec7`. `report.json` **19.914 bytes**, SHA-256 `c9b4691fbb4a7c1f54964fe568abad111fd891b51543251b3782545adb6c8473`. Essa coleta demonstra o método de auditoria; não substitui o checker SHA-exato adicionado posteriormente.
- **Arquivos reproduzíveis:** [sonda](../../../../docs/qa/alexscaves_1010_galena_211248_spawn_denial_guards_probe.py), [manifesto SHA-exato](EXACT-GALENA-SPAWN-DENIAL-GUARDS-21.1.248.json), [verificador adversarial](../../../../docs/qa/alexscaves_1010_galena_211248_spawn_denial_guards_checks.py), [workflow](../../../../.github/workflows/alexscaves-1010-galena-neoforge-211248-denial-guards.yml) e [ficha individual](equipment/galena-gauntlet.md). O relatório e manifesto não reproduzem código-fonte, body Java, bytecode ou assets de terceiros.

A prova rastreia **4 métodos**, **35 instruções de acesso a membros tipadas** (invoke/getfield/getstatic/etc.), **9 branches** e **9 pontos de retorno** neste recorte. Seus hashes por método, por roster de referências, branch e terminal são conferidos pelo checker, além do SHA-256 de todo o relatório.

## 2. Três causas de recusa distinguíveis na distribuição oficial

### A. Recusa antecipada: entidade já removida

Na rotina `ServerLevel.addEntity(Entity):Z`, há chamada JVM tipada a `Entity.isRemoved():Z` no offset **1**. O `ifeq` @**4** salta para **27** na condição falsa; a continuação local retorna `iconst_0 → ireturn` @**26** quando `isRemoved` é verdadeiro. Esse caminho de recusa ocorre **antes** da invocação a `PersistentEntitySectionManager.addNewEntity` @**32** e não depende do resultado de `EntityJoinLevelEvent`. O mesmo método tem outro `ifeq` @**35**, relacionado ao resultado booleano do manager, com retorno `false` @**45** e aceitação normal com `onAddedToLevel` @**39**, `true` @**43**. A [auditoria de CFG anterior](EXACT-GALENA-SPAWN-RETURN-CFG-21.1.248.md) já fixou os ramos.

### B. Recusa por evento cancelado, antes de registrar UUID

`PersistentEntitySectionManager.addEntity(EntityAccess,Z):Z` tem publicação de `EntityJoinLevelEvent`, consulta `isCanceled():Z` @**36** e `ifeq` @**39**. Com evento cancelado, a rotina distribuída termina em `iconst_0 → ireturn` @**43**; com o evento não cancelado, prossegue para `addEntityWithoutEvent` @**47** e retorna seu booleano @**50**. A verificação do evento é condicionada ao `instanceof Entity` presente no mesmo método. O presente estudo não identificou um listener real ou um cancelamento ocorrido no jogo.

### C. Recusa por UUID já registrado, independentemente do evento

A nova descoberta localiza em `PersistentEntitySectionManager.addEntityWithoutEvent(EntityAccess,Z):Z` uma chamada tipada a `addEntityUuid(EntityAccess):Z` @**2** seguida de `ifne` @**5**; o ramo falso retorna `iconst_0 → ireturn` @**9**, sem alcançar a criação/seleção de seção de entidade.

O próprio `addEntityUuid(EntityAccess):Z` (Code SHA-256 `5f312b918531647b3983fc55ad0330bb0e43acd5f3609d66e5d8148aac7a2b25`) acessa `knownUuids:java.util.Set` @**1**, chama `EntityAccess.getUUID():UUID` @**5**, consulta `Set.add(Object):Z` @**10** e testa o booleano em `ifne` @**15**. Se `Set.add` devolve `false`, retorna `iconst_0 → ireturn` @**30**; se `true`, o caminho aceita e retorna `iconst_1 → ireturn` @**32**. Pela semântica padrão de `java.util.Set.add`, uma tentativa de inserir um valor já presente não aumenta o conjunto e retorna `false`; **este é um motivo distinto e estaticamente comprovado de recusa**, não um cancelamento de evento. Não significa que um UUID duplicado tenha sido observado no modpack.

Depois dessa guarda, a mesma rotina distribuída referencia `EntitySectionStorage.getOrCreateSection` @**25**, `EntitySection.add` @**33**, `EntityAccess.setLevelCallback` @**49**, callbacks condicionados ao flag de carregamento e `Visibility.isAccessible/isTicking`, `startTracking` @**89** e `startTicking` @**102**. O método possui um `ireturn` verdadeiro @**106**. Branches posteriores @55/@84/@97 regulam esses efeitos de lifecycle e **não correspondem a outros pontos de retorno falso locais** no recorte; exceções de chamadas externas não foram simuladas.

## 3. Relevância para a Galena e limites

O dossiê do publisher [`RETURN-DROP-1.0.10`](EXACT-GALENA-GAUNTLET-RETURN-DROP-1.0.10.md) demonstra que `GalenaGauntletItem.onUseTick` pede `ItemStack.copy()` @193 e `ItemStack.setCount(0)` @201 **antes** de `ACCompat.createEntity` @216 e `Level.addFreshEntity` @258; seu booleano é descartado por `pop` @261. O encadeamento [JVM distribuído já selado](EXACT-GALENA-DISTRIBUTED-SPAWN-21.1.248.md) e a [CFG](EXACT-GALENA-SPAWN-RETURN-CFG-21.1.248.md) demonstram caminhos normais que devolvem `false`, incluindo (a) entidade removida, (b) evento cancelado e (c) UUID já presente no conjunto.

**Inferência limitada:** essas três condições são motivos estruturalmente distintos pelos quais uma tentativa de entrada de entidade pode resultar em `false` na distribuição. Isso **não demonstra que alguma delas tenha ocorrido para `MagneticWeaponEntity`**, nem que a cópia seja perdida, restaurada ou duplicada no mundo, nem ausência de compensação externa. A autoridade da stack, a criação física, o registro de entity UUID, NBT, owner, world protection, modded listeners e transformações de ModLauncher continuam não verificados.

A inspeção desta nova fronteira não autoriza mutar o cálculo de ataques, raio, cooldown, spawn, inventário, Mastery, XP ou eventos. O **Black Arcana** mantém autoridade exclusiva sobre seu runtime mágico, e o **RPG Skill Tree** é sibling/provider de progressão, atributos, Mastery e perks apenas mediante boundary server-owned certificado e efetivamente consumado. **Sem hook real e transação segura: `NO_MUTATION`/fail-closed.**

## 4. Reprodução e gates

```bash
python3 docs/qa/alexscaves_1010_galena_211248_spawn_denial_guards_probe.py \
  --server /caminho/neoforge-21.1.248-server.jar \
  --srg /caminho/server-1.21.1-20240808.144430-srg.jar \
  --javap /caminho/java21/bin/javap \
  --output /diretorio-novo/report.json

python3 docs/qa/alexscaves_1010_galena_211248_spawn_denial_guards_checks.py \
  --report /diretorio-novo/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-SPAWN-DENIAL-GUARDS-21.1.248.json' \
  --adversarial
```

**Certificação somente deste subcontrato** exige reexecução no GitHub Actions com o JAR distribuído oficial e seus SHA-256, SHA e tamanho do relatório idênticos, hashes de cada roster de métodos/membros JVM, 35+ falsificações rejeitadas e os gates canônicos do repositório na HEAD final. Manter a PR como rascunho enquanto qualquer gate estiver pendente.

**Pendências bloqueantes para certificação da ficha individual:** verificar bytecode **pós-ModLauncher** da instância, listeners concretos, cenários físicos com evento cancelado, UUID duplicado e entidade removida, falha de criação, state de inventário/stack, owner, drops, reload, troca de dimensão, proteção territorial e aceitação de `addFreshEntity` no servidor. Nenhuma dessas condições foi observada em QA física nesta auditoria.

**Índices:** estado Galena ⚠️ parcial, Alex's Caves **130/134** contratos estáticos certificados do recorte observado, global **269/2.446**, providers documentais concluídos **4/164** e integralmente perk-ready **0/164**. Os três motivos de recusa pertencem ao mesmo objeto Galena, **sem criar três magias ou ampliar o numerador**.
