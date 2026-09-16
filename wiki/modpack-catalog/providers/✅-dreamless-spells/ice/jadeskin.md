# Jadeskin

- ID: `dreamless_spells:jadeskin`
- escola: Ice (`irons_spellbooks:ice`)
- rarity: Legendary
- níveis: 1–3
- cast: INSTANT
- mana neutra: 150 / 230 / 310
- cooldown: 60 s
- neutral spell power: 5 / 10 / 15
- duração neutra: 200 / 400 / 600 ticks = 10 / 20 / 30 s

## Descrição provider

O lang 1.1.9 descreve Jadeskin como um aumento forte de Ice Spell Power, Attack Speed e Attack Damage.

## Efeito

No cast, aplica `dreamless_spells:jadeskin` ao próprio caster com:

- duração = `spellPower × 40` ticks;
- amplifier = `spellLevel - 1`.

O MobEffect declara três attribute modifiers:

- Attack Damage: `+0.5 ADD_MULTIPLIED_BASE`;
- Ice Spell Power: `+0.12 ADD_MULTIPLIED_BASE`;
- Attack Speed: `+1.0 ADD_VALUE`.

Com o scaling padrão de MobEffect por amplifier, os modifiers nominais por nível são:

| Nível | Attack Damage | Ice Spell Power | Attack Speed |
|---:|---:|---:|---:|
| 1 | +50% base | +12% base | +1 |
| 2 | +100% base | +24% base | +2 |
| 3 | +150% base | +36% base | +3 |

Os valores finais dependem da ordem/combinação com outros attribute modifiers do pack.

## Obtenção

Jadeskin usa a escola Ice do Iron's, não Empty. Não exige `Emptied`.

Seu `DefaultConfig` mantém `allowCrafting=true`. Como Ice é escola lootável e Jadeskin não sobrescreve `allowLooting`, ela é elegível aos pipelines padrão que selecionam spells Ice e a pools genéricas de spells do Iron's.

Fonte garantida criada pelo próprio Dreamless: **NÃO VERIFICADO**.

## Authority / dedup

Authority = `DSSEffects.JADESKIN_EFFECT` aplicado pelo `onCast` da spell. Não aplicar modifiers equivalentes uma segunda vez por perk/bridge.

## QA

- confirmar duração 10/20/30 s com caster neutro;
- medir stacking com outros boosts de Attack Damage/Ice Spell Power;
- confirmar aquisição por Scroll Forge e loot Ice no pack efetivo.