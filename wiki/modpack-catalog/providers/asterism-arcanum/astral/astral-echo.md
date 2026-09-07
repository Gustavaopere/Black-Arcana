# Astral Echo

- ID: `asterismarcanum:astral_echo`
- escola: Astral
- rarity: Rare
- níveis: 1–8
- cast: INSTANT
- mana: 15 / 20 / 25 / 30 / 35 / 40 / 45 / 50
- cooldown: 12 s
- neutral spell power: 4–11

## Efeito

Teleporta o caster para frente e deixa no ponto de origem uma `StarcutterEntity` marcada como `astral_echo_entity`. A distância usa `9 + softCap(entityPowerMultiplier) * level * 3.5` e o destino passa pelo pipeline de teleport de Iron's, incluindo fallback de localização válida.

O caster é desmontado antes do teleport e tem fall distance resetada.

A sombra não é apenas VFX: quando recebe anti-magic, a entidade tenta teleportar o owner de volta para a posição do echo e então expira.

## Obtenção

Participa da escola Astral lootável. Fonte concreta: pool de Astral Scroll do Astromancer (`randomize_spell`, quality 0.25–0.85). Crafting continua sujeito à configuração efetiva do Iron's/pack.

## Authority e dedup

Authority = Iron's teleport pipeline + echo entity. Não implementar segundo return-anchor, segundo teleport ou segunda cobrança de mana.

## QA

Validar obstáculos,跨-dimension/portal interactions e anti-magic com player montado. Falhas devem manter comportamento provider-native.