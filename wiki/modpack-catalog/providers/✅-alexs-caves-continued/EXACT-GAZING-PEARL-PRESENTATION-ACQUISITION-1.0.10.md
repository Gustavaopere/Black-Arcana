# Gazing Pearl — aquisição declarativa e fronteira de apresentação (publisher 1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Alex's Caves Continued 1.0.10, modlist física #019, Minecraft 1.21.1 / Java 21. Publisher SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Não comparado a novo dump instalado.

## Evidência anterior reutilizada

[Run 44936198921, job 136943226304](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44936198921/job/136943226304), relatório SHA-256 `d73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5`, [manifesto](EXACT-GAZING-PEARL-DISCOVERY-1.0.10.json). O censo anterior identificou três owners que referenciam o tipo GazingPearlItem (ClientProxy, ACItemRegistry e próprio). A receita filename-matched consome a pérola (Gazing Pearl + Marine Snow → Pearl), não comprova sua aquisição inicial. O getPearlColor já tem fórmula própria auditada. O tooltip chama DeepOneReaction.fromReputation @32, name @39, Locale.ROOT @42, toLowerCase @45, concat bootstrap @48 e Component.translatable @58; a chave completa ainda precisa do argumento BootstrapMethods. Não repetir as provas de persistência nem transferir efeitos da IA à pérola.

## Nova coleta delimitada

[Sonda](../../../../docs/qa/alexscaves_1010_gazing_pearl_presentation_probe.py) e [CI](../../../../.github/workflows/alexscaves-1010-gazing-pearl-presentation.yml): classfile GazingPearlItem e digest do tooltip fixados. Censo dos 1.555 classfiles por referências tipadas ao tipo e ao campo ACItemRegistry.GAZING_PEARL, incluindo cadeia de handles locais de bootstrap. Para corpos grandes, somente janelas ao redor de sites e digest integral; não afirmar CFG completo. Para corpos pequenos selecionados, projeção integral. O scanner de recursos verifica chaves/valores JSON exatos e distingue referência em data de chave de tradução; registra hashes, erros de parse e limites. Não tratar contagem de hits como drop rate nem provar recursos efetivos, geração dinâmica ou outras mods. Chaves de tooltip são derivadas da concatenação JVM e das quatro categorias conhecidas; não supor prefixo por convenção. A prova de registry é estática, sem executar registro ou cliente.

Primeiro replay e revisão do conteúdo pendentes. Sem novo certificado, hook, alteração de índices, nova raiz ou QA física. [Ficha](items/gazing-pearl.md). Não conceder Mastery por renderização, leitura, receita ou referência ao UUID.
