# Magic From The East 1.1.5 — fonte da release e limites da prova

Auditoria de 27/10/2026. A identidade das **22 spells** continua `COUNTED_EXACT` conforme a [auditoria binária anterior](EXACT-BINARY-SPELLS-1.1.5.md). A referência para estudar seus parâmetros passa a ser **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, classificada `RELEASE_BOUNDED_SOURCE`. Não há comprovação de equivalência integral entre essa árvore e os métodos do JAR.

## Artefato e cronologia

| Evidência | Valor e alcance |
|---|---|
| Release pública | [CurseForge 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), projeto `1224162` |
| Metadados oficiais consultados | [API do arquivo](https://www.curseforge.com/api/v1/mods/1224162/files/7385201): criação `2025-12-27T17:17:39.317Z`, modificação `2025-12-27T17:25:31.43Z` |
| Arquivo publicado pelo autor | `iss_magicfromtheeast-1.1.5.jar`, **1680780 bytes** |
| SHA-1 revalidado localmente | `e3552ea6b7b32b843c48bf0d857237d4b7129ab0` |
| SHA-256 revalidado localmente | `e5ab22492b300d8f5e797f3f9d196e1e06f4a4a1db3650ac5a5979e6956e4920` |
| Relação com o pack | SHA-1 igual ao registro histórico da modlist física **#346**; o perfil original não foi medido novamente |
| Commit candidato | [f2a095c](https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/commit/f2a095cbbc89f8d8428dca758140663adf54ae88), autor e committer em `2025-12-27T16:35:34Z`, anterior à criação do arquivo público |
| Versões declaradas pela fonte | [MC 1.21.1, mod 1.1.5, NeoForge 21.1.187, Iron’s 3.14.8, GeckoLib 4.7.5.1, Curios 9.2.2][versions] |
| Pack usado como referência | NeoForge **21.1.250**, Iron’s **3.16.3**; compatibilidade de execução e configuração implantada continuam pendentes |

Datas de commit, nome de versão e timestamps ZIP restringem candidatos; não autenticam o código de cada método. A fonte de agosto de 2026 `13208302c9fdf5beb171a328558cbef07a25ba46`, embora também declare `1.1.5`, é posterior à publicação e possui diferenças relevantes. O candidato intermediário `904a011b04cc33c45b5c4c79f97e2f7345ebeffb`, de 14/12/2025, também antecede mudanças já presentes no JAR. Nenhum dos dois deve continuar como referência geral do comportamento instalado.

## Confrontos binários delimitados

Inspeção local com **JDK 21, `javap -c -p`**, no arquivo cujo hash consta acima. Foram examinados literais, campos, instruções e referências de chamadas; não foi incorporada uma implementação de terceiros. Os resultados abaixo não afirmam que todos os métodos de uma classe sejam iguais à fonte candidata.

| Classe / método | Fato observado no JAR SHA-exato | Consequência documental |
|---|---|---|
| [`CloudRideSpell#getRecastCount`, `#onCast`, `#getEmptyCastData`, `#onRecastFinished`][cloud-paths] | Retorno de recasts **2**; referências a `hasRecastForSpell`, `SummonManager.initSummon`, `addRecast`, `SummonedEntitiesCastData` e encerramento pelo helper de summon | Esses caminhos estão em f2a095c e não constam de 904a011b. Não descrever Cloud Ride como cast sem recast a partir da fonte antiga |
| `DrapesOfReflectionSpell` [construtor][drapes-fields] e [`#getDrapesHP`][drapes-hp] | Base de power **2**, incremento por nível **1**, HP calculado com **1 + P** | Corrobora os campos correspondentes em f2a095c; 904a011b tinha **3**, **4** e **4 + P** |
| `SwordDanceSpell` [configuração][sword-config] e [`#onCast`][sword-cast] | Cooldown default **90.0 s**; condição de silêncio com resto da divisão por **3**; retorno de `getSpeed` descartado | Não importar o cooldown **40 s** e o teste de índices pares da fonte posterior |
| [`MFTESchoolRegistries` inicializador][school-init] | Três chamadas de `registerSchool`, com atribuições `SYMMETRY`, `SPIRIT` e **`DUNE`**; a última chamada ocorre no offset **170**, seguida da atribuição de `DUNE` no **173** | A escola Dune está declarada no JAR. Isso não cria uma spell Dune dentro das 22 inscrições comprovadas |

O source f2a095c também mostra `impermanencePercentLimit=0.2`, `cloud_bless` e sua associação a `SAFE_FALL_DISTANCE`. Esses fatos da **fonte** não recebem prova binária apenas por aparecerem na mesma tabela de auditoria: consultar o alcance específico na ficha correspondente. A fonte posterior altera, entre outros pontos, Bone Hands, Kitsune e Soulburn; suas regras não podem ser combinadas silenciosamente com a fonte candidata.

## Como reproduzir os confrontos

Obter o arquivo na publicação acima e conferir tamanho/SHA-1/SHA-256 antes de inspecioná-lo. Com JDK 21, executar `javap -classpath <JAR-verificado> -c -p <classe-completa>` para as quatro classes listadas. O prefixo das classes de spell é `net.warphan.iss_magicfromtheeast.spells.symmetry.`; o registry usa `net.warphan.iss_magicfromtheeast.registries.MFTESchoolRegistries`. Comparar somente os campos e métodos indicados contra os permalinks da fonte candidata e preservar as divergências. Reproduzir o inventário completo de IDs exige o procedimento separado da [auditoria de registros](EXACT-BINARY-SPELLS-1.1.5.md).

## Efeito sobre os contadores e a integração

Este lote reconcilia e aprofunda as **22 fichas existentes**. **+0 identidades semânticas, +0 certificados no manifesto estrito**. Uma ficha source-causal revisada não passa automaticamente a ✅. Os índices de certificação permanecem independentes da cobertura editorial; o universo de atributos, equipamentos, sistemas e demais objetos integráveis do provider segue aberto.

O [contrato comum](SPELL-PERK-BOUNDARIES-1.1.5.md) distingue observação, mutação do evento, atributos nativos e ausência de hook. Todas as integrações por perks e a validação em servidor/cliente/Survival continuam condicionadas. Não houve alteração do runtime, dependências ou Stage do Black Arcana, RPG Skill Tree ou Enshrouded.

Consulta factual, paráfrases e referências imutáveis. A [licença do mod][metadata] declara **All Rights Reserved**; a licença do template não deve ser estendida à implementação, textos ou assets do mod.

[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L10-L36
[metadata]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/META-INF/neoforge.mods.toml#L1-L14
[cloud-paths]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/CloudRideSpell.java#L67-L101
[drapes-fields]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/DrapesOfReflectionSpell.java#L38-L43
[drapes-hp]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/DrapesOfReflectionSpell.java#L72-L73
[sword-config]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/SwordDanceSpell.java#L33-L38
[sword-cast]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/SwordDanceSpell.java#L69-L85
[school-init]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESchoolRegistries.java#L32-L64
