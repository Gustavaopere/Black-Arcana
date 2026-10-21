# Feed — dossiê de engenharia NEG 4.6.2

**ID completo:** `not_enough_glyphs:glyph_feed` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.effects.EffectFeed` · **source 4.6.2:** [`effects/EffectFeed.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectFeed.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **30**, **tier:** II. **Aquisição no catálogo anterior:** 6 food-tag items + Conjuration Essence (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- `onResolveEntity` requer `LivingEntity` que **não** pertença à tag `EntityTypeTags.UNDEAD`. Extrai **1** item alimentício através de `spellContext.getCaster().getInvManager()`; `Randomize` escolhe `extractRandomItem`, sem Randomize usa `extractItem`. Esse caminho é uma transação **provider inventory-owned**, não Mana/BA-owned.
- Se `getFoodProperties(toFeed)` é null, retorna; caso contrário chama `toFeed.eat(world,food.getStack())` e aplica `Registry.STUFFED_EFFECT` por **400 ticks**, amplifier `min(foodXplosionLevel,9)`.
- `foodXplosionLevel` começa no amplifier anterior ou zero; em Player com fome `>18` ou `hunger+nutrition>=20`, acrescenta `ceil(nutrition/5)`. Em entidade não-Player acrescenta `ceil(nutrition/10)`. A classe não faz acréscimo nesse ramo para Player que ainda tem margem de fome.
- O [`Events.onCrushStuff(SpellDamageEvent.Pre)`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/Events.java) verifica damage source `CRUSH` e efeito Stuffed. Se `health/maxHealth < 0.25` e `random < foodxplosion_chance*(amplifier+1)`, chama `entity.kill()`, exibe partículas e aplica dano de área a candidatos filtrados em AABB de semi-extensão **4**. Senão multiplica o dano do evento por `1+stuffed_crush_multiplier*(amplifier+1)`. **Defaults da config:** chance 0.1 (0..1) e multiplier 0.25 (>=0). Não há clamp local do produto chance×nível nem confirmação de dano pós-evento neste método.
- Augment único: `Randomize`; escola `CONJURATION`. Perks de alimento/Crush precisam conservar exatamente uma extração, distinguir efeito de kill da liquidação de dano e respeitar a causalidade do provider. **Stuffed não é Black Arcana Backlash ou Corruption**.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
