# Spell Transcription

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:spell_transcription`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.4`.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- **✅ 3.3.4 JAR static registry ID:** `ars_n_spells:spell_transcription`, class `com.otectus.arsnspells.rituals.SpellTranscriptionRitual`, gate `IRONS_GATED`; [dossier](../EXACT-BINARY-RITUALS-3.3.4.md), [audit #38336011675](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38336011675). Functional semantics/Survival remain ⚠️.

This ritual is registered by the 3.3.0 NeoForge baseline only when `irons_spellbooks` is loaded. Iron's is physically present in the current pack.

## Semantics

The ritual transcribes one supported spell-bearing source onto one supported blank carrier target through the provider's cross-cast serialization path.

The audited NeoForge baseline performs validation before mutation and distinguishes:

- existing ANS-inscribed items;
- exactly one source;
- exactly one blank target;
- targets already carrying a rooted Ars spell;
- provider-defined inscription-plan rejection;
- source parse failure;
- Ars payloads containing provider-blacklisted/caster-bound glyphs.

The 3.3.0 NeoForge hardening also prevents a dropped stack of blank targets from being duplicated into a fully inscribed stack: the provider plan authorizes the output count and preserves the remainder. Reusable books/foci can be read without being consumed when the provider plan marks them reusable; disposable sources are consumed only by the authorized amount.

Baseline search radius: **3 blocks** around the brazier.

This is a one-shot `AnsRitual` at the source baseline, using the default **60 server-tick** completion lifecycle.

## Deduplication boundary

Black Arcana must not serialize arbitrary Ars spell graphs into foreign carriers itself, guess whether a source is disposable, bypass the provider blacklist, or mutate carrier state before provider validation completes.

A transcribed payload remains Ars 'n' Spells/host-owned data. Black Arcana may observe an approved provider outcome through a real adapter, but must not become a second inscription authority.

## Engenharia para perks — métodos source 3.3.3 (não 3.3.4)

- **Source 3.3.3 real:** [`SpellTranscriptionRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/SpellTranscriptionRitual.java), commit `41fac17065c381104b17fdaab307d89ba21b49ab`; [`AnsRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/AnsRitual.java) para o lifecycle e [`AnsConfig.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/config/AnsConfig.java) para defaults. O JAR físico 3.3.4 já teve **identidade/gate** verificados, porém seus métodos não são declarados equivalentes a este source.
- **Sequência de validação:** `onEnd` consulta `AABB.inflate(3)` e chama `InscriptionInputs.classify`; recusa qualquer já inscrito; exige **exatamente uma entidade** source e uma entidade blank, target sem Ars spell enraizado, source parseável, blacklist de caster-bound glyphs e `InscriptionPlanner.plan` permitido.
- **Contabilidade efetiva:** `InscriptionOutcome.of(plan,sourceStack.getCount(),targetStack.getCount())` fixa `transformedTargets`, `targetRemainder` e `consumedFromSource`. Apenas `copyWithCount(outcome.transformedTargets())` fica inscrito; o resto do target permanece blank. Se há resto, `dropBeside(...)` deve retornar true antes de o original e a source sofrerem shrink/mutação.
- **Branch source:** para `CrossSpellType.ARS_NOUVEAU` invoca `CrossCastingHandler.addCrossModSpell(inscribed,source.arsSpell)`; para `IRONS_SPELLBOOKS` usa `(source.spellId,source.spellLevel,type)`. Se plano diz source reutilizável (`consumedFromSource=0`), não a consome; caso contrário diminui **somente** unidades autorizadas.
- **Risco de transactional boundary:** o snippet não mostra rollback geral para exceção inesperada após a criação do output; não presumir garantia universal. A receita original e o runtime **3.3.4** introduziram revisões de payment/cast que devem ser verificados no JAR exato.
- **Perks:** Nunca emitir segunda inscrição, reabrir stack de 64 ou creditar sucesso por VFX antes de observar resultado estável provider-owned. Dados ANS no carrier não são um novo registro de feitiço.
- **Estados separados:** ✅ identidade física 3.3.4, ✅ métodos localizados **na linha 3.3.3**, ⚠️ método exato 3.3.4/config instalada/teste Survival/CI ainda não demonstrados; ⛔ adapter RPG de custo/progressão/perk não implementado. Fonte somente para interoperabilidade, clean-room sem replicar implementação.
