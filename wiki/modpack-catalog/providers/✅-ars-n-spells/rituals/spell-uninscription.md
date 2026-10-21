# Spell Uninscription

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:spell_uninscription`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.4`.
- Current physical/release line: 3.3.4; detailed implementation evidence remains source-pinned as stated below.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- **✅ 3.3.4 JAR static registry ID:** `ars_n_spells:spell_uninscription`, class `com.otectus.arsnspells.rituals.SpellUninscriptionRitual`, gate `ALWAYS`; [dossier](../EXACT-BINARY-RITUALS-3.3.4.md), [audit #38336011675](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38336011675). Functional semantics/Survival remain ⚠️.

The 3.3.0 NeoForge `RitualRegistryHandler` registers this ritual unconditionally, including when Iron's Spellbooks is absent.

## Semantics

At the source baseline the ritual cleans one supported ANS-inscribed item. It validates the nearby item set before mutation, rejects ambiguous source/blank combinations, and requires exactly one inscribed target.

The provider cleanup path removes Ars 'n' Spells-owned cross-cast state and reconciles provider-owned native proxy entries rather than treating unrelated/native spells as ANS state.

Baseline search radius: **3 blocks** around the brazier.

This is a one-shot `AnsRitual` at the source baseline. The shared one-shot lifecycle finishes after the provider's default **60 server ticks** unless overridden; this ritual does not override that duration in the audited source.

## Deduplication boundary

Black Arcana must not independently strip Ars 'n' Spells carrier components/proxy entries or create its own cleanup format. If Black Arcana ever exposes an integration action for this lifecycle, provider-native cleanup is authoritative.

Do not infer that every arbitrary item with Ars/Iron's data is a valid uninscription target. Eligibility remains provider-owned.

## Engenharia para perks — métodos source 3.3.3 (não 3.3.4)

- **Source 3.3.3 real:** [`SpellUninscriptionRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/SpellUninscriptionRitual.java), commit `41fac17065c381104b17fdaab307d89ba21b49ab`; [`AnsRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/AnsRitual.java) para o lifecycle e [`AnsConfig.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/config/AnsConfig.java) para defaults. O JAR físico 3.3.4 já teve **identidade/gate** verificados, porém seus métodos não são declarados equivalentes a este source.
- **Lifecycle:** `SpellUninscriptionRitual extends AnsRitual`; o executor pai server-side incrementa progress por tick e chama `setFinished()` em `progress>=60` por default. `onEnd()` retorna sem ação se mundo/posição null ou client side; inicia uma consulta `ItemEntity` vivos/não vazios em `AABB(brazier).inflate(3)`.
- **Admissão:** `InscriptionInputs.classify(entities)` diferencia fontes, blanks e inscritos; o ritual recusa *qualquer* fonte ou blank, exige `inputs.inscribed.size()==1` e não tenta adivinhar outro alvo no range. A quantidade **de entidades** é a usada no check, não prova de `ItemStack.count==1` sem classificador.
- **Settlement:** somente após validar chama `IronsBookBindingUtil.removeAllArsEntries(stack)` e atualiza `inscribedEntity.setItem(stack)`; essa rotina também limpa proxies do wheel e sidecar/export marker, mas a ordem e o detalhe do helper precisam ser consultados para modificar estado. Partículas/som e mensagem são pós-operação, não events de sucesso compartilhados com RPG.
- **Perks/QA:** a limpeza é a operação nativa ANS, não um ritual Black Arcana nem exclusão genérica de dados de outro mod. Falhas de validação não devem gerar Mastery; progresso do tempo não é prova de remoção.
- **Estados separados:** ✅ identidade física 3.3.4, ✅ métodos localizados **na linha 3.3.3**, ⚠️ método exato 3.3.4/config instalada/teste Survival/CI ainda não demonstrados; ⛔ adapter RPG de custo/progressão/perk não implementado. Fonte somente para interoperabilidade, clean-room sem replicar implementação.
