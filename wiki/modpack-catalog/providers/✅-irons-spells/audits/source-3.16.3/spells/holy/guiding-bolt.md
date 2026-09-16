# Guiding Bolt — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:guiding_bolt`
- **Escola:** Holy
- **Raridade:** Common
- **Max level:** 10
- **Função:** projétil ofensivo Holy

## Custo e casting
- **Mana base:** 20
- **Mana/level:** +5
- **Cooldown:** 8 s
- **Cast:** Instant
- **Spell power base:** 6
- **Spell power/level:** +1

## Efeito
Cria `GuidingBoltProjectile` na altura dos olhos do caster, dispara na direção de visão e configura:

`damage = getSpellPower(level, caster) * 0.5`

O tooltip também declara efeito com duração de 25 s; a semântica detalhada pós-impacto pertence ao projectile/effect do provider e deve ser extraída antes de documentar qualquer debuff adicional.

## Deduplicação
Bloqueia novo bolt/rajada Divine/Holy genérico.
