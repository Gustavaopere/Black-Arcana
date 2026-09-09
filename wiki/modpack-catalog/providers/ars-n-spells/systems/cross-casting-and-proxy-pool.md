# Cross-Casting and Proxy Pool

## Evidence boundary

Physical runtime is Ars 'n' Spells `3.3.2`. Registry/proxy implementation facts below are source-pinned to the official NeoForge 1.21.1 `3.3.0` branch at `a9930223c96806e5d748ea69d02f9a32cab62de9`. Exact 3.3.2 binary internals remain unverified.

## Finite native-wheel proxy pool

With Iron's Spellbooks present, the baseline registers eight real Iron's `AbstractSpell` objects:

- `ars_n_spells:ars_cross_1`
- `ars_n_spells:ars_cross_2`
- `ars_n_spells:ars_cross_3`
- `ars_n_spells:ars_cross_4`
- `ars_n_spells:ars_cross_5`
- `ars_n_spells:ars_cross_6`
- `ars_n_spells:ars_cross_7`
- `ars_n_spells:ars_cross_8`

`CrossModSpellComponents.PROXY_POOL_SIZE` is **8** at the source baseline.

These registry objects are infrastructure. A bound Ars spell claims a proxy slot so Iron's native wheel can resolve a legitimate registered id; the actual spell recipe/payload remains serialized Ars data associated with the carrier/book entry.

## Semantic count

- Real Iron's registry objects contributed for proxy transport: **8 baseline objects**.
- Distinct standalone semantic spells represented by the fixed proxy identities themselves: **0**.
- Maximum distinct Ars entries representable in one native Iron's wheel through this pool at the baseline: **8**.

The same proxy id may represent different serialized Ars payloads on different carriers/books; counting `ars_cross_3` as a fixed offensive spell would therefore destroy causal identity.

## Accounting boundary

The baseline source explicitly treats the proxy as a zero-cost/placeholder transport identity whose real cost, school and cooldown belong to the delegated Ars cast. Provider-side accounting avoids attributing ordinary Iron's affinity/cooldown/progression/mana to the placeholder as though it were the actual payload.

Black Arcana must preserve the same causal distinction:

1. one user action selects one bound Ars payload;
2. Iron's native wheel resolves a proxy transport id;
3. Ars 'n' Spells delegates to the Ars cast pipeline;
4. resource/school/cooldown outcome belongs to the provider-routed real cast;
5. Black Arcana must not create a second cast/proc because it observed both proxy and delegated payload.

## Network and authority rule

A client-selected wheel entry is not authority for cost, payload, progression or success. Any Black Arcana integration must consume a verified server/provider result and must not introduce a second C2S path that bypasses Ars 'n' Spells carrier/proxy validation.

If no safe 3.3.2 hook exists to correlate proxy and delegated cast identities, integration remains fail-closed rather than risking double processing.