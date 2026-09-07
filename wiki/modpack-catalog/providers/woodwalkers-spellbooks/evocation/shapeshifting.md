# Shapeshifting

- ID: `woodwalkers_spellbooks:shapeshifting`
- Provider: Woodwalkers SpellBooks `0.3.1-BETA`
- School: Evocation (`irons_spellbooks:evocation`)
- Levels: 1–6
- Min rarity: Rare
- Cast type: LONG
- Cast time: 60 ticks
- Cooldown: 40 s
- Mana neutral: `40 / 50 / 60 / 70 / 80 / 90`
- Spell power neutral: `8 / 9 / 10 / 11 / 12 / 13`
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## O que faz

Integra o casting do Iron's ao sistema de formas do Woodwalkers. Com alvo vivo e jogador não transformado, o cast pode salvar a entidade alvo como segunda forma e transformar o jogador nela. Depois de existir uma segunda forma, o spell pode ser usado sem alvo para reutilizá-la.

A forma é aplicada por APIs do Woodwalkers (`PlayerShapeChanger`, `ShapeType`, `PlayerShape`, `PlayerDataProvider`), não por uma representação paralela do addon.

## XP para desbloquear forma

Defaults de `woodwalkers-spellbooks.toml`:

| Spell level | XP levels exigidos |
|---:|---:|
| 1 | 6 |
| 2 | 5 |
| 3 | 4 |
| 4 | 3 |
| 5 | 2 |
| 6 | 1 |

Por padrão o XP é exigido em survival e não em creative. O débito ocorre no cast com alvo usado para registrar a forma. Reutilizar a segunda forma sem alvo não debita XP novamente.

## Duração da transformação

Defaults:

| Spell level | Duração |
|---:|---:|
| 1 | 30 s |
| 2 | 45 s |
| 3 | 75 s |
| 4 | 90 s |
| 5 | 120 s |
| 6 | 240 s |

Em survival, `Infinity Spell` é `false` por padrão. Em creative, `Infinity Spell On Creative` é `true` por padrão. Quando o modo infinito não está ativo, a transformação é acompanhada pelo effect `woodwalkers_spellbooks:shapeshifter`.

## Targeting

O contrato estático possui dois valores que precisam permanecer separados até QA:

- `Utils.preCastTargetHelper(..., 16, .25f, false)` no pre-cast;
- fallback `Utils.raycastForEntity(..., 32, true, .25f)` dentro de `getTarget`.

O comportamento efetivo entre 16 e 32 blocos é um gate de runtime; Black Arcana não deve escolher um alcance arbitrariamente.

## Spellcasting enquanto transformado

Por padrão, `Spells while Transformed = false`. O addon observa `SpellPreCastEvent` no server e cancela o cast de qualquer spell enquanto `PlayerShape.getCurrentShape(player) != null`.

Essa regra pertence ao provider. Não registrar outro cancelamento equivalente no Black Arcana.

## Obtenção / aprendizado

O config da spell não desabilita crafting, e o source pin não define uma loot table/boss-scroll customizada para Shapeshifting. Isso não prova uma receita ou peso específico: a rota efetiva via crafting/loot genérico do Iron's deve ser confirmada em runtime/JEI antes de documentar detalhes de aquisição.

## Authority / anti-duplicação

- Iron's: mana, cooldown, spell level, cast lifecycle e school.
- Woodwalkers: forma atual, segunda forma, entidade transformada e shape abilities.
- Woodwalkers SpellBooks: XP gate, duration config, infinite mode e bloqueio de spellcast transformado.
- Black Arcana: não duplicar shape state, XP debit, timer/effect ou `SpellPreCastEvent` gate.

## QA

- dedicated server;
- desbloqueio com alvo e XP insuficiente/suficiente;
- débito único de XP;
- recast sem alvo;
- níveis 1–6 e duração;
- infinity survival/creative;
- cast de outros spells transformado com config false/true;
- target range 16/32;
- logout/login, death/respawn e dimension change;
- aquisição real via Iron's/JEI.

## Source

- `SpellRegistry.java`
- `ShapeshiftingSpell.java`
- `core/Shapeshifting.java`
- `core/Config.java`
- `WoodwalkersSpellBooks.java`
- `EffectRegistry.java`

Source pin: `jo-devnull/woodwalkers-spellbooks@fd52733f6ba6e00028492ba1fa945f6a851de1fd`.
