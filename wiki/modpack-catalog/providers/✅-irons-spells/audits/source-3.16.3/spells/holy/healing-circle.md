# Healing Circle — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:healing_circle`
- **Escola:** Holy
- **Raridade:** Common
- **Max level:** 10
- **Função:** área persistente de cura

## Custo e casting
- **Mana base:** 40
- **Mana/level:** +10
- **Cooldown:** 25 s
- **Cast time:** 20 ticks
- **Cast type:** Long
- **Spell power base:** 2
- **Spell power/level:** +1
- **Targeting:** entidade ou ponto até 32 blocos

## Efeito
Cria `HealingAoe` circular no alvo/ponto escolhido:
- **raio:** 5 blocos;
- **duração:** 200 ticks (10 s);
- **healing value:** `getSpellPower * 0.25` por settlement definido pela entidade do provider.

Também cria `TargetedAreaEntity` visual vermelho com fade.

## Deduplicação
Bloqueia círculo/área de cura Holy/Divine genérico. Uma futura zona consagrada precisa ter semântica adicional — exorcismo, ward, law, anti-infernal etc. — e não apenas outra healing AoE.
