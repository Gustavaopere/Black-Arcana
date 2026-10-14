# Propagate Overhead — dossiê de engenharia NEG 4.6.2

**ID completo:** `arsomega:glyph_propagate_overhead` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.propagators.PropagateOverhead` · **source 4.6.2:** [`propagators/PropagateOverhead.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/propagators/PropagateOverhead.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **100**, **tier:** II. **Aquisição no catálogo anterior:** Manipulation Essence + Overhead glyph (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- `onResolve` usa `copyResolver` e `propagate` redireciona o restante da spell para **bloco sobre o alvo**. Em entidade cria `BlockHitResult(entity.getEyePosition(), Direction.DOWN, entity.blockPosition().above(2), true)`.
- Em hit de bloco constrói `BlockHitResult(hit.getLocation(), hit.getDirection(), hit.getBlockPos().above(), hit.isInside())` — preserva **localização vetorial do hit original**, mas desloca BlockPos para Y+1. Alinhamento entre location/pos é um item específico de QA.
- `getTypeIndex=8`, augments compatíveis delegados a `MethodOverhead.INSTANCE.getCompatibleAugments()` (lista vazia no código 4.6.2). Escola Manipulation; não há novo cast independente nem cobrança extra autorizada em BA.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
