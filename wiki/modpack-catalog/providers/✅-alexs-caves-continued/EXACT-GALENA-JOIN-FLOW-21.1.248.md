# Galena Gauntlet — fluxo causal declarado pelos patches Entity Join (NeoForge 21.1.248)

**Estado:** ⚠️ **subcontrato de controle de fluxo estático, read-only, limitado ao código de patch `userdev` oficial**. Não certifica a execução do Minecraft transformado, aceitação de `MagneticWeaponEntity`, restituição da stack, mutating hook ou QA física. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false`.

## 1. Proveniência verificável

A [ABI-alvo NeoForge 21.1.248](EXACT-GALENA-ENTITY-JOIN-ABI-21.1.248.md) certifica somente as assinaturas externas de `EntityJoinLevelEvent`; a [auditoria de patches 21.1.248](EXACT-GALENA-ENTITY-JOIN-PATCHES-21.1.248.md) localizou o uso do evento e o cancelamento. Esta etapa avança **apenas a estrutura local de decisões e callbacks**, no mesmo JAR fixado, sem inferir funcionamento do modpack.

- **Engine-alvo de compilação:** Minecraft **1.21.1**, NeoForge **21.1.248**, Java **21**. Conferência anterior: `neo_version=21.1.248` nos `gradle.properties` da Black Arcana e do sibling RPG Skill Tree.
- **Artefato oficial:** `neoforge-21.1.248-userdev.jar`, **3.983.248 bytes**, SHA-256 `9278d08154a82927391ed5257481f56d6d0fcb147822c6a79ec9b5129799e79a`, SHA conferido com [Maven NeoForge](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.248/neoforge-21.1.248-userdev.jar). O JAR efetivo instalado/transformado permanece **NÃO VERIFICADO**.
- **Provider Galena:** Alex's Caves Continued **1.0.10**; JAR publisher SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, modlist sibling SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Nova comparação de dump físico **NÃO VERIFICADA**.
- **Patch `ServerLevel.java.patch`:** SHA-256 `d9dc7428b5467f35b42e9f972b3eb9079312e660755b77b6be1f880ed88e6249`.
- **Patch `PersistentEntitySectionManager.java.patch`:** SHA-256 `a2a5ef2bdbf3fec5b7db2f7cc4674338358011b3b738622a7f180faeeb2a56a0`.
- **Descoberta inicial concluída:** [workflow #45208324051](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45208324051), job `137810026496`, HEAD `75f565da91bb88b9b0ebfa223335a2967306a5a2`.
- **Relatório canônico de observação:** `report.json`, **8.996 bytes**, SHA-256 `39605a4b034b7e43cc301111b4d7352aad67b5a1dd4cc78cefc6b9f8b31bcce7`. Os [marcadores](EXACT-GALENA-JOIN-FLOW-21.1.248.json) não incluem implementação de terceiros: somente papel, tipo ADD/CONTEXT, linha, hunk, tamanho, SHA de linha e classificações estruturais.
- [Sonda](../../../../docs/qa/alexscaves_1010_galena_neoforge_211248_join_flow_probe.py) · [verificador adversarial](../../../../docs/qa/alexscaves_1010_galena_neoforge_211248_join_flow_checks.py) · [workflow exato](../../../../.github/workflows/alexscaves-1010-galena-neoforge-211248-join-flow.yml). **Os gates do verificador adicionados após a primeira descoberta precisam ser comprovados na HEAD final antes do merge**.

## 2. Classificações comprovadas no patch upstream exato

### A. `ServerLevel`: jogadores e entidades ordinárias têm tratamentos distintos

**Rota especial de `addPlayer(ServerPlayer)`:**

1. O método declara uma verificação de `EntityJoinLevelEvent` **antes** de sua solicitação de registro; o caminho cancelado tem um retorno de método **`void`**.
2. A inclusão de jogador no manager usa a superfície **`addNewEntityWithoutEvent`**. O nome e a ordem local deixam explícita a intenção de evitar nova emissão nesse trecho, mas não excluem todos os mecanismos de evento do runtime.
3. A solicitação de `onAddedToLevel()` aparece depois do registro especial no patch.

**Rota de `addEntity(Entity)` ordinária:**

1. O patch introduz uma condicional sobre o retorno booleano de `entityManager.addNewEntity`.
2. Somente no ramo verdadeiro da condicional o trecho chama `onAddedToLevel` e retorna `true`. O outro ramo retorna `false`.
3. O código inteiro de `Level.addFreshEntity` e os transformers externos **não** são inspecionados nesta prova. A existência de um `false` na rota `addEntity` não demonstra, isoladamente, que o consumidor Galena receba esse valor no caso concreto.

**Distinção essencial:** a linha `EntityJoinLevelEvent` localizada em `ServerLevel` é a do caminho específico para **jogadores**. A emissão genérica de entidade relevante para avaliar uma arma projetada deve ser investigada na fronteira do **manager**, não atribuída automaticamente ao `addPlayer`.

### B. `PersistentEntitySectionManager`: recusa antes de registrar UUID

O patch distingue a função de admissão `addEntity(T,boolean)` da rotina `addEntityWithoutEvent(T,boolean)`. A primeira verifica `instanceof Entity`, publica `EntityJoinLevelEvent` e, quando `isCanceled`, declara retorno **`false`**. O encaminhamento para `addEntityWithoutEvent` aparece **depois** dessa condição. A checagem `addEntityUuid` aparece no trecho da rotina de registro, após a condição de cancelamento.

A separação estabelece a seguinte **relação de ordem no patch**: *testar evento cancelável → eventualmente recusar com boolean false → caso não recusado, solicitar registro/checagem de UUID*. Não comprova a ausência de outros consumidores, efeitos antecipados no provider ou comportamento após falha no mundo.

### C. Três rotas de carregamento e callback de inclusão

A sonda verificou no patch três rotas que solicitam a admissão e, na linha imediatamente seguinte adicionada, invocam `onAddedToLevel` sem conferir explicitamente o resultado booleano daquela solicitação:

| Rota | Parâmetro de loaded-from-disk na solicitação | Checagem do retorno no fragmento |
|---|---|---|
| `addLegacyChunkEntities` | `true` | **Não** |
| `addWorldGenChunkEntities` | `false` | **Não** |
| `processPendingLoads` | `true` | **Não** |

**Risco hipotético a testar:** em um cenário em que um listener cancele a admissão durante uma dessas rotas, o callback de inclusão pode ser solicitado sem registro aceito. Isso é uma hipótese baseada no trecho de patch, sem comprovação de execução, consequência física, frequência, persistência ou alcance na Galena Gauntlet. Não declarar bug, exploit ou correção necessária.

O registro inclui **16 âncoras de métodos/decisões** (9 de `ServerLevel` e 7 do manager), além de 9 âncoras de três caminhos de carregamento. Elas são **componentes técnicos de um único recorte**, não 25 novas magias, efeitos ou contratos estáticos individuais.

## 3. Impacto e limites para Galena Gauntlet

A prova publisher 1.0.10 já demonstra a **ordem local de solicitação**: `GalenaGauntletItem.onUseTick` zera a stack da arma oposta antes de `ACCompat.createEntity` e de `Level.addFreshEntity`, ignorando o booleano deste último. Os novos patches ajudam a formular um **caminho causal de risco**, porém permanece sem verificação a premissa de que a entidade específica seja aceita/recusada pelo caminho demonstrado, que qualquer cancelamento aconteça na instância, ou que uma arma efetivamente desapareça sem restituição.

Não derivar daí um hook mutador. Em particular, não reverter `setCount(0)` por evento sem transação comprovada, pois cancelamentos em outros mods, autoridade de inventário, tracking, reload, sincronização e deduplicação continuam desconhecidos.

**Black Arcana** conserva autoridade do runtime mágico e da `WorldEffectPolicy`; o sibling **RPG Skill Tree** somente pode receber progresso, atributos, Mastery e perks a partir de boundary server-owned autorizado e de efeito consumado. Publicação de evento, pedido de spawn ou simples registro de UUID **não** equivalem a conclusão de cast ou concessão de XP.

## 4. Reprodução e pendências

```sh
python3 docs/qa/alexscaves_1010_galena_neoforge_211248_join_flow_probe.py \
  --userdev /caminho/neoforge-21.1.248-userdev.jar \
  --output /diretorio-novo/report.json

python3 docs/qa/alexscaves_1010_galena_neoforge_211248_join_flow_checks.py \
  --report /diretorio-novo/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-JOIN-FLOW-21.1.248.json' \
  --adversarial
```

Pendências técnicas bloqueantes: (a) rastrear o método final transformado `Level.addFreshEntity` e sua relação com `ServerLevel.addEntity` / `PersistentEntitySectionManager.addEntity`; (b) demonstrar se `MagneticWeaponEntity` atravessa essa rota no alvo real; (c) auditar tratamento de cancelamento, UUID, owner, integridade da stack, drops, inventário, reload e world protection; (d) testes físicos em servidor dedicado/modpack sob D035/Stage 09 quando aplicáveis; (e) comprovar qualquer extensão segura antes de propor perks. Sem esses testes: `NO_MUTATION`.

**Índices/contadores preservados:** Galena ⚠️ parcial; Alex's Caves **130/134** certificados estáticos do universo observado (4 pendentes); global **269/2.446** objetos observados certificados, **4/164** providers com catálogo documental encerrado, **0/164** integralmente perk-ready. Nova evidência de infraestrutura não altera esses valores nem encerra o universo integral.
