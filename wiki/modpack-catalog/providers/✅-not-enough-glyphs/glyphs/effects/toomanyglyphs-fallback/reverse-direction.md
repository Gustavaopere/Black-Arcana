# Redirect Placement — dossiê de engenharia NEG 4.6.2

**ID completo:** `toomanyglyphs:glyph_reverse_direction` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectReverseDirection` · **source 4.6.2:** [`effects/EffectReverseDirection.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectReverseDirection.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **0**, **tier:** I. **Aquisição no catálogo anterior:** Manipulation Essence + Glass Pane (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- `onResolveBlock` chama `copyResolver`; `propagate` só suporta `BlockHitResult` (outros hits fazem return). Resgata `direction=hit.getDirection()`; com `Sensitive`, alterna eixo vertical→`NORTH` ou horizontal→`UP`.
- Quando a direção calculada é horizontal, converte `ampMultiplier` em `int`; se negativo, gira para anti-horário `abs(amp)` vezes; caso contrário, gira horário `1+abs(amp)` vezes. Portanto **amp zero também causa um giro horário** quando o ramo é horizontal.
- Produz novo `BlockHitResult` com direção oposta; se hit não está dentro, translada a posição original **duas vezes na direção resolvida** antes de inverter a face. Entrega o restante a `resolver.onResolveEffect`.
- Augments Amplify (limite 2), Dampen (2), Sensitive (1); podem inverter o sinal/posição sem novo custo original. Não duplicar placement ou assumir que a operação move/destrói bloco por si só.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
