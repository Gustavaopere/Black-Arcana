# Marine Snow

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21. Modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423), HEAD `b5bc7f2d5f70fe485036dc7e79285fa96ae7867b`, duas saídas idênticas de 335.054 bytes, SHA-256 `a9afad89d2771265dfbb4f86c2981bba8d204943e053d4364af82af69c5a7f41`. [Dossiê](../EXACT-MARINE-FISH-MOTH-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:marine_snow`; owner `MarineSnowItem`; factory `ACItemRegistry.lambda$static$90`, Code SHA-256 `d385d5b08e71c8ae683c30c5f0402acecbcb5ec0b6f13d0e33c25bbf57cdf7ba`. [Registro](../systems/item-registry.md). Insumo de crescimento/recuperação e duplicação de blocos aquáticos. Descrição interpretativa do binário. Modelo `assets/alexscaves/models/item/marine_snow.json`, SHA-256 `179f4314608e9b3f7b8351759bc30e0a1641620c978e909f568e9daf31e4451c`, apenas apresentação.

## Ativação, efeitos e parâmetros

useOn inicializa mapas; scanForWater verifica FluidTags.WATER no bloco clicado ou em uma posição adjacente de cada Direction. Sem água retorna PASS. O alvo é o bloco clicado. GROWS_INTERACTIONS contém 20 pares de corais mortos → vivos (TUBE, BRAIN, BUBBLE, FIRE, HORN × bloco, planta, fan, wall fan); copia propriedades compatíveis e solicita setBlockAndUpdate @152. DUPLICATES_INTERACTIONS contém 25 entradas (20 corais vivos, SPONGE → WET_SPONGE, WET_SPONGE → WET_SPONGE, anêmonas DUSK/TWILIGHT/MIDNIGHT); nextInt(2)==0 pede ItemEntity no click location, addFreshEntity @254. A flag de interação é ajustada antes do sorteio. MUSSEL com MUSSELS < 5 recebe pedido de +1 via setBlockAndUpdate @334. Retornos de alteração/inserção descartados. Se flag de interação, evento 1505 no lado não cliente; shrink(1) fora de creative @382 e sidedSuccess. Não há guarda explícita de lado antes dos pedidos de alteração de mundo. Não equiparar solicitação a sucesso.

## Custos, estado e integração

Uma unidade solicitada mesmo quando sorteio não produz entidade. Mapas estáticos lazy, sem estado per-player demonstrado; stack e bloco sob autoridade nativa. Sem dano, projétil, AOE de combate, mana, cooldown ou duração próprios demonstrados. Aquisição, componentes efetivos e comportamento com player nulo não fechados. Perks conceituais: chance de duplicação, crescimento, custo. WORLD_SAFETY_BLOCKED: não reexecutar useOn, alterar mapa/estado/drop ou creditar Mastery antes de validar claims, callbacks, lado, aceitação e limites. Investigar engine Item, proteção de bloco, fluido, propriedades e eventual reutilização da stack armazenada no mapa.

## Localizadores de evidência

Classfile SHA-256 `b7515b5195e7ae5f1aa4f82fb2fb9e93faa339ad3a754ea62313ce438db46526`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 6 | `8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c` |
| `useOn(Lnet/minecraft/world/item/context/UseOnContext;)Lnet/minecraft/world/InteractionResult;` | 169 | `dec29a166ca2ab5e84b8f78f3c35d157e9403a293a0e97c167cc3a73adbcf206` |
| `scanForWater(Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/core/BlockPos;)Z` | 35 | `ddd9d511d51511cf1831277df3c24e98fb1def06784b82327e63ccf71adf384d` |
| `initGrowth()V` | 16 | `73f1070a2c895ae97a6af0f4decd7e2f989b511b89cd328904986e17f0bc4c83` |
| `lambda$initGrowth$1(Ljava/util/HashMap;)V` | 213 | `0740caf393748346c5690ac6b98376eb85788337d545fc6f3b03b1645976d71f` |
| `lambda$initGrowth$0(Ljava/util/HashMap;)V` | 101 | `6329ada9dbdbe900f68e49a6134a370eb63c6ca3149014b96be32441baafd95f` |


## Continuação downstream — autoridade e limites do efeito no mundo

Base Black Arcana `81dbec3021492e8862b36bb6bbb844d956d742d9`, modlist sibling `b05e2536461bc0a9c526dc47a38e3b9af62d941c`, #001 NeoForge 21.1.250 e #019 Alex's Caves 1.0.10. Licowitch Radiant Essence permanece reservado ao PR #1240; Marine Snow é o próximo item livre. Releitura do replay de 45653331096/job 139343330423 confirmou os pivôs abaixo.

- useOn: verificação água @25/28; GROWS_INTERACTIONS @33 e containsKey @40, ramo cresce com flag true @48, percorre propriedades existentes do novo estado e testa hasProperty no estado original @110, getValue @123/setValue @126, solicita setBlockAndUpdate @152, descarta booleano @155. Ramo exclusivo de crescimento, não também sorteio de duplicação.
- DUPLICATES_INTERACTIONS @159/166, flag true @174 ANTES de nextInt(2) @184; ifne @189 segue ao assentamento. getOrDefault @202 fornece a stack do mapa (sem chamada de copy na rota observada), passada ao construtor ItemEntity @243 nas coordenadas do click, addFreshEntity @254 e pop @257. Investigar se o construtor/campos/synched data mantêm alias com o mapa e se merge/tick podem alterá-lo; não afirmar duplicação efetiva de recurso ou bug confirmado.
- Mussel: identidade @273, MUSSELS @280/getValue @283 e limite 5 @292/293, flag true @296, incremento 1 @323/setValue @328/setBlockAndUpdate @334 com pop. Evento de mundo 1505 @364 somente se !isClientSide; player @368/isCreative @371 sem guarda de null local; shrink(1) @382. Ausência de guarda local não exclui autorização/validação upstream, mas invocação sintética sem player não é segura. Mesmo ramo de débito quando sorteio falha ou solicitação de alteração/entidade é negada; efeitos e assentamento não constituem receipt atômico.
- scanForWater: primeiro estado clicado @1/7, depois Direction.values @15 e BlockPos.relative @43/BlockGetter.getFluidState @46 com FluidTags.WATER @54. É uma consulta de condições de adjacência, não AOE de efeito; não estender ao entorno por perk sem boundary.
- initGrowth testa ambos os mapas @0/6 e, se algum null, instancia os dois com Util.make @21/38 e handles lambda$initGrowth$0/$1. Mapas compartilhados não devem ser alterados por perk global.

### Coleta preparada

[Sonda](../../../../../docs/qa/alexscaves_1010_marine_snow_world_probe.py), commit `8af07c191194d9f0f614abbd92e764549abd49a4`; [workflow](../../../../../.github/workflows/alexscaves-1010-marine-snow-world.yml), commit `11bce6c84961e22931407cc6f9f8cf3dac56260d`. Mantém pins publisher e seis Code hashes, materializa engine distribuída 21.1.250, projeta ItemStack.useOn/ServerPlayerGameMode.useItemOn e candidatos de hooks, contexto/estado/propriedades, Level.setBlock e callbacks de chunk, Mussel/corais, ItemEntity e inserção. Censo de Fieldref e referências tipadas do publisher, recursos JSON data/ com ID literal ou basename, sem presumir ausência transitiva. Duas reproduções determinísticas, orçamento e testes de filtro. Seletores sem declaração nominal não equivalem a ausência de comportamento. Resultado PENDENTE; não promove ficha/ledger ou runtime.

`STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / WORLD_SAFETY_BLOCKED / NO_MUTATION / NOT_TESTED`.
