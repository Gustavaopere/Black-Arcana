# Archmage Shard

**✅ Contrato técnico estático do ritual** · Alshanex’s Familiars 4.0.3 · `STATIC_TECHNICAL_CATALOG_ONLY`

O ritual consome uma Familiar Soul e quatro ingredientes do Iron’s Spells para produzir um Archmage Shard no pedestal central. O shard pode ser usado depois para solicitar a invocação do familiar Archmage. [Evidência no JAR exato](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

| Identidade | Valor |
|---|---|
| ID da receita | `alshanex_familiars:ritual_recipes/archmage_shard` |
| Tipo da receita | `alshanex_familiars:ritual_recipe` |
| Item produzido | `alshanex_familiars:archmage_shard` |
| Contagem semântica | `COUNTED_EXACT` · um ritual do provider |

## Receita e registro

Inspeção factual do publisher JAR 4.0.3, SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`, CurseForge `1171602/8675568`. O recurso declara `central_item` como item `alshanex_familiars:pet_soul`, sem contagem central explícita. As quatro entradas, na ordem do recurso, são:

| Entrada | Item | `count` | `consume` |
|---|---|---:|---|
| 1 | `irons_spellbooks:legendary_ink` | 1 | true |
| 2 | `irons_spellbooks:arcane_essence` | 1 | true |
| 3 | `irons_spellbooks:arcane_rune` | 1 | true |
| 4 | `irons_spellbooks:magic_cloth` | 1 | true |

`result` contém somente `id=alshanex_familiars:archmage_shard`, sem `count` ou components explícitos; `particle_type=minecraft:end_rod`. Ausência no JSON não é prova isolada de default do codec ou de settlement. `RecipeRegistry` registra serializer e type com o literal `ritual_recipe`; `ItemRegistry.ARCHMAGE_RUNE` registra `archmage_shard` por supplier do construtor de `item.shards.ArchmageShard`. O nome Java `ARCHMAGE_RUNE` não cria outra identidade de item. Localizadores e validação: [contrato exato de Archmage](../EXACT-4.0.3-ARCHMAGE-RITUAL.md).

## Execução no altar

| Eixo | Contrato do publisher JAR |
|---|---|
| Geometria | Quatro `FamiliarStatueEntity` no mesmo Y, exatamente a dois blocos do núcleo nos quatro pontos cardeais. `RitualHelper.getSurroundingPedestals` resolve as posições a cada consulta. |
| Seleção | `RitualRecipeType.matches` testa o ingrediente central e compara as quantidades periféricas como multiconjunto. Para esta receita, o total é quatro, com uma unidade de cada item. A ordem das estátuas é livre. `RitualHelper.findMatchingRecipe` usa a primeira receita do tipo cuja combinação passa no teste. |
| Ativação e custo | `RitualCorePedestal.useItemOn` e `ArchmageStatue.useItemOn` processam a troca no servidor, com inserção de cópia de uma unidade e redução de uma unidade da stack de origem. A conclusão substitui a alma e esvazia as quatro stacks participantes marcadas `consume=true`. Mana, XP e cooldown de jogador são inaplicáveis nesse caminho. |
| Tempo | `RitualCorePedestalEntity.tick` conclui ao atingir 100 incrementos com a receita válida. O contador pausa se faltarem ingredientes periféricos enquanto o item central continuar elegível. `setHeldItem` no núcleo reinicia o contador. São aproximadamente 5 s a 20 TPS com a receita válida continuamente. |
| Resultado | `completeRitual` resolve a receita atual, chama `clearItemsFromPedestals` e coloca uma nova stack do item resultado no núcleo. O caminho inspecionado usa o construtor de uma unidade e não reaplica os components da stack da receita. |
| Efeito e alvo | As estátuas e o núcleo são os destinos do ritual. O progresso usa partículas `minecraft:end_rod` a cada dez incrementos, e o final envia um efeito visual Iron’s Blastwave de parâmetro `6.0f` com a cor de Evocation. Dano, hitbox de projétil, efeito de status, PvP e atribuição de kill são inaplicáveis ao craft. |
| Persistência | O núcleo lê e escreve a stack central, os dois flags e o contador em NBT. O resultado pertence ao inventário do bloco. A recuperação de um processo interrompido durante o salvamento depende de QA físico. |

## Ritual Automator

O Automator usa o ID da receita para abastecer e recolher os itens. O núcleo continua escolhendo a receita pela combinação presente no altar. O Automator busca o primeiro núcleo no volume de ±10 blocos em X/Z e ±5 em Y e usa o inventário logo abaixo. Cada transferência programada dura 20 ticks de processamento. Ao recolher, compara item e components com a saída selecionada, retira a stack do núcleo e tenta entregar ao inventário. Quando o inventário está indisponível ou cheio, solicita o drop do que restar acima do Automator. Os 100 incrementos do núcleo continuam sendo o tempo do ritual. [Fluxo e localizadores compilados](../EXACT-4.0.3-ARCHMAGE-RITUAL.md#automação)

## Uso posterior do shard

`ArchmageShard` estende FamiliarsLib `AbstractRuneItem` e sobrescreve `spawnFamiliar(Level, Player, BlockPos)`. Nesse override, cria `ArchmagePetEntity` usando `EntityRegistry.ARCHMAGE_PET`, marca `setIsImpostor(false)`, posiciona no centro do bloco informado mais `(0,1,0)`, atribui a rotação Y negada do jogador (`-getYRot()`) e chama `Level.addFreshEntity`. O retorno booleano dessa chamada é descartado. O único membro do jogador consultado nesse método é `getYRot`; não há chamada direta a setter de owner/tame nesse override. Isso não comprova ownership, registro de familiar do jogador ou sucesso de spawn ([evidência exata](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)).

A ativação posterior é herdada de **FamiliarsLib 1.7.1**, artefato publisher `1316458/8059464`, SHA-1 físico confirmado `7fa3f3116e35c12456425ae195924ced33fcc2eb`. `AbstractRuneItem.useOn(UseOnContext)` obtém level/player/bloco clicado, reduz a stack em 1, chama `spawnFamiliar` e retorna SUCCESS; o teste `ServerPlayer` restringe o trigger de advancement. Nesse método não há gate local adicional de lado, creative, jogador null, espaço seguro ou ownership, nem refund pelo resultado de spawn. Esse uso posterior **não é uma segunda execução do ritual** e não é uma seam mutadora certificada. Lifecycle, taming/ownership efetivos e comportamento cliente/servidor do familiar continuam `NOT_VERIFIED`/`NOT_TESTED`; Black Arcana não deve criar um segundo spawn, débito ou ledger de familiar ([evidência exata](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)).

## Integração e validação

O altar e o Automator controlam a montagem, o consumo e a entrega. Perks do RPG Skill Tree e Enshrouded podem usar esta ficha como referência para custos, duração e receptores. O ponto de alteração desses valores e o evento de conclusão utilizável para Mastery seguem `NOT_VERIFIED`. A atribuição do ritual a um jogador requer uma evidência distinta da autoria da interação manual.

O relatório vincula a receita e os métodos selecionados aos hashes das classes e dos JARs. `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`. [Reprodução e limites](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)
