# Druid Shard

**✅ Contrato técnico estático do ritual** · Alshanex’s Familiars 4.0.3 · `STATIC_TECHNICAL_CATALOG_ONLY`

O altar transforma uma Familiar Soul em um Druid Shard. A flor de esporos ocupa uma das quatro estátuas e permanece disponível para o próximo ciclo. [Evidência no JAR exato](../EXACT-4.0.3-DRUID-RITUAL.md)

| Identidade | Valor |
|---|---|
| Receita | `alshanex_familiars:ritual_recipes/druid_shard` |
| Tipo | `alshanex_familiars:ritual_recipe` |
| Saída | `alshanex_familiars:druid_shard` |
| Contagem semântica | `COUNTED_EXACT` · um ritual do provider |

## Custo e montagem

O núcleo recebe `alshanex_familiars:pet_soul`. As quatro estátuas ficam a dois blocos nos pontos cardeais e na mesma altura do núcleo. A ordem dos itens nas estátuas é livre. `RitualRecipeType.matches` exige quatro unidades no total, uma de cada item abaixo.

| Item periférico | Quantidade | Destino ao concluir |
|---|---:|---|
| `irons_spellbooks:greater_oakskin_elixir` | 1 | Consumido |
| `irons_spellbooks:arcane_essence` | 1 | Consumido |
| `irons_spellbooks:nature_rune` | 1 | Consumido |
| `minecraft:spore_blossom` | 1 | Retido |

`RitualHelper.clearItemsFromPedestals` pula o ingrediente quando `consume=false`. A flor continua obrigatória para o matching. O núcleo substitui a alma por uma unidade de Druid Shard. Custos de mana e XP e cooldown de jogador são inaplicáveis ao craft.

## Duração, alvo e resultado

O servidor conclui ao atingir **100 incrementos válidos** em `RitualCorePedestalEntity.tick`, cerca de 5 s com montagem contínua a 20 TPS. Retirar um periférico pausa o contador enquanto a alma continuar no núcleo e elegível. Trocar o item central reinicia o progresso. `minecraft:composter` é a partícula solicitada a cada 10 incrementos, e a conclusão solicita o efeito visual de Evocation. Núcleo e estátuas são os receptores do craft. Dano, projétil, status de combate e alcance de alvo vivo são inaplicáveis. [Contrato comum do altar](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

## Ritual Automator e uso posterior

O Automator usa o ID completo da receita para abastecer a partir do inventário abaixo dele. Reconhece a flor compatível na estátua e marca seu requisito como atendido enquanto ela permanecer ali. Cada voo dura 20 ticks de processamento. A coleta pede a inserção do shard no armazenamento e solicita drop do restante se necessário. O núcleo continua fazendo o matching pela montagem presente. [Seleção, abastecimento e coleta](../EXACT-4.0.3-DRUID-RITUAL.md#ritual-automator)

Ao usar o shard em bloco, `AbstractRuneItem.useOn` do FamiliarsLib 1.7.1 reduz a stack em uma unidade e chama `DruidShard.spawnFamiliar`. O override cria `DruidPetEntity` com `DRUID_PET`, marca impostor falso e solicita spawn no centro do bloco mais um bloco em Y, com yaw igual a `-Player.getYRot()`. O override descarta o booleano de `Level.addFreshEntity`. Aceitação do spawn, domesticação e autoria efetiva ficam fora da certificação do ritual. [Métodos e localizadores](../EXACT-4.0.3-DRUID-RITUAL.md#binding-e-uso-do-shard)

## Integração e QA

Alshanex gerencia o relógio, o consumo e a entrega. As fichas de RPG Skill Tree e Enshrouded podem usar os parâmetros documentados de custo, retenção de catalisador e duração. A mutação desses valores e a atribuição de Mastery ainda exigem um contrato do provider. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`. [Reprodução](../EXACT-4.0.3-DRUID-RITUAL.md#reprodução)
