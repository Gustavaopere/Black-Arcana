# Dampen

- Registry ID: `ars_nouveau:glyph_dampen`
- Source class: `AugmentDampen`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **0**

## Source-pinned behavior

Adds **-1.0** amplification. Compatible glyphs interpret that lower-power state. Pantomime separately uses Dampen as a target-distance reduction and caps it to one instance for that Form.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:nether_brick`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns the interpretation and compatible-glyph surface. Zero default mana is a provider source default, not permission for Black Arcana to treat reduced-power magic as globally cost-free.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentDampen.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDampen.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.addAmplification(-1.0)`, custo default 0, tier II.
- **Diferença por consumidor:** `MethodPantomime.findPosition` examina a **presença/contagem** de Dampen e fixa `offset=-1` (max default 1), enquanto `EffectExplosion` subtrai `0.5*count(Dampen)` da intensidade; outros consumidores leem `getAmpMultiplier()`.
- **Perks:** custo zero da parte não significa cast total grátis. Um buff global de spell damage não reproduz corretamente a semântica de Dampen e seus efeitos por consumidor.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
