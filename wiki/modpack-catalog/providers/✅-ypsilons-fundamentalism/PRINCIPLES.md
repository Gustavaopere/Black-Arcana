# Os 13 Fundamental Principles

**Boundary físico 2026-10-13:** [15/15 registries estáticos do provider](EXACT-BINARY-SPELLS-1.1.7.1.md) foram certificados por [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443); os **13 Principles** são categorização/progressão provider-native, **não** spell registrations extras nem XP/Mastery que Black Arcana/RPG Skill Tree possam liquidar em paralelo. `SpellCategoriesGenerator`, `PrinciplesLevelsAttachment`, mana reinforcement, exhaustion e multiplayer seguem ⚠️ quanto a runtime/configuração.


Os Principles são **categorias mecânicas**, não spells. A release 1.1.7.1 os define em `Principles.java` e gera a associação aos spells por ASM sobre o registry global.

| Principle | Categoria técnica | Passiva/default 1.1.7.1 |
|---|---|---|
| [Concentratio](principles/concentratio.md) | `createEntity` | +20 mana por nível via MAX_MANA ADD_VALUE; flags e lifecycle próprios |
| [Potentia](principles/potentia.md) | `usesShoot` | accuracy=clamp(0,40+0,03l,0..1); direção rotacionada/normalizada quando <1; não hitbox |
| [Vitale](principles/vitale.md) | `usesSummon` | CDR=clamp(0,045l,0..1) apenas para usesSummon com getRecastCount(1,player)==2 |
| [Locus](principles/locus.md) | `usesTargeting` | multiplica finalRange por clamp(0,40+0,02l,0..10), só se bbInflation>0, após Perceptio |
| [Repetitio](principles/repetitio.md) | `hasRecasts` | chance clamp(0,05l,0..1) de +1 recast apenas se totalRecasts>2 e existente não ativo |
| [Apparitio](principles/apparitio.md) | `usesTeleport` | falha base min(90,(100/cooldownSegundosInteiro)×2); reduz proporcionalmente por clamp(0,025l,0..1) |
| [Pertinacia](principles/pertinacia.md) | `addEffects` | duração de MagicMobEffect recebido por ServerPlayer; usa nível do receptor, pula -1 |
| [Expansio](principles/expansio.md) | `createsAoeEntities` | raio ×max(0,50+0,05l,0), uma vez por AoeEntity elegível, exceto EchoingStrikeEntity; clamp host depois |
| [Motus](principles/motus.md) | `usesMobility` | +0,05l ADD_VALUE em CASTING_MOVESPEED; não multiplica diretamente velocidade final |
| [Perceptio](principles/perceptio.md) | `usesRaycast` | range=8+distânciaOriginal/5+(int)(1,5l); pode receber Locus; não apenas soma ao original |
| [Remedium](principles/remedium.md) | `usesHealing` | food/HP=max(3−0,125lCaster,0), debitado do receptor; Regression≥5; nível17 omitido no switch |
| [Augere](principles/augere.md) | `usesPotentiation` | +0,5l no retorno positivo de Utils.getWeaponDamage para Player; não é todo dano físico |
| [Certum](principles/certum.md) | `immutable` | multiplica custo immutable por 1+tabelaFatigue×(1−0,02l); preflight/evento têm guards diferentes |

## Progressão

- nível inicial: 0;
- máximo: 20;
- XP de nível n para n+1: `(int)(20 + 20×1.3^(n+1))`; primeiro 0→1 exige 46 XP. O helper recebe o nível de destino, não o atual;
- XP fica em attachment persistente por jogador e é sincronizado ao cliente;
- spell categories são geradas em `config/fundamentalism/spell_categories.json`.

## Modificador genérico de spell power

Default: `basePrinciplePower=-0.10` e `levelAddition=+0.01` por nível. O termo aditivo por categoria é `base × (-0.10 + 0.01×level)`; o retorno não é só esse termo: `PowerSpellsMixin` soma as contribuições ao poder original e aplica a razão de fatigue quando ativa. `SUBCATEGORIES_HALF=true` divide termos de usesShoot, createsAoeEntities, usesSummon e usesTargeting por dois. Flags das passivas individuais não são checadas nesse loop.

## Dominan / fatigue / spellbooks

A mesma release possui sistemas transversais adicionais:

- Dominan: default exige 4 Principles e thresholds por rarity `[0,5,8,12,15]`;
- fatigue system: ativo por padrão, stages e spell-power/mana-regen debuffs configuráveis;
- spellbook leveling: ativo por padrão; progressão por covers e restricted inscription;
- esses estados pertencem ao provider e não devem ser reimplementados por Black Arcana.

## Deduplicação

Uma perk/bridge pode observar o resultado provider-native, mas não criar XP paralelo, forçar category membership, conceder level sem hook autorizado, nem aplicar novamente as passivas após o provider já ter liquidado o cast.

## Reauditoria por campo — 22/10/2026

[13/13 fichas de sistemas/passivas](principles/README.md), com valores/defaults, consumidores, fases, gates, mutabilidade e testes pendentes. **+0 magias** e sem completude técnica/QA inferida. O quadro acima corrige os resumos de range, cooldown, recast, nível do destinatário e XP com base no mesmo source pin. Config efetiva e compatibilidade 3.16.2→3.16.3 continuam PENDING.
