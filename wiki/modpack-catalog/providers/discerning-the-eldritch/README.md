# Discerning The Eldritch — provider canônico

Status: `INSTALLED 1.4.4-1.21 / SOURCE-PINNED / 22 REGISTERED SPELLS / CATALOG IN PROGRESS`

- **JAR do pack:** `discerning_the_eldritch-1.4.4-1.21.jar`
- **Mod ID:** `discerning_the_eldritch`
- **Version authority:** modlist atual + upstream branch `1.21`
- **Source pin auditado:** `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`
- **Upstream `gradle.properties`:** `mod_version=1.4.4-1.21`; branch 1.21 atualizada em 2026-09-05.
- **Casting authority:** Iron's Spells 'n Spellbooks.

## Correção da contagem antiga

A página pública histórica dizia “15 spells” e enumerava apenas 14. O **registry exato da versão 1.4.4** resolve a discrepância: `SpellRegistries` registra **22 `AbstractSpell`** ativos.

| Classificação real | Quantidade |
|---|---:|
| Eldritch | 9 |
| Blood | 1 |
| Evocation | 2 |
| Fire | 2 |
| Holy | 1 |
| Ice | 2 |
| Ritual (`discerning_the_eldritch:ritual`) | 5 |
| **Total registrado** | **22** |

Comentários de ideias futuras no registry (Meteorology, Apocalypse, Eternal Chains, Malevolent Maelstrom etc.) **não são registrations** e não entram no catálogo ativo.

## Escola Ritual

O addon registra uma escola própria `discerning_the_eldritch:ritual`, com focus tag, Ritual Power, Ritual Resist, targeting color e Ritual damage type próprios. `AbstractRitualSpell` estabelece gates comuns:

- `allowCrafting=false` e `canBeCraftedBy=false`;
- rituais complexos não entram em loot normal;
- super-complexos falham via `SPELLBOOK` e `SWORD`;
- complexos não-super falham via `SPELLBOOK`;
- cast de ritual é não-interruptível pelo contrato base.

Cada ritual preserva overrides próprios de `isComplex`/`isSuperComplex`.

## Inventário exato 1.4.4

### Eldritch — 9

`silence`, `conjure_forsaken_aid`, `esoteric_edge`, `conjure_gaoler`, `otherworldly_presence`, `mend_flesh`, `rift_walker`, `abracadabra`, `esoteric_strike`.

### Blood — 1

`vein_ripper`.

### Evocation — 2

`boogie_woogie`, `guardians_gaze`.

### Fire — 2

`soul_slice`, `soul_set_ablaze`.

### Holy — 1

`exorcism`.

### Ice — 2

`glacial_edge`, `crystalline_carver`. A documentação pública usa “Glacial Cleave”; o registry/source real é `glacial_edge` / `GlacialEdgeSpell`.

### Ritual — 5

`call_ascended_one`, `blades_of_rancor`, `zealous_harbinger`, `ravenous_revenant`, `libras_judgement`.

## Sistemas provider-native relevantes

- `SpellPreCastEvent` cancela casts de jogadores com `SILENCE_POTION_EFFECT`.
- Casts Eldritch incrementam Insanity somente quando o sistema opcional está habilitado; default upstream é `false`, max default 15.
- `METAPHYSICAL_POTION_EFFECT` também cancela novos casts pelo server event.
- Mend Flesh possui heal inicial e efeito reativo; lifesteal-on-hit e heal-on-XP são configuráveis, ambos default `true`.
- Abracadabra possui damage cap configurável (default habilitado, base cap 80) e bloqueio de efeitos harmful configurável (default habilitado), respeitando `BYPASS_ABRACADABRA`.
- Summons usam `SpellSummonEvent`/`SummonManager` quando apropriado; bridges não devem duplicar lifecycle.

## Deduplicação imediata

Este provider já ocupa: hard anti-casting; damage-cap defense; harmful-effect prevention; neutral/metaphysical teleport state; transposition; Eldritch weapon-scaled slashes/punches; controlled and feral Eldritch summons; Blood lifesteal dash/cleave; Soul Fire stack-spending attacks; Insanity cleanse; Frostbite combo; boss ritual summon; Ritual homing blades; predator/prey hunting state; health-threshold judgement.

Black Arcana não deve reproduzir esses contracts apenas alterando nome/VFX.

## Regra de evidência

Valores abaixo são extraídos do branch 1.21 pinado. Quando comportamento está dentro de projectile/entity/event não auditado diretamente, a ficha marca `NÃO VERIFICADO` e mantém a entity/effect do provider como authority. Bugs estáticos detectados são QA blockers, não correções silenciosas.
