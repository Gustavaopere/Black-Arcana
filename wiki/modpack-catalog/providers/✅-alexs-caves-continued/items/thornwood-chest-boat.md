# Thornwood Chest Boat — recurso `alexscaves:thornwood_chest_boat`

**Catálogo** ✅ Contrato técnico estático da colocação, da aquisição e dos pedidos locais da entidade de transporte. Hook `NOT_VERIFIED`, QA física `NOT_TESTED`, perk `NOT_CERTIFIED` e `NO_MUTATION`.

## 1. Identidade e versão
- Nome: Thornwood Chest Boat; resource ID `alexscaves:thornwood_chest_boat`; provider Alex's Caves Continued, `alexscaves` 1.0.10, Minecraft 1.21.1, NeoForge 21.1.250 no último snapshot documental e Java 21.
- Fonte física publisher: `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A paridade com novo dump instalado não foi verificada.
- Factory exata `ACItemRegistry.lambda$static$146()Item`, Code SHA-256 `aa6d34966ba31d55c535bd67e05f6c97a40b5e984bacc3e088bdf663676ec32b`: `new CaveBoatItem(true, THORNWOOD, Item.Properties.stacksTo(1))`. A enum `THORNWOOD` usa ordinal 1. A factory ativa o caminho de embarcação com baú.
- Classe compartilhada `CaveBoatItem`, SHA-256 `92fc0840e49f71306bbcafbd3e5f4f5814acbf87846846430007310a2577c18d`; caminho `com/github/alexmodguy/alexscaves/server/item/CaveBoatItem`. Grafo e método completo em [auditoria causal comum](../EXACT-CAVE-BOAT-CAUSAL-1.0.10.md).

## 2. Descrição e ativação
O item solicita a colocação de uma embarcação com armazenamento herdado de `ChestBoat`. `use(Level,Player,InteractionHand)` lê a stack da mão usada e solicita um raycast com `ClipContext.Fluid.ANY`. Na referência de desenvolvimento de Minecraft 1.21.1 / NeoForge 21.1.248, `Item.getPlayerPOVHitResult` parte do olho do jogador e segue o vetor calculado de pitch e yaw, escalado pelo atributo `BLOCK_INTERACTION_RANGE`. O contexto usa `ClipContext.Block.OUTLINE` e o modo de fluido recebido do item.

O teste local de obstrução usa um envelope distinto, `AABB.expandTowards(viewVector*5.0).inflate(1.0)`. Exclui espectadores e considera entidades selecionáveis. Se a AABB de uma delas, inflada pelo seu `pickRadius`, contiver o olho do jogador, retorna `PASS`. `MISS` e os demais resultados diferentes de `BLOCK` também retornam `PASS`. Em `BLOCK`, o item usa o ponto do impacto e retorna `FAIL` se `Level.noCollision` falhar.

## 3. Efeito, custo e consumidores
- Em `BLOCK`, o item cria `AlexsCavesChestBoatEntity(level,hitPos,THORNWOOD)` e aplica `setYRot(player.getYRot())` antes do teste de colisão. Com a posição livre, solicita `addFreshEntity` no servidor e descarta o retorno booleano. Mesmo se a chamada retornar `false`, o ramo solicita `GameEvent.ENTITY_PLACE` e chama `shrink(1)` se `instabuild` estiver desativado. Em ambos os lados, o fluxo segue para `Stats.ITEM_USED` e `useSidedSuccess`. Na referência de desenvolvimento, o resultado é `SUCCESS` no cliente e `CONSUME` no servidor.
- `AlexsCavesChestBoatEntity` herda `ChestBoat`, recebe `THORNWOOD` em `DATA_ID_TYPE` e resolve o item de drop via `getChestDropSupplier`. `ACEntityRegistry.CHEST_BOAT` declara `alexscaves:chest_boat` na categoria `MISC`, com largura `1.375F`, altura `0.5625F` e alcance de rastreamento cliente 10. Na referência de desenvolvimento, o limite herdado é de um passageiro e o contêiner tem 27 slots.
- A stack tem limite 1. Durabilidade, mana, XP, cooldown próprio, níveis, dano direto ao alvo e área ofensiva são **N/A** para a colocação descrita.

## 4. Aquisição/receita
A receita publisher usa `minecraft:crafting_shapeless`, no grupo `chest_boat`. Uma unidade de `alexscaves:thornwood_boat` e uma de `minecraft:chest` produzem uma unidade de `alexscaves:thornwood_chest_boat`. O campo `result.count` é omitido e recebe o padrão 1 do codec de referência. O ID consta na tag publisher `#minecraft:chest_boats`. A disponibilidade da receita e o desbloqueio no modpack dependem do ambiente carregado.

`data/alexscaves/recipe/thornwood_chest_boat.json` · SHA-256 `4e93e21da802378b1f4089be67ef8a3383afa7f4ef54bef80b466eefac8cfb9c`.

## 5. Estado, persistência, queda e drops
- `AlexsCavesChestBoatEntity` salva `ACBoatType` por nome e restaura o tipo com `Type.byName` quando o campo está presente. Na referência de desenvolvimento, `ChestBoat` chama os métodos do contêiner para gravar e ler o inventário. Os dois overrides do publisher tratam o tipo e omitem a chamada à superclasse. A persistência do conteúdo após recarregar continua pendente de teste físico.
- `getVariant()` fornece `Boat.Type.OAK` e `setVariant(Boat.Type)` é no-op neste classfile; o tipo PEWEN/THORNWOOD é gerido separadamente por `getACBoatType` e `setACBoatType`. Tipo inválido por nome/ordinal cai no enum inicial PEWEN no corpo local.
- Ao tocar o chão, se a embarcação não estiver como passageira de outra entidade, tiver `Boat.Status.ON_LAND` e `fallDistance>3.0F`, solicita dano de queda com multiplicador `1.0F` e descarta o retorno. No servidor, se ainda não estiver removida, chama `kill()`. Com `RULE_DOENTITYDROPS` habilitada, solicita três tábuas do fornecedor da enum e dois `Items.STICK`. O fornecedor declarado para `THORNWOOD` usa `PEWEN_PLANKS`, embora a receita exija `THORNWOOD_PLANKS`.

## 6. Integração, validação e pendências
O contrato estático cobre o JAR publisher, as definições de receita e as chamadas imediatas do item. A referência de desenvolvimento delimita o raycast herdado, os retornos de uso e os parâmetros da entidade. Custo, tipos, física, drops e armazenamento são candidatos conceituais a perks. Registro efetivo, colisão e alcance no modpack, aceitação de spawn e drops, permissões e claims, inventário após restart, movimento de passageiros e QA física continuam pendentes. O universo integral do provider permanece aberto. [Prova estática e reprodução](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.md) · [Auditoria causal](../EXACT-CAVE-BOAT-CAUSAL-1.0.10.md) · [Manifesto de descoberta](../EXACT-CAVE-BOAT-DISCOVERY-1.0.10.json)
