# LootBagItem — contexto de loot e consumo na abertura

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** API de item reutilizável · **estado:** ⚠️ `SOURCE_VERSION_ONLY`, integração `CONDITIONAL`, sem certificação de perk.

`net.acetheeldritchking.aces_spell_utils.items.custom.LootBagItem` permite que um item concreto abra uma loot table junto ao usuário. Esta ficha descreve o contrato da base; a identidade registrada e a tabela escolhida pelo exemplo estão em [example_loot_bag](../examples/example_loot_bag.md). O helper não registra spell ou um segundo sistema de recompensa.

## API e execução no servidor

Os [dois construtores][constructors] recebem `Item.Properties` e `ResourceLocation lootTable`; o segundo também recebe `ParticleOptions`. Armazenam os valores sem validação local da tabela, setter público ou fallback de conteúdo. Partícula omitida/null seleciona `HAPPY_VILLAGER` no uso. `appendHoverText` acrescenta a tradução `getDescriptionId()+".desc"` em cinza; esse texto não descreve necessariamente o resultado do sorteio ([tooltip][tooltip]).

[`use(Level,Player,InteractionHand)`][use] só resolve a tabela e gera drops no ramo `!level.isClientSide` com `ServerLevel`. Consulta `server.reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE,lootTable))`, portanto conteúdo, pesos, quantidade e efeitos de reload pertencem à tabela efetivamente carregada/host. O contexto `LootContextParamSets.ENTITY` é construído com:

| Parâmetro | Valor lido na abertura |
|---|---|
| `THIS_ENTITY`, `LAST_DAMAGE_PLAYER` | O jogador que usa o item |
| `ATTACKING_ENTITY`, `DIRECT_ATTACKING_ENTITY` | O mesmo jogador, passados como opcionais |
| `ORIGIN` | `player.position()` |
| `DAMAGE_SOURCE` | `player.damageSources().playerAttack(player)` |
| luck | `player.getLuck()` |

Esses parâmetros são contexto sintético de abertura: a classe não mata uma entidade nem aplica o `DAMAGE_SOURCE`. Uma chamada `loot.getRandomItems(lootParams)` produz a lista; cada stack passa a `player.drop(stack,true)`, sem inserção direta em inventário nem verificação do retorno ([contexto e drops][context]). Não há multiplicador local de rolls ou garantia de loot não vazio.

## Alvo, apresentação, custo e liquidação

O alvo contextual é o próprio usuário; não há busca espacial, LOS, inimigo, projétil ou área de recompensa. Depois dos drops, o servidor chama `ASUtils.spawnParticlesInCircle(8,0.55F,0.5F,0.1F,player,partícula)` ([emissão][visual]). O [helper de círculo][circle] posiciona cada emissão em `θᵢ=radians(360/count)×i`, `x=player.x+cos(θᵢ)×radius`, `y=player.y+yHeight`, `z=player.z+sin(θᵢ)×radius`; cada chamada ao `MagicManager.spawnParticles` pede quantidade 1 e offsets zero. Neste uso `count=8`, logo o passo é 45°. Raio `0.55` e altura `0.5` são apresentação, sem alterar alcance/pickup.

O [final do método][settlement] fica fora da guarda de servidor: se `!player.isCreative()`, executa **`player.getMainHandItem().shrink(1)`**, depois `level.playLocalSound(...BUNDLE_DROP_CONTENTS,PLAYERS,1,1,false)` e retorna `InteractionResultHolder.success(player.getItemInHand(usedHand))`. Assim, a mão consumida é sempre mainhand, embora o resultado use a mão da interação; o uso offhand pode reduzir outro item. O trecho de consumo é executável em ambos os lados, enquanto o sorteio é server-only. `playLocalSound` não comprova broadcast para todos os clientes.

Não há mana, cast time, cooldown, duração de habilidade, teste de loot entregue, rollback ou proteção local contra aberturas repetidas. Drops vazios/negados não mudam o retorno local; uma exceção antes do final interrompe o fluxo sem compensação explícita. A anotação de sucesso não constitui transação de recompensa confirmada. Não inferir do `true` de `drop` uma política de ownership, pickup, claims ou proteção: esses contratos pertencem ao host.

## Limites de integração e QA

Tabela e partícula são parâmetros nativos de construção. Troca de tabela por jogador, abertura extra, multiplicação de rolls, correção de mão, retry/devolução e um hook de recompensa única **não têm seam seguro comprovado nesta classe**. Uma integração deve preservar uma resolução de loot/consumo por abertura; RPG Skill Tree não deve sortear novamente ou creditar Mastery por uma confirmação apenas visual. Luck efetiva não garante aumento de todos os pools. Black Arcana conserva suas regras de progressão e WorldEffectPolicy; o host conserva o pipeline de drops e loot.

QA pendente relevante: mainhand/offhand com item diferente, creative/survival, tabela vazia/ausente, contexto aceito pelo host, cancelamento dos drops, reload/datapack/modificadores, servidor dedicado e efeitos cliente. Não foram executados nesta ficha.

Pin oficial `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, sem paridade source/JAR demonstrada. A dependência efetiva do source é Iron's `3.16.2`, enquanto o pack anota `3.16.3`; esta leitura estática não prova compatibilidade desse conjunto. `source_pinned=true` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false` · **+0 magias registradas, +0 perks implementadas.**

[constructors]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/custom/LootBagItem.java#L28-L41
[tooltip]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/custom/LootBagItem.java#L43-L48
[use]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/custom/LootBagItem.java#L50-L97
[context]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/custom/LootBagItem.java#L56-L78
[visual]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/custom/LootBagItem.java#L80-L87
[circle]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASUtils.java#L95-L115
[settlement]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/custom/LootBagItem.java#L90-L96
