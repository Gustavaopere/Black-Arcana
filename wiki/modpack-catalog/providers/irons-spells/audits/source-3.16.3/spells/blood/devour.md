# Devour — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:devour`
- **Escola:** Blood
- **Raridade:** Uncommon
- **Max level:** 10
- **Função:** ataque dirigido com lifesteal e bônus ligado à morte

## Custo atual
- **Mana base:** 25
- **Mana/level:** +4
- **Cooldown:** 20 s
- **Cast:** Instant
- **Target:** 9 blocos
- **Spell power base:** 6
- **Spell power/level:** +1

## Efeito
Cria `DevourJaw` sobre o alvo:
- `damage = spellPower`;
- damage source: **15% lifesteal**;
- `hpBonus = 2 * floor(spellPower * 0.25)`;
- `vigorLevel = hpBonus/2 - 1` é passado à entidade do spell.

A semântica exata do bônus de HP após kill pertence ao runtime `DevourJaw` e deve ser auditada antes de afirmar duração/persistência final.

## Migração Blood
Trocar mana por sangue não altera o damage/lifesteal/kill contract do provider.
