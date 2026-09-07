# Dullard

- ID: `dreamless_spells:dullard`
- escola: Empty (`dreamless_spells:empty`)
- rarity: Legendary
- níveis: 1–3
- cast: LONG
- cast time base: 30 ticks = 1.5 s
- mana: 0
- cooldown: 180 s
- target range: 32
- target-area visual: raio 3
- neutral spell power: 5 / 10 / 15

## Gate

Exige `dreamless_spells:emptied` no caster antes do cast.

## Descrição provider

`Reduces the target's spell power by 10% per level`.

## Settlement do source 1.1.9

Aplica `dreamless_spells:dullard` ao target.

O effect declara `irons_spellbooks:spell_power` com `-0.1 ADD_MULTIPLIED_TOTAL`.

Porém a spell retorna **amplifier 1 fixo** em todos os spell levels, em vez de `spellLevel - 1`.

Com o scaling padrão de MobEffect, o modifier esperado é aproximadamente -20% Spell Power para qualquer nível, se o efeito estiver ativo. Isso diverge do guide de -10% por nível.

## Divergência crítica de duração

`getUniqueInfo` mostra duração usando:

`spellPower × 10 ticks`

Com power neutro 5 / 10 / 15:

- 50 ticks = 2.5 s;
- 100 ticks = 5 s;
- 150 ticks = 7.5 s.

O settlement real chama:

`getDuration = (int)(spellPower × 0.1)`

Portanto neutralmente:

- nível 1: 0 tick;
- nível 2: 1 tick;
- nível 3: 1 tick.

Isso torna o comportamento efetivo drasticamente menor que o tooltip e pode fazer o nível 1 não produzir debuff observável.

## Obtenção

Crafting permitido por default e escola Empty lootável por default. Empty Gem é focus. Uso prático exige `Emptied`; ver `PROGRESSION.md` para o blocker da Empty Rune.

## Authority / dedup

Authority = `DSSEffects.DULLARD_EFFECT`. Não criar debuff paralelo de Spell Power para “compensar” a duração/escala aparentemente quebrada; qualquer correção exige decisão explícita de compat/provider.

## QA

- medir duração em ticks níveis 1–3;
- medir Spell Power antes/depois para confirmar amplifier 1;
- confirmar se nível 1 chega a adicionar o effect;
- testar cast em player/mob target e party/friendly semantics do targeting base.