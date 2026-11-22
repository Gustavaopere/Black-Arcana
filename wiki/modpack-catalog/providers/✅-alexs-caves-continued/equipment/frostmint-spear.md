# Frostmint Spear — `alexscaves:frostmint_spear`

**Contrato técnico estático** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`, grau `SHA_EXACT_BINARY_BEHAVIOR`. A ficha cobre a lança, o projétil e os consumidores de congelamento acionados pelo item. **Zero novas raízes mágicas**. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED` e `NO_MUTATION`. [Prova do publisher](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## Identidade, atributos e aquisição

O JAR publisher **1.0.10** (CurseForge **8856293**, 75.279.314 bytes) tem SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A classe `server.item.FrostmintSpearItem` tem SHA-256 `0156bc79eb7c6bc48229c6811a3d5907e05f74b548fba4c1c467369b22a8f0be`. O binding `ACItemRegistry.FROSTMINT_SPEAR` (`<clinit> @3381–3395`) usa a fábrica `lambda$static$192()Item @0–19`, Code SHA-256 `77af284e6a1cafcde0382f7c188510bf17598d6f0b5c16f8a0627d812539fa77`. Declara `stacksTo(16)` e não solicita durabilidade própria. O binding `frostmint_spear_inventory` é o `Item` de apresentação consumido pelo renderer, separado do item de uso. O idioma `en_us` chama os dois de **Frostmint Spear**. [Registro](../systems/item-registry.md)

O construtor chama `SpearItem.<init>(Item.Properties,double)` com **5D**. Seu mapa nativo pede `ATTACK_DAMAGE +5D` e `ATTACK_SPEED −3D`, ambos `ADD_VALUE` para `MAINHAND`. O mapa é convertido em grupo de slot por `ACCompat.itemAttributes`. Dano efetivo, composição dos modificadores e alcance corpo a corpo dependem da entidade, do engine e de outros mods. O JSON de Better Combat tem somente `parent: bettercombat:spear`. [Atributos dinâmicos](../systems/dynamic-attributes.md)

A receita `minecraft:crafting_shaped` usa o padrão ` F ` / `FCF` / ` C `. Três Frostmint e dois Candy Cane produzem **4 lanças** no dado empacotado (SHA-256 `4a2f50e9f4d6caf1455d42bc67040f21320b5018923d87d5d32e1e2da2dcbc8a`). Para obter Frostmint, a receita publicada usa oito Peppermint Powder e um Blue Ice para produzir seis. O advancement de inventário tem pai `alexscaves:alexscaves/frostmint_explosion`. [Recursos e hashes](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## Uso, arremesso e custo

`SpearItem.use` consulta a stack da mão indicada. A guarda herdada de stack danificável retorna `PASS` quando o dano chegou a `maxDamage − 1`. Caso contrário, solicita `startUsingItem` e retorna `CONSUME`. A animação herdada é `SPEAR` com **72.000 ticks** de duração de uso. A solicitação de arremesso ocorre no callback de soltura.

`FrostmintSpearItem.releaseUsing @0–156` exige `Player` e calcula `t = 72000 − timeLeft`, `x = t/20F` e `p = (x² + 2x)/3F`, limitado acima a 1 no helper `SpearItem.getPowerForTime`. O teste em `@32–39` é `(double)p > 0.1D`. No domínio usual de ticks não negativos, passa a partir de **3 ticks** e satura aos **20 ticks**. O valor de carga alimenta `shootFromRotation` com pitch/yaw do jogador, roll 0, velocidade **2.5F × p** e imprecisão **1F**. O item não executa uma busca própria de alvo.

Em `@98–153`, pede inserção do projétil, descarta o booleano, toca o som de arremesso, pede `shrink(1)` fora de `instabuild` e incrementa `ITEM_USED`. A inserção e o débito são pedidos distintos. Em `instabuild`, muda pickup para `CREATIVE_ONLY` e pula o débito. O corpo não faz solicitação própria de desgaste, cooldown ou mana no arremesso e não declara guarda própria de lado nesse callback. O melee e a mineração herdados ainda solicitam desgaste por `hurtAndBreak`, em quantidades **1** e **2** respectivamente. A fábrica publisher fornece stack comum de 16 sem durabilidade declarada. A aplicação efetiva é do engine.

## Projétil, dano e seleção

`ACEntityRegistry.FROSTMINT_SPEAR` usa `lambda$static$82` para `FrostmintSpearEntity`, categoria `MISC`, **0,5 × 0,5 bloco**, parâmetro de atualização 1 e deltas de velocidade habilitados. O construtor com atirador recebe a stack original e, em `@14–33`, passa ao `AbstractArrow` uma **nova stack padrão** e um argumento de arma `null`. O corpo não lê a stack original. O pickup default também constrói uma nova stack. Copiar componentes, encantamentos ou dados de uma perk para o item de origem por si só não os faz chegar ao cálculo de impacto. [Projétil e fábrica](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

| Caminho | Parâmetro e alvo |
|---|---|
| **Acerto corpo a corpo** | `FrostmintSpearItem.acHurtEnemy @0–29` recebe a vítima do callback. Escreve o limiar de congelamento dela + **200** em `setTicksFrozen`, ativa a flag Frostmint e delega o desgaste ao base. A seleção da vítima e o dano primário pertencem ao combate que invoca o callback. |
| **Impacto direto** | `findHitEntity` delega a `AbstractArrow` até `dealtDamage` ficar verdadeiro. `onHitEntity @0–82` escolhe **6F** mais `ACCompat.damageBonus` para vítima viva, calculado com uma stack **padrão**. Pede fonte `trident(projétil,ownerOuProjétil)`. Define `dealtDamage` antes do pedido de dano. |
| **Pós-impacto direto** | Com dano aceito e vítima viva, `@88–135` pede efeitos de pós-ataque se o owner é vivo e aplica congelamento pelo helper local. O teste de tipo `ENDERMAN` retorna antes desse trecho. Os demais caminhos chegam à multiplicação de velocidade `(−0.01,−0.1,−0.01)` e ao som do impacto. |
| **Área** | `onHit @0–39` chama a explosão antes de delegar ao `AbstractArrow` quando `tickCount > 1`, `!exploded` e lado servidor. Marca o latch antes da chamada. O centro é X/Z do projétil e `getY(0.5)`. O construtor recebe o owner, raio **2F**, modo `KEEP`, `fromSpear=true`. |

A entidade mantém `OWNER_ID` inicial `−1`, escreve o ID do owner no servidor após `super.tick` quando ele existe e usa a resolução local por ID no cliente quando este foi fornecido. Sem ID no cliente e no servidor, usa o owner herdado. Os booleanos `dealtDamage` e `exploded` não têm método próprio de leitura ou gravação NBT na classe. O salvamento e a sincronização herdados exigem verificação em runtime. O renderer e a propriedade de modelo `throwing` são superfícies de apresentação.

## Área de Frostmint e estado de congelamento

`FrostmintExplosion.explode` usa `R = 2 × raio`, portanto **4 blocos** para a checagem de distância da lança. A pré-seleção usa AABB com limites por eixo `floor(centro ± (R+1))` e exclui a entidade fonte na consulta. Depois avalia `ignoreExplosion`, descarta `EnderMan`, verifica distância normalizada até 1 e exige vetor direcional não nulo. Calcula exposição com `getSeenPercent`. Se `q = (1 − distância/R) × exposição`, o pedido de dano é `int(((q² + q)/2) × 7 × R + 1)`, convertido para float. A fonte usa `DamageSources.explosion(direct,indirect)`. A lança fornece o owner como fonte da explosão. [Locais e operandos](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

No ramo da lança, `ItemEntity` pula o pedido de dano. O movimento do alvo tem caminho próprio, com `ACCompat.explosionKnockback` para seres vivos. O booleano do dano é descartado e seres vivos elegíveis recebem a escrita de congelamento e a flag em `@988–1023` mesmo sem confirmação daquele dano. O modo `KEEP` torna falso `interactsWithBlocks()` no finalizador. Em servidor, o finalizador ainda emite a mensagem visual de tipo 9 para o ramo da lança. Frostmint Block, Purple Soda e Falling Frostmint possuem contextos próprios para o mesmo helper de explosão. A solicitação em área e o impacto direto têm ordem e filtros distintos. A soma de dano líquido, a prioridade entre chamadas, PvP e proteções do pack precisam de teste.

A escrita `getTicksRequiredToFreeze() + 200` atualiza um **contador**, que o jogo processa. `LivingEntityMixin.ac_livingTick`, injetado no `TAIL` de `LivingEntity.tick`, limpa a flag quando o contador não está positivo ou `canFreeze()` é falso. No servidor, pode emitir partículas quando o contador ainda supera o limiar e as condições do tick são atendidas. O congelamento não usa uma `MobEffectInstance`. Os **200 ticks adicionais ao limiar** não definem uma duração física garantida de imobilização. [Accessor e consumidor](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## Integração e validação

A [descoberta inicial](../EXACT-FLOATER-FROSTMINT-1.0.10.md) e o [manifesto histórico](../EXACT-FLOATER-FROSTMINT-DISCOVERY-1.0.10.json) mantêm a captura parcial original. O [selo atual](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.json) sustenta os campos desta ficha.

O verificador reproduz três corpos do item, 16 do projétil com o inicializador, os consumidores do Frostmint, o registro, os recursos e as fronteiras herdadas. Os pontos relevantes para perks são o callback de carga, a seleção do projétil, o dano direto, a geometria/efeito em área e o estado do alvo. Cada um tem consumidor e autoridade próprios. A homologação depende de identificar o owner certo, preservar custo e eventos nativos e testar o ciclo em servidor. Permanecem pendentes recusa de spawn, owner ausente, dano negado, duração efetiva de freeze, PvP, proteção de mundo, descarte, salvamento e compatibilidade de modpack.
