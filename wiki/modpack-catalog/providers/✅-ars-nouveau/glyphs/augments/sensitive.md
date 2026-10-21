# Sensitive

- Registry ID: `ars_nouveau:glyph_sensitive`
- Source class: `AugmentSensitive`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **1** (inherited provider default)
- Default mana: **10**

## Source-pinned behavior

Sets Ars Nouveau's Sensitive spell-stat flag. Compatible glyphs change their targeting/behavior when that flag is present. Exact examples in 5.13.1 include Projectile/Orbit targeting motion-nonblocking materials and Touch targeting fluids/air; other effects may define their own Sensitive behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:scaffolding` + `minecraft:poppy` + `minecraft:water_bucket`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Sensitive is not permission to relax Black Arcana target validation. Black Arcana remains server-authoritative for range, LOS, loaded-state and target-kind geometry even when an Ars integration composes with this glyph.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentSensitive.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentSensitive.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.setSensitive()`; default mana 10; tier default herdado conforme ficha. O flag não é uma permissão genérica de targeting fora do protocolo da Form.
- **Consumidores:** `MethodTouch` aceita alvo em ar/fluidos conforme regras provider; `EffectIgnite` cria `MAGIC_FIRE` em vez de fogo normal quando Sensitive; `EffectFreeze` troca água por `FROSTED_ICE`; `EffectPlaceBlock` usa contagem Sensitive 1/2 para direção de fake player; `EffectRune` armazena `runeTile.isSensitive` para uso de inventário.
- **Perks:** o `setSensitive()` binário e a **contagem** de glyphs são dados distintos; não reproduzir o flag como bypass do `WorldEffectPolicy` do Black Arcana.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
