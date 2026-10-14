# Fertility

Status: `SOURCE-PINNED 5.13.1 / BREEDING RITUAL`

- Registry id: `ars_nouveau:ritual_fertility`
- Class: `RitualBreed`
- Source cost declaration: `500`
- Processing cadence: every `200` game ticks
- Radius: `5` blocks
- Local population hard cap: no effect at `20+` nearby animals
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every 200 ticks, Fertility obtains `Animal` entities inside radius 5. If the local count is at least 20, the work cycle aborts.

Below that cap, each animal not in the provider breeding blacklist is checked for adulthood (`age == 0`) and `canFallInLove()`. Eligible animals are placed into love state through the provider. If at least one animal changes state, the cycle requests Source.

The ritual tooltip independently refreshes the `20+ animals` warning once per second.

## Authority / Black Arcana boundary

Population admission, breeding state and Source use remain Ars Nouveau authority. Black Arcana must not add a second breeding trigger, second Source charge or extra progression credit per animal.

The 20-animal ceiling is part of the provider's bounded operational identity and should not be silently bypassed by integration.

## QA

Source behavior is pinned to 5.13.1. Compatibility with modded animal breeding implementations remains full-pack runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`RitualBreed.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualBreed.java), `com.hollingsworth.arsnouveau.common.ritual.RitualBreed`, Ars 5.13.1.
- **Frequência e cap:** a cada `200` ticks, procura `Animal` em `AABB(brazier).inflate(5)`. Se `animals.size()>=20` retorna **sem efeito** (todos os animais contam antes do filtro de blacklist); tooltips atualizam aviso a cada 20 ticks quando consultados.
- **Processamento:** ignora `EntityTags.BREED_BLACKLIST`; exige idade `getAge()==0` e `canFallInLove()`, chama `setInLove(null)` e marca `didWorkOnce`. Após ao menos uma operação marca `setNeedsSource(true)`; `getSourceCost=500` é declarado por ritual, não prova de custo por animal.
- **Perks:** remover cap populacional, tornar animals adultos ou induzir love fora de `canFallInLove` mudaria contrato da autoridade Ars; status de breeding não garante nascimento nem novo cast. Observação de Mastery deve ser deduplicada.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.
