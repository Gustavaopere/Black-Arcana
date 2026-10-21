# Ars Elemental 0.7.10.1 — Charm

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_charm` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Charm**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** II.
- **Mana source-default:** 30.
- **Schools:** provider registry plus Necromancy added in post-init.
- **Compatible augments:** Extend Time, Duration Down, Amplify.
- **Provider-specific defaults/limits:** potion 30s; extend 8; charm_hp_limit 150.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

**Observação individual na auditoria:** Charm is server/player-driven, blacklist-aware and source-default health-limited to targets below 150 max HP.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe exata:** [`EffectCharm.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectCharm.java) fonte pinned 0.7.10.1, sem prova de byte-equality ao JAR.
- **Admissão:** cast válido só para shooter `Player` em `ServerLevel`, alvo `Mob` não `CHARM_BLACKLIST`; admite `mob.getMaxHealth()<GENERIC_INT` (default 150) ou UUID especial de desenvolvimento, depois divide Enemy/NeutralMob e Animal.
- **Chance hostil:** `resistance=10+100*(currentHealth/maxHealth)` convertido para int na chamada; `chanceBoost=10+5*ampMultiplier`, com +50 se undead e `NecroticFocus.hasFocus`; sucesso quando `rand.nextInt(0,resistance)+chanceBoost>=resistance`. No sucesso aplica `ENTHRALLED` com duração `getBaseDuration()*20+getExtendTimeDuration()*getDurationInTicks` e owner.
- **Domesticadores:** TamableAnimal, AbstractHorse, Fox e Animal love têm tentativas individuais com `rollToSeduce(100 ou 90,25*(1+ampMultiplier),random)`; isso não equivale a controle de inimigos e não garante sucesso em todos os mobs.
- **Perks:** evitar bônus que ignorem blacklist/HP cap, duplicação de tame/owner ou uso de efeitos de controle em players; sorteio não é função da UI.
- **Estado:** ✅ ID JAR + código exato no source commit; ⚠️ gameplay/config/host/auxiliares requerem confirmação; ⛔ adapter de perk RPG não implementado, sem duplicar status, mana ou dano.
