# Heal — Iron's Spells 'n Spellbooks

## Estado

`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:heal`
- **Escola:** Holy
- **Raridade:** Uncommon
- **Max level:** 8
- **Função:** self-heal instantâneo

## Custo e casting
- **Mana base:** 30
- **Mana/level:** +15
- **Cooldown:** 30 s
- **Cast:** Instant
- **Spell power base:** 5
- **Spell power/level:** +1

## Efeito
`healAmount = getSpellPower(level, caster)`.

Antes de `entity.heal`, publica `SpellHealEvent(caster, caster, healAmount, HOLY)`. O evento é um hook relevante para RPG/Black Arcana e deve ser preferido a inferir cura por diferença de HP quando causalidade do provider for necessária.

## VFX/animação
- círculo de 16 partículas `HEART` ao redor do caster;
- animação `SELF_CAST_ANIMATION`.

## Deduplicação
Bloqueia qualquer nova cura Divine/Holy cuja única semântica seja curar imediatamente o próprio caster.
