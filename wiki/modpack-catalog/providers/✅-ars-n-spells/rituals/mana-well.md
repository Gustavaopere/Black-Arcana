# Mana Well

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:mana_well`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.4`.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- **✅ 3.3.4 JAR static registry ID:** `ars_n_spells:mana_well`, class `com.otectus.arsnspells.rituals.ManaWellRitual`, gate `IRONS_GATED`; [dossier](../EXACT-BINARY-RITUALS-3.3.4.md), [audit #38336011675](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38336011675). Functional semantics/Survival remain ⚠️.

The 3.3.0 NeoForge registration handler registers this ritual when Iron's Spellbooks is loaded. Iron's is present in the current physical pack.

## Semantics

Mana Well is a continuous ritual. At the source baseline its server tick:

- reads the provider-configured range;
- builds a bounded area around the brazier;
- walks the current level's player list rather than scanning all entity sections;
- grants the configured regeneration rate to players whose bounding boxes intersect the ritual area;
- routes each grant through the active Ars 'n' Spells `BridgeManager`.

Unlike Spell Transcription, Spellbook Binding, Spell Uninscription and Mana Infusion, Mana Well does **not** extend the provider's one-shot `AnsRitual` base in the audited source. Therefore the 60-tick one-shot duration must not be applied to Mana Well.

Exact duration/termination/config defaults beyond what the current source explicitly exposes remain provider-owned and are not guessed here.

## Deduplication boundary

Black Arcana must not run a parallel per-tick mana aura for the same ritual, duplicate each routed mana grant, or globally scan entities/chunks to reproduce this provider behavior.

If Black Arcana observes the ritual for its own approved hazard/progression purposes, observation must remain causal and deduplicated; provider mana routing remains authoritative.

## Engenharia para perks — métodos source 3.3.3 (não 3.3.4)

- **Source 3.3.3 real:** [`ManaWellRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/ManaWellRitual.java), commit `41fac17065c381104b17fdaab307d89ba21b49ab`; [`AnsRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/AnsRitual.java) para o lifecycle e [`AnsConfig.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/config/AnsConfig.java) para defaults. O JAR físico 3.3.4 já teve **identidade/gate** verificados, porém seus métodos não são declarados equivalentes a este source.
- **Executor contínuo:** herda diretamente `AbstractRitual`, **não** `AnsRitual`. `tick()` não define `setFinished()`; só retorna client-side/null world. Logo não possui o deadline de 60 ticks de rituals one-shot neste código.
- **Geometria/custo:** lê `range=AnsConfig.MANA_WELL_RANGE.get()` (default 8, range 1..64) e `regenRate=MANA_WELL_REGEN_RATE` (default **2.0 mana/tick**, range 0.1..100). AABB.inflate(range) em torno de `getPos`; itera `getWorld().players()` e admite players cujas bounding boxes intersectem essa AABB, em vez de buscar chunks/entidades do mundo inteiro.
- **Transferência:** para cada player aceito chama `BridgeManager.getBridge().addMana(p,regenRate)` **a cada tick do ritual**; não declara débito de Source por jogador no método. `onEnd(){}` sem side effects não prova que o ritual tenha limpeza de outro lifecycle ausente.
- **Perks:** crescimento contínuo soma no bridge nativo, não é uma série de casts; dedup de efeitos derivados e cap de ganho por tick precisam de hook real/observação física, sobretudo restart e multiplayer.
- **Estados separados:** ✅ identidade física 3.3.4, ✅ métodos localizados **na linha 3.3.3**, ⚠️ método exato 3.3.4/config instalada/teste Survival/CI ainda não demonstrados; ⛔ adapter RPG de custo/progressão/perk não implementado. Fonte somente para interoperabilidade, clean-room sem replicar implementação.
