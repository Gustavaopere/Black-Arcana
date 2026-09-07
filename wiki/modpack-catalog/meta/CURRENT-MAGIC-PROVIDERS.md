# Inventário atual de providers mágicos

## Estado

`AUDITORIA EM ANDAMENTO — autoridade física 2026-09-07`

A autoridade de presença/JAR/runtime é a modlist física atual do pack, com **612 entradas top-level incluindo NeoForge**. O guia mágico reconciliado em 2026-09-07 cobre **103 referências mágicas/cross-domain**. Capítulos e tabelas históricas abaixo continuam úteis para rastrear deltas, mas não prevalecem sobre o snapshot físico atual.

## Freshness 2026-09-07

Updates mágicos confirmados no snapshot atual incluem:

- Apotheosis `8.7.0 → 8.8.0`;
- Ars 'n' Spells `3.2.4 → 3.3.0`;
- GTBC's SpellLib `2.1.0 → 2.2.0` (`2.2.0-1.21.1` no runtime);
- Vampirism `1.10.12 → 1.10.13`.

Novos módulos mágicos/cross-domain incorporados ao recorte atual incluem:

- `ironsable-wind-1.0.0.jar` — bridge Wind's Spellbooks ↔ IronSable/Sable; compatibilidade física, não nova escola;
- `morerelics-1.7.7-1.21.1.jar` — decisão curatorial `Manter`, porém contracts provider-specific permanecem fail-closed até compatibilidade real com Relics `0.12.8` ser comprovada.

A presença/update de um JAR não revalida automaticamente hook, API ou compatibilidade já assumidos por auditorias anteriores.

## Delta histórico do snapshot 2026-09-06

O snapshot anterior continha 607 entradas top-level. O guia mágico anterior catalogava 94 JARs/providers relevantes; todos esses 94 continuavam presentes naquele checkpoint, mas o guia histórico nunca foi autoridade de versão quando divergente da modlist física.

| Provider | Guia anterior | Snapshot 2026-09-06 |
|---|---:|---:|
| Ace's Spell Utils | 1.2.7.1 | 1.2.7.2 |
| Apothic Enchanting | 1.6.1 | 1.6.2 |
| Ars 'n' Spells | 3.2.2 | 3.2.4 |
| Cataclysm: Spellbooks | 1.1.12 | 1.1.13 |
| Discerning The Eldritch | 1.4.3 | 1.4.4 |
| Iron's Spells: Recolor | 1.2.5 | 1.3.2 |
| Monsters & Spellbooks | 0.0.16.2 / metadata histórico 0.0.14 | 0.0.16.3 |
| Starbunclemania | 1.5.7 | 1.5.8 |

## Classificação obrigatória

Cada JAR mágico deve ser classificado antes da extração spell-by-spell:

1. `SPELL_PROVIDER` — possui spells/glyphs/poderes jogáveis que precisam de catálogo individual.
2. `RITUAL_RESOURCE_PROVIDER` — fornece ritos, recursos, fluidos, espíritos, toxinas, plantas, altares ou progressão mágica reutilizável.
3. `BRIDGE_COMPAT` — integra providers; não deve ser contado como escola paralela salvo se realmente adicionar spell próprio.
4. `LIBRARY_INFRA` — biblioteca/API/VFX/UI; documentar capabilities, não inventar spells.
5. `GEAR_LOOT_SUPPORT` — gear, loot ou atributos mágicos sem catálogo próprio de spells.
6. `MIXED` — contém mais de uma das categorias; decompor por feature.

## Providers prioritários para deduplicação

### Iron's Spells e grandes addons

- Iron's Spells 'n Spellbooks;
- Cataclysm: Spellbooks;
- Monsters & Spellbooks;
- T.O Magic n' Extras;
- Hazen N Stuff;
- ISS: Magic From The East;
- Asterism Arcanum;
- Leyline Spellbooks;
- Paladin Spells;
- Somake;
- Discerning The Eldritch;
- Dreamless Spells;
- Fire's Ender Expansion;
- GTBC's Geomancy Plus;
- Farmer's Spell 'n Spellbooks;
- Apprentice's Codex;
- demais addons Iron's presentes na modlist.

### Ars Nouveau

Ars Nouveau e seus addons devem ser catalogados em nível de glyph/form/augment e também em combinações canônicas somente quando o pack tratar a combinação como poder nomeado. Não criar uma página para cada permutação possível.

### Sistemas externos de magia/ritual/recurso

- Goety;
- Malum;
- Eidolon: Repraised;
- Hexalia;
- Toxony;
- Vampirism/Bloodlines e bridges mágicas;
- demais providers ocultistas/alquímicos presentes.

## Checkpoint Apprentice's Codex — Phase 2L

`apprenticecodex` está source-catalogado contra o artefato instalado `0.9.7.1` e o pin exato `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`:

- 83/83 spells individualizados;
- 9 escolas canônicas do Iron's;
- School Affinity auditado;
- registries de suporte auditados;
- acquisition/learning auditados;
- compat packages reconciliados com a modlist física;
- runtime QA integral do pack ainda pendente.

A cobertura source-level não converte o addon em authority de Black Arcana nem em provider de Mastery do RPG Skill Tree.

## Regra de completude

A Wiki só poderá declarar `CATÁLOGO MÁGICO COMPLETO` quando:

- todos os JARs mágicos/relacionados da modlist atual tiverem classificação;
- todo `SPELL_PROVIDER` tiver inventário individual ou regra explícita de composição;
- todo spell tiver assinatura semântica para deduplicação;
- versão/JAR/mod ID estiverem reconciliados com a modlist atual;
- aquisição, custo, dano/efeito, cooldown e scaling forem extraídos do provider/runtime/config, não inferidos;
- sobreposições forem resolvidas por provider-native first;
- novos spells Black Arcana tiverem justificativa de delta mecânico real.
