# Asterism Arcanum

## Estado canônico

- mod id: `asterismarcanum`
- JAR instalado: `asterismarcanum-1.21.1-0.1.0.jar`
- versão: `1.21.1-0.1.0`
- Minecraft: 1.21.1
- loader: NeoForge
- source pin exato: `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583` (`wrapping up!`, 2026-05-28)
- source dependency: Iron's Spells `1.21.1-3.15.6`
- pack dependency atual: Iron's Spells `1.21.1-3.16.3`
- estado: **SOURCE-PINNED 0.1.0 / REGISTRY 11 / SURVIVAL 10/10 CATALOGADO / RUNTIME QA PENDENTE**

Asterism Arcanum é um addon de Iron's Spells que introduz a escola própria **Astral** e um ecossistema de Astromancer, Lunar Moths, Dragonflies, equipamento Astral, Astrolabe Spellbook e Celestial Staff.

## Inventário de spells

O registry 0.1.0 contém 11 registrations. O catálogo survival contém 10 spells, exatamente os apresentados como utilizáveis na release:

| Spell | ID | Rarity | Níveis | Estado |
|---|---|---:|---:|---|
| Astral Echo | `asterismarcanum:astral_echo` | Rare | 1–8 | survival |
| Brightburst | `asterismarcanum:brightburst` | Rare | 1–6 | survival |
| Celestial Tether | `asterismarcanum:celestial_tether` | Uncommon | 1–8 | survival |
| Luminous Beam | `asterismarcanum:luminous_beam` | Common | 1–10 | survival |
| Piercing Light | `asterismarcanum:piercing_light` | Rare | 1–10 | survival |
| Silvery Barbs | `asterismarcanum:silvery_barbs` | Rare | 1–5 | survival |
| Starcutter | `asterismarcanum:starcutter` | Uncommon | 1–8 | survival |
| Starfire | `asterismarcanum:starfire` | Common | 1–10 | survival |
| Star Swarm | `asterismarcanum:star_swarm` | Common | 1–10 | survival |
| Summon Lunar Moth | `asterismarcanum:summon_lunar_moths` | Rare | 1 | survival |
| Astral Gateway | `asterismarcanum:astral_gateway` | Legendary | 1 | **creative-only / unfinished** |

`TrailblazeSpell` existe no source, mas seu registration está comentado. Portanto não integra o runtime 0.1.0 e não entra na contagem.

## Escola Astral

`asterismarcanum:astral` é uma `SchoolType` real com:

- atributo próprio de Astral Spell Power;
- atributo próprio de Astral Magic Resist;
- damage type Astral próprio;
- sound próprio;
- tag de focus própria.

O construtor usado mantém os defaults de Iron's: `requiresLearning=false` e `allowLooting=true` para a escola.

## Obtenção

O Astromancer possui loot table nativa que gera um `irons_spellbooks:scroll` com `randomize_spell` e filtro `school: asterismarcanum:astral`, quality 0.25–0.85. Essa é uma fonte concreta de Astral Scrolls.

Os `DefaultConfig` dos 10 spells survival não desabilitam crafting; no Iron's atual, `allowCrafting` default é `true`. Config/datapacks do pack continuam podendo alterar a disponibilidade efetiva.

O Astrolabe é um SpellBook de 12 slots com +200 Max Mana, +20% Astral Spell Power e +5% Mana Regen. A receita usa Clock, Mithril Ingot, Tarnished Crown e Chains.

## Regra de integração Black Arcana

**Provider-native first.** Projectiles, beams, summons, teleport anchors, damage cancellation e targeting pertencem a Asterism/Iron's. Black Arcana pode observar eventos para progressão/perks, mas não deve recriar settlement, reaplicar dano ou manter ownership paralelo.

Ver `TECHNICAL-AUDIT.md` para divergências de source e gates de QA.