# Horn Merchant — entidade e política de economia

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** contrato binário documentado; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). PC é offset de método do publisher. Conflito publisher ARR / TOML MIT aberto; somente fatos de interoperabilidade, sem código, disassembly ou assets reproduzidos.

## Identidade, atributos e AI

Registry **`acolyte:horn_merchant`**, `HornMerchantEntity extends AbstractVillager implements GeoEntity`; categoria **CREATURE**, dimensão **0,6 × 1,95**, tracking range configurado **64**. Atributos: vida máxima **20**, movement speed **0,5**, follow range **48**. Não é `IMagicEntity`, não registra spell nem objetivo de cast.

Goals: prioridade 0 Float; prioridade 1 TradeWithPlayer, LookAtTradingPlayer, Panic(speed0,5) e AvoidEntity; prioridade 3 WaterAvoidingRandomStroll(speed0,35); prioridade 4 LookAtPlayer(8); prioridade 5 RandomLookAround. Evita Zombie/Vindicator/Vex a distância8, Evoker/Illusioner12, Pillager15, Zoglin10; speeds de fuga0,5/0,5. Não há alvo de ataque/provider spell pool local. A regra global em `ModCommonSetup.onLivingChangeTarget` impede AbstractVillager de tomar HumanEntity como alvo; não é imunidade universal a dano.

## Geração de ofertas e pesos

`updateTrades()` acrescenta ofertas à lista recebida de `getOffers()`, sem limpá-la no início. O ciclo normal de inicialização é herdado de AbstractVillager; chamá-lo manualmente pode acrescentar mais ofertas e não constitui refresh idempotente.

| Etapa | Quantidade / escolha | Ficha de custo/produto |
|---|---|---|
| materiais comuns | 2 entradas distintas de 20, shuffle sem reposição | [MiscSellTrade](../economy/misc-sell-trade.md) |
| foco | 1 candidato de 7 opções uniformes | [FocusSellTrade](../economy/focus-sell-trade.md) |
| poção/elixir | 1 categoria de 2, uniforme; elixir recebe false/false | [PotionSellTrade](../economy/potion-sell-trade.md), [ExilirSellTrade](../economy/elixir-sell-trade.md) |
| tinta normal | 1 candidato, uncommon/rare | [RandomInkSellTrade](../economy/random-ink-sell-trade.md) |
| scroll baixo | 1 candidato, quality [0;0,25] | [RandomScrollTrade](../economy/random-scroll-trade.md) |
| scroll adicional | 70% de pedir 1 candidato, quality [0,3;0,8] | [RandomScrollTrade](../economy/random-scroll-trade.md) |
| categoria intermediária | 1 de curio/arma/runa/tinta alta, 1/4 cada | [Curio](../economy/random-curio-trade.md), [Armas](../economy/weapons-sell-trade.md), [Runas](../economy/rune-sell-trade.md), [Tinta](../economy/random-ink-sell-trade.md) |
| Dark Horn | 1 de minério/upgrade orb, 1/2 cada | [OreSellTrade](../economy/ore-sell-trade.md), [UpgradeOrbSellTrade](../economy/upgrade-orb-sell-trade.md) |

São **8 ou 9 solicitações de oferta**, antes de remoção de nulls; não 8/9 produtos garantidos. Scroll pode retornar null por `SpellRegistry.none`, curio por loot vazio/lado cliente; as fábricas selecionadas não são repetidas para preencher vaga perdida. O filtro de limpeza final é `Objects.isNull` (bootstrap #1). Os quatro shuffles de listas usam **`Collections.shuffle(List)` sem RandomSource passado**: a geração inteira não é reprodutível apenas pela seed do RNG da entidade. Escolhas internas e scroll chance usam `entity.random`.

Não existe override/provider timer de restock ou refresh de ofertas nesta classe nem nas fábricas. Usos são aumentados em `notifyTrade`; não supor renovação diária, recarga ao reabrir UI, ou reposição ao esgotar. A lista de ofertas/save do merchant é delegada à superclass; valores efetivos de preço e persistência no host montado continuam `NOT_TESTED`.

## Interação, liquidação e XP

`mobInteract(Player,Hand)` abre negociação somente no **servidor**, vivo, sem trading player atual e não-baby; define o jogador e abre UI com nível1, retorna SUCCESS. Caso contrário PASS. Não há vínculo de owner/recruit, pagamento de entrada ou cooldown local de interação.

`notifyTrade(MerchantOffer)` incrementa usos, ajusta ambientSoundTime e chama `rewardTradeXp`, cujo override local é vazio. Se há trading player, chama `ExperienceOrb.award` na posição do jogador com **`offer.getXp()`**. Portanto os valores XP das fichas de fábrica são entregues por esse caminho; não adicionar uma segunda recompensa de XP por observer. `getVillagerXp()` retorna0 e `showProgressBar()` false: não há level-up de villager. `notifyTradeUpdated` é vazio; `getBreedOffspring` retorna null.

## Spawn, tempo de vida e save

Consumidor ativo: `ModCommonSetup.onLevelTick(LevelTickEvent.Post)` chama um **spawner estático** somente em ServerLevel **OVERWORLD**; primeiro cria `HornMerchantSpawner`, depois `tick(level,true,true)`. O próprio tick não usa os dois booleanos recebidos.

- `tickDelay` inicial **24000** chamadas; a cada vencimento, é reiniciado para **24000 + nextInt(12000)**, portanto **24000–35999** ticks, antes das demais checagens.
- Exige gamerule `allowHornMerchantSpawning` (`ALLOW_HORN_MERCHANT_SPAWNING`, default registrado **true**, categoria SPAWNING); no sorteio `nextInt(100)`, aceita **0…15 inclusive**: chance **16%**, não15%. Sem jogador aleatório retorna0.
- Um único candidato por tentativa: offsets X e Z independentes de magnitude **24…39**, cada sinal escolhido por boolean; altura `MOTION_BLOCKING_NO_LEAVES`. Posição deve estar dentro do world border e ser ar. Não faz retry, nem procura radial; a distância horizontal é aproximadamente33,94…55,15 blocos, pois ambos os eixos têm esse afastamento.
- Spawn via `EntityType.spawn(..., EVENT)`; se criado, `setDespawnDelay(48000)` e retorna1. O timer do spawner não tem save próprio no provider; a regra de vida do merchant é separada.
- Merchant inicia `despawnDelay=0`; no `aiStep` servidor, só decrementa quando positivo e descarta ao atingir0. Não pausa por trading player. Spawn por ovo/comando não passa automaticamente pelo setter do spawner.
- `addAdditionalSaveData` delega à superclass e grava inteiro **`DespawnDelay`**; leitura delega e restaura quando a tag numérica existir. O delay acompanha entidade salva; não há owner UUID/provider trade refresh timestamp local.

## Apresentação e observabilidade

`HornMerchantRenderer` usa `HornMerchantModel`; model/texture/animation são `acolyte:geo/entity/horn_merchant.geo.json`, `textures/entity/horn_merchant.png`, `animations/horn_merchant.animation.json`. Controller movement de transição5 alterna idle/walk; a rotação da cabeça é interpolada no modelo. Isso não estabelece uma fase de combate ou evento de cast. Sons são os de villager ambient/hurt/death/yes/no; assets não são copiados.

## Evidência reproduzível

- `ModEntityRegistry.<clinit>` PC 107–120 e `lambda$static$6` PC 0–36: ID/type/dimensões/tracking.
- `HornMerchantEntity.prepareAttributes` PC 0–30; `registerGoals` PC 0–304; `updateTrades` PC 0–421 e bootstrap #1 → `Objects.isNull`.
- `mobInteract` PC 0–53; `notifyTrade` PC 0–46; `rewardTradeXp`/`notifyTradeUpdated` PC0; `getVillagerXp`/`showProgressBar` PC0–1; `getBreedOffspring` PC0–1.
- `setDespawnDelay` PC0–5; `aiStep` PC0–18; `maybeDespawn` PC0–25; `addAdditionalSaveData` PC0–16; `readAdditionalSaveData` PC0–28.
- `HornMerchantSpawner.<init>` PC0–11; `tick` PC0–74; `spawnMerchantNearPlayer` PC0–165.
- `ModGameRules.<clinit>` PC30–42: ID/default da regra; `ModCommonSetup.onLevelTick` PC0–53; `onLivingChangeTarget` PC0–35. `HornMerchantModel` três métodos de resource PC0–5, `setCustomAnimations` PC0–90; renderer `<init>` PC0–12.

## Boundary de integração e validação

Acolyte possui entidade, AI, geração/preço e despawn; Minecraft/NeoForge possui merchant/inventário/loot-context; Iron's possui os produtos e todas as magias. Não há hook seguro documentado para mudar ofertas, reconstituir stacks ou repetir `notifyTrade`. Essas assinaturas são candidatos de observação `NOT_VERIFIED`, sem certificação de mutação. `ModUtils` contém spawn rules/biome/animation helpers, **nenhum helper de preço/trade/restock**; não é intermediário obrigatório desta economia.

`NOT_TESTED`: conferir hash instalado, boot dedicado, gamerule efetiva, RNG/pool de host e data packs, geração sem produto, débito/entrega/XP exatamente uma vez, usos/repouso/reabertura, save/reload, descarte durante trade, dimension travel, dois jogadores e proteção. Relog não certifica restock nem nova posse. Nenhum destes gates foi executado no pack físico.
