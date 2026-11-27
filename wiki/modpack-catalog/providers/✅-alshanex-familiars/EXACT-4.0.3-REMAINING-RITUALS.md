# Rituais do Alshanex’s Familiars 4.0.3

O pacote do publisher contém **11 receitas `alshanex_familiars:ritual_recipe`** no diretório `data/alshanex_familiars/recipe/ritual_recipes/`. Este lote documenta as nove que faltavam e reproduz os contratos de Archmage e Druid. O fechamento cobre o craft dessas onze receitas, da montagem à saída e sua movimentação pelo Automator. As referências de uso posterior identificam os consumidores de cada saída. [Índice dos rituais](rituals/INDEX.md) · [Selo SHA-exato](EXACT-4.0.3-REMAINING-RITUALS.json)

## Identidade e autoridade

- Alshanex 4.0.3, publisher 1171602/8675568, SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`, SHA-256 `ed006afb15a68bee9685ddac45c0f8bfc2a16e3a8a05004c6e1a3373f5f9a284`.
- FamiliarsLib 1.7.1, publisher 1316458/8059464, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`, SHA-256 `bf53bc48bb220c268b2db3619c68d75dba15e140bbd2d3799dd85b9299a0e5a9`.
- A prova vincula a lista completa de recursos deste tipo, contagens, flags de consumo, partículas, IDs de resultado, registros do item e métodos consumidores pelos hashes. Componentes e métodos de terceiros aparecem como metadados factuais e referências.
- Atos de consumo e duração continuam sob autoridade de Alshanex. Dados efetivos de servidor, reload, atribuição de jogador e salvamento exigem validação em jogo. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`.

## Comportamento comum

Cada receita exige quatro estátuas na altura do núcleo, a dois blocos nos quatro pontos cardeais. `RitualRecipeType.matches` compara o ingrediente central e o total de quatro periféricos com os quatro requisitos unitários. `RitualHelper.findMatchingRecipe` resolve a primeira receita compatível. Nenhuma ordem fixa de ingredientes por estátua é exigida.

`RitualCorePedestalEntity.tick` revalida a montagem e conclui após cem incrementos válidos. O relógio pausa com configuração periférica inválida e item central elegível. Ao remover ou trocar o central pelo setter do núcleo, o contador reinicia. As partículas de progresso são solicitadas a cada dez incrementos. A saída central é uma nova stack de uma unidade do item, produzida por `completeRitual` após a limpeza das stacks periféricas consumíveis. O ritual usa custos de inventário e tempo, com dano, status, projéteis, mana e XP inaplicáveis ao craft. O destino primário é o inventário do núcleo.

O Ritual Automator procura a primeira entidade de núcleo na caixa de ±10 blocos em X/Z e ±5 em Y, usa o inventário imediatamente abaixo e programa trajetos de 20 ticks ativos. Ele escolhe por ID de receita para abastecer e coletar. O núcleo continua resolvendo os ingredientes no altar. A coleta limpa o núcleo e encaminha a stack de saída para armazenamento ou drop. O setup pode sofrer alterações entre o despacho e a chegada, quando a rota revalida o destino.

`RitualHelper.clearItemsFromPedestals @143–149` pula o item com `consume=false`. Ele continua obrigatório para o matching. `RitualAutomatorBlockEntity.performCleanup @209–231` mantém um input compatível, e `performSupply @152` chama `removeNeed` para o item que já está presente. A flor de esporos de Druid e o Divine Soulshard das duas receitas de nível 3 podem servir ao ciclo seguinte se continuarem válidos e disponíveis. [Relógio, custos e automação](EXACT-4.0.3-ARCHMAGE-RITUAL.md) · [Retenção e reaproveitamento](EXACT-4.0.3-DRUID-RITUAL.md)

## Bindings das saídas

Os registros usam o namespace `alshanex_familiars`. O invocador do bootstrap vincula o ID ao construtor do item ou ao método que inicia suas propriedades. A tabela segue a ordem do inventário.

| Receita e ficha | Campo de ItemRegistry | Literal em `<clinit>` | Bootstrap e consumidor |
|---|---|---:|---|
| [Frostling Shard](rituals/frostling-shard.md) | `FROSTLING_RUNE` | 772 | 43 → `FrostlingShard()` |
| [Hunter Shard](rituals/hunter-shard.md) | `HUNTER_RUNE` | 704 | 39 → `HunterShard()` |
| [Lightning Mage Shard](rituals/lightning-mage-shard.md) | `MAGE_RUNE` | 738 | 41 → `MageShard()` |
| [Magic Power Tier 2](rituals/magic-power-tier-2.md) | `MAGIC_POWER_TIER_2` | 1108 | 62 → `lambda$static$40` |
| [Magic Power Tier 3](rituals/magic-power-tier-3.md) | `MAGIC_POWER_TIER_3` | 1125 | 63 → `lambda$static$41` |
| [Magic Resist Tier 2](rituals/magic-resist-tier-2.md) | `MAGIC_RESIST_TIER_2` | 1159 | 65 → `lambda$static$43` |
| [Magic Resist Tier 3](rituals/magic-resist-tier-3.md) | `MAGIC_RESIST_TIER_3` | 1176 | 66 → `lambda$static$44` |
| [Summoner Shard](rituals/summoner-shard.md) | `SUMMONER_RUNE` | 755 | 42 → `SummonerShard()` |
| [Truth Mirror](rituals/truth-mirror.md) | `TRUTH_MIRROR` | 904 | 50 → `TruthMirror()` |

### Shards de familiar

Os quatro overrides `spawnFamiliar` usam respectivamente `FROSTLING_PET`, `HUNTER_PET`, `MAGE_PET` e `SUMMONER_PET`. Em cada um, o campo do registro é lido em `@4`. O construtor recebe o tipo obtido do registro, com flag impostor falsa definida em `@21–25`, posição no centro do bloco clicado acrescida de um bloco em Y em `@31–40` e yaw `-Player.getYRot()` em `@46–50`. `addFreshEntity @56` tem seu retorno descartado em `@59`. O débito de uma unidade ocorre antes do override no `AbstractRuneItem.useOn` de FamiliarsLib. Aceitação do spawn, autoria efetiva e ciclo de vida do familiar exigem validação própria.

### Consumíveis de familiar

Os quatro resultados são `Item` com stack máxima 64 e componente padrão `FAMILIAR_CONSUMABLE`. A propriedade manda o tipo e o tier em `ItemRegistry.lambda$static$40/41/43/44 @22–44`. Os tiers 2 são raros e os tiers 3 são épicos. O craft troca o item central do tier anterior. A aplicação posterior no familiar usa o componente do item entregue.

FamiliarsLib lê os limites de `ConsumableType`. As duas famílias declaram bônus `[3,5,15]` e tetos `[15,30,45]` por tier no inicializador. Para o tier 2, o bônus é 5 e o teto é 30. Para o tier 3, o bônus é 15 e o teto é 45. `handleConsumableInteraction` resolve o valor corrente `C`, rejeita a aplicação na rota do servidor se `C >= teto`, e grava `min(C + bônus, teto)` no caminho aceito (`@221–253`). Aplica os modificadores e reduz a stack em uma unidade (`@259–277`). A leitura do tier não exige consumo prévio dos tiers inferiores. A ficha de cada item descreve esse detalhe separadamente da progressão de ingredientes no altar.

`FamiliarConsumableSystem.applyAttributeModifiers` materializa `C/100.0` como `ADD_MULTIPLIED_BASE` permanente nos atributos Iron’s `SPELL_POWER` (`@110–167`) e `SPELL_RESIST` (`@171–228`). Os dados são persistidos pelo fluxo `saveConsumableData`/ `loadConsumableData`. O modificador representa uma fração do atributo-base. Dano líquido e interação com outras fontes dependem dos consumidores e da composição do host.

### Truth Mirror

O construtor configura stack máxima 1, raridade `EPIC` e durabilidade máxima 3 (`@8–19`). `interactLivingEntity` verifica a classe `AbstractSpellCastingPet` e o lado servidor antes de ler a flag de impostor (`@0–32`). Para impostor com `getSummoner()` resolvido em `null`, tenta criar a entidade na posição e yaw do alvo, pede seus efeitos, remove o original e dispara a chamada de avanço para `ServerPlayer` (`@35–230`). A biblioteca implementa `getSummoner` via `OwnerHelper.getAndCacheOwner` com level, cache e UUID. Um retorno nulo deixa a presença de dono persistido em aberto.

Se o invocador resolvido existe, `LivingEntity.is` compara com o jogador (`@233–242`). A troca aceita copia stacks de armadura, vida e fúria, flag de bloqueio e UUID (`@268–315`), além de posição e yaw. Os ramos de troca pedem 25 partículas `POOF` e uma Blastwave com parâmetro `2.0f` e cor de Evocation. Ambos descartam o resultado de `addFreshEntity` antes de solicitar `remove(DISCARDED)` no alvo original. Logo, a chamada de troca não serve como prova de inserção ou de transação atômica.

O caminho que alcança `@482` pede `hurtAndBreak(1, jogador, MAINHAND)` e retorna `SUCCESS`. O alvo que passa no tipo e no lado mas tem flag de impostor falsa ou comparação de invocador falsa também alcança esse ponto. O gate inicial retorna `FAIL` fora do tipo e lado aceitos. Os valores são pedidos ao host, com desgaste efetivo, mão secundária, aceitação de spawn, progresso e autorização a verificar em QA. [Ficha do espelho](rituals/truth-mirror.md)

## Reexecução

Com Java 21 disponível e os dois JARs identificados acima:

```sh
python3 docs/qa/alshanex_403_remaining_rituals.py \
  --jar /caminho/alshanex_familiars-1.21.1_v4.0.3.jar \
  --familiarslib /caminho/familiarslib-1.7.1.jar --verify
```

O verificador reproduz os selos de Archmage e Druid antes de validar as nove receitas adicionais, seus registros e os métodos de uso selecionados. A validação física continua pendente para pausa e retomada no altar, ciclos com catalisador, entrega a inventários cheios, aplicação de consumível no limite, persistência de bônus e troca de impostor com estados de dono distintos. O fechamento deste recorte não define o universo de sistemas do provider.
