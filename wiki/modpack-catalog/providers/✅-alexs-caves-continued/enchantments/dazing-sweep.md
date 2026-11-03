# Dazing Sweep — atordoamento secundário do Primitive Club (publisher 1.0.10)

**Estado da ficha individual:** ⚠️ **parcial/condicionado**. O recurso do encantamento, a tag, o classfile produtor e os pontos JVM relevantes **já estão cobertos pelo contrato de efeitos SHA-exato**. Esta ficha consolida somente o consumidor de Dazing Sweep: `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `NO_MUTATION`. Nenhum runtime/provider, hook, Stage ou certificado foi alterado.

**Identidade funcional:** `alexscaves:dazing_sweep` modifica o **Primitive Club**: depois de um ataque que consegue aplicar `Stunned` ao alvo principal, o encantamento pode atingir outras entidades dentro de uma região delimitada, solicitar **1 ponto de dano corpo a corpo** por secundário elegível e tentar aplicar **Stunned por 80–159 ticks**. Não é um cast adicional, um novo `DamageType`, um projétil ou um atordoamento automático a cada ataque. O `Stunned` e suas consequências são do [efeito já catalogado](../effects/stunned.md).

## 1. Versão instalada, autoridade e provas reutilizadas

| Elemento | Evidência física do JAR 1.0.10 |
|---|---|
| Provider / mod ID | Alex's Caves Continued / `alexscaves`, Minecraft **1.21.1** / NeoForge |
| JAR exato | `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes** |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Recurso `data/alexscaves/enchantment/dazing_sweep.json` | SHA-256 `c86a7aceb5dfec02083dabc93ab51dc5253fbeb616c013a5f33f343656c26318` |
| Tag `data/alexscaves/tags/item/enchantable/primitive_club.json` | SHA-256 `71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43` |
| Classfile `server/item/PrimitiveClubItem.class` | SHA-256 `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac` |
| Efeito `server/potion/StunnedEffect.class` | SHA-256 `1ca7aea9ca512e10f2c06da58093e6197c57645ce2d32fc03cce0869d21a0a9e` |
| Mensagem de apresentação `server/message/UpdateEffectVisualityEntityMessage.class` | SHA-256 `4fb1a0200619ce7597470ebd500d6da12bd190a32910bde7ebbc6ac9e9298280` |

**Evidência canônica reutilizada, sem nova sonda ou download do JAR:** [`EXACT-EFFECT-CONTRACTS-1.0.10.json`](../EXACT-EFFECT-CONTRACTS-1.0.10.json) e [memorial do contrato](../EXACT-EFFECT-CONTRACTS-1.0.10.md), especialmente a ficha técnica [Stunned](../effects/stunned.md). O manifesto existente inclui o caminho e o SHA-256 do JSON Dazing Sweep, da tag e dos classfiles, além dos offsets compilados de `PrimitiveClubItem.acHurtEnemy`. O código deste encantamento já estava auditado como **consumidor do efeito**, mas faltava a ficha individual.

O repositório público adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão **1.1.1** e não é autoridade para o bytecode 1.0.10. Os **bytes específicos** de `dazing_sweep.json` (367 bytes) e da tag `primitive_club.json` (54 bytes) desse snapshot produzem, independentemente, os **mesmos SHA-256** selados no manifesto 1.0.10. Essa identidade vale **só para esses dois recursos**: não estabelece paridade de métodos, parâmetros binários de outras classes ou comportamento físico entre releases.

**Clean-room:** informações de identidade, parâmetros, assinaturas e localizadores de interoperabilidade; nenhum método ou recurso proprietário do provider foi copiado para o runtime Black Arcana.

## 2. Dados declarativos e aquisição do encantamento

| Campo do `dazing_sweep.json` físico | Valor |
|---|---|
| `description.translate` | `enchantment.alexscaves.dazing_sweep` |
| `supported_items` | `#alexscaves:enchantable/primitive_club` |
| `weight` | `2` — peso de aquisição, **não** probabilidade de Stunned |
| `max_level` | `2` — níveis I e II |
| `min_cost` | `base=1`, `per_level_above_first=10` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | `4` |
| `slots` | `mainhand` |
| `exclusive_set` | Não declarado no recurso |

O recurso da tag suporta **`alexscaves:primitive_club`**. A faixa declarativa de custo para nível I é **1–41**, para nível II **11–51**. Não confundir custo de enchanting/bigorna com carga de ataque, mana, cooldown, duração de stun ou dano.

O `PrimitiveClubItem` é o único owner da lógica de splash examinada; `StunnedEffect` tem outros produtores (incluindo itens, comida e mobs) documentados separadamente. Dazing Sweep **não** modifica esses outros produtores.

## 3. Producer compilado: ataque do Primitive Club

**Owner:** `com.github.alexmodguy.alexscaves.server.item.PrimitiveClubItem`, classfile SHA-256 acima.

**Entrada de ataque:** `hurtEnemy(ItemStack,LivingEntity,LivingEntity)Z`, descritor JVM `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z`; encaminha ao consumer `acHurtEnemy` de **mesmo descritor**. O manifesto SHA-exato preserva os dois métodos e seus offsets.

**Ordem causal de `acHurtEnemy` no bytecode publisher:**

1. `@0–6` solicita **1 de desgaste** da stack na mainhand por `ACCompat.hurtAndBreak`. Esse pedido antecede o guarda de lado do mundo e não é um custo extra criado por Dazing Sweep.
2. `@16` separa o trecho de efeito para **servidor** (`level.isClientSide`). `@36–44` obtém sorteio do alvo principal e exige `nextFloat() < 0.8F`. Trata-se de **80% de probabilidade nominal para entrar no ramo**, não probabilidade observada de controle efetivo: duração/elegibilidade e `addEffect` ainda podem falhar.
3. `@47–95` constrói `MobEffectInstance(STUNNED, 150 + nextInt(150), amplifier=0, ambient=false, visible=false)`, duração **150–299 ticks** (nominalmente **7,50–14,95 s** com 20 TPS), e solicita `hurtEntity.addEffect`. Caso o efeito **não seja aceito**, o fluxo não entra na varredura de Dazing Sweep.
4. `@101–119` comunica apresentação visual quando o `addEffect` principal foi aceito. Só depois é lido `ACEnchantmentRegistry.DAZING_SWEEP @136` e o nível com `ACCompat.enchantLevel @139`.
5. `@146` exige **nível inteiro positivo**. Nenhum clamp 0–2 é aplicado pelo consumidor antes de usar esse nível: `max_level=2` é restrição do recurso normal, não limite garantido para datapacks/comandos não convencionais.
6. `@149–170` calcula a dimensão `f=L+1.2F` e constrói `AABB.ofSize(primaryTarget.position(),f,f,f)`. `@175–204` consulta `Level.getEntities(attacker,aabb,Entity::canBeHitByProjectile)` e percorre os candidatos.
7. `@225–254` exclui o **alvo principal**, os candidatos `entity.isAlliedTo(attacker)`, os que excedem `distanceTo(primaryTarget)>f` e os que não são `LivingEntity`. A consulta recebe o atacante como argumento e o predicado de projétil; não equivale a um seletor de alvos de Black Arcana.
8. Para cada secundário restante, `@264–299` constrói **Stunned 80 + nextInt(80) ticks** (**80–159 ticks; 4,00–7,95 s** a 20 TPS), amplifier 0 e flags false. `@308–319` solicita **1.0F** de dano via `DamageSources.mobAttack(attacker)`; `@327` tenta `secondary.addEffect`. O retorno booleano de `secondary.hurt` **não condiciona** a tentativa de Stunned.
9. `@330–355` envia a mensagem visual **somente se** o `addEffect` secundário foi aceito. A sequência não possui verificação própria de linha de visão nem hook de autorização de perks.

**Atenção às probabilidades:** os secundários **não** executam outro `nextFloat()<0.8` no laço. O gate aleatório é o **primeiro Stunned**, seguido da aceitação do efeito principal; o sorteio de cada secundário nesta janela é para **duração**, não uma nova chance percentual de aplicação. Uma falha de dano secundário não impede automaticamente a tentativa de status.

## 4. Geometria correta, níveis e seleção

Defina `L=level(DAZING_SWEEP)`. A expressão comprovada é `f=L+1.2F` e **a mesma variável** é passada aos três eixos de `AABB.ofSize`:

| Encantamento | `L` | Lado X/Y/Z da AABB | Semiextensão geométrica em cada eixo | Gate adicional de distância |
|---|---:|---:|---:|---:|
| Ausente | 0 | **Não executa sweep** | — | — |
| I | 1 | **2.2 blocos** | **1.1 bloco** | `distanceTo(primary) <= 2.2F` |
| II | 2 | **3.2 blocos** | **1.6 bloco** | `distanceTo(primary) <= 3.2F` |

`AABB.ofSize(center,f,f,f)` recebe **comprimentos totais**, não raios. A consulta de entidades é baseada na interseção de suas bounding boxes com a AABB, e há um filtro adicional de distância entre entidades. Portanto, **nem 2,2/3,2 são raios esféricos garantidos, nem 1,1/1,6 são limites de alcance absoluto para entidades com bounding box grande**. Não converter para um círculo de raio `f`, explosão ou área de dano universal.

O pipeline aplica os gates adicionais do provedor: `Entity.canBeHitByProjectile`, exclusão do alvo principal, aliança `candidate.isAlliedTo(attacker)`, `distanceTo` e `instanceof LivingEntity`. **Não** testa explicitamente a aliança no sentido `attacker.isAlliedTo(candidate)`, linha de visão, permissões de claim, classe específica de criatura, limite máximo de vítimas ou aceitação final de dano. O mecanismo original tem **busca local delimitada geometricamente**, mas sem um teto numérico independente para a quantidade de candidatos encontrados; isso importa para budgets e XP.

Uma perk que aumente `L` fora do máximo de dados pode aumentar a AABB e o custo de varredura. **Não há limite nem clamp extra neste método**, logo não promover escalabilidade ilimitada baseada somente nessa expressão.

## 5. Dano, Stunned e consumidores downstream

A solicitação `mobAttack(attacker)` com **`1.0F`** é uma chamada de **dano corpo a corpo nativo** por secundário, não uma escola mágica ou um tipo novo `dazing_sweep`. O valor solicitado é **antes** de armadura, invulnerabilidade, resistências, PvP, eventos e proteções, portanto não indica perda de vida garantida.

**Duração do efeito:** alvo principal `150–299` ticks; secundários `80–159` ticks. Esses intervalos não são períodos de cooldown, frequência de dano nem duração de uma área persistente: o sweep ocorre dentro do consumidor de acerto; `Stunned` continua seu próprio lifecycle depois.

O [contrato próprio de Stunned](../effects/stunned.md) registra modifier negativo de velocidade, intervenções de movimento/AI e cancelamento de determinados danos originados **diretamente** de entidades atordoadas. Essas consequências pertencem ao **efeito**; não devem ser executadas outra vez por um perk que apenas modifique Dazing Sweep. O efeito também é consumido por mecânicas específicas de criaturas e por rotas de remoção/alimentação. Ampliar sua aplicação pode alterar sistemas fora do combate com o Club.

A mensagem `UpdateEffectVisualityEntityMessage` do provider sinaliza a apresentação visual de uma instância **aceita** e é enviada para o alvo principal e secundários nos ramos correspondentes. Sua existência não transforma um packet de renderização em autorização de status, reescrita de duração ou contagem de hits por Black Arcana.

## 6. Matriz de parâmetros para integração de perks

| Eixo | Evidência estática 1.0.10 | Regra de segurança |
|---|---|---|
| **Probabilidade** | `nextFloat()<0.8F` somente no alvo primário | ⛔ Nenhum hook verificado para mudar `0.8` ou garantir `addEffect` |
| **Duração do controle** | Primário `150–299`, secundário `80–159` ticks, amplifier `0` | ⛔ Sem alteração de instâncias, renovação indiscriminada ou stacks sem contrato |
| **Range / AoE** | AABB lado `L+1.2F` centrada no alvo; filtro `distanceTo<=f` | ⛔ Sem confundir lado de caixa e raio; mutações precisam de budget e PvP/claims |
| **Targeting** | Predicado `canBeHitByProjectile`, exclusão do alvo principal, aliança em um sentido e `LivingEntity` | ⛔ Não converter em homing, área global, seleção por categoria ou permitir aliados sem contrato |
| **Dano e tipo** | Pedido de `mobAttack(attacker)` `1.0F` por secundário; `hurt` pode falhar independentemente de `addEffect` | ⛔ Sem segunda cobrança, segunda aplicação de status nem duplicação do settlement |
| **Projétil / velocidade / hitbox** | O sweep do Club **não cria entidade-projétil** nem altera dimensão de entidades | N/A para resize e velocidade; não importar fórmulas do Dreadbow/Arrow |
| **Custo e cooldown** | `hurtAndBreak(...,1,MAINHAND)` no início de `acHurtEnemy` | ⛔ Sem mana/cooldown novo deduzido; frequência real depende do ataque nativo |
| **Mastery / XP / proc** | Uma tentativa de ataque pode produzir múltiplas solicitações de dano e status | ⛔ Não premiar XP por candidato ou mensagem; exigir autoria, resultados aceitos e dedupe |
| **Persistência / reload** | `MobEffectInstance` delega duração e lifecycle ao sistema nativo | ⛔ Sem duração/reaplicação compensatória de Black Arcana sem evidência física |
| **Segurança de mundo** | Não há alteração de blocos neste consumidor delimitado | WorldEffectPolicy continua obrigatório caso outra perk introduza efeito destrutivo |

**Autoridade:** Black Arcana controla seu runtime mágico e efeitos de mundo. RPG Skill Tree fornece progressão, atributos, Mastery, perks e gates via **contratos reais**, sem substituir o consumidor `PrimitiveClubItem` ou o runtime `StunnedEffect`. Sem um seam seguro provado: **fail-closed**. Não implementar um novo scan por tick, pipeline de dano ou packet próprio baseado apenas nesses localizadores JVM.

## 7. Certificação, QA e contabilidade

**Comprovado estaticamente pelo manifesto exato já existente:** identidade do recurso e tag; parâmetros de nível/slots/custo; `PrimitiveClubItem.class` e métodos `hurtEnemy/acHurtEnemy`; gate do lado servidor, chance primária `0.8F`, aceitação de `addEffect`, dimensão da AABB, filtros de seleção, durações secundárias, `mobAttack(...,1F)`, ordenação de `hurt/addEffect` e notificação de efeito.

**Não comprovado por teste físico:** taxas reais de stun; necessidade de ataque completamente carregado; modificação de vanilla/Forge event handling; ordem client/server no pack; proteção PvP/claims; hitboxes e alvos de outros mods; efeitos já ativos/Immunity; expiração e remoção; número de vítimas, rede de mensagens e duplicações; sincronização entre mãos; duração efetiva em baixa TPS; estabilidade de níveis inválidos; efeitos de Mastery e hooks de perks.

**Estados finais desta entrada:** `resource_and_consumer_evidence=EXACT_BINARY_EXISTING`; `individual_partial_dossier=YES`; `individual_full_certification=NO`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `perk_certification=NOT_CERTIFIED`; `NO_MUTATION`. A ficha adiciona **uma entrada documental parcial** ao denominador de fichas observadas, **zero** contratos estáticos certificados, **zero** novas raízes mágicas, **zero** providers concluídos.

**Próxima entrada alfabética:** `alexscaves:detonating_death`.
