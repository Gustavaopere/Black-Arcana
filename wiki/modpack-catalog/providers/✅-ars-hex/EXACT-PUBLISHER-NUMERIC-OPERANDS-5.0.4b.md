# Ars Hex 5.0.4b — prova binária delimitada de constantes e operandos

**Checkpoint 17/10/2026 — ✅ `PUBLISHER_BINARY_CONSTANT_PRESENCE` · ⚠️ ausência de prova de dataflow completo / runtime · ⛔ adapters sem homologação.** Este relatório complementa [a auditoria anterior de seis classes](EXACT-PUBLISHER-PERK-SCYTHE-REFERENCES-5.0.4b.md), sem reclassificar a lógica inteira como `BINARY_FORMULA_EXACT`.

## Evidência executada

- [GitHub Actions #39089774180](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39089774180), job `inspect_publisher_perk_bytecode`: **SUCCESS**. Logs confirmam **13/13** autotestes de referência mais **12/12** autotestes de constantes, sem falhas.
- Download do JAR publisher CurseForge file `7404679`, `ars-hex-unity-1357380-7404679.jar`: **SHA-1 `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4` validado**, 273389 bytes esperados. Este SHA coincide com o registro histórico da modlist física, mas não é um novo hash local do perfil.
- Validação de referência original: `PASS_BOUNDED_BYTECODE_REFERENCES`, desvios `[]`.
- Novo verificador: `PASS_BOUNDED_NUMERIC_OPERANDS`, desvios `[]`. Resultados do job publicados no **artefato JSON #12121819084** (ZIP compactado de 2024 bytes com os dois relatórios), sem redistribuir o JAR.
- [Verificador numérico Python](../../../../docs/qa/ars_hex_504b_numeric_operands.py), [workflow Java 21](../../../../.github/workflows/ars-hex-504b-perk-bytecode.yml). Somente inspeção read-only de `javap -p -c -s` após o gate SHA, sem classloading do provider.

## Resultados do escopo exato

| Objeto compilado / método | Prova nova limitada | Contrato source que ainda exige dataflow/QA |
|---|---|---|
| `SoulWardPerk.applyAttributeModifiers` | `iconst_2`, constante double `0.5`, multiplicação e carregamento do argumento `slotValue` | (+2 × slotValue) para capacidade; (+0,5 × slotValue) em `ADD_MULTIPLIED_BASE` para integridade |
| `MagicProficencyPerk.applyAttributeModifiers` | constante double `0.1`, multiplicação e leitura do argumento `slotValue` | `0.1 × slotValue` no atributo Lodestone `MAGIC_PROFICIENCY` |
| `SpiritSpoilsPerk.applyAttributeModifiers` | carregamento do argumento `slotValue` no método compilado | `slotValue` como incremento `ADD_VALUE`; payout efetivo Malum desconhecido |
| `EnchanterScythe.getManaDiscount` | constante double `0.2` e opcode de multiplicação | `ceil(sum(0.2 × cost))` das partes Necromancy; aplicação de custo/refund no host não testada |

O verificador detecta instruções dentro de **métodos declarados únicos** e rejeita constantes trocadas, operações removidas, carregamentos ausentes, comentários não numéricos e classes/métodos ausentes. Os testes sintéticos foram executados em Java 21 no runner com Python 3; **não** são GameTests do Minecraft.

## Interpretação e limites

**Fato compilado:** o JAR SHA-exato carrega as constantes/opcodes esperados dentro dos métodos correspondentes. **Fato de source:** as fórmulas de referência usadas nas fichas derivam do código upstream `Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227`. **Ainda não demonstrado:** uma análise def-use/CFG que prove qual constante alimenta qual `withModifierAdded`, ordem entre multiplicação/atributos, tratamento de conflitos, equip/unequip, compatibilidade real de Malum/Lodestone/Ars, execução de hit/boomerang e consumos de mana.

A auditoria é deliberadamente fail-closed: se o JAR não coincidir com o SHA de referência, ou se um símbolo, constante ou operação não aparecer na fronteira esperada, o workflow falha. Um `PASS` não representa homologação de perks, alvo/área, dano, cooldown ou Mastery; o RPG Skill Tree continua dono da progressão e Black Arcana do seu próprio runtime.

**Métricas imutáveis nesta rodada:** Ars Hex ✅ `1/1` glifo próprio; ✅ `3/3` perks auxiliares e `1/1` equipamento com fichas causais e prova delimitada; **+0** magias, **+0** adapters. Global **1.857 mínimo / 1.855 estritos**, denominador final **—%**. Stage 06.05 🟡; Stage 09 QA real-client pendente; PR #825 draft sem merge.
