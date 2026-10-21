# Ars Creo — Ars Nouveau ↔ Create bridge provider

## Engenharia causal dos sistemas — 17/10/2026

**✅ 7/7 sistemas de compatibilidade com dossiês causais source-pinned**: Starbuncle Wheel, Moving Turrets, Source on Contraptions, Moving Portals, Moving Rituals, Potion Jar Fluid Bridge e Create Display Sources. As [sete fichas em `systems/`](systems/) receberam parâmetros que afetam casting, atributos/recursos, temporização, targeting, área, owners, efeitos e limites, quando aplicáveis. [Matriz de engenharia e QA](PERK-CAUSAL-ENGINEERING-MATRIX-5.4.0.md).

**Novas observações de código relevantes para perks:** `ITurretBehavior` cobra Source antes de selecionar MethodProjectile/MethodTouch; `ContraptionCaster` reporta `CasterType.OTHER` e `expendMana` vazio. `PortalBehavior` zera fallDistance após tentativa de teleport, mesmo sem confirmação no método. `RitualBehavior` tem tile mockada e não guarda todo o `tryTick` por `!isClientSide`; interação custom com mão/tablet está comentada. `PotionTank` converte unidades Ars em 2.5 mB, realiza `ceil(mB×0.4)` ao registrar fill/drain e mostra possíveis divergências entre volume reportado e adição à jar; **nenhum bug runtime foi reproduzido**, host pode limitar efeitos.

**Barra global: —%** (piso de última auditoria 1.857 objetos semânticos / 1.855 estritos, denominador aberto). **Barra Ars Creo: 7/7 famílias = 100% de documentação source-causal; 0 glyphs, 0 novos IDs mágicos; ⚠️ QA físico/provider/Survival pendente; ⛔ 0 adapters homologados.** O source oficial é `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2`, não paridade byte-a-byte dos métodos com JAR instalado. Black Arcana preserva seus próprios casting, rituais e WorldEffectPolicy; Ars/Create preservam seus mecanismos externos.

Status: `PHASE 2S / SOURCE-PINNED 5.4.0 CATALOG COMPLETE / RUNTIME+PACK QA PENDING`

## Exact installed identity

- JAR: `ars_creo-1.21.1-5.4.0.jar`
- Mod id: `ars_creo`
- Runtime version: `5.4.0`
- Physical SHA-1: `22a6afd4fbe76354acc9c1ba076c89a94d120d94`
- Physical base providers: Ars Nouveau `5.13.1`, Create `6.0.10`

## Exact source checkpoint

Read-only factual audit is pinned to `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2`, commit message `5.4.0`.

The exact source declares Minecraft 1.21.1 and requires Ars Nouveau `>=5.0.0`, Create `>=6.0.9` and NeoForge `>=21`. The physical pack satisfies those declared ranges, but compatibility with the newer installed Ars/Create builds remains runtime QA.

## Classification

Ars Creo 5.4.0 is a `BRIDGE / COMPAT / INFRASTRUCTURE` provider, not a glyph provider.

Exact own registry:

- 1 block;
- 1 BlockEntityType;
- 1 block item;
- 1 creative tab;
- 2 Create Display Sources;
- 0 Ars Creo glyph/spell-part registries found.

The own block/item/BE is `ars_creo:starbuncle_wheel`.

## Material bridge surface

Seven source-pinned behavior families are cataloged:

1. Starbuncle Wheel kinetic generation;
2. moving Ars Spell Turrets;
3. Ars Source Jars as contraption Source providers;
4. moving Ars Portal Blocks;
5. moving Ars Ritual Blocks;
6. Ars Potion Jar ↔ Create potion-fluid capability;
7. Create Display Sources for Ars turrets and Source Jars.

## Authority

- Create owns contraption state, movement, kinetic/stress, Display Link and fluid transport primitives.
- Ars Nouveau owns spell grammar/resolver, Source, turrets, Portal behavior, Ritual identity/effects and Potion Jar contents.
- Ars Creo owns only the adapter behavior joining those surfaces.
- Black Arcana does not create a second Create↔Ars bridge, second Source ledger, second cast settlement or second ritual/portal execution.

Moving turret casts use Ars `SpellContext`, an Ars fake player and an Ars Creo `ContraptionCaster` whose caster type is `OTHER`; mana expenditure is manually replaced by provider Source settlement. Ownership/Mastery must therefore not be assigned to an arbitrary player by proximity or contraption ownership inference.

## Exact corrections against editorial material

The Notion dossier's eight-block/eight-BE inventory is stale for exact 5.4.0. Names such as `source_motor`, `source_gearbox`, converter/correspondent blocks and related machinery do not appear in the exact registry/tree.

The Starbuncle Wheel runtime does not search for a living Starbuncle. Its exact recipe uses a Starbuncle Charm + Create Water Wheel; runtime speed is config-driven and receives the gold-block positional bonus.

## Provenance warning

Source metadata declares `LGPLv3`, while the exact root `LICENSE` file is the Unlicense/public-domain dedication text. Phase 2S records this as `LICENSE METADATA DIVERGENCE` and does not resolve it by assumption. Source use in this phase remains read-only factual inspection; no upstream code/assets are copied or adapted.

Runtime/config/client/full-pack QA remains pending. Phase 2S does not promote any Black Arcana runtime Stage or adapter.