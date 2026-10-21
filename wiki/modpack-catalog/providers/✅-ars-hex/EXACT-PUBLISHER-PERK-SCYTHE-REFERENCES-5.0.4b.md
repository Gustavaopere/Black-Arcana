# Ars Hex 5.0.4b — prova binária limitada de perks e foice

**Estado (17/10/2026): ✅ PUBLISHER_BINARY_REFERENCES_ONLY para 6 classes / ⚠️ operandos e runtime não provados / ⛔ adapters.** Esta auditoria expande a prova anterior de registry do glifo, mas **não** cria quatro novos spells nem certifica compatibilidade de jogo.

## Prova independente executada

- [GitHub Actions #39087382649](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39087382649) — job `inspect_publisher_perk_bytecode` **SUCCESS**, Java 21, 13/13 testes sintéticos e verificação estática no JAR publicado.
- Artefato JSON **12121013880**, nome `ars-hex-504b-perk-bounded-55f8421f72acbfc712c60e9a1c03b24be5568f59`. Os logs mostram download SHA OK, `PASS_BOUNDED_BYTECODE_REFERENCES` e `deviations=[]`. O hash do artefato ZIP é `4d6b0d082ed85107b9886ef71688745d81c85d729cfea216410d245dd998c846` (não é hash do JAR).
- JAR publicado: [CurseForge Ars Hex Unity file 7404679](https://www.curseforge.com/minecraft/mc-mods/ars-hex-unity/files/7404679), **273389 bytes**, SHA-1 **`2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`**. Corresponde ao SHA-1 histórico da modlist física, mas não houve nova leitura do disco do usuário.
- Novos arquivos: [verificador fail-closed Java21](../../../../docs/qa/ars_hex_504b_perk_bytecode.py) e [workflow](../../../../.github/workflows/ars-hex-504b-perk-bytecode.yml). A auditoria não redistribui o JAR; publica apenas JSON estreito.

## Assinaturas/callsites delimitados

| Classe | Referências compiladas provadas |
|---|---|
| `ArsNouveauRegistry` | gate `malum`/`isLoaded`, exatamente 3 invocações `PerkRegistry.registerPerk`, três singletons correspondentes |
| `SoulWardPerk` | `SOUL_WARD_CAPACITY`, `SOUL_WARD_INTEGRITY`, `ADD_VALUE`, `ADD_MULTIPLIED_BASE` e `withModifierAdded` |
| `MagicProficencyPerk` | `MAGIC_PROFICIENCY`, `ADD_MULTIPLIED_BASE`, `withModifierAdded` |
| `SpiritSpoilsPerk` | `SPIRIT_SPOILS`, `ADD_VALUE`, `withModifierAdded` |
| `EnchanterScythe` | `hurtEnemy` contém `SpellContext`, `SpellResolver`, `onCastOnEntity`; scribing menciona `MethodTouch`; desconto usa `NECROMANCY`, `getCastingCost`, `ceil` |
| `MalumCompat` | callback `workaround` contém `ScytheBoomerangEntity`, `getDirectEntity`, `hurtEnemy` |

`javap` executou sobre classfiles da distribuição real SHA-verificada, sem carregamento de classes em JVM do Minecraft. O algoritmo exige métodos declarados únicos e marcadores observáveis nos respectivos métodos; o registro conta instruções efetivas `invokestatic` para `PerkRegistry.registerPerk`.

**Limite importante:** não houve rastreamento dataflow/CFG suficiente para demonstrar os coeficientes `2`, `0.5`, `0.1`, `0.2`, a ordem de operações, a eficácia de `getManaDiscount` na cobrança, o número de chamadas de `hurtEnemy` por hit ou a execução do ramo Reactive. Esses valores e relações permanecem `SOURCE_CAUSALITY` da revisão [Ars-Unity@b25528a](https://github.com/Alexthw46/Ars-Unity/tree/b25528adf8c0135585cd6d654582efa147e0a227), não promovidos automaticamente a `BINARY_OPERAND_EXACT`.

## Consequências para engenharia de perks

- Não atribuir Mastery a `applyAttributeModifiers` ou callbacks boomerang sem origem de cast observável e deduplicação.
- Validar `AttributeInstance` em player real (equip/unequip, dois slots, restart, reload) antes de usar multiplicadores ou aumentar caps.
- A foice possui caminho potencial de execução derivado; não tratar `onCastOnEntity` como cast novo de Black Arcana, não criar segunda cobrança de mana, dano ou progressão.
- Preservar autoridade Ars (spell/thread/mana), Malum (spirit, soul ward, scythe), Lodestone (proficiency), RPG Skill Tree (progressão/perks) e Black Arcana (runtime mágico próprio).
- **⚠️** Paridade fresca do JAR local e runtime físico/cliente/modpack completo pendentes; **⛔** nenhum hook/adapter de alvo, área, dano, cooldown ou Mastery homologado.

**Contagem:** catálogo mágico global mínimo **1.857 semânticos / 1.855 estritos** e denominador —%; Ars Hex **1/1 glyph**, **3/3 perks e 1/1 foice** (objetos auxiliares não contabilizados como magias); **+0 novas raízes**, **+0 adapters**, Stage 06.05 🟡 / Stage 09 físico PENDING. A PR #825 continua em draft e esta prova não justifica merge.
