# Propagate Projectile — dossiê de engenharia NEG 4.6.2

**ID completo:** `arsomega:glyph_propagate_projectile` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.propagators.PropagateProjectile` · **source 4.6.2:** [`propagators/PropagateProjectile.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/propagators/PropagateProjectile.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **100**, **tier:** II. **Aquisição no catálogo anterior:** Manipulation Essence + Ars Projectile glyph (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- `onResolveBlock/onResolveEntity` chamam `copyResolver`; `getCastType=MethodProjectile.INSTANCE`; `getTypeIndex=8`. `propagate` cria **1+count(Split)** instâncias Ars `EntityProjectileSpell(world,resolver)` na posição de impacto + (0,1,0).
- Velocidade `max(0.1f,0.75f+accMultiplier/2)`. Com `FakePlayer` ou `Extract`, usa direção `IPropagator.getDirection(shooter,resolver,pos)`; caso contrário dispara pela rotação do caster, com yaw alternado de 5 graus por split. Atualiza yaw/posição e `world.addFreshEntity` para cada projétil.
- `getCompatibleAugments` toma `MethodProjectile` e adiciona `AugmentExtract` explicitamente. O custo/efeito do projétil e a conclusão física pertencem a Ars; **não** contabilizar cada entidade de projectile como uma segunda spell para Mastery.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
