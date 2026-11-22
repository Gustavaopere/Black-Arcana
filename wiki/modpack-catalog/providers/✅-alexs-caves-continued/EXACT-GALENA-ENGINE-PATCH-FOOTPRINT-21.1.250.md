# Galena Gauntlet — fronteira de patches NBT do NeoForge 21.1.250 (Minecraft 1.21.1)

**Estado:** ⚠️ recorte **estático limitado ao artefato oficial `userdev`**, sem reconstrução de métodos vanilla ou execução do cliente/servidor transformado. Não certifica o contrato completo da Galena Gauntlet, a persistência real, a viabilidade de hooks, nem os resultados de gameplay. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false`.

## 1. Proveniência e limites do universo inspecionado

- **Caller/provider:** Alex's Caves Continued `alexscaves` **1.0.10** (Minecraft 1.21.1/NeoForge/Java 21), nome registrado na modlist física sibling `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. JAR publisher lido na auditoria anterior: 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A paridade de um novo dump da instância continua `NOT_VERIFIED`.
- **Elo imediatamente anterior:** [10 corpos de `ACCompat` e 17 chamadas tipadas](EXACT-GALENA-ACCOMPAT-HELPERS-1.0.10.md), relatório original SHA-256 `ca395f3418979d8302363cf9db8d54c620572b16ebdc2ecacee5014fce0add64`. Eles encaminham `saveStack` a `ItemStack.save`, `loadStack` a `ItemStack.parse` e delegam tags customizadas a `CustomData.copyTag/of`.
- **Fonte atual:** artefato **oficial NeoForge 21.1.250** `neoforge-21.1.250-userdev.jar`, 3.983.248 bytes, SHA-1 `45f4a0daf3ecd5864338cb5ab7368afbee02e529`, SHA-256 `deb6dd1e002aa85406e92501f49d5429cc8eaefe32fc353433e67030c32d8372`, obtido de [Maven NeoForged](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.250/neoforge-21.1.250-userdev.jar). Versão já pinada no contrato de referência de eventos de item do mesmo catálogo; não equivale ao runtime instalado transformado.
- **Censo:** 963 entradas ZIP, 753 caminhos `patches/net/minecraft/**/*.java.patch`, SHA-256 do roster lexicalmente ordenado `22046c708c5774e479f335fcef95a0c526670fbc9dde01fc29281c94102a640f`.
- **Evidência reproduzida:** `patch-report.json`, **10.185 bytes**, SHA-256 `7cb488b63c2abafcf17c839661ac7ff05a367fca84c497c174dea5017ded6411`, produzido pelo workflow [#45078806235](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45078806235), artefato #14776063917. A sonda foi executada sobre os bytes do `userdev` SHA-exato. Este report inclui **somente hashes, números de linha, tokens e classificações dos diffs**, não conteúdo original de patches.

## 2. Três arquivos procurados e suas disposições

| Alvo da cadeia NBT | Disposição no artefato oficial | Evidência |
|---|---|---|
| `patches/net/minecraft/world/item/ItemStack.java.patch` | **Presente:** 20 hunks, 264 linhas, 12.326 bytes | SHA-256 `5e910db862cc11662067e5ffbd2a792197d2eb618ce76f4281ee6fb5998c8c7d`; **25 linhas** correspondentes a tokens do filtro (3 `ADD`, 6 `DELETE`, 16 `CONTEXT`) |
| `patches/net/minecraft/world/item/component/CustomData.java.patch` | **Ausente no roster de patches do userdev** | Ausência do **arquivo de patch específico**, não da classe, do bytecode, dos métodos, de modificações por outros mecanismos ou da implementação vanilla |
| `patches/net/minecraft/nbt/CompoundTag.java.patch` | **Presente:** 3 hunks, 50 linhas, 2.018 bytes | SHA-256 `6d4eb62dc6dddb7dd58b02fc1dfe5e76e6ca4634c5ae03bed2875a05c69abe02`; **4 linhas** pertinentes (1 `ADD`, 0 `DELETE`, 3 `CONTEXT`) |

Na patch de `ItemStack`, o filtro de palavras completas encontrou referências a `codec`, `encode`, `components`, `DataComponents` e `set`. A ocorrência em linhas `ADD`/`DELETE` demonstra **mudanças do patch nesse trecho**, não demonstra que `ItemStack.save` ou `ItemStack.parse` usem necessariamente essas janelas. **Não houve correspondência literal isolada para `parse` nem `save` nas 25 linhas de patch selecionadas.** Esse resultado também não demonstra que tais métodos não existam ou não possam ter sido alterados indiretamente.

Na patch de `CompoundTag`, as quatro linhas selecionadas contêm apenas o token `CompoundTag`. Uma linha `ADD` com esse token, por si só, não demonstra semântica de `getUUID`, `putUUID`, `hasUUID` ou `getCompound`. O dossiê não atribui a essas rotinas validação ou fallback não observado.

## 3. Integração com os wrappers de Galena e limitações de segurança

**`saveStack`/`loadStack`:** o contrato SHA-exato de `ACCompat` verifica **invocações de** `ItemStack.save` e `ItemStack.parse`, respectivamente, e o fallback local `Optional.orElse(ItemStack.EMPTY)` quando `parse` devolve `Optional.empty`. Este recorte de patches **não** confirma os corpos internos de `save/parse`, comportamento de codecs, falha/erro no parsing, persistência de componentes nem recuperação após restart. Nenhum teste read-only dos patches substitui execução sobre a engine efetivamente transformada.

**`getTag`/`getOrCreateTag`/`setTag`:** no wrapper `ACCompat`, `getTag` pode devolver `null` e `getOrCreateTag` prepara cópia/novo `CompoundTag`; somente `setTag` solicita atualização do `DataComponents.CUSTOM_DATA`. A ausência de `CustomData.java.patch` no `userdev` não prova ausência de transformações externas, nem semântica de cópia profunda, ownership, serialização ou replicação de `CustomData.copyTag/of`. Testar equivalência de objetos, mudanças in-place, `ItemStack.set/remove` e ciclo save/reload na instância permanece necessário.

**`ControllerUUID`:** a chamada ao `CompoundTag` passa pelo helper do provider; o resultado do censo de patch não valida UUID contra entidades presentes ou jogadores autenticados. Os consumidores de controller por UUID e ID sincronizado continuam cobertos apenas pelos recortes estáticos já publicados, não por QA física.

**Mastery/perks/world safety:** nenhuma patch verificada fornece autorização para hook mutador ou um evento de ação consumada. Sem confirmar o estado final servidor-autorativo e deduplicado, não contabilizar progressão por leitura de NBT, presença de UUID, envio de stack ou simples pedido de mineração. Qualquer efeito novo criado **pelo Black Arcana** continua sujeito à sua `WorldEffectPolicy` e às decisões D006–D009; não declarar bypass do provider sem prova.

## 4. Como reproduzir e certificar apenas a fronteira de patch

A execução no GitHub baixa o mesmo `userdev` oficial, verifica tamanho/SHA-256, faz a varredura de 753 patches, confere os caminhos e hashes de `ItemStack`/`CompoundTag`, reconstitui o report fixado e executa o teste adversarial.

```sh
python3 docs/qa/alexscaves_1010_galena_engine_patch_probe.py --selftest
python3 docs/qa/alexscaves_1010_galena_engine_patch_probe.py \
  --userdev /caminho/neoforge-21.1.250-userdev.jar \
  --output /diretorio-novo/patch-report.json
python3 docs/qa/alexscaves_1010_galena_engine_patch_checks.py \
  --report /diretorio-novo/patch-report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-ENGINE-PATCH-FOOTPRINT-21.1.250.json' --adversarial
```

O [manifesto](EXACT-GALENA-ENGINE-PATCH-FOOTPRINT-21.1.250.json) fixa todos os 29 registros de linha pertinentes e as três disposições de arquivo. O [verificador](../../../../docs/qa/alexscaves_1010_galena_engine_patch_checks.py) exige a identidade oficial e **37 alterações report-only adversariais** rejeitadas mesmo dispensando apenas o digest externo do relatório na simulação. A [CI dedicada](../../../../.github/workflows/alexscaves-1010-galena-engine-patch-footprint.yml) é um gate estático, não uma execução de gameplay. Os resultados devem sempre ser associados à **HEAD final** da PR; CI de versões preliminares não substitui esse gate.

## 5. Pendências antes de qualquer certificação adicional

1. Localizar e verificar **corpos realmente executados** de `ItemStack.save`, `ItemStack.parse`, `CustomData.copyTag`, `CustomData.of` e `CompoundTag` na versão exata de Minecraft/NeoForge após os patches/transformações relevantes; o `userdev` de patches não os fornece completos.
2. Confrontar o JAR do mod efetivamente presente na instância com o publisher e auditar mixins/configurações/datapacks opcionais que alteram serialização ou inventário.
3. Testar save/reload/restart, falha de parse, mudança de dimensão/logout, falha de spawn/retorno da arma, serialização com componentes e rollback com observação física real, inclusive deduplicação e integridade dos itens.
4. Só avaliar hooks server-owned após comprovação de causalidade, aceitação do efeito e segurança de mundo; até lá, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `static_contract=NOT_CERTIFIED`.

**Limite formal:** este documento certifica **somente o fingerprint da fronteira de patches upstream**. Não aumenta numeradores de fichas estáticas completas, não fecha o universo de Alex's Caves e não adiciona roots semânticas.
