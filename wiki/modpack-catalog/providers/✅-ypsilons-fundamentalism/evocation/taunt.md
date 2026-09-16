# Taunt

- ID: `ypfundamentals:taunt`
- escola: Evocation
- rarity: Epic
- níveis: 1–4
- cast: LONG, 3 / 2.5 / 2 / 1.5 s
- mana: 50 / 55 / 60 / 65
- cooldown: 20 s
- target range: 24
- dano: nenhum

## Efeito

Se target é `Mob`, server-side executa `mob.setTarget(caster)`. Se target é `ServerPlayer`, envia `LookAtEntityPacket` para fazê-lo olhar para o caster e toca roar; não converte player em AI target.

## Obtenção

Pipeline padrão permitido; fonte concreta: **NÃO VERIFICADO**.

## Authority / dedup

Não manter aggro loop paralelo. O `setTarget` provider-native e o packet player-facing são o settlement do cast. PvP/input acceptance visual deve ser validado em cliente real.