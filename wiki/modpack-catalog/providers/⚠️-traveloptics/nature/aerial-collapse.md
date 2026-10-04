# `traveloptics:aerial_collapse`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Nature**
- Registry: `traveloptics:aerial_collapse`
- Registry field: `AERIAL_COLLAPSE_SPELL`
- Concrete class: `AerialCollapseSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

lift then slam; health-percentage damage.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Publisher quantitative / conditional note — version-conditioned

Lift timing: **2.5 seconds** before the slam. The same current page describes the slam as percentage-health damage that ignores damage caps.

This is **publisher-only context**, not exact-alpha/current-physical proof. The corresponding runtime value or rule remains unverified for File `6342780` and SHA-1 `7b74816e...` unless independently proven.

## Reachability

`HOST-DEFAULT CRAFTABLE / CONFIG+LEARNING CONDITIONAL`: exact File `6342780` class has no direct `DefaultConfig.setAllowCrafting(...)`; current Iron's `1.21.1-3.16.3` host defaults craftability to `true`. Effective spell config and `canBeCraftedBy(player)` learning gates remain authoritative. This closes default Scroll Forge eligibility only, not unconditional survival acquisition.

## Evidence boundary

Identity + school are cataloged from the exact-version audit. Mana, cooldown, cast time, levels, rarity, formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.
