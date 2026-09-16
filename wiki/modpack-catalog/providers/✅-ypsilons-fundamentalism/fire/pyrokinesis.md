# Pyrokinesis

- ID: `ypfundamentals:pyrokinesis`
- escola: Fire
- rarity: Rare
- níveis: 1–5
- cast: CONTINUOUS, 1 / 2 / 3 / 4 / 5 s
- mana: 10 / 12 / 14 / 16 / 18
- cooldown: 5 s
- área: raio 3 ao redor do caster
- dano próprio: nenhum dano direto

## Efeito

Durante server cast ticks limpa fogo do caster e redireciona projectiles dentro de 3 blocos para o look vector do caster, reassumindo ownership quando elegível: fire-named `AbstractMagicProjectile`, flaming arrows, Fireballs e Firework Rockets.

## Obtenção

Pipeline padrão permitido; fonte exata: **NÃO VERIFICADO**.

## Authority / anti-abuso

O próprio loop provider-native é a única authority de reflexão. Uma bridge não deve re-refletir o mesmo projectile nem reatribuir owner uma segunda vez.

## QA

A identificação de magic projectile usa class-name contendo `FIRE`; projectiles semanticamente Fire sem esse nome podem não ser reconhecidos.