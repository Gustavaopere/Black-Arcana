# Projectile

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_projectile`
- Source class: `MethodProjectile`

## Source-pinned behavior

Projectile creates a spell projectile and resolves the following spell effects when that projectile reaches a target or block. Its default mana cost in the 5.13.1 source is **10**; the effective casting cost remains configuration-owned by Ars Nouveau.

The projectile count is increased by Split. Its launch velocity is derived from the spell acceleration multiplier, and the provider exposes a configurable maximum projectile lifespan with a default of **60 seconds**.

## Compatible augments

The exact source permits:

- `ars_nouveau:glyph_pierce` — additional piercing through targets/blocks;
- `ars_nouveau:glyph_split` — creates additional projectiles;
- `ars_nouveau:glyph_accelerate` — raises projectile velocity;
- `ars_nouveau:glyph_decelerate` — lowers projectile velocity;
- `ars_nouveau:glyph_sensitive` — allows collision with plants/materials that normally do not block motion.

`MethodProjectile` explicitly marks itself as a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:fletching_table` + `minecraft:arrow`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, the player is treated as already knowing Projectile without consuming a Glyph item.
- The generated recipe still exists; the Ars Glyph-use path rejects learning while the part is currently considered a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Ars Nouveau owns this projectile cast method, projectile entity lifecycle, provider mana/config values and glyph compatibility. Black Arcana must not replace it with a second Ars projectile pipeline. A Black Arcana projectile spell may exist only as Black Arcana-owned content entering the canonical Black Arcana cast pipeline, with its own bounded targeting/effect contracts and a material forbidden-domain distinction.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

This page records source facts, not proof that the installed 612-mod pack preserves every default config value.

## Localizadores e parâmetros para Codex — fonte exata

- **Java:** [`MethodProjectile.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java) no commit `112920ff774831f204031da75b4c4e73d3765157` correspondente ao catálogo Ars 5.13.1.
- **Método resolutor:** `MethodProjectile.onCast` → `summonProjectiles` → entidades `EntityProjectileSpell`, que resolvem **efeitos de glyph posteriores** quando colidem.
- **Quantidade no disparo pela entidade:** `numSplits = 1 + spellStats.getBuffCount(AugmentSplit.INSTANCE)`; velocity `max(0.1, 0.75 + spellStats.getAccMultiplier()/2)`; ângulos de yaw variam em passos alternados de 10°.
- **Diferença importante para perks:** o overload de lançamento em bloco também usa `AugmentSplit`, mas possui posicionamento/velocidade próprios. Qualquer perk de split/velocidade deve preservar origem e resolver do feitiço, não injetar cast extra após o impacto.
- **Lifespan default:** `getProjectileLifespan` busca `PROJECTILE_TTL` configurável (fallback 60 segundos); não é um alcance máximo por blocos.
- **Limites:** `getCompatibleAugments` permite Pierce, Split, Accelerate, Decelerate e Sensitive. Quantidade/velocidade são dados do `SpellStats` provider-native; nenhuma API de reescrita por RPG perk foi comprovada.

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
