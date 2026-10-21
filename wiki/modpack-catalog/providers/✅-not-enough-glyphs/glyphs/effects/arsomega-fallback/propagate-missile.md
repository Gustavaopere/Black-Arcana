# Propagate Missile — dossiê de engenharia NEG 4.6.2

**ID completo:** `arsomega:glyph_propagate_missile` · **classe:** `alexthw.not_enough_glyphs.common.glyphs.propagators.PropagateMissile` · **source 4.6.2:** [`propagators/PropagateMissile.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/propagators/PropagateMissile.java).

**Status:** ✅ registrado pelo provider na presença/ausência atual dos hosts condicionais; ⚠️ config SERVER e runtime não testados. **Mana default:** **200**, **tier:** II. **Aquisição no catálogo anterior:** Manipulation Essence + Missile glyph (sem teste de recipe neste lote).

## Caminho de execução e fórmulas

- `onResolveEntity/onResolveBlock` chamam `copyResolver`; `IPropagator.getTypeIndex=8`; `getCastType()` retorna `MethodMissile.INSTANCE`. `propagate` cria **1+count(Split)** instâncias NEG `MissileProjectile(world,resolver)` na posição do hit + (0,1,0).
- Velocidade delegada a `MethodMissile.getProjectileSpeed(stats)`; gravidade aplica-se se `Dampen`. Direção é `IPropagator.getDirection(shooter,resolver,pos)` se `shooter instanceof FakePlayer` **ou** `hasBuff(Extract)`; caso contrário usa `proj.shoot(shooter,...)` com deslocamento de yaw de até múltiplos de 5.
- **Caveat de compatibilidade:** `addAugmentDescriptions` descreve Extract, porém `getCompatibleAugments` retorna apenas a lista de `MethodMissile`, que não incluía Extract na classe 4.6.2 auditada. Não declarar que Extract pode ser anexado via gramática normal sem teste do host.
- O helper `MissileProjectile(world,resolver)` usa defaults diferentes do overload da forma Missile; efeitos ao impactar/expirar permanecem provider-owned. Perks de direção/quantidade precisam preservar lançador, recursos e token de cast.

## Authority, hooks e verificações

**Fonte e registrabilidade:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` com versão declarada **4.6.2**; [registro do provider](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Instalação documentada `not_enough_glyphs-1.21.1-4.6.2.jar`; equivalência bytecode/JAR e configuração SERVER efetiva **⚠️ não testadas neste lote**.

**Perks A/B/C/D:** defaults e rotas Java localizadas são A (fato da fonte), não atributação RPG editável. Hook/evento **B não homologado** para alterar esse comportamento; wrapper C requer integração com ownership e validação no provider; caso contrário D = **⛔ fail-closed**. Autoridade de execução/custo permanece Ars + NEG + Sauce/vanilla; Black Arcana não cria segundo cast/custo ou efeito e detém apenas seu runtime, enquanto RPG Skill Tree fornece progressão/Mastery/gates por contrato.

**QA de aceitação:** rodar configuração SERVER, startup dedicado, GameTests com fake/real player, riscos de divisão de casts/procs, idempotência, recibos de mana/item, PvP/claims, save/restart e Survival. Sem build/CI ou QA atribuíveis a este dossiê. Clean-room: só fatos e localizadores, sem copiar código de terceiros.

[Índice](../../../README.md) · [Matriz de conclusão](../../../PERK-ENGINEERING-MATRIX-COMPLETION-4.6.2.md).
