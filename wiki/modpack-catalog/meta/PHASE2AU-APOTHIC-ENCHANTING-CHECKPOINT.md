# Phase 2AU — Apothic Enchanting 1.6.2 checkpoint

## Scope

Phase 2AU audits `apothic_enchanting` 1.6.2 against the current physical modpack, exact publisher release and exact official 1.6.2 source commit. This is catalog/deduplication work only; no Black Arcana runtime implementation is added.

## Canonical base

- initial Phase 2AU branch base: `main@3c9795820f48cbe01a28ed1d4c3f1238cce816a0`
- latest reconciled `main`: `78639998c212e91469e9036484bd5ac2ac9b699b`
- intervening PRs #157 and #159 are Stage 05 keyboard-focus work with zero catalog coverage delta; none of their changed files overlaps this Phase 2AU catalog tranche
- canonical component count on the reconciled base: **48/100 = 48%**
- Phase 2AT / PR #156 is canonical as component #48 (`apothic_spawners` 1.4.0)

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: `21.1.248`
- physical modlist: 595 top-level entries
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- physical artifact: `ApothicEnchanting-1.21.1-1.6.2.jar`
- mod ID: `apothic_enchanting`
- physical version: `1.6.2`
- physical SHA-1: `2623af251d3ddeae1d8e710afa76afe753834bab`
- physical required-provider versions relevant to exact source metadata: Placebo 9.9.2 and Apothic Attributes 2.10.1

## Publisher/source evidence

- CurseForge project/file: `1063926 / 8797650`, uploaded 2026-09-03 for NeoForge Minecraft 1.21.1.
- Official repository: `Shadows-of-Fire/Apothic-Enchanting`.
- Exact release commit: `00fbcf00a2f42701645daf8906e54f67ec65a5dc`, message `1.6.2`, dated 2026-09-03.
- Exact release tree: `cad9b01b8d366e770cb811552884848afb320b30`.
- Exact Java subtree: `7f20d16f0d3f0c49caa1c5ae4582f88b22e8bd42`, recursive tree `truncated=false`.
- Exact generated metadata requires Minecraft 1.21.1+, NeoForge 21.1.187+, Placebo 9.9.0+ and Apothic Attributes 2.4.0+.
- Source root code license: MIT; source `LICENSE_ASSETS`: All Rights Reserved; current CurseForge project surface: All Rights Reserved.

Satisfying declared dependency ranges is not promoted to proof of full-modpack interoperability.

## Semantic closure

Exact 1.6.2 source closes:

- no standalone provider spell/glyph/ritual registration surface;
- no provider mana/cast resource;
- Eterna, Quanta and Arcana as enchanting-table statistics, plus clues, blacklist, treasure and stability;
- one synced `apothic_enchanting:max_eterna` attribute, default 100 and range 0..100;
- 20 provider enchantment registry keys;
- `EnchantmentStatBlock` and `EnchantableItem` extension interfaces;
- data-backed `EnchantingStatRegistry` for block statistics;
- IMC hard-cap method `set_ench_hard_cap`;
- infusion and keep-NBT infusion recipe serializers;
- persistent Raven-table Eterna/Quanta/Arcana attachment;
- four PLAY payloads: 3 clientbound synchronization payloads + 1 serverbound Raven-table stats payload;
- exactly 17 common + 3 client mixins.

The serverbound Raven payload is server-validated/clamped and is not a spell-cast path.

## Enchantability version boundary

The exact changelog places the Enchantability redesign in **1.6.1**, not 1.6.2. Version 1.6.2 itself fixes star-prefixed enchantment level display and adds JEI transfer for Raven-table infusion recipes.

Exact 1.6.2 source also exposes a comparison in `ApothEnchantmentHelper` whose observed condition (`rand.nextFloat() >= chance`) is not silently equated with the changelog's percentage-chance wording. Source/JAR equality and physical runtime reproduction are unproven, so that discrepancy remains explicit QA/fail-closed evidence rather than an asserted runtime bug.

## Authority / deduplication result

Apothic Enchanting owns enchanting-system semantics, not Black Arcana casting. Black Arcana therefore does not:

- create spell identities for the provider's enchantments;
- reinterpret provider `Arcana` as Black Arcana authority or resource state;
- implement a second Eterna/Quanta/Arcana roll engine;
- mirror Raven-table persistent state;
- resend or bypass provider table state without the provider's validation path;
- duplicate provider enchantment proc/effect settlement;
- directly rewrite provider enchantment caps/rolls from generic RPG perks;
- use mixin/internal classes as an assumed stable integration API.

If a future BA feature genuinely needs enchanting interoperability, provider-native seams (`EnchantmentStatBlock`, `EnchantableItem`, documented/observed IMC/data surfaces, and vanilla/NeoForge registry contracts) are preferred, with exact-version verification.

## License / clean-room boundary

Black Arcana uses the source only for read-only factual interoperability/deduplication analysis. No provider code, assets, translations, models, sounds or implementation text are copied.

License evidence is kept layered:

- root source code: MIT;
- generated metadata: `MIT License`;
- source assets: All Rights Reserved;
- current CurseForge project surface: All Rights Reserved.

No broad reuse right is inferred from the MIT code license for separately restricted assets or publisher-hosted material.

## Remaining QA

Fail-closed:

- byte-for-byte source↔physical-JAR reproducibility;
- direct physical-vs-publisher-file hash equality;
- complete-modpack reload/event ordering;
- physical runtime reproduction of Enchantability behavior;
- compatibility of all provider mixins with the installed modpack;
- optional JEI/Jade/Curios behavior in the physical pack;
- stability of non-public/non-`api` implementation classes for future adapters.

## Coverage decision

The provider is eligible to become component **#49** because current physical identity plus exact 1.6.2 source close the provider-owned semantic surfaces relevant to Black Arcana deduplication, including the explicit result that its enchanting systems are not a second Black Arcana spell/casting authority.

Until exact-head CI GREEN, final latest-main gate, merge and post-merge `main` confirmation, canonical coverage remains **48/100 = 48%** and Phase 2AU represents **49/100 = 49%** only as a candidate.

Phase 3 remains blocked.
