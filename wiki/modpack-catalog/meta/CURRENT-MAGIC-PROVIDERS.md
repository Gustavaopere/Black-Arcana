# Inventário atual de providers mágicos

## Estado

`AUDITORIA EM ANDAMENTO — base instalada 2026-09-06`

A autoridade de presença é a `modlist.txt` atual do pack, com 607 entradas top-level. O guia mágico anterior catalogava 94 JARs/providers relevantes; todos esses 94 continuam presentes, mas o guia histórico não é autoridade de versão quando divergir da modlist atual.

## Deltas de versão confirmados desde o guia anterior

| Provider | Guia anterior | Modlist atual |
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

## Entradas novas/infraestrutura a auditar após o snapshot antigo

A modlist de 607 entradas contém itens que precisam ser incorporados ao guia e classificados, incluindo infraestrutura de scripting/integração e apresentação. Exemplos já detectados na reconciliação local incluem Iron's Spellbooks KubeJS, KubeJS Ars Nouveau, Dynamic Resource Bars, compat visual de Iron's e Soul Fire'd. A presença não implica automaticamente que cada um fornece spells.

## Regra de completude

A Wiki só poderá declarar `CATÁLOGO MÁGICO COMPLETO` quando:

- todos os JARs mágicos/relacionados da modlist atual tiverem classificação;
- todo `SPELL_PROVIDER` tiver inventário individual ou regra explícita de composição;
- todo spell tiver assinatura semântica para deduplicação;
- versão/JAR/mod ID estiverem reconciliados com a modlist atual;
- aquisição, custo, dano/efeito, cooldown e scaling forem extraídos do provider/runtime/config, não inferidos;
- sobreposições forem resolvidas por provider-native first;
- novos spells Black Arcana tiverem justificativa de delta mecânico real.
