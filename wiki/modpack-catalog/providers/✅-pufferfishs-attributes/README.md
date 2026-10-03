# Pufferfish's Attributes — 0.8.3

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 42 ATTRIBUTE IDS / ZERO_SEMANTIC_ATTRIBUTE_FRAMEWORK / +0 STRICT / RUNTIME-CONSUMER QA SEPARATE`

## Current physical identity

Sibling physical authority: current `neoforge-rpg-skilltree` dossier for row **#463**.

- JAR: `puffish_attributes-0.8.3-1.21-neoforge.jar`;
- mod id: `puffish_attributes`;
- runtime: `0.8.3`;
- Minecraft / loader: NeoForge 1.21/1.21.1;
- physical SHA-1: `9e6a87f790fc9281ea2685f8d4f6435d0d7c6d1f`.

Pufferfish's Attributes owns a dynamic-attribute framework used by RPG systems. Attribute names such as Magic Damage, Magic Resistance or Stamina describe numeric/stat surfaces; they are not player-selected spells or supernatural action identities.

## Exact artifact closure

NON-MERGE evidence PR **#546** audits the exact current publisher artifact.

- exact-artifact run: `37137133861` — **SUCCESS**;
- evidence artifact: `11278014339`;
- evidence digest: `sha256:a0c3a257f169e2fea76ebf3f8b40643df650aa6f43bfeec638724c824ff13e99`;
- CurseForge project/file: `991341 / 8610466`;
- publisher SHA-1: `9e6a87f790fc9281ea2685f8d4f6435d0d7c6d1f`;
- publisher SHA-256: `b21c165e033360e112eb2c3426437e1ba4ebf70f971535b72b1b1891d04c87f0`;
- bytes: `235,542`.

The publisher SHA-1 exactly equals the physical pack SHA-1.

See [`EXACT-0.8.3-ARTIFACT-AUDIT.md`](EXACT-0.8.3-ARTIFACT-AUDIT.md).

## Exact attribute denominator

The exact artifact closes **42 localized/registered attribute identities**. They cover damage/resistance/shred, stamina/mobility, action speeds, healing/life-steal, fortune/experience, stealth and weapon-specific stats.

Detailed inventory: [`ATTRIBUTE-INVENTORY-0.8.3.md`](ATTRIBUTE-INVENTORY-0.8.3.md).

## Semantic result

The exact JAR contains **71 archive entries / 32 classes / 39 resources / 4 provider data paths**. Its semantic-path scan produced one lexical hit only: `HungerManagerMixin`, because the bounded regex matched the substring `mana` inside `Manager`; it is not a mana system.

The four provider data paths are attribute-tag infrastructure. The artifact exposes no provider-owned spell/ritual/glyph/rite/mana/arcane/summon/teleport action roster.

`magic_damage` and `magic_resistance` are numeric attributes. A consumer may use them when computing external spell damage or resistance, but that does not make the attribute itself a spell.

Therefore Pufferfish's Attributes contributes **`+0 ZERO_SEMANTIC_ATTRIBUTE_FRAMEWORK`**.

## Authority boundary

Pufferfish's Attributes remains authority for its attribute registries, dynamic-base semantics, modifiers and event integration. Concrete equipment, skill, spell or effect providers that apply these attributes remain owners of their own player-facing actions.

Black Arcana must not count an external spell twice merely because its numerical damage/resistance is modified through Pufferfish's Attributes.

## Runtime QA remains separate

Current-pack consumers, modifier stacking, dynamic-base behavior, stamina integration, shred ordering, life-steal loops and client/server synchronization remain runtime/compatibility QA. They do not reopen the provider-owned semantic denominator.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_ATTRIBUTE_FRAMEWORK`.**

Strict semantic delta: **+0**.
