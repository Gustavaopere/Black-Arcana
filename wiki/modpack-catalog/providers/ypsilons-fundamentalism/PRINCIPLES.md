# Os 13 Fundamental Principles

Os Principles são **categorias mecânicas**, não spells. A release 1.1.7.1 os define em `Principles.java` e gera a associação aos spells por ASM sobre o registry global.

| Principle | Categoria técnica | Passiva/default 1.1.7.1 |
|---|---|---|
| Concentratio | `createEntity` | +20 mana por nível quando ativo |
| Potentia | `usesShoot` | accuracy = clamp(0.40 + 0.03×lvl, 0..1) |
| Vitale | `usesSummon` | CDR = clamp(0.045×lvl, 0..1) |
| Locus | `usesTargeting` | range multiplier = clamp(0.40 + 0.02×lvl, 0..10) |
| Repetitio | `hasRecasts` | chance de cast/recast adicional = clamp(0.05×lvl, 0..1) |
| Apparitio | `usesTeleport` | reduz failure chance de teleporte em 2.5% do valor por nível |
| Pertinacia | `addEffects` | multiplica duração de efeitos benéficos/prejudiciais por fórmulas configuráveis |
| Expansio | `createsAoeEntities` | raio multiplier = max(0.50 + 0.05×lvl, 0) |
| Motus | `usesMobility` | +5% casting movement speed por nível |
| Perceptio | `usesRaycast` | +1.5 blocos de range por nível |
| Remedium | `usesHealing` | custo de food por healing = max(3.0 - 0.125×lvl, 0); desbloqueia Regression a partir de 5 |
| Augere | `usesPotentiation` | +0.5 dano de arma por nível; também governa Reinforcement tiers |
| Certum | `immutable` | modifica custo/mana associado ao fatigue; redução padrão 2% por nível sobre o debuff configurado |

## Progressão

- nível inicial: 0;
- máximo: 20;
- XP para próximo nível: `floor(20 + 20×1.3^level)`;
- XP fica em attachment persistente por jogador e é sincronizado ao cliente;
- spell categories são geradas em `config/fundamentalism/spell_categories.json`.

## Modificador genérico de spell power

Default: `basePrinciplePower=-0.10` e `levelAddition=+0.01` por nível. A fórmula provider-native é `base × (-0.10 + 0.01×level)` para a modificação aplicável. Subcategories podem receber metade conforme `SUBCATEGORIES_HALF=true`.

## Dominan / fatigue / spellbooks

A mesma release possui sistemas transversais adicionais:

- Dominan: default exige 4 Principles e thresholds por rarity `[0,5,8,12,15]`;
- fatigue system: ativo por padrão, stages e spell-power/mana-regen debuffs configuráveis;
- spellbook leveling: ativo por padrão; progressão por covers e restricted inscription;
- esses estados pertencem ao provider e não devem ser reimplementados por Black Arcana.

## Deduplicação

Uma perk/bridge pode observar o resultado provider-native, mas não criar XP paralelo, forçar category membership, conceder level sem hook autorizado, nem aplicar novamente as passivas após o provider já ter liquidado o cast.