# Nuke — tipo de dano `alexscaves:nuke` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:nuke`.
- **Caminho ZIP:** `data/alexscaves/damage_type/nuke.json`.
- **SHA-256 do JSON:** `c44737192a4999c35799e24bb3df4cd9ca77e8f58d5fce1c74a53a71f0170d92`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `nuke` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.1` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- `minecraft:bypasses_cooldown`
- `minecraft:is_explosion`
- `minecraft:is_fire`

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.
O tag `minecraft:bypasses_cooldown` corresponde à classificação de tipo de dano do Minecraft, **não** demonstra redução/bypass do cooldown de lançamento de magias.


## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | `NÃO VERIFICADO` |
| Fórmula de dano, mitigação, críticos e resistências | `NÃO VERIFICADO` |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | `NÃO VERIFICADO` |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | `NÃO VERIFICADO` |
| Duração, intervalo de hits, custo de ação e cooldown de casting | `NÃO VERIFICADO` |
| Persistência, ordenação de eventos, server authority e deduplicação | `NÃO VERIFICADO` |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeNukeDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `NUKE` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;I)V`.
- **Parâmetros da factory:** apenas `RegistryAccess` — nenhum argumento `Entity` na assinatura da factory.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/item/NuclearExplosionEntity.class` | `public void tick()` | `()V` | 618 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Aprofundamento de fluxo — 1.0.10 (instruções compiladas)

**Evidência estática delimitada:** [manifesto de janelas e branch opcodes](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json), auditado no JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe `com/github/alexmodguy/alexscaves/server/entity/item/NuclearExplosionEntity.class` (SHA-256 `d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912`). Método `public void tick()`, descritor JVM `()V`; 348 instruções extraídas e 39 anchors de branch registrados. Resumo de chamadas diretas: `causeIntentionalGameDesign` @ `605`, `causeNukeDamage` @ `618`.

- Em `tick()`, o offset `586` usa `ifle` como guarda antes da seleção; `isIntentionalGameDesign()` é consultado em `592`, seguido por `ifeq 611` em `595`.
- O caminho que passa por `605` chama `causeIntentionalGameDesign()`, e `goto 621` no offset `608` desvia da factory `causeNukeDamage()` localizada em `618`; ambos convergem na referência a `LivingEntity.hurt()` em `623`.
- A bifurcação local comprova uma escolha de factory **nesse trecho**. Não demonstra o dano total da explosão, número de alvos, proteção de blocos, PvP nem quantas vezes `tick()` percorre essa região.

**Limite metodológico:** offsets, referências de método, testes e desvios são provas do *bytecode*; a análise não reconstruiu exceções, switch dispatch, todos os caminhos de CFG ou condições de runtime. `NOT_CERTIFIED` para comportamento integral; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Black Arcana não deve substituir settlement, autorizações de servidor, segurança do mundo ou rotinas próprias do provider.


## Origem dos objetos de explosão nuclear — JAR 1.0.10

**Manifesto de referências SHA-exatas:** [EXACT-NUCLEAR-PRODUCERS-1.0.10.json](../EXACT-NUCLEAR-PRODUCERS-1.0.10.json), auditado em [CI específica](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-nuclear-producers.yml). Nove classes do provider contêm os tokens binários pesquisados, seis contêm referências localizadas em método por `javap`, e quatro são candidatas de emissão nativa de `NuclearExplosionEntity`; não se declara fechamento global dos produtores ou enumeração de mixins/indireções.

| Produtor e método | Superfície técnica SHA-exata | Dependência ou ressalva |
|---|---|---|
| `NuclearBombEntity.explode()` | `ACEntityRegistry.NUCLEAR_EXPLOSION` @0 → `ACCompat.createEntity` @15 → `copyPosition` @24 → `setSize` @43 → `Level.addFreshEntity` @51. | `setSize` recebe `floatValue` de `ModConfigSpec.DoubleValue.get` via configuração comum do mod; **não há tamanho fixo global auditado**. |
| `NucleeperEntity.explode()` | Registry @0 → factory @15 → `copyPosition` @24 → `setSize` @42. `ACCompat.gameRule` consulta `GameRules.RULE_MOBGRIEFING` @49/53; `ifne 64` @56 contorna `setNoGriefing(true)` @61 no ramo verdadeiro. Spawn solicitado @69. | Respeita a decisão nativa de bloqueio de griefing nesse caminho; não substitui a política de segurança do Black Arcana. A expressão de tamanho requer investigação específica. |
| `NuclearFurnaceBlockEntity.destroyWhileCritical(boolean)` | Condição `ifeq 318` @257 precede registry @260 e factory @275; `setPos` @294, `setSize(0.75f)` @299/302 e `Level.addFreshEntity` @311. | Explosão condicionada à destruição crítica da fornalha; não existe prova de casting ou atribuição a player. |
| `SackOfSatingItem.acInventoryTick` | Condição `isExploding(ItemStack)` @275/278, checagem client-side @282/285; registry @288; factory @300; `setSize(0.5f)` @327/330; `setIntentionalGameDesign(true)` @335/336; spawn @342. | Este emissor **altera o modo de dano** da mesma entidade: não atribuir automaticamente `alexscaves:nuke` à sua explosão; no ramo observado a classificação selecionada pode ser `alexscaves:intentional_game_design`. |

O recorte demonstra diferentes **origens, valores de tamanho e gates nativos** que convergem numa implementação compartilhada de `NuclearExplosionEntity.tick`. Essa rotina seleciona entre `causeIntentionalGameDesign(RegistryAccess)` @605 e `causeNukeDamage(RegistryAccess)` @618 antes de uma chamada `LivingEntity.hurt(DamageSource,float)` @623. A variante do `SackOfSatingItem` e a da bomba não devem gerar processos de perk duplicados pelo nome ou pelas tags de `DamageSource`.

**Owner e segurança:** a factory de criação `ACCompat.createEntity(EntityType,Level)` selecionada delega a `EntityType.create(Level)`. Nenhum owner causal foi certificado para estes quatro emitters, ainda que alguns sejam disparados por itens/entidades. `setNoGriefing` em um produtor e o valor default `NO_GRIEFING=false` na entidade não comprovam proteção de blocos em todos os caminhos. Qualquer implementação futura requer boundary de `WorldEffectPolicy`, limites de área, deduplicação e validação servidor/PvP.

**Limites documentados:** inventário estático de candidatos, não um call graph exaustivo. O parser exclui inicializadores de classe, não resolve lambdas indiretas, callbacks, outras bibliotecas, mixins ou runtime. **`NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`**; contadores e Stage intactos.


## Cálculo numérico e tamanho de emissão — método SHA-exato 1.0.10

**Manifesto adicional verificável:** [EXACT-NUCLEAR-NUMERIC-1.0.10.json](../EXACT-NUCLEAR-NUMERIC-1.0.10.json) · [workflow de verificação](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-nuclear-numeric.yml). O arquivo contém as **26 instruções** de `NuclearExplosionEntity.calculateDamage(FF)F`, as **34 instruções** de `NucleeperEntity.explode()V` e as **24 instruções** de `NuclearBombEntity.explode()V`, verificadas contra hashes de método e classe publicados anteriormente. É evidência de bytecode selecionado do JAR publisher 1.0.10, sem garantir alcance operacional ou dano pós-mitigação.

### Expressão compilada por `calculateDamage(float, float)`

Definindo `d` como o primeiro argumento `fload_1`, `r` como o segundo argumento `fload_2` e `s` como `getSize()`, o método calcula:

\[
D_{\mathrm{raw}} = \left(\frac{r-d}{r}\right)\cdot M(s),
\quad
M(s)=
\begin{cases}
100,&s\leq1.5\\
100+400(s-1.5),&s>1.5.
\end{cases}
\]

**Proveniência de instruções:** `fload_2, fload_1, fsub, fload_2, fdiv` (offsets 0–4) formam a proporção; `getSize` @7, `1.5f` @10, `fcmpg` @13, `ifgt 23` @14 escolhem o ramo; `100f` @17 ou `100f + (getSize()-1.5f)*400f` @23–38; `fmul` @44 e `freturn` @45.

O segundo `float` é fornecido pela variável local `5` em `NuclearExplosionEntity.tick` na chamada `calculateDamage` @466; o primeiro vem de `LivingEntity.distanceTo` @456. **Não chamar `r` de raio de destruição comprovado**, pois o significado e a inicialização de `local 5` requerem rastreamento completo do consumidor. Não existe `clamp` explícito **neste método**; divisão por zero, valores fora do intervalo e regras de arredondamento IEEE 754 devem ser avaliados separadamente. O `tick` usa `fstore 9` @469 e verifica `ifle 627` @586 antes de chamar `LivingEntity.hurt` @623; portanto, valores numéricos calculados **não equivalem a hits aceitos ou dano final**. A seleção entre `nuke` e `intentional_game_design` é uma etapa diferente da fórmula.

### Fontes de `SIZE` verificadas sem inferir configuração efetiva

| Origem | Código de emissão selecionado | Interpretação limitada |
|---|---|---|
| `NucleeperEntity.explode` | `isCharged()` @29; `ifeq 41` @32; `ldc float 1.75f` @35, alternativamente `fconst_1` @41; ambos convergem em `NuclearExplosionEntity.setSize` @42. | `SIZE=1.75f` quando carregado e `SIZE=1.0f` quando não carregado, **neste produtor**. |
| `NuclearBombEntity.explode` | `AlexsCaves.COMMON_CONFIG` @28 → campo exato `ACServerConfig.nukeExplosionSizeModifier` @31 → `ModConfigSpec.DoubleValue.get` @34 → `Double.floatValue` @40 → `setSize` @43. | O tamanho é um **parâmetro de configuração nativo**; o valor efetivo, os limites e overrides da instalação continuam `NOT_VERIFIED`. |
| `NucleeperEntity.explode` (griefing) | `RULE_MOBGRIEFING` @49, `ACCompat.gameRule(Level,Key,true)` @53, `ifne 64` @56; sob retorno falso, `setNoGriefing(true)` @61. | Essa condição de um emissor não demonstra proteção contra destruição para todos os demais nem autoriza contornar `WorldEffectPolicy`. |

**Permissões para perks:** tratar o tamanho da emissão, a intensidade numérica bruta e o settlement do dano como variáveis diferentes. As flags de world griefing, a atribuição causal a jogador e os limites de área não foram integralmente auditados. Não inferir escalonamento global a partir do caso `Nucleeper` ou promover integração por interpolação da fórmula.

**Status:** ⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. Não houve promoção do certificado de sete campos, alteração de índices, concessão de hooks nem avanço de Stage.
