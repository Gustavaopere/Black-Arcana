# Aquisição e consumidores de tags — Holocoder, Hot Chocolate Bottle e Ink Bombs (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. Minecraft 1.21.1, Java 21. Modlist física #001 NeoForge 21.1.250; nenhuma observação de runtime transformado.

Run [45473794747](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45473794747), job 138728477989, artifact 14958583092: relatório **178.620 bytes**, SHA-256 `534c8c6a7534d203d994ea1e4f4948b03c5a0ed01c79a5d97aa6a5eb2fdf79c2`, 1555 classfiles, quatro owners candidatos à tag, cinco recursos fixados por hash. Probe `docs/qa/alexscaves_1010_four_items_resources_tag_probe.py`; workflow exige replay do selo.

## Aquisição declarativa

Cada tabela abaixo tem um pool, sem condição de pool, sem funções de pool/tabela, sem bonus_rolls explicitado; entradas diretas, sem condições, quality ou children explícitos no recorte projetado. A quantidade é argumento da função set_count da entrada selecionada.

| Recurso publisher (data/alexscaves/loot_table) | Item | Índice da entrada | Peso / soma dos pesos declarados | Rolls | Quantidade declarada |
|---|---|---:|---:|---|---|
| chests/licowitch_tower.json | hot_chocolate_bottle | 15 | 10/153 | min 3, max 8 | min 1, max 2 |
| gameplay/deep_one_barter.json | ink_bomb | 12 | 35/646 | 1 | min 2, max 5 |
| gameplay/deep_one_knight_barter.json | ink_bomb | 14 | 10/247 | 1 | min 2, max 5 |
| gameplay/deep_one_mage_barter.json | glow_ink_bomb | 14 | 24/299 | 1 | min 2, max 5 |

Hashes individuais no relatório; não converter peso em chance física sem engine de loot, contexto, registry recarregável, condições e modificadores globais efetivos. Não deduzir quantidade de casts, custo de troca ou aquisição garantida. Holocoder permanece com receita própria anteriormente auditada; este recorte não descobriu nova tabela para ele.

## Tag de roubo e consumidores

`data/alexscaves/tags/item/gingerbread_man_steals.json`, SHA `59c2591008e62e6bb91011202fa7aa2200fd950f9da55d309dbf0bea243682f8`: 12 valores diretos; hot_chocolate_bottle índice 5; replace não explicitado. ACTagRegistry.<clinit> Code `9ed12570499de2ff711f48f5f5bd8d4a9c8f5215fc36544be23e8eb2f1f0496c` literal @374, registerItemTag @377, GINGERBREAD_MAN_STEALS @380. Censo exato de Fieldref e literais: três consumidores e registry, não inclui caminhos reflexivos ou outros mods.

- GingerbreadManStealGoal.hasStealableInventory(Entity)Z Code `743e60488d74ff7cb037f381ea9a1031383ac4d6cd5e5d25ee6668a55cae9d14`: canStealFromEntityType @1, entityItemHandler @10; rejeita handler nulo; itera size e stackInSlot, testa tag @40, retorna true no primeiro match.
- stealOneFrom(Entity)ItemStack Code `659433b3f558c484d8d7f4356a0acf81f013abbe5fbdc2076cfe0624ee430d33`: obtém handler, coleta índices de slots compatíveis, rejeita lista vazia; Util.getRandom @83 e takeOne @97, devolve retorno, senão EMPTY. Seleção de slot, não peso por quantidade de itens; não comprova débito, autorização ou conservação. Implementações concretas ACItemAccess e consumidores do retorno precisam de evidência adicional.
- GingerbreadManStoreStolenItemsGoal.canUse Code `cb5dae66dd327ae92b9b1a699447286f4086e45e17bc2370e4f18516caa83b7f` consulta tag @29 e gates próprios de inventário/oven/tempo/seleção. tick Code `9dfe2154bd1b766d126a42854751ecd8edccbe588bd792eb2b2e1f93c4ee8`: copia item da off-hand @346, HopperBlockEntity.addItem @357; ramo não oven-spawned verifica tipos distintos de itens da tag @417–447; limiar 9 @452; percorre slots e shrink(1) @498 dos itens compatíveis @489; solicita getRandomArmor e addItem @522; setItemInHand @536. Não assumir que o chocolate é sempre roubado, que conversão em armadura sempre ocorre, ou que inserção é transacional.
- GingerbreadManEntity.canTargetItem Code `cf42fa153bbd1d513bb411d1610fdd76798f372f86fbdbe5cd18935d50caf270`: isOvenSpawned @1 permite pular teste da tag; caso contrário requer tag @11. Depois verifica hasLostLimb(isLeftHanded(),true) @23 e rejeita se verdadeiro. É elegibilidade de target, não pickup aceito.

## Factory da entidade

ACEntityRegistry classe SHA `7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072`, lambda$static$43 Code `5f095071ddceb4d09df9169080fcd8cda9d0fdbe185340560e692aa7b63d0fe7`, instruction SHA `ebf33e4001e4ec0b07ee29546558633e3a3be800512e1ad12a68ebfdf2c28d51`: categoria MISC; sized(0.6F,0.6F) @17, setShouldReceiveVelocityUpdates(true) @21, setUpdateInterval(1) @25, id/build @31/34; não há chamada de trackingRange explícita no corpo. Esses são argumentos declarativos; hitbox efetiva, sincronização e alcance de tracking dependem do builder/registry/engine. Não confundir dimensão da entidade com raio da nuvem.

## Limites

Sem novo certificado, sem delta de raízes mágicas, universo não encerrado. As quatro fichas permanecem parciais. Faltam handlers concretos de inventário, ingresso/consumidores de troca, defaults e overrides efetivos, listeners, runtime e QA. Não usar tag global como perk individual, nem creditar Mastery por sorteio, tentativa de extração ou referência de stack.
