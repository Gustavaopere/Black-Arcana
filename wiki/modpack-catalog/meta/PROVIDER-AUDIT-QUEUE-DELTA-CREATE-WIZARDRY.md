# Provider Audit Queue Delta — Create: Wizardry 1.21.1-0.5.1-pre1

Date: `2026-09-23`

This narrow overlay applies to `create_wizardry` until the current physical magic-provider queue is regenerated from the sibling's newest physical modlist.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `create_wizardry` | `create_wizardry-1.21.1-0.5.1-pre1.jar` / runtime `1.21.1-0.5.1-pre1` / physical order #166 | ✅ `SOURCE-PINNED CURRENT COMPONENT / CREATE↔IRON'S MAGIC AUTOMATION / ZERO PROVIDER-OWNED SPELL IDENTITIES / ZERO_SEMANTIC_HOST_SPELL_AUTOMATION / +0 / ASSEMBLED-PACK RUNTIME QA FAIL-CLOSED` |

## Evidence

Physical authority:

- sibling `neoforge-rpg-skilltree@4767f5c637c02c6d91ccb43a86ea1539f42a2e9b`;
- certified physical row #166;
- JAR `create_wizardry-1.21.1-0.5.1-pre1.jar`;
- mod id `create_wizardry`;
- runtime `1.21.1-0.5.1-pre1`.

Source pin:

`TTZPlayz/Create-Wizardry@9c4e53aad0ee9477187487443b597b77ef06f323`

The source commit and project metadata both identify the installed version line. Source-to-physical byte equality is not claimed because the current sibling dossier does not preserve an independent installed-JAR hash for this row.

## Closed by source evidence

- provider does not register a provider-owned spell registry;
- 0 provider spell resource paths found;
- 0 `registerSpell`, `SpellRegistry`, `DeferredRegister<AbstractSpell>`, `Registries.SPELL`, `SPELLS.register` or `spell.create_wizardry` identity surfaces found;
- Blaze Caster consumes Iron's `SpellData` / `AbstractSpell` and invokes existing host spells;
- 31 explicit Blaze Caster blacklist entries are host spell path names, not provider-owned registrations;
- Mana Siphon and Depletion alter host mana/casting conditions without minting spell identities;
- semantic classification: `ZERO_SEMANTIC_HOST_SPELL_AUTOMATION`;
- semantic delta: **+0**.

## Still fail-closed

- installed-JAR ↔ source-build byte equality;
- deployed config;
- current Create/Iron's assembled-host compatibility;
- addon-spell automation parity;
- exactly-once mana/cooldown/effect settlement;
- projectile/summon/caster ownership;
- multiplayer/protection;
- Mana Siphon and fluid settlement;
- reload/restart/persistence.

## Global accounting consequence

Create: Wizardry closes another current physical magic-relevant component discovered during the rebase of the sibling modlist, but adds **0** independent semantic spell identities.

The strict semantic minimum is unchanged by this provider. The technical provider denominator remains `PENDING REBASE`; no new technical fraction or percentage is inferred from the stale historical denominator.
