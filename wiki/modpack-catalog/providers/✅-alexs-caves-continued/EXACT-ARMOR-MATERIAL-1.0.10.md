# ACArmorMaterial 1.0.10 — adaptador de armaduras e disposição do marcador de tick

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
perk_certification=NOT_CERTIFIED
mutation=NO_MUTATION
provider_universe_closed=false
```

A [ficha do sistema de materiais](systems/armor-material.md) documenta o adaptador `ACArmorMaterial`, suas configurações nativas e os pontos de consumo diretamente identificados. O [manifesto SHA-exato](EXACT-ARMOR-MATERIAL-1.0.10.json) e o [auditor reproduzível](../../../../docs/qa/alexscaves_1010_armor_material_audit.py) sustentam os sete eixos estáticos. A disposição de `ACArmorTickItem` é de **suporte**, sem ficha, habilidade ou certificado adicional: o marcador não define uma API executável.

## Autoridade e escopo finito

| Campo | Evidência |
|---|---|
| Release | `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto 1645389 / arquivo 8856293 |
| Plataforma | Minecraft 1.21.1, NeoForge, Java 21 |
| Tamanho | 75.279.314 bytes |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Adaptador | `com/github/alexmodguy/alexscaves/server/item/ACArmorMaterial.class` |
| Adaptador SHA-256 | `478accf7ab37014dc06a8f3d801348948638dc517db0e21b7fd91d2b47ca40a6` |
| Marcador | `com/github/alexmodguy/alexscaves/server/item/ACArmorTickItem.class` |
| Marcador SHA-256 | `f3f9e0ea4b09af538ad28414da3f9e34b07f9a16fdc72beeeffd73ee1505f038` |
| Censo binário | 1.555 classes no JAR publisher; referências tipadas delimitadas por owner |
| Corpos próprios do material | 10, incluindo dois construtores e o inicializador; 149 instruções, 5 branches diretos |
| Corpos completos do recorte de consumidores | 55 métodos em 12 owners; 2.479 instruções, 22 branches diretos |
| Selo JSON | 115.383 bytes; SHA-256 `d063229c6414ea4cb4a1b6b5022a546a339c7cdbb640745e64f128db1e9395cc` |
| Contabilidade | Uma ficha de sistema, zero novas raízes mágicas, zero hooks/QA promovidos |

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e permanece adjacente. Os parâmetros desta entrega são de **1.0.10**, obtidos do artefato exato. O sistema auxilia a construção de equipamentos; nomes de classes ou atributos não o transformam em spell, efeito de combate ou integração executável com RPG Skill Tree.

O contrato cobre os dois construtores, sete métodos públicos próprios e o inicializador estático adicional. O recorte de 55 corpos completos não inclui a declaração abstrata de `ACTickingItem` nem a janela de operandos `DarknessArmorItem.acInventoryTick @0–30`; esses dois testemunhos são registrados separadamente, sem certificar o sufixo de poderes ativos. Declarações, descritores, corpos, constantes, chamadas e branches delimitam o comportamento; fingerprints isolados não substituem essas relações. Os consumidores de construção e configuração identificados recebem seu próprio escopo no manifesto. Os métodos completos de cada peça de armadura, os atributos e algoritmos internos do Minecraft e a execução do modpack não são promovidos por este recorte.

## Construção, estado e conversão

| Corpo | Contrato nativo |
|---|---|
| Construtor de seis argumentos | Encaminha nome, fator de durabilidade, array de defesa, encantabilidade, som e toughness ao overload com resistência a knockback igual a zero |
| Construtor de sete argumentos | Guarda os argumentos nos campos; o array é mantido por referência, sem cópia defensiva; ingredient começa null; resistência a knockback é pública |
| `vanilla()` | Cria novo `EnumMap<ArmorItem.Type,Integer>` e percorre os tipos; inclui apenas ordinais menores que o comprimento de `damageReduction`; constrói novo `ArmorMaterial` e devolve `Holder.direct` |
| `properties(Properties,Type)` | Solicita `properties.durability(MAX_DAMAGE_ARRAY[type.ordinal()] × durability)` |
| `defense(Type)` | Retorna `damageReduction[type.ordinal()]` |
| `toughness()` / `knockbackResistance()` | Retornam os campos correspondentes |
| `getRepairIngredient()` | Retorna `Ingredient.EMPTY` quando ingredient é null; nos demais casos, retorna o campo |
| `setRepairMaterial(Ingredient)` | Substitui o campo bruto, sem validação de jogador ou transação de reparo |
| Inicializador estático | Instala `MAX_DAMAGE_ARRAY=[13,15,16,11]` |

Os dois acessos diretos por ordinal em `properties` e `defense` não possuem a guarda de comprimento usada por `vanilla`. O contrato não presume tolerância a tipos externos, arrays null/curtos ou valores inválidos. Os quatro índices são documentados como índices: nomes de slots ou sua ordem efetiva na engine exigem a autoridade correspondente, sem dedução pelo texto de um enum.

`vanilla()` copia os elementos de defesa presentes para o mapa novo e passa encantabilidade, som, toughness e knockback ao construtor. A lista de layers é `List.of()` vazia nesse caminho; o nome armazenado não é consumido ali para criar texturas. A factory não registra um material em uma registry nem mantém um cache de `Holder` por chamada.

O fornecedor de reparo captura o adaptador e chama `getRepairIngredient` posteriormente. Há, portanto, **snapshot de valores no material construído e leitura tardia de reparo**. Alterar o array original ou o campo público pode influenciar outras leituras ou futuras conversões; não se presume mutação retroativa de todos os campos do material já construído. O setter de reparo atua no adaptador compartilhado, sem isolamento por jogador. Essa superfície pública não é um hook de perk homologado.

## Configurações e consumidores nativos

O censo encontra referências ao adaptador em sua própria classe, em `ACItemRegistry` e em seis owners de armadura: `DarknessArmorItem`, `DivingArmorItem`, `GingerbreadArmorItem`, `HazmatArmorItem`, `PrimordialArmorItem` e `RainbounceBootsItem`. A [ficha](systems/armor-material.md) individualiza os valores de cada configuração e suas atribuições de reparo, com os intervalos compilados correspondentes no [selo](EXACT-ARMOR-MATERIAL-1.0.10.json).

São **seis configurações nativas** e **cinco atribuições explícitas de reparo** no fluxo examinado. Não há atribuição equivalente para Rainbounce nesse setup. Isso prova a ausência naquele caminho, sem declarar impossível todo reparo por engine, datapack ou código externo. `Ingredient` declarado, possibilidade de matching e consumo físico de recurso são etapas distintas; o setter não efetua uma transação de anvil.

Defesa, encantabilidade, toughness e knockback são argumentos para o material da engine, não dano líquido, mitigação garantida ou autorização para mudar atributos de um jogador. A fórmula de durabilidade define a capacidade solicitada às propriedades da peça. Ela não gasta durabilidade, repara automaticamente uma stack, aplica mana, cria cooldown ou confirma que uma peça foi equipada.

## Marcador ACArmorTickItem e tick real

`ACArmorTickItem` é uma interface sem campos e sem métodos. No censo tipado do JAR exato, ela aparece na própria declaração e na lista de interfaces de `DarknessArmorItem`. Não há dispatcher nativo que use o marcador como condição ou o invoque como callback. Essa é uma conclusão limitada ao artefato publisher; transformações e consumidores externos não foram executados.

Darkness implementa também `ACTickingItem`, que possui a boundary real de inventário. O caminho delimitado de `ItemStackTickMixin.ac_inventoryTick` testa `ACTickingItem` e chama `acInventoryTick`; o callback de Darkness encaminha ao seu helper privado `acArmorTick`. O nome do helper não cria um método na interface vazia. O marker é registrado como **`EMPTY_MARKER_SUPPORT_ONLY`**, com zero candidatos adicionais e sem uma promessa de tick por slot equipado.

O [inventário de integração](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) conserva seu roster físico original e acrescenta a disposição do prefixo revisado: material certificado e marcador de suporte. Isso permite continuar a ordem alfabética sem repetir a auditoria nem confundir suporte com ação mágica.

## Sete eixos e limites de integração

| Eixo | Evidência estática | Limite |
|---|---|---|
| Identidade | JAR e classes SHA-exatos, roster tipado e descritores | Fonte 1.1.1 adjacente, sem paridade presumida |
| Comportamento | Construção, conversão, getters/setter, propriedades e consumidores delimitados | Sem certificar todo o comportamento das peças ou da engine |
| Parâmetros | Arrays, fatores, defesa, encantabilidade, som, toughness, knockback e reparo nativos | Sem clamp, isolamento por jogador ou mapeamento de enum inventado |
| Targeting | Material sem aquisição de alvo, área, projétil, fonte de dano ou seleção de vítima | Atributos defensivos não se tornam spell ou política de PvP/claims |
| Custos/tempo | Capacidade de durabilidade e ingrediente de reparo declarados; sem débito/cooldown próprio | Nenhuma transação, desgaste ou reparo físico executado |
| Integração | Snapshot versus supplier tardio, owners e marcador/dispatcher separados | `NO_MUTATION`; nenhum hook per-player, XP ou Mastery aprovado |
| Validação | Selo reproduzível, regressões causais/negativas e verificação de metadados/índices | `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` |

Black Arcana mantém seu runtime mágico e RPG Skill Tree sua progressão. Os valores documentados orientam o desenho de perks; não autorizam reconfiguração global do material, substituição de `Holder`, atribuição de array compartilhado ou segunda aplicação de atributos/reparo. Dano, efeitos, ticks, animações e estado próprios das peças exigem seus contratos. Não há novo cast ou crédito de Mastery nesta camada.

## Reprodução e aceitação

O [workflow dedicado](../../../../.github/workflows/alexscaves-1010-armor-material.yml) obtém o artefato exato e executa o [auditor](../../../../docs/qa/alexscaves_1010_armor_material_audit.py), seus negativos e as regressões documentais. A execução deve confrontar os hashes e as relações semânticas do selo:

```bash
python docs/qa/alexscaves_1010_armor_material_audit.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ARMOR-MATERIAL-1.0.10.json' \
  --output /tmp/armor-material-evidence.json
```

Critérios: duas saídas idênticas ao selo; rejeição de artefato/transcript/pivô/roster/boundary alterados; correspondência entre configurações, consumidores, ficha e certificado; preservação das evidências anteriores; índices gerados sem inconsistências. Sucesso do auditor e da CI comprova a evidência estática dentro desse escopo, não uma sessão física do modpack.

**QA física permanece pendente:** construção e equipamento de cada peça, atributos efetivos e ordem de slots, dano/knockback recebido, encantamento e custo de anvil, matching/consumo de reparo, persistência após reload, mudança de configuração, material compartilhado entre usuários, duplicação de atributos, cliente/servidor, overrides, mod transformado e regressões das habilidades de cada equipamento. Nenhum cenário recebe PASS por ter um getter, setter ou referência de classe.

## Contagem atual e continuação

Esta ficha adiciona **um sistema de suporte observado e um contrato estático**, sem nova raiz mágica. O catálogo passa a **220/2394 contratos estáticos**, **470/2394 fichas catalogadas**; Alex's Caves chega a **82/82 fichas observadas**. Dano **11/11** e encantamentos **51/51** permanecem concluídos em seus recortes; a nova árvore `systems/` mostra **1/1 (100%)** das fichas detectadas, sem fechar todos os sistemas do provider.

O universo integral de Alex's Caves continua aberto. Providers com catálogo encerrado permanecem **4/164**, providers integralmente homologados para perks **0/164**. Próximo item do prefixo alfabético ainda sem disposição: **`server/item/ACClientExtensionItem`**. A presença do nome no inventário identifica trabalho restante, não prova comportamento ou escopo concluído.
