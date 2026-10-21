# Contingency: Heal — dossiê técnico 4.6.2

**Identidade:** `not_enough_glyphs:glyph_contingency_heal` · **classe Java:** `alexthw.not_enough_glyphs.common.glyphs.contingency.HealContingency` · **source:** [HealContingency.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/contingency/HealContingency.java).
**Estado:** ✅ registrado no source; ⚠️ habilitação em SERVER config/runtime não comprovada. **Tier/custo/duração herdados Sauce:** NÃO VERIFICADOS nos métodos exatos do host. **Aquisição anteriormente catalogada:** Abjuration Essence + Repeater + Honey Bottle (não revalidada em datapack neste lote).

## Disparo e causalidade

O `getTrigger()` devolve `ON_HEAL`. A classe `ContingencyTriggers.ON_HEAL` é um trigger sem override explícito. O handler real do NEG é `Events.onHealTrigger(LivingHealEvent)`, que consulta `ModRegistry.CONTINGENCY`, confere o trigger por identidade e chama `cei.triggerSpell(event.getEntity())`. `LivingHealEvent` não prova por si só que a cura foi efetivamente aplicada; dedução de amount, cancelamento ou ordem exige QA de evento.

Referências compartilhadas: [`ContingencyTriggers.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/contingency/ContingencyTriggers.java) e [`Events.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/Events.java). Cada chamada `triggerSpell` é **solicitação ao objeto Sauce**; a execução da spell armazenada, tempo efetivo, cancelamento, mana e recaptura persistida ainda dependem de inspeção do `ContingencyEffectInstance` da versão embutida.

**Augments/limites observados:** Não sobrescritos por esta classe; possível herança Sauce/Ars não foi expandida.

**Risco para perks e Mastery:** Não pagar Mastery de cura/contingência duas vezes quando o feitiço armazenado também cura. O event hook de cura não é automaticamente um hook seguro de custo/efeito.

## Evidência, custos e interoperabilidade

- **Evidência estática:** [registro condicional 4.6.2](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java), [montagem de IDs em CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java); release source `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` e JAR da modlist `not_enough_glyphs-1.21.1-4.6.2.jar`. Equivalência dos métodos bytecode ao JAR **não verificada nesta etapa**.
- **Custo de execução:** o valor acima é default/inferência explicitamente localizada, não configuração efetiva; leitura dos arquivos `SERVER`, descontos, aquisição real e pagamento do Ars no pack ainda **⚠️ pendentes**.
- **Perks:** classes e campos verificados não demonstram hook RPG gravável. Superfície mutável homologada **NÃO VERIFICADA**; adapter, atribuição causal, deduplicação e testes **⛔ fail-closed**. Ars/NEG/Sauce detêm a execução e mana; RPG Skill Tree somente progressão por contrato; Black Arcana mantém seu runtime.
- **QA:** testes unitários, GameTest, dedicados, cliente/Survival, recarga, claim/PvP e composições com outros filtros permanecem pendentes. Esta é documentação técnica clean-room, sem código/asset externo incorporado.

[Índice](../../../README.md) · [Matriz](../../../PERK-ENGINEERING-MATRIX-4.6.2.md).
