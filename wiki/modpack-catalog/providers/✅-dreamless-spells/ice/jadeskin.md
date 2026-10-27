# Jadeskin

**Status do registro:** ✅ `COUNTED_EXACT` para ID estático no JAR físico — [evidência](../EXACT-BINARY-SPELLS-1.1.9.md) ([run #38302406303](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38302406303)). As fórmulas, efeitos, gate, custos e duração abaixo continuam source-pinned, sem QA física de execução/Survival.

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

## Atualização de ABI exata 1.1.9 — 27/10/2026

A [auditoria do JAR físico dreamless_spells-1.1.9.jar](../EXACT-1.1.9-SPELL-CAST-AND-COUNTERSPELL-ABI-20261027.md) (SHA-1 `d51960bfb8af1aafa5d716ef9a48c3135f36b956`, run [#40499150605](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40499150605)) confirmou estas relações de código **sem importar corpos de método**:

O classfile `JadeskinSpell.onCast` referencia `DSSEffects.JADESKIN_EFFECT`, `LivingEntity.addEffect` e `AbstractSpell.onCast`. Isso confirma a superfície binária de aplicação de efeito, mas não os multiplicadores, duração em ticks, acúmulo de atributos nem sucesso de casts em servidor; os valores anteriores continuam baseados somente na fonte release-aligned.

**Status:** `EXACT_BINARY_METHOD_REFERENCES` (estático) · `SOURCE_ALIGNED_NUMBERS_NOT_BINARY_PROVEN` · `physical_qa=NOT_TESTED` · `mutating_hook=NOT_VERIFIED`. Nenhum registro novo, certificação de perk, custo adicional ou segundo pipeline Black Arcana. O provider permanece autoridade do efeito, e Iron's da transação de casting.
