# Ars Nouveau — Rotate

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_rotate`
- Display name: Rotate
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Amplify, Sensitive, AOE, Pierce, Dampen, Randomize
- Default Sensitive limit: 1
- Default Randomize limit: 1

## Provider-native behavior

Rotate changes entity/block orientation. Amplification adds clockwise rotations; Dampen produces counter-clockwise rotation; Sensitive changes block axis where possible or forces entity look direction; Randomize selects arbitrary rotation. Projectile velocity is rotated alongside projectile orientation. AOE/Pierce expand block coverage.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this orientation/projectile-direction utility. Black Arcana should not duplicate generic rotation control or replay provider projectile movement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectRotate`).

## Engenharia para perks — caminho causal individual

- **Código exato:** [`EffectRotate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRotate.java), Ars 5.13.1.
- **Entidades:** `counterClockwise` quando `(int)ampMultiplier<0`; laço `i<1+abs(ampMod)` gira 90° na direction escolhida ou angle aleatória `world.random.nextFloat()*360`. Sensitive afeta look; sem Sensitive define YRot; se `Projectile`, também altera delta vector por `rotateVec`.
- **Blocos:** `SpellUtil.calcAOEBlocks` gera candidatos; Randomize altera `AXIS` ou `FACING` quando propriedades existem e faz `state.rotate(...Rotation.getRandom)`; no determinístico aplica `1+abs(ampMod)` passos clockwise, mas quando counterClockwise o limite do loop é apenas `abs(ampMod)` (sem +1). Sensitive muda AXIS/FACING com switches especiais.
- **QA de matemática e claims:** `rotateVec` passa o parâmetro chamado `angle` diretamente a `Math.cos/Math.sin`, enquanto callsites geram ângulos 90/−90 ou valores 0..360. Como `Math.cos/sin` esperam radianos, isso é possível divergência de direção estática; exige teste físico para verificar comportamento real. `world.setBlockAndUpdate` por candidato não exibe claim gate local. Nenhuma correction ou exploit declarada.
- **Estado:** ✅ assinatura/source; ⚠️ integração de plugins proteção, configs e gameplay pending; ⛔ nenhum adapter RPG testado nem permissão para duplicar a cadeia causal/perk/mastery.
