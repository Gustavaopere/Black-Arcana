# Summoner Shard

**✅ Contrato técnico estático do ritual** · Alshanex’s Familiars 4.0.3 · `STATIC_TECHNICAL_CATALOG_ONLY`

O altar consome uma Familiar Soul e quatro insumos para produzir uma Summoner Shard no núcleo. O uso posterior do item solicita a invocação do familiar em uma fase separada do craft. [Prova da receita e do consumidor](../EXACT-4.0.3-REMAINING-RITUALS.md)

| Identidade | Valor |
|---|---|
| Receita | `alshanex_familiars:ritual_recipes/summoner_shard` |
| Tipo | `alshanex_familiars:ritual_recipe` |
| Saída | `alshanex_familiars:summoner_shard` |
| Binding do item | `ItemRegistry.SUMMONER_RUNE` → `item.shards.SummonerShard` |
| Contagem semântica | `COUNTED_EXACT` · um ritual do provider |

## Custo e montagem

O recurso `data/alshanex_familiars/recipe/ritual_recipes/summoner_shard.json` do JAR `alshanex_familiars-1.21.1_v4.0.3.jar` usa `alshanex_familiars:pet_soul` como ingrediente central. A evidência foi conferida no publisher 1171602/8675568, SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`. O núcleo exige quatro estátuas `FamiliarStatueEntity`, no mesmo Y e a dois blocos nos pontos cardeais. A ordem dos ingredientes nas estátuas é livre.

| Item periférico | Quantidade | `consume` | Destino ao concluir |
|---|---:|---|---|
| `irons_spellbooks:ruined_book` | 1 | true | Consumido |
| `irons_spellbooks:arcane_essence` | 1 | true | Consumido |
| `irons_spellbooks:eldritch_manuscript` | 1 | true | Consumido |
| `minecraft:sculk_catalyst` | 1 | true | Consumido |

`RitualRecipeType.matches` testa a alma central e exige exatamente quatro unidades periféricas, uma de cada item. Na montagem canônica, `RitualHelper.clearItemsFromPedestals` esvazia as quatro stacks consumíveis e `completeRitual` substitui a alma por uma nova stack de **uma** shard. O recurso declara somente o ID do resultado, sem count/components explícitos; o caminho do núcleo usa o construtor de uma unidade. Mana, XP, nível de magia e cooldown de jogador são inaplicáveis ao craft. A obtenção da Familiar Soul fica fora deste recorte. [Execução e limites do altar](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

## Duração, receptores e estado

`RitualCorePedestalEntity.tick` revalida a montagem no servidor e conclui ao atingir **100 incrementos válidos**, cerca de 5 s a 20 TPS com receita continuamente válida. Periféricos ausentes ou incompatíveis pausam o contador enquanto o central continuar elegível; a troca do central por `setHeldItem` reinicia o progresso. O núcleo persiste a stack, os flags e o contador em NBT. Persistência declarada não certifica recuperação exatamente uma vez após save/unload.

A receita solicita partículas `minecraft:sculk_charge_pop` a cada dez incrementos, e o final solicita o efeito visual Blastwave de Evocation. Os receptores do craft são os inventários do núcleo e das quatro estátuas. Dano, alvo vivo, projétil e status de combate são inaplicáveis ao procedimento; o familiar ainda não é criado nessa conclusão. A saída permanece no núcleo até retirada ou coleta. [Contrato comum](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

## Ritual Automator e uso posterior

O Automator seleciona o ID completo da receita, abastece o altar pelo inventário abaixo dele e recolhe o resultado compatível por item/components. O núcleo continua resolvendo a receita pela montagem presente. Cada voo de item dura 20 ticks de processamento; a entrega tenta o inventário e solicita drop do restante quando necessário. Mudar a receita selecionada não é contrato de cancelamento do progresso do núcleo. [Abastecimento, coleta e estado em trânsito](../EXACT-4.0.3-ARCHMAGE-RITUAL.md#automação)

`ItemRegistry.SUMMONER_RUNE` registra o ID `summoner_shard` pelo construtor de `SummonerShard`. A classe estende `AbstractRuneItem` de FamiliarsLib 1.7.1, JAR publisher 1316458/8059464, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`. O uso herdado em bloco reduz a stack em uma unidade, chama `spawnFamiliar` e retorna SUCCESS; o ramo de `ServerPlayer` dispara o advancement. O método herdado não contém gate local adicional de lado, creative ou ownership, nem refund ligado ao sucesso de spawn.

`SummonerShard.spawnFamiliar` cria `SummonerPetEntity` com `EntityRegistry.SUMMONER_PET`, marca impostor falso, posiciona no centro do bloco clicado mais `(0,1,0)` e aplica yaw `-Player.getYRot()`. Solicita `Level.addFreshEntity` e descarta o booleano retornado. Não há chamada direta a setter de dono/tame nesse override. A aceitação da entidade, o vínculo de familiar e seus ataques/spells permanecem fora do certificado do ritual. [Binding e observações exatas](../EXACT-4.0.3-REMAINING-RITUALS.md)

## Integração e QA

Alshanex e seus consumidores nativos controlam matching, relógio, consumo e entrega. Black Arcana não deve executar o rito, duplicar débito/saída ou repetir a tentativa de spawn; sua WorldEffectPolicy não é aplicada automaticamente a operações de outro provider. RPG Skill Tree e Enshrouded podem consultar custo, duração e receptores documentados, mas mutação e crédito de Mastery exigem contrato próprio. Interação com um bloco não comprova autoria de todo o ritual.

`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`. QA pendente: permutação e falta/excesso de insumos, pausa/retomada, troca central, dois ciclos, inventário cheio, quebra de bloco, save/unload e múltiplos jogadores. O uso posterior exige QA distinta de lado, consumo, spawn e ownership. A ficha não promove o universo integral do provider. [Prova e reprodução](../EXACT-4.0.3-REMAINING-RITUALS.md)
