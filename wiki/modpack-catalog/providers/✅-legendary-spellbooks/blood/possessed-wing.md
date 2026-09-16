# Possessed Wings

- ID: `legendary_spellbooks:possessed_wing`
- School: Blood
- Levels: 1–2
- Min rarity: Legendary
- Cooldown: 240 s
- Cast-time field: 20 ticks
- Mana neutral: 250 / 275
- Effect duration: 400 / 800 ticks = 20 / 40 s
- Effect amplifier: 0 / 1
- Movement Speed: +10% total while the effect is active
- Step Height: +0.25 while active
- Jump handler: adds `0.25 × amplifier` vertical motion; therefore +0 at level 1 and +0.25 at level 2
- Direct-hit rider: attacks by the affected living caster apply Legendary Monsters `Soul Fracture` through the provider handler
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Aplica `POSSESSED_WING_EFFECT` com nível convertido para amplifier `level-1`. `PossessedWingEffect` owns the movement/step modifiers; `PossessedWingHandler` owns the direct-damage Soul Fracture rider and jump impulse.

A localização/visual do provider representa as asas do Lost Paladin, mas o catálogo técnico não infere uma segunda mecânica de voo quando o boundary observado nestes handlers não a demonstra.

## Acquisition

Pool do Possessed Paladin: níveis 1–2, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não aplicar Soul Fracture por um segundo evento, não somar outro jump impulse e não duplicar modifiers de movimento/step height.

## Source

`PossessedWingSpell.java`, `PossessedWingEffect.java`, `PossessedWingHandler.java` @ source pin 0.3.2.
