# Galena Gauntlet — retorno booleano e CFG distribuído de spawn (NeoForge 21.1.248)

**Estado:** ⚠️ subcontrato estático de *control-flow graph* (CFG) do **bytecode oficialmente distribuído**. Os dados foram extraídos de classfiles de Minecraft 1.21.1/NeoForge 21.1.248 sem rodar gameplay, sem copiar corpos Java e sem observar o ModLauncher. **A Galena Gauntlet continua com contrato individual NÃO CERTIFICADO.** `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

## 1. Fontes e escopo

- **Provider de objeto:** Alex's Caves Continued 1.0.10, `alexscaves`, `alexscaves-1.0.10-neoforge+1.21.1.jar`; SHA-1 físico registrado na modlist sibling `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; publisher JAR SHA-256 já auditado `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Paridade de novo dump da instalação: **NÃO VERIFICADA**.
- **Alvo de compilação:** Minecraft 1.21.1, NeoForge `neo_version=21.1.248`, Java 21, nos `gradle.properties` de Black Arcana e RPG Skill Tree.
- **Distribuição oficial (sem transformações da instância):** instalador `neoforge-21.1.248-installer.jar` SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`; overlay server `neoforge-21.1.248-server.jar` SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359` (**5.675.624 bytes**); Minecraft SRG `server-1.21.1-20240808.144430-srg.jar` SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`.
- **Evidência observacional inicial:** [workflow #45223070726](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45223070726), job `137862201325`, HEAD `e7ae329b24a748649242c1a6909461349b58251c`, **success**. Relatório `report.json` **18.311 bytes**, SHA-256 `19ce72117b30cbb716cd385638ebbcdf40b8ea68690a0c4a07aa9b53b8bad579`.
- **Rastreabilidade versionada:** [sonda read-only](../../../../docs/qa/alexscaves_1010_galena_211248_spawn_return_cfg_probe.py), [manifesto SHA-exato](EXACT-GALENA-SPAWN-RETURN-CFG-21.1.248.json), [verificador adversarial](../../../../docs/qa/alexscaves_1010_galena_211248_spawn_return_cfg_checks.py) e [workflow dedicado](../../../../.github/workflows/alexscaves-1010-galena-neoforge-211248-return-cfg.yml). O checker posterior precisa passar na **HEAD final** antes de merge; a execução de descoberta anterior não o substitui.
- **Compatibilidade com evidência anterior:** o checker também executa a validação do [manifesto da cadeia distribuída aprovado na PR #1176](EXACT-GALENA-DISTRIBUTED-SPAWN-21.1.248.json), depois remove exclusivamente os campos de CFG para preservar seus **16 callsites JVM tipados previamente selados**. O novo manifesto pinou **5 métodos**, **8 branches** e **9 locais de retorno**.

A extração preserva apenas classe, assinatura, SHA-256 de classfile e Code, offsets, código de opcode de salto/retorno, destino/fallthrough, contagens de instruções, SHA-256 do roster de arestas e quantidade de handlers. O programa não reconstrói scripts, patches ou implementação de terceiros. Nenhuma execução da Galena no servidor foi observada.

## 2. Métodos e topologia de retorno da distribuição

Os métodos abaixo estão na distribuição NeoForge 21.1.248 e todos os seus bytes de Code foram pinados; cada método selecionado tem **zero handlers de exceção declarados**, o que **não elimina possíveis exceções vindas de chamadas externas**.

| Owner e método | Desvios condicionais | `ireturn` observados | SHA-256 do roster de arestas |
|---|---:|---:|---|
| `ServerLevel.addFreshEntity(Entity):Z` | 0 | 1, @5 | `4605a0a2c5f831bf9e8f5b6c115ebc4b1a5837c77d67706bd565b4d406553ef0` |
| `ServerLevel.addEntity(Entity):Z` | 2 | 3, @26/@43/@45 | `d0e2e07d531fcd64251f3b8f8f23a88012d84532ad838b8d9223bab3d969c452` |
| `PersistentEntitySectionManager.addNewEntity(EntityAccess):Z` | 0 | 1, @6 | `f5d1a6fccdc4735230732c6cdc9e1fc795a1f97e4e3c0837b4a8a435fcd5b892` |
| `PersistentEntitySectionManager.addEntity(EntityAccess,Z):Z` | 2 | 2, @43/@50 | `249d43c5e8015ec0e2f67bc4a5944ae48cd71e2eac36a972655aab543e4fe3e7` |
| `PersistentEntitySectionManager.addEntityWithoutEvent(EntityAccess,Z):Z` | 4 | 2, @9/@106 | `50fa6100975fa0909dee0031c40f295cf735c3f01ea0e11c8885befe7ed0b7c3` |

**Todos os offsets de instrução dos cinco métodos foram alcançáveis na CFG normal, sem saltos a posições inválidas.** O scanner não modela exceções, estados de pilha para todos os opcodes ou efeitos no mundo. Portanto, a topologia normal não constitui garantia transacional, nem comprova que a instância carregada pela ModLauncher possua os mesmos Code SHAs.

### 2.1. O cancelamento do evento tem retorno falso no recorte distribuído

Em `PersistentEntitySectionManager.addEntity(EntityAccess,Z):Z`, o [dossiê de chamadas anterior](EXACT-GALENA-DISTRIBUTED-SPAWN-21.1.248.md) identificou `EntityJoinLevelEvent.isCanceled():Z` @**36**. A auditoria nova identifica `ifeq` @**39**: quando a condição é falsa, o fluxo salta a **44**; a continuação local alternativa passa por **42**, `iconst_0` e `ireturn` @**43**. O caminho sem cancelamento encaminha-se a `addEntityWithoutEvent(...):Z` @**47** e retorna seu booleano em `ireturn` @**50**.

A verificação é **sobre o comportamento declarado nos classfiles oficiais distribuídos**, sem alegar cancelamento efetivamente executado para `MagneticWeaponEntity`.

### 2.2. A recusa é convertida em `false` em `ServerLevel.addEntity`

A invocação tipada `entityManager.addNewEntity(...):Z` aparece @**32**. O `ifeq` @**35** salta para **44** no caminho falso, que termina em `ireturn` @**45** precedido de `iconst_0`. A rota verdadeira segue a **38**, solicita `Entity.onAddedToLevel()` @**39** e retorna `iconst_1` por `ireturn` @**43**. Há também retorno precoce `false` @**26** relacionado a uma guarda anterior @**4**, cujo gatilho completo deve ser examinado quando necessário; não atribuir todas as recusas ao evento.

`ServerLevel.addFreshEntity(Entity):Z` chama `ServerLevel.addEntity(Entity):Z` @**2** e faz `ireturn` @**5**, imediatamente depois da invocação. `PersistentEntitySectionManager.addNewEntity(EntityAccess):Z` chama `addEntity(EntityAccess,Z):Z` @**3** e faz `ireturn` @**6**. **Esses dois wrappers não possuem branches locais** no Code exato observado.

Assim, no caminho de retorno normal dessa versão **distribuída**, a recusa produz uma saída booleana falsa propagável até `Level.addFreshEntity`, enquanto o caminho aceito solicita o callback de inclusão. Não há prova correspondente de compensação do `ItemStack` da Galena.

### 2.3. Recusas independentes do evento

O método distribuído `PersistentEntitySectionManager.addEntityWithoutEvent(EntityAccess,Z):Z` possui **quatro** branches @5, @55, @84 e @97. Há retorno com `iconst_0` @**9** e retorno com `iconst_1` @**106**. O simples fato de existirem dois resultados impede atribuir todos os falsos a `EntityJoinLevelEvent`. Os detalhes de guardas e da aceitação efetiva de UUID, se relevantes, requerem prova de operandos e chamadas adicionais; não atribuir condição concreta por aproximação.

## 3. Galena: a consequência sobre a arma ainda não foi demonstrada

A evidência publisher 1.0.10 já registra que `GalenaGauntletItem.onUseTick` solicita `ItemStack.setCount(0)` na stack oposta antes de `ACCompat.createEntity` e `Level.addFreshEntity`, descartando seu booleano. A evidência desta etapa acrescenta que **uma recusa de entrada no recorte distribuído pode percorrer uma cadeia de retornos `false`** sem que o resultado seja tratado por esse consumidor.

Isso **não é reprodução de perda de item**: não foram executados cancelamento por mod de proteção, conflito de UUID, criação nula, inventário cheio, restituição, owner, reload, troca de dimensão ou sincronização cliente/servidor. Também não comprova se mixins e outros mods mudam a rota final. Essa incerteza é bloqueante para efeitos mutadores, XP, Mastery e perks de captura/retorno da arma.

**Invariantes:** Black Arcana detém autoridade do runtime mágico e `WorldEffectPolicy`. RPG Skill Tree permanece sibling para progressão, atributos, Mastery/perks apenas via boundary de efeito concluído, deduplicado e autorizado. Sem comprovação de transação e hook: `NO_MUTATION`, *fail-closed*.

## 4. Reprodução, critérios de certificação e próximos testes

```sh
python3 docs/qa/alexscaves_1010_galena_211248_spawn_return_cfg_probe.py \
  --server /caminho/neoforge-21.1.248-server.jar \
  --srg /caminho/server-1.21.1-20240808.144430-srg.jar \
  --javap /caminho/java21/bin/javap \
  --output /novo-diretorio/report.json

python3 docs/qa/alexscaves_1010_galena_211248_spawn_return_cfg_checks.py \
  --report /novo-diretorio/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-SPAWN-RETURN-CFG-21.1.248.json' \
  --parent 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-DISTRIBUTED-SPAWN-21.1.248.json' \
  --adversarial
```

**Bloqueios externos:** provar o bytecode *pós*-ModLauncher da mesma build de instalação; identificar todos os listeners que podem cancelar o evento no modpack; executar cenários normal/cancelado/UUID duplicado/entidade removida e verificar aceite de spawn, estado da stack, drops, persistência, reload, world protection e segurança transacional. Só com essa evidência poderá haver proposta de hook mutador ou atualização de estados.

**Estado individual:** Galena Gauntlet ⚠️ parcial, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. **Não alterar contadores**: Alex's Caves **130/134** certificados estáticos do universo observado, global **269/2.446**, providers integralmente catalogados **4/164**, providers integralmente perk-ready **0/164**.
