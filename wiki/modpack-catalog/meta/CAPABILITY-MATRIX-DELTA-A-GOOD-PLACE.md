# Capability Matrix Delta — A Good Place 1.21-1.2.5

Status: `CATALOGED / CLIENT PLACEMENT PRESENTATION / +0 SEMANTIC MAGIC ACTIONS`

| A Good Place capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| placement animation | client visual response to accepted block placement | never use as casting/gameplay authority |
| Resource Pack animation definitions | data-driven visual configuration | presentation data only |
| block-state predicates | choose which animation applies | no semantic magic identity |
| scale/translation/rotation | visual transforms | no action identity |
| rotation pivot | render transform origin | presentation only |
| duration/curves | interpolation timing | presentation only |
| restrict direction | chooses visible approach direction | presentation only |
| optional sound | visual event feedback | not a magical resource/action |
| block-entity handling | rendering compatibility surface | UI/runtime QA only |
| shader/VFX composition | external render interaction | no gameplay overlap |

## Semantic boundary

A Good Place is not a spell provider.

It does not own:

- casting;
- spell identity;
- ritual state;
- magical resources;
- progression;
- damage/healing;
- authoritative placement.

Therefore:

- spells: **0**;
- rituals/rites: **0**;
- equivalent discrete magical actions: **0**.

Strict semantic delta: **+0**.

## Runtime boundary

The server/provider initiating the placement owns the final world state.

A Good Place owns only the client presentation of that state transition.

Catalog closure does not imply renderer compatibility PASS.
