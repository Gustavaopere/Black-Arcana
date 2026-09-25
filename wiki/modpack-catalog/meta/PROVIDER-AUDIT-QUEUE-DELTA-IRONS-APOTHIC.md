# Provider Audit Queue Delta — Iron's Apothic 2.2.2

Date: `2026-09-24`

This overlay applies to `irons_apothic` until the full current physical magic-provider queue is regenerated from the sibling's latest recertified modlist.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `irons_apothic` | `irons_apothic-2.2.2.jar` / runtime `2.2.2` / certified index row #339 | ✅ `CATALOGED / EXACT SOURCE-PINNED 2.2.2 / 7 CUSTOM AFFIX CODECS / 140 AFFIX DEFINITIONS / 48 SPELL-TRIGGER OR IMBUED AFFIX DEFINITIONS / 24 GEMS / ZERO PROVIDER-OWNED SPELL REGISTRATIONS / +0 STRICT SPELL-SEMANTIC / ASSEMBLED-PACK RUNTIME QA FAIL-CLOSED` |

## Physical evidence

Sibling authority:

`neoforge-rpg-skilltree@c3de5878d69a7a6b4441606ef2b9e96a61a8f2e9`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Magic/✅-irons-apothic v2.2.2.md`

The current index records row #339 as:

`Apotheosis x Iron's Spellbooks Compat / irons_apothic-2.2.2.jar / 2.2.2`.

No independent physical digest is preserved in the certified dossier used here, so exact byte equality is not claimed.

## Source evidence

Official source pin:

`muon-rw/Apotheosis-Irons-Spells@c5d501219cc9bbbfb8c69acc08bebac76983d1c1`

The commit declares `mod_version=2.2.2` and exposes the complete source/resource tree used for this catalog audit.

## Closed by current evidence

- physical presence, mod id and version;
- exact release-correlated 2.2.2 source identity;
- 7 custom affix codec registrations;
- 140 provider affix JSON definitions;
- exact 48-entry spell/imbued spell affix subset;
- 24 gem resource definitions;
- 25 school-family resource groups;
- external spell ownership through Iron's `SpellRegistry`;
- exact source use of Iron's server-side cast pipeline;
- no independent provider spell registry in the exact source tree;
- strict semantic spell contribution fixed at +0.

## Runtime gates remain fail-closed

- physical binary ↔ source byte equality;
- current assembled datapack/resource overrides;
- numerical affix/gem values;
- current optional-school resolution;
- recursive proc behavior with every installed addon;
- target/cooldown exactly-once behavior;
- Curios/equipment lifecycle;
- FakePlayer/automation behavior;
- multiplayer/relog/restart persistence;
- Iron's 3.16.3 + Apotheosis 8.8.0 runtime regression.

## Semantic accounting

Iron's Apothic is a magic bridge/support provider, not an owner of independent spells.

Strict semantic spell delta: **+0**.

The existing strict semantic minimum therefore does **not** increase from this catalog closure. The technical provider denominator remains `PENDING REBASE` because the sibling physical set contains additional magic/cross-domain components beyond the historical 100.
