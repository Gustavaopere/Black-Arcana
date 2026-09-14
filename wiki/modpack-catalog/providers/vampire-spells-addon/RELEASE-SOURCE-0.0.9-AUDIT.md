# Vampire Spells Addon 0.0.9 — release/source audit

## Scope

Phase 2BT audits installed `vampire_spells_addon-neoforge-1.21.1-0.0.9.jar` as a semantic-magic provider candidate. Physical presence/version comes from the current sibling modlist snapshot; semantic evidence comes from the official 0.0.9 release and its exact source target.

## Release identity

Official GitHub release `1.21.1-0.0.9`:

- target commit: `2d36e94e67611a316b7311b11e4574b499025580`;
- NeoForge asset: `vampire_spells_addon-neoforge-1.21.1-0.0.9.jar`;
- asset SHA-256 reported by GitHub: `8997f71035f29e4d2fe9e37dd76ca5f4b574906d1aed0914df6c119111570fed`;
- asset size: 97181 bytes.

The installed filename matches that official asset. No independent current physical-pack digest is preserved in the sibling repository, so byte-for-byte physical equivalence is not asserted. Provenance for the semantic conclusion is therefore **exact-release source-pinned**, consistent with the existing provider README and technical audit.

## Exact source tree

Exact commit tree `7563dad11b8c8e3156217f6f60da070cabe7af69` contains common code under event/integration/mechanics plus platform adapters/mixins. Relevant exact files include:

- `SpellIds.java`;
- `BloodSpellHandler.java`;
- `HolySpellHandler.java`;
- `SpellEventHandler.java`;
- `IronsSpellsBridge.java`;
- `VampirismBridge.java`;
- `BloodMechanics.java`;
- NeoForge `AbstractSpellMixin.java`;
- NeoForge `VampireSpellsAddon.java` entrypoint.

The resource tree contains localization overrides under `src/main/resources/assets/irons_spellbooks/lang` and addon presentation/config resources. No provider-owned spell/ritual datapack tree is present.

## Identity audit

`SpellIds` constructs every magic identifier with namespace `irons_spellbooks`. Exact referenced identities are:

- `ray_of_siphoning`;
- `devour`;
- school `holy`;
- utility spells `angel_wing`, `fortify`, `wisp`, `haste`, `cleanse`, `sunbeam`.

No `vampire_spells_addon:*` spell identity is created there.

## Registration audit

`SpellEventHandler.register()` resolves `IronsSpellsBridge` and `VampirismBridge`, then installs platform listeners. The NeoForge entrypoint registers SERVER config and invokes that integration registration during common setup.

No spell, school, ritual or equivalent provider-owned magical-action registrar is invoked by those exact registration paths.

## Behavioral audit

`BloodSpellHandler` operates on Iron's event spell IDs/schools to:

- replace mana with atomic Vampirism blood payment under configured conditions;
- adjust Blood-school cooldown;
- scale Devour mana pricing;
- restore blood from delivered damage of Ray of Siphoning or Devour.

`HolySpellHandler` operates on Iron's Holy school/identities to modify vampire interaction: utility-cast cancellation/self-damage, Holy damage amplification/reflection and Holy heal inversion/suppression.

NeoForge `AbstractSpellMixin` targets Iron's `io.redspace.ironsspellbooks.api.spells.AbstractSpell`; it changes mana-gate/cancellation behavior for an existing host cast. It does not mint a provider-owned spell identity.

## Semantic conclusion

The exact 0.0.9 release source establishes a compatibility/runtime-policy addon, not an independent spell catalog.

Evidence/provenance: **exact-release `SOURCE-PINNED`**.

Semantic state: **`ZERO_BRIDGE_INFRA`**.

Semantic delta: **+0**.

Iron's-owned spells referenced or behaviorally modified by this addon remain counted under Iron's/provider ownership and must not be duplicated.

## Remaining fail-closed gates

This audit does not prove:

- installed physical-JAR digest equality to the official asset;
- assembled-pack reflective contract resolution;
- mixin/event ordering;
- effective serverconfig;
- live blood/mana/damage/cooldown behavior;
- compatibility with other installed bridges;
- any Black Arcana adapter/runtime behavior.
