# Ars Nouveau — Perks / Threads

State: `20/20 SOURCE-PINNED / INDIVIDUAL PAGES COMPLETE / SLOT-PROVIDER MATRIX AUDIT IN PROGRESS / RUNTIME QA PENDING`

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

A registry de produção 5.13.1 registra exatamente 20 perks. O catálogo segue exclusivamente essa registry; classes auxiliares presentes na pasta de source não viram perks ativos por associação nominal.

## Contrato provider-native

- `PerkSlot.ONE`, `TWO` e `THREE` possuem valores 1, 2 e 3.
- `IPerk.minimumSlot()` é ONE por padrão; perks podem exigir slot maior.
- `validForSlot` rejeita a aplicação quando o valor mínimo do perk excede o valor do slot.
- `PerkRegistry` separa a registry de perks dos providers tiered de slots por item de armadura.
- Fórmulas de perk recebem `slotValue` quando aplicável; isso não é automaticamente igual à quantidade total do perk equipada.
- Event-driven perks são despachados pelo `PerkEvents` do Ars e continuam dentro da causalidade provider-native.

## Aquisição-base

`ars_nouveau:blank_thread` é craftado em shaped crafting com padrão `xxx / yyy / xxx`, onde `x = ars_nouveau:magebloom_fiber` e `y = c:nuggets/gold`.

Os Threads especializados aqui confirmados usam Blank Thread como reagent no Enchanting Apparatus e, nas receitas 5.13.1 auditadas, possuem `sourceCost: 0`. Ingredientes ficam registrados individualmente em cada ficha.

## Registry — 20/20

1. [Blank / Empty](blank-thread.md) — `ars_nouveau:blank_thread`
2. [The Starbuncle](starbuncle.md) — `ars_nouveau:thread_starbuncle`
3. [High Step](high-step.md) — `ars_nouveau:thread_high_step`
4. [Immolation](immolation.md) — `ars_nouveau:thread_immolation`
5. [Depths](depths.md) — `ars_nouveau:thread_depths`
6. [Feather](feather.md) — `ars_nouveau:thread_feather`
7. [Gliding](gliding.md) — `ars_nouveau:thread_gliding`
8. [Heights](heights.md) — `ars_nouveau:thread_heights`
9. [The Drygmy / Looting](drygmy.md) — `ars_nouveau:thread_drygmy`
10. [Magic Capacity](magic-capacity.md) — `ars_nouveau:thread_magic_capacity`
11. [Warding](warding.md) — `ars_nouveau:thread_warding`
12. [The Wixie / Potion Duration](wixie.md) — `ars_nouveau:thread_wixie`
13. [Repairing](repairing.md) — `ars_nouveau:thread_repairing`
14. [The Whirlisprig / Saturation](whirlisprig.md) — `ars_nouveau:thread_whirlisprig`
15. [Spell Power](spell-power.md) — `ars_nouveau:thread_spellpower`
16. [Chilling](chilling.md) — `ars_nouveau:thread_chilling`
17. [Kindling](kindling.md) — `ars_nouveau:thread_kindling`
18. [Undying](undying.md) — `ars_nouveau:thread_undying`
19. [Life Drain](life-drain.md) — `ars_nouveau:thread_life_drain`
20. [The Amethyst Golem / Knockback Resistance](amethyst-golem.md) — `ars_nouveau:thread_amethyst_golem`

## QA / divergências que permanecem explícitas

- Chilling: descrição textual e amplifier executável aparentam divergir; não normalizar sem runtime QA.
- Repairing: `BASE_ARMOR_REPAIR_RATE` é configurável e não recebe número inventado neste catálogo.
- Event ordering com outros mods/perks precisa ser testado no modpack quando houver integração que dependa de morte, potion duration, loot, lifesteal ou damage mitigation.

## Boundary Black Arcana / RPG Skill Tree

Perks/Threads, slot layouts, perk attributes e alteração de spell cost/damage provider-native continuam authority do Ars Nouveau. RPG Skill Tree não deve duplicar um Thread como perk próprio sem um contrato explícito de bridge e deduplicação. Black Arcana não deve inferir spell provenance ou aplicar modificadores Ars por inspeção visual do armor item.
