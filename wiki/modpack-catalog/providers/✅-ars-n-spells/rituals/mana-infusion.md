# Mana Infusion

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:mana_infusion`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.4`.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- **✅ 3.3.4 JAR static registry ID:** `ars_n_spells:mana_infusion`, class `com.otectus.arsnspells.rituals.ManaInfusionRitual`, gate `IRONS_GATED`; [dossier](../EXACT-BINARY-RITUALS-3.3.4.md), [audit #38336011675](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38336011675). Functional semantics/Survival remain ⚠️.

The 3.3.0 NeoForge registration handler registers this ritual when Iron's Spellbooks is loaded. Iron's is present in the current physical pack.

## Semantics

Mana Infusion is a one-shot ritual that resolves the provider's ritual recipient and grants a configured mana amount through `BridgeManager` rather than directly owning either host pool.

At the source baseline the mana grant therefore follows the active Ars 'n' Spells bridge routing rather than Black Arcana or the ritual itself becoming a separate mana authority.

This ritual uses the provider's one-shot `AnsRitual` lifecycle and its default **60 server-tick** completion interval.

## Deduplication boundary

Black Arcana must not mirror the grant into a second pool, independently choose which host pool receives it, or award a second grant after observing provider completion.

The configured amount, active routing mode and settlement remain provider-owned. If an exact 3.3.4 integration hook is needed, it remains fail-closed until that hook is verified on the installed artifact.

## Engenharia para perks — métodos source 3.3.3 (não 3.3.4)

- **Source 3.3.3 real:** [`ManaInfusionRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/ManaInfusionRitual.java), commit `41fac17065c381104b17fdaab307d89ba21b49ab`; [`AnsRitual.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/rituals/AnsRitual.java) para o lifecycle e [`AnsConfig.java`](https://github.com/otectus/ars-n-spells/blob/41fac17065c381104b17fdaab307d89ba21b49ab/src/main/java/com/otectus/arsnspells/config/AnsConfig.java) para defaults. O JAR físico 3.3.4 já teve **identidade/gate** verificados, porém seus métodos não são declarados equivalentes a este source.
- **Lifecycle:** herda `AnsRitual` server-only com completion default 60 ticks; `onEnd()` primeiro verifica mundo/server, então resolve `Player player=recipient()` (UUID do iniciador persistido ou fallback de proximidade segundo `RitualFeedback`), retorna se null.
- **Transação:** chama **uma vez** `BridgeManager.getBridge().addMana(player,AnsConfig.RITUAL_MANA_INFUSION_AMOUNT.get().floatValue())`. Valor default no source da linha 3.3.3 é **500.0** e faixa config 1..10000. Isso é amount enviado ao bridge, não mana *efetivamente recebida* depois de caps/regras host.
- **Perks:** Ars 'n' Spells decide a fonte/rota de mana, Black Arcana não cria pool alternativo nem concede 500 extra. Não recompensar 60 progress ticks como 60 infusões, e não inferir que a mesma função existe byte-idêntica no 3.3.4.
- **Estados separados:** ✅ identidade física 3.3.4, ✅ métodos localizados **na linha 3.3.3**, ⚠️ método exato 3.3.4/config instalada/teste Survival/CI ainda não demonstrados; ⛔ adapter RPG de custo/progressão/perk não implementado. Fonte somente para interoperabilidade, clean-room sem replicar implementação.
