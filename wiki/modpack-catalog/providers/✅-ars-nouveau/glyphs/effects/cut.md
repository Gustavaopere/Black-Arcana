# Ars Nouveau — Cut

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_cut`
- Display name: Cut
- School: Manipulation
- Default tier: 1
- Default mana cost: 0
- Compatible augments: Extract, Fortune, Amplify, Dampen
- Default Amplify limit: 2
- Source default base damage: 1
- Source default Amplify scalar: +1 damage

## Provider-native behavior

Cut simulates shears on shearable entities/blocks. Against non-shearable entities it deals small spell damage. Amplify changes block interaction to an axe-like strip/use path; Extract/Fortune apply tool enchantment semantics where supported. The source includes explicit duplicate-prevention checks around item-handler/container block entities before fake-player tool interaction.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:shears` + `minecraft:iron_sword`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this magical shearing/stripping utility. Black Arcana should not add a generic duplicate zero-cost cutting/shearing spell or double-spawn shear drops.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCut`).

## Engenharia de perks — evidência de execução individual

- **Classe versionada:** [`EffectCut.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCut.java) no Ars Nouveau 5.13.1.
- **Alvo vivo:** se é `IShearable`, usa `isShearable/onSheared` com shears e lança os itens retornados; demais entidades recebem `IDamageEffect.attemptDamage` com dano `DAMAGE.get()+AMP_VALUE.get()*getAmpMultiplier()`, defaults 1.0 e 1.0.
- **Blocos:** usa `SpellUtil.calcAOEBlocks` mas `getCompatibleAugments` inclui somente Extract, Fortune, Amplify e Dampen; Amplify count >0 aciona `doStrip` (diamond axe), senão `doShear` (shears). `dupeCheck` recusa block entities com capability `ItemHandler.BLOCK` ou `Container` para interação por fake player. **Aviso de fonte:** há comentários TODO sobre Fortune em shear; não afirmar bônus concluído em todas as superfícies.
- **Perks:** dano e extração não são mesmo resultado; nenhuma dupla geração de drops por callback externo.
- **Status:** ✅ code pin/identidade; ⚠️ downstream, config e Survival pendentes; mutação por RPG perk só pode ocorrer via [eventos reais](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e adapter validado, não por inferência temática.
