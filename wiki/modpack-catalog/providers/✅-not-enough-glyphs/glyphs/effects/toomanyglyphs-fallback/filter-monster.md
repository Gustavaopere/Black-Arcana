# Filter: Monster — dossiê técnico 4.6.2

**ID completo:** `toomanyglyphs:glyph_filter_monster` · **implementação:** `alexthw.not_enough_glyphs.common.glyphs.filters.FilterMonster` · **registry role:** fallback de Too Many Glyphs porque `toomanyglyphs` não está instalado · **aquisição no catálogo anterior:** Lily of the Valley (datapack do pack ainda não revalidado).

**Source pin:** [`FilterMonster.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/filters/FilterMonster.java) · `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77`.

## Predicado verificável / parâmetros

Exige `FilterLiving` e `target.getEntity().getClassification(false) == MobCategory.MONSTER`. Não testa explicitamente se pertence à classe base `Monster` nem verifica hostilidade atual, time/faction, dominação ou neutralidade.

A implementação base [AbstractEffectFilter](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/filters/AbstractEffectFilter.java) herda [AbstractFilter Ars 5.13.1](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractFilter.java): `getDefaultManaCost()=0`, `AbstractEffectFilter.getTypeIndex()=15`, escola `MANIPULATION`, `onResolve` cancela o contexto quando `shouldAffect` retorna false. O caminho efetivo da interface de filtro e seus callsites não foi certificado fisicamente; **0 mana é default herdado, não débito configurado**. A base contém `inverted` mutável, mas só declarar uso quando comprovado pela subclasse.

**Perks e compatibilidade:** Classification pode divergir do comportamento de ataque de mobs customizados. Não transferir isto para friendly-fire ou consentimento BA.

## Evidência, custos e interoperabilidade

- **Evidência estática:** [registro condicional 4.6.2](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java), [montagem de IDs em CompatRL](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java); release source `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` e JAR da modlist `not_enough_glyphs-1.21.1-4.6.2.jar`. Equivalência dos métodos bytecode ao JAR **não verificada nesta etapa**.
- **Custo de execução:** o valor acima é default/inferência explicitamente localizada, não configuração efetiva; leitura dos arquivos `SERVER`, descontos, aquisição real e pagamento do Ars no pack ainda **⚠️ pendentes**.
- **Perks:** classes e campos verificados não demonstram hook RPG gravável. Superfície mutável homologada **NÃO VERIFICADA**; adapter, atribuição causal, deduplicação e testes **⛔ fail-closed**. Ars/NEG/Sauce detêm a execução e mana; RPG Skill Tree somente progressão por contrato; Black Arcana mantém seu runtime.
- **QA:** testes unitários, GameTest, dedicados, cliente/Survival, recarga, claim/PvP e composições com outros filtros permanecem pendentes. Esta é documentação técnica clean-room, sem código/asset externo incorporado.

[Índice](../../../README.md) · [Matriz](../../../PERK-ENGINEERING-MATRIX-4.6.2.md).
