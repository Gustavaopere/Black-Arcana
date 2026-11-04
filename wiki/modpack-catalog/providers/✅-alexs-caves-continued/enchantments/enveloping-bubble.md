# Enveloping Bubble — Water Bolt com aplicação de Bubbled (1.0.10)

**Estado individual:** ⚠️ **parcial/condicionado para perks**; identidade do JSON, campos declarativos, produtor, flag, solicitação de dano e efeito downstream rastreados com evidência estática do **JAR publisher exato 1.0.10**. **Não** é uma magia autônoma nem uma nova raiz de casting: altera a ação `sea-staff-water-bolt` do `alexscaves:sea_staff`.

**Certificação de integração:** `perk_certification=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `mutation=NO_MUTATION`. Os contratos estáticos certificados da ação **não certificam automaticamente um novo hook de perk** ou observação real no modpack.

## 1. Identidade e proveniência física

| Elemento | Evidência da versão instalada |
|---|---|
| Mod / ID | Alex's Caves Continued / `alexscaves` |
| Modlist | [RPG Skill Tree, modlist atual](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada #019: `alexscaves-1.0.10-neoforge+1.21.1.jar` |
| Loader / runtime alvo | Minecraft **1.21.1**, NeoForge, Java 21 |
| JAR publisher físico | **75.279.314 bytes**; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| ID do encantamento | `alexscaves:enveloping_bubble` |
| Recurso embarcado | `data/alexscaves/enchantment/enveloping_bubble.json` |
| SHA-256 embarcado | `d984c8cc3f8d72bffa2fce0972a2449b393907f7686626cc6135bf2a8260ed5a` |
| Item / tag | `alexscaves:sea_staff` / `#alexscaves:enchantable/sea_staff` |
| Tag embarcada | `data/alexscaves/tags/item/enchantable/sea_staff.json`, SHA-256 `22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e` |
| Efeito downstream | `alexscaves:bubbled`, implementado por `BubbledEffect` |

Fontes internas: [manifesto SHA-exato de ações e recursos](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json), [ação Sea Staff — Water Bolt](../actions/sea-staff-water-bolt.md), [efeito Bubbled](../effects/bubbled.md), [inventário dos 51 encantamentos](../INTEGRATION-SCOPE-INVENTORY-1.0.10.json).

**Comparação externa restrita e verificável:** o texto UTF-8 de **367 bytes** em `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`, caminho `src/main/resources/data/alexscaves/enchantment/enveloping_bubble.json`, apresenta **o mesmo SHA-256 `d984…0ed5a` do recurso publisher selado**. Portanto, **os bytes desse JSON declarativo coincidem** com a identidade física registrada para o publisher 1.0.10. O repositório público declara versão **1.1.1**: a correspondência do **arquivo JSON específico** não torna classes Java, lógica de execução, tags de terceiros ou build 1.1.1 equivalentes à 1.0.10. Os valores Java abaixo vêm do manifesto do binário instalado, não dessa fonte adjacente.

## 2. Campos do encantamento, JSON exato

| Campo | Valor do recurso com SHA-256 correspondente |
|---|---|
| `description.translate` | `enchantment.alexscaves.enveloping_bubble` |
| `supported_items` | `#alexscaves:enchantable/sea_staff` |
| `weight` | **2** — peso de encantamento, não probabilidade de criar bolha |
| `max_level` | **1** |
| `min_cost` | `base=1`, `per_level_above_first=13` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | **4** |
| `slots` | `["mainhand"]` |
| `exclusive_set` | **Não declarado neste arquivo**; isso não certifica todas as combinações com outros encantamentos |

A tag física do Sea Staff lista `alexscaves:sea_staff`. Custos `min_cost/max_cost/anvil_cost` são **custos de aquisição/encantamento**, não um débito de mana, durabilidade ou cooldown de cada projétil. `max_level=1` é o limite declarado do JSON; comportamento de níveis inválidos, overrides por datapack e compatibilidade com outros sistemas de encantamento não foram testados.

## 3. Produtor e ativação — `SeaStaffItem.use`

**Classe produtora:** `com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.class`, SHA-256 `cb3153a35e7f4c3ab23e68693aec110edf03ecd050c3b485e35ccbb257b4bbc6`.

**Método:** `use(Level,Player,InteractionHand)InteractionResultHolder`, descritor JVM `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;`.

A [ação-base SHA-exata](../actions/sea-staff-water-bolt.md) já identifica `use @74–355` como ramo de criação no servidor, com owner e UUID opcional do alvo. Para **cada** `WaterBoltEntity` criado nesse loop:

1. `use @272–294` consulta `ACEnchantmentRegistry.ENVELOPING_BUBBLE` via `ACCompat.enchantLevel`.
2. Com nível positivo, solicita `RandomSource.nextBoolean() @289` e alimenta `WaterBoltEntity.setBubbling(Z) @294`. No lançamento comum, isso representa uma **decisão booleana aleatória por bolt**, com duas saídas equiprováveis na API usual; **não** é uma chance de `weight=2`, bônus percentual por nível ou aplicação garantida por tiro.
3. O bolt recebe `shootFromRotation` do item (velocidade inicial **2F** no central, **1F** nos laterais, imprecisão **12F**), o `seekAmount` próprio da ação e, se houver candidato, `setArcingTowards(UUID)`. São operações do **Water Bolt**; o encantamento não demonstra alterar diretamente velocidade, hitbox, homing, distância ou quantidade de bolts.
4. `Level.addFreshEntity @345` solicita o spawn. A chamada compilada não comprova que o mundo aceitou cada entidade, nem que cada bolt alcançou e atingiu um alvo.

**Multiplicação já nativa:** `TRIPLE_SPLASH > 0` muda o loop da ação de **1 para 3 bolts** com yaw adicional `0/-50/+50°`; o teste de Enveloping Bubble ocorre dentro do loop. Assim, um mesmo cast pode gerar múltiplas decisões de `Bubbling`. Isso **não** certifica quantidade de hits aceitos, dano efetivo, independência estatística entre execuções ou compatibilidade de combinações alteradas. `TRIPLE_SPLASH` e `BOUNCING_BOLT` têm suas próprias regras; não são raízes de cast adicionais.

## 4. Consumidor — dano, alvo e aplicação de `BUBBLED`

**Classe consumidora:** `com/github/alexmodguy/alexscaves/server/entity/item/WaterBoltEntity.class`, SHA-256 `342c011b0178e1f65cd2e6ef315fe6bad49bd5ead237b2274e822560e2eac401`. **Método:** `damageMobs()V`.

| Região | Contrato estático da versão 1.0.10 |
|---|---|
| `damageMobs @27` | Cria fonte vanilla `DamageSources.mobProjectile(this, owner LivingEntity ou null)`. Não introduz `DamageType` próprio do Enveloping Bubble |
| `@35`, `@90–126` | Enumera `LivingEntity` na **AABB do bolt inflada 2D em cada eixo** e exclui owner, aliados, aliados do owner e `DeepOneBaseEntity` |
| `@133–139` | Solicita `ACCompat.hurt(target,damageSource,3F)`; **3F solicitado** não é HP líquido perdido |
| `@133–181` | **Somente com dano aceito** pelo caminho `hurt` e flag `isBubbling()` verdadeira, solicita `new MobEffectInstance(ACEffectRegistry.BUBBLED,200)` e `LivingEntity.addEffect` |
| `@184–213` | Envia `UpdateEffectVisualityEntityMessage` com tipo **1** e duração **200** em caminho condicionado; o pacote não é prova autônoma de dano/efeito efetivo |

**Duração nominal = 200 ticks** (10 segundos a 20 TPS), não 200 ticks garantidos após a aplicação. O contrato de [Bubbled](../effects/bubbled.md) descreve limpeza antes da expiração ao entrar em fluido e outras origens da mesma instância. A aplicação é por **alvos elegíveis que receberam o processamento do bolt**, não necessariamente o alvo usado para homing, nem uma área circular de 2 blocos. A AABB inflada é um volume de busca; não é tamanho, raio ou velocidade física do projétil.

**Persistência e ricochete:** o bolt sincroniza `Bubbling` por getters/setters. Os overrides NBT observados leem/escrevem **somente** `Bubbling`, sem persistir ali `seekAmount`, `ricochet`, UUID de alvo ou `dieIn`; um reload não tem restauração total do cast certificada. Se `BOUNCING_BOLT` ocasionar a criação de um filho, `onRicochetHit @254–257` copia a flag `Bubbling`; o filho não recebe `ricochet=true` nem copia `seekAmount` alterado. Esse filho pode ser mais um **downstream da mesma ação**, não um novo casting ou uma nova cobrança. Nem o spawn do filho nem novo dano são garantidos.

**Causalidade:** dano negado pelo engine/proteções **não equivale** a efeito Bubbled aplicado. Notificação visual, estado `Bubbling=true`, tick da entidade ou `addFreshEntity` não são comprovantes de `hurt=true`, aceite de `addEffect`, atribuição de kill ou permissão de PvP. Não repetir efeito por observação de rede.

## 5. O que `BubbledEffect` faz depois da aplicação

O encantamento é **um dos possíveis produtores** de `Bubbled`; a instância segue sob autoridade do efeito. Segundo o [contrato exato Bubbled](../effects/bubbled.md):

- `BubbledEffect.shouldTick` solicita processamento a cada tick de efeito; o amplifier não é usado no corpo `tick(LivingEntity,int)`. Não se pode assumir que nível ou amplifier aumente os efeitos.
- Para alvo **aquático** ou com capacidade de respirar sob água e **fora** de `RESISTS_BUBBLED`, repõe ar ao máximo e pode adicionar velocidade vertical `(0,-0.08D,0)` quando fora do chão; o ramo resistente não cai no ramo de sufocamento.
- Para alvo **não aquático**, sem `Water Breathing` e sem invulnerabilidade de jogador, aplica fator horizontal aproximadamente **0.8F** e reduz ar em **2** até **-20**; quando chega ao limiar, solicita `drown(),2F` e partículas, sem garantir perda líquida de vida.
- `CommonEvents.livingTick` remove Bubbled em **qualquer fluido reconhecido** por `ACFluids.isInAnyFluid` na inspeção exata, e `DeepOneMageEntity` também possui caminho independente de autoaplicação/remoção. Portanto, **nem toda instância Bubbled veio de Enveloping Bubble**.
- `UpdateEffectVisualityEntityMessage` contém handler capaz de adicionar/remover uma instância do efeito no lado de recepção, além de som/visual; não classificar cegamente esse pacote como exclusivamente cosmético. Credenciais, direção/autorização integral e deduplicação ainda requerem QA.

O dano de afogamento solicitado pelo efeito é **um caminho posterior distinto** do dano `mobProjectile` pedido pelo bolt, com condições e fonte de dano diferentes. Perks devem evitar contabilizar um segundo cast ou múltiplos procs ofensivos a partir da mesma raiz sem contrato de causalidade real.

## 6. Parâmetros relevantes para integração de perks

| Dimensão | Dado confirmado | Limite / estratégia |
|---|---|---|
| **Trigger / origem** | `SeaStaffItem.use` no servidor → `WaterBoltEntity`; campo positivo de encantamento governa o RNG da flag | Respeitar a única raiz; **não** realizar novo cast Black Arcana no impacto |
| **Chance / condicionais** | Uma decisão booleana por bolt encantado, e efeito só após dano aceito e flag ativa | Não prometer 50% dos alvos atingidos nem garantias de aplicação |
| **Quantidade de projéteis** | 1 baseline ou 3 com Triple Splash; Enveloping Bubble não cria bolts adicionais por si | Não duplicar disparos/charge, não criar outra raiz |
| **Velocidade / alcance** | 2F central, 1F lateral, precisão 12F; aquisição por helper com argumento 128D | Não confundir argumento de targeting com alcance máximo do projétil |
| **Área / raio / tipo de alvo** | AABB do bolt inflada 2D por eixo, filtro de aliados/owner/Deep One; `LivingEntity` elegível | Não certificar raio circular nem permitir bypass de aliados |
| **Dano do impacto** | `mobProjectile` com solicitação 3F por victim processada | Não certificar dano líquido, crítico ou escola; não duplicar `hurt` |
| **Debuff / duração** | `BUBBLED` com 200 ticks solicitados, amplifier padrão | Não reaplicar sem guard; duração efetiva depende de fluidos, imunidade/limpeza e ciclo vanilla |
| **Dano posterior** | `BubbledEffect` pode solicitar `drown(),2F` após redução de ar em condições específicas | Evento downstream distinto; autoria/proc/Mastery não certificados |
| **Durabilidade / mana / cooldown** | Uso da ação solicita **1** de durabilidade fora de `instabuild`; não se observou cobrança adicional do encantamento nesse caminho | Não adicionar segunda mana/cobrança; cooldown global do pack não auditado |
| **NBT / persistência** | Override do bolt persiste flag `Bubbling`, não o estado completo de targeting/ricochete | Salvar/carregar, morte, mudança de dimensão e sincronização física pendentes |
| **Hooks / eventos / rede** | `EventHooks.onProjectileImpact`, `ACCompat.hurt`, `addEffect` e mensagem visual são pontos nativos observados | Nenhum hook mutador com timing, cancelamento, safety, autorização ou dedup comprovados |

**Integrações Black Arcana / Enshrouded / RPG Skill Tree:** Black Arcana mantém autoridade sobre seu próprio runtime; o Sea Staff e o efeito continuam sob responsabilidade do provider. RPG Skill Tree pode informar progressão, Mastery, atributos, perks e gates **somente** por contrato de integração efetivamente demonstrado. Nenhum hook seguro de alteração de chance, duração, área, alvo, dano, custo ou comportamento do status foi homologado; `NO_MUTATION` (fail-closed) até essa prova. Não atribuir este encantamento ao inventário de magias castáveis do Black Arcana como novo spell.

## 7. Critérios pendentes de aceitação

1. Fechar contrato de acesso ao nível do encantamento, configuração/datapacks, exclusividades efetivas, e o caminho de `ACCompat.enchantLevel` em runtime da versão instalada.
2. Validar ordem e domínio de execução da decisão RNG, aceite de `hurt`, `addEffect`, atribuição do owner e do debuff, mutadores/handlers coexistentes e efeitos de múltiplos bolts/ricochetes.
3. Executar QA físico no modpack real 1.0.10: cast sem/ com encantamento I; Triple Splash, Bouncing Bolt e outras combinações; aliados, criaturas aquáticas e resistentes, Water Breathing, jogador Creative, PvP, proteção de claims, dano cancelado, servidor dedicado, multiplayer e baixa TPS.
4. Testar `Bubbling` sincronizado, NBT save/reload, entrada em fluido, expiração prematura, instâncias repetidas, handler `UpdateEffectVisualityEntityMessage`, antirreplay e ausência de XP/procs duplicados.
5. Identificar hook provider-native realmente seguro, com ordem de processamento, caps/budgets, autorização do servidor e lifecycle. Não marcar `COMPLETE_PERK_READY` apenas por existir o encantamento ou por a ação Sea Staff já possuir contrato estático certificado.

**Resultado desta ficha:** `JSON_SHA_EXACT_RESOURCE_MATCH` + `SHA_EXACT_SEA_STAFF_PRODUCER` + `SHA_EXACT_WATER_BOLT_CONSUMER` + `SHA_EXACT_BUBBLED_EFFECT`; **escopo técnico estático documentado**, certificação para **perk mutadora pendente**. **Contabilidade:** +1 ficha parcial, +0 certificados adicionais, +0 novas raízes mágicas, +0 providers concluídos, +0 avanço de Stage. **Próxima identidade alfabética:** `alexscaves:explosive_flavor`.
