# Gamma Ray 1.0.10 — prova técnica estática individual

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
version=1.0.10
enchantment=alexscaves:gamma_ray
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
perk_certification=NOT_CERTIFIED
mutation=NO_MUTATION
whole_provider_catalog_closed=false
```

A [ficha individual](enchantments/gamma-ray.md) descreve um modificador nativo da Raygun. Esta prova conclui a documentação estática do encantamento, sem concluir o contrato integral da [Raygun](damage-types/raygun.md), autorizar um mutador ou criar outro cast. Dano solicitado, aceitação do hit, aplicação do status e entrega de mensagem visual continuam sendo fatos distintos.

## Artefato e evidências reutilizadas

O artefato instalado é `alexscaves-1.0.10-neoforge+1.21.1.jar`, publisher file `8856293`, Minecraft 1.21.1 / NeoForge / Java 21:

| Identificador | Valor |
|---|---|
| Tamanho | 75.279.314 bytes |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| `RaygunItem.class` SHA-256 | `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| `onUseTick` digest normalizado | `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5` |
| Corpo de `onUseTick` | 523 instruções JVM e 57 branches diretos |

O novo [manifesto individual](EXACT-GAMMA-RAY-CAUSAL-1.0.10.json) combina a análise causal de Gamma com as identidades e verificações integrais já existentes de [Energy Efficiency](EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json). Os recortes históricos [Gamma/X-Ray](EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json), [consumidores](EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) e [guardas de radiação](EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) mantêm seus bytes e escopos. A prova do status [Irradiated](effects/irradiated.md) continua sendo a autoridade documental para seus consumidores posteriores.

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**. Ela é adjacente: não substitui o JAR físico 1.0.10 nem prova equivalência de código ou números. As evidências desta ficha vêm do artefato SHA-exato e dos recursos extraídos dele.

## Definição e exclusão declarada

`data/alexscaves/enchantment/gamma_ray.json` declara:

| Campo | Valor publisher |
|---|---|
| `description.translate` | `enchantment.alexscaves.gamma_ray` |
| `supported_items` | `#alexscaves:enchantable/raygun` |
| `max_level` / `weight` | 1 / 2 |
| `min_cost` | base 1; passo 18 por nível acima do primeiro |
| `max_cost` | base 41; passo 10 por nível acima do primeiro |
| `anvil_cost` / `slots` | 4 / `mainhand` |
| `exclusive_set` próprio | Ausente |

A tag de item aponta para `alexscaves:raygun`. A exclusão é declarada em **`x_ray.json`**, cujo `exclusive_set` contém `alexscaves:gamma_ray`; não se inventa esse campo no recurso Gamma. Custos de encantamento não são consumo de carga, mana, cooldown ou dano. Recursos e tags publisher não comprovam os datapacks efetivos de um mundo ou a obtenção real do encantamento.

## Seleção Gamma e consumidores

O descritor de `RaygunItem.onUseTick` é `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`. A leitura `ACCompat.enchantLevel(stack,GAMMA_RAY)` acontece em `@332–335`. O `ifle @338` seleciona zero ou um, seguido pela única escrita `istore 18 @346`. Os consumidores leem esse mesmo slot em `@367`, `@402`, `@922`, `@1029` e `@1138`.

| Região | Seleção nativa |
|---|---|
| `@367–404` | Variantes de partículas/feedback azul; não representam dano adicional |
| `@922–932` | Amplifier local 23: Gamma positivo → 4; alternativa → 0 |
| `@1029–1041` | Dano solicitado: Gamma positivo → 2F; alternativa → 1,5F |
| `@1111–1119` | Solicitação de `Irradiated` por 800 ticks com o amplifier local 23 |
| `@1138–1154` | Payload visual 4/0 e 800; enviado somente no caminho de aplicação aceito |

O nível positivo escolhe uma variante booleana. O código não usa o valor numérico do nível para escalar continuamente dano, duração ou amplifier. Amplifier 4 corresponde ao nível visual V; isso não significa dano multiplicado por cinco.

## Disposição dos consumidores visuais

O censo literal de `GAMMA_RAY` encontra quatro classes: `ACEnchantmentRegistry`, `RaygunItem`, `ACItemstackRenderer` e `RaygunRenderHelper`. A seção `visual_consumers` do novo selo identifica os dois consumidores cliente, separadamente dos corpos causais de dano/carga/status.

- `ACItemstackRenderer.renderByItem`: corpo de 1.771 instruções com digest `b409b1c334dae2bcf0ed11c0327dd36850adf755fd88c7b434f169bad8197f87`. A leitura Gamma em `@1968` passa por `enchantLevel @1971`, gera o booleano local 14 e seleciona `RAYGUN_BLUE_TEXTURE @1989` ou `RAYGUN_TEXTURE @1995`.
- `RaygunRenderHelper.renderRaysFor`: corpo de 209 instruções com digest `2862f26fbb27c44fdd180a77f64a8bf1165e98619d083063157f52ef99ae3eae`. As leituras em `@64` e `@294` formam booleanos locais encaminhados aos calls de desenho do feixe.

Os hashes identificam os corpos; os pivôs selecionados comprovam essas relações visuais específicas. Não se declara CFG completo do renderizador de todos os itens, nem execução física de cada caminho gráfico. Textura, desenho, partículas e mensagem visual são consumidores diferentes, sem novo dano ou recibo de Mastery estabelecido por esses trechos.

## Cadência de dano e consumo de carga são separados

O bloco de tentativa de dano está no servidor: `Level.isClientSide @875`, `ifne @878 → 1160`. Depois, o método calcula `(elapsed−15)%3` em `@881–888` e pula o bloco quando o resto não é zero. **Não há nesse gate uma condição adicional `elapsed>=15`.**

No domínio normal de elapsed não negativo, a congruência permite oportunidades em 0, 3, 6, 9 e 12, além de 15 e seguintes. Isso é uma propriedade estática da condição, não prova de que o callback ou um hit aceito ocorra em cada instante. A consulta anterior de carga e os outros filtros continuam aplicáveis.

O aquecimento de 15 ticks do caminho cliente pertence a outro ramo, documentado por Energy Efficiency: o consumo considera `p>=1`, periodicidade própria e exceção criativa. `ChargeUsed`, limite 1000, recarga e mensagem de atualização pertencem à Raygun. Gamma não acrescenta um débito próprio. A existência de envio cliente→servidor não comprova autorização server-side, imunidade a replay ou persistência efetiva de um valor recebido.

## Targeting, dano, resistência e feedback

A expressão nativa `25F*p` participa do targeting do item, com `p` dependente de elapsed/aquecimento. Gamma não altera essa expressão. X-Ray seleciona outros caminhos de trace; a exclusividade declarada não permite pressupor o comportamento de stacks produzidas por comandos ou outros mods.

O bloco de dano constrói uma **AABB entre local 14−(1,1,1) e local 14+(1,1,1)** em `@891–917`. É uma caixa de lado 2, não um novo projétil, hitbox ou raio esférico de Gamma. A consulta `Level.getEntities @943` é seguida por exclusão do próprio usuário, testes de aliança nos dois sentidos e `isPassengerOfSameVehicle`. Sem prova adicional não se transforma essa consulta em política universal de PvP, claims ou linha de visão.

A fonte direta recebe o caster: `aload_2 @1025`, `ACDamageTypes.causeRaygunDamage @1026`. A chamada `ACCompat.hurt @1041` usa o valor 2F/1,5F, mas o resultado não é universalmente necessário para a flag local de aprovação:

1. `instanceof TremorzillaEntity @1013` e `ifne @1016 → 1047` contornam `hurt` e selecionam a flag verdadeira.
2. Para os demais alvos, `ifeq @1044 → 1051` transforma o retorno de `hurt` em zero ou um.
3. `istore 26 @1052` e `ifeq @1056 → 1157` controlam a continuação para status.
4. O status exige alvo vivo e ausência da tag `RESISTS_RADIATION`, testada em `@1082–1088`.
5. A instância é solicitada por `addEffect @1119`; seu retorno falso pula a mensagem visual (`ifeq @1122 → 1157`).

Portanto, não se descreve “dano aceito” como pré-requisito universal do status. A exceção Tremorzilla está no código; a tag publisher de resistência também o inclui e normalmente impede esse caminho de status no conjunto de dados original. Substituições de tags/datapacks são outro estado de mundo, ainda não certificado.

`sendMSGToAll @1154` demonstra um pedido de entrega visual após a aplicação aceita naquele ramo. Não é um segundo `addEffect`, confirmação de entrega a todos os clientes, recibo de dano ou autenticação de um pacote.

## Duração, autoria e consequências posteriores

Os 800 ticks são a duração solicitada da instância de Irradiated, não duração da canalização nem garantia de exposição integral. Imunidades, substituição/remoção de status e consumidores externos permanecem fora da aceitação física desta ficha.

O contrato certificado de [Irradiated](effects/irradiated.md) distingue amplifier e dano periódico. Amplifier 0 não executa o tick próprio do efeito; amplifier 4 seleciona o período nominal `200/4=50`, com fase baseada na duração. Hazmat, RNG e outros guards afetam a solicitação posterior de dano. A fonte de radiação periódica não recebe o caster da Raygun. Consequentemente, o dono do hit direto não transfere automaticamente crédito de kill, XP ou **Mastery** a cada tick de Irradiated.

Não foi identificado um projétil Gamma autônomo ou um timer próprio persistente do encantamento. O item usa sua stack, callbacks e estado de carga; a instância de status e o subsistema de efeitos têm seus próprios ciclos de vida. Esses limites não autorizam promessas de replay, reload, troca de mão, desconexão ou comportamento multiplayer.

## Sete eixos e fronteira de integração

| Eixo | Prova estática | Limite conservado |
|---|---|---|
| Identidade | JSON Gamma/X-Ray, tag Raygun, versão/JAR/classes SHA-exatos | Fonte 1.1.1 apenas adjacente; datapacks efetivos não verificados |
| Comportamento | Slot 18 e consumidores de dano/status/visual; método integral pinado | Não é novo cast nem execução de perk |
| Parâmetros | Máximo I, custos declarativos, 2F/1,5F, 800 ticks, amplifier 4/0 | Nível visual não é multiplicador do dano periódico |
| Targeting | Trace do item, AABB de lado 2, self/aliança/veículo, exceção Tremorzilla e resistência | Sem bônus próprio de range, autorização PvP/claims ou acerto garantido |
| Custos/tempo | Cadência servidor separada de aquecimento/consumo cliente; carga nativa | Sem débito Gamma próprio, cooldown inventado ou autorização C2S certificada |
| Integração | Fonte direta com caster; efeitos e feedback posteriores distintos | `NO_MUTATION`; sem duplicação de hit, recibo ou Mastery |
| Validação | Auditor reproduzível, selo, pivôs/branches e regressões da ficha/índices | `NOT_VERIFIED` para hooks; `NOT_TESTED` para QA física |

Black Arcana mantém seu runtime mágico e world safety. RPG Skill Tree pode fornecer progressão/perks somente através de contratos reais. A documentação localiza parâmetros úteis para design; não fornece um hook mutador homologado. Alterar dano, amplifier, duração, cadence ou targeting exige uma integração própria, respeitando a autoridade do provider e seus custos.

## Reprodução e validação

A [sonda](../../../../docs/qa/alexscaves_1010_gamma_ray_causal_audit.py), seus [testes do auditor](../../../../docs/qa/alexscaves_1010_gamma_ray_causal_audit_test.py), os [testes semânticos](../../../../docs/qa/alexscaves_1010_gamma_ray_causal_cards_test.py) e o [workflow](../../../../.github/workflows/alexscaves-1010-gamma-ray-causal.yml) permitem repetir a extração no JAR exato. O workflow também verifica o manifesto canônico e os índices.

O comando abaixo usa a variável `AC_GAMMA_JAR` apontando para o JAR com os hashes da tabela, e Java 21:

```bash
python3 docs/qa/alexscaves_1010_gamma_ray_causal_audit.py \
  --jar "$AC_GAMMA_JAR" --javap "$JAVA_HOME/bin/javap" \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GAMMA-RAY-CAUSAL-1.0.10.json' \
  --output build/gamma-ray-1010/gamma-ray-native-evidence.json
```

| Evidência final | Resultado local observado |
|---|---|
| Manifesto individual | 96.363 bytes; SHA-256 `cf36a14f33464b6bd75f476b03dc654f11b9fb0f9676ec6337cc442c7c1e2b7c` |
| Corpos causais selecionados | 12 métodos completos; 688 instruções; 72 branches diretos; 165 pivôs; seis classfiles identificados, cinco com métodos selecionados |
| Recursos | Quatro JSONs: Gamma, X-Ray, item Raygun e resistência à radiação |
| Visuais selecionados | Dois classfiles e dois métodos identificados por hash; 44 pivôs; CFG visual integral e pixels não verificados |
| Reprodução | CLI no JAR SHA-exato PASS; duas execuções byte-idênticas ao selo |
| Auditor | 14 testes PASS, incluindo rejeição de artefato, escopo, selo, constante de dano e seleção visual alterados, além de chaves JSON duplicadas |
| Regressão local | 1.539 testes Alex's Caves + 165 de catálogo = **1.704 PASS**, sem falhas, erros ou skips |
| Índices | 544 índices consistentes; conferência e geração canônica sem divergência |

Os testes do auditor estão incluídos na suíte Alex's Caves, não somados novamente ao total. A primeira regressão encontrou três expectativas de redação da fila alfabética; a expressão do crosswalk foi corrigida, mantendo os testes e seus gates nativos. A execução seguinte habilitou também os cenários opcionais do JAR físico e passou integralmente. Isso não é QA física de combate.


QA física permanece pendente: cliente/servidor completos, resistência/tag alterada, cargas e elapsed diversos, alvo Tremorzilla/comum, aplicação negada, latência, recarga/reload, PvP/claims e crédito de efeitos periódicos. CI e inspeção de bytecode não substituem esses cenários no modpack real.

Esta entrega acrescenta **um contrato técnico estático individual**, **zero raízes mágicas**, **zero hooks mutadores homologados** e **zero providers integralmente concluídos**. O provider e a Raygun continuam abertos; o próximo encantamento parcial é X-Ray.
