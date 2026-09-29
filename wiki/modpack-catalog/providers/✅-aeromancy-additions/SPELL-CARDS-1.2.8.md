# SnackPirate's Aeromancy Additions 1.2.8 — fichas canônicas de spells

Este índice materializa as **10 identidades de spell ativamente registradas** fechadas pelo source pin exato `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`.

O provider permanece **✅ catalogado / COUNTED_SOURCE_PINNED 10 / +10 strict**. Esta materialização não altera o contador global nem converte source pin em equivalência binária com o JAR físico.

## Wind spells — 10

- [Wind Charge](spells/wind-charge.md) — `aero_additions:wind_charge`
- [Updraft](spells/updraft.md) — `aero_additions:updraft`
- [Airstep](spells/airstep.md) — `aero_additions:airstep`
- [Asphyxiate](spells/asphyxiate.md) — `aero_additions:asphyxiate`
- [Feather Fall](spells/feather-fall.md) — `aero_additions:feather_fall`
- [Wind Shield](spells/wind-shield.md) — `aero_additions:wind_shield`
- [Airblast](spells/airblast.md) — `aero_additions:airblast`
- [Wind Blade](spells/wind-blade.md) — `aero_additions:wind_blade`
- [Flush](spells/flush.md) — `aero_additions:flush`
- [Dash](spells/dash.md) — `aero_additions:dash`

## Registry authority

`AASpells` registra exatamente os dez objetos acima através do `DeferredRegister<AbstractSpell>` ligado ao Iron's `SpellRegistry`. O mod registra esse provider registry diretamente no event bus.

Não foi encontrada branch/config provider-side que condicione a criação ou remoção desses dez registros.

## Exclusões

Os seguintes registros aparecem comentados no source pin e contribuem **+0**:

- Tornado;
- Thunderclap;
- Summon Breeze;
- Telelink;
- Shapeshift.

Classes, effects, entities, equipment e itens de suporte também não criam identidades adicionais quando apenas implementam, suportam ou dão acesso aos dez spells registrados.

## Authority boundary

Aeromancy Additions é authority para as dez identidades Wind e seus efeitos provider-specific. Iron's continua authority para casting, mana, cooldown, host registry e Scroll Forge.

Fontes canônicas: [EXACT-1.2.8-SPELL-INVENTORY.md](EXACT-1.2.8-SPELL-INVENTORY.md) e [README.md](README.md).
