# Hematite Trishula

- ID: `legendary_spellbooks:hematite_trishula`
- School: Blood
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 30 s
- Cast-time field: 60 ticks
- Mana neutral: 200 / 250 / 300
- Spell power neutral: 20 / 30 / 40
- UI damage field: `spellPower / 2` → 10 / 15 / 20 antes dos multiplicadores aplicáveis
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Carrega e arremessa uma trishula/soul trident própria do addon. A entidade projectile e o pipeline de Blood do provider são autoridade do impacto, efeitos e damage source; a página não converte o campo de UI em uma segunda aplicação de dano.

## Acquisition

Pool do Possessed Paladin: níveis 1–3, weight 10. Crafting não é desabilitado no config da spell.

## Regra para o Black Arcana

Não adicionar segundo projectile hit, Blood proc ou dano calculado a partir do mesmo `spellPower`.

## Source

`HematiteTrishulaSpell.java`, `SpellSoulTridentEntity.java` @ source pin 0.3.2.
