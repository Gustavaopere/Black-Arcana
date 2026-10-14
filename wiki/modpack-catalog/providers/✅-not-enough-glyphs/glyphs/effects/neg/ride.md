# Ride — dossiê de engenharia NEG 4.6.2

**ID completo:** `not_enough_glyphs:glyph_ride` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectRide` · **source 4.6.2:** [`effects/EffectRide.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectRide.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **20**, **tier:** não sobrescrito (host/base). **Aquisição no catálogo anterior:** Saddle + Manipulation Essence (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- `onResolveEntity` exige `isNotFakePlayer(shooter)` e `shooter != target`. Rejeita `target instanceof Enemy` e tipos marcados em `Registry.RIDE_BLACKLIST`, depois chama `shooter.startRiding(target)`.
- **A presença de `startRiding` não garante êxito de montar:** o método não consulta o boolean de retorno nem estabelece controle de direção. Escolha de mount, passageiros, capacidade de veículo e colisão pertencem ao host/vanilla.
- Escola `MANIPULATION`, augments **nenhum**. O código não confere consentimento de outro player nem valida mudança de estado posterior. Um perk de movimento deve tratar mount confirmado separadamente de tentativa de feitiço.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
