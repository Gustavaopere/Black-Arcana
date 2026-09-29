- quest prose;
- datapack payload bodies;
- player data;
- raw log lines, timestamps, thread names, chat/player message bodies and unrelated log content;
- saves;
- authentication/secrets;
- unrelated mod configuration.

Only relative paths, selected values, file hashes, bounded exact-literal locations and whitelisted structured catalog-probe fields are emitted.

Review the JSON before attaching it anywhere.

## Evidence discipline

A collector result is **evidence input**, not an automatic catalog promotion.

For every provider:

1. verify the report came from the actual current pack/world;
2. match physical hashes to the current modlist/provider line;
3. apply the provider's canonical acceptance rule;
4. update only the rows actually proven;
5. preserve fail-closed state for missing/ambiguous values;
6. keep runtime/integration QA separate from catalog closure.

Do not convert missing files into source-default values unless the actual runtime/config contract proves that fallback for the deployed environment.

## Current blockers this can reduce

- Asterism: deployed Astral Gateway Iron's spell config/datapack;
- Gaze: effective `disableGazeRites`;
- NEG: effective enabled state for 39 candidates, via deployed TOML evidence or schema-3 exact-server `type=glyph` runtime observations;
- Corail Tombstone: physical 9.5.6 equality plus the 12 bounded `AllowedMagicItems` booleans that gate the remaining tablets/gemstones/Grave Key/Lost Tablet/Magic Scroll/Scroll of Knowledge candidates; semantic deduplication and reachability still require provider-specific review;
- Somake: physical equality and 83/83 registration composition are already closed canonically; the collector can corroborate the installed hash and reduce the remaining deployed `enableSpellLockSystem` plus Iron's per-spell/global/datapack `enabled` / `school` / `allow_crafting` gates;
- Mowzie's Mobs: current physical 1.8.2 equality plus effective deployed `enable_tunneling`;
- Ice And Fire CE: current physical 2.1.2 equality plus deployed `config/iceandfire/iaf-common.json -> tools.phantasmalBladeAbility` for the sole remaining Ghost Sword gate; Dread Lich Staff acquisition is already closed by provider-specific runtime audit `36327488231`;
- Simply Swords: Cataclysm: current physical 1.0.2 equality plus the ten exact STARTUP values needed to classify all four source-pinned abilities;
- Simply Swords: current physical 1.70.2 equality plus bounded Awakening and loot/remnant config evidence; per-stack Awakening/unlock, complete acquisition/reformation, compat materialization and addon ownership remain provider-specific;
- Traveloptics: current physical override/provider blocker — classify the actual installed JAR and discover bounded deployed `traveloptics:blackout` references; exact-current registry/loot/acquisition review remains provider-specific.
- Iron's Spellbooks KubeJS / KubeJS Ars Nouveau: use `kubejs_script_inventory` to bind the review to the exact current script/data tree; inspect non-empty files separately according to each provider checklist.

Somake's exact 1.0.9 registry and current 83/83 registration composition are already closed by canonical provider evidence; the collector is used for deployed config/host/reachability evidence, not to redo that registry. Pair it with [`provider-catalog-runtime-registry-probe.md`](provider-catalog-runtime-registry-probe.md) when exact assembled-server Iron's registry identity and effective host `school` / `enabled` / `allow_crafting` observations are required. For the current physical pack, those runtime rows may close the deployed registration outcome when paired with physical identity/mod-presence evidence; they do not establish a universal predicate contract. The runtime probe is separate QA evidence and still does not prove survival acquisition, provider-owned progression gates, Traveloptics Blackout reachability or Somake↔Traveloptics Aqua authority.