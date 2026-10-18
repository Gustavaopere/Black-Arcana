# Ars Hex 5.0.4b — matriz de contratos técnicos para perks

**Prova binária posterior:** ✅ [workflow Java21 #39087382649](EXACT-PUBLISHER-PERK-SCYTHE-REFERENCES-5.0.4b.md) — hash SHA-1 do JAR publicado 5.0.4b validado, 13/13 autotestes e seis classes compiladas com referências delimitadas; operações/atributos e ingressos da foice confirmados por marcadores, mas **coeficientes, dataflow, pagamento de mana e execução real continuam source-pinned / ⚠️**. Nenhum adapter. [Relatório técnico detalhado](EXACT-PUBLISHER-PERK-SCYTHE-REFERENCES-5.0.4b.md).

**Escopo auditado (17/10/2026):** ✅ glyph próprio 1/1 registrado no JAR; ✅ 3/3 perks de thread e 1/1 equipamento spell-on-hit com fichas individuais **SOURCE_CAUSALITY**; **+0 magias**, +0 adapters, nenhuma equivalência bytecode completa/QA físico certificada nesta tranche. Este denominador de objetos de engenharia não é o denominador de identidades mágicas. Source pin oficial `Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227`.

| Objeto / ID | Owner efetivo | Alteração técnica observada | Faixa de perk segura agora? | Ficha |
|---|---|---|---|---|
| `ars_hex:glyph_soul_shatter` | Ars resolver + Malum VOODOO | base damage `5+3*amp`, mana base 30, Amplify máx. 2; tipo de dano Malum | ⛔ sem QA de host/cast | [Soul Shatter](glyphs/soul-shatter.md) |
| `ars_hex:thread_soul_ward` | Ars thread → Malum attributes | capacidade `+2*slotValue` ADD_VALUE; integridade `+0.5*slotValue` ADD_MULTIPLIED_BASE | ⛔ modifier/stack QA | [Soul Ward](perks/soul-ward.md) |
| `ars_hex:thread_magic_proficiency` | Ars thread → Lodestone attribute | `+0.1*slotValue` ADD_MULTIPLIED_BASE | ⛔ consumers/dano final QA | [Magic Proficiency](perks/magic-proficiency.md) |
| `ars_hex:thread_soul_spoils` | Ars thread → Malum attribute | `+slotValue` ADD_VALUE | ⛔ reward settlement QA | [Spirit Spoils](perks/spirit-spoils.md) |
| `ars_hex:enchanter_scythe` | Ars resolver + Malum weapon | `hurtEnemy`→target entity; boomerang `LivingDamageEvent.Post`; desconto `ceil(Σ(0.2*necromancy_cost))` | ⛔ provenance/duplo hit QA | [Enchanter's Scythe](equipment/enchanters-scythe.md) |

## Campos de implementação
- **Target/range/área/projétil:** os três threads alteram atributos de equipamento; não são casts com geometria. Soul Shatter usa target via Ars, não introduz setter de alcance aqui; foice usa `EntityHitResult(target)` em seu `hurtEnemy`.
- **Tipo de dano:** somente Soul Shatter fornece o tipo `VOODOO` no effect; outros atributos e a foice não fornecem troca genérica de `DamageType`.
- **Tempo, duração, cooldown:** provider-owned quando existem; não foram inferidos valores de threads/foice.
- **Custos:** Soul Shatter declara mana-base 30 no source; scythe expõe apenas a equação de desconto, sujeita à resolução de mana Ars.
- **Lançamento/atribuição:** `applyAttributeModifiers` não é casting; `hurtEnemy`/boomerang não equivalem necessariamente a nova intenção do player.

## Próximos gates verificáveis
1. Confrontar classfiles dos 3 `Perk` e `EnchanterScythe` no JAR `ars_hex-1.21.1-5.0.4b.jar` cujo SHA físico foi catalogado.
2. No servidor com Malum/Ars/Lodestone, observar `AttributeInstance` antes/durante/depois de thread slot/equip/reload, com dois slots e respec/remoção.
3. Inspecionar transações de mana, tick e origem causal de cast/boomerang/Reactive na foice; deduplicação para Mastery, dano e proc.
4. Sem hook real seguro de controle de destino, área, raio ou tipo de dano: permanecer **⛔ fail-closed**.

Fontes primárias: [registry source `ArsNouveauRegistry.java#L19-L48`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/ArsNouveauRegistry.java#L19-L48); [foice `EnchanterScythe.java`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/malum/EnchanterScythe.java); [bridge `MalumCompat.java`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/malum/MalumCompat.java). [Auditoria binária anterior](EXACT-BINARY-GLYPH-5.0.4b.md). **Sem copiar código/asset upstream.**
