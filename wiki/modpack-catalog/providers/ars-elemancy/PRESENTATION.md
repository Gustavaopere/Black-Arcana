# Ars Elemancy 1.18.3 — presentation-only surfaces

Status: `SOURCE-PINNED / CLIENT QA PENDING`

## Focus rendering

When client config `Enable SpellFocusRender=true`, the seven foci register Curios renderers. This is presentation only and never gameplay authority.

## Starbuncle name skins

Static initialization adds Ars Nouveau Starbuncle texture/model mappings for:

- Frostbuncle;
- Pyrobuncle;
- Cavebuncle;
- Cloudbuncle;
- Sculkbuncle;
- Sandbuncle;
- Lyrellion.

A Faebuncle block exists only as commented source and is not active.

### Source discrepancy

The Pyrobuncle block stores its texture under key `Pyrobuncle`, but writes the model into `Starbuncle.MODELS` using key **`Frostbuncle`** instead of `Pyrobuncle`. This can overwrite the Frostbuncle model mapping and leaves Pyrobuncle without a matching local model key in that block.

Phase 2T records this exact source defect and does not infer the final rendered result in the installed client. `CLIENT QA REQUIRED`.

No visual mapping is used as evidence for spell, damage, ownership or progression.