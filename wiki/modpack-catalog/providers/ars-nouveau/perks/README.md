# Ars Nouveau — Perks / Threads

State: `5/20 SOURCE-PINNED / CATALOG IN PROGRESS / RUNTIME QA PENDING`

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

A registry de produção 5.13.1 registra 20 perks. O catálogo segue exclusivamente essa registry; classes auxiliares presentes na pasta de source não viram perks ativos por associação nominal.

## Contrato provider-native

- `PerkSlot.ONE`, `TWO` e `THREE` possuem valores 1, 2 e 3.
- `IPerk.minimumSlot()` é ONE por padrão; perks podem exigir slot maior.
- `validForSlot` rejeita a aplicação quando o valor mínimo do perk excede o valor do slot.
- `PerkRegistry` separa a registry de perks dos providers tiered de slots por item de armadura.
- Fórmulas de perk recebem `slotValue` quando aplicável; isso não é automaticamente igual à quantidade total do perk equipada.

## Aquisição-base

`ars_nouveau:blank_thread` é craftado em shaped crafting com padrão `xxx / yyy / xxx`, onde `x = ars_nouveau:magebloom_fiber` e `y = c:nuggets/gold`.

Threads especializadas observadas neste catálogo usam o Blank Thread como reagent em receitas provider-native do Enchanting Apparatus. Receita e Source cost são registrados individualmente quando confirmados.

## Registry — 20 entradas

1. [Blank / Empty](blank-thread.md) — `ars_nouveau:blank_thread`
2. [The Starbuncle](starbuncle.md) — `ars_nouveau:thread_starbuncle`
3. [High Step](high-step.md) — `ars_nouveau:thread_high_step`
4. [Immolation](immolation.md) — `ars_nouveau:thread_immolation`
5. [Depths](depths.md) — `ars_nouveau:thread_depths`
6. Feather — pendente
7. Gliding — pendente
8. Jump Height — pendente
9. Looting — pendente
10. Magic Capacity — pendente
11. Magic Resist — pendente
12. Potion Duration — pendente
13. Repairing — pendente
14. Saturation — pendente
15. Spell Damage — pendente
16. Chilling — pendente
17. Ignite — pendente
18. Totem — pendente
19. Vampiric — pendente
20. Knockback Resist — pendente

## Boundary Black Arcana / RPG Skill Tree

Perks/Threads, slot layouts, perk attributes e alteração de spell cost/damage provider-native continuam authority do Ars Nouveau. RPG Skill Tree não deve duplicar um Thread como perk próprio sem um contrato explícito de bridge e deduplicação. Black Arcana não deve inferir spell provenance ou aplicar modificadores Ars por inspeção visual do armor item.
