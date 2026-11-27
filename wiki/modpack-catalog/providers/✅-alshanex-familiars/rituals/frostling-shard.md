# Frostling Shard

**✅ Contrato técnico estático do ritual** · Alshanex’s Familiars 4.0.3 · `STATIC_TECHNICAL_CATALOG_ONLY`

O altar transforma uma Familiar Soul e quatro ingredientes em uma unidade de Frostling Shard no núcleo. As estátuas são esvaziadas ao concluir a montagem canônica. [Evidência específica do JAR](../EXACT-4.0.3-REMAINING-RITUALS.md) · [Contrato compartilhado do altar](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

| Identidade | Valor |
|---|---|
| Receita | `alshanex_familiars:ritual_recipes/frostling_shard` |
| Recurso exato | `data/alshanex_familiars/recipe/ritual_recipes/frostling_shard.json` |
| Tipo | `alshanex_familiars:ritual_recipe` |
| Item produzido | `alshanex_familiars:frostling_shard` |
| Contagem semântica | `COUNTED_EXACT` · um ritual do provider |
| Escopo | Montagem, resultado no núcleo e transporte pelo Automator |

## Custo e montagem

O núcleo recebe `alshanex_familiars:pet_soul`. As quatro `FamiliarStatueEntity` ficam exatamente a dois blocos nos pontos cardeais e no mesmo Y do núcleo. `RitualHelper.getSurroundingPedestals` consulta norte, sul, leste e oeste a cada avaliação. O matching usa multiconjunto de ingredientes, com ordem livre nas estátuas e total exato de quatro unidades. [Geometria e seleção](../EXACT-4.0.3-ARCHMAGE-RITUAL.md#geometria-cardinal-e-seleção-de-receita)

| Item periférico | Quantidade | Destino ao concluir |
|---|---|---|
| `minecraft:blue_ice` | 1 | Consumido |
| `irons_spellbooks:arcane_essence` | 1 | Consumido |
| `irons_spellbooks:ice_rune` | 1 | Consumido |
| `irons_spellbooks:frozen_bone` | 1 | Consumido |

As quatro entradas do recurso têm `count=1` e `consume=true`. Na inserção manual, o provider coloca uma cópia de uma unidade e reduz a stack de origem em uma unidade. Esse caminho não apresenta exceção própria de creative. Na conclusão, `RitualHelper.clearItemsFromPedestals` esvazia uma stack real por requisito consumível. O total exato e os quatro ingredientes distintos limitam a montagem correspondente a uma unidade de cada. O núcleo substitui a alma pelo resultado. Mana, XP e cooldown de jogador são inaplicáveis ao craft.

## Duração, execução e resultado

| Eixo | Contrato estático 4.0.3 |
|---|---|
| Ativação | O tick do núcleo no servidor revalida o central e os periféricos. A escolha vem da primeira receita do tipo que passa em `matches`. |
| Tempo | A conclusão ocorre ao atingir 100 incrementos válidos, aproximadamente 5 s com montagem contínua a 20 TPS. Retirar um periférico pausa o contador enquanto o central continuar elegível. `setHeldItem` no núcleo reinicia o progresso. |
| Liquidação | `completeRitual` resolve o resultado atual, chama `clearItemsFromPedestals` e coloca `new ItemStack(resultItem)` no núcleo. A saída manual é uma unidade. O construtor não reaplica components arbitrários do stack de resultado da receita. |
| Receptores | O núcleo e as quatro estátuas recebem as alterações de inventário. Alvo vivo, raio de combate, hitbox de projétil, dano e debuff são inaplicáveis. |
| Apresentação | `particle_type=minecraft:snowflake` fornece o efeito de progresso a cada dez incrementos. A conclusão solicita Blastwave visual com a cor de Evocation e parâmetro `6.0f`. |
| Persistência | HeldItem, flags e contador têm rotinas NBT. Save, unload e recuperação do processo permanecem sujeitos a QA físico. A presença dos campos não garante a gravação de cada incremento. |

A partícula de neve é apresentação do progresso. Efeitos de congelamento, dano de gelo e status de combate são inaplicáveis ao craft. Os métodos do altar não definem uma chance aleatória de sucesso para esta receita. A remoção de bloco, troca de central e atualizações de dados continuam sujeitas aos gates nativos do provider e do host. [Relógio e liquidação](../EXACT-4.0.3-ARCHMAGE-RITUAL.md#ticker-pausa-e-duração)

## Ritual Automator

O Automator seleciona `alshanex_familiars:ritual_recipes/frostling_shard` e abastece usando o inventário logo abaixo. Busca o primeiro núcleo no volume de ±10 em X/Z e ±5 em Y. O núcleo continua fazendo o matching pela montagem presente. Ingredientes compatíveis já presentes e entregas em trânsito participam do controle de abastecimento.

Cada voo programado dura 20 ticks de processamento. A coleta compara item e components com a saída selecionada, retira a stack do núcleo e solicita entrega ao armazenamento. Destino ocupado ou indisponível segue o retorno nativo ao inventário ou drop do restante acima do Automator. As quatro entradas deste ritual são consumíveis, e o ciclo seguinte exige seu reabastecimento. Os 100 incrementos do core continuam sendo o relógio próprio do rito. [Seleção, transporte e coleta](../EXACT-4.0.3-ARCHMAGE-RITUAL.md#automação)

## Registro e uso posterior do shard

`ItemRegistry.<clinit> @772–783` registra `frostling_shard` em `FROSTLING_RUNE`. O supplier usa bootstrap 43 e o construtor de `item.shards.FrostlingShard`. O nome Java conserva a identidade de registro do item. [Bindings e verificações](../EXACT-4.0.3-REMAINING-RITUALS.md)

`FrostlingShard` estende `AbstractRuneItem` do FamiliarsLib 1.7.1. Na classe base, o uso em bloco reduz a stack em uma unidade `@25`, chama `spawnFamiliar @33` e encaminha o advancement no ramo `ServerPlayer @52`. Os defaults do item herdado são raridade EPIC e tamanho máximo de stack 16. O método não adiciona gate local de creative, lado, espaço seguro, ownership ou refund condicionado ao spawn.

O override `spawnFamiliar(Level, Player, BlockPos)` tem 30 instruções JVM e nenhuma ramificação própria. Cria `FrostlingPetEntity` com `EntityRegistry.FROSTLING_PET @4`, ligado ao ID `alshanex_familiars:frostling_pet` no registro `@203–213`, define impostor falso `@21–25` e posiciona no centro do bloco clicado mais `(0,1,0)` `@31–40`. A rotação usa `Player.getYRot @46`, **`fneg @49`** e `setYRot @50`, produzindo yaw igual a `-Player.getYRot()`. Solicita `Level.addFreshEntity @56` e descarta o booleano com `pop @59`. [Localizadores específicos](../EXACT-4.0.3-REMAINING-RITUALS.md)

Esse uso ocorre depois da obtenção da shard. Aceitação da entidade, domesticação, vínculo com jogador, ciclo de vida e combate do familiar permanecem fora da certificação estática do ritual. Black Arcana mantém uma atribuição causal própria para progressão e não cria outro spawn ou débito para o mesmo uso. [Dependência FamiliarsLib e limites](../EXACT-4.0.3-ARCHMAGE-RITUAL.md)

## Proveniência, integração e QA

O publisher Alshanex `1171602/8675568` corresponde ao JAR `alshanex_familiars-1.21.1_v4.0.3.jar`, SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`. A receita tem SHA-256 `da170f851a13d200f6e201518d788d90ccbbd82740fe45acd0ff64f841231a4b` e o classfile `FrostlingShard` tem SHA-256 `0c7b49c3fb9f3f1d10ee98f781b7e27fbd72babbbb5dc2f00982d9b9323520c4`. O FamiliarsLib 1.7.1 é o publisher `1316458/8059464`, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`. A inspeção retém fatos, hashes e localizadores delimitados. Implementação e assets permanecem com os fornecedores.

Alshanex gerencia montagem, relógio, consumo e entrega. RPG Skill Tree e Enshrouded podem consultar os parâmetros para planejamento de perks. Alterar custo, duração, resultado ou transporte depende de seam comprovada. O evento utilizável para Mastery e a autoria do ritual por jogador continuam `NOT_VERIFIED`. WorldEffectPolicy Black Arcana não intercepta automaticamente as alterações internas de outro mod.

QA físico permanece `NOT_TESTED`. Conferir Blue Ice e Frozen Bone nos slots, permutação dos quatro itens, retirada durante a contagem, retomada e saída de uma unidade. Validar também coleta com inventário cheio, destino ocupado, troca da receita no Automator, save/unload/restart e ausência de entregas ou recompensas duplicadas. O teste do uso posterior deve observar consumo, rotação negada, quantidade de tentativas e resultado efetivo no cliente e servidor do pack.

`mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `mutation=NO_MUTATION`. O universo integral do provider continua aberto. [Reprodução e escopo](../EXACT-4.0.3-REMAINING-RITUALS.md)
