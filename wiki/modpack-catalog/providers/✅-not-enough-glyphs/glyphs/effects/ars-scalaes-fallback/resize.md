# Resize — dossiê de engenharia NEG 4.6.2

**ID completo:** `ars_scalaes:glyph_resize` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectResize` · **source 4.6.2:** [`effects/EffectResize.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectResize.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **100**, **tier:** II. **Aquisição no catálogo anterior:** Manipulation Essence + Abjuration Essence + Brown Mushroom (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- Registro **incondicional no source NEG**, usando namespace histórico `ars_scalaes` embora o addon original esteja ausente. `onResolveEntity` atua apenas em `LivingEntity` que possua atributo vanilla `Attributes.SCALE`.
- Com `ampMultiplier==0`, remove ambos efeitos `Registry.GROWING_EFFECT` e `Registry.SHRINKING_EFFECT`. Caso contrário, escolhe Growing para sinal positivo e Shrinking para sinal negativo, chamando `applyConfigPotion`.
- `applyPotion` calcula `ticks=baseDurationSeconds*20 + durationBuffSeconds*stats.getDurationInTicks()` e nível `amp=(int)abs(stats.getAmpMultiplier())`; aplica `MobEffectInstance` com `forceAddEffect`. **O código tem combinação de unidades a verificar:** `buildConfig` chama `addPotionConfig(60*20)`, `addExtendTimeConfig(2*60*20)`, `addDurationDownConfig(20*20)`, enquanto `applyPotion` multiplica o primeiro valor novamente por 20. Getters sem configuração retornam 60,120,30. Não interpretar a duração em segundos finais sem reconstruir os helpers `IPotionEffect` e testar valores da SERVER config.
- Augments Extend Time, Reduce Time, Amplify e Dampen; escola Manipulation. Perks de tamanho exigem cap de Scale, testes de persistência/reversão de status e nenhuma segunda alteração manual de atributo BA.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
