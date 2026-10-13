# Moonfall

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-TIME RITUAL`

- Registry id: `ars_nouveau:ritual_moonfall`
- Class: `RitualMoonfall`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Moonfall operates on the server Overworld because Ars Nouveau treats time as global. While daytime is before the night threshold, it advances Overworld day time by `100` ticks per ritual tick. It also increments ritual progress once per 20 server ticks.

When progress reaches `18`, it snaps the Overworld to the provider helper's next night time and sends time synchronization packets to Overworld players, then marks the ritual finished.

The provider description is simply: sets the time to night.

## Authority / Black Arcana boundary

Global time mutation belongs to Ars Nouveau for this ritual. Black Arcana must not duplicate the time advance, completion or synchronization merely because it observes ritual completion.

Any future Black Arcana celestial/time ritual must be compared mechanically against Moonfall and remain server-authoritative and bounded rather than becoming a cosmetic duplicate.

## QA

Source lifecycle is pinned to 5.13.1. Runtime interaction with other time-control mods/game rules in the full pack remains pending.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualMoonfall.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualMoonfall.java), versão Ars Nouveau 5.13.1.
- **Authority temporal:** `RitualMoonfall.tick()` usa `ServerLevel.getServer().overworld()`, mesmo quando o ritual está em outro lugar; isso é alteração do tempo global do servidor, não de dimensão local.
- **Relógio:** se `dayTime%24000<13000` adiciona `100` day ticks por tick do ritual e envia `ClientboundSetTimePacket` aos players Overworld. **Detalhe corrigido do ciclo:** no `else`, `incrementProgress()` ocorre **a cada tick** quando a condição de dia deixou de ser atendida; separadamente, se `getGameTime()%20==0`, incrementa outra vez. Em progress `>=18`, define `MathUtil.getNextDaysTime(...NIGHT_TIME)`, sincroniza e `setFinished`.
- **Perks/segurança:** progresso não tem uma cadência única fixa de 20 ticks; não duplicar atualização de tempo nem tratar observação visual como confirmação de conclusão. Qualquer magia temporal própria exige autoridade de mundo e limites.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.
