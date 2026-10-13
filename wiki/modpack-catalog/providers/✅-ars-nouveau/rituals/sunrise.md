# Sunrise

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-TIME RITUAL`

- Registry id: `ars_nouveau:ritual_sunrise`
- Class: `RitualSunrise`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Sunrise operates on the server Overworld because Ars Nouveau treats time as global. While the world is outside the provider's daytime target window, it advances Overworld day time by `100` ticks and synchronizes time packets to Overworld players.

Once per 20 server ticks it also increments ritual progress. At progress `18`, it snaps the Overworld to the provider helper's next day time, synchronizes clients and marks the ritual finished.

Provider description: sets the time to day.

## Authority / Black Arcana boundary

Time mutation and synchronization are Ars Nouveau authority for this ritual. Black Arcana must not reapply them or credit repeated time packets as separate magical actions.

Any independent Black Arcana solar/time ritual must occupy a distinct semantic role and remain server-authoritative/bounded.

## QA

Exact source lifecycle is pinned to 5.13.1. Interaction with other global time-control providers remains full-pack runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`RitualSunrise.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualSunrise.java) no Ars 5.13.1.
- **Dimensão e relógio:** `tick()` opera em `ServerLevel` e redireciona ao `server.overworld()`. Se `dayTime%24000<1000` ou `>=12000`, incrementa dayTime em 100 por tick e sincroniza `ClientboundSetTimePacket` com todos players Overworld.
- **Progresso não linear:** quando o mundo **já está** dentro da janela de dia, o `else` chama `incrementProgress()` a cada tick; separadamente, a cada `gameTime%20==0` incrementa novamente. Ao atingir progress>=18, fixa `MathUtil.getNextDaysTime(...DAY_TIME)`, sincroniza e finaliza. Assim não declarar duração fixa de `18*20` ticks.
- **Perks:** alteração global do relógio tem conflitos potenciais com outros providers de tempo, autoridade é Ars e não deve ser replicada; pacotes são sincronização e não novos casts/credit de progressão.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.
