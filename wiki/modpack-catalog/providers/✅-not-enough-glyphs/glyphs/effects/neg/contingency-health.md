# Contingency: Health — dossiê técnico 4.6.2

**Identidade:** `not_enough_glyphs:glyph_contingency_health` · **classe Java:** `alexthw.not_enough_glyphs.common.glyphs.contingency.HeroicsContingency` · **source:** [HeroicsContingency.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/contingency/HeroicsContingency.java).
**Estado:** ✅ registrado no source; ⚠️ habilitação em SERVER config/runtime não comprovada. **Tier/custo/duração herdados Sauce:** NÃO VERIFICADOS nos métodos exatos do host. **Aquisição anteriormente catalogada:** Abjuration Essence + Repeater + Leather Chestplate (não revalidada em datapack neste lote).

## Disparo e causalidade

O método `getTrigger()` devolve `HEROICS`. Em `ContingencyTriggers.HEROICS.onMobHurt`, o limiar é `entity.getMaxHealth() * (2 + instance.getAmplifier()) / 10.0`. Se `entity.getHealth() <= threshold`, solicita `instance.triggerSpell(entity)`. Default narrativo **20% da vida máxima**; incremento do texto da classe **10 pontos percentuais por Amplify**; limite Amplify **3**. O callback consulta `getHealth()` no momento em que é executado; valor anterior/posterior ao dano requer verificação da ordem de evento do Sauce.

Referências compartilhadas: [`ContingencyTriggers.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/contingency/ContingencyTriggers.java) e [`Events.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/Events.java). Cada chamada `triggerSpell` é **solicitação ao objeto Sauce**; a execução da spell armazenada, tempo efetivo, cancelamento, mana e recaptura persistida ainda dependem de inspeção do `ContingencyEffectInstance` da versão embutida.

**Augments/limites observados:** `getPotionAugments()` herdado; classe configura limite de Amplify 3, mas lista completa desse helper não está verificada.

**Risco para perks e Mastery:** Dano único grande, morte, totens e thresholds cruzados precisam de teste para impedir proc repetido ou Mastery sem cast confirmado.

## Evidência, custos e interoperabilidade

- **Evidência estática:** [registro condicional 4.6.2](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java), [montagem de IDs em CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java); release source `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` e JAR da modlist `not_enough_glyphs-1.21.1-4.6.2.jar`. Equivalência dos métodos bytecode ao JAR **não verificada nesta etapa**.
- **Custo de execução:** o valor acima é default/inferência explicitamente localizada, não configuração efetiva; leitura dos arquivos `SERVER`, descontos, aquisição real e pagamento do Ars no pack ainda **⚠️ pendentes**.
- **Perks:** classes e campos verificados não demonstram hook RPG gravável. Superfície mutável homologada **NÃO VERIFICADA**; adapter, atribuição causal, deduplicação e testes **⛔ fail-closed**. Ars/NEG/Sauce detêm a execução e mana; RPG Skill Tree somente progressão por contrato; Black Arcana mantém seu runtime.
- **QA:** testes unitários, GameTest, dedicados, cliente/Survival, recarga, claim/PvP e composições com outros filtros permanecem pendentes. Esta é documentação técnica clean-room, sem código/asset externo incorporado.

[Índice](../../../README.md) · [Matriz](../../../PERK-ENGINEERING-MATRIX-4.6.2.md).
