# X-Ray 1.0.10 — targeting e fechamento estático dos 51 recursos publisher

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
version=1.0.10
enchantment=alexscaves:x_ray
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
perk_certification=NOT_CERTIFIED
mutation=NO_MUTATION
whole_provider_catalog_closed=false
```

A [ficha individual](enchantments/x-ray.md) conclui os sete eixos documentais de X-Ray no publisher SHA-exato. O [manifesto causal](EXACT-XRAY-CAUSAL-1.0.10.json) revalida os contratos compartilhados de [Gamma Ray](EXACT-GAMMA-RAY-CAUSAL-1.0.10.json) e [Energy Efficiency](EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json), acrescentando prova própria do booleano, extremos, busca segmentada, fallback e registry de X-Ray. Nenhuma dessas provas certifica a Raygun inteira, o alcance físico de um hit ou um hook mutador.

## Artefato e identidades

| Campo | Valor publisher |
|---|---|
| Release | `alexscaves-1.0.10-neoforge+1.21.1.jar`; CurseForge arquivo 8856293 |
| Plataforma | Minecraft 1.21.1 / NeoForge / Java 21 |
| Tamanho | 75.279.314 bytes |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Raygun class SHA-256 | `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| Registry class SHA-256 | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |
| `onUseTick` | 523 instruções / 57 branches diretos |
| Digest normalizado do método | `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5` |

O descritor é `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`. O censo literal de `X_RAY` encontra apenas `ACEnchantmentRegistry` e `RaygunItem`; os consumidores visuais compartilhados permanecem sob o contrato de Gamma. A presença de nomes não é usada como prova de atravessamento de blocos.

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é apenas adjacente. O novo selo preserva os hashes das provas anteriores. A [prova histórica de janelas de targeting](EXACT-RAYGUN-XRAY-TARGET-1.0.10.json), a [análise de condicionais](EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json) e os [consumidores](EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) mantêm seus bytes e limites; não são reclassificados retroativamente como CFG integral.

## Definição e binding de registry

`data/alexscaves/enchantment/x_ray.json` tem 406 bytes e SHA-256 `612b1f7b126cea12085dea00736115b05fd4789bf9fc9ff6c4344a427135b0f8`.

| Campo | Valor |
|---|---|
| `description.translate` | `enchantment.alexscaves.x_ray` |
| `supported_items` | `#alexscaves:enchantable/raygun` |
| `max_level` / `weight` | 1 / 10 |
| `min_cost` | base 1; incremento 12 por nível acima do primeiro |
| `max_cost` | base 41; incremento 10 por nível acima do primeiro |
| `anvil_cost` / `slots` | 1 / `mainhand` |
| `exclusive_set` | `["alexscaves:gamma_ray"]` |

A tag publisher contém `alexscaves:raygun`. O JSON de Gamma não possui `exclusive_set` próprio; a exclusão é declarada aqui por X-Ray. Isso não comprova a configuração final de datapacks, editores ou stacks criadas por outros mods. Custos de encantamento não são mana, gasto por alvo ou cooldown da arma.

No inicializador compilado da registry, `String x_ray @194` passa por `key @197` e é armazenada em `X_RAY @200`. O helper `key` usa `Registries.ENCHANTMENT` e o namespace `alexscaves`. O auditor sela os seis comandos de `key` e o inicializador de 182 instruções. Para o parser identificar `static {}`, sua declaração é normalizada em memória; não há reescrita do classfile ou mudança do runtime.

## Booleano, distância e extremos

`X_RAY @44` → `ACCompat.enchantLevel @47` → `ifle @50` normaliza o nível positivo para 1, e os demais valores para 0. O local inteiro 9 tem escrita única em `@58` e leituras em `@105`, `@122` e `@569`. Níveis positivos forçados acima de I continuam selecionando o mesmo caminho; não existe multiplicação do range por esse nível.

O fluxo da distância é separado:

1. `elapsed=getUseDuration(stack,null)−remainingUseTicks`.
2. Progresso local 7: `elapsed/15F` se elapsed<15; caso contrário 1F. Esse trecho não adiciona clamp inferior.
3. Distância local 8: `r=25F×progresso`, escrita em `@41` e usada nos traces/caixa de busca.
4. `ProjectileUtil.getHitResultOnViewVector @69` produz o resultado inicial no local 10.
5. `LivingEntity.pick(r,0F,false) @80` produz outro resultado no local 11.
6. `eyePosition+getViewVector(0F)×r` produz o extremo geométrico no local 12, em `@103`.

| Local | Com X-Ray | Sem X-Ray |
|---|---|---|
| 13, seleção `@105–120` | local 12 | local 11.getLocation() |
| 14, seleção `@122–137` | local 12 | local 11.getLocation() |

Essas duas seleções não são um único parâmetro de alcance. O caminho cliente usa componentes do local 13 para `setRayPosition @233`; o local 14 será usado pela consulta de dano. Estado local, escrita solicitada e representação no cliente não comprovam entrega efetiva ou autoridade da rede.

## Busca segmentada e fallback

Com X-Ray, `@569–666` executa a busca adicional. Sem X-Ray, `ifeq @571 → 669` a contorna.

| Operação | Contrato nativo |
|---|---|
| Caixa de busca | `usuario.getBoundingBox().inflate((double)r)` em `@575–584`, expandida por r em cada direção |
| Inicialização | contador float local 23=1F; posição local 24=eyePosition |
| Condição | `local23<r`, comparada em `@595–600` |
| Início do segmento | `local24=local24+getViewVector(1F)`, armazenado em `@613` |
| Fim do segmento | `local25=local24+getViewVector(1F)`, armazenado em `@625` |
| Busca | `ProjectileUtil.getEntityHitResult(level,usuario,local24,local25,local22,predicate) @640` |
| Retorno não nulo | Substitui local 10 em `@652`; `goto @654 → 666 → 734` encerra a busca |
| Retorno nulo | Soma 1F ao contador em `@657–661` e volta para a condição |

O primeiro segmento adicional começa após a primeira soma do vetor de visão: eye+view(1F) até esse ponto+view(1F), sem acrescentar um segmento inicial eye→eye+view. As chamadas de visão são explícitas, não um snapshot persistente de cast. Se o helper devolver um resultado, o laço para no **primeiro segmento com retorno não nulo**. Não há nesse laço comparação própria para determinar uma entidade globalmente mais próxima entre todos os segmentos.

Se nenhum segmento devolver resultado, o local 10 permanece o resultado inicial de `@69`; ele não é substituído por null ou pelo último segmento. O helper e os filtros externos podem determinar resultados que não se inferem apenas da geometria da caixa. Não se promete quantidade de iterações realmente executadas, hits aceitos ou penetração física em obstáculos específicos.

## Blocos, impacto visual e centro da consulta de dano

O caminho sem X-Ray em `@669–732` verifica `BlockHitResult`, lê sua posição/direção e o estado do bloco; `!isAir && isFaceSturdy(level,pos,direction)` prepara o local 21 com o ponto de impacto. X-Ray salta esse bloco por `@666 → 734`. Não há nesse salto uma autorização de claims, mutação de blocos ou garantia universal de atravessamento.

Os dois caminhos se juntam em `@734`. Se o resultado final do local 10 for `EntityHitResult`, `getEntity().position() @754` preenche local 21; a direção passa a `UP` e `@766` reescreve local 14. O centro é a posição da entidade, não necessariamente o ponto de interseção geométrica do trace.

`ifnull @770 → 874` verifica o local 21 e pula a preparação de impacto visual quando ele é nulo. **Não impede a consulta final de dano.** Essa consulta tem seus próprios gates servidor/cadência e usa o local 14 já selecionado. Sem resultado final de entidade, X-Ray pode manter o extremo geométrico no local 14, mesmo quando o resultado inicial preservado era de bloco; isso ainda não garante uma vítima elegível.

O volume de dano é `AABB(local14+(-1,-1,-1),local14+(1,1,1))`, em `@891–917`: cubo de lado 2. Não é o mesmo volume da caixa de busca inflada por r, uma esfera ou a largura de uma entidade projétil. Identidade do usuário, aliança nas duas direções, mesmo veículo e o predicate nativo continuam filtrando candidatos.

Os slots JVM têm lifetimes tipados: o índice 23 é float no laço (`fstore @587/@661`), referência `BlockPos` no caminho normal (`astore @689`) e amplifier inteiro no status (`istore @932`). Não se transforma uma reutilização de índice em uma relação causal entre contador, posição e dose de radiação.

## Custos, efeitos, autoria e integração reutilizados

O contrato de Gamma revalidado pelo novo auditor mantém separados:

- Consumo cliente de `ChargeUsed`, limite 1000, Energy Efficiency e seu aquecimento; não há custo extra próprio de X-Ray.
- Tentativas de dano no servidor por `(elapsed−15)%3==0`, sem uma condição adicional elapsed>=15 nesse gate.
- Dano solicitado 1,5F ou 2F selecionado por Gamma, não um bônus numérico de X-Ray.
- Fonte direta com o usuário, exceção Tremorzilla, resistência à radiação, solicitação de Irradiated por 800 ticks e aceitação do efeito antes do feedback visual.
- Dano posterior de [Irradiated](effects/irradiated.md), cuja frequência e autoria não são as do hit direto. O nível visual não é um multiplicador de dano, e o caster não é automaticamente transferido à fonte Radiation periódica.

X-Ray altera a configuração de targeting e pode influenciar indiretamente os candidatos consultados; não se converte isso em dano aceito, kill, lifesteal, XP ou **Mastery**. Black Arcana mantém seu runtime e world safety; RPG Skill Tree integra progressão por boundaries reais. Os helpers localizados são evidências para desenho de perks, sem mutação homologada.

Projétil autônomo, sua velocidade/tamanho/homing, timer, mana e cooldown **próprios de X-Ray** são N/A neste contrato: o pipeline usa o item, traces e consultas nativas. Estado e duração de uso da Raygun e status nos alvos têm consumidores próprios. Salvar dados, enviar mensagens ou ter um setter não comprova recepção autorizada, persistência após reload ou cleanup multiplayer. A [ficha integral da Raygun](damage-types/raygun.md) continua parcial, com rede/codec/autoridade ainda delimitados.

## Sete eixos do certificado estático

| Eixo | Evidência | Limite conservado |
|---|---|---|
| Identidade | JSON/tag/registry, JAR e métodos SHA-exatos | Fonte pública 1.1.1 apenas adjacente; datapacks efetivos pendentes |
| Comportamento | Booleano 9, extremos 12/13/14, laço, primeiro retorno e fallback | Não cria outro cast nem garante alvo globalmente mais próximo |
| Parâmetros | Nível I/custos declarativos, r=25F×progresso, passo1F | Range numérico não é alcance físico de dano garantido |
| Targeting | Caixas de busca e de dano separadas, posição da entidade e filtros | Não equivale a penetrar qualquer parede, ignorar claims ou confirmar hit |
| Custos/tempo | Charge e Energy Efficiency reutilizados; cadência de servidor separada | Sem débito Gamma/X-Ray extra ou cooldown inventado |
| Integração | Fonte direta, efeitos e feedback distintos; scopes Raygun/Gamma preservados | `NO_MUTATION`; sem novo recibo ou Mastery por trace/partícula |
| Validação | Selo, reprodução e regressões semânticas/negativas; censo dos 51 recursos | Hooks `NOT_VERIFIED`; QA física `NOT_TESTED`; provider ainda aberto |

## Fechamento dos 51 JSONs publisher

O novo selo inclui o conjunto exato `data/alexscaves/enchantment/*.json`: **51 caminhos, 51 IDs e seus 51 SHA-256**. Os IDs coincidem com `remaining_family_inventory.enchantment_ids` do [inventário de famílias](INTEGRATION-SCOPE-INVENTORY-1.0.10.json). A verificação documental compara esse conjunto com os 51 caminhos de fichas do ledger e seus certificados estáticos individuais.

Com X-Ray, esse recorte fica **✅ 51/51 — 100% do catálogo estático dos recursos publisher**, com zero fichas parciais de encantamentos. O [índice da família](enchantments/INDEX.md) e o [crosswalk](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md) registram o fechamento. Isso não é fechamento da registry/runtime sob qualquer datapack ou de todos os sistemas do mod.

`publisher_json_static_catalog_complete=true` descreve somente esse recorte. `family_universe_closed=false` e `whole_provider_catalog_closed=false` conservam a fronteira mais ampla. A ficha observada de [Raygun](damage-types/raygun.md) permanece parcial. O [DamageType Tremorzilla Beam](damage-types/tremorzilla-beam.md) já tem [certificação estática individual](EXACT-TREMORZILLA-BEAM-STATIC-1.0.10.md), preservada nesta entrega; ela não certifica a entidade inteira. Não se avança o provider alfabético nem se promove hook, QA física ou Stage por completar estes 51 recursos.

## Reprodução e validação

O [auditor](../../../../docs/qa/alexscaves_1010_xray_causal_audit.py), os [testes nativos](../../../../docs/qa/alexscaves_1010_xray_causal_audit_test.py), os [testes semânticos](../../../../docs/qa/alexscaves_1010_xray_causal_cards_test.py) e o [workflow](../../../../.github/workflows/alexscaves-1010-xray-causal.yml) permitem reexecutar a prova. Defina `AC_XRAY_JAR` para o artefato com os hashes da tabela e use Java 21:

```bash
python3 docs/qa/alexscaves_1010_xray_causal_audit.py \
  --jar "$AC_XRAY_JAR" --javap "$JAVA_HOME/bin/javap" \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-XRAY-CAUSAL-1.0.10.json' \
  --output build/xray-1010/xray-native-evidence.json
```

| Evidência final | Resultado local observado |
|---|---|
| Manifesto individual | 78.375 bytes; SHA-256 `158f03ac7f0369f0a5d90113493ff41314e3d55ea0388a903bd47caf3355aaff` |
| Seleção própria | `onUseTick` 523 instruções/57 branches; helper `key` 6/0; inicializador da registry 182/0; 189 pivôs e 21 edges diretos selecionados |
| Contratos reutilizados | 12 métodos causais e dois consumidores visuais de Gamma; `onUseTick` é comum às seleções, não um corpo novo contado em duplicidade |
| Roster publisher | 51 JSONs com nomes e hashes, comparados ao inventário e aos 51 certificados de fichas |
| Reprodução | CLI obrigatória no JAR exato PASS; evidência byte-idêntica ao selo em execuções repetidas |
| Auditor e semântica | 15 testes nativos + 12 testes semânticos PASS; negativos de artefato, escopo, branch, registry, recurso, roster e JSON duplicado |
| Regressão local | 1.639 testes Alex's Caves + 165 do catálogo = **1.804 PASS**, sem falhas, erros ou skips |
| Índices | 544 índices consistentes; geração canônica conferida |

Os testes focados estão incluídos na suíte Alex's Caves, sem nova soma ao total. A execução local habilitou os cenários opcionais de CLI contra o JAR físico de Gamma e X-Ray; não executa combate ou prova aceitação no modpack.

A integração preserva a certificação de Tremorzilla Beam e as provas recentes da Raygun já presentes na base `6cc7dc6aa99b6dc80840b87e4a978e2c580c481d`. O checkpoint histórico de nove contratos de dano continua intacto no inventário, acompanhado de campos explícitos para os dez certificados atuais. O resultado corrente é 80/81 contratos observados, não uma conclusão integral do provider.


QA física continua pendente: combinações de carga, elapsed e nível; obstáculos/formas de bloco, entidades próximas e múltiplas por segmento, aliados/veículos e Tremorzilla; recusa de dano/efeito, tipos de alvo, datapacks e stacks forçadas; servidor dedicado/multiplayer, rede, reload, PvP/claims e crédito único de Mastery. Inspeção de bytecode e CI não certificam esses resultados no modpack real.

Contabilidade da entrega: um contrato estático individual acrescentado a uma ficha existente; zero raízes mágicas, zero hooks mutadores homologados, zero QA física e zero providers integralmente encerrados. O fechamento de 51/51 pertence exclusivamente ao recorte publisher de encantamentos descrito acima.
