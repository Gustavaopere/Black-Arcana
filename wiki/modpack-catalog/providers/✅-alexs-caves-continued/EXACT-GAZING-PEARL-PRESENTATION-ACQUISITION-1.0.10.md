# Gazing Pearl — aquisição declarativa e fronteira de apresentação (publisher 1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Alex's Caves Continued 1.0.10, modlist física #019, Minecraft 1.21.1 / Java 21. Publisher SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Não comparado a novo dump instalado.

## Evidência anterior reutilizada

[Run 44936198921, job 136943226304](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44936198921/job/136943226304), relatório SHA-256 `d73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5`, [manifesto](EXACT-GAZING-PEARL-DISCOVERY-1.0.10.json). O censo anterior identificou três owners que referenciam o tipo GazingPearlItem (ClientProxy, ACItemRegistry e próprio). A receita filename-matched consome a pérola (Gazing Pearl + Marine Snow → Pearl), não comprova sua aquisição inicial. O getPearlColor já tem fórmula própria auditada. O tooltip chama DeepOneReaction.fromReputation @32, name @39, Locale.ROOT @42, toLowerCase @45, concat bootstrap @48 e Component.translatable @58; a chave completa ainda precisa do argumento BootstrapMethods. Não repetir as provas de persistência nem transferir efeitos da IA à pérola.

## Nova coleta delimitada

[Sonda](../../../../docs/qa/alexscaves_1010_gazing_pearl_presentation_probe.py) e [CI](../../../../.github/workflows/alexscaves-1010-gazing-pearl-presentation.yml): classfile GazingPearlItem e digest do tooltip fixados. Censo dos 1.555 classfiles por referências tipadas ao tipo e ao campo ACItemRegistry.GAZING_PEARL, incluindo cadeia de handles locais de bootstrap. Para corpos grandes, somente janelas ao redor de sites e digest integral; não afirmar CFG completo. Para corpos pequenos selecionados, projeção integral. O scanner de recursos verifica chaves/valores JSON exatos e distingue referência em data de chave de tradução; registra hashes, erros de parse e limites. Não tratar contagem de hits como drop rate nem provar recursos efetivos, geração dinâmica ou outras mods. Chaves de tooltip são derivadas da concatenação JVM e das quatro categorias conhecidas; não supor prefixo por convenção. A prova de registry é estática, sem executar registro ou cliente.

Primeiro replay e revisão do conteúdo pendentes. Sem novo certificado, hook, alteração de índices, nova raiz ou QA física. [Ficha](items/gazing-pearl.md). Não conceder Mastery por renderização, leitura, receita ou referência ao UUID.

## Resultado do replay e selo

[Run 45544536346, job 138970844483](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45544536346/job/138970844483), HEAD `239d7189eba843aab6e8269d30f46019062e6cc7`: três self-checks, dois relatórios byte a byte iguais, 163.013 bytes, SHA-256 `258579e263ef54487b374c67cd6157180af2281608725f20963f84026df7000e`. O workflow consolidado fixa tamanho e hash; sua nova execução é gate distinto. Censo de 1.555 classfiles, quatro owners candidatos e nove projeções, duas delas janelas de métodos grandes, sem alegar CFG integral dessas duas.

### Registro, tooltip e cor

- ACItemRegistry.<clinit>: literal gazing_pearl @1973, bootstrap 111 @1976 para lambda$static$104, register @1981, putstatic GAZING_PEARL @1984. Factory Code SHA `9868e34dbf3a04069b519c24047b9a3f461dc7ad514f62323ac120ff232a3dfa`, instruction SHA `70ebd3ce11f335078507bcdbb0ae3aaa78e1e68e821852af72c68345ef11b116`, new @0. Creative tab lambda$static$14 Code SHA `af594c86ba85f8f91b86614d79bd0a7cf814f03ed32e83f12b1a88b96bcc2290`: GAZING_PEARL @421, Supplier.get @424, add @432. Não equivale a disponibilidade efetiva no pack.
- Tooltip appendHoverText: bootstrap StringConcatFactory @48 contém template literal item.alexscaves.gazing_pearl.desc_ seguido do marcador de argumento U+0001. Chaves exatas: item.alexscaves.gazing_pearl.desc_aggressive, desc_stalking, desc_neutral, desc_helpful (mesmo prefixo). O relatório identifica 13 arquivos de idioma, incluindo pt_br, com chave de nome e as quatro descrições. Não pressupor idioma ativo ou conteúdo alterado por resource pack.
- ClientProxy.commonInit Code SHA `735c1d4a3a8be3cb24ff29048a245c39e60ca1530fa0613d7dd2d2557985bf3e`: event bus @6, handle onItemColors @12, addListener @17. onItemColors Code SHA `3249fa89f491fcb3d7e484ad238786a747b0d8b72cda962c143ad829d3de137d`: bootstrap 183 @66 para lambda$onItemColors$21, GAZING_PEARL @77, supplier @80, register @89. Lambda Code SHA `c4d93fe646b83344f9e934b3a33568dcf04b3b4ce761c55dd3ed2745527223eb`: tintIndex !=0 retorna -1; tintIndex 0 chama getPearlColor @9 e ACColors.opaque(I)I @12. O corpo de opaque não consta desta seleção; não inferir transformação de bits. Registro observado estaticamente, não render físico.

### Aquisição declarativa e limites do censo

| Recurso (namespace alexscaves) | Evidência |
|---|---|
| data/alexscaves/loot_table/gameplay/deep_one_barter.json | 4.500 bytes; SHA `eb208ca3660daed76aaf13dfeba2cdef15bbce90ae3d2c235ecb63a4480042ac`; pool 0, entry 14, item gazing_pearl, peso 26, soma declarada 646, rolls 1; sem condição, quality ou função de count nessa entrada. Não é probabilidade efetiva nem prova do consumidor da troca. |
| data/alexscaves/advancement/alexscaves/deep_one_items.json | 1.730 bytes; SHA `20b9fb23f3c89f404849ab1291aa2b18f08f639f41cc3ae826f0443ad36939d9`; critério gazing_pearl, trigger minecraft:inventory_changed, condição items contém ID exato; parent alexscaves:alexscaves/deep_ones_become_helpful; quatro critérios, requirements não explicitado. Sem prova de concessão. |
| data/alexscaves/recipe/pearl_from_gazing_pearl.json | 282 bytes; SHA `663ecb4f1b80e92a251e541e6a9b2c312efecccfd322f959d81ecc2e8b4e14d2`; consome Gazing Pearl, não é receita de obtenção dela. |

Varredura: 3.434 caminhos JSON, 3.441.429 bytes, 16 arquivos com hits (13 lang e 3 data). 3.433 analisáveis; 1 rejeição pelo parser estrito (chave duplicada) em assets/alexscaves/models/block/thornwood_door_top_left_open.json, sem relação causal estabelecida com a pérola. Não declarar censo completo de recursos sem ressalva, nem interpretar keys de idioma como loot. Sem QA física, certificado individual novo, hook ou mudança de índice. NO_MUTATION.
