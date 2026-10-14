# Chaining — dossiê de engenharia NEG 4.6.2

**ID completo:** `toomanyglyphs:glyph_chaining` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectChaining` · **source 4.6.2:** [`effects/EffectChaining.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectChaining.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **300**, **tier:** II. **Aquisição no catálogo anterior:** Manipulation Essence + 3 Chains + Lapis Block + Redstone Block + Source Gem Block (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- Ambos `onResolveBlock` e `onResolveEntity` chamam `spellContext.setCanceled(true)`, obtêm `getRemainingSpell()` e para **cada Edge selecionada** constroem `spellContext.clone().withSpell(continuation)`, instanciam `resolver.getNewResolver(newContext)` e invocam `onResolveEffect`. Assim, um cast pode gerar muitos resolvers derivados sem significar vários casts originais.
- **Blocos:** `maxBlocks=(int)(BASE_MAX_BLOCKS+BONUS_BLOCKS*aoeMultiplier)` com defaults **16 +16×AOE**; distância `1.75+1.0×count(Pierce)` blocos. Seleciona mesmo bloco (`is(struck.getBlock())`); Sensitive 1 exige algum vizinho substituível, Sensitive 2 usa a face original.
- **Entidades:** `maxEntities=(int)(8+16×aoeMultiplier)`, distância `8+4×count(Pierce)` defaults; sem Sensitive exige **mesmo EntityType do atingido** e `!=shooter`; com Sensitive só `!=shooter`. O algoritmo `SearchTargets` ordena uma fila por distância e guarda melhores edges/selecionados; o alvo inicial pode fazer parte da coleção selecionada.
- `Randomize` rejeita candidatos quando `0.1+nextDouble < count(Randomize)/3`. Não usar essa forma como chance final de disparo de cast, pois só filtra candidatos à corrente.
- Augments: AOE, Pierce, Sensitive (limite default 2), Randomize (limite 3). Combinações locais inválidas: Linger, Wall, Burst. Config de número máximo aceita até `Integer.MAX_VALUE`; **limite padrão não é teto global**. Testar budgets de AABB, blocos, entidade e partículas antes de qualquer perk de chain/Mastery.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
