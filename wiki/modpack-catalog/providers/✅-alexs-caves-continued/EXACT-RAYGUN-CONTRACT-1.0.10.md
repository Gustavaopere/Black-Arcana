# Raygun 1.0.10 — contrato estático consolidado dos sete eixos

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
static_technical_contract=CERTIFIED_STATIC_7_AXES
version=1.0.10
damage_type=alexscaves:raygun
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
perk_certification=NOT_CERTIFIED
network_authorization=NOT_VERIFIED
mutation=NO_MUTATION
provider_universe_closed=false
```

A [ficha Raygun](damage-types/raygun.md) conclui o contrato documental individual do DamageType e de seu consumidor nativo. O [novo selo](EXACT-RAYGUN-CONTRACT-1.0.10.json) combina provas anteriores em seus escopos e acrescenta disposições comportamentais e pivôs para **cada um dos 26 métodos próprios** do item. O inicializador estático e o consumidor externo de anvil recebem registros separados. Identidade de corpo, instrução observada, argumento solicitado e resultado físico mantêm significados distintos.

A [ficha histórica](damage-types/EXACT-RAYGUN-HISTORICAL-CARD-1.0.10.md) foi preservada byte a byte: **57.610 bytes**, SHA-256 `75f033bc9c27195c85ca952e0b70bc18ff00f5f1aba1955e58242c98c11e0f87`. Seus contadores e conclusões parciais pertencem aos checkpoints anteriores. Os antigos arquivos `EXACT-*` e seus limites não foram reescritos para aparentar um contrato completo retroativo. Este documento acrescenta uma conclusão estática atual; não declara segurança da rede, hooks mutadores ou execução no modpack.

## Identidade e procedência

| Evidência | Valor exato |
|---|---|
| Artefato | `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto 1645389 / arquivo 8856293 |
| Plataforma | Minecraft 1.21.1, NeoForge, Java 21 |
| Tamanho | 75.279.314 bytes |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Classe | `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class` |
| Classe SHA-256 | `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| DamageType JSON | `data/alexscaves/damage_type/raygun.json` |
| JSON SHA-256 | `dc1095e92e0695b302100993af8fafd72c8d6b948d90717e667a6ced2ae1bc35` |
| Métodos próprios | 26 / 1.111 instruções / 107 branches diretos |
| Inicializador adicional | 3 instruções, binding de `AMMO` ao predicado sintético |

O JSON literal declara `message_id=raygun`, `scaling=never` e `exhaustion=0.3`. As três inclusões diretas empacotadas são `minecraft:bypasses_cooldown`, `minecraft:is_explosion` e `minecraft:is_projectile`; o auditor enumera as tags de DamageType no JAR para verificar o conjunto. Tags resolvidas com datapacks, cooldown de casting, explosão de mundo ou uma entidade projétil não decorrem desses rótulos.

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**: é adjacente, sem autoridade para os parâmetros de 1.0.10. O artefato físico e os corpos compilados são a autoridade desta conclusão.

## Sete eixos e evidências próprias

| Eixo | Evidência estática certificada | Limite preservado |
|---|---|---|
| Identidade | JAR/classe/recurso SHA-exatos, tags diretas, factory e construtor de DamageSource | Registry/datapacks transformados do mundo não executados |
| Comportamento | Censo completo com disposição e pivôs dos 26 métodos; inicializador e anvil delimitados | Não promete execução de callbacks nem resultados físicos |
| Parâmetros | Charge, munição, duração, rampa/range, EE/Solar, dano/status, estado e UI | Setters brutos não oferecem clamps ou autorização universais |
| Targeting | Traces, endpoints, busca X-Ray, fallback, cubo final e filtros nativos | Sem garantia de nearest global, PvP/claims ou penetração física |
| Custos/tempo | Recarga, gasto cliente, recuperação servidor e cadência ofensiva separados | Sem recibo autenticado de custo ou cooldown inventado |
| Integração | Owners item/factory/status/UI/anvil/rede, fonte direta versus periódica | `NO_MUTATION`; kill, deduplicação, XP e Mastery não homologados |
| Validação | Reprodução do selo, regressões de comportamento, negativos e integridade dos índices | `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` |

O [selo anterior dos métodos](EXACT-RAYGUN-ALL-METHODS-1.0.10.json) continua `SHA_EXACT_1010_RAYGUN_26_METHOD_BODY_FINGERPRINTS_ONLY`. O novo auditor exige, além de seus digests, descritor, contagem, branches e `method_dispositions` com fatos e pivôs semânticos para todos os corpos. O inicializador `static {}` não entra no censo anterior de 26: é extraído separadamente e seu bootstrap vincula `AMMO` a `lambda$static$0`.

O construtor solicita stacks de uma unidade. Encantabilidade, renderer, animação e reequip são classificados por seus próprios retornos/delegações; não são consumidores de dano. Os leitores e escritores enumeram todas as chaves nativas: `ChargeUsed`, `UseTime`, `PrevUseTime`, `RayX/Y/Z` e `PrevRayX/Y/Z`. `getRayPosition` retorna `Vec3.ZERO` sem tag/chave `RayX`; `getLerpedRayPosition` retorna null sem tag e estreita os doubles por float antes da interpolação. UI e setters não impõem clamp próprio.

`AlwaysCombinableOnAnvil` é um marcador sem métodos. O registro separado de `CommonEvents.onUpdateAnvil` sela os pivôs de marcador, identidade do item, encantamentos não vazios, cópia, merge, custo e output. O caminho não contém chamadas a `setCharge`, `setUseTime`, `setDamageValue` ou `shrink`. Ele não transforma Uranium Rod em reparo de durabilidade nem comprova toda a CFG de anvil. A [ficha](damage-types/raygun.md) mantém o contrato dos owners externos delimitado.

## Contratos compostos e causalidade

| Prova preservada/reexecutada | Relação que fornece |
|---|---|
| [Charge/munição](EXACT-RAYGUN-CHARGE-AMMO-FLOW-1.0.10.json) | Oito métodos, 168 instruções, 15 branches; uso carregado, busca de rod, shrink, reset e retorno |
| [Charge/cost](EXACT-RAYGUN-CHARGE-COST-1.0.10.json) | Lado cliente do débito e condições de recuperação Solar servidor |
| [CFG de outcomes](EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json) | Fluxo normal delimitado de uma iteração de dano, status e feedback |
| [Guardas pós-hit](EXACT-RAYGUN-POST-HIT-GUARDS-1.0.10.json) | Valor local booleano, retorno de hurt e condições da continuação |
| [X-Ray](EXACT-XRAY-CAUSAL-1.0.10.json) | Endpoint/scan/fallback/impacto, composição dos contratos Gamma e Energy Efficiency |
| [Gamma](EXACT-GAMMA-RAY-CAUSAL-1.0.10.json) | Factory/caster, valores de dano/status, consumidores visuais e Energy Efficiency |
| [Receiver](EXACT-RAYGUN-RECEIVER-1.0.10.json) e [CFG condicional](EXACT-RAYGUN-RECEIVER-CFG-1.0.10.json) | Encaminhamento condicionado de tags de entrada, sem aprovação de autoridade |

Defina D=`ChargeUsed` e T=`72000−remainingUseTicks`. D é consumo acumulado: `hasCharge` testa D<1000. O setter grava o inteiro bruto. Ao esgotar, `use` procura a primeira rod elegível, consome uma unidade e solicita D=0; Creative tem via própria sem rod. O ramo de recarga retorna `useFail`, inclusive após recarregar, e não começa imediatamente o uso. `releaseUsing` envia tags somente no cliente, chama a superclasse e limpa o cache de som; não reseta charge/tempos/posição nesse corpo.

A rampa é p=T/15F se T<15, senão 1F, sem clamp inferior próprio; r=25F×p. **Gasto de charge e dano possuem gates diferentes.** O débito cliente exige p≥1, T%I=0 e não Creative, com I=2+floor(1.5F×nível EE), e solicita min(D+1,1000). O gate de dano servidor é `!isClientSide && (T−15)%3==0`: **não possui condição adicional T≥15**. Logo a congruência também admite 0/3/6/9/12, se os demais caminhos forem alcançados. Rampa visual e de custo não garantem quinze ticks sem dano.

Solar positivo exige stack ociosa, D>0, sorteio <0.02F, céu, dia, dimensão sem horário fixo e helper solar; solicita D−1 e UseTime=0 no servidor. A animação de inventário cliente atualiza PrevUseTime e sobe/desce UseTime sob seus guards. Chance por callback elegível não é taxa física garantida por segundo.

X-Ray altera extremos e uma busca segmentada em caixa inflada por r. Primeiro retorno não nulo substitui o trace inicial e encerra o laço; sem retorno, mantém o resultado inicial. O dano usa outro volume: **cubo de lado 2, centro local14 ±1**. Um resultado de entidade substitui o centro por `entity.position()`, não pelo ponto de interseção. Local21 nulo pula feedback visual, sem bloquear por si só a consulta final de dano. Self, aliança nas duas direções, mesmo veículo e predicate nativo continuam filtrando candidatos.

O dano solicitado é 1.5F/2F, conforme Gamma positivo. `causeRaygunDamage(registryAccess,usuario)` constrói uma fonte com o usuário; isso não garante crédito final de kill. Tremorzilla pula hurt e seleciona continuação verdadeira; a tag de resistência publisher a inclui e bloqueia Irradiated nesse conjunto de dados. Nos demais alvos o retorno de hurt controla a continuação, e o status ainda exige LivingEntity fora da resistência. Irradiated é solicitado por 800 ticks, amplifier0/4. Só `addEffect=true` permite o feedback visual. Pedido de dano, aceitação de dano, aceitação do efeito e pacote são fatos separados.

[Irradiated](effects/irradiated.md) e [Radiation](damage-types/radiation.md) mantêm seu contrato periódico: a factory de radiação não recebe caster. O novo certificado não transfere autoria direta para DoT, lifesteal, kill, XP ou Mastery. Gamma, Energy Efficiency, Solar e X-Ray mantêm fichas próprias e contabilidade anterior, sem novos casts ou raízes mágicas.

## Boundary de rede e campos N/A

O item implementa `UpdatesStackTags` sem override próprio. O callback default encaminha a tag a `ACCompat.setTag`, que remove ou grava `CUSTOM_DATA`. O receiver resolve entityId, exige LivingEntity e compara o item nas mãos antes do callback condicionado. Isso documenta um **encaminhamento de entrada cliente condicionado**, sem comprovar vínculo autorizado remetente/entityId, saneamento por chave, antirreplay, limite efetivo de payload ou entrega de pacote. Os antigos proofs de codec/Minecraft conservam seus limites; a certificação estática não depende de presumir que toda a rede é segura, nem declara uma vulnerabilidade reproduzida.

Entidade/velocidade/dimensões/vida de projétil, summon, cura, mana/stamina, cooldown de casting, timer autônomo de spell e explosão/mutação de mundo são **N/A nos métodos próprios**. Traces, partículas, tags de DamageType e uso72000 não preenchem esses campos por analogia. Black Arcana mantém a autoridade de seu runtime e world safety; RPG Skill Tree usa boundaries reais para perks e progressão. Não existe aqui autorização para setter mutador, adapter presumido ou processamento duplicado de um hit.

## Reprodução e critérios de aceitação

O [auditor](../../../../docs/qa/alexscaves_1010_raygun_contract_audit.py) é somente leitura. O [workflow](../../../../.github/workflows/alexscaves-1010-raygun-contract.yml) verifica o JAR publisher e executa regressões nativas/documentais. A reprodução usa Java 21 e o JAR exato:

```bash
python docs/qa/alexscaves_1010_raygun_contract_audit.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-CONTRACT-1.0.10.json' \
  --output /tmp/raygun-contract-reproduced.json
```

O comando deve rejeitar artefato, recurso, censo, corpo, pivô, tag, seal ou boundary de segurança divergente. A saída deve coincidir com o selo congelado em duas execuções independentes. Os testes incluem a manutenção dos limites de rede/QA, a cobertura dos 26 métodos e o relacionamento entre a ficha atual e o arquivo histórico. Os resultados locais e da CI ficam no registro verificável da PR; sucesso estático não corresponde a combate físico.

## Contabilidade e próximo escopo

Esta entrega acrescenta **um certificado estático a uma ficha existente**, **zero candidatos** e **zero raízes mágicas**. O recorte corrente de DamageTypes publisher fica **11/11**, com os 11 JSONs identificados e as 11 fichas individuais certificadas. O inventário preserva os campos do **checkpoint histórico de nove contratos** e registra Tremorzilla Beam e Raygun como certificados individuais adicionais, sem reescrever aquela prova.

O recorte observado do provider passa a **81/81 (100%)** e os encantamentos permanecem **51/51**. Os índices mostram 100% desses recortes. Isso não encerra o universo de integração: material/armor APIs, itens, poções, configuração e mensagens do inventário ainda exigem fichas ou disposições individuais. A próxima superfície não coberta em ordem alfabética é `server/item/ACArmorMaterial`, seguida por `ACArmorTickItem`; o provider continua aberto, sem avanço automático da fila.

O catálogo global passa a **219/2393 contratos estáticos** e **469/2393 fichas catalogadas**; providers com catálogo encerrado permanecem **4/164**, providers integralmente homologados para perks **0/164**. Hooks mutadores, QA física, aceitação real de dano/custo/efeitos, multiplayer, persistência, PvP/claims e promoção de Stage não recebem aprovação nesta entrega.
