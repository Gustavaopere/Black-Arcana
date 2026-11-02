# Handoff — NeoForge 21.1.250: grief de entidades e cadeia Tremorzilla

**Objeto:** continuar a PR [#1008](https://github.com/Gustavaopere/Black-Arcana/pull/1008) sem reproduzir o inventário ou as 24 regressões do provider. A versão **21.1.250** é a versão de NeoForge na linha física **#001** da modlist em `neoforge-rpg-skilltree/main@59ff2a0e827fd08faa603f4482f8104ac433383c`. O Black Arcana compila, separadamente, com baseline 21.1.248 conforme D014.

## Procedimento exato

1. [Sonda de bytecode 21.1.250](../../docs/qa/neoforge_211250_grief_event_probe.py) reaproveita o analisador já selado de 21.1.248 e seus cinco contratos de método, sem transcrever código do NeoForge.
2. Baixar o `net.neoforged:neoforge:21.1.250:universal` do Maven oficial e registrar SHA-256/tamanho, classe, método, descritor JVM, callsites e contagem de instruções.
3. Comparar ao [manifesto 21.1.248](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/NEOFORGE-211248-GRIEF-EVENT-ABI.json) usando hashes de classes, digests de métodos, listas de callsites exatas e sequências simbólicas sem offsets. A comparação não se propõe a certificar comportamento em runtime transformado.
4. A primeira execução do [workflow](../../.github/workflows/neoforge-211250-grief-event.yml) **não é selada**. Usar o relatório obtido para fixar o manifesto `NEOFORGE-211250-GRIEF-EVENT-ABI.json`, e somente então executar a CI com `--seal` na HEAD final.

## Resultado SHA-exato da descoberta — workflow #41445890080

O JAR Maven oficial `neoforge-21.1.250-universal.jar` possui **3.551.255 bytes**, SHA-256 `1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956`. A [primeira CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41445890080) executou a sonda contra o artefato compilado e comparou seus resultados ao manifesto já selado de 21.1.248. O [manifesto 21.1.250](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/NEOFORGE-211250-GRIEF-EVENT-ABI.json) fixa os dados observados.

| Verificação entre 21.1.248 e 21.1.250 | Resultado compilado |
|---|---|
| Duas classes selecionadas (`EventHooks`, `EntityMobGriefingEvent`) | 2/2 SHA-256 idênticos |
| Cinco métodos (`canEntityGrief`, construtor, `canGrief`, `setCanGrief`, `isMobGriefingEnabled`) | 5/5 digests e contagem de instruções idênticos |
| Callsite/opcode selecionado com offset | 5/5 sequências de métodos equivalentes |
| Sequência simbólica de callsites, independente de offsets | 5/5 equivalentes |

Os bytes das **classes selecionadas** são idênticos nos dois artefatos; os JARs completos possuem SHA e tamanhos diferentes. Essa igualdade não engloba todos os métodos auxiliares do loader, transformações, mixins ou listeners carregados. Uma execução posterior com `--seal` sobre a HEAD final é necessária antes de considerar o manifesto validado por CI.

## Interpretação e limites

O recorte de 21.1.248 comprovou apenas o caminho `EventHooks.canEntityGrief` → gamerule ou evento → `canGrief()`. A análise de 21.1.250 deverá determinar se os cinco métodos selecionados preservam esse contrato. **Não converter igualdade de bytecode em permissão de destruição em claims.** O helper do NeoForge recebe `Level` e `Entity`, não `BlockPos`; listeners podem fazer verificações adicionais por entidade ou contexto, mas nenhuma integração concreta foi comprovada.

A cadeia nativa `TremorzillaEntity.breakBlocksAround` do Alex's Caves Continued 1.0.10 consulta `ACPlatform.canEntityGrief` antes dos pontos destrutivos observados no bytecode. Isso não comprova o `WorldEffectPolicy` de Black Arcana nem garante autorização para todos os blocos atingidos, ownership de player, proteção contra chunks descarregados ou rollback de explosões. Sem prova de hooks mutadores seguros, manter **`NO_MUTATION` / `NOT_CERTIFIED` / `physical_qa=NOT_TESTED`**.

**Contabilidade:** nenhum novo objeto catalogado, nenhum provider promovido; índices 28/30 (Alex's Caves Continued), 416/2.342 (fichas) e 4/164 (providers completos) inalterados. Stage 06 não é promovido.
