# Spellbook Binding

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:spellbook_binding`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.2`.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- Exact 3.3.2 binary registry parity: `NÃO VERIFICADO`.

This ritual is registered by the 3.3.0 NeoForge baseline only when Iron's Spellbooks is loaded. The current physical pack contains Iron's `1.21.1-3.16.3`.

## Semantics

The baseline binds one valid exported Ars carrier scroll into one Iron's spellbook so the serialized Ars spell can appear through Iron's native spell-selection flow.

Validation precedes mutation and includes:

- provider configuration kill switch for Ars spells in Iron's spellbooks;
- exactly one recognized carrier scroll;
- exactly one Iron's spellbook;
- no unrelated item in the ritual area;
- readable/castable Ars payload;
- duplicate rejection;
- provider-defined capacity/proxy-slot availability;
- rollback/failure handling if the native container refuses the entry.

Only after a successful provider append does the ritual consume one scroll. A failed duplicate/full/native-container operation does not become a successful binding.

Baseline search radius: **3 blocks** around the brazier.

The source baseline has a fixed native-wheel proxy pool of **8** slots. A configuration value cannot turn those transport slots into more than the provider's actual proxy capacity.

This is a one-shot `AnsRitual` at the source baseline, using the default **60 server-tick** lifecycle.

## Deduplication boundary

Black Arcana must not allocate `ars_cross_*` ids, rewrite Iron's spellbook containers, bypass the provider kill switch, or create a second native-wheel binding route.

The successful bound spell is still one Ars spell executed through provider routing. It must not be processed once as the proxy and again as the serialized Ars payload.