# Heartstop — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:heartstop`
- **Escola:** Blood
- **Raridade:** Rare
- **Max level:** 5
- **Função:** buff/effect Blood no próprio caster

## Custo atual
- **Mana base:** 100
- **Mana/level:** +10
- **Cooldown:** 120 s
- **Cast:** Instant
- **Spell power base:** 200
- **Spell power/level:** +30

## Efeito confirmado no spell class
Aplica `MobEffectRegistry.HEARTSTOP` ao **caster**, com duração em ticks igual a `getSpellPower(level,caster)`.

O nome não autoriza interpretar que o spell mata/paralisa o coração de um inimigo. A mecânica interna de `HEARTSTOP` precisa ser auditada na classe do efeito antes de documentar seus modificadores.

## VFX
35 partículas Blood em padrão swirling + som `HEARTSTOP_CAST`.

## Migração Blood
O custo normal de mana deverá ser substituído por combustível hemático segundo a política futura, sem alterar silenciosamente a semântica do efeito.
