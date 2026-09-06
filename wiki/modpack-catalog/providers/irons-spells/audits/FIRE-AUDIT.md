# Iron's Spells 3.16.3 — Auditoria Fire

## Estado

`13/13 SPELLS REGISTRADOS AUDITADOS NO SOURCE / PÁGINAS INDIVIDUAIS EM CRIAÇÃO`

O registry oficial 3.16.3 possui 13 spells Fire ativos. `SoulfireRaySpell.java` existe no source e aparece em busca por `FIRE_RESOURCE`, mas **não está registrado no SpellRegistry atual**; portanto não entra como spell ativo do provider.

| Spell | Raridade | Max Lv | Mana base | Mana/Lv | CD | Cast | Núcleo mecânico |
|---|---:|---:|---:|---:|---:|---|---|
| Blaze Storm | Common | 10 | 5 | 1 | 20s | Continuous | small fireballs periódicas, i-frames 0 |
| Burning Dash | Common | 10 | 20 | 2 | 10s | Instant | dash/spin + fire |
| Fireball | Rare | 5 | 60 | 15 | 25s | Long 40t | explosive projectile |
| Firebolt | Common | 10 | 10 | 2 | 1s | Instant | fast projectile |
| Fire Breath | Common | 10 | 5 | 1 | 12s | Continuous 100t | cone fire |
| Magma Bomb | Uncommon | 8 | 30 | 5 | 12s | Long 20t | projectile + explosion/AoE |
| Wall of Fire | Common | 5 | 30 | 5 | 30s | Instant/recasts | multi-anchor persistent wall |
| Heat Surge | Common | 6 | 50 | 10 | 45s | Long 20t | AoE Rend + burn |
| Flaming Strike | Common | 5 | 30 | 15 | 15s | Long 10t | weapon+spell melee arc |
| Scorch | Uncommon | 10 | 50 | 5 | 12s | Long 20t | targeted blast + fire field |
| Flaming Barrage | Rare | 5 | 80 | 5 | 15s | Instant/recasts | 5 cursor-homing fireballs |
| Fire Arrow | Rare | 10 | 40 | 5 | 8s | Long 20t | explosive fire arrow |
| Raise Hell | Legendary | 5 | 90 | 45 | 25s | Long 16t/recasts | repeated fire eruption AoE |

## Consequência para Magia Infernal

A futura Infernal **não pode ser uma segunda escola Fire com textura vermelha**. Os seguintes nichos já estão ocupados no Iron's base:

- bolt;
- fireball;
- breath/cone;
- explosive magma projectile;
- wall;
- dash;
- barrage;
- melee flaming strike;
- burn/rend AoE;
- persistent scorched field;
- eruption/`Raise Hell`.

Além disso, Cataclysm: Spellbooks/Ignis já adiciona uma família infernal própria (Incineration, Infernal Strike, Hellish Blade, Bone Storm, Ashen Breath etc.).

Logo o delta da nova Arcana Infernal precisa vir de **fonte, pactos e regras**, especialmente:

1. Lava Infernal real em mB;
2. reservatório exclusivamente no Nether;
3. link caster ↔ infraestrutura infernal;
4. dano/estado `INFERNAL` somente se houver damage/effect contract próprio;
5. pactos/dívidas/tributos;
6. invocação/banimento com provider-native Goety/Eidolon/Cataclysm;
7. efeitos de território/Nether que Fire base não oferece;
8. VFX/materialidade próprios;
9. alto custo e devastação bounded.

## Raise Hell — colisão nominal e funcional importante

`irons_spellbooks:raise_hell` já é Legendary, não craftável, não lootável, possui recasts e cria `FireEruptionAoe` de raio 8. Portanto nenhum novo spell da escola Infernal deve usar “Raise Hell” ou replicar sua erupção como identidade central.

## World effects

`Scorch`, `Wall of Fire` e outros criam entities/fields do provider, não autorizam o Black Arcana a assumir mutação arbitrária de terreno. A futura Lava Infernal continua sujeita a Stage 04 World Safety e não deve usar esses spells como justificativa para bypass.

## Próximo cruzamento Infernal

- Cataclysm Spellbooks 1.1.13 — extrair JAR atual quando possível;
- Ignis Soulfires + Spellbooks;
- Goety;
- Eidolon;
- Malum/Black Flame;
- Iron's `Raise Hell`/Fire family;
- qualquer addon com demon/hellfire/soulfire.
