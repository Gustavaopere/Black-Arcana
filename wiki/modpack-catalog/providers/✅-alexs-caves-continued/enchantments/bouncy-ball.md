# Bouncy Ball — limite de ricochetes do Shot Gum (1.0.10)

**Estado:** ⚠️ ficha individual técnica **parcial/condicionada** de encantamento. Os recursos publisher e janelas de bytecode da versão instalada estão verificados; **não** há certificação integral para perks, nem QA físico, nem hook mutador seguro. `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

O encantamento é um parâmetro do **Shot Gum** e de seus projéteis **Gumball**, não uma nova magia deliberada ou uma nova raiz de casting. Reutilizar os contratos técnicos já catalogados de [Shot Gum](../equipment/shot-gum.md) e [Gumball](../damage-types/gumball.md), evitando contagem e execução duplicadas.

## 1. Identidade e evidência versionada

- **Provider:** Alex's Caves Continued, mod ID `alexscaves`, Minecraft 1.21.1 NeoForge.
- **Enchantment ID:** `alexscaves:bouncy_ball`; chave de tradução `enchantment.alexscaves.bouncy_ball`.
- **Item elegível:** `alexscaves:shot_gum`, via `#alexscaves:enchantable/shot_gum`.
- **JAR físico publisher 1.0.10:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Manifesto individual SHA-exato:** [EXACT-BOUNCY-BALL-1.0.10.json](../EXACT-BOUNCY-BALL-1.0.10.json), reproduzido por [sonda JVM somente leitura](../../../../../docs/qa/alexscaves_1010_bouncy_ball_probe.py), [9 regressões sintéticas](../../../../../docs/qa/alexscaves_1010_bouncy_ball_probe_test.py) e [CI dedicada](../../../../../.github/workflows/alexscaves-1010-bouncy-ball.yml).
- **Evidência estática anterior independente:** [EXACT-GUMBALL-STATE-1.0.10.json](../EXACT-GUMBALL-STATE-1.0.10.json) e [EXACT-GUMBALL-CONTRACTS-1.0.10.json](../EXACT-GUMBALL-CONTRACTS-1.0.10.json).
- **Clean-room:** um checkout público de `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, portanto não pode certificar os parâmetros do JAR 1.0.10. A prova abaixo deriva diretamente dos recursos e JVM compilada SHA-verificados, sem copiar classes do provider.

## 2. Parâmetros publisher de encantamento

| Campo do recurso `data/alexscaves/enchantment/bouncy_ball.json` | Valor exato |
|---|---|
| SHA-256 do JSON | `003c602b45f66154304a0cabdff36b71450da876b071bd355ad604e2cab632ca` |
| `supported_items` | `#alexscaves:enchantable/shot_gum` |
| `weight` | `10` — **peso de enchanting**, não probabilidade de ricochete |
| `max_level` | `3` |
| `min_cost.base` / `per_level_above_first` | `1` / `7` |
| `max_cost.base` / `per_level_above_first` | `41` / `10` |
| `anvil_cost` | `1` |
| `slots` | `mainhand` |
| `exclusive_set` | **Não declarado neste recurso**; não inventar incompatibilidades |

O item tag publisher `data/alexscaves/tags/item/enchantable/shot_gum.json` contém `alexscaves:shot_gum` (SHA-256 `3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d`). `targeted_ricochet.json` é recurso separado, SHA-256 `adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e`, com exclusão declarada de `triple_split`; isso **não** torna Bouncy Ball incompatível com ambos.

Dados efetivos após datapacks, tags `minecraft:in_enchanting_table`, vendedores, outras regras de encantamento, mods e níveis fora do padrão não foram revalidados fisicamente nesta ficha. `slots=mainhand` não é um guard de runtime adicional na chamada manual que lê o nível do stack; consulte a [ficha Shot Gum](../equipment/shot-gum.md).

## 3. Produtor: como Bouncy Ball ajusta o projétil

Classe publisher `com/github/alexmodguy/alexscaves/server/item/ShotGumItem.class` SHA-256 `08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238`. Método exato `acInventoryTick(ItemStack,Level,Entity,boolean)V` — descriptor `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V`, **285 instruções**, digest de parse SHA-256 `6f9325406aaf142af4b415bff94b9123882b72a2ab981370d9be30a5e7c18093`.

No ramo de disparo nativo condicionado à captura inicial `S=isShooting(stack)` e `T=getShootTime(stack)`, com `S && T==5` (contrato previamente catalogado), o binário tem sequência delimitada:

- `iconst_4 @188`: base do máximo de ricochetes do disparo do **Shot Gum**.
- `ACEnchantmentRegistry.BOUNCY_BALL @190` e `ACCompat.enchantLevel @193`: obtém o **nível inteiro** no stack.
- `iconst_2 @196`, `imul @197`, `iadd @198`, `istore 12 @199`: calcula `M = 4 + 2 × level(BOUNCY_BALL)` e guarda M para as tentativas de disparo.
- O objeto Gumball primário é construído com `GumballEntity(Level,LivingEntity) @316`; `shootFromRotation @480` solicita lançamento, e `setMaximumBounces(M) @487` aplica o limite **ao projétil produzido**.
- `setDamage(4F) @495` configura o dano solicitado padrão no Gumball da arma; `Level.isClientSide @499` protege a solicitação `addFreshEntity @508`. O retorno de `addFreshEntity` não é prova de inserção bem-sucedida nem de dano causado.

**Tabela de níveis segundo a fórmula binária:**

| `enchantLevel` efetivo | `M` configurado pelo Shot Gum |
|---:|---:|
| 0 | 4 |
| I (1) | 6 |
| II (2) | 8 |
| III (3) | 10 |

Os valores são **configurações internas de `MAXIMUM_BOUNCES`**, não garantia de quatro, seis, oito ou dez impactos reais. Os setters da entidade não impõem clamp próprio; níveis editados/fora do padrão seriam aplicados aritmeticamente pela expressão nativa, sem que esta ficha certifique comportamento seguro/estável nesse caso.

**Distinguir defaults:** `GumballEntity.defineSynchedData` registra `MAXIMUM_BOUNCES=5` para instâncias comuns; o emissor Shot Gum **sobrescreve com M=4** mesmo sem o encantamento. A discrepância é intencional no escopo de código observado, não um dado conflitante a corrigir.

## 4. Consumidor: contagem, aquisição, ricochete e descarte

Classe `com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.class` SHA-256 `343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535`. Método `bounceFromDirection(Direction)V`, descriptor `(Lnet/minecraft/core/Direction;)V`, **198 instruções** e digest JVM SHA-256 `0f687d784c92e2b8e7eebfc3cc9a85041b5fdfb37c6c5e4a32aaa2489df66282`.

O consumidor invoca `getBounces @3`, `getMaximumBounces @7`, `setBounces @34` e, nos outros ramos, combina os getters, incremento de B e descarte. Helpers próprios `getMaximumBounces()I` e `setMaximumBounces(I)V` possuem **7 instruções** cada (digests `c45e92256a3739bc4614241d9d6cc8e814632cbc8950109980a57495046d1573` e `6ccec525f7d55393d30907d20a4d3fe5e48583df2c41f70fa87be0e214808da9`). `getBounces()I` / `setBounces(I)V` também são getters/setters de dados sincronizados de 7 instruções, sem clamp próprio.

**Guardas distintos**, conforme a [análise completa já catalogada do Gumball](../damage-types/gumball.md):

1. **Explosivo no limite:** se `B > M−1 && isExplosive()`, zera o movimento (`Vec3.ZERO`), grava `BOUNCES=M` e retorna, antes do processamento ordinário de som/incremento. Não afirmar que explode exatamente no instante da colisão.
2. **Targeted Ricochet ativo:** somente com `TARGETS_ON_BOUNCE` busca `LivingEntity` na AABB de `eyePosition + [-10,+10]` em cada eixo via `Level.getEntitiesOfClass @101`. Filtra o owner/alianças, IDs já atingidos e ordena por menor distância ao Gumball. Sem linha de visão explícita nesse laço. Ao escolher alvo, solicita uma nova direção com fator `0.800000011920929D`, incrementa B **no servidor** e descarta quando `B > M` (`@231–242`).
3. **Reflexão ordinária:** sem alvo escolhido, espelha o componente X/Z afetado com fator aproximado `0.8`, ou o componente Y com `0.5`; incrementa B no servidor e descarta quando `B > M` (`@414–445`). Não aplica escala a todos os componentes indistintamente.
4. `bounceSoundCooldown=5` é **intervalo de som**, não cooldown de cast nem do Bouncy Ball. A interação de gravidade, colisões herdadas e tipos de alvo permanece engine/provider-owned.

A área `±10` é **busca de homing opcional de Targeted Ricochet**, não aumento de alcance fornecido por Bouncy Ball. A caixa/hitbox física registrada do Gumball é **0.25F × 0.25F** no contrato existente; aumentar `M` **não** altera o tamanho do projétil, área de dano, tiro inicial ou tipo da `DamageSource`.

Com `TRIPLE_SPLIT`, os descendentes de `onHitEntity` copiam `MAXIMUM_BOUNCES` do pai, mas a construção por `ACCompat.createEntity` não transporta explicitamente o owner. Não creditar kills ou Mastery desses filhos a quem disparou sem uma cadeia de autoria verificada. O encantamento Bouncy Ball **não** liga split, homing ou explosão; essas flags pertencem a encantamentos distintos.

## 5. Escopo de produção nativa, recursos e tempo

A emissão do Shot Gum tenta criar **dois Gumballs** não explosivos ou **um** explosivo por ciclo disparado, se o holder for `LivingEntity`; os números vêm dos contratos nativos do [equipamento](../equipment/shot-gum.md). Não converter `M` em número de projéteis ou danos por cast. No caminho padrão, a arma usa `GUMBALL_PILE` como munição, recarrega quatro cargas quando permitido e debita uma carga por ciclo de disparo para jogadores não criativos, conforme contratos separados. Nenhum custo de mana, stamina ou cooldown por ricochete foi identificado no recorte proprietário; não equivale a comprovar que não existam interceptações externas.

`GumbeeperEntity.shootGumball(LivingEntity)V` é **outro emissor** com método SHA-exato `26380c4830c57381fa6d39220234305da5b408e7ad11bf56878e061b6e45ecb2`. Gumbeeper carregado pode ajustar `MAXIMUM_BOUNCES=10` sob suas próprias regras. **Não** atribuir o nível de Bouncy Ball do Shot Gum ao Gumbeeper, nem converter seu limite de ricochetes em perk da arma.

A contagem `BOUNCES`, seleção de vítimas, efeitos, owner, split, explosão e lógica de descarte são do Gumball e do motor. Os overrides próprios de NBT/persistência não comprovam serialização individual de todos esses accessors; qualquer perk de duração/reload/replay precisa auditar o comportamento efetivo.

## 6. Matriz de dados para perks e limites de implementação

| Dimensão | Dado exato que pode informar design | Intervenção permitida hoje |
|---|---|---|
| **Bounce cap** | `ShotGumItem: M=4+2×L`, passando por `setMaximumBounces`; descarte em `B>M`, gate explosivo distinto | ⛔ Nenhum hook versionado/estável identificado para variar M; não escrever accessors nativos sem controle da autoridade e teste |
| **Dano/tipo** | Gumball primário usa `setDamage(4F)` e o tipo `alexscaves:gumball` no consumidor de impacto | ⛔ Não repetir `hurt` nem atribuir novo `DamageSource`; quantidade de ricochetes não implica dano garantido |
| **Alvos/range** | Homing opcional de Targeted Ricochet usa AABB `±10`, owner, alianças e vítimas anteriores | ⛔ Não confundir busca com limite de ricochetes nem estender range sem API adequada |
| **Projétil / hitbox** | Gumball `0.25F × 0.25F`; reflexões `0.8` horizontais / `0.5` verticais | ⛔ Não alterar tamanho, gravidade, velocidade ou targeting por interpretação de campo de encantamento |
| **Quantidade de tiros / split** | Shot Gum 2 normais ou 1 explosivo; Triple Split cria filhos com M copiado | ⛔ Sem proc extra por bounce nem novo cast; preservar separação das fontes de criação |
| **Custo / cooldown** | Regras nativas de carga, munição e disparo T=5/S verdadeiro; enchanting weight/cost são metadados | ⛔ Não criar cobrança separada de mana, stamina, munição ou cooldown por ricochete |
| **Persistência / rede** | Dados sincronizados B/M; retorno e setters não garantem restore ou anti-replay | ⛔ Sem hook mutador para modificar B/M ou salvar estado nativo de outro mod |
| **XP / Mastery** | Tiros, colisões, descendentes e explosões liquidam a raiz semântica do provider | ⛔ Sem crédito de Mastery/XP por cada salto até dedupe, autoria, aceitação do hit e authority serem comprovados |

**Fronteira:** o runtime mágico Black Arcana mantém casting e segurança próprios. O RPG Skill Tree é apenas sibling/provider de progressão, Mastery, atributos e gates mediante contratos reais. Um projeto de perk que modifique um atributo nativo do Shot Gum precisa de contrato explícito, seguro, server-authoritative e verificável; sem isso, **fail-closed**. Não introduzir wrappers que dobrem o dano, consumam munição novamente ou transformem cada ricochete em novo cast.

## 7. Certificação, QA futura e contagem

- **Identidade/JSON/slots e dados publisher:** `VERIFIED_EXACT_BINARY`.
- **Produtor e consumidores delimitados, hashes/descriptors/offsets:** `VERIFIED_EXACT_BINARY_SELECTED_WINDOWS`; o CFG completo e todos os outros hooks de ambiente não foram reconstruídos.
- **Enchanting/drops/loot de datapacks, slots efetivos, PvP/claims, proteção de chunks, interações de mods, side, replay, ownership dos descendentes e hits realmente aceitos:** `NOT_VERIFIED`.
- **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **perk individual:** `NOT_CERTIFIED`; **mutação:** `NO_MUTATION`.

Para futura validação física, testar L=0/1/2/3 com tiros isolados, obstáculos X/Y/Z, ricochetes com e sem Targeted Ricochet, split, explosivo, múltiplos donos, alvo imune/aliado, colisões repetidas, mods que cancelam hit, limites de chunk, persistência/reload, sons, munição, distância e contagem B real versus M configurado. Registrar telemetria do cliente e servidor e diferenciar `setMaximumBounces` de ricochetes observados.

**Contabilidade nesta rodada:** **+1 ficha individual parcial**, **+0 contratos estáticos certificados**, **+0 raízes mágicas**, **+0 providers concluídos**, sem promoção de Stage. O próximo recurso na ordem alfabética é `alexscaves:charting_call`.
