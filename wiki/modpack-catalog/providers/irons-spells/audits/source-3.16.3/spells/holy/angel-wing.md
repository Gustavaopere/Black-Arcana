# Angel Wing — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID real:** `irons_spellbooks:angel_wing`
- **Nome de classe:** `AngelWingsSpell`
- **Escola:** Holy
- **Raridade:** Legendary
- **Max level:** 5
- **Função:** voo/asas temporárias

## Custo e casting
- **Mana base:** 80
- **Mana/level:** +20
- **Cooldown:** 120 s
- **Cast:** Instant
- **Spell power base:** 10
- **Spell power/level:** +10
- **Duração:** `getSpellPower * 20` ticks

## Efeito
Aplica `MobEffectRegistry.ANGEL_WINGS` ao caster com duração derivada do spell power.

## VFX
Cria 35 partículas `WISP` em padrão swirling ao redor do caster.

## Deduplicação
Bloqueia voo/asas Divine genérico. Qualquer mobilidade celestial nova precisa de diferença mecânica real — por exemplo ascensão contextual, resgate/levitação de aliados ou traversal associado a Sanctum — e deve ser comparada também com outros mods de voo do pack.
