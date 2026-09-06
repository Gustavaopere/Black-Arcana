# Divine Smite — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:divine_smite`
- **Escola:** Holy
- **Raridade:** Common
- **Max level:** 5
- **Função:** smite melee/AoE Holy

## Custo e casting
- **Mana base:** 30
- **Mana/level:** +15
- **Cooldown:** 15 s
- **Cast time:** 16 ticks
- **Cast type:** Long
- **Interrupção:** não pode ser interrompido pelo método do spell
- **Cast-time scaling:** deliberadamente ignorado para preservar timing da animação melee
- **Spell power base:** 8
- **Spell power/level:** +3

## Targeting e efeito
- avanço/raycast curto: ~1.7 bloco;
- raio de impacto: 2.2 blocos;
- exige line of sight para cada entidade atingida.

`damage = HolySpellPower + weaponDamage + SmiteEnchantmentContribution`

O spell aplica efeitos pós-ataque de enchantment quando o dano confirma.

## VFX/animação
- blastwave na cor Holy;
- 50 electric sparks;
- camera shake;
- sons próprios de windup/cast;
- animação `OVERHEAD_MELEE_SWING_ANIMATION`.

## Deduplicação
Bloqueia novo “golpe divino” melee genérico. Julgamentos Celestiais precisam de alvo/condição/recurso/mecânica diferentes.
