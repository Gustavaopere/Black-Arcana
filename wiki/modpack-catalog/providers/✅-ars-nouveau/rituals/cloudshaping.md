# Cloudshaping

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-WEATHER RITUAL`

- Registry id: `ars_nouveau:ritual_cloudshaping`
- Class: `RitualCloudshaper`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Cloudshaping operates on the server Overworld because Ars Nouveau treats weather as global. Once per 20 game ticks it advances ritual progress; at progress `18` it applies one weather outcome and finishes.

Optional item state is mutually exclusive because `canConsumeItem` accepts only one item while the consumed-item list is empty:

- no modifier: clear weather using a random clear delay sampled from `12000..180000` ticks;
- Gunpowder: rain for a random duration sampled from `12000..24000` ticks;
- Lapis Block: rain + thunder for a random duration sampled from `3600..15600` ticks.

The modifier item is provider-owned ritual input state, not a Black Arcana cost channel.

## Authority / Black Arcana boundary

Weather selection, random duration and global settlement remain Ars Nouveau authority. Black Arcana must not reapply weather, double-consume the modifier or convert this ritual into a generic weather cast.

Future Black Arcana weather/domain mechanics require a semantic gap and independent safety/budget contracts.

## QA

Exact source behavior is pinned to 5.13.1. Interaction with other weather-control providers in the 612-mod runtime remains a separate QA item.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`RitualCloudshaper.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualCloudshaper.java) no Ars 5.13.1.
- **Fase/ciclo:** servidor `getGameTime()%20==0` incrementa progress; em `>=18`, usa exclusivamente o `server.overworld()` para aplicar o clima **global**, independentemente da dimensão da execução do brazier. Chama `setFinished()` no ramo escolhido.
- **Resultados separados:** sem modifier aplica tempo claro com `RAIN_DELAY=UniformInt.of(12000,180000)`; consumido `Items.GUNPOWDER`, chuva `UniformInt.of(12000,24000)`; consumido `Items.LAPIS_BLOCK`, thunderstorm `UniformInt.of(3600,15600)`. `canConsumeItem` aceita no máximo um modifier na lista vazia, portanto os ramos ficam mutuamente exclusivos.
- **Perks:** weather global, seed aleatória do Overworld e escolha do input são authority Ars. Não emitir segundo clima, reexecutar custo ou Mastery para cada pacote de tempo/chuva.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.

## Certificação técnica estática para perks — clima global (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Identidade `ars_nouveau:ritual_cloudshaping` ↔ `RitualCloudshaper` vinculada ao [JAR de IDs compilados](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Comportamento inspecionado em [`RitualCloudshaper.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualCloudshaper.java) e [`AbstractRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/AbstractRitual.java), revision `112920ff774831f204031da75b4c4e73d3765157`. JAR físico `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` comprova identidade de registro, **não equivalência integral dos métodos**.

| Campo relevante | Evidência e limite de alteração |
|---|---|
| Execução e alvo | `tick` produz apresentação `spawnRitualSkyEffect`, mas **apenas no servidor e em `getGameTime()%20==0`** incrementa `progress` e, se `progress>=18`, seleciona `getWorld().getServer().overworld()`. O alvo é o estado meteorológico global do **Overworld**, não área ao redor do brazier ou caster. |
| Modificadores e admissão | `canConsumeItem` aceita exatamente **um** de `Items.LAPIS_BLOCK` ou `Items.GUNPOWDER`, apenas com `getConsumedItems().isEmpty()`. `isStorm` e `isRain` consultam o tipo de item consumido. O caminho normal fica mutuamente exclusivo, mas os três `if` no `tick` são independentes: listas/NBT anormais não têm garantia adicional de exclusão nesta classe. |
| Sem modificador | Se `!isStorm() && !isRain()`, `setWeatherParameters(RAIN_DELAY.sample(world.getRandom()),0,false,false)` com `RAIN_DELAY=UniformInt.of(12000,180000)`. É **tempo de espera até chuva** no argumento de clima claro, não uma duração fixa de buff. |
| Com Gunpowder | `world.setWeatherParameters(0,RAIN_DURATION.sample(...),true,false)`, `RAIN_DURATION=UniformInt.of(12000,24000)` game ticks: chuva sem tempestade, sorteio feito com RNG do Overworld. |
| Com Lapis Block | `world.setWeatherParameters(0,THUNDER_DURATION.sample(...),true,true)`, `THUNDER_DURATION=UniformInt.of(3600,15600)` game ticks: chuva e trovão. É RNG de runtime, não constante ou duração determinística. |
| Término e custo | Cada ramo executado chama `setFinished()`; progresso e clima não criam casts repetidos nem efeito de dano/projétil de spell. `RitualCloudshaper` herda `AbstractRitual.getSourceCost()=0` (getter local); **não equivale a ritual grátis**: entrada/ativação e consumo de itens continuam autoridade do brazier. Sem cooldown de spell exposto. |
| Integração | Alterar estado do tempo atmosférico pode conflitar com outras fontes globais do modpack. `WorldEffectPolicy` do Black Arcana não intercepta automaticamente a meteorologia deste ritual; RPG Skill Tree não deve duplicar `setWeatherParameters`, debitar modificador ou creditar Mastery por partículas. Alteração de duração, clima alvo ou RNG exige contrato/adapter provado. |

**QA ainda necessária:** dimensões, multiplayer, gamerules/servidor, ordem de modificadores, NBT anormal, interação com outros weather mods, save/reload, custo efetivo e timing em servidor. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
