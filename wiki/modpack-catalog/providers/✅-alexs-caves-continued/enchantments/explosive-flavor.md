# Explosive Flavor — gumball explosiva do Shot Gum (1.0.10)

**Estado do encantamento:** ⚠️ **ficha individual parcial/condicionada**. O JSON e os parâmetros estáticos do equipamento/projétil já estão documentados em contratos binários SHA-exatos. **Hooks mutadores não homologados**, QA física em modpack não executada e ausência de certificação individual para perks: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `NO_MUTATION`.

**Descrição funcional delimitada:** `alexscaves:explosive_flavor` modifica o disparo de `alexscaves:shot_gum`. No fluxo nativo inventariado, nível positivo habilita a flag `EXPLOSIVE` dos projéteis `GumballEntity`, muda **quantidade e velocidade** dos gumballs primários e permite um caminho de parada e explosão retardada. Não adiciona um spell Black Arcana, não aumenta o dano-base de impacto por fórmula do encantamento e não transforma cada contato em uma explosão instantânea garantida.

## 1. Identidade, versão e cadeia de autoridade

| Campo | Evidência |
|---|---|
| Provider e mod ID | Alex's Caves Continued / `alexscaves` |
| Modlist sibling | [RPG Skill Tree — modlist física](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada 019: `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1 / NeoForge |
| Artefato publisher | 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| ResourceKey | `alexscaves:explosive_flavor`; campo `ACEnchantmentRegistry.EXPLOSIVE_FLAVOR`, registrado em `<clinit> @455–461` |
| JSON publisher | `data/alexscaves/enchantment/explosive_flavor.json`; SHA-256 `2da6cbf1a482c69cb268a65667a4b25ea402bc3d9c7b055ef2bd7e5d8f2d08e8` |
| Tag publisher de itens | `data/alexscaves/tags/item/enchantable/shot_gum.json`; SHA-256 `3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d` |
| Produtor | `com/github/alexmodguy/alexscaves/server/item/ShotGumItem.class`; SHA-256 `08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238` |
| Consumidor | `com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.class`; SHA-256 `343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535` |

**Fontes canônicas reutilizadas:** [manifesto Gumball SHA-exato](../EXACT-GUMBALL-CONTRACTS-1.0.10.json), [protocolo de evidência](../EXACT-GUMBALL-CONTRACTS-1.0.10.md), [equipamento Shot Gum](../equipment/shot-gum.md), [dano/projétil Gumball](../damage-types/gumball.md), [inventário de identidades](../INTEGRATION-SCOPE-INVENTORY-1.0.10.json). Nenhum classfile foi modificado, copiado para o repositório ou alegado como reexecutado nesta ficha.

**Corroboração byte a byte, com escopo limitado:** o recurso público `src/main/resources/data/alexscaves/enchantment/explosive_flavor.json` do snapshot `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` possui **365 bytes** e SHA-256 calculado **`2da6cbf1a482c69cb268a65667a4b25ea402bc3d9c7b055ef2bd7e5d8f2d08e8`**, igual ao registrado no manifesto publisher 1.0.10. **Isso equivale somente o JSON específico**: esse snapshot declara versão **1.1.1** e não autoriza importar bytecode, lógica de outros métodos ou paridade da distribuição.

## 2. Definição JSON — versão publisher 1.0.10 por hash idêntico

| Campo | Valor |
|---|---|
| `description.translate` | `enchantment.alexscaves.explosive_flavor` |
| `supported_items` | `#alexscaves:enchantable/shot_gum` |
| `weight` | **1** (peso de seleção do encantamento, não chance da explosão) |
| `max_level` | **1** |
| `min_cost` | `base=1`; `per_level_above_first=16` |
| `max_cost` | `base=41`; `per_level_above_first=10` |
| `anvil_cost` | **8** |
| `slots` | `["mainhand"]` |
| `exclusive_set` | **Não declarado nesse JSON**; coexistência final de outras regras/editores não testada |

A tag de item SHA-exata inclui `alexscaves:shot_gum`. A ficha do equipamento também identifica os tags `minecraft:in_enchanting_table`, `non_treasure`, `on_random_loot` e `tradeable` como referências diretas. Isso não certifica chances efetivas de obtenção ou override por datapack. `min_cost/max_cost/anvil_cost` são custos do sistema de encantamento, não munição, mana, explosão, durabilidade, cooldown ou número de hits.

## 3. Gatilho nativo — `ShotGumItem.acInventoryTick`

**Assinatura própria:** `acInventoryTick(ItemStack,Level,Entity,boolean)V`, ativada pela ponte `ACTickingItem` em `ItemStackTickMixin` no HEAD de `ItemStack.inventoryTick`; a ativação real após transformações do modpack permanece sujeita a QA.

O método captura uma vez `S=isShooting(stack)` e `T=getShootTime(stack)`. No ramo **`S && T==5`** (`@81–89`), desarma a flag `Shooting` antes de construir os projéteis. Um `LivingEntity` é exigido para entrar no laço de emissão, mas o débito posterior de carga tem critérios separados. A verificação do booleano `selected` **não** é realizada nesse corpo.

- `EXPLOSIVE_FLAVOR @172` é consultado por `ACCompat.enchantLevel @175`; `ifle @178→185` converte **nível positivo** em booleano, persistido como local `11` (`@186`). Nenhuma multiplicação por nível é identificada nesse gate; o nível máximo do recurso é I.
- No disparo, o fluxo certificado do equipamento usa esse booleano para escolher **1 tentativa de gumball explosiva**, contra **2 tentativas de gumballs normais** (`@291–306`), mantendo uma cobrança de **uma carga por disparo**, não por tentativa.
- O item usa `new GumballEntity(Level,LivingEntity)` para o projétil primário, chama `setDamage(4F)`, transmite flags de targeting/split e invoca `setExplosive(boolean) @448`. O `4F` é **dano de impacto solicitado**, e não força da explosão.
- Lançamento com `shootFromRotation` em velocidade inicial **0.5F** para explosivo ou **1.5F** para normal, com dispersão `5F`. O equipamento só solicita `Level.addFreshEntity` no servidor e não verifica seu resultado.
- `BOUNCY_BALL` compõe separadamente o máximo **`M=4+2×level(BOUNCY_BALL)`**, calculado antes do laço. Em níveis JSON normais 0/1/2/3, M = **4/6/8/10**; o encantamento Explosive Flavor **não** altera M por si.
- `TRIPLE_SPLIT` e `TARGETED_RICOCHET` são flags calculadas independentemente. O ramo de `exclusive_set` de Targeted Ricochet menciona Triple Split, não constitui prova de compatibilidade irrestrita com Explosive Flavor em condições de datapack/modded anvils.

**Custos e timing da arma:** o stack Shot Gum tem `Gumballs` inicial **4**, `ShootTime`, `Shooting` e `CrankAngle` em `CUSTOM_DATA`. A munição é **`alexscaves:gumball_pile`**, por item exato. No caminho de recarga, uma unidade de munição (não Creative) pode ser debitada para repor **quatro cargas**; o fluxo de tiro debita **uma carga por callback de disparo**, mesmo quando o mundo não aceita inserir o projétil. `T==5` é o limiar interno observado, **não uma cadência física ou cooldown universal garantido**. O item não possui débito de mana Black Arcana.

## 4. Consumidor — estado e comportamento explosivo de `GumballEntity`

**Flag:** `EXPLOSIVE` é um `EntityDataAccessor<Boolean>` sincronizado, cujo default em `defineSynchedData` é `false`; `setExplosive(Z)V` e `isExplosive()Z` escrevem/leem essa flag. Outros accessors incluem `BOUNCES`, `MAXIMUM_BOUNCES`, `DAMAGE`, `TARGETS_ON_BOUNCE` e `SPLITS_ON_HIT`. Ter a flag no projétil **não prova** spawn aceito, impacto, dano, explosão ou ownership imutável.

### 4.1. Ricochete e parada

Defina `B=getBounces()` e `M=getMaximumBounces()`. No início de `bounceFromDirection(Direction)`, o guard compilado é:

- Se **`B > M−1 && isExplosive()`**, o projétil recebe `Vec3.ZERO`, `setBounces(M)` e o método retorna **antes** de som, seleção de alvo e incremento posterior de bounce (`@0–37`). Não descarta a entidade imediatamente nesse caminho.
- Caso contrário, os caminhos nativos de ricochete e `TARGETS_ON_BOUNCE` podem selecionar `LivingEntity` em AABB delimitada pelos olhos `±10` unidades, excluindo alguns owner/aliados e IDs já observados, ou refletir o componente da face colidida. Para incremento por servidor e descarte normal, o limite separado é **`B > M`**. Não converter essa AABB em raio esférico nem em área da explosão.
- `hitEntityIds` auxilia a **aquisição de alvo do ricochete**, mas não é deduplicação de dano por vítima. O método `onHit` chama a superclasse antes dos filtros locais. Assim, nenhum dos guards próprios certifica imunidade automática a hits ou replay.

### 4.2. Contagem e explosão

O ramo de `GumballEntity.tick()V` só progride quando **`isExplosive() && B>=M`**. Se `explodeProgress<=20F`, soma **1F**. Na chamada elegível seguinte, quando o progresso já é **maior que 20F**, o servidor solicita a operação nativa:

```text
Level.explode(getOwner(), x, y + 0.5, z, 2F, false, ExplosionInteraction.NONE)
discard()
```

Esse é o contrato compilado em `tick @176–247`, com `Level.explode @242` e `discard @247`. `2F` é **força da explosão**, não 2 pontos de dano; `false` é a opção de fogo e `ExplosionInteraction.NONE` é a modalidade de interação solicitada. O dano/knockback final, exposição, proteção de claims, força alterada por eventos e bloqueios vêm do motor/provider, sem homologação de valores efetivos. O argumento causal para a explosão é `getOwner()` **naquele instante**; não é `causeGumballDamage` ou um dano Black Arcana reaplicado.

Com progresso inicial zero, o código soma até **21** incrementos elegíveis, com pedido de explosão na passagem elegível seguinte. Esse **não** é o tempo total desde o disparo, nem um cooldown da arma: depende de alcançar o limite B/M e de continuar satisfazendo os guards, sem remoção anterior. `getExplodeProgress` é interpolação visual normalizada por **20F**, não variável de dano ou raio. Não se afirma uma taxa observada de explosões por segundo no modpack.

### 4.3. Dano do impacto, split e descendentes

`onHitEntity` tem um caminho distinto que solicita `Entity.hurt(causeGumballDamage(...),getDamage())` após guards de owner/aliança e de Gumbeeper possuído. O retorno de `hurt` é ignorado pelo corpo próprio, e `onHitEntity` não impede automaticamente o ramo `splitsOnHit()` após dano negado. O `4F` dos gumballs primários do Shot Gum é **pedido inicial**, sujeito a armor, proteção, invulnerabilidade e outros modificadores.

Quando `TRIPLE_SPLIT` estiver ativo e o ramo correspondente for tomado, são até **três tentativas de filhos**. A construção nativa de cada filho copia **`DAMAGE`, `MAXIMUM_BOUNCES`, `TARGETS_ON_BOUNCE` e `EXPLOSIVE`**, define `SPLITS_ON_HIT=false` e usa velocidade horizontal base **~0.7** para pai explosivo, contra **1.5** no outro caso. O helper de criação **não chama `setOwner` nesse caminho**; atribuição de kills, Mastery, dano e procs dos filhos ao usuário do Shot Gum não é certificada. Filho e explosão são **settlement downstream**, não nova despesa de munição ou novo `ArcanaCast`.

O `GumbeeperEntity` também produz Gumballs por lógica própria, inclusive burst; seu estado de `EXPLODING` e seus predicados de tiro **não derivam automaticamente do encantamento de um Shot Gum de jogador**. Não fundir produção de mob, acionamento explosivo de projétil e cast do jogador em uma única origem sem prova explícita.

## 5. Estado, persistência, targeting, mundo e rede

| Eixo | Contrato estático | Limite de integração |
|---|---|---|
| **Identidade/trigger** | Estado do Shot Gum `Shooting,ShootTime`, inventário `ACTickingItem`; `EXPLOSIVE_FLAVOR>0` consulta-se uma vez por disparo | Não gerar cast adicional, callback duplicado ou procs por tick |
| **Quantidade** | Uma tentativa explosiva vs. duas normais; split posterior pode produzir filhos | Não equivaler tentativas a spawns ou hits confirmados |
| **Velocidade** | `0.5F` explosivo/ `1.5F` normal; filhos seguem outras rotinas | Não confundir velocidade física, precisão `5F` e ângulo do renderer |
| **Hitbox/gravidade** | Gumball declara dimensões **0.25F×0.25F** e gravidade padrão aproximada **0.08**; physics herdada | Tamanho, altura da explosão e campo visual são grandezas distintas |
| **Alvo/range/LOS** | Shot Gum não seleciona vítima; ricochete usa AABB e filtros distintos; não existe alcance máximo de explosão verificado como número de blocos | Não usar busca ±10 como área de dano nem contornar proteção/filtros |
| **Dano** | `getDamage` do impacto, `causeGumballDamage`; `Level.explode` é caminho diferente | Não duplicar dano de impacto e explosão, XP, critical ou status |
| **Tempo** | Ativação `T==5`; explosão condicionada a B>=M e progresso >20F | Não derivar duração total, DPS, cooldown, per-tick budget de dados de animação |
| **Recursos** | Uma carga Shot Gum por disparo; uma unidade Gumball Pile para recarregar quatro (conforme guards) | Não cobrar novamente por projétil, explosão ou filho |
| **Persistência** | `ShotGumItem` usa `CUSTOM_DATA`; overrides de `GumballEntity` gravam/leem explicitamente apenas `Color` além da superclasse | Não assumir restauração de `EXPLOSIVE`, contagem, progresso, owner de filho ou deduplicação |
| **Autoridade/world safety** | `Level.explode(..., ExplosionInteraction.NONE)` e efeitos de dano são operações nativas; `addFreshEntity` só no servidor para primários | Nenhum direito implícito de alterar/blindar `WorldEffectPolicy` do Black Arcana ou burlar claims |
| **Rede/QA** | `GumballEntity` sincroniza accessors e possui spawn packet nativo; física, mixins, handshake e reconexão não homologados em modpack | `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION` |

**Sistemas sibling:** Black Arcana conserva seu runtime, hazards, casting, Corruption/Strain/Arcane Danger e `WorldEffectPolicy`. A entidade Gumball e `Level.explode` permanecem sob autoridade do provider/engine; o RPG Skill Tree só pode oferecer progressão, atributos, Mastery, perks e gates via contrato real. Enshrouded não herda authority de detonação. Nenhuma bridge ou intervenção executável foi inferida dos métodos de classfile.

## 6. Critérios pendentes antes de perks mutadoras

1. Validar configuração real de encantamento e tags/datapacks, aquisição, exclusividades, níveis inválidos e interação com `BOUNCY_BALL`, `TARGETED_RICOCHET` e `TRIPLE_SPLIT`.
2. Homologar o boundary e a ordem de alterações da flag `EXPLOSIVE`, de `M`/bounces, de velocidade, dano, owner e explosão; prever clamps, caps de entidades, latência e cancelamento por outros mods.
3. Confirmar no modpack e em servidor dedicado o ciclo **disparo → ricochetes → parada → contagem → explosão**, impacto/split e queda/remoção; medir explosão sob regras de reivindicação, PvP, proteção contra griefing e eventos de mundo.
4. Testar cliente/servidor, Creative, falta de munição, alteração de `CUSTOM_DATA`, troca de mão, dimensão, save/reload, exceções, múltiplos alvos e influência de hit cancellation; medir processamento de Gumballs sem procs repetidos.
5. Obter prova explícita de ownership e causalidade de projéteis filhos e da explosão, inclusive dano final e deduplicação de XP/Mastery; só então considerar uma perk alteradora de explosão, raio, dano, duração, quantidade ou custo.

**Resultado:** `RESOURCE_JSON_SHA_EXACT_MATCH` + `SHA_EXACT_SHOT_GUM_FLAG_AND_DISPARO` + `SHA_EXACT_GUMBALL_EXPLOSIVE_CONSUMER`; apenas documentação estática delimitada. **Sem** hook mutador, QA física, implementação, certificado novo, Stage promotion ou novo feitiço castável. **Contabilidade:** +1 ficha parcial, +0 contratos certificados, +0 novas raízes, +0 providers fechados. **Próxima identidade alfabética:** `alexscaves:far_flung`.
