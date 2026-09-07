# Possessed Soul Blade

- ID: `legendary_spellbooks:possessed_soul_blade`
- School runtime: Evocation nos níveis 1–2; Blood nos níveis 3–4
- Levels: 1–4
- Min rarity: Epic
- Cooldown: 20 s
- Cast-time field: 35 ticks
- Mana neutral: 125 / 150 / 175 / 200
- Spell power neutral: 6 / 10 / 14 / 18
- Blade rings: 3 / 4 / 5 / 6
- Approx. blade count from provider formula `floor(1.5 × rings)`: 4 / 6 / 7 / 9
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

É uma spell de escola dupla real, implementada sobre `BaseDoubleSchoolSpell`. O provider muda a escola efetiva para Blood a partir do nível 3; Black Arcana não deve congelar a classificação em uma única escola nem aplicar power/resistance pelo ramo errado.

O cast cria os anéis/lâminas provider-native e conserva a resolução de dano no próprio addon/Iron's.

## Acquisition

Pool do Possessed Paladin: níveis 1–3, weight 10. O config da spell não desabilita crafting.

## Regra para o Black Arcana

Consultar a escola efetiva do spell level quando necessário. Não duplicar blades, dano ou school-power application.

## Source

`PossessedSoulBladeSpell.java`, `BaseDoubleSchoolSpell.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.
