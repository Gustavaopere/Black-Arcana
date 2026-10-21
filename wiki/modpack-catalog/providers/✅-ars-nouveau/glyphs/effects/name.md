# Ars Nouveau — Name

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_name`
- Display name: Name
- School: Manipulation
- Default tier: 2
- Default mana cost: 25
- Compatible augments: none

## Provider-native behavior

Name derives a new name first from an available Name Tag through the Ars inventory manager, otherwise from the held caster tool's configured spell name. It can rename entities, held off-hand items, dropped item stacks, skull ownership text and nameable container blocks. Named mobs are marked persistent.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:name_tag`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this naming/persistence utility. Black Arcana should not duplicate generic remote naming or silently manipulate Ars-associated persistence through a second effect path.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectName`).

## Engenharia para perks — caminho causal individual

- **Código exato:** [`EffectName.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectName.java), Ars 5.13.1.
- **Escolha do nome:** `getName` procura primeiro `Items.NAME_TAG` via `InventoryManager.findItem(...InteractType.EXTRACT)` e lê `getDisplayName().plainCopy()`; caso contrário tenta nome configurado no caster tool `SpellCasterRegistry.from(stack).getSpellName()`. A classe **não** decrementar Name Tag nesse path, apenas consulta a stack.
- **Entidades/inventário:** `onResolveEntity` pode alterar `Entity.setCustomName` e `Mob.setPersistenceRequired`, ou `ItemEntity` `DataComponents.CUSTOM_NAME`; se caster tem offhand não vazia, atualiza seu componente de nome também. No caso self com offhand, o nome da própria entidade não é alterado.
- **Blocos:** `SkullBlockEntity` recebe `ResolvableProfile` novo; `BaseContainerBlockEntity` recebe `name` e `setChanged`; outros blocos podem disparar rename de entidades em AABB `inflate(0.08)`. Sem augments, custo default 25. **Perks:** nome e persistência são estado de mundo e não novos casts/drops; não criar acesso ou persistência universal em entidades protegidas.
- **Estado:** ✅ assinatura/source; ⚠️ integração de plugins proteção, configs e gameplay pending; ⛔ nenhum adapter RPG testado nem permissão para duplicar a cadeia causal/perk/mastery.
