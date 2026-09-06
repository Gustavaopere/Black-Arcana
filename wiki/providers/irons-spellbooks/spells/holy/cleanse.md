# Cleanse — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:cleanse`
- **Escola:** Holy
- **Raridade:** Epic
- **Max level:** 1
- **Função:** purificação de efeitos nocivos em aliados

## Custo e casting
- **Mana:** 100
- **Cooldown:** 60 s
- **Cast time:** 60 ticks
- **Cast type:** Long
- **Raio:** 3 blocos

## Efeito
No cast, encontra living entities na caixa 6×6×6 centrada no caster. Para entidades que `Utils.shouldHealEntity` considera aliadas/elegíveis:

1. lê efeitos ativos;
2. filtra `MobEffectCategory.HARMFUL`;
3. preserva efeitos com tag `ModTags.CLEANSE_IMMUNE`;
4. remove os demais efeitos nocivos elegíveis;
5. emite partículas de cleanse.

## VFX/animação
- pre-cast cria `TargetedAreaEntity` de raio 3;
- cast start: `CAST_KNEELING_PRAYER`;
- finish: `SELF_CAST_TWO_HANDS`.

## Deduplicação
Bloqueia purificação Holy/Divine genérica. Exorcismo continua potencialmente distinto apenas se remover **possession/demon/spirit/curse semantics** específicas, não qualquer efeito harmful indiscriminadamente.
