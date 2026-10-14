# Reliquified Iron's Spells 'n Spellbooks 0.2.7 — exact-JAR audit gate

**Opened 2026-10-14 · status 🟡 implementation of read-only binary audit / ⚠️ exact artifact result PENDING.** Black Arcana baseline `main@b7af4777cd3040de8770f46e92cdd80e36f1cd9e`; sibling modlist `main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`. No new spells, no runtime Java and no Stage promotion.

## Provenance

- Installed item #478: `reliquified_irons_spells_and_spellbooks-1.21.1-0.2.7.jar`, mod ID `reliquified_irons_spells_and_spellbooks`, source of installed **SHA-1 `e22fd94c87cb88b3cfa4637c48a1058260d35a9b`**.
- Publisher [CurseForge file 8221834](https://www.curseforge.com/minecraft/mc-mods/reliquified-irons-spells-n-spellbooks/files/8221834): NeoForge 1.21.1, 0.2.7 Beta, uploaded 2026-06-09. The CDN is only a *candidate* until CI verifies SHA-1 equality.
- Source `Octo-Studios/reliquified-irons-spells-n-spellbooks@1dfa5557ae3ae59c793682bd8e386f81d7feaa32` declares version 0.2.7. `init/RISASItems.java` lists **24** deferred item registrations, of which `HatOfOmniscienceItem` has no `AbilityTemplate.builder`; the remaining 23 item classes have **25** primary ability roots, with two each in `SlicerItem` and `ShadowClawsItem`. Counts source-derived; not yet physically certified.
- Source license All Rights Reserved. Read-only classfile inspection is for identity/evidence; no publisher code/assets/decompiled disassembly is redistributed.

## Exact binary assertion

In the proposed audit workflow `.github/workflows/reliquified-irons-027-binary-audit.yml`, first fetch publisher file `8221834`, verify its SHA-1 against sibling physical metadata and NeoForge mod ID, then read only `RISASItems.class` and 24 registered item classes using `javap -c -p` under Java 21.

The independent collector `docs/qa/reliquified_irons_binary_audit.py` checks:

1. Precisely 24 item `DeferredRegister.register(String,Supplier)` callsites: `ITEMS` load → literal ID → supplier invokedynamic → register → `putstatic` field. Registry fields and IDs must match the audited release source, without duplicates/extras.
2. `AbilityTemplate.builder(String)` calls on the registered items produce precisely **25 unique, provider-owned primary IDs** across **23** classes. `HatOfOmniscienceItem` contributes zero ability roots; `SlicerItem` and `ShadowClawsItem` contribute two each.
3. Missing class, altered ID, ability mismatch, file hash mismatch, duplicated ZIP entry, invalid NeoForge metadata or unavailable javap **fails closed**. The tests generate **synthetic Java 21 fixtures**, never third-party gameplay.
4. The JSON report includes SHA-1, SHA-256, file byte size, audited counts, limited deviations and explicit unproven-runtime list. Only the small JSON may be uploaded as workflow artifact.

**Until an actual run ends in PASS, this document does not promote the provider to `COUNTED_EXACT`.** Current frozen campaign after PR #809: 26/39 exact, 13/39 pending. Reliquified Iron's is one of the pending 13. No global semantic count change: 25 already source-counted roots; strict minimum 1857 global / 1855 scoped.

## Runtime blockers

⚠️ Test full installed stack Relics 0.12.8, Iron's 3.16.3 and the provider 0.2.7 together in dedicated/client Survival. Loot entry to actual chest, item equip/unequip, relic rank/XP, mana/cooldown and duplicated execution, research icon, death/logout/restart, multiplayer/claims still untested. An exact binary registry, when achieved, certifies only compiled callsites, not real gameplay.

⛔ No real RPG Skill Tree Mastery/perks hook has been homologated. Black Arcana does not add its own Relics ability mana/XP pipeline, and Stage 06.05 remains unpromoted.
