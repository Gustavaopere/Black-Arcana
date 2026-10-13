# Ritual Catalog — Ars 'n' Spells 3.3.4

This index has **✅ five exact ritual static binary IDs/gates** from physical 3.3.4 ([dossier](../EXACT-BINARY-RITUALS-3.3.4.md), [CI #38336011675](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38336011675)). Functional semantics still derive from the older 3.3.0 source, not verified 3.3.4 runtime. Count remains **5**, +0 new objects.

Under the physical pack condition where Iron's Spellbooks is installed, the baseline registers five ritual identities:

| Registry identity | Type | Current semantic role |
|---|---|---|
| `ars_n_spells:spell_uninscription` | one-shot / unconditional | remove/reconcile Ars 'n' Spells-owned inscription state |
| `ars_n_spells:spell_transcription` | one-shot / Iron's-gated | transcribe one supported spell source onto one carrier target |
| `ars_n_spells:spellbook_binding` | one-shot / Iron's-gated | bind exported Ars payload into an Iron's spellbook/native wheel flow |
| `ars_n_spells:mana_infusion` | one-shot / Iron's-gated | provider-routed configured mana grant |
| `ars_n_spells:mana_well` | continuous / Iron's-gated | provider-routed area mana regeneration |

Individual pages:

- [Spell Uninscription](spell-uninscription.md)
- [Spell Transcription](spell-transcription.md)
- [Spellbook Binding](spellbook-binding.md)
- [Mana Infusion](mana-infusion.md)
- [Mana Well](mana-well.md)

The four one-shot entries extend the baseline `AnsRitual` lifecycle with a default 60-server-tick completion interval. Mana Well does not use that one-shot base and must not inherit that duration by assumption.

The five ritual identities count as provider capabilities. The eight internal `ars_cross_*` Iron's proxy objects are cataloged separately as transport infrastructure and are not added to the ritual or standalone-spell count.