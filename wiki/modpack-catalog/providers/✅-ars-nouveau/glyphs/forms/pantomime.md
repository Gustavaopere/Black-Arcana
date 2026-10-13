# Pantomime

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_pantomime`
- Source class: `MethodPantomime`

## Source-pinned behavior

Pantomime resolves the following spell effects at a provider-computed block position in the caster's line of sight rather than requiring a normal clicked target. Its base distance is derived from the caster's view pitch and then modified by Amplify/Dampen.

The exact source uses a default mana cost of **5**. Dampen is explicitly limited to one instance by this Form's default augment-limit table. Provider configuration remains authoritative for effective casting cost and other configurable spell-part data.

## Compatible augments

The exact source permits:

- `ars_nouveau:glyph_amplify` — increases target distance;
- `ars_nouveau:glyph_dampen` — reduces target distance, default limit 1 on this Form;
- `ars_nouveau:glyph_sensitive` — highlights the selected block through provider presentation behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `#c:glass_blocks` ×8.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned: using the crafted Glyph server-side records it in Ars player data and consumes the Glyph in survival. Runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Pantomime is an Ars-owned line-of-sight targeting form. Its existence is a strong deduplication signal against generic "cast at a nearby looked-at block" content. Black Arcana targeting remains server-owned under D006/D019 and must not trust an Ars/client-computed position as authoritative for Black Arcana world effects.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`MethodPantomime.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodPantomime.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Seleção de posição:** `MethodPantomime.findPosition(shooter,stats)` usa `offset = count(Dampen)>0 ? -1 : count(Amplify)`. A distância é `viewXRot < 45.0 ? 2+offset : 3+offset` blocos ao longo de `getViewVector(1.0f)`, a partir da posição dos olhos. O alvo final é `BlockHitResult` na posição calculada; **não** se trata de raycast comum com colisão/LOS comprovado pela classe.
- **Overloads:** `onCast`, `onCastOnBlock`, `onCastOnEntity` chamam todos `getTarget`, que resolve os efeitos subsequentes via `resolver.onResolveEffect` e produz partículas/som. Uma EntityHit externa não é passada como alvo direto.
- **Augments e controle:** Amplify, Dampen, Sensitive, Dampen max 1 por default. Dampen prevalece sobre Amplify no ternário quando ambos presentes; Sensitive fornece apresentação de highlight, não aumenta distância nessa fórmula. Mana declarada 5, config efetiva Ars.
- **Perk segura:** distinguir potência/alcance do glyph e modificação externa de `SpellStats`; range baixo ou negativo por combinações fora do default requer análise de admissão. Hook externo não verificado.
- **Mutação externa:** ⛔ nenhum hook de escrita de `SpellStats` por RPG Skill Tree comprovado; a presença do método Java **não** valida bridge. Source auditado; config real, testes físicos/Survival e integração continuam ⚠️ condicionados.
